rst_include
===========

|Pypi Status| |pyversion| |license| |maintenance|

|Build Status| |Codecov Status| |Better Code| |code climate| |snyk security|

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License
.. |maintenance| image:: https://img.shields.io/maintenance/yes/2019.svg
.. |Build Status| image:: https://travis-ci.org/bitranox/rst_include.svg?branch=master
   :target: https://travis-ci.org/bitranox/rst_include
.. for the pypi status link note the dashes, not the underscore !
.. |Pypi Status| image:: https://badge.fury.io/py/rst-include.svg
   :target: https://badge.fury.io/py/rst_include
.. |Codecov Status| image:: https://codecov.io/gh/bitranox/rst_include/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/bitranox/rst_include
.. |Better Code| image:: https://bettercodehub.com/edge/badge/bitranox/rst_include?branch=master
   :target: https://bettercodehub.com/results/bitranox/rst_include
.. |snyk security| image:: https://snyk.io/test/github/bitranox/rst_include/badge.svg
   :target: https://snyk.io/test/github/bitranox/rst_include
.. |code climate| image:: https://api.codeclimate.com/v1/badges/ff3f414903627e5cfc35/maintainability
   :target: https://codeclimate.com/github/bitranox/rst_include/maintainability
   :alt: Maintainability
.. |pyversion| image:: https://img.shields.io/badge/python-%3E%3D3.5-brightgreen.svg
   :target: https://badge.fury.io/py/rst_include
   :alt: Python Version

since You can not include files into RST files on github, You can replace those imports with this software.

That means You can locally write Your RST documents (for instance with pycharm) and use there
the .. include: option to include other RST Files or code snippets into Your Document.
Afterwards You can run this software to create a monolithic README.rst that can be viewed on Github or Pypi

This has many advantages like :

- dont repeat Yourself, create standard blocks to include into Your documentation
- include tested code snippets from Your code files into Your documentation, to avoid untested or outdated documentation
- include other RST Files
- very simple usage, throwing exit codes to detect errors on documentation at travis build-time
- commandline or programmatic interface, You can even use it in the travis.yml
- commandline interface supporting shellscript, cmd, pipes, config-files

This README was also created with rst_include, You might look at ./docs/README_template.rst ,
build_docs.sh, build_docs.cmd and build_docs.py as examples. (they all do the same, just different versions)

The travis.yml builds the Documentation on every run, so You can be sure that there are no Errors.
rst_include does only work on python > 3.5.2

`100% code coverage <https://codecov.io/gh/bitranox/rst_include>`_, mypy static type checking, tested under `Linux, OsX, Windows and Wine <https://travis-ci.org/bitranox/rst_include>`_, automatic daily builds  and monitoring

----

- `Installation and Upgrade`_
- `Basic Usage`_
- `Example Build Script Python`_
- `Example Build Script DOS Batch`_
- `Example Build Script Shellscript`_
- `RST Includes Example`_
- `RST Include Parameters`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/rst_include/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/rst_include/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/rst_include/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_

----

Installation and Upgrade
------------------------

From source code:

.. code-block:: bash

    # normal install
    python setup.py install
    # test without installing
    python setup.py test

via pip latest Release:

.. code-block:: bash

    # latest Release from pypi
    pip install rst_include

    # test without installing
    pip install rst_include --install-option test

via pip latest Development Version:

.. code-block:: bash

    # upgrade all dependencies regardless of version number (PREFERRED)
    pip install --upgrade https://github.com/bitranox/rst_include/archive/master.zip --upgrade-strategy eager
    # normal install
    pip install --upgrade https://github.com/bitranox/rst_include/archive/master.zip
    # test without installing
    pip install https://github.com/bitranox/rst_include/archive/master.zip --install-option test

via requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release:
    rst_include
    # for the latest Development Version :
    https://github.com/bitranox/rst_include/archive/master.zip

    # to install and upgrade all modules mentioned in requirements.txt:
    pip install --upgrade -r /<path>/requirements.txt

via python:

.. code-block:: python

    # for the latest Release
    python -m pip install upgrade rst_include

    # for the latest Development Version
    python -m pip install upgrade https://github.com/bitranox/rst_include/archive/master.zip

Basic Usage
-----------

- get help :

.. code-block:: shell

    # get help on shell or windows commandline
    $> rst_inc -h

.. code-block:: shell

    usage: __main__.py [-h] {include,replace} ...

    Process .rst File Includes

    positional arguments:
      {include,replace}
        include          include rst includes
        replace          string replace

    optional arguments:
      -h, --help         show this help message and exit

    check the documentation on github

