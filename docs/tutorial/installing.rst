..
    This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
    Copyright 2022-2024 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT

Installing Chipshot
###################

Chipshot is published to the Python Package Index (PyPI).
If you have a preferred way to install Python packages,
feel free to use that method.


pipx
====

`pipx`_ is an excellent way to install Python applications.
If you already have pipx installed on your system,
you can use it to install Chipshot.

..  code-block:: console

    $ pipx install chipshot
    $ chipshot --version


pip
===

If you have Python installed, then you have pip installed.
However, you should avoid installing Chipshot into your system Python's packages.

There are two methods you can follow:

#.  Create a virtual environment
#.  Install Chipshot in your Python user packages

The virtual environment method is preferable
because it will help isolate Chipshot's Python dependencies
and reduce the possibility of a conflict in dependency versions,
but you will have to activate the virtual environment
each time you want to use Chipshot.

Virtual Environment Method
--------------------------

..  rubric:: Linux/macOS
..  code-block:: console

    $ python -m venv venv
    $ . venv/bin/activate
    (venv) $ python -m pip install chipshot
    (venv) $ chipshot --version

..  rubric:: Windows
..  code-block:: doscon

    C:\Users\Me> python -m venv venv
    C:\Users\Me> venv\Scripts\activate.bat
    (venv) C:\Users\Me> python -m pip install chipshot
    (venv) C:\Users\Me> chipshot --version

Python User Directory Method
----------------------------

..  rubric:: Linux/macOS/Windows
..  code-block:: console

    $ python -m pip install --user chipshot
    $ chipshot --version


..  Links
..  -----
..
..  _pipx: https://pypa.github.io/pipx/
