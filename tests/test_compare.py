# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2025 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pytest

import chipshot.compare


def test_empty_before():
    assert chipshot.compare.get_similarity("", "# Copyright\n# License") == 0.0


def test_empty_after():
    assert chipshot.compare.get_similarity("# Copyright\n# License", "") == 0.0


def test_identical():
    text = "# Copyright\n# License"
    assert chipshot.compare.get_similarity(text, text) == pytest.approx(1.0)


def test_similar_second_year_added():
    old = "# Copyright 2022 Kurt McKee\nSPDX-License-Identifier: MIT"
    new = "# Copyright 2022-2023 Kurt McKee\nSPDX-License-Identifier: MIT"
    similarity = chipshot.compare.get_similarity(old, new)
    assert similarity > 0.90


def test_similar_year_bump():
    old = "# Copyright 2009-2022 Kurt McKee\nSPDX-License-Identifier: MIT"
    new = "# Copyright 2009-2023 Kurt McKee\nSPDX-License-Identifier: MIT"
    similarity = chipshot.compare.get_similarity(old, new)
    assert similarity > 0.90
