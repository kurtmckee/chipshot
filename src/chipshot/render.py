# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import datetime
import pathlib
import typing as t

import jinja2

import chipshot.exceptions


def render_header(file: pathlib.Path, configuration: dict[str, t.Any]) -> str:
    """Render a (possibly file-specific) template into a header."""

    suffixes = "".join(file.suffixes)[1:]
    suffix = file.suffix[1:]

    suffixes_config = configuration["extension"].get(suffixes, {})
    suffix_config = configuration["extension"].get(suffix, {})

    # Look for the correct template to load.
    jinja_loader: jinja2.DictLoader | jinja2.FileSystemLoader
    # Check for a literal template or a template path for the file's suffixes config.
    if "template" in suffixes_config:
        template_name = "literal"
        jinja_loader = jinja2.DictLoader({"literal": suffixes_config["template"]})
    elif "template_path" in suffixes_config:
        template_path = pathlib.Path(suffixes_config["template_path"])
        template_name = template_path.name
        jinja_loader = jinja2.FileSystemLoader(template_path.parent)
    # Check for a literal template or a template path for the file's suffix config.
    elif "template" in suffix_config:
        template_name = "literal"
        jinja_loader = jinja2.DictLoader({"literal": suffix_config["template"]})
    elif "template_path" in suffix_config:
        template_path = pathlib.Path(suffix_config["template_path"])
        template_name = template_path.name
        jinja_loader = jinja2.FileSystemLoader(template_path.parent)
    # Check for a literal template or a template path in the global config.
    elif "template" in configuration:
        template_name = "literal"
        jinja_loader = jinja2.DictLoader({"literal": configuration["template"]})
    elif "template_path" in configuration:
        template_path = pathlib.Path(configuration["template_path"])
        template_name = template_path.name
        jinja_loader = jinja2.FileSystemLoader(template_path.parent)
    else:
        raise chipshot.exceptions.NoTemplateDefined

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
