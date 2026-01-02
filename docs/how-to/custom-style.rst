..
    This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
    Copyright 2022-2026 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT

How To Create a Custom Style
############################

Chipshot supports a wide variety of header styles
for many different programming and markup languages,
but you might want to create a new style.

This document walks you through the process of creating a new style.

*   :ref:`variables`
*   :ref:`create`

..  _variables:

The Four Control Variables
==========================

Chipshot anticipates that all header styles require
some kind of document-specific comment markup,
and that the comment markup will follow some of these rules:

*   There may be some kind of markup that introduces the comment block.

    Some languages support multiline comments
    which are introduced with start and end markers.
    For example, Typescript supports ``/*`` and ``*/`` markers.

    Some languages only use a dedicated start marker.
    For example, ReStructuredText uses ``..`` as its start marker
    and relies on blank lines to signal the end of the comment.

    Chipshot uses the terms ``block_prefix`` and ``block_suffix``
    to refer to the start and end markers.

*   Individual lines may need to prefixed with some kind of markup.

    Some languages only support single-line comments.
    For example, PostgreSQL comment lines must start with ``--``.

    Chipshot support line prefixes and, if desired, line suffixes.
    It uses the terms ``line_prefix`` and ``line_suffix``
    to refer to the beginning-of-line and end-of-line markers.


..  _create:

Create a New Style
==================

All styles in Chipshot are created under the ``styles`` configuration key,
and then file extensions are configured to use the new style.
(It is not supported to define the style in the file extension configuration.)

Let's say you want to add support for PHP files.
First, define the style in ``.chipshot.toml``.
In the example below, the style name is defined as ``my-php-style``.
Escaped newlines must be embedded in the block prefix and suffix
to ensure that they render nicely.

..  code-block:: toml

    [chipshot.styles.my-php-style]
    block_prefix = "<?php\n/*\n"
    line_prefix = " * "
    block_suffix = "\n */\n?>"

Then, configure files with the "php" extension to use the new style.

..  code-block:: toml

    [chipshot.extensions.php]
    style = "my-php-style"

Here's the complete ``.chipshot.toml`` file, including a template:

..  code-block:: toml

    [chipshot]
    template = """
    Copyright 2022-{{ year }} Company Name
    Licensed under the terms of the MIT License.
    """

    [chipshot.styles.my-php-style]
    block_prefix = "<?php\n/*\n"
    line_prefix = " * "
    block_suffix = "\n */\n?>"

    [chipshot.extensions.php]
    style = "my-php-style"

Run Chipshot with the ``--update`` flag and pass it a PHP file to update.
For example:

..  code-block:: console

    $ chipshot --update example.php

The header will be added at the top of the file like this:

..  code-block:: php

    <?php
    /*
     * Copyright 2022-2023 Company Name
     * Licensed under the terms of the MIT License.
     */
    ?>
