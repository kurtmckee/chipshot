Fixed
-----

*   Strip the executable extension (like ``.exe``) before removing version numbers
    when identifying a file type based on its hashbang.

    This resolves a bug that prevented identification of version-specific
    executable names, like ``python3.14.exe``, on Windows platforms.
