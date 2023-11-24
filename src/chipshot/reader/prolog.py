# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import re
import typing as t

from .. import exceptions
from ..shared import FileInfo

log = logging.getLogger(__name__)


def handle(info: FileInfo, config: dict[str, t.Any]) -> None:
    suffixes = "".join(info.path.suffixes)[1:]
    suffix = "".join(info.path.suffix)[1:]

    suffixes_config = config["extension"].get(suffixes, {})
    suffix_config = config["extension"].get(suffix, {})

    if "prolog" in suffixes_config:
        prolog_key = suffixes_config["prolog"]
    else:
        prolog_key = suffix_config.get("prolog")
    if not (isinstance(prolog_key, str) and prolog_key):
        return

    prolog_pattern = config["prolog"].get(prolog_key, {}).get("pattern", "")
    if not (isinstance(prolog_pattern, str) and prolog_pattern):
        return

    pattern = re.compile(prolog_pattern, flags=re.M)
    match = pattern.search(info.contents)
    if match is None:
        return

    match_start, match_end = match.span(0)

    # The prolog, if found, must start at the first character in the document.
    if match_start != 0:
        log.warning(
            f"{info.path}: "
            "A prolog was found, but not at the beginning of the document. "
            "It will be ignored."
        )
        return

    # The prolog must end with a newline.
    if info.contents[match_end : match_end + 1] != "\n":
        raise exceptions.PrologRequiresTrailingNewline

    info.prolog = match.group(0)
    info.contents = info.contents[match_end + 1 :]
