# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pathlib
import textwrap

import pytest

import chipshot.render
import chipshot.shared

test_templates_root = (pathlib.Path(__file__).parent / "files/templates").resolve()
rendered_files = [
    pytest.param(file, id=str(file.relative_to(test_templates_root)))
    for file in test_templates_root.rglob("**/defaults.*")
]


@pytest.mark.parametrize("rendered_file", rendered_files)
def test_render_header(default_config, rendered_file: pathlib.Path):
    default_config.update({"template_path": str(rendered_file.parent / "template.txt")})
    expected = rendered_file.read_text()
    file = chipshot.shared.FileInfo(rendered_file, raw_contents=b"")
    rendered = chipshot.render.render_header(file, default_config)
    fail_message = textwrap.dedent(
        """
        Expected:
        {0}

        Rendered:
        {1}
    """
    ).format(expected, rendered)
    assert expected.startswith(rendered), fail_message
