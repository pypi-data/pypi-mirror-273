# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0


def fqn(obj) -> tuple[str, str]:
    """See: https://stackoverflow.com/a/70693158"""
    try:
        module = obj.__module__
    except AttributeError:
        module = obj.__class__.__module__
    try:
        name = obj.__qualname__
    except AttributeError:
        name = obj.__class__.__qualname__
    # if obj is a method of builtin class, then module will be None
    if module == "builtins" or module is None:
        raise AssertionError("should not be called on a builtin")
    return module, name
