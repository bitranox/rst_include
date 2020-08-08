# STDLIB
import importlib
import importlib.util
import pathlib3x as pathlib
import sys
from typing import Tuple, Union, IO

# OWN
import lib_log_utils

# PROJECT
try:
    from .libs import lib_main
except (ImportError, ModuleNotFoundError):              # pragma: no cover
    from libs import lib_main       # type: ignore      # pragma: no cover


# CONSTANTS
CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def include(source: str, target: str, quiet: bool, inplace: bool, source_encoding: str, target_encoding: str) -> None:
    lib_log_utils.log_handlers.set_stream_handler()

    target, quiet = adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace)

    path_source: Union[pathlib.Path, IO[str]]
    path_target: Union[pathlib.Path, IO[str]]

    if source == '-':
        path_source = sys.stdin
    else:
        path_source = pathlib.Path(source)

    if target == '-':
        path_target = sys.stdout
        quiet = True
    else:
        path_target = pathlib.Path(target)

    lib_log_utils.log_settings.quiet = quiet
    lib_main.rst_inc(source=path_source, target=path_target, source_encoding=source_encoding, target_encoding=target_encoding, inplace=inplace)


def replace(source: str, target: str, str_pattern: str, str_replace: str, count: int,
            quiet: bool, inplace: bool, source_encoding: str, target_encoding: str) -> None:

    target, quiet = adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace)

    path_source: Union[pathlib.Path, IO[str]]
    path_target: Union[pathlib.Path, IO[str]]

    if source == '-':
        path_source = sys.stdin
    else:
        path_source = pathlib.Path(source)

    if target == '-':
        path_target = sys.stdout
        quiet = True
    else:
        path_target = pathlib.Path(target)

    lib_log_utils.log_handlers.set_stream_handler()
    lib_log_utils.log_settings.quiet = quiet
    lib_main.rst_str_replace(source=path_source, target=path_target, str_pattern=str_pattern, str_replace=str_replace, count=count,
                             source_encoding=source_encoding, target_encoding=target_encoding, inplace=inplace)


def import_module_from_file(module_fullpath: Union[pathlib.Path, str], reload: bool = False):   # type: ignore
    """
    TODO : replace with lib_import when avail maybe take from pycharm
    """
    module_fullpath = pathlib.Path(module_fullpath)

    if not module_fullpath.suffix == '.py':
        module_fullpath = module_fullpath.with_suffix('.py')

    module_name = module_fullpath.stem

    if not reload and module_name in sys.modules:
        return sys.modules[module_name]

    if reload:
        invalidate_caches()

    if sys.version_info < (3, 6):
        sys.path.append(str(module_fullpath.parent))
        mod = importlib.import_module(module_name)
        sys.path.pop()
        sys.modules[module_name] = mod

    else:
        sys.path.append(str(module_fullpath.parent))

        spec = importlib.util.spec_from_file_location(module_name, module_fullpath)
        if spec is None:
            sys.path.pop()
            raise ImportError('can not get spec from file location "{}"'.format(module_fullpath))

        try:
            mod = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = mod
        except Exception as exc:
            raise ImportError('can not load module "{}"'.format(module_name)) from exc
        finally:
            sys.path.pop()
            sys.path.append(str(module_fullpath.parent))

        try:
            spec.loader.exec_module(mod)    # type: ignore
        except Exception as exc:
            sys.path.pop()
            raise ImportWarning('module "{}" reloaded, but can not be executed'.format(module_name)) from exc

    return mod


def invalidate_caches() -> None:    # see https://docs.python.org/3/library/importlib.html
    if sys.version_info >= (3, 3):
        importlib.invalidate_caches()


def adjust_cli_parameters(target: str, quiet: bool, inplace: bool) -> Tuple[str, bool]:
    """
    Returns adjusted target and quiet, because we have to be quiet when target = '-'
    >>> target = 'test'
    >>> quiet = False
    >>> inplace = False
    >>> assert adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace) == ('test', False)

    >>> inplace = True
    >>> assert adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace) == ('', False)

    >>> target = '-'
    >>> inplace = True
    >>> assert adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace) == ('', False)

    >>> target = '-'
    >>> inplace = False
    >>> assert adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace) == ('-', True)


    """
    if inplace:
        target = ''

    if target == '-':
        quiet = True

    return target, quiet


# entry point if main
if __name__ == '__main__':
    print('this is a library only, the executable is named rst_include_cli.py')
