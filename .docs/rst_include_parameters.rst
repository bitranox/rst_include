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
