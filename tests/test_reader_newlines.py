import pytest

import chipshot.reader.newlines
from chipshot import exceptions


@pytest.mark.parametrize("newline", ("\n", "\r", "\r\n"))
def test_newlines(bogus_file, default_config, newline):
    contents = f"print(1){newline}print(2){newline}print(3)"
    bogus_file.contents = contents

    chipshot.reader.newlines.handle(bogus_file)
    assert bogus_file.newlines == newline
    assert bogus_file.contents == "print(1)\nprint(2)\nprint(3)"


def test_inconsistent_newlines(bogus_file, default_config):
    bogus_file.contents = "print(1)\nprint(2)\rprint(3)\r\nprint(4)"

    with pytest.raises(exceptions.InconsistentNewlines):
        chipshot.reader.newlines.handle(bogus_file)
