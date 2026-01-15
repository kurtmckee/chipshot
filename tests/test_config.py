# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pytest

import chipshot.config
import chipshot.exceptions


@pytest.mark.parametrize("top_level_key", ("extensions", "styles"))
def test_defaults_key_order_first_level(default_config, top_level_key):
    """Guarantee the default config has sorted keys."""

    previous_name = ""
    for name in default_config[top_level_key]:
        assert name > previous_name, f"'{name}' is not sorted in '{top_level_key}'"
        previous_name = name


def test_load_no_files_available(fs):
    """Verify Chipshot can load a default config when no files are specified."""

    assert bool(chipshot.config.load())


@pytest.mark.parametrize(
    "create_file, load_file",
    (
        (".chipshot.toml", None),
        ("pyproject.toml", None),
        ("custom.toml", "custom.toml"),
    ),
)
def test_load_no_config_found_in_file(fs, create_file, load_file):
    """Verify that ConfigNotFound is raised when a parseable file has no config."""

    fs.create_file(create_file)
    with pytest.raises(chipshot.exceptions.ConfigNotFound):
        chipshot.config.load(load_file)


def test_custom_extension_enablement(fs):
    """Confirm that an extension in the user config is recursively integrated."""

    contents = b"[chipshot.extensions.yaml]\nstyle = 'hash'"
    fs.create_file(".chipshot.toml", contents=contents)
    config = chipshot.config.load()
    assert "yaml" in config["extensions"]
    assert "py" in config["extensions"]
