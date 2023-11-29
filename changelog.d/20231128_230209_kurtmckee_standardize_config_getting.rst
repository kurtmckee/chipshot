Changed
-------

*   Standardize how configurations for styles, prologues, and templates are found.

    This helps ensure that the most specific configuration for a given file is always used.
    For example, code interacting with a file with two extensions (like ``.jinja.html``)
    will consistently find a configuration for ``.jinja.html`` before ``.html``.

*   Rename ``prolog`` to ``prologue`` everywhere.

*   The configuration keys ``style`` and ``prolog`` are now ``styles`` and ``prologues``.
