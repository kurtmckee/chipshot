# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import typing as t

from .. import exceptions
from ..config import get_config_value
from ..shared import FileInfo

log = logging.getLogger(__name__)


def handle(info: FileInfo, config: dict[str, t.Any]) -> None:
    """Detect and extract an existing header."""

    try:
        (style_key,) = get_config_value(config, info.path, "style")
    except KeyError:
        # If no style is defined for the file, do nothing.
        return

    style: dict[str, str] = config["styles"][style_key]

    # If the first non-whitespace content doesn't start with *block_prefix*,
    # there is no header.
    left_stripped_content = info.contents.lstrip()
    if style["block_prefix"] and not left_stripped_content.startswith(
        style["block_prefix"].strip()
    ):
        return

    # If a block suffix is defined, consume everything up to that point.
    if style["block_suffix"]:
        suffix_start = info.contents.find(style["block_suffix"])
        if suffix_start >= 0:
            suffix_end = suffix_start + len(style["block_suffix"])
            info.original_header = info.contents[:suffix_end]
            if info.contents[suffix_end : suffix_end + 1] != "\n":
                raise exceptions.HeaderBlockRequiresTrailingNewline
            elif info.contents[suffix_end : suffix_end + 2] == "\n\n":
                info.contents = info.contents[suffix_end + 2 :]
            else:  # Only 1 newline.
                info.contents = info.contents[suffix_end + 1 :]
        return

    # Prepare to search the content line-by-line.
    # Find the end of the block prefix, if any.
    scan_start = 0
    if style["block_prefix"]:
        scan_start = left_stripped_content.find(style["block_prefix"])
        if scan_start == -1:
            return
        scan_start += len(style["block_prefix"])

    # Strip trailing whitespace from the *line_prefix*.
    # This anticipates how lines will appear for blank lines in the header.
    line_prefix = style["line_prefix"]
    line_prefix_is_whitespace = True
    if line_prefix.rstrip():
        line_prefix = line_prefix.rstrip()
        line_prefix_is_whitespace = False

    # Assume that a block prefix with no prefixed lines means there is no header.
    header_end_index = 0

    for current_line, next_line, index in two_lines(left_stripped_content, scan_start):
        # Keep going if the current line starts with the line prefix.
        if current_line.startswith(line_prefix):
            header_end_index = index
            continue

        # Keep going if the current line is blank
        # but the next line looks like it's part of the header.
        if (
            line_prefix_is_whitespace
            and current_line.rstrip() == ""
            and (
                next_line is None
                or next_line.rstrip() == ""
                or next_line.startswith(line_prefix)
            )
        ):
            continue

        break

    # If no header was found, exit to prevent changes to newlines.
    if not header_end_index:
        return

    info.original_header = left_stripped_content[:header_end_index]
    if left_stripped_content[header_end_index : header_end_index + 1] != "\n":
        msg = f"{info.path}: The header block does not end with a newline."
        log.warning(msg)
        info.contents = left_stripped_content[header_end_index:]
    elif left_stripped_content[header_end_index : header_end_index + 2] == "\n\n":
        info.contents = left_stripped_content[header_end_index + 2 :]
    else:  # Only 1 newline.
        info.contents = left_stripped_content[header_end_index + 1 :]


def two_lines(
    content: str, start: int
) -> t.Generator[tuple[str, str | None, int], None, None]:
    """Iterate over the content, yielding the current and next lines."""

    if start == len(content):
        return

    middle = content.find("\n", start + 1)
    if middle == -1:
        yield content[start:], None, len(content)
        return
    current_line = content[start:middle]

    end = content.find("\n", middle + 1)
    while end != -1:
        next_line = content[middle + 1 : end]
        yield current_line, next_line, middle
        current_line = next_line
        start, middle, end = middle, end, content.find("\n", end + 1)

    next_line = content[middle + 1 :]
    yield current_line, next_line, middle
    yield next_line, None, len(content)
