rst_include
===========


Version v2.1.3 as of 2023-07-21 see `Changelog`_

|build_badge| |codeql| |license| |pypi|
|pypi-downloads| |black| |codecov| |cc_maintain| |cc_issues| |cc_coverage| |snyk|



.. |build_badge| image:: https://github.com/bitranox/rst_include/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/bitranox/rst_include/actions/workflows/python-package.yml


.. |codeql| image:: https://github.com/bitranox/rst_include/actions/workflows/codeql-analysis.yml/badge.svg?event=push
   :target: https://github.com//bitranox/rst_include/actions/workflows/codeql-analysis.yml

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License

.. |jupyter| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/bitranox/rst_include/master?filepath=rst_include.ipynb

.. for the pypi status link note the dashes, not the underscore !
.. |pypi| image:: https://img.shields.io/pypi/status/rst-include?label=PyPI%20Package
   :target: https://badge.fury.io/py/rst_include

.. |codecov| image:: https://img.shields.io/codecov/c/github/bitranox/rst_include
   :target: https://codecov.io/gh/bitranox/rst_include

.. |cc_maintain| image:: https://img.shields.io/codeclimate/maintainability-percentage/bitranox/rst_include?label=CC%20maintainability
   :target: https://codeclimate.com/github/bitranox/rst_include/maintainability
   :alt: Maintainability

.. |cc_issues| image:: https://img.shields.io/codeclimate/issues/bitranox/rst_include?label=CC%20issues
   :target: https://codeclimate.com/github/bitranox/rst_include/maintainability
   :alt: Maintainability

.. |cc_coverage| image:: https://img.shields.io/codeclimate/coverage/bitranox/rst_include?label=CC%20coverage
   :target: https://codeclimate.com/github/bitranox/rst_include/test_coverage
   :alt: Code Coverage

.. |snyk| image:: https://snyk.io/test/github/bitranox/rst_include/badge.svg
   :target: https://snyk.io/test/github/bitranox/rst_include

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/rst-include
   :target: https://pypi.org/project/rst-include/
   :alt: PyPI - Downloads

since You can not include files into RST files on github or PyPi, You can resolve such imports with this software.

That means You can locally write Your RST documents (for instance with pycharm) and use there
the *.. include:* option to include other RST Files or code snippets into Your Document.
Afterwards You can run this software to create a monolithic README.rst that can be viewed on Github or Pypi

You might also include Text/Code from Jupyter Notebooks (sorry, no pictures at the moment, but it is not very hard to do that)

This has many advantages like :

- dont repeat Yourself, create standard blocks to include into Your documentation
- include tested code snippets from Your code files into Your documentation, to avoid untested or outdated documentation
- include other RST Files
- very simple usage, throwing exit codes to detect errors on documentation at travis build-time
- commandline or programmatic interface, You can even use it in the travis.yml
- commandline interface supporting shellscript, cmd, pipes, config-files

----

automated tests, Github Actions, Documentation, Badges, etc. are managed with `PizzaCutter <https://github
.com/bitranox/PizzaCutter>`_ (cookiecutter on steroids)

Python version required: 3.8.0 or newer

tested on recent linux with python 3.8, 3.9, 3.10, 3.11, 3.12-dev, pypy-3.9, pypy-3.10 - architectures: amd64

`100% code coverage <https://codeclimate.com/github/bitranox/rst_include/test_coverage>`_, flake8 style checking ,mypy static type checking ,tested under `Linux, macOS, Windows <https://github.com/bitranox/rst_include/actions/workflows/python-package.yml>`_, automatic daily builds and monitoring

----

- `Usage`_
- `Usage from Commandline`_
- `Installation and Upgrade`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/rst_include/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/rst_include/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/rst_include/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----



Usage
-----------

Yo might use rst_include from the commandline (Windows, Linux and MacOs is supported) or import the module to Your python script and use it from there. You
can also use it from Bash Scripts and Windows Batch Files - See Examples.

use rst_include from commandline
--------------------------------

