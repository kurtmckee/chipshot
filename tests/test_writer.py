# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2025 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import codecs
import pathlib

import pytest

import chipshot.writer
from chipshot.shared import FileInfo

encodings = pytest.mark.parametrize("encoding", ("utf-8", "shift-jis"))
newlines = pytest.mark.parametrize("newline", ("\n", "\r", "\r\n"))
boms = pytest.mark.parametrize(
    "bom, encoding",
    (
        (codecs.BOM_UTF32_BE, "utf-32-be"),
        (codecs.BOM_UTF32_LE, "utf-32-le"),
        (codecs.BOM_UTF16_BE, "utf-16-be"),
        (codecs.BOM_UTF16_LE, "utf-16-le"),
        (codecs.BOM_UTF8, "utf-8"),
    ),
)


emoji = "\N{SMILING FACE WITH SUNGLASSES}"


@encodings
def test_basic(fs, encoding):
    info = FileInfo(
        path=pathlib.Path("file"),
        raw_contents=b"",
        contents="あ",
        encoding=encoding,
    )
    chipshot.writer.write(info)

    assert info.path.read_bytes().decode(encoding) == "あ"


@boms
def test_bom(fs, bom, encoding):
    info = FileInfo(
        bom=bom,
        encoding=encoding,
        path=pathlib.Path("file"),
        raw_contents=b"",
        contents=emoji,
    )
    chipshot.writer.write(info)

    raw_content = info.path.read_bytes()
    assert raw_content.startswith(bom)
    assert raw_content[len(bom) :].decode(encoding) == emoji


@newlines
def test_newlines(fs, newline):
    info = FileInfo(
        newlines=newline,
        path=pathlib.Path("file"),
        raw_contents=b"",
        contents="1\n2\n3",
        encoding="utf-8",
    )
    chipshot.writer.write(info)

    assert info.path.read_bytes().count(newline.encode("utf-8")) == 2


@newlines
def test_prologue(fs, newline):
    info = FileInfo(
        newlines=newline,
        prologue="1\n2\n3",
        path=pathlib.Path("file"),
        raw_contents=b"",
        contents="",
        encoding="utf-8",
    )
    chipshot.writer.write(info)

    assert info.path.read_bytes().count(newline.encode("utf-8")) == 2 + 2


def test_header_with_prologue(fs):
    info = FileInfo(
        newlines="\r\n",
        prologue="pl",
        header="1\n2\n3",
        path=pathlib.Path("file"),
        raw_contents=b"",
        contents="abc",
        encoding="utf-8",
    )
    chipshot.writer.write(info)

    assert info.path.read_bytes() == b"pl\r\n\r\n1\r\n2\r\n3\r\n\r\nabc"


def test_header_without_prologue(fs):
    info = FileInfo(
        newlines="\r\n",
        header="1\n2\n3",
        path=pathlib.Path("file"),
        raw_contents=b"",
        contents="abc",
        encoding="utf-8",
    )
    chipshot.writer.write(info)

    assert info.path.read_bytes() == b"1\r\n2\r\n3\r\n\r\nabc"


def test_original_header_without_new_header(fs):
    info = FileInfo(
        newlines="\r\n",
        original_header="1\n2\n3",
        path=pathlib.Path("file"),
        raw_contents=b"",
        contents="abc",
        encoding="utf-8",
    )
    chipshot.writer.write(info)

    assert info.path.read_bytes() == b"1\r\n2\r\n3\r\n\r\nabc"


def test_original_header_with_new_header(fs):
    info = FileInfo(
        newlines="\r\n",
        header="hd",
        original_header="1\n2\n3",
        path=pathlib.Path("file"),
        raw_contents=b"",
        contents="abc",
        encoding="utf-8",
    )
    chipshot.writer.write(info)

    assert info.path.read_bytes() == b"hd\r\n\r\n1\r\n2\r\n3\r\n\r\nabc"
