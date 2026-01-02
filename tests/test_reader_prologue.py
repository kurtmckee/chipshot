# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pathlib

import pytest

import chipshot.exceptions
import chipshot.reader.prologue

variants = pytest.mark.parametrize(
    "variant",
    (
        pytest.param("bogus", id="suffix"),
        pytest.param("bogus.bogus", id="suffixes"),
    ),
)


def test_prologue_success_no_header(fs, default_config):
    path = pathlib.Path("script.sh")
    fs.create_file(path, contents=b"#!/bin/sh\n\necho success")

    info = chipshot.reader.read(path, default_config)
    assert info.prologue == "#!/bin/sh"
    assert info.original_header == ""
    assert info.contents == "\necho success"


def test_prologue_success_with_header(fs, default_config):
    path = pathlib.Path("script.sh")
    fs.create_file(path, contents=b"#!/bin/sh\n\n# header\n\necho success")

    info = chipshot.reader.read(path, default_config)
    assert info.prologue == "#!/bin/sh"
    assert info.original_header == "# header"
    assert info.contents == "echo success"


def test_prologue_empty_pattern(bogus_file, bogus_config):
    bogus_file.contents = "anything"
    bogus_config["extensions"]["bogus"]["prologue"] = "bogus"
    bogus_config["prologues"]["bogus"]["pattern"] = ""

    chipshot.reader.prologue.handle(bogus_file, bogus_config)

    assert bogus_file.prologue == ""
    assert bogus_file.contents == "anything"


@variants
def test_prologue_not_first_line(bogus_file, bogus_config, variant, caplog):
    caplog.set_level(0)
    bogus_file.contents = "# first\n#!/bin/sh\necho success"
    bogus_config["prologues"][variant] = bogus_config["prologues"]["hashbang"]
    bogus_config["extensions"][variant]["prologue"] = variant

    chipshot.reader.prologue.handle(bogus_file, bogus_config)

    assert (
        "A prologue was found, but not at the beginning of the document." in caplog.text
    )
    assert bogus_file.prologue == ""
    assert bogus_file.contents == "# first\n#!/bin/sh\necho success"


def test_prologue_not_configured(bogus_file, bogus_config):
    bogus_config["extensions"] = {}
    bogus_file.contents = "#!/bin/sh\necho success"

    chipshot.reader.prologue.handle(bogus_file, bogus_config)

    assert bogus_file.prologue == ""
    assert bogus_file.contents == "#!/bin/sh\necho success"


@variants
def test_prologue_no_newline(bogus_file, bogus_config, variant):
    bogus_config["prologues"][variant]["pattern"] = "^#!.+?;"
    bogus_config["extensions"][variant]["prologue"] = variant
    bogus_file.contents = "#!/bin/sh; echo success"

    with pytest.raises(chipshot.exceptions.PrologueRequiresTrailingNewline):
        chipshot.reader.prologue.handle(bogus_file, bogus_config)


def test_css_prologue(bogus_file, default_config):
    bogus_file.path = pathlib.Path("sample.css")
    bogus_file.contents = """@charset: "shift-jis";\n.x::before { content: '🎮 '; }"""

    chipshot.reader.prologue.handle(bogus_file, default_config)

    assert bogus_file.prologue == '@charset: "shift-jis";'
    assert bogus_file.contents == ".x::before { content: '🎮 '; }"
