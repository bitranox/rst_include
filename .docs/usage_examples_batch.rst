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
