import pathlib
import textwrap
import tomllib


def main() -> None:
    root = pathlib.Path(__file__).parent.parent
    toml = tomllib.loads((root / "pyproject.toml").read_text())
    version = toml["project"]["version"]
    this_file = pathlib.PurePosixPath(pathlib.Path(__file__).relative_to(root))
    text = f"""
    ..  DO NOT EDIT THIS CODE BLOCK!
    ..  INSTEAD, EDIT {this_file}.

    ..  code-block:: yaml

        # Filename: .pre-commit-config.yaml
        repos:
          - repo: 'https://github.com/kurtmckee/chipshot'
            rev: 'v{version}'
            hooks:
              - id: 'update-headers'
    """

    print(textwrap.dedent(text))
