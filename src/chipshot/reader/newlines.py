# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging

from .. import exceptions
from ..shared import FileInfo

log = logging.getLogger(__name__)


def handle(info: FileInfo) -> None:
    """Detect and handle the newline style present in the file."""

    windows = info.contents.count("\r\n")
    if windows:
        info.newlines = "\r\n"
        info.contents = info.contents.replace("\r\n", "\n")

    macos = info.contents.count("\r")
    if macos:
        if macos > windows:
            info.newlines = "\r"
        info.contents = info.contents.replace("\r", "\n")

    linux = info.contents.count("\n") - windows - macos
    if linux > macos and linux > windows:
        info.newlines = "\n"

    # Detect inconsistent newlines.
    if not (
        (windows == linux == macos == 0)  # No newlines found
        or (windows and linux == macos == 0)  # Windows-style newlines
        or (macos and windows == linux == 0)  # macOS-style newlines
        or (linux and windows == macos == 0)  # Linux-style newlines
    ):
        raise exceptions.InconsistentNewlines
