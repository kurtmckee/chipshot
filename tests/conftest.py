# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2024 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import copy
import pathlib

import pytest

import chipshot.config
import chipshot.shared


@pytest.fixture(scope="session")
def _load_default_config_once():
    defaults = chipshot.config._load_default_config()
    return chipshot.config._normalize_config(defaults)


@pytest.fixture
def default_config(_load_default_config_once):
    return copy.deepcopy(_load_default_config_once)


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
