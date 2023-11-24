# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import logging

from .shared import FileInfo

log = logging.getLogger(__name__)


def write(file: FileInfo) -> None:
    file.path.write_bytes(_render(file))


def _render(file: FileInfo) -> bytes:
    text: str = ""
    if file.prolog:
        text = f"{file.prolog}{file.newlines * 2}"
    if file.header:
        text += f"{file.header}{file.newlines * 2}"
    if file.original_header:
        text += f"{file.original_header}{file.newlines * 2}"
    text += file.contents

    return file.bom + text.encode(file.encoding)
