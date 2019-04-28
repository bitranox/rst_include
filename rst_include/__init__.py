__title__ = 'rst_include'
__version__ = '1.0.3'
__name__ = 'rst_include'

import sys
import logging

if sys.version_info < (3, 5):
    logging.basicConfig(level=logging.INFO)
    main_logger = logging.getLogger('init')
    main_logger.info('only Python Versions from 3.5 are supported, exit with exitcode 0')
    sys.exit(0)

from rst_include.libs.lib_classes import RstFile
from rst_include.libs.lib_classes import RstConf
from rst_include.libs.lib_main import rst_str_replace
from rst_include.libs.lib_main import rst_inc_from_config
from rst_include.libs.lib_main import rst_inc
