# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import datetime
import pathlib
import typing as t

import jinja2

from . import exceptions
from .config import get_config_value


def render_header(file: pathlib.Path, config: dict[str, t.Any]) -> str:
    """Render a (possibly file-specific) template into a header."""

    # Look for a template or template path.
    jinja_loader: jinja2.DictLoader | jinja2.FileSystemLoader
    try:
        template, template_path_str = get_config_value(
            config, file, "template", "template_path"
        )
    except KeyError:
        raise exceptions.NoTemplateDefined

    if template is not None:
        template_name = "literal"
        jinja_loader = jinja2.DictLoader({"literal": template})
    else:  # template_path_str is not None
        template_path = pathlib.Path(template_path_str)
        template_name = template_path.name
        jinja_loader = jinja2.FileSystemLoader(template_path.parent)

    # Render the template.
    env = jinja2.Environment(
        loader=jinja_loader,
        undefined=jinja2.StrictUndefined,
    )
    template = env.get_template(template_name)
    rendered_template: str = template.render(
        {
            "year": datetime.datetime.now().strftime("%Y"),
        },
    )

    # Use the most specific style possible.
    (style_key,) = get_config_value(config, file, "style")
    style = config["styles"][style_key]

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
