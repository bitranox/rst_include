import pathlib

with open(pathlib.Path(__file__).parent / 'version.txt', mode='r') as version_file:
    version = version_file.readline()

__title__ = 'rst_include'
__version__ = version
__name__ = 'rst_include'

import errno                            # this we need tor main() in __main__.py probably for commandline entry point - to check
import sys                              # this we need tor main() in __main__.py probably for commandline entry point - to check
import logging                          # this we need tor main() in __main__.py probably for commandline entry point - to check
from .libs.lib_classes import RstFile
from .libs.lib_classes import RstConf
from .libs.lib_main import rst_str_replace
from .libs.lib_main import rst_inc
