Example Shellscript
===================

.. code-block:: bash

    #!/bin/bash

    sudo_askpass="$(command -v ssh-askpass)"
    export SUDO_ASKPASS="${sudo_askpass}"
    export NO_AT_BRIDGE=1  # get rid of (ssh-askpass:25930): dbind-WARNING **: 18:46:12.019: Couldn't register with accessibility bus: Did not receive a reply.

    echo "import the include blocks"
    rst_include include ./.docs/README_template.rst ./README.rst

    echo "replace some patterns"

    # example for piping
    cat ./README.rst \
        | rst_include --inplace replace - - "{{pattern1}}" "some_text_1" \
        | rst_include --inplace replace - - "{{pattern2}}" "some_text_2" \
        | rst_include --inplace replace - - "{{pattern3}}" "some_text_3" \
         > ./README.rst
