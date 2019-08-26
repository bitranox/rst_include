# STDLIB
import argparse
import errno
import os
import sys
from typing import List

# OWN
import lib_log_utils

# PROJECT
try:
    from . import *
    from .libs import lib_args
    from .libs import lib_main
    from .libs import lib_test
    from .libs import lib_test_compare_results
except ImportError:                                  # type: ignore # pragma: no cover
    from libs import lib_args                        # type: ignore # pragma: no cover
    from libs import lib_main                        # type: ignore # pragma: no cover
    from libs import lib_test                        # type: ignore # pragma: no cover
    from libs import lib_test_compare_results        # type: ignore # pragma: no cover


def main(sys_argv: List[str] = sys.argv[1:]) -> None:
    """
    >>> import pathlib
    >>> source_file = lib_test.get_test_dir() + '/../../.docs/README_template.rst'
    >>> target_file = lib_test.get_test_dir() + '/../../.docs/README_template_doctest_included.rst'
    >>> if pathlib.Path(target_file).exists(): pathlib.Path(target_file).unlink()
    >>> main(['include', '-s', source_file, '-t', target_file])
    >>> main(['include', '-s', source_file, '-t', target_file])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [...] WARNING : RST File ... exists and will be overwritten
    >>> lib_test.run_template_tests()
    >>> lib_test.run_template_tests_not_supported()

    >>> # test no parameter given
    >>> main([])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    usage: ...

    >>> # test help
    >>> main(['-h'])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    SystemExit: 0

    >>> # test replace
    >>> source_file = lib_test.get_test_dir() + '/test1_no_includes_template.rst'
    >>> target_file = lib_test.get_test_dir() + '/test1_no_includes_result.rst'
    >>> expected_file_replace = lib_test.get_test_dir() + '/test1_no_includes_expected_replace.rst'
    >>> expected_file = lib_test.get_test_dir() + '/test1_no_includes_expected.rst'

    >>> lib_test.remove_file_silent(target_file)
    >>> main(['replace', '-s', source_file, '-t', target_file, '=', '*', '-1'])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> assert lib_test_compare_results.compare_results_equal(expected_file_replace, target_file)

    >>> # test include source and target given
    >>> lib_test.remove_file_silent(target_file)
    >>> main(['include', '-s', source_file, '-t', target_file])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> assert lib_test_compare_results.compare_results_equal(expected_file, target_file)

    """
    try:
        lib_log_utils.setup_console_logger()
        argparse_namespace, parser = lib_args.parse_args(sys_argv)

        if argparse_namespace.which_parser == 'parser_replace':
            lib_main.rst_str_replace(argparse_namespace.source, argparse_namespace.target,
                                     argparse_namespace.old, argparse_namespace.new, argparse_namespace.count,
                                     argparse_namespace.source_encoding, argparse_namespace.target_encoding, argparse_namespace.inplace)
        elif argparse_namespace.which_parser == 'parser_include':
            lib_main.rst_inc(argparse_namespace.source,
                             argparse_namespace.target,
                             argparse_namespace.source_encoding,
                             argparse_namespace.target_encoding,
                             argparse_namespace.inplace)
        else:
            parser.print_help()

    except FileNotFoundError:
        # see https://www.thegeekstuff.com/2010/10/linux-error-codes for error codes
        # No such file or directory
        sys.exit(errno.ENOENT)      # pragma: no cover
    except FileExistsError:
        # File exists
        sys.exit(errno.EEXIST)      # pragma: no cover
    except TypeError:
        # Invalid Argument
        sys.exit(errno.EINVAL)      # pragma: no cover
        # Invalid Argument
    except ValueError:
        sys.exit(errno.EINVAL)      # pragma: no cover


if __name__ == '__main__':
    main()                          # pragma: no cover
