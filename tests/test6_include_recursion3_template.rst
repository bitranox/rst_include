TEST6 - include recursion 3
===========================

the content of this document does not really matter - it is used for testing against a stored file.

It will be checked that the content will match the expected result after replacing the includes and running test

RESULT Section should show the same like EXPECTED


CODE
====

.. code-block:: bash

    .. include:: ./test6_include_recursion1_template.rst

EXPECTED
========

.. code-block:: bash

    since:

    test6_include_recursion1_template.rst includes test6_include_recursion2_template.rst

    test6_include_recursion2_template.rst includes test6_include_recursion3_template.rst

    and

    test6_include_recursion3_template.rst includes test6_include_recursion1_template.rst

    this should throw recursion error

RESULT
======

.. include:: ./test6_include_recursion1_template.rst
