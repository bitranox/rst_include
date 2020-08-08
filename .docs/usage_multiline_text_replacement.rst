multiline text replacement
--------------------------

Additional You can easily replace (also multiline) text strings :

.. code-block:: bash

    # replace text strings easily
    # examples :

    $> rst_include replace ./source.rst ./target.rst "{{template_string}}" "new content"

    # multiline example
    # note ${IFS} is the standard bash seperator
    $> rst_include --inplace replace ./source.txt - "line1${IFS}line2" "line1${IFS}something_between${IFS}line2"


piping under Linux:

.. code-block:: bash

    # piping examples
    $> rst_include include ./source.rst - | rst_include replace - ./target.rst "{{pattern}}" "new content"
    # same result
    $> cat ./source.rst | rst_include include - - | rst_include replace - - "{template_string}" "new content" > ./target.rst

    # multiline example
    $> cat ./text.txt | rst_include replace - - "line1${IFS}line2" "line1${IFS}something_between${IFS}line2" > ./text.txt

