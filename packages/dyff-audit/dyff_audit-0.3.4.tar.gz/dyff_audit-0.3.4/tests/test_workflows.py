# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import time

# mypy: disable-error-code="import-untyped"
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import pydantic
import pytest

from dyff.audit.local import mocks
from dyff.audit.local.platform import DyffLocalPlatform
from dyff.client import Client, HttpResponseError
from dyff.schema import ids
from dyff.schema.base import int32
from dyff.schema.dataset import ReplicatedItem, arrow
from dyff.schema.platform import *
from dyff.schema.requests import *


class BlurstCountScoredItem(ReplicatedItem):
    blurstCount: int32() = pydantic.Field(  # type: ignore
        description="Number of times the word 'blurst' is used in the response."
    )
    cromulent: int32() = pydantic.Field(  # type: ignore
        description="Whether the text is cromulent."
    )
    embiggen: str = pydantic.Field(description="Which man to embiggen.")


DATA_DIR = Path(__file__).parent.resolve() / "data"


@pytest.fixture(scope="session")
def dyffapi(pytestconfig, tmp_path_factory):
    """Creates a DyffLocalPlatform that is shared by all tests.

    This is needed because a workflow's dependencies must be present before we can test
    the workflow.
    """
    if pytestconfig.getoption("test_remote"):
        from dyff.client import Client

        endpoint = (
            pytestconfig.getoption("api_endpoint") or os.environ["DYFF_API_ENDPOINT"]
        )
        token = pytestconfig.getoption("api_token") or os.environ["DYFF_API_TOKEN"]
        insecure = (
            pytestconfig.getoption("api_insecure")
            or os.environ.get("DYFF_API_INSECURE") == "1"
        )
        yield Client(api_key=token, endpoint=endpoint, insecure=insecure)
    else:
        storage_root = pytestconfig.getoption("storage_root")
        if storage_root is not None:
            storage_root_path = Path(storage_root).resolve()
            yield DyffLocalPlatform(storage_root_path)
        else:
            yield DyffLocalPlatform(tmp_path_factory.mktemp("dyff"))


@pytest.fixture(scope="session")
def ctx(pytestconfig):
    """Shared dict for storing the workflow dependencies that we add incrementally as
    testing progresses."""
    d: dict[str, Any] = {"model": None}
    if pytestconfig.getoption("test_remote"):
        d.update(
            {
                "account": "test",
            }
        )
    else:
        account = ids.generate_entity_id()
        d.update(
            {
                "account": account,
                "inferenceservice": DyffModelWithID(
                    id=ids.generate_entity_id(), account=account
                ),
            }
        )
    yield d


@pytest.fixture(scope="session", autouse=True)
def cleanup(dyffapi: Client | DyffLocalPlatform, ctx, request):
    def terminate_session():
        session = ctx.get("inferencesession")
        if session:
            dyffapi.inferencesessions.delete(session.id)

    request.addfinalizer(terminate_session)


def wait_for_ready(
    dyffapi: Client | DyffLocalPlatform, session_id: str, *, timeout: timedelta
):
    then = datetime.now()
    while (datetime.now() - then) < timeout:
        if dyffapi.inferencesessions.ready(session_id):
            return
        time.sleep(10)
    raise AssertionError("timeout")


def wait_for_success(get_entity_fn, *, timeout: timedelta):
    then = datetime.now()
    while (datetime.now() - then) < timeout:
        try:
            status = get_entity_fn().status
            if is_status_success(status):
                return
            elif is_status_failure(status):
                raise AssertionError(f"failure status: {status}")
        except HttpResponseError as ex:
            if ex.status_code != 404:
                raise
        time.sleep(10)
    raise AssertionError("timeout")


