# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2024 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pathlib

import pytest

import chipshot.exceptions
import chipshot.reader.header


def test_find_header_no_style(bogus_file, bogus_config):
    bogus_file.contents = "/*#//*/';rem"

    chipshot.reader.header.handle(bogus_file, bogus_config)

    assert bogus_file.original_header == ""
    assert bogus_file.contents == "/*#//*/';rem"


def test_find_header_starts_with_non_block_prefix_text(fs, default_config):
    path = pathlib.Path("sample.css")
    fs.create_file(path, contents=b"a { color: blue; } /* classic */")

    info = chipshot.reader.read(path, default_config)
    assert info.original_header == ""
    assert info.contents == "a { color: blue; } /* classic */"


def test_find_header_no_block_suffix(fs, default_config):
    path = pathlib.Path("sample.css")
    fs.create_file(path, contents=b"/*\n * no block suffix\n")

    info = chipshot.reader.read(path, default_config)
    assert info.original_header == ""
    assert info.contents == "/*\n * no block suffix\n"


@pytest.mark.parametrize("newline_count", (0, 1, 2))
def test_find_header_by_block_suffix(fs, default_config, newline_count):
    newlines = "\n" * newline_count
    contents = f"/*\n * success\n */{newlines}// other"
    path = pathlib.Path("sample.c")
    fs.create_file(path, contents=contents)

    if newline_count:
        info = chipshot.reader.read(path, default_config)
        assert info.original_header == "/*\n * success\n */"
        assert info.contents == "// other"
    else:  # newline_count == 0
        with pytest.raises(chipshot.exceptions.HeaderBlockRequiresTrailingNewline):
            chipshot.reader.read(path, default_config)


def test_find_header_line_by_line(fs, default_config):
    path = pathlib.Path("sample.py")
    fs.create_file(path, contents="# 1\n# 2\n\nprint('success')")

    info = chipshot.reader.read(path, default_config)
    assert info.prologue == ""
    assert info.original_header == "# 1\n# 2"
    assert info.contents == "print('success')"


def test_restructured_text_success(bogus_file, default_config):
    bogus_file.path = pathlib.Path("sample.rst")
    bogus_file.contents = "..\n    Copyright\n\n    License\n\nHello\n#####"

    chipshot.reader.header.handle(bogus_file, default_config)

    assert bogus_file.original_header == "..\n    Copyright\n\n    License"
    assert bogus_file.contents == "Hello\n#####"


def test_restructured_text_block_prefix_incomplete(bogus_file, default_config):
    bogus_file.path = pathlib.Path("sample.rst")
    bogus_file.contents = ".."

    chipshot.reader.header.handle(bogus_file, default_config)

    assert bogus_file.original_header == ""
    assert bogus_file.contents == ".."


def test_restructured_text_block_prefix_no_content(bogus_file, default_config):
    bogus_file.path = pathlib.Path("sample.rst")
    bogus_file.contents = "..\n"

    chipshot.reader.header.handle(bogus_file, default_config)

    assert bogus_file.original_header == ""
    assert bogus_file.contents == "..\n"


@pytest.mark.parametrize(
    "content", ("..\n    Copyright", "..\n    Copyright\n    License")
)
def test_restructured_text_only_header_no_trailing_newline(
    bogus_file, default_config, content
):
    bogus_file.path = pathlib.Path("sample.rst")
    bogus_file.contents = content

    chipshot.reader.header.handle(bogus_file, default_config)

    assert bogus_file.original_header == content
    assert bogus_file.contents == ""


def test_restructured_text_header_without_blank_line(bogus_file, default_config):
    bogus_file.path = pathlib.Path("sample.rst")
    bogus_file.contents = "..\n    Copyright\n    License\nINVALID RST"

    chipshot.reader.header.handle(bogus_file, default_config)

    assert bogus_file.original_header == "..\n    Copyright\n    License"
    assert bogus_file.contents == "INVALID RST"
