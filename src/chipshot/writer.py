# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import logging

from .shared import FileInfo

log = logging.getLogger(__name__)


def write(file: FileInfo) -> None:
    two_newlines = (file.newlines * 2).encode(file.encoding)
    add_two_newlines = False

    with file.path.open("wb") as f:
        f.write(file.bom)

        if file.prologue:
            f.write(file.prologue.replace("\n", file.newlines).encode(file.encoding))
            add_two_newlines = True

        if file.header:
            if add_two_newlines:
                f.write(two_newlines)
            f.write(file.header.replace("\n", file.newlines).encode(file.encoding))
            add_two_newlines = True

        if file.original_header:
            if add_two_newlines:
                f.write(two_newlines)
            f.write(
                file.original_header.replace("\n", file.newlines).encode(file.encoding)
            )
            add_two_newlines = True

        if add_two_newlines:
            f.write(two_newlines)
        f.write(file.contents.replace("\n", file.newlines).encode(file.encoding))
