# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import codecs
import logging
import re
import typing

from .. import exceptions
from ..config import get_config_value
from ..shared import FileInfo

log = logging.getLogger(__name__)


encoding_comment_pattern = re.compile(
    r"\A(?:^#.*$\n)?#.*(?:en)?coding[\t ]*[:=][\t ]*(?P<encoding>[A-Za-z0-9_.-]+)",
    flags=re.MULTILINE,
)


def handle(info: FileInfo, config: dict[str, typing.Any]) -> None:
    """Detect and handle the file encoding.

    The encoding may be embedded in the file in the following ways:

    *   A byte order mark may appear in the first ~4 bytes of the file
    *   An encoding comment that is ASCII-compatible may appear at the top of the file

    If no embedded encoding is found (or honored),
    Chipshot will use a configured encoding.
    """

    # If the raw content has a byte order mark, use it.
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

    if info.bom:
        log.debug(f"{info.path}: Found BOM for encoding '{info.encoding}'")
        info.raw_contents = info.raw_contents[len(info.bom) :]
        try:
            info.contents = info.raw_contents.decode(info.encoding)
        except UnicodeDecodeError:
            raise exceptions.FileDoesNotMatchBOMEncoding
        return

    # If the file contains a "coding" or "encoding" comment, use it.
    chunk = info.raw_contents[:500].decode("utf-8", errors="ignore")
    match = encoding_comment_pattern.search(chunk)
    if match is not None:
        info.encoding = match.group("encoding")
        log.debug(f"{info.path}: Found comment encoding '{info.encoding}'")
        try:
            info.contents = info.raw_contents.decode(info.encoding)
        except LookupError:
            log.debug(f"{info.path}: '{info.encoding}' is not a valid encoding")
        except UnicodeDecodeError:
            raise exceptions.FileDoesNotMatchEmbeddedEncoding
        else:
            return

    # Fallback to a configured encoding.
    (info.encoding,) = get_config_value(config, info, "encoding")
    log.debug(f"{info.path}: Found configured encoding '{info.encoding}'")
    try:
        info.contents = info.raw_contents.decode(info.encoding)
    except UnicodeDecodeError:
        raise exceptions.FileDoesNotMatchConfiguredEncoding