@pytest.mark.datafiles(DATA_DIR)
def test_datasets_create(dyffapi: DyffLocalPlatform, ctx, datafiles):
    account = ctx["account"]
    dataset_dir = datafiles / "dataset"
    dataset = dyffapi.datasets.create_arrow_dataset(
        dataset_dir, account=account, name="dataset"
    )
    dyffapi.datasets.upload_arrow_dataset(dataset, dataset_dir)
    print(f"dataset: {dataset.id}")
    ctx["dataset"] = dataset

    wait_for_success(
        lambda: dyffapi.datasets.get(dataset.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
def test_inferenceservices_create(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("test_remote"):
        assert isinstance(dyffapi, Client)
        account = ctx["account"]

        service_request = InferenceServiceCreateRequest(
            account=account,
            name="mock-llm",
            model=None,
            runner=InferenceServiceRunner(
                kind=InferenceServiceRunnerKind.MOCK,
                resources=ModelResources(
                    storage="1Gi",
                    memory="2Gi",
                ),
            ),
            interface=InferenceInterface(
                # This is the inference endpoint for the vLLM runner
                endpoint="generate",
                # The output records should look like: {"text": "To be, or not to be"}
                outputSchema=DataSchema.make_output_schema(
                    DyffDataSchema(
                        components=["text.Text"],
                    ),
                ),
                # How to convert the input dataset into the format the runner expects
                inputPipeline=[
                    # {"text": "The question"} -> {"prompt": "The question"}
                    SchemaAdapter(
                        kind="TransformJSON",
                        configuration={"prompt": "$.text"},
                    ),
                ],
                # How to convert the runner output to match outputSchema
                outputPipeline=[
                    # {"text": ["The answer"]} -> [{"text": "The answer"}]
                    SchemaAdapter(
                        kind="ExplodeCollections",
                        configuration={"collections": ["text"]},
                    ),
                ],
            ),
        )

        inferenceservice = dyffapi.inferenceservices.create(service_request)
        print(f"inferenceservice: {inferenceservice.id}")
        ctx["inferenceservice"] = inferenceservice
    else:
        assert isinstance(dyffapi, DyffLocalPlatform)
        account = ctx["account"]
        inferenceservice = dyffapi.inferenceservices.create_mock(
            mocks.TextCompletion, account=account
        )
        print(f"inferenceservice: {inferenceservice.id}")
        ctx["inferenceservice"] = inferenceservice

    wait_for_success(
        lambda: dyffapi.inferenceservices.get(inferenceservice.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_inferenceservices_create",
    ]
)
def test_inferencesessions_create(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    service: InferenceService = ctx["inferenceservice"]

    session_request = InferenceSessionCreateRequest(
        account=account,
        inferenceService=service.id,
        useSpotPods=False,
        accelerator=service.runner.accelerator if service.runner else None,
    )
    session_and_token = dyffapi.inferencesessions.create(session_request)
    session = session_and_token.inferencesession

    print(f"inferencesession: {session.id}")
    ctx["inferencesession"] = session
    ctx["session_token"] = session_and_token.token

    wait_for_ready(dyffapi, session.id, timeout=timedelta(minutes=5))


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_inferencesessions_create",
    ]
)
def test_inferencesessions_infer(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    session: InferenceSession = ctx["inferencesession"]

    if pytestconfig.getoption("test_remote"):
        assert isinstance(dyffapi, Client)
        session_client = dyffapi.inferencesessions.client(
            session.id,
            ctx["session_token"],
            interface=session.inferenceService.interface,
        )
        response = session_client.infer({"text": "Open the pod bay doors, Hal!"})
    else:
        assert isinstance(dyffapi, DyffLocalPlatform)
        response = dyffapi.inferencesessions.infer(
            session.id, "generate", {"text": "Open the pod bay doors, Hal!"}
        )
    print(f"infer response: {response}")


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_inferenceservices_create",
    ]
)
def test_evaluations_create(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    dataset = ctx["dataset"]

    inferenceservice = ctx["inferenceservice"]
    evaluation_request = EvaluationCreateRequest(
        account=account,
        dataset=dataset.id,
        inferenceSession=EvaluationInferenceSessionRequest(
            inferenceService=inferenceservice.id,
            expires=datetime.now() + timedelta(days=1),
            replicas=1,
            useSpotPods=False,
        ),
        replications=2,
        workersPerReplica=2,
    )
    evaluation = dyffapi.evaluations.create(evaluation_request)

    print(f"evaluation: {evaluation.id}")
    ctx["evaluation"] = evaluation

    wait_for_success(
        lambda: dyffapi.evaluations.get(evaluation.id),
        timeout=timedelta(minutes=5),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_inferencesessions_create",
    ]
)
def test_evaluations_create_with_session_reference(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    dataset = ctx["dataset"]
    session = ctx["inferencesession"]

    evaluation_request = EvaluationCreateRequest(
        account=account,
        dataset=dataset.id,
        inferenceSessionReference=session.id,
        replications=2,
        workersPerReplica=2,
    )
    evaluation = dyffapi.evaluations.create(evaluation_request)
    print(f"evaluation_with_session_reference: {evaluation.id}")

    wait_for_success(
        lambda: dyffapi.evaluations.get(evaluation.id),
        timeout=timedelta(minutes=5),
    )


@pytest.mark.datafiles(DATA_DIR)
def test_evaluations_import(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    dataset = ctx["dataset"]

    if pytestconfig.getoption("test_remote"):
        pytest.skip()
    else:
        assert isinstance(dyffapi, DyffLocalPlatform)
        evaluation_request = EvaluationCreateRequest(
            account=account,
            dataset=dataset.id,
            inferenceSession=EvaluationInferenceSessionRequest(inferenceService=""),
        )
        evaluation = dyffapi.evaluations.import_data(
            datafiles / "evaluation", evaluation_request=evaluation_request
        )

    print(f"evaluation: {evaluation.id}")
    ctx["evaluation"] = evaluation


@pytest.mark.datafiles(DATA_DIR)
def test_modules_create_jupyter_notebook(dyffapi: DyffLocalPlatform, ctx, datafiles):
    account = ctx["account"]
    module_jupyter_notebook_dir = datafiles / "module_jupyter_notebook"
    module_jupyter_notebook = dyffapi.modules.create_package(
        module_jupyter_notebook_dir, account=account, name="module_jupyter_notebook"
    )
    dyffapi.modules.upload_package(module_jupyter_notebook, module_jupyter_notebook_dir)
    print(f"module_jupyter_notebook: {module_jupyter_notebook.id}")
    ctx["module_jupyter_notebook"] = module_jupyter_notebook

    wait_for_success(
        lambda: dyffapi.modules.get(module_jupyter_notebook.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
def test_modules_create_python_function(dyffapi: DyffLocalPlatform, ctx, datafiles):
    account = ctx["account"]
    module_python_function_dir = datafiles / "module_python_function"
    module_python_function = dyffapi.modules.create_package(
        module_python_function_dir, account=account, name="module_python_function"
    )
    dyffapi.modules.upload_package(module_python_function, module_python_function_dir)
    print(f"module_python_function: {module_python_function.id}")
    ctx["module_python_function"] = module_python_function

    wait_for_success(
        lambda: dyffapi.modules.get(module_python_function.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
def test_modules_create_python_rubric(dyffapi: DyffLocalPlatform, ctx, datafiles):
    account = ctx["account"]
    module_python_rubric_dir = datafiles / "module_python_rubric"
    module_python_rubric = dyffapi.modules.create_package(
        module_python_rubric_dir, account=account, name="module_python_rubric"
    )
    dyffapi.modules.upload_package(module_python_rubric, module_python_rubric_dir)
    print(f"module_python_rubric: {module_python_rubric.id}")
    ctx["module_python_rubric"] = module_python_rubric

    wait_for_success(
        lambda: dyffapi.modules.get(module_python_rubric.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.depends(
    on=[
        "test_modules_create_jupyter_notebook",
    ]
)
def test_methods_create_jupyter_notebook(dyffapi: DyffLocalPlatform, ctx):
    account = ctx["account"]
    module_jupyter_notebook = ctx["module_jupyter_notebook"]
    method_jupyter_notebook_request = MethodCreateRequest(
        name="method_notebook",
        scope=MethodScope.InferenceService,
        description="""# Markdown Description""",
        implementation=MethodImplementation(
            kind=MethodImplementationKind.JupyterNotebook,
            jupyterNotebook=MethodImplementationJupyterNotebook(
                notebookModule=module_jupyter_notebook.id,
                notebookPath="test-notebook.ipynb",
            ),
        ),
        parameters=[MethodParameter(keyword="trueName", description="His real name")],
        inputs=[
            MethodInput(kind=MethodInputKind.Measurement, keyword="cromulence"),
        ],
        output=MethodOutput(
            kind=MethodOutputKind.SafetyCase,
            safetyCase=SafetyCaseSpec(
                name="safetycase_notebook",
                description="""# Markdown Description""",
            ),
        ),
        modules=[module_jupyter_notebook.id],
        account=account,
    )
    method_jupyter_notebook = dyffapi.methods.create(method_jupyter_notebook_request)
    print(f"method_jupyter_notebook: {method_jupyter_notebook.id}")
    ctx["method_jupyter_notebook"] = method_jupyter_notebook

    wait_for_success(
        lambda: dyffapi.methods.get(method_jupyter_notebook.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.depends(
    on=[
        "test_modules_create_python_function",
    ]
)
def test_methods_create_python_function(dyffapi: DyffLocalPlatform, ctx):
    account = ctx["account"]
    module_python_function = ctx["module_python_function"]
    method_python_function_request = MethodCreateRequest(
        account=account,
        modules=[module_python_function.id],
        name="method_python_function",
        scope=MethodScope.Evaluation,
        description="""# Markdown Description""",
        implementation=MethodImplementation(
            kind=MethodImplementationKind.PythonFunction,
            pythonFunction=MethodImplementationPythonFunction(
                fullyQualifiedName="dyff.fake.method.blurst_count",
            ),
        ),
        parameters=[
            MethodParameter(keyword="embiggen", description="Who is being embiggened")
        ],
        inputs=[
            MethodInput(kind=MethodInputKind.Dataset, keyword="dataset"),
            MethodInput(kind=MethodInputKind.Evaluation, keyword="outputs"),
        ],
        output=MethodOutput(
            kind=MethodOutputKind.Measurement,
            measurement=MeasurementSpec(
                name="example.dyff.io/blurst-count",
                description="The number of times the word 'blurst' appears in the text.",
                level=MeasurementLevel.Instance,
                schema=DataSchema(
                    arrowSchema=arrow.encode_schema(
                        arrow.arrow_schema(BlurstCountScoredItem)
                    )
                ),
            ),
        ),
    )
    method_python_function = dyffapi.methods.create(method_python_function_request)
    print(f"method_python_function: {method_python_function.id}")
    ctx["method_python_function"] = method_python_function

    wait_for_success(
        lambda: dyffapi.methods.get(method_python_function.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.depends(
    on=[
        "test_datasets_create",
        "test_evaluations_create",
        "test_methods_create_python_function",
    ]
)
def test_measurements_create_python_function(dyffapi: DyffLocalPlatform, ctx):
    account = ctx["account"]
    evaluation = ctx["evaluation"]
    inferenceservice = ctx["inferenceservice"]
    model = ctx["model"]
    dataset = ctx["dataset"]
    method_python_function = ctx["method_python_function"]
    measurement_python_function_request = AnalysisCreateRequest(
        account=account,
        method=method_python_function.id,
        scope=AnalysisScope(
            evaluation=evaluation.id,
            dataset=dataset.id,
            inferenceService=inferenceservice.id,
            model=(model and model.id),
        ),
        arguments=[
            AnalysisArgument(keyword="embiggen", value="smallest"),
        ],
        inputs=[
            AnalysisInput(keyword="dataset", entity=dataset.id),
            AnalysisInput(keyword="outputs", entity=evaluation.id),
        ],
    )
    measurement_python_function = dyffapi.measurements.create(
        measurement_python_function_request
    )
    print(f"measurement_python_function: {measurement_python_function.id}")
    ctx["measurement_python_function"] = measurement_python_function

    wait_for_success(
        lambda: dyffapi.measurements.get(measurement_python_function.id),
        timeout=timedelta(minutes=5),
    )


@pytest.mark.depends(
    on=[
        "test_datasets_create",
        "test_evaluations_create",
        "test_modules_create_python_rubric",
    ]
)
def test_reports_create(dyffapi: DyffLocalPlatform, ctx):
    account = ctx["account"]
    evaluation = ctx["evaluation"]
    module = ctx["module_python_rubric"]
    report_request = ReportCreateRequest(
        account=account,
        rubric="dyff.fake.rubric.BlurstCount",
        evaluation=evaluation.id,
        modules=[module.id],
    )
    report = dyffapi.reports.create(report_request)
    print(f"report: {report.id}")
    ctx["report"] = report

    wait_for_success(
        lambda: dyffapi.reports.get(report.id),
        timeout=timedelta(minutes=5),
    )


@pytest.mark.depends(
    on=[
        "test_methods_create_jupyter_notebook",
        "test_measurements_create_python_function",
    ]
)
def test_safetycase(dyffapi: DyffLocalPlatform, ctx):
    account = ctx["account"]
    inferenceservice = ctx["inferenceservice"]
    model = ctx["model"]
    method_jupyter_notebook = ctx["method_jupyter_notebook"]
    measurement_python_function = ctx["measurement_python_function"]

    # SafetyCase for JupyterNotebook
    safetycase_jupyter_notebook_request = AnalysisCreateRequest(
        account=account,
        method=method_jupyter_notebook.id,
        scope=AnalysisScope(
            evaluation=None,
            dataset=None,
            inferenceService=inferenceservice.id,
            model=(model and model.id),
        ),
        arguments=[
            AnalysisArgument(keyword="trueName", value="Hans Sprungfeld"),
        ],
        inputs=[
            AnalysisInput(keyword="cromulence", entity=measurement_python_function.id),
        ],
    )
    safetycase_jupyter_notebook = dyffapi.safetycases.create(
        safetycase_jupyter_notebook_request
    )
    print(f"safetycase_jupyter_notebook: {safetycase_jupyter_notebook.id}")
    ctx["safetycase_jupyter_notebook"] = safetycase_jupyter_notebook

    wait_for_success(
        lambda: dyffapi.safetycases.get(safetycase_jupyter_notebook.id),
        timeout=timedelta(minutes=5),
    )
