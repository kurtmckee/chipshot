# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pathlib
import sys


def main() -> None:
    root = pathlib.Path(__file__).parent.parent
    chipshot_path = root / "src"
    sys.path.insert(0, str(chipshot_path))
    import chipshot.cli

    docs_path = root / "docs"
    chipshot_configs = docs_path.rglob("**.chipshot.toml")

    for chipshot_config in chipshot_configs:
        name = chipshot_config.with_suffix("").with_suffix("").name
        targets = chipshot_config.parent.glob(f"{name}.*")
        for target in targets:
            if target == chipshot_config:
                continue
            print(f"Checking {target} for updates")
            args = ("--config", str(chipshot_config), "--update", str(target))
            chipshot.cli.run(args, standalone_mode=False)


if __name__ == "__main__":
    main()
