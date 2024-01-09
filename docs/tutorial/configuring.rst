..
    This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
    Copyright 2022-2024 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT

Configuring Chipshot
####################

Chipshot needs to know what header text to put at the tops of your files.
This is configured in one of two files by default:

*   ``.chipshot.toml``
*   ``pyproject.toml``

This section of the documentation will show you
how to configure Chipshot using ``.chipshot.toml``.


Header Templates
================

Open your favorite text editor and put this text into it:

..  code-block:: toml

    [chipshot]
    template = """
    Copyright {{ year }} Developer <dev@domain.example>
    """

Save the file as ``.chipshot.toml``.
Then, at the command line, run Chipshot
and pass a directory containing source code files as the first argument.
By default, Chipshot won't update any files;
it will simply tell you what it believes it should do with the file.

..  code-block:: console

    $ chipshot src/
    INFO: src/no_header.py: Adding header (no original header found)
    INFO: src/has_comments_but_no_header.py: Adding header (29.46% similarity)
    INFO: src/has_header_with_different_email.py: Updating header (96.46% similarity)

If the output looks correct to you,
add the ``--update`` flag to have Chipshot make changes to the files.

..  code-block:: console

    $ chipshot --update src/
    INFO: src/no_header.py: Adding header (no original header found)
    INFO: src/has_comments_but_no_header.py: Adding header (29.46% similarity)
    INFO: src/has_header_with_different_email.py: Updating header (96.46% similarity)
