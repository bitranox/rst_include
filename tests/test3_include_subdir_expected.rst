TEST3 - include from subdirectory
=================================

the content of this document does not really matter - it is used for testing against a stored file.

It will be checked that the content will match the expected result after replacing the includes and running test

RESULT Section should show the same like EXPECTED


CODE
====

.. code-block:: bash

    .. include:: ./subdir/include_subdir.py
        :code: python
        :number-lines: 10
        :start-line: 6
        :end-line: 23
        :start-after: # start marker
        :end-before: # end-marker
        :encoding: utf-8

EXPECTED
========

.. code-block:: python
    :number-lines: 10

    def my_include2_2():
        pass

        pass


RESULT
======

.. code-block:: python
    :number-lines: 10

    def my_include2_2() -> None:
        pass

        pass

