__title__ = 'rst_include'
__version__ = '1.0.1'
__name__ = 'rst_include'

import sys
import logging
try:
    from .libs.lib_log import setup_logger
except ImportError:   # pragma: no cover
    from rst_include.libs.lib_log import setup_logger


def exit_if_not_python_3(major_version=None):
    """
    >>> exit_if_not_python_3()
    >>> exit_if_not_python_3(2)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    SystemExit: 0
    """
    if major_version is None:
        major_version = sys.version_info[0]

    if major_version < 3:
        setup_logger()
        main_logger = logging.getLogger('init')
        main_logger.info('only Python 3 is supported, exit with exitcode 0')
        sys.exit(0)


exit_if_not_python_3()


from rst_include.libs.lib_classes import RstFile
from rst_include.libs.lib_classes import RstConf
from rst_include.libs.lib_main import rst_str_replace
from rst_include.libs.lib_main import rst_inc_from_config
from rst_include.libs.lib_main import rst_inc
