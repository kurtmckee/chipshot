# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import dataclasses
import pathlib
import typing as t

bom_type = t.Literal[
    b"\xef\xbb\xbf",
    b"\xff\xfe",
    b"\xfe\xff",
    b"\xff\xfe\x00\x00",
    b"\x00\x00\xfe\xff",
    b"",
]
newline_type = t.Literal["", "\n", "\r", "\r\n"]


@dataclasses.dataclass
class FileInfo:
    path: pathlib.Path
    raw_contents: bytes
    encoding: str = ""
    newlines: newline_type = ""
    bom: bom_type = b""
    prologue: str = ""
    header: str = ""
    original_header: str = ""
    contents: str = ""
