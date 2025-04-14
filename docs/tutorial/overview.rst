..
    This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
    Copyright 2022-2025 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT

An overview of Chipshot's features
##################################

Chipshot helps ensure source code headers are consistent.
You tell it what the header text should be using a *template*,
and it will render the header as a comment based on the file extension.

Not all file formats use the same types of comment styles or conventions,
so Chipshot works to respect:

*   :ref:`comment-styles`
*   :ref:`prologues`
*   :ref:`boms`
*   :ref:`newlines`

In addition, Chipshot is flexible, and supports a great deal of customization:

*   `multiple-templates`
*   :ref:`custom-styles`


Throughout this overview, the following header template will be used:

..  code-block:: text

    Copyright 2022-{{ year }} Company Name
    Licensed under the terms of the MIT license.

Note that ``{{ year }}`` will be rendered as ``2023`` in this document.


..  _comment-styles:

Comment styles
==============

Different programming and markup languages have different comment styles.
Here is a small sample of comment styles that Chipshot supports by default.

..  rubric:: Python
..  code-block:: python

    # Copyright 2022-2023 Company Name
    # Licensed under the terms of the MIT license.

..  rubric:: ReStructuredText
..  code-block:: rst

    ..
        Copyright 2022-2023 Company Name
        Licensed under the terms of the MIT license.

..  rubric:: SQL
..  code-block:: sql

    -- Copyright 2022-2023 Company Name
    -- Licensed under the terms of the MIT license.

..  rubric:: XML
..  code-block:: xml

    <!--
        Copyright 2022-2023 Company Name
        Licensed under the terms of the MIT license.
    -->


..  _prologues:

Document Prologues
==================

Some files have mandatory *prologues* -- content that MUST appear on the first line or lines.
For example, many executable script files must start with a hashbang line
so the operating system knows how to execute the file.

If Chipshot finds a hashbang in a file format that supports it,
Chipshot will always add or update headers after the hashbang:

..  rubric:: Example: A hashbang in a NodeJS shell script
..  code-block:: js

    #!/usr/bin/env node

    // Copyright 2022-2023 Company Name
    // Licensed under the terms of the MIT license.

    console.log("Hello, World!");

Executable scripts aren't the only place where the first line is important;
XML requires declarations to appear before comments, too.

..  rubric:: Example: An XML declaration
..  code-block:: xml

    <?xml version="1.0"?>

    <!--
        Copyright 2022-2023 Company Name
        Licensed under the terms of the MIT license.
    -->


..  _boms:

Unicode Byte Order Marks
========================

Some programming languages and file formats rely on Unicode byte order marks (BOMs)
to enable Unicode features. For example, AutoHotkey relies on UTF-8 BOMs
to indicate when it should switch from ANSI to Unicode.

When Chipshot encounters a byte order mark in a file
it will always decode the file using the encoding indicated by the BOM.
If Chipshot adds or updates a header,
it will always retain the original BOM.

..  note::

    Chipshot does not add nor remove BOMs;
    it only retains existing BOMs.


..  _newlines:

Newlines
========

Different files in your repository may use different newline styles.
When Chipshot updates headers, it respects each file's existing newline style.

..  note::

    Chipshot does not standardize newlines;
    it only retains the existing newline style.


..  _custom-styles:

Custom Styles
=============

Chipshot allows custom comment styles,
so it's possible to add new styles as needed.

..  rubric:: Example: A custom style in ``.chipshot.toml`` for PHP scripts
..  code-block:: toml

    [chipshot.extensions.php]
    block_prefix = "<?php\n"
    line_prefix = "// "
    block_suffix = "\n?>"

This will result in a header rendered like this:

..  rubric:: Example: A rendered PHP header
..  code-block:: php

    <?php
    // Copyright 2022-2023 Company Name
    // Licensed under the terms of the MIT license.
    ?>
