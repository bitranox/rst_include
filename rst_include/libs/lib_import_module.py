import sys
from types import ModuleType
from rst_include.libs import lib_test


def get_module_from_file(module_name: str, path_to_module: str) -> ModuleType:
    """
    >>> module = get_module_from_file('test', lib_test.get_test_dir()+'/include1.py')
    >>> assert hasattr(module, 'my_include')
    >>> function = getattr(module, 'my_include')
    >>> assert function() is None
    >>> import test
    >>> assert hasattr(test, 'my_include')
    >>> function = getattr(test, 'my_include')
    >>> assert function() is None
    """
    if sys.version_info < (3, 0):  # pragma: no cover
        import imp
        module = imp.load_source(module_name, path_to_module)
        sys.modules[module_name] = module
        return module

    elif sys.version_info >= (3, 5):
        import importlib.util
        from importlib.abc import Loader
        spec = importlib.util.spec_from_file_location(module_name, path_to_module)
        assert isinstance(spec.loader, Loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module
        return module

    elif sys.version_info < (3, 5):  # pragma: no cover
        from importlib.machinery import SourceFileLoader
        module = SourceFileLoader(module_name, path_to_module).load_module()
        sys.modules[module_name] = module
        return module
