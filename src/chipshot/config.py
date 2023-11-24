# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import copy
import logging
import pathlib
import sys
import typing as t

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:  # Python < 3.9
    import importlib_resources

if sys.version_info >= (3, 11):
    import tomllib
else:  # Python < 3.11
    import tomli as tomllib

from . import exceptions, resources

log = logging.getLogger(__name__)


def load(path: str | pathlib.Path | None = None) -> dict[str, t.Any]:
    """Load the default configuration and any specified config, if any."""

    config = _load_default_config()
    if path is None:
        # Try to load 'pyproject.toml'.
        pyproject_toml = pathlib.Path("pyproject.toml")
        if pyproject_toml.is_file():
            config.update(_load_toml(pyproject_toml))
    else:
        path = pathlib.Path(path)
        config.update(_load_toml(path))

    return _normalize_config(config)


def _load_toml(path: pathlib.Path) -> dict[str, t.Any]:
    """Load configuration from a `pyproject.toml` file."""

    toml = tomllib.loads(path.read_text("utf-8"))
    try:
        config = toml["tool"]["chipshot"]
        if not isinstance(config, dict):
            raise exceptions.BadConfig(f"'tool.chipshot' in {path} is not a valid type")
    except KeyError:
        raise exceptions.ConfigNotFound(f"No Chipshot config found in {path}")

    return config


def _load_default_config() -> dict[str, t.Any]:
    """Load the default config."""

    resources_root = importlib_resources.files(resources)
    toml_content = (resources_root / "default-config.toml").read_text("utf-8")
    return tomllib.loads(toml_content)


def _normalize_config(configuration: dict[str, t.Any]) -> dict[str, t.Any]:
    """Copy default style values into each style configuration block."""

    result: dict[str, t.Any] = copy.deepcopy(configuration)
    for key, style in result["style"].items():
        value = result["default"]["style"].copy()
        value.update(style)
        result["style"][key] = value

    return result
