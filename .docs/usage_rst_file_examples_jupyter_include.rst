include jupyter notebooks
=========================

jupyter notebooks can be first converted to rst via nbconvert, see : https://nbconvert.readthedocs.io/en/latest/usage.html#convert-rst

pandoc is a requirement for nbconvert, see : https://pandoc.org/


.. code-block:: bash

    # convert the attached test.ipynb to test.rst
    $ jupyter nbconvert --to rst test.ipynb

unfortunately the pictures are not shown and needed to be extracted - a first hint might be : https://gist.github.com/sglyon/5687b8455a0107afc6f4c60b5f313670

I would prefer to exctract the pictures after the conversion to RST, and make it a module in rst_include.
Filenames can be a hash of the picture data, in order to avoid web caching issues.
