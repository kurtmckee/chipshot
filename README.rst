..
    This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
    Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


Chipshot
########

*Set up game-winning headers!*

----

Chipshot helps standardize header information in software development files.

Its target goal is to ensure that copyright dates are standardized
and that licensing information is present.

It supports a wide range of file formats,
including source code and documentation formats.
It purposely does not support configuration file formats by default
(such as TOML, INI, or YAML)
but can be configured to support those, too.


Sample configuration
====================

Create a file named ``.chipshot.toml`` with the following content:

..  code-block:: toml

    [chipshot]
    template = """
    Copyright 2021-{{ year }} Developer or Company
    Released under the terms of the MIT license.
    SPDX-License-Identifier: MIT
    """

You can then run ``chipshot path1 path2`` to see what files will be modified.
If you're satisfied, run ``chipshot --update path1 path2`` to update the files.


Pre-commit hooks
================

Chipshot offers two pre-commit hooks to help you manage your projects:

*   ``check-headers``
*   ``update-headers``

Here's a sample configuration for ensuring your files have correct headers:

..  code-block:: yaml

    # .pre-commit-config.yaml
    repos:
      - repo: 'https://github.com/kurtmckee/chipshot'
        rev: 'v0.4.0'
        hooks:
          - id: 'update-headers'
