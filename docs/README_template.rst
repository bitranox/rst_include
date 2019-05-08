rst_include
===========

.. include:: ./badges_without_jupyter.rst

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


.. include:: ./tested_under.rst

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
- `Report Issues <https://github.com/{repository_slug}/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/{repository_slug}/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/{repository_slug}/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_

----

Installation and Upgrade
------------------------

.. include:: ./installation.rst


Basic Usage
-----------

- get help :

.. code-block:: shell

    # get help on shell or windows commandline
    $> rst_inc -h

.. include:: ./rst_include_help_output.txt
        :code: shell


.. code-block:: shell

    # get help on shell or windows commandline for include
    $> rst_inc include -h

.. include:: ./rst_include_help_include_output.txt
        :code: shell

.. code-block:: shell

    # get help on shell or windows commandline for string replace
    $> rst_inc replace -h

.. include:: ./rst_include_help_replace_output.txt
        :code: shell

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

    # will try to load the default conf_res_inc.py from the current directory
    $> rst_inc include -c

    # will load another config file another directory
    $> rst_inc include -c ./conf_this_project.py

Structure of the configuration file:

the files are processed in the given order, by that way You can even realize nested .. include:: blocks.

You might also specify the encoding for source and target files

.. include:: ../conf_res_inc_sample.py
    :code: python

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
.. include:: ./rst_include_parameters.rst


Requirements
------------

following modules will be automatically installed :

.. include:: ../requirements.txt
        :code: shell

Acknowledgements
----------------
.. include:: ./acknowledgment.rst

Contribute
----------
.. include:: ./contribute.rst

License
-------
.. include:: ./licence_mit.rst
