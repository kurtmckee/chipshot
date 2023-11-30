# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import codecs
import logging
import typing

from .. import exceptions
from ..config import get_config_value
from ..shared import FileInfo

log = logging.getLogger(__name__)


def handle(info: FileInfo, config: dict[str, typing.Any]) -> None:
    """Detect and handle the file encoding.

    The encoding may be determined by a byte order mark at the beginning of the file.
    """

    # If the raw content has a byte order mark, ignore the default encoding.
    # Note that the order of these conditions is sensitive.
    if info.raw_contents.startswith(codecs.BOM_UTF32_BE):
        info.bom = codecs.BOM_UTF32_BE
        info.encoding = "utf-32-be"
    elif info.raw_contents.startswith(codecs.BOM_UTF32_LE):
        info.bom = codecs.BOM_UTF32_LE
        info.encoding = "utf-32-le"
    elif info.raw_contents.startswith(codecs.BOM_UTF16_BE):
        info.bom = codecs.BOM_UTF16_BE
        info.encoding = "utf-16-be"
    elif info.raw_contents.startswith(codecs.BOM_UTF16_LE):
        info.bom = codecs.BOM_UTF16_LE
        info.encoding = "utf-16-le"
    elif info.raw_contents.startswith(codecs.BOM_UTF8):
        info.bom = codecs.BOM_UTF8
        info.encoding = "utf-8"
    else:
        (info.encoding,) = get_config_value(config, info.path, "encoding")

    if info.bom:
        info.raw_contents = info.raw_contents[len(info.bom) :]

    try:
        info.contents = info.raw_contents.decode(info.encoding)
    except UnicodeDecodeError:
        if info.bom:
            raise exceptions.FileDoesNotMatchBOMEncoding
        raise exceptions.FileDoesNotMatchConfiguredEncoding
