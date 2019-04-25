# -*- coding: utf-8 -*-

import sys
from types import ModuleType

from rst_include.libs import lib_test


def get_module_from_file(module_name, path_to_module):
    # type: (str,str) -> ModuleType
    """
    >>> module = get_module_from_file('test', lib_test.get_test_dir()+'/include1.py')
    >>> assert module.my_include() == None
    >>> import test
    >>> assert test.my_include() == None

    """
    if sys.version_info < (3, 0):
        import imp
        module = imp.load_source(module_name, path_to_module)
        sys.modules[module_name] = module
        return module

    elif sys.version_info >= (3, 5):
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, path_to_module)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module
        return module

    elif sys.version_info < (3, 5):
        from importlib.machinery import SourceFileLoader
        module = SourceFileLoader(module_name, path_to_module).load_module()
        sys.modules[module_name] = module
        return module
