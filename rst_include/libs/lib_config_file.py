import logging
from rst_include.libs import lib_path
from rst_include.libs import lib_import_module
from rst_include.libs import lib_test


import os
from types import ModuleType


def config_exists(config_file_name: str) -> bool:
    """
    >>> # test file exists
    >>> config_file_name = lib_test.get_test_dir() + '/conf_rst_include_test.py'
    >>> assert config_exists(config_file_name) == True

    >>> # test file not exists
    >>> config_file_name = lib_test.get_test_dir() + '/does_not_exist.py'
    >>> assert config_exists(config_file_name) == False

    """
    if os.path.isfile(config_file_name):
        return True
    else:
        return False


def load_config_file(conf_file_name: str) -> ModuleType:
    """
    >>> # test load named config File
    >>> conf_file_name = lib_test.get_test_dir() + '/conf_rst_include_test.py'
    >>> module = load_config_file(conf_file_name)
    >>> assert len(module.rst_conf.l_rst_files) > 1

    >>> # test config file not correct
    >>> conf_file_name = lib_test.get_test_dir() + '/conf_rst_include_test_attr_rst_conf_missing.py'
    >>> module = load_config_file(conf_file_name)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: the config file ".../conf_rst_include_test_attr_rst_conf_missing.py" has not the correct attribute "rst_conf"


    >>> conf_file_name = lib_test.get_test_dir() + '/conf_rst_include_test_attr_l_rst_files_missing.py'
    >>> module = load_config_file(conf_file_name)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: the config file ".../conf_rst_include_test_attr_l_rst_files_missing.py" has not the correct attribute "l_rst_files"

    >>> # default config File not found
    >>> module = load_config_file('')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileNotFoundError: can not load config file .../conf_res_inc.py

    """
    logger = logging.getLogger('load_config_file')
    if not conf_file_name:
        conf_file_name = 'conf_res_inc.py'
        logger.info('loading default config file "conf_res_inc.py" from current directory')

    conf_file_name_absolute = lib_path.strip_and_replace_backslashes(os.path.abspath(conf_file_name))
    if not os.path.isfile(conf_file_name_absolute):
        s_error = 'can not load config file {conf}'.format(conf=conf_file_name_absolute)
        logger.error(s_error)
        raise FileNotFoundError(s_error)

    module = lib_import_module.get_module_from_file(module_name='conf_rst_include', path_to_module=conf_file_name_absolute)

    if not hasattr(module, 'rst_conf'):
        raise_config_import_error(conf_file_name, 'rst_conf')

    rst_conf = module.rst_conf
    if not hasattr(rst_conf, 'l_rst_files'):
        raise_config_import_error(conf_file_name, 'l_rst_files')
    return module


def raise_config_import_error(conf_file_name: str, attribute: str):
    logger = logging.getLogger('load_config_file')
    s_error = 'the config file "{conf_file_name}" has not the correct attribute "{attribute}"'.format(
        conf_file_name=conf_file_name, attribute=attribute)
    logger.error(s_error)
    raise ValueError(s_error)
