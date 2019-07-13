rst_include
===========

.. include:: ./badges_without_jupyter.rst

since You can not include files into RST files on github and PyPi, You can replace those imports with this software.

That means You can locally write Your RST documents (for instance with pycharm) and use there
the .. include: option to include other RST Files or code snippets into Your Document.
Afterwards You can run this software to create a monolithic README.rst that can be viewed on Github or Pypi

You might also include Text/Code from Jupyter Notebooks (sorry, no pictures at the moment, but it is not very hard to do that)

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
rst_include does only work on python > 3.6


.. include:: ./tested_under.rst

----

- `Installation and Upgrade`_
- `Basic Usage`_
- Examples
    - `Example Build Script Python`_
    - `Example Build Script DOS Batch`_
    - `Example Build Script Shellscript`_
    - `RST Includes Examples`_
    - `simple code include`_
    - `text or RST file include`_
    - `include jupyter notebooks`_
- `RST Include Parameters`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/{repository_slug}/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/{repository_slug}/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/{repository_slug}/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

-----------------------------------------------------------------

Installation and Upgrade
------------------------

.. include:: ./installation.rst

-----------------------------------------------------------------

Basic Usage
-----------

since rst_include is registered as a console script command with Your current python interpreter, You have to use the command "rst_include" (not "rst_include.py")


- issue command :

.. code-block:: shell

    # issue command on shell or windows commandline
    $> rst_include [OPTIONS]

    # or, if python/bin is not in Your python path :
    # on Windows
    $> c:\python37\scripts\rst_include [OPTIONS]
    # on Linux/oSX
    $> /python37/bin/rst_include [OPTIONS]

    # issue command with python interpreter
    $> python -m rst_include [OPTIONS]



- get help :

.. code-block:: shell

    # get help on shell or windows commandline
    $> rst_include -h


.. include:: ./rst_include_help_output.txt
        :code: shell


.. code-block:: shell

    # get help on shell or windows commandline for include
    $> rst_include include -h

.. include:: ./rst_include_help_include_output.txt
        :code: shell

.. code-block:: shell

    # get help on shell or windows commandline for string replace
    $> rst_include replace -h

.. include:: ./rst_include_help_replace_output.txt
        :code: shell

- replace the include statements in source.rst and save it to target.rst via commandline parameters :

.. code-block:: shell

    # replace the include statements on shell or windows commandline
    # path can be relative or absolute path
    # examples :

    # relativ path
    $> rst_include include -s ./source.rst -t ./target.rst

    # absolute path
    $> rst_include include -s /project/docs/source.rst -t /project/docs/target.rst

    # on linux via pipe
    $> cat /project/docs/source.rst | rst_include include > /project/docs/target.rst

    # on Windows via pipe
    $> type /project/docs/source.rst | rst_include include > /project/docs/target.rst


- replace include statements on multiple files via config.py :

.. code-block:: shell

    # replace the include statements on shell or windows commandline
    # path to the config file can be absolute or relative path
    # option -c or --config :

    # will try to load the default conf_rst_inc.py from the current directory
    $> rst_include include -c

    # will load another config file another directory
    $> rst_include include -c ./conf_this_project.py

Structure of the configuration file:

the files are processed in the given order, by that way You can even realize nested .. include:: blocks.

You might also specify the encoding for source and target files

.. include:: ../conf_rst_inc_sample.py
    :code: python

Additional You can easily replace (also multiline) text strings :

.. code-block:: shell

    # replace text strings easily
    # examples :

    $> rst_include replace -s ./source.rst -t ./target.rst "{template_string}" "new content"

    # multiline example
    # note ${IFS} is the standard bash seperator
    $> rst_include replace --inplace -s ./source.txt "line1${IFS}line2" "line1${IFS}something_between${IFS}line2"


piping under Linux:

.. code-block:: shell

    # piping examples
    $> rst_include include -s ./source.rst | rst_include replace -t ./target.rst "{template_string}" "new content"
    # same result
    $> cat ./source.rst | rst_include include | rst_include replace "{template_string}" "new content" > ./target.rst

    # multiline example
    $> cat ./text.txt | rst_include replace "line1${IFS}line2" "line1${IFS}something_between${IFS}line2" > ./text.txt


-----------------------------------------------------------------

Example Build Script Python
===========================

.. include:: ../build_docs.py
    :code: python

Example Build Script DOS Batch
==============================

.. include:: ../build_docs.cmd
    :code: bat


Example Build Script Shellscript
================================

.. include:: ../build_docs.sh
    :code: shell

-----------------------------------------------------------------

RST Includes Examples
=====================

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

RST Include Parameters
======================
.. include:: ./rst_include_parameters.rst

-----------------------------------------------------------------

Requirements
------------

following modules will be automatically installed :

.. include:: ../requirements.txt
        :code: shell

-----------------------------------------------------------------

Acknowledgements
----------------
.. include:: ./acknowledgment.rst

-----------------------------------------------------------------

Contribute
----------
.. include:: ./contribute.rst

-----------------------------------------------------------------

License
-------
.. include:: ./licence_mit.rst

-----------------------------------------------------------------

.. Changelog link comes from the included document !

.. include:: ../CHANGES.rst

