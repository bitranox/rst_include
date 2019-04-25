TEST1 - no includes
*******************

the content of this document does not really matter - it is used for testing against a stored file.

It will be checked that the content will match the expected result after replacing the includes and running tests



rst include file replace
************************

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



simple code include
*******************

.. code-block:: bash

    .. include:: test_include.py
        :code: py

same, defined it as codeblock :

.. code-block:: bash

    # simple text include
    .. code-block:: py

        def my_include():
            pass

Result:

.. code-block:: py

    def my_include():
        pass

text file include
*****************

.. code-block:: bash

    # simple text include, without code setting - it is imported as normal textfile, as it is.
    .. include:: test_include3.py
        :start-line: 0       # working, also end-line, etc ... all others suppressed.
        :number-lines:       # not working without :code: setting

same, just imported as it is as normal text :

.. code-block:: bash

    def my_include():
        # comment    <-- started import here
        pass
        pass

Result:

    # comment
    pass
    pass


2 x simple code include, no empty line between
**********************************************

.. code-block:: bash

    # 2 x simple text include, no empty line between
    .. include:: test_include.py
        :code: py
    .. include:: test_include.py
        :code: py

same, defined it as codeblock :

.. code-block:: bash

    # 2 x simple text include, no empty line between
    .. code-block:: py

            def my_include():
                pass
    .. code-block:: py

                def my_include():
                pass

Result:

.. code-block:: py

        def my_include():
            pass
.. code-block:: py

            def my_include():
            pass

simple code include, with line numbers
**************************************

.. code-block:: bash

    # simple include, with line numbers
    .. include:: test_include.py
        :code: py
        :number-lines:

same, defined it as codeblock :

.. code-block:: bash

    # simple include, with line numbers
    .. code-block:: py
        :number-lines:

        def my_include():
            pass

Result:

.. code-block:: py
    :number-lines:

    def my_include():
        pass


simple code include, with line numbers starting from 10
*******************************************************

.. code-block:: bash

    # simple include, with line numbers starting from 10
    .. include:: test_include.py
        :code: py
        :number-lines: 10

same, defined it as codeblock :

.. code-block:: bash

    # simple include, with line numbers starting from 10
    .. code-block:: py
        :number-lines: 10

        def my_include():
            pass

Result:

.. code-block:: py
    :number-lines: 10

    def my_include():
        pass

simple code include, with line numbers starting from 10
*******************************************************

.. code-block:: bash

    # simple include, with line numbers starting from 10
    .. include:: test_include2.py
        :code: py
        :number-lines: 10

same, defined it as codeblock :

.. code-block:: bash

    # simple include, with line numbers starting from 10
    .. code-block:: py
        :number-lines: 10

        def my_include2_0():
            pass

            pass


        def my_include2_1():
            pass

            pass


        # marker

        def my_include2_2():
            pass

            pass

        # endmarker


        def my_include2_3():
            pass

            pass

Result:

.. code-block:: py
    :number-lines: 10

    def my_include2_0():
        pass

        pass


    def my_include2_1():
        pass

        pass


    # marker

    def my_include2_2():
        pass

        pass

    # endmarker


    def my_include2_3():
        pass

        pass

start-line
**********

.. code-block:: bash

    #  start line 13
    # count line starts with 0
    .. include:: test_include2.py
        :code: py
        :number-lines: 10
        :start-line: 13

same, defined it as codeblock :

.. code-block:: bash

    # start line 13
    #  count line starts with 0
    .. code-block:: py
        :number-lines: 10

        def my_include2_2():
            pass

            pass

        # endmarker


        def my_include2_3():
            pass

            pass

Result:

.. code-block:: py
    :number-lines: 10

    def my_include2_2():
        pass

        pass

    # endmarker


    def my_include2_3():
        pass

        pass

start-line to end-line
**********************

.. code-block:: bash

    #  start-line
    .. include:: test_include2.py
        :code: py
        :number-lines: 10
        :start-line: 13
        :end-line: 15

same, defined it as codeblock :

.. code-block:: bash

    #  start-line - actually code starts after the first non-empty-line - but the Lines are counted
    .. code-block:: py
        :number-lines: 10

        def my_include2_2():


.. code-block:: py
    :number-lines: 10

    def my_include2_2():
