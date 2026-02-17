..
    This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
    Copyright 2022-2026 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT

Configuration
#############

Chipshot supports several top-level config keys:

*   :ref:`ref-config-prologues`
*   :ref:`ref-config-styles`
*   :ref:`ref-config-extensions`
*   :ref:`ref-config-interpreters`
*   :ref:`ref-config-types`


..  _ref-config-prologues:

``prologues``
=============

Many types of files require the first line (or lines) to have specific content.
Chipshot refers to these mandatory first lines as "prologues",
and uses regular expressions to identify them.

The ``prologues`` key maps names to regular expression patterns.
The format is:

..  code-block:: toml

    [chipshot.prologues.PROLOGUE_NAME]
    pattern = "REGULAR EXPRESSION"

File configurations then refer to the prologues by name.

..  note::

    Regular expressions often contain backslashes.
    These must be escaped to prevent errors in the TOML file.

    See the :ref:`XML DOCTYPE example <ref-config-prologue-example-xml-doctype>`
    to see an example of backslash escapes for TOML.


Default prologues
-----------------

Chipshot ships with these prologues already available:

..  [[[cog
..
..  ]]]



..  [[[end]]]

``hashbang``
    This is the standard hashbang that shells rely on
    to determine what executable to run when a script is executed.

``hashbang-with-encoding``
    This prologue recognizes hashbang lines at the start of scripts,
    but it also recognizes encoding comments that some interpreters rely on.

    For example, Python and Ruby both recognize encoding comments
    that are cause them to decode the rest of the file
    in a different encoding, like SHIFT-JIS.

Example: hashbang prologues
---------------------------

It is common for the first line in a file contain a hashbang comment
so that the correct interpreter can be used to execute the script.
The example below shows the hashbang line for a Javascript file:

..  literalinclude:: examples/config-prologues-hashbang/example.js
    :language: js

Here's an example of a prologue definition named ``"hashbang"``:

..  literalinclude:: examples/config-prologues-hashbang/example.chipshot.toml
    :language: toml
    :start-at: [chipshot.prologues.hashbang]
    :end-before: #end

Later in the config, for a file extension like ``.js``,
the prologue pattern can be referred to by name:

..  literalinclude:: examples/config-prologues-hashbang/example.chipshot.toml
    :language: toml
    :start-at: [chipshot.extensions.js]
    :end-before: #end


..  _ref-config-prologue-example-xml-doctype:

Example: XML DOCTYPE prologues
------------------------------

XML DOCTYPE declarations must be the first text in the file.
The DOCTYPE declarations contain literal question marks,
which have a special meaning in regular expressions.

..  code-block:: xml

    <?xml version="1.1"?>

Because question marks are special characters in regular expressions,
the question marks must be escaped using backslashes.
Here's what the regular expression might look like:

..  code-block:: text

    ^<\?xml(.|\n)+\?>$

Those three backslashes (``\?``, ``\n``, and ``\?``)
must be escaped with backslashes again
when writing the regular expression in the TOML config:

..  code-block:: toml

    [chipshot.prologues.xml_declaration]
    pattern = "^<\\?xml(.|\\n)+\\?>$"


..  _ref-config-styles:

``styles``
==========

Different file types use different comment formats.
Chipshot refers to these comment formats as "styles".

The ``styles`` key maps style names to comment format definitions,
and supports configuration of prefixes and suffixes for blocks and lines.
It is not necessary to specify all four configuration keys.

..  code-block:: toml

    [chipshot.styles.STYLE_NAME]
    block_prefix = "STRING"
    line_prefix = "STRING"
    line_suffix = "STRING"
    block_suffix = "STRING"

File configurations then refer to the styles by name.

..  warning::

    Where possible, it is recommended to prefer comment styles
    that cannot be closed prematurely by the template text.

    For example, the following style definition would work for C++ files:

    ..  code-block:: toml

        [chipshot.styles.slash-star]
        block_prefix = "/*\n"
        block_suffix = "\n*/"

    However, if the template text contained ``*/``
    it would end the comment prematurely:

    ..  code-block:: cpp

        /*
        The template may contain */, if (a_problem == "desired").
        */


Example: Full rendering
=======================

The example below shows a full rendering
of how Chipshot uses the ``styles`` configuration keys.

Given these configuration keys:

..  literalinclude:: examples/config-styles-render/bare.chipshot.toml
    :start-at: [chipshot.styles.full_rendering]
    :end-before: #end
    :language: toml

and given this template text:

