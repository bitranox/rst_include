rst_include
===========


|Pypi Status| |license| |maintenance|

|Build Status| |Codecov Status| |Better Code| |code climate| |snyk security|

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License
.. |maintenance| image:: https://img.shields.io/maintenance/yes/2019.svg
.. |Build Status| image:: https://travis-ci.org/bitranox/rst_include.svg?branch=master
   :target: https://travis-ci.org/bitranox/rst_include
.. for the pypi status link note the dashes, not the underscore !
.. |Pypi Status| image:: https://badge.fury.io/py/{repository_dashed}.svg
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

This README was also created with rst_include, You might look at ./docs/README_template.rst , build_readme.sh, build_readme.cmd and build_readme.py as examples. (they all do the same, just different versions)


`100% code coverage <https://codecov.io/gh/bitranox/rst_include>`_, tested under `Linux, OsX, Windows and Wine <https://travis-ci.org/bitranox/rst_include>`_

----

- `Installation and Upgrade`_
- `Basic Usage`_
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
    $> rst_include.py -h

.. code-block:: shell

    usage: rst_inc.py [-h] {include,replace} ...

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
    $> rst_include.py include -h

.. code-block:: shell

    usage: rst_inc.py include [-h] [-s [source]] [-t [target]]
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
                            If no filename is passed, the default conf_res_inc.py
                            is searched in the current directory


.. code-block:: shell

    # get help on shell or windows commandline for string replace
    $> rst_include.py replace -h

.. code-block:: shell

    usage: rst_inc.py replace [-h] [-s [source]] [-t [target]]
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
    $> rst_include.py include -s ./source.rst -t ./target.rst

    # absolute path
    $> rst_include.py include -s /project/docs/source.rst -t /project/docs/target.rst

    # on linux via pipe
    $> cat /project/docs/source.rst | rst_include.py include > /project/docs/target.rst

    # on Windows via pipe
    $> type /project/docs/source.rst | rst_include.py include > /project/docs/target.rst


- replace include statements on multiple files via config.py :

.. code-block:: shell

    # replace the include statements on shell or windows commandline
    # path to the config file can be absolute or relative path
    # option -c or --config :

    # will try to load the default conf_res_inc.py from the current directory
    $> rst_include include -c

    # will load another config file another directory
    $> rst_include include -c ./conf_this_project.py

Structure of the configuration file:

the files are processed in the given order, by that way You can even realize nested .. include:: blocks.

You might also specify the encoding for source and target files

.. code-block:: python

    from rst_include import *

    # set config here
    rst_conf = RstConf()

    # paths absolute, or relative to the location of the config file
    rst_conf.l_rst_files = [RstFile(source='./rst_include/tests/test1_no_includes_template.rst',
                                    target='./rst_include/tests/test1_no_includes_result.rst',
                                    source_encoding='utf-8-sig',  # default = utf-8-sig because it can read utf-8 and utf-8-sig
                                    target_encoding='utf-8'      # default = utf-8
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

    $> rst_include.py -s ./source.rst -t ./target.rst replace {template_string} "new content"

piping under Linux:

.. code-block:: shell

    $> rst_include.py replace -s ./source.rst {template_string} "new content" | rst_include.py include -t ./target.rst


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
