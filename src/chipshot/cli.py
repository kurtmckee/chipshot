# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import pathlib
import textwrap
import typing

import click
import click.exceptions

from . import compare, config, logger, reader, render, writer


@click.command()
@click.help_option("-h", "--help")
@click.version_option(
    None,
    "-V",
    "--version",
    prog_name="Chipshot",
    message="%(prog)s v%(version)s",
)
@click.option(
    "-c",
    "--config",
    "config_file",
    help=textwrap.dedent(
        """
        The Chipshot configuration file to use.

        If unspecified, '.chipshot.toml' in the current directory will be loaded.
        If that doesn't exist, 'pyproject.toml' will be tried next.

        Chipshot's default values will always be loaded first.
    """
    ),
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--update",
    is_flag=True,
    help="Update files in-place.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose output.",
)
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
)
def run(
    config_file: str | None, update: bool, verbose: bool, paths: tuple[str]
) -> None:
    """Chipshot -- Set up game-winning headers!"""

    files_updated = False

    # Set up logging.
    logger.setup(enable_debug=verbose)
    log = logging.getLogger(__name__)

    # Load the configuration.
    if config_file is None:
        configuration = config.load()
    else:
        configuration = config.load(pathlib.Path(config_file))

    for path in _get_files(paths, configuration):
        info = reader.read(path, configuration)

        # If the file is empty, do nothing.
        if not info.raw_contents:
            log.debug(f"{path}: Empty file (no-op)")
            continue

        info.header = render.render_header(path, configuration)

        # If the headers match, do nothing.
        if info.header == info.original_header:
            log.debug(f"{path}: Headers match (no-op)")
            continue

        # If this is a net-new header, log that information.
        if info.header and not info.original_header:
            log.info(f"{path}: Adding header (no original header found)")
            files_updated = True

        # If there is an existing header, it might be kept or replaced.
        else:
            similarity = compare.get_similarity(info.original_header, info.header)
            percentage = f"{similarity*100:0.2f}%"
            # If the headers are sufficiently similar, replace the existing header.
            if similarity > 0.90:
                log.info(f"{path}: Updating header ({percentage} similarity)")
                files_updated = True
                info.original_header = ""
            # The headers are sufficiently different. Keep the original header.
            else:
                log.info(f"{path}: Adding header ({percentage} similarity)")
                files_updated = True

        if update:
            writer.write(info)

    if files_updated:
        raise click.exceptions.Exit(1)


def _get_files(
    paths: tuple[str], configuration: dict[str, typing.Any]
) -> typing.Generator[pathlib.Path, None, None]:
    exclusions: list[pathlib.Path] = [
        pathlib.Path(exclusion) for exclusion in configuration.get("exclusions", [])
    ]
    for path_string in paths:
        path = pathlib.Path(path_string)

        # Prepare for iteration.
        sub_paths: typing.Iterable[pathlib.Path]
        if path.is_file():
            sub_paths = [path]
        else:
            sub_paths = path.rglob("*")

        for sub_path in sub_paths:
            # Exclude directories.
            if not sub_path.is_file():
                continue

            # Ensure that there's a configuration to apply to this file.
            if not _get_suffixes(sub_path) & configuration["extensions"].keys():
                continue

            # Ensure that the path is not excluded.
            if any(sub_path == exclusion for exclusion in exclusions):
                continue

            yield sub_path


def _get_suffixes(path: pathlib.Path) -> set[str]:
    return {"".join(path.suffixes[-n:])[1:] for n in range(1, len(path.suffixes) + 1)}
