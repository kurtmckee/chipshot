# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import pathlib
import typing

from ..shared import FileInfo

log = logging.getLogger(__name__)


def handle(info: FileInfo, config: dict[str, typing.Any]) -> None:
    """Determine the file type by examining the prologue."""

    # If the file has an extension, do nothing.
    if info.path.name.rfind(".") > 0:
        log.debug(f"{info.path}: Skipping identity check because file has an extension")
        return

    # If the prologue doesn't start with a hashbang, do nothing.
    if not info.contents.startswith("#!"):
        log.debug(f"{info.path}: Skipping identity check because file has no hashbang")
        return

    for piece in info.contents[2:200].split()[:2]:
        # PureWindowsPath is compatible with both *nix and Windows paths,
        # and ensures the name can be extracted, regardless of platform.
        path = pathlib.PureWindowsPath(piece)

        # Look for the full name.
        name = path.name.lower()
        if name in config["interpreters"]:
            log.debug(f"{info.path}: Found interpreter '{name}'")
            info.identity = config["interpreters"][name]
            return

        # Look for a version-less name.
        name_without_version = name.rstrip("0123456789.")
        if name_without_version in config["interpreters"]:
            log.debug(f"{info.path}: Found versioned interpreter '{name}'")
            info.identity = config["interpreters"][name_without_version]
            return

        # Try removing the extension (such as "python.exe" on Windows).
        stem = path.stem
        if stem in config["interpreters"]:
            log.debug(f"{info.path}: Found base interpreter '{name}'")
            info.identity = config["interpreters"][stem]
            return
