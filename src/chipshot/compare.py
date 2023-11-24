# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import datetime
import math
import re

interesting_text_pattern = re.compile(
    r"""
    \b
    (
        copyright
        |licensed?
        |spdx
        |\d{4}
        |https?://[\w/-]+
        |[\w/.-]+@[\w/.-]+
    )
    \b
    """,
    flags=re.MULTILINE | re.IGNORECASE | re.VERBOSE,
)


def get_similarity(existing: str, new: str) -> float:
    """Determine the similarity between an existing header and a new header.

    A value close to 0 means that the headers are very different;
    this may indicate that the existing header should be kept
    and that the target header should be added in ahead of it.

    A value close to 1 means that the headers are very similar;
    this may indicate that the existing header should be replaced.
    """

    # This is an implementation of the cosine similarity equation:
    #
    #     x • y      <-- dot product
    #   ---------
    #   ║x║ • ║y║    <-- product of Euclidean norms
    #
    # ║x║ is the square root of the sum of x's squares.
    #
    # x and y are vectors with arbitrary axes.
    # This implementation assigns values to axes like this:
    #
    #   *   The word "copyright" is in the text
    #   *   The word "license" is in the text
    #   *   ...etc
    #

    vector_1 = _get_vector(existing)
    vector_2 = _get_vector(new)

    keys = set(vector_1.keys()) | set(vector_2)
    cross_product = 0
    squared_sum_1 = 0
    squared_sum_2 = 0
    for key in keys:
        cross_product += vector_1.get(key, 0) * vector_2.get(key, 0)
        squared_sum_1 += vector_1.get(key, 0) ** 2
        squared_sum_2 += vector_2.get(key, 0) ** 2

    try:
        return cross_product / math.sqrt(squared_sum_1) / math.sqrt(squared_sum_2)
    except ZeroDivisionError:
        return 0.0


def _get_vector(text: str) -> dict[str, int]:
    vector = {
        "copyright": 0,
        "license": 0,
        "spdx": 0,
        "year": 0,
        "url": 0,
        "email": 0,
    }

    words = interesting_text_pattern.findall(text.lower())

    for word in words:
        # Favored weighting: 3
        if word == "copyright":
            vector["copyright"] = 3
        elif word in {"license", "licensed"}:
            vector["license"] = 3
        elif word == "spdx":
            vector["spdx"] = 3
        elif word.isnumeric() and 1970 <= int(word) <= datetime.datetime.now().year + 2:
            vector["year"] = 3
            # Keep track of the year itself.
            vector[word] = 1

        # Basic weighting: 2
        elif word.startswith(("https://", "http://")):
            vector["url"] = 2
            # Include the URL in the weighting.
            vector[word] = 1
        elif "@" in word:
            vector["email"] = 2
            # Include the email address in the weighting.
            vector[word] = 1

    return vector
