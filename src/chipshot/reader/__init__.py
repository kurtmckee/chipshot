# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import pathlib
import typing as t

from ..shared import FileInfo
from . import encoding, header, newlines, prologue

log = logging.getLogger(__name__)


def read(path: pathlib.Path, config: dict[str, t.Any]) -> FileInfo:
    """Read a file and return its contents and metadata."""

    raw_contents = path.read_bytes()
    info = FileInfo(path=path, raw_contents=raw_contents)

    # If the file is empty, skip all other steps.
    if not raw_contents:
        return info

    encoding.handle(info, config)
    newlines.handle(info)
    prologue.handle(info, config)
    header.handle(info, config)

    return info
