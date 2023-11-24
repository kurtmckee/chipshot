# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import pathlib
import typing as t

from ..shared import FileInfo
from . import encoding, header, newlines, prolog

log = logging.getLogger(__name__)


def read(path: pathlib.Path, config: dict[str, t.Any]) -> FileInfo:
    """Read a file and return its contents and metadata."""

    raw_contents = path.read_bytes()
    info = FileInfo(
        path=path,
        raw_contents=raw_contents,
        encoding=_determine_default_encoding(path, config),
    )

    # If the file is empty, skip all other steps.
    if not raw_contents:
        return info

    encoding.handle(info)
    newlines.handle(info)
    prolog.handle(info, config)
    header.handle(info, config)

    return info


def _determine_default_encoding(path: pathlib.Path, config: dict[str, t.Any]) -> str:
    """Determine the default encoding for the given path."""

    suffixes = "".join(path.suffixes)[1:]
    suffix = "".join(path.suffix)[1:]

    suffixes_config = config["extension"].get(suffixes, {})
    suffix_config = config["extension"].get(suffix, {})

    default_encoding = str(
        suffixes_config.get("encoding")
        or suffix_config.get("encoding")
        or config["default"]["file_info"]["encoding"]
    )
    return default_encoding
