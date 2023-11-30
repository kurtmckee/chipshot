import codecs

import pytest

import chipshot.exceptions
import chipshot.reader.encoding


@pytest.mark.parametrize(
    "bom, encoding",
    (
        (b"", "utf-8"),
        (codecs.BOM_UTF8, "utf-8"),
        (codecs.BOM_UTF16_BE, "utf-16-be"),
        (codecs.BOM_UTF16_LE, "utf-16-le"),
        (codecs.BOM_UTF32_BE, "utf-32-be"),
        (codecs.BOM_UTF32_LE, "utf-32-le"),
    ),
)
def test_bom(bogus_file, default_config, bom, encoding):
    raw_contents = bom + "success".encode(encoding)
    bogus_file.raw_contents = raw_contents
    bogus_file.encoding = "utf-8"

    chipshot.reader.encoding.handle(bogus_file, default_config)

    assert bogus_file.encoding == encoding
    assert bogus_file.bom == bom
    assert bogus_file.contents == "success"


@pytest.mark.parametrize(
    "bom, exception",
    (
        (b"", chipshot.exceptions.FileDoesNotMatchConfiguredEncoding),
        (codecs.BOM_UTF8, chipshot.exceptions.FileDoesNotMatchBOMEncoding),
    ),
)
def test_decode_errors(bogus_file, default_config, bom, exception):
    bogus_file.raw_contents = bom + b"\xf0"
    bogus_file.encoding = "utf-8"

    with pytest.raises(exception):
        chipshot.reader.encoding.handle(bogus_file, default_config)
