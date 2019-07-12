From source code:

.. code-block:: bash

    # normal install
    python setup.py install
    # test without installing
    python setup.py test

via pip latest Release:

.. code-block:: bash

    # latest Release from pypi
    # under Linux You have to use sudo, or it will not be installed as a commandline application
    # [sudo] means, that the command "sudo" is optional for Linux if You want to use it from bash commandline
    [sudo] pip3 install {repository}

    # test without installing
    [sudo] pip3 install {repository} --install-option test

via pip latest Development Version:

.. code-block:: bash

    # upgrade all dependencies regardless of version number (PREFERRED)
    [sudo] pip3 install --upgrade https://github.com/{repository_slug}/archive/master.zip --upgrade-strategy eager
    # normal install
    [sudo] pip3 install --upgrade https://github.com/{repository_slug}/archive/master.zip
    # test without installing
    [sudo] pip3 install https://github.com/{repository_slug}/archive/master.zip --install-option test

via requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release:
    {repository}
    # for the latest Development Version :
    https://github.com/{repository_slug}/archive/master.zip

    # to install and upgrade all modules mentioned in requirements.txt:
    [sudo] pip3 install --upgrade -r /<path>/requirements.txt

via python:

.. code-block:: python

    # for the latest Release
    [sudo] python3 -m pip install upgrade {repository}

    # for the latest Development Version
    [sudo] python3 -m pip install upgrade https://github.com/{repository_slug}/archive/master.zip