.. code-block:: bash

    # replace the include statements on shell or windows commandline
    # path can be relative or absolute path
    # examples :

    # relativ path
    $> rst_include include ./source.rst ./target.rst

    # absolute path
    $> rst_include include /project/docs/source.rst /project/docs/target.rst

    # on linux via pipe - You need to change to the source directory first because of relative include paths
    $> cd /project/docs
    $> cat ./source.rst | rst_include include - - > /project/docs/target.rst

    # on Windows via pipe - You need to change to the source directory first because of relative include paths
    $> cd /project/docs
    $> type ./source.rst | rst_include include - - > /project/docs/target.rst

-----------------------------------------------------------------

multiline text replacement
--------------------------

Additional You can easily replace (also multiline) text strings :

.. code-block:: bash

    # replace text strings easily
    # examples :

    $> rst_include replace ./source.rst ./target.rst "{{template_string}}" "new content"

    # multiline example
    # note ${IFS} is the standard bash seperator
    $> rst_include --inplace replace ./source.txt - "line1${IFS}line2" "line1${IFS}something_between${IFS}line2"


piping under Linux:

.. code-block:: bash

    # piping examples
    $> rst_include include ./source.rst - | rst_include replace - ./target.rst "{{pattern}}" "new content"
    # same result
    $> cat ./source.rst | rst_include include - - | rst_include replace - - "{template_string}" "new content" > ./target.rst

    # multiline example
    $> cat ./text.txt | rst_include replace - - "line1${IFS}line2" "line1${IFS}something_between${IFS}line2" > ./text.txt

-----------------------------------------------------------------

Examples
========

Example Python
==============

.. code-block:: python

    # STDLIB
    import subprocess

    # OWN
    from rst_include import *

    def main():
        rst_inc(source='./.docs/README_template.rst', target='./README.rst')
        rst_str_replace(source='./README.rst', target='', str_pattern='{{some pattern}}', str_replace='some text', inplace=True)

    if __name__ == '__main':
        main()

----

Example Shellscript
===================

.. code-block:: bash

    #!/bin/bash

    sudo_askpass="$(command -v ssh-askpass)"
    export SUDO_ASKPASS="${sudo_askpass}"
    export NO_AT_BRIDGE=1  # get rid of (ssh-askpass:25930): dbind-WARNING **: 18:46:12.019: Couldn't register with accessibility bus: Did not receive a reply.

    echo "import the include blocks"
    rst_include include ./.docs/README_template.rst ./README.rst

    echo "replace some patterns"

    # example for piping
    cat ./README.rst \
        | rst_include --inplace replace - - "{{pattern1}}" "some_text_1" \
        | rst_include --inplace replace - - "{{pattern2}}" "some_text_2" \
        | rst_include --inplace replace - - "{{pattern3}}" "some_text_3" \
         > ./README.rst

----

Example Batch
=============

.. code-block:: bat

    REM
    REM rst_include needs to be installed and python paths set correctly
    @echo off
    cls

    rst_include include ./.docs/README_template.rst ./README.rst
    rst_include --inplace replace ./.docs/README_template.rst - "{{pattern}}" "replace string 1"

    echo 'finished'

-----------------------------------------------------------------

rst file examples
=================

simple code include
===================

.. code-block:: bash

    # simple text include, empty line after
    .. include:: ./include1.py
        :code: python
        :number-lines: 10
        :start-line: 6
        :end-line: 23
        :start-after: # start marker
        :end-before: # end-marker
        :encoding: utf-8

text or RST file include
========================
.. code-block:: bash

    # simple text include, without code setting - it is imported as normal textfile, as it is.
    # You might also include other rst files
    .. include:: include3.py
        :start-line: 0       # working, also end-line, etc ... all others suppressed.
        :number-lines:       # not working without :code: setting

include jupyter notebooks
=========================

jupyter notebooks can be first converted to rst via nbconvert, see : https://nbconvert.readthedocs.io/en/latest/usage.html#convert-rst

pandoc is a requirement for nbconvert, see : https://pandoc.org/


.. code-block:: bash

    # convert the attached test.ipynb to test.rst
    $ jupyter nbconvert --to rst test.ipynb

unfortunately the pictures are not shown and needed to be extracted - a first hint might be : https://gist.github.com/sglyon/5687b8455a0107afc6f4c60b5f313670

I would prefer to exctract the pictures after the conversion to RST, and make it a module in rst_include.
Filenames can be a hash of the picture data, in order to avoid web caching issues.

-----------------------------------------------------------------

