Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

v2.1.3
--------
2023-07-21:
    - require minimum python 3.8
    - remove python 3.7 tests
    - introduce PEP517 packaging standard
    - introduce pyproject.toml build-system
    - remove mypy.ini
    - remove pytest.ini
    - remove setup.cfg
    - remove setup.py
    - remove .bettercodehub.yml
    - remove .travis.yml
    - update black config
    - clean ./tests/test_cli.py
    - add codeql badge
    - move 3rd_party_stubs outside the src directory to ``./.3rd_party_stubs``
    - add pypy 3.10 tests
    - add python 3.12-dev tests

v2.1.2.2
--------
2022-06-02: setup github actions v3, python3.10 test matrix

v2.1.1
--------
2020-10-09: service release
    - update travis build matrix for linux 3.9-dev
    - update travis build matrix (paths) for windows 3.9 / 3.10

v2.1.0
--------
2020-08-08: service release
    - fix documentation
    - fix travis
    - deprecate pycodestyle
    - implement flake8

v2.0.9
---------
2020-08-07: implement flake8 - transitional

v2.0.8
---------
2020-08-01: fix pypi deploy

v2.0.7
---------
2020-07-31: fix travis build

v2.0.6
---------
2020-07-31: fix environ.pop issue in doctest

v2.0.5
---------
2020-07-29: feature release
    - use the new pizzacutter template
    - use cli_exit_tools

v2.0.4
---------
2020-07-23: patch release
    - adopt lib_log_utils 0.3.0

v2.0.3
---------
2020-07-16: feature release
    - fix cli test
    - enable traceback option on cli errors

v2.0.2
---------
2020-07-16: patch release
    - fix cli test
    - enable traceback option on cli errors

v2.0.1
---------
2020-07-05 : patch release
    - fix typos
    - manage project with PizzaCutter
    - restructured cli entry points

v2.0.0
---------
2020-06-19
    - new CLI Interface
    - avoid recursive imports
    - manage the project with lib_travis_template

v1.0.9
---------
    - drop support for configfiles
    - update documentation
    - implement --version on commandline
    - test commandline registration
    - strict mypy typechecking

1.0.8
---------
    - drop python 2.7 / 3.4 support
    - implement --inplace option
    - implement --quiet option
    - implement multiline string replacement
    - extend documentation


1.0.2
---------
2019-04-28: fix import errors

1.0.1
---------
2019-04-28: add empty line at the end of the assembled documentation, to be able to add CHANGES.rst with setup.py

1.0.0
---------
2019-04-19: Initial public release, PyPi Release
