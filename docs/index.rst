..  rst-class:: visually-hidden

Welcome to the Chipshot documentation
#####################################

..  image:: _static/banner.png
    :alt: The Chipshot logo, with a soccer ball shooting up and away from the project name.

Chipshot helps you standardize headers in your source code.
Its aim is to help ensure that all source files have excellent headers
with accurate copyright and license information.
If it can help you achieve your goals, then it will have done its job!

Example
=======

Chipshot respects byte order marks, newlines, and document prologues
(like hashbangs and XML declarations) when adding and updating headers.
Its default configuration supports many different file types
so it's easy to get started with a minimal configuration file.

..  rubric:: ``.chipshot.toml``
..  code-block:: toml

    [chipshot]
    template = """
    Copyright 2022-{{ year }} Company Name <oss@company.example>
    SPDX-License-Identifier: MIT
    """

Headers will be rendered as comments based on the file extension.

..  rubric:: Python
..  code-block:: python

    # Copyright 2022-2023 Company Name <oss@company.example>
    # SPDX-License-Identifier: MIT

..  rubric:: C
..  code-block:: c

    /*
     * Copyright 2022-2023 Company Name <oss@company.example>
     * SPDX-License-Identifier: MIT
     */


Getting Started
===============

..  toctree::
    :maxdepth: 1

    tutorial/overview
    tutorial/installing
    tutorial/configuring

*   Default comment styles gallery


How-To Guides
=============

..  toctree::
    :maxdepth: 1

    how-to/custom-style

*   How to integrate Chipshot in your everyday development


Reference
=========

..  toctree::
    :maxdepth: 1

    reference/boms
    colophon
    license

*   Configuration file format
*   Pre-commit hooks
*   CLI options
