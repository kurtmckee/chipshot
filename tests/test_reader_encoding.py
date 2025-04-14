# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2025 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import codecs
import pathlib

import pytest

import chipshot.exceptions
import chipshot.reader.encoding


@pytest.mark.parametrize(
    "bom, encoding",
    (
        (b"", "utf-8"),
        (codecs.BOM_UTF8, "utf-8"),
        (codecs.BOM_UTF16_BE, "utf-16-be"),
        (codecs.BOM_UTF16_LE, "utf-16-le"),
        (codecs.BOM_UTF32_BE, "utf-32-be"),
        (codecs.BOM_UTF32_LE, "utf-32-le"),
    ),
)
def test_bom(bogus_file, default_config, bom, encoding):
    raw_contents = bom + "success".encode(encoding)
    bogus_file.raw_contents = raw_contents
    bogus_file.encoding = "utf-8"

    chipshot.reader.encoding.handle(bogus_file, default_config)

    assert bogus_file.encoding == encoding
    assert bogus_file.bom == bom
    assert bogus_file.contents == "success"


@pytest.mark.parametrize(
    "bom, exception",
    (
        (b"", chipshot.exceptions.FileDoesNotMatchConfiguredEncoding),
        (codecs.BOM_UTF8, chipshot.exceptions.FileDoesNotMatchBOMEncoding),
    ),
)
def test_decode_errors(bogus_file, default_config, bom, exception):
    bogus_file.raw_contents = bom + b"\xf0"
    bogus_file.encoding = "utf-8"

    with pytest.raises(exception):
        chipshot.reader.encoding.handle(bogus_file, default_config)


@pytest.mark.parametrize(
    "embedded_encoding",
    (
        # Source: https://peps.python.org/pep-0263/
        pytest.param("# coding=shift-jis", id="pep263-basic"),
        pytest.param("# -*- coding: shift-jis -*-", id="pep263-emacs"),
        pytest.param("# vim: set fileencoding=shift-jis :", id="pep263-vim"),
        pytest.param("# This file uses this encoding: shift-jis", id="pep263-text"),
    ),
)
@pytest.mark.parametrize("hashbang", ("", "#!/usr/bin/python\n"))
def test_embedded_encoding(embedded_encoding, hashbang, bogus_file, default_config):
    bogus_file.path = pathlib.Path("script")
    expected_contents = f"{hashbang}{embedded_encoding}\nprint('平仮名')"
    bogus_file.raw_contents = expected_contents.encode("shift-jis")

    chipshot.reader.encoding.handle(bogus_file, default_config)
    assert bogus_file.encoding == "shift-jis"
    assert bogus_file.contents == expected_contents


@pytest.mark.parametrize(
    "embedded_encoding",
    (
        b"# -*- coding: utf-42 -*-",
        b'@charset: "utf-42";',
    ),
)
def test_embedded_encoding_lookup_error(
    embedded_encoding, bogus_file, default_config, caplog
):
    caplog.set_level(0)
    bogus_file.path = pathlib.Path("script")
    bogus_file.raw_contents = embedded_encoding

    chipshot.reader.encoding.handle(bogus_file, default_config)
    assert bogus_file.encoding == "utf-8"
    assert "'utf-42', but that encoding is not recognized" in caplog.text


@pytest.mark.parametrize(
    "contents",
    (
        "# coding=shift-jis\nprint('平仮名')",
        """@charset: "shift-jis";\n.games::before { content: '🎮 '; }""",
    ),
)
def test_comment_encoding_incorrect(contents, bogus_file, default_config):
    bogus_file.path = pathlib.Path("script")
    bogus_file.raw_contents = contents.encode("utf-8")

    with pytest.raises(chipshot.exceptions.FileDoesNotMatchEmbeddedEncoding):
        chipshot.reader.encoding.handle(bogus_file, default_config)


def test_comment_encoding_3rd_line(bogus_file, default_config):
    bogus_file.path = pathlib.Path("script")
    bogus_file.raw_contents = b"\n\n# coding=ascii"

    chipshot.reader.encoding.handle(bogus_file, default_config)
    assert bogus_file.encoding == "utf-8"
