# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pathlib

import pytest

import chipshot.reader.identity


@pytest.mark.parametrize(
    "prologue, expected",
    (
        # No-op
        pytest.param("", "", id="empty prologue"),
        pytest.param("bogus", "", id="not a hashbang"),
        # Actual code
        pytest.param("#!/usr/bin/python", "python", id="base executable name"),
        pytest.param("#!/usr/bin/python3.11", "python", id="trailing version"),
        pytest.param("#!/usr/bin/env python", "python", id="env"),
        pytest.param(r"#!C:\Program Files\Python39\python.exe", "python", id="windows"),
        # Loop exhaustion
        pytest.param("#!env unknown -c", "", id="loop exhaustion"),
    ),
)
def test_identity(bogus_file, default_config, prologue, expected):
    bogus_file.path = pathlib.Path("script")
    bogus_file.contents = prologue

    chipshot.reader.identity.handle(bogus_file, default_config)

    assert bogus_file.identity == expected
