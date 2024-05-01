# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2024 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import copy
import pathlib
import unittest.mock

import pytest

import chipshot.config
import chipshot.shared


@pytest.fixture(scope="session", autouse=True)
def _load_default_config_once():
    """Load the default config exactly once, and mock the loader function."""

    default_config = chipshot.config._load_default_config()
    mock = unittest.mock.Mock(side_effect=lambda: copy.deepcopy(default_config))
    with unittest.mock.patch("chipshot.config._load_default_config", mock):
        yield copy.deepcopy(default_config)


@pytest.fixture
def default_config(_load_default_config_once):
    return chipshot.config._normalize_config(_load_default_config_once)


@pytest.fixture
def bogus_file():
    info = chipshot.shared.FileInfo(
        path=pathlib.Path("bogus.bogus.bogus"),
        raw_contents=b"",
    )
    yield info


@pytest.fixture
def bogus_config(default_config):
    default_config["extensions"].update(
        {
            "bogus": {},
            "bogus.bogus": {},
        }
    )
    default_config["styles"].update(
        {
            "bogus": {},
            "bogus.bogus": {},
        }
    )
    default_config["prologues"].update(
        {
            "bogus": {},
            "bogus.bogus": {},
        }
    )
    yield default_config


@pytest.fixture
def fs(fs):
    """Allow access to test assets in the fake filesystem."""

    test_files_path = pathlib.Path(__file__).parent / "files"
    fs.add_real_directory(test_files_path)

    yield fs
