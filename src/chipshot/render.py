# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import datetime
import pathlib
import typing as t

import jinja2


def render_header(file: pathlib.Path, configuration: dict[str, t.Any]) -> str:
    """Render a (possibly file-specific) template into a header."""

    suffixes = "".join(file.suffixes)[1:]
    suffix = file.suffix[1:]

    suffixes_config = configuration["extension"].get(suffixes, {})
    suffix_config = configuration["extension"].get(suffix, {})

    # Look for the correct template to load.
    template_root = configuration.get("template_root", "")
    template_path = (
        suffixes_config.get("template")
        or suffix_config.get("template")
        or configuration["template"]
    )
    template = pathlib.Path(template_root) / template_path

    # Render the template.
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template.parent),
        undefined=jinja2.StrictUndefined,
    )
    template = env.get_template(template.name)
    rendered_template: bytes = template.render(
        {
            "year": datetime.datetime.now().strftime("%Y"),
        },
    )

    # Use the most specific style possible.
    style = (
        configuration["style"].get(suffixes_config.get("style", ...), {})
        or configuration["style"].get(suffix_config.get("style", ...), {})
        or configuration["default"]["style"]
    )

    lines: list[str] = []
    line_prefix = style["line_prefix"]
    line_suffix = style["line_suffix"]
    for line in rendered_template.splitlines():
        rendered_line = line_prefix + line + line_suffix
        lines.append(rendered_line.rstrip())

    header = "\n".join(lines)
    if style["block_prefix"]:
        header = style["block_prefix"] + header
    if style["block_suffix"]:
        header = header + style["block_suffix"]

    return header
