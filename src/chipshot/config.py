# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import copy
import importlib.resources as importlib_resources
import logging
import pathlib
import typing as t

from . import exceptions, resources
from ._compat.py310 import tomllib
from .shared import FileInfo

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

    config = _integrate_configs(_load_default_config(), custom_config)

    return _normalize_config(config)


def get_config_value(
    config: dict[str, t.Any],
    info: FileInfo,
    *keys: str,
) -> tuple[t.Any, ...]:
    """Get the most specific config value possible for a given file.

    "Most specific" means the following:

    1.  Check all possible extensions, from the greatest number to the least number.

        For example, if the filename is `sidebar.jinja.html`,
        then these extensions will be tried in this order:

        *   jinja.html
        *   html

    2.  If no extension matches, check the file type for a configuration value.

    3.  If no extension or file type matches, check the global configuration.

    If more than one key is specified (for example, "template" and "template_path"),
    the first key found in the most specific config will be selected.

    The return value will be a tuple with the same length as the number of keys.

    ``KeyError`` is raised if no configuration value is defined anywhere.
    """

    return_value = [None] * len(keys)

    # Look for the config in the 'extension' values.
    path = info.path
    suffix_list = path.suffixes
    for starting_index in range(len(suffix_list)):
        extension = "".join(suffix_list[starting_index:])[1:]
        for key_index, key in enumerate(keys):
            if key not in config["extensions"].get(extension, {}):
                continue
            log.debug(f"{path}: Using '{key}' config found for extension {extension}")
            return_value[key_index] = config["extensions"][extension][key]
            return tuple(return_value)

    type_ = info.identity
    if type_ in config["types"]:
        for key_index, key in enumerate(keys):
            if key not in config["types"][type_]:
                continue
            log.debug(f"{path}: Using '{key}' config found for file type '{type_}'")
            return_value[key_index] = config["types"][type_][key]
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


def _integrate_configs(
    base_config: dict[str, t.Any],
    new_config: dict[str, t.Any],
) -> dict[str, t.Any]:
    """Integrate an additional configuration into an existing configuration.

    This differs from a simple `dict.update()` call because it is semi-recursive.
    """

    integrated_config: dict[str, t.Any] = {}

    unique_base_keys = set(base_config) - set(new_config)
    unique_new_keys = set(new_config) - set(base_config)
    shared_keys = set(base_config) & set(new_config)

    integrated_config.update({key: base_config[key] for key in unique_base_keys})
    integrated_config.update({key: new_config[key] for key in unique_new_keys})

    # Integrate overlapping keys.
    for key in shared_keys:
        if isinstance(value := base_config[key], dict):
            integrated_config[key] = _integrate_configs(value, new_config.get(key, {}))
        else:
            integrated_config[key] = value

    return integrated_config
