import sys
import traceback
from typing import Any, TextIO


class _Config(object):
    traceback: bool = False


config = _Config()


def get_system_exit_code(exc: BaseException) -> int:
    """
    Return the exit code for linux or windows, based on the exception.
    If, on windows, the winerror is set on the Exception, we return that winerror code.

    >>> try:
    ...     raise RuntimeError()
    ... except RuntimeError as exc:
    ...     assert get_system_exit_code(exc) == 1
    ...     setattr(exc, 'winerror', 42)
    ...     assert get_system_exit_code(exc) == 42
    ...     setattr(exc, 'winerror', None)
    ...     assert get_system_exit_code(exc) == 1

    """

    # from https://www.thegeekstuff.com/2010/10/linux-error-codes
    # dict key sorted from most specific to unspecific
    posix_exceptions = {FileNotFoundError: 2, PermissionError: 13, FileExistsError: 17, TypeError: 22,
                        ValueError: 22, RuntimeError: 1, BaseException: 1}
    windows_exceptions = {FileNotFoundError: 2, PermissionError: 5, ValueError: 13, FileExistsError: 80, TypeError: 87,
                          RuntimeError: 1, BaseException: 1}

    if hasattr(exc, 'winerror'):
        try:
            exit_code = int(exc.winerror)    # type: ignore
            return exit_code
        except (AttributeError, TypeError):
            pass

    if 'posix' in sys.builtin_module_names:
        exceptions = posix_exceptions
    else:
        exceptions = windows_exceptions

    for exception in exceptions:
        if isinstance(exc, exception):
            return exceptions[exception]
    # this should never happen
    return 1   # pragma: no cover


def print_exception_message(trace_back: bool = config.traceback, stream: TextIO = sys.stderr) -> None:
    """
    Prints the Exception Message to stderr

    if trace_back is True, it also prints the traceback information


    >>> # test with exc_info = None
    >>> print_exception_message()

    >>> # test with exc_info
    >>> try:
    ...     raise FileNotFoundError('test')
    ... except Exception:       # noqa
    ...     print_exception_message(False)
    ...     print_exception_message(True)

    >>> # test with subprocess to get stdout, stderr
    >>> import subprocess
    >>> try:
    ...     discard=subprocess.run('unknown_command', shell=True, check=True)
    ... except subprocess.CalledProcessError:
    ...     print_exception_message(False)
    ...     print_exception_message(True)

    """
    exc_info = sys.exc_info()[1]
    if exc_info is not None:
        exc_info_type = type(exc_info).__name__
        exc_info_msg = ''.join([exc_info_type, ': ', str(exc_info.args[0])])
        if trace_back:
            print_stdout(exc_info)
            print_stderr(exc_info)
            exc_info_msg = ''.join(['Traceback Information : \n', str(traceback.format_exc())]).rstrip('\n')
        print(exc_info_msg, file=stream)


def print_stdout(exc_info: Any) -> None:
    """
    >>> class ExcInfo(object):
    ...    pass

    >>> exc_info = ExcInfo()

    >>> # test no stdout attribute
    >>> print_stdout(exc_info)

    >>> # test stdout=None
    >>> exc_info.stdout=None
    >>> print_stdout(exc_info)

    >>> # test stdout
    >>> exc_info.stdout=b'test'
    >>> print_stdout(exc_info)
    STDOUT: test

    """
    encoding = sys.getdefaultencoding()
    if hasattr(exc_info, 'stdout'):
        if exc_info.stdout is not None:
            assert isinstance(exc_info.stdout, bytes)
            print('STDOUT: ' + exc_info.stdout.decode(encoding))


def print_stderr(exc_info: Any) -> None:
    """
    >>> class ExcInfo(object):
    ...    pass

    >>> exc_info = ExcInfo()

    >>> # test no stdout attribute
    >>> print_stderr(exc_info)

    >>> # test stdout=None
    >>> exc_info.stderr=None
    >>> print_stderr(exc_info)

    >>> # test stdout
    >>> exc_info.stderr=b'test'
    >>> print_stderr(exc_info)
    STDERR: test

    """
    encoding = sys.getdefaultencoding()
    if hasattr(exc_info, 'stderr'):
        if exc_info.stderr is not None:
            assert isinstance(exc_info.stderr, bytes)
            print('STDERR: ' + exc_info.stderr.decode(encoding))
