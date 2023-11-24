import pathlib

import pytest

import chipshot.exceptions
import chipshot.reader.prolog

variants = pytest.mark.parametrize(
    "variant",
    (
        (pytest.param("bogus", id="suffix")),
        (pytest.param("bogus.bogus", id="suffixes")),
    ),
)


def test_prolog_success(fs, default_config):
    path = pathlib.Path("script.sh")
    fs.create_file(path, contents=b"#!/bin/sh\n\necho success")

    info = chipshot.reader.read(path, default_config)
    assert info.prolog == "#!/bin/sh"
    assert info.contents == "\necho success"


def test_prolog_empty_pattern(bogus_file, bogus_config):
    bogus_file.contents = "anything"
    bogus_config["extension"]["bogus"]["prolog"] = "bogus"
    bogus_config["prolog"]["bogus"]["pattern"] = ""

    chipshot.reader.prolog.handle(bogus_file, bogus_config)

    assert bogus_file.prolog == ""
    assert bogus_file.contents == "anything"


@variants
def test_prolog_not_first_line(bogus_file, bogus_config, variant, caplog):
    bogus_file.contents = "# first\n#!/bin/sh\necho success"
    bogus_config["prolog"][variant] = bogus_config["prolog"]["hashbang"]
    bogus_config["extension"][variant]["prolog"] = variant

    chipshot.reader.prolog.handle(bogus_file, bogus_config)

    assert (
        "A prolog was found, but not at the beginning of the document." in caplog.text
    )
    assert bogus_file.prolog == ""
    assert bogus_file.contents == "# first\n#!/bin/sh\necho success"


def test_prolog_not_configured(bogus_file, bogus_config):
    bogus_config["extension"] = {}
    bogus_file.contents = "#!/bin/sh\necho success"

    chipshot.reader.prolog.handle(bogus_file, bogus_config)

    assert bogus_file.prolog == ""
    assert bogus_file.contents == "#!/bin/sh\necho success"


@variants
def test_prolog_no_newline(bogus_file, bogus_config, variant):
    bogus_config["prolog"][variant]["pattern"] = "^#!.+?;"
    bogus_config["extension"][variant]["prolog"] = variant
    bogus_file.contents = "#!/bin/sh; echo success"

    with pytest.raises(chipshot.exceptions.PrologRequiresTrailingNewline):
        chipshot.reader.prolog.handle(bogus_file, bogus_config)
