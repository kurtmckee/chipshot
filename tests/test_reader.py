import pathlib

import chipshot.reader


def test_empty_file(fs, default_config):
    path = pathlib.Path("sample.css")
    fs.create_file(path, contents="")

    info = chipshot.reader.read(path, default_config)
    assert info.raw_contents == b""
    assert info.bom == b""
    assert info.encoding == ""
    assert info.prologue == ""
    assert info.original_header == ""
    assert info.contents == ""
    assert info.newlines == ""
    assert info.path == path
