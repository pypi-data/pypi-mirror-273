# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess
from pathlib import Path
from typing import Optional

from dyff.schema.platform import MethodBase, MethodImplementationKind, Report

from .._internal import fqn
from . import jupyter, legacy, python


def run_analysis(method: MethodBase, *, storage_root: Path, config_file: Path):
    pythonpath = os.pathsep.join(
        str(storage_root / module) for module in method.modules
    )
    env = os.environ.copy()
    env.update(
        {
            "DYFF_AUDIT_LOCAL_STORAGE_ROOT": str(storage_root),
            "DYFF_AUDIT_ANALYSIS_CONFIG_FILE": str(config_file),
            "PYTHONPATH": pythonpath,
        }
    )

    if method.implementation.kind == MethodImplementationKind.JupyterNotebook:
        impl_module, impl_name = fqn(jupyter.run_jupyter_notebook)
    elif method.implementation.kind == MethodImplementationKind.PythonFunction:
        impl_module, impl_name = fqn(python.run_python_function)
    elif method.implementation.kind == MethodImplementationKind.PythonRubric:
        impl_module, impl_name = fqn(python.run_python_rubric)
    else:
        raise NotImplementedError(
            f"method.implementation.kind = {method.implementation.kind}"
        )

    cmd = f"from {impl_module} import {impl_name}; {impl_name}()"
    subprocess.run(
        ["python3", "-c", cmd],
        env=env,
        check=True,
        capture_output=True,
    )


def run_report(report: Report, *, storage_root: Path):
    return legacy_run_report(
        rubric=report.rubric,
        dataset_path=str(storage_root / report.dataset),
        evaluation_path=str(storage_root / report.evaluation),
        output_path=str(storage_root / report.id),
        modules=[str(storage_root / module) for module in report.modules],
    )


def legacy_run_report(
    *,
    rubric: str,
    dataset_path: str,
    evaluation_path: str,
    output_path: str,
    modules: Optional[list[str]] = None,
):
    if modules is None:
        modules = []

    def quote(s) -> str:
        return f'"{s}"'

    args = [
        quote(rubric),
        quote(dataset_path),
        quote(evaluation_path),
        quote(output_path),
        ", ".join(quote(module) for module in modules),
    ]

    impl_module, impl_name = fqn(legacy.run_python_rubric)
    cmd = (
        f"from {impl_module} import {impl_name}; {impl_name}"
        "(rubric={}, dataset_path={}, evaluation_path={}, output_path={}, modules=[{}])".format(
            *args
        )
    )

    pythonpath = os.pathsep.join(str(module) for module in modules)
    env = os.environ.copy()
    env.update({"PYTHONPATH": pythonpath})

    subprocess.run(
        ["python3", "-c", cmd],
        env=env,
        check=True,
        capture_output=True,
    )


__all__ = [
    "legacy_run_report",
    "run_analysis",
    "run_report",
]
