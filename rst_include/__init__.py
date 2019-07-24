__title__ = 'rst_include'
__version__ = '1.0.8'
__name__ = 'rst_include'

import errno                            # this we need tor main() in __main__.py
import sys                              # this we need tor main() in __main__.py
import logging                          # this we need tor main() in __main__.py
from .libs.lib_classes import RstFile
from .libs.lib_classes import RstConf
from .libs.lib_main import rst_str_replace
from .libs.lib_main import rst_inc_from_config
from .libs.lib_main import rst_inc
