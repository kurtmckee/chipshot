# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import sys

if sys.version_info >= (3, 11):
    import tomllib
else:  # Python < 3.11
    import tomli as tomllib

__all__ = ["tomllib"]
