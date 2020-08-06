Example Python
==============

.. code-block:: python

    # STDLIB
    import subprocess

    # OWN
    from rst_include import *

    def main():
        rst_inc(source='./.docs/README_template.rst', target='./README.rst')
        rst_str_replace(source='./README.rst', target='', str_pattern='{{some pattern}}', str_replace='some text', inplace=True)

    if __name__ == '__main':
        main()
