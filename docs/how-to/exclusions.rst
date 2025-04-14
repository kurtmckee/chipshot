..
    This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
    Copyright 2022-2025 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT

How To Exclude Specific Files
#############################

In some circumstances, you may want to exclude certain files.
For example, some tools use configuration files written in Python or Ruby,
and as configuration files you may not want to standardize their headers.

Chipshot supports a global ``"exclusions"`` configuration option.
It supports a list of files that Chipshot must ignore.

The example below will tell Chipshot to exclude ``conf.py``,
which is the standard name for a Sphinx configuration file;
it will also ignore ``Gruntfile.js``,
which is a common name for a Grunt configuration file;
it will also ignore everything in the ``tests/`` subdirectory.

..  code-block:: toml

    [chipshot]
    exclusions = [
        "docs/conf.py",
        "Gruntfile.js",
        "tests/",
    ]
