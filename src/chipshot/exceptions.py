# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT


class ChipshotError(Exception):
    pass


class BadConfig(ChipshotError):
    """The configuration does not match the expected schema."""


class ConfigNotFound(ChipshotError):
    """A config file was successfully loaded but no Chipshot configuration was found."""


class NoTemplateDefined(ChipshotError):
    """No *template* or *template_path* was found."""


class FileDecodeError(ChipshotError):
    """A file could not be decoded."""


class FileDoesNotMatchBOMEncoding(FileDecodeError):
    """A file could not be decoded using the encoding specified by its BOM."""


class FileDoesNotMatchConfiguredEncoding(FileDecodeError):
    """A file could not be decoded using the encoding specified in the config."""


class InconsistentNewlines(ChipshotError):
    """The file contains multiple newline styles."""


class PrologueRequiresTrailingNewline(ChipshotError):
    """The prologue must end with a trailing newline."""


class HeaderBlockRequiresTrailingNewline(ChipshotError):
    """The header block must end in a newline."""