rst file include parameters
===========================

taken from : http://docutils.sourceforge.net/docs/ref/rst/directives.html

Standard data files intended for inclusion in reStructuredText documents are distributed with the Docutils source code, located in the "docutils" package in the docutils/parsers/rst/include directory.
To access these files, use the special syntax for standard "include" data files, angle brackets around the file name:


.. code-block:: bash

        .. include:: <isonum.txt>    # not supported now


The current set of standard "include" data files consists of sets of substitution definitions. See reStructuredText Standard Definition Files for details.

The following options are recognized:

.. code-block:: bash

    # Only the content starting from this line will be included.
    # (As usual in Python, the first line has index 0 and negative values count from the end.)
    # Combining start/end-line and start-after/end-before is possible.
    # The text markers will be searched in the specified lines (further limiting the included content).
    start-line : integer

.. code-block:: bash

    # Only the content up to (but excluding) this line will be included.
    # Combining start/end-line and start-after/end-before is possible.
    # The text markers will be searched in the specified lines (further limiting the included content).
    end-line : integer

.. code-block:: bash

    # Only the content after the first occurrence of the specified text will be included.
    # Combining start/end-line and start-after/end-before is possible.
    # The text markers will be searched in the specified lines (further limiting the included content).
    start-after : text to find in the external data file

.. code-block:: bash

    # Only the content before the first occurrence of the specified text (but after any after text) will be included.
    # Combining start/end-line and start-after/end-before is possible.
    # The text markers will be searched in the specified lines (further limiting the included content).
    end-before : text to find in the external data file

.. code-block:: bash

    # The entire included text is inserted into the document as a single literal block.
    literal : flag (empty)

.. code-block:: bash

    # The argument and the content of the included file are passed to the code directive (useful for program listings).
    # (New in Docutils 0.9)
    code : formal language (optional)

.. code-block:: bash

    # Precede every code line with a line number. The optional argument is the number of the first line (default 1).
    # Works only with code or literal. (New in Docutils 0.9)
    number-lines : [start line number]

.. code-block:: bash

    # The text encoding of the external data file. Defaults to the document's input_encoding.
    encoding : name of text encoding

.. code-block:: bash

    # Number of spaces for hard tab expansion. A negative value prevents expansion of hard tabs.
    # Defaults to the tab_width configuration setting.
    tab-width : integer

.. code-block:: bash

    With code or literal the common options :class: and :name: are recognized as well.
    all other option in the format :<option>: are just passed through the codeblock

-----------------------------------------------------------------

Usage from Commandline
------------------------

.. code-block::

   Usage: rst_include [OPTIONS] COMMAND [ARGS]...

     commandline tool to resolve RST File includes

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     include  include the include files, use "-" for stdin as SOURCE and "-"...
     info     get program informations
     replace  replace <str_pattern> with <str_replace> <count> times

Installation and Upgrade
------------------------

- Before You start, its highly recommended to update pip and setup tools:


.. code-block::

    python -m pip --upgrade pip
    python -m pip --upgrade setuptools

- to install the latest release from PyPi via pip (recommended):

.. code-block::

    python -m pip install --upgrade rst_include


- to install the latest release from PyPi via pip, including test dependencies:

.. code-block::

    python -m pip install --upgrade rst_include[test]

- to install the latest version from github via pip:


.. code-block::

    python -m pip install --upgrade git+https://github.com/bitranox/rst_include.git


- include it into Your requirements.txt:

.. code-block::

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi:
    rst_include

    # for the latest development version :
    rst_include @ git+https://github.com/bitranox/rst_include.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt


- to install the latest development version, including test dependencies from source code:

.. code-block::

    # cd ~
    $ git clone https://github.com/bitranox/rst_include.git
    $ cd rst_include
    python -m pip install -e .[test]

- via makefile:
  makefiles are a very convenient way to install. Here we can do much more,
  like installing virtual environments, clean caches and so on.

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/bitranox/rst_include.git
    $ cd rst_include

    # to run the tests:
    $ make test

    # to install the package
    $ make install

    # to clean the package
    $ make clean

    # uninstall the package
    $ make uninstall

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
    click
    cli_exit_tools
    lib_list
    lib_log_utils
    pathlib3x

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/rst_include/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

---

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

