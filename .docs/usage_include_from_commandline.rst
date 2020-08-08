use rst_include from commandline
--------------------------------

.. code-block:: bash

    # replace the include statements on shell or windows commandline
    # path can be relative or absolute path
    # examples :

    # relativ path
    $> rst_include include ./source.rst ./target.rst

    # absolute path
    $> rst_include include /project/docs/source.rst /project/docs/target.rst

    # on linux via pipe - You need to change to the source directory first because of relative include paths
    $> cd /project/docs
    $> cat ./source.rst | rst_include include - - > /project/docs/target.rst

    # on Windows via pipe - You need to change to the source directory first because of relative include paths
    $> cd /project/docs
    $> type ./source.rst | rst_include include - - > /project/docs/target.rst