.. code-block:: shell

    # get help on shell or windows commandline for include
    $> rst_inc include -h

.. code-block:: shell

    usage: __main__.py include [-h] [-s [source]] [-t [target]]
                               [-se [source encoding]] [-te [target encoding]]
                               [-c [configfile.py]]

    optional arguments:
      -h, --help            show this help message and exit
      -s [source], --source [source]
                            default: stdin
      -t [target], --target [target]
                            default: stdout
      -se [source encoding], --source_encoding [source encoding]
                            default: utf-8-sig
      -te [target encoding], --target_encoding [target encoding]
                            default: utf-8
      -c [configfile.py], --config [configfile.py]
                            If no filename is passed, the default conf_rst_inc.py
                            is searched in the current directory

.. code-block:: shell

    # get help on shell or windows commandline for string replace
    $> rst_inc replace -h

.. code-block:: shell

    usage: __main__.py replace [-h] [-s [source]] [-t [target]]
                               [-se [source encoding]] [-te [target encoding]]
                               old new [count]

    positional arguments:
      old                   old
      new                   new
      count                 count

    optional arguments:
      -h, --help            show this help message and exit
      -s [source], --source [source]
                            default: stdin
      -t [target], --target [target]
                            default: stdout
      -se [source encoding], --source_encoding [source encoding]
                            default: utf-8-sig
      -te [target encoding], --target_encoding [target encoding]
                            default: utf-8

- replace the include statements in source.rst and save it to target.rst via commandline parameters :

.. code-block:: shell

    # replace the include statements on shell or windows commandline
    # path can be relative or absolute path
    # examples :

    # relativ path
    $> rst_inc include -s ./source.rst -t ./target.rst

    # absolute path
    $> rst_inc include -s /project/docs/source.rst -t /project/docs/target.rst

    # on linux via pipe
    $> cat /project/docs/source.rst | rst_inc include > /project/docs/target.rst

    # on Windows via pipe
    $> type /project/docs/source.rst | rst_inc include > /project/docs/target.rst


- replace include statements on multiple files via config.py :

.. code-block:: shell

    # replace the include statements on shell or windows commandline
    # path to the config file can be absolute or relative path
    # option -c or --config :

    # will try to load the default conf_rst_inc.py from the current directory
    $> rst_inc include -c

    # will load another config file another directory
    $> rst_inc include -c ./conf_this_project.py

Structure of the configuration file:

the files are processed in the given order, by that way You can even realize nested .. include:: blocks.

You might also specify the encoding for source and target files

.. code-block:: python

    from rst_include import *

    # set config here
    rst_conf = RstConf()

    # paths absolute, or relative to the location of the config file
    # the notation for relative files is like on windows or linux - not like in python.
    # so You might use ../../some/directory/some_document.rst to go two levels back.
    # avoid absolute paths since You never know where the program will run.
    rst_conf.l_rst_files = [RstFile(source='./rst_include/tests/test1_no_includes_template.rst',
                                    target='./rst_include/tests/test1_no_includes_result.rst',
                                    # default = utf-8-sig because it can read utf-8 and utf-8-sig
                                    source_encoding='utf-8-sig',
                                    # default = utf-8
                                    target_encoding='utf-8'
                                    ),
                            RstFile(source='./rst_include/tests/test2_include_samedir_template.rst',
                                    target='./rst_include/tests/test2_include_samedir_result.rst'),
                            RstFile(source='./rst_include/tests/test3_include_subdir_template.rst',
                                    target='./rst_include/tests/test3_include_subdir_result.rst'),
                            RstFile(source='./rst_include/tests/test4_include_nocode_template.rst',
                                    target='./rst_include/tests/test4_include_nocode_result.rst')]

Additional You can easily replace text strings :

.. code-block:: shell

    # replace text strings easily
    # examples :

    $> rst_inc -s ./source.rst -t ./target.rst replace {template_string} "new content"

piping under Linux:

.. code-block:: shell

    $> rst_inc replace -s ./source.rst {template_string} "new content" | rst_inc include -t ./target.rst


Example Build Script Python
===========================

