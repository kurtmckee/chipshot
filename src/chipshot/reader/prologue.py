# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import re
import typing as t

from .. import exceptions
from ..config import get_config_value
from ..shared import FileInfo

log = logging.getLogger(__name__)


def handle(info: FileInfo, config: dict[str, t.Any]) -> None:
    try:
        (prologue_key,) = get_config_value(config, info.path, "prologue")
    except KeyError:
        return

    prologue_pattern = config["prologues"][prologue_key]["pattern"]
    if not (isinstance(prologue_pattern, str) and prologue_pattern):
        return

    pattern = re.compile(prologue_pattern, flags=re.M)
    match = pattern.search(info.contents)
    if match is None:
        return

    match_start, match_end = match.span(0)

    # The prologue, if found, must start at the first character in the document.
    if match_start != 0:
        log.warning(
            f"{info.path}: "
            "A prologue was found, but not at the beginning of the document. "
            "It will be ignored."
        )
        return

    # The prologue must end with a newline.
    if info.contents[match_end : match_end + 1] != "\n":
        raise exceptions.PrologueRequiresTrailingNewline

    info.prologue = match.group(0)
    info.contents = info.contents[match_end + 1 :]
