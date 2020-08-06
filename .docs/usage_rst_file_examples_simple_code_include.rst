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