.. code-block:: python

    import argparse
    import errno
    import logging
    import os
    import sys
    from rst_include import *
    from rst_include.libs import lib_log
    import subprocess


    # CONSTANTS & PROJECT SPECIFIC FUNCTIONS
    codeclimate_link_hash = "ff3f414903627e5cfc35"


    def project_specific(repository_slug, repository, repository_dashed):
        # PROJECT SPECIFIC
        logger = logging.getLogger('project_specific')
        logger.info('create help documentation files {dir}'.format(dir=os.path.abspath(os.path.curdir)))
        subprocess.run('{sys_executable} ./rst_include/__main__.py -h > ./docs/rst_include_help_output.txt'.format(sys_executable=sys.executable), shell=True, check=True)
        subprocess.run('{sys_executable} ./rst_include/__main__.py include -h > ./docs/rst_include_help_include_output.txt'.format(sys_executable=sys.executable), shell=True, check=True)
        subprocess.run('{sys_executable} ./rst_include/__main__.py replace -h > ./docs/rst_include_help_replace_output.txt'.format(sys_executable=sys.executable), shell=True, check=True)


    def parse_args(cmd_args=sys.argv[1:]):
        # type: ([]) -> []
        parser = argparse.ArgumentParser(
            description='Create Readme.rst',
            epilog='check the documentation on github',
            add_help=True)

        parser.add_argument('travis_repo_slug', metavar='TRAVIS_REPO_SLUG in the form "<github_account>/<repository>"')
        args = parser.parse_args(cmd_args)
        return args, parser


    def main(args):
        logger = logging.getLogger('build_docs')
        logger.info('create the README.rst')
        travis_repo_slug = args.travis_repo_slug
        repository = travis_repo_slug.split('/')[1]
        repository_dashed = repository.replace('_', '-')

        project_specific(travis_repo_slug, repository, repository_dashed)

        """
        paths absolute, or relative to the location of the config file
        the notation for relative files is like on windows or linux - not like in python.
        so You might use ../../some/directory/some_document.rst to go two levels back.
        avoid absolute paths since You never know where the program will run.
        """

        logger.info('include the include blocks')
        rst_inc(source='./docs/README_template.rst',
                target='./docs/README_template_included.rst')

        # please note that the replace syntax is not shown correctly in the README.rst,
        # because it gets replaced itself by the build_docs.py
        # we could overcome this by first replacing, and afterwards including -
        # check out the build_docs.py for the correct syntax !
        logger.info('replace repository related strings')
        rst_str_replace(source='./docs/README_template_included.rst',
                        target='./docs/README_template_repo_replaced.rst',
                        old='bitranox/rst_include',
                        new=travis_repo_slug)
        rst_str_replace(source='./docs/README_template_repo_replaced.rst',
                        target='./docs/README_template_repo_replaced2.rst',
                        old='rst_include',
                        new=repository)
        rst_str_replace(source='./docs/README_template_repo_replaced2.rst',
                        target='./docs/README_template_repo_replaced3.rst',
                        old='rst-include',
                        new=repository_dashed)

        rst_str_replace(source='./docs/README_template_repo_replaced3.rst',
                        target='./README.rst',
                        old='ff3f414903627e5cfc35',
                        new=codeclimate_link_hash)

        logger.info('cleanup')
        os.remove('./docs/README_template_included.rst')
        os.remove('./docs/README_template_repo_replaced.rst')
        os.remove('./docs/README_template_repo_replaced2.rst')
        os.remove('./docs/README_template_repo_replaced3.rst')

        logger.info('done')
        sys.exit(0)


    if __name__ == '__main__':
        lib_log.setup_logger()
        main_logger = logging.getLogger('main')
        try:
            _args, _parser = parse_args()

            main(_args)
        except FileNotFoundError:
            # see https://www.thegeekstuff.com/2010/10/linux-error-codes for error codes
            sys.exit(errno.ENOENT)      # No such file or directory
        except FileExistsError:
            sys.exit(errno.EEXIST)      # File exists
        except TypeError:
            sys.exit(errno.EINVAL)      # Invalid Argument
        except ValueError:
            sys.exit(errno.EINVAL)      # Invalid Argument

Example Build Script DOS Batch
==============================

