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

    # Try to load '.chipshot.toml' if no path was specified.
    if path is None:
        chipshot_toml = pathlib.Path(".chipshot.toml")
        if chipshot_toml.is_file():
            log.debug("Defaulting to load a '.chipshot.toml' file")
            path = chipshot_toml

    # If no path was specified and '.chipshot.toml' doesn't exist,
    # try to load 'pyproject.toml'.
    if path is None:
        pyproject_toml = pathlib.Path("pyproject.toml")
        if pyproject_toml.is_file():
            log.debug("Defaulting to load a 'pyproject.toml' file")
            path = pyproject_toml

    # If *path* is a string, convert it to a Path object.
    if isinstance(path, str):
        path = pathlib.Path(path)

    custom_config = {}
    if path is not None:
        log.debug(f"Loading config file '{path}'")
        custom_config = _load_toml(path)

    config = _load_default_config()
    config.update(custom_config)

    return _normalize_config(config)


def get_config_value(
    config: dict[str, t.Any],
    path: pathlib.Path,
    *keys: str,
) -> tuple[t.Any, ...]:
    """Get the most specific config value possible for a given file path.

    "Most specific" means "the greatest number of suffixes with a matching config key".

    For example, if the filename is `sidebar.jinja.html`,
    then these extensions will be tried in this order:

    *   jinja.html
    *   html

    If more than one key is specified (for example, "template" and "template_path"),
    the first key found in the most specific config will be selected.

    The return value will be a tuple with the same length as the number of keys.

    """

    return_value = [None] * len(keys)

    # Look for the config in the 'extension' values.
    suffix_list = path.suffixes
    for starting_index in range(len(suffix_list)):
        extension = "".join(suffix_list[starting_index:])[1:]
        for key_index, key in enumerate(keys):
            if key not in config["extensions"].get(extension, {}):
                continue
            log.debug(f"{path}: Using '{key}' config found for extension {extension}")
            return_value[key_index] = config["extensions"][extension][key]
            return tuple(return_value)

    # Look for the config in the global values.
    for key_index, key in enumerate(keys):
        if key in config:
            log.debug(f"{path}: Using '{key}' config found in the global configuration")
            return_value[key_index] = config[key]
            return tuple(return_value)

    # No config was found.
    log.debug(f"{path}: No config was found for key(s): {', '.join(keys)}")
    raise KeyError


def _load_toml(path: pathlib.Path) -> dict[str, t.Any]:
    """Load configuration from a TOML file."""

    toml = tomllib.loads(path.read_text("utf-8"))
    try:
        if path.name == "pyproject.toml":
            log.debug("Looking for config in the 'tool.chipshot' key")
            config = toml["tool"]["chipshot"]
        else:  # All other configuration files use a top-level "chipshot" key.
            log.debug("Looking for config in the 'chipshot' key")
            config = toml["chipshot"]
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
    for key, value in result["styles"].items():
        style = {
            "block_prefix": "",
            "line_prefix": "",
            "line_suffix": "",
            "block_suffix": "",
        }
        style.update(value)
        result["styles"][key] = style

    return result
