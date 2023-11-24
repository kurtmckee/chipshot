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

Create a directory that will contain your header template.
For example, the directory might be named ``assets/headers``.

Then, create a text file that will contain your header template,
such as ``global.txt``.
You can use ``{{ year }}`` as a stand-in for the current year.

..  code-block:: text

    Copyright 2021-{{ date }} Developer or Company
    Released under the terms of the MIT license.
    SPDX-License-Identifier: MIT

Next, add the following configuration to ``pyproject.toml``:

..  code-block:: toml

    [tool.chipshot]
    template_root = "assets/headers"
    template = "global.txt"

You can then run ``chipshot path1 path2`` to see what files will be modified.
If you're satisfied, run ``chipshot --update path1 path2`` to update the files.