.. code-block:: bat

    REM
    REM rst_include needs to be installed and python paths set correctly
    @echo off
    cls

    REM # You might also use Environment Variable here, or as commandline parameter
    REM # this is just an example, I use actually the build_readme.py python file myself
    REM # I do not recommend cmd files anymore - why it it is so much easier under python ...
    REM # I am sure there is a more elegant was to do it on batch files, this is only an example

    SET repository_slug="bitranox/rst_include"
    SET repository="rst_include"
    SET codeclimate_link_hash="ff3f414903627e5cfc35"

    REM # get dashed repository name for pypi links
    echo %repository% | rst_inc replace "_" "-" > temp.txt
    set /p repository_dashed= < temp.txt
    del temp.txt


    REM paths absolute, or relative to the location of the config file
    REM the notation for relative files is like on windows or linux - not like in python.
    REM so You might use ../../some/directory/some_document.rst to go two levels back.
    REM avoid absolute paths since You never know where the program will run.

    echo 'create the sample help outputs'
    rst_inc -h > ./docs/rst_include_help_output.txt
    rst_inc include -h > ./docs/rst_include_help_include_output.txt
    rst_inc replace -h > ./docs/rst_include_help_replace_output.txt

    echo "import the include blocks"
    rst_inc include -s ./docs/README_template.rst -t ./docs/README_template_included.rst

    REM please note that the replace syntax is not shown correctly in the README.rst,
    REM because it gets replaced itself by the build_docs.py
    REM we could overcome this by first replacing, and afterwards including -
    REM check out the build_docs.cmd for the correct syntax !

    echo "replace repository_slug"
    rst_inc replace -s ./docs/README_template_included.rst -t ./docs/README_template_repo_replaced.rst bitranox/rst_include %repository_slug%
    echo "replace repository"
    rst_inc replace -s ./docs/README_template_repo_replaced.rst -t ./docs/README_template_repo_replaced2.rst rst_include %repository%
    echo "replace repository_dashed"
    rst_inc replace -s ./docs/README_template_repo_replaced2.rst -t ./docs/README_template_repo_replaced3.rst rst-include %repository_dashed%
    echo "replace codeclimate_link_hash"
    rst_inc replace -s ./docs/README_template_repo_replaced3.rst -t ./README.rst ff3f414903627e5cfc35 %codeclimate_link_hash%

    REM ### oddly del "./docs/README_template_included.rst" does not work here - You need to use backslashes
    echo "cleanup"
    del ".\docs\README_template_included.rst"
    del ".\docs\README_template_repo_replaced.rst"
    del ".\docs\README_template_repo_replaced2.rst"
    del ".\docs\README_template_repo_replaced3.rst"

    echo 'finished'

Example Build Script Shellscript
================================

.. code-block:: shell

    #!/bin/bash

    ### CONSTANTS
    codeclimate_link_hash="ff3f414903627e5cfc35"
    # TRAVIS_TAG

    function include_dependencies {
        local my_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"  # this gives the full path, even for sourced scripts
        chmod +x "${my_dir}"/lib_bash/*.sh
        source "${my_dir}/lib_bash/lib_color.sh"
    }

    include_dependencies  # we need to do that via a function to have local scope of my_dir

    function check_repository_name {
        if [[ -z ${TRAVIS_REPO_SLUG} ]]
            then
                clr_bold clr_red "ERROR no travis repository name set - exiting"
                exit 1
            fi
    }

    clr_bold clr_green "Build README.rst for repository: ${TRAVIS_REPO_SLUG}"

    check_repository_name

    repository="${TRAVIS_REPO_SLUG#*/}"                                 # "username/repository_name" --> "repository_name"
    repository_dashed="$( echo -e "$repository" | tr  '_' '-'  )"       # "repository_name --> repository-name"

    clr_green "create the sample help outputs"
    rst_inc -h > ./docs/rst_include_help_output.txt
    rst_inc include -h > ./docs/rst_include_help_include_output.txt
    rst_inc replace -h > ./docs/rst_include_help_replace_output.txt

    clr_green "import the include blocks"
    rst_inc include -s ./docs/README_template.rst -t ./docs/README_template_included.rst

    clr_green "replace repository strings"

    # please note that the replace syntax is not shown correctly in the README.rst,
    # because it gets replaced itself by the build_docs.py
    # we could overcome this by first replacing, and afterwards including -
    # check out the build_docs.sh for the correct syntax !

    # example for piping
    cat ./docs/README_template_included.rst \
        | rst_inc replace "bitranox/rst_include" "${TRAVIS_REPO_SLUG}" \
        | rst_inc replace "rst_include" "$rst_include" \
        | rst_inc replace "rst-include" "$rst-include" \
        | rst_inc replace "ff3f414903627e5cfc35" "$ff3f414903627e5cfc35" \
         > ./README.rst

    clr_green "cleanup"
    rm ./docs/README_template_included.rst

    clr_green "done"
    clr_green "******************************************************************************************************************"
    clr_bold clr_green "FINISHED building README.rst"
    clr_green "******************************************************************************************************************"

RST Includes Example
====================

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


RST Include Parameters
======================

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

Requirements
------------

following modules will be automatically installed :

.. code-block:: shell

    pytest  # see : https://github.com/pytest-dev/pytest
    typing  # see : https://pypi.org/project/typing/

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

