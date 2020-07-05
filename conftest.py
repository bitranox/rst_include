import platform
import sys
from typing import List

collect_ignore = ['setup.py']


def pytest_cmdline_preparse(args: List[str]) -> None:
    """
    # run tests on multiple processes if pytest-xdist plugin is available
    # unfortunately it does not work with codecov
    import sys
    if "xdist" in sys.modules:  # pytest-xdist plugin
        import multiprocessing

        num = int(max(multiprocessing.cpu_count() / 2, 1))
        args[:] = ["-n", str(num)] + args
    """

    # add mypy option if not pypy - so mypy will be called with setup.py install test
    # add mypy only on 3.x versions
    # mypy does not find some functions on python 3.6

    additional_arg: List[str]

    if platform.python_implementation() != "PyPy" and sys.version_info >= (3, 5) and sys.version_info != (3, 6):  # type: ignore
        additional_arg = ["--mypy"]
        args[:] = additional_arg + args

    additional_arg = ["--pycodestyle"]
    args[:] = additional_arg + args