..  literalinclude:: examples/config-styles-render/bare.chipshot.toml
    :start-after: template
    :end-before: """
    :language: text

Chipshot would render the template text in this way:

..  literalinclude:: examples/config-styles-render/bare.txt
    :language: text

It is possible to add newlines to the block prefix and suffix.

..  literalinclude:: examples/config-styles-render/newlines.chipshot.toml
    :start-at: [chipshot.styles.full_rendering]
    :end-before: #end
    :language: toml

..  literalinclude:: examples/config-styles-render/newlines.txt
    :language: text


..  _ref-config-extensions:

``extensions``
==============

Most file types conventionally have file extensions.
(There are some exceptions to this convention.
See :ref:`ref-config-interpreters` for more information.)

The ``extensions`` key maps file extensions to prologue names and style names.
The format is:

..  code-block:: toml

    [chipshot.extensions.EXTENSION]
    prologue = "PROLOGUE_NAME"
    style = "STYLE_NAME"

See :ref:`ref-config-prologues` and :ref:`ref-config-styles`
for information about configuring a prologue name or a style name.

In some cases, files may have multiple extensions.
These can be represented by adding double quotes around the full extension:

..  code-block:: toml

    [chipshot.extensions."EXT.ENS.ION"]
    prologue = "PROLOGUE_NAME"
    style = "STYLE_NAME"


Example: HTML template languages
--------------------------------

There are many template languages for HTML, each with its own comment style.

It may be desirable to add comments in the template language's style
so that the rendered HTML doesn't contain HTML comments.

Here's an example of style definitions for the Jinja and Mako template languages,
together with the ``extensions`` definitions needed to use them.

..  literalinclude:: examples/config-styles-html-templates/example.chipshot.toml
    :start-after: #start
    :end-before: #end
    :language: toml


A file named ``base.jinja.html`` would use the "jinja-html" style:

..  literalinclude:: examples/config-styles-html-templates/example.jinja.html
    :language: jinja

A file named ``base.mako.html`` would use the "mako-html" style:

..  literalinclude:: examples/config-styles-html-templates/example.mako.html
    :language: mako

Finally, a file with the name ``index.html`` would fall back to the default HTML style:

..  literalinclude:: examples/config-styles-html-templates/example.html
    :language: html


..  _ref-config-interpreters:

``interpreters``
================

It is common to have executable scripts that lack a file extension.
If the first line is a hashbang, Chipshot will attempt to identify the file type
based on the executable listed in the hashbang.

Chipshot maps (possibly normalized) executable names to file types
in the ``interpreters`` config key,
and then maps file types to prologues and styles
in the :ref:`ref-config-types` config key.

..  code-block:: toml

    [chipshot.interpreters]
    EXECUTABLE = "TYPE"

See the :ref:`ref-config-types` documentation, below,
for information about configuring file types.


Normalization
-------------

Chipshot tries to recognize file types by iteratively normalizing components
of the hashbang line and then checking to see if the normalized executable name
is set in the ``interpreters`` config key.

For the discussion below, this hashbang line is used:

..  code-block:: shell

    #!/path/to/EXECUTABLE1.EXE ARGUMENT2

The hashbang is split by whitespace, and each piece is then interpreted
as a possible executable path.

#.  The exact executable name in lowercase (``executable1.exe``) is checked.
#.  The extension, if any, is stripped (``executable1``) and the name is checked.
#.  Trailing version numbers are stripped (``executable``) and checked.


Example: Python hashbangs
-------------------------

The following hashbang lines all normalize to the ``python`` file type:

..  code-block:: shell

    #!/usr/bin/python
    #!/usr/bin/python2
    #!/usr/bin/env python3.13
    #!"C:\Program Files\Python312\python3.13.exe"

Given the following ``interpreters`` config,
the ``python`` executable name will map to the the ``python`` file type:

..  code-block:: toml

    [chipshot.interpreters]
    python = "python"


..  _ref-config-types:

``types``
=========

The ``types`` config associates prologues and styles with file types.
This config key is similar to the :ref:`ref-config-extensions` configurations,
but the file types were identified by examining their hashbang lines.

The syntax is:

..  code-block:: toml

    [chipshot.types.TYPE]
    prologue = "PROLOGUE"
    style = "STYLE"

The ``TYPE`` must have a ``prologue`` configured
so that file type's hashbang is preserved.

It is likely that the ``prologue`` value will frequently be ``hashbang``.
However, in some cases a more complicated prologue must be configured.
For example, both Python and Ruby support optional file encoding comments
immediately after the hashbang line, and such comments must be preserved.

..  seealso::

    *   :ref:`ref-config-prologues`
    *   :ref:`ref-config-styles`


Example: A TCL script file type
-------------------------------

Consider a hashbang that refers to a ``tclsh9.0`` executable:

..  code-block:: shell

    #!/usr/local/tclsh9.0

Due to executable name normalization,
the Chipshot configuration could refer to ``tclsh9.0``, ``tclsh9``, or ``tclsh``.
For this example, the executable name ``tclsh`` will be chosen.

TCL uses hash symbols (``#``) to begin comments, so the ``hash`` style will be configured.
It is also important to configure the ``prologue``

Remember: Chipshot maps executable names to file types,
and then maps file types to prologues and styles.

..  code-block:: toml

    [chipshot.interpreters]
    tclsh = "tcl"

    [chipshot.types.tcl]
    prologue = "hashbang"
    style = "hash"
