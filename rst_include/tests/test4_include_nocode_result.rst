TEST4 - include no code
=======================

the content of this document does not really matter - it is used for testing against a stored file.

It will be checked that the content will match the expected result after replacing the includes and running test

RESULT Section should show the same like EXPECTED


CODE
====

.. code-block:: bash

    .. include:: ./include2.py
        :number-lines: 10
        :start-line: 6
        :end-line: 23
        :start-after: # start marker
        :end-before: # end-marker
        :encoding: utf-8

EXPECTED
========


def my_include2_2():
    pass

    pass


RESULT
======

def my_include2_2() -> None:
    pass

    pass

