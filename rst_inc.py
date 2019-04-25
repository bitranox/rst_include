import errno
import os
from rst_include import *
from rst_include.libs import lib_log
from rst_include.libs import lib_args
from rst_include.libs import lib_test

import sys

# for python 2.7 compatibility
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError
    FileExistsError = IOError


def main(cmd_args=sys.argv[1:]):
    # type ([str]) -> None
    """

    >>> source_file = './docs/README_template.rst'
    >>> target_file = './docs/README_template_included.rst'
    >>> main(['include', '-s', source_file, '-t', target_file])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE




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
    >>> assert lib_test.compare_results_equal(expected_file_replace, target_file)

    >>> # test include source and target given
    >>> lib_test.remove_file_silent(target_file)
    >>> main(['include', '-s', source_file, '-t', target_file])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> assert lib_test.compare_results_equal(expected_file, target_file)

    >>> # test default config file from current directory
    >>> save_dir = os.path.abspath(os.curdir)
    >>> test_dir = lib_test.get_test_dir()
    >>> os.chdir(test_dir)
    >>> lib_test.remove_file_silent(target_file)
    >>> main(['include', '-c'])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> assert lib_test.compare_results_equal(expected_file, target_file)
    >>> os.chdir(save_dir)

    >>> # test load config file
    >>> lib_test.remove_file_silent(target_file)
    >>> config_file = lib_test.get_test_dir() + '/conf_rst_include_test.py'
    >>> main(['include', '-c', config_file])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> assert lib_test.compare_results_equal(expected_file, target_file)

    """

    args, parser = lib_args.parse_args(cmd_args)

    if lib_args.is_replace_command(args):
        rst_str_replace(args.source, args.target, args.old, args.new, args.count, args.source_encoding, args.target_encoding)

    elif lib_args.is_include_command(args):
        if lib_args.cmd_args_config_flag_given(cmd_args):
            rst_inc_from_config(args.config)
        else:
            rst_inc(args.source, args.target, args.source_encoding, args.target_encoding)
    else:
        parser.print_help()


if __name__ == '__main__':
    try:
        lib_log.setup_logger()
        main()
    except FileNotFoundError:
        # see https://www.thegeekstuff.com/2010/10/linux-error-codes for error codes
        sys.exit(errno.ENOENT)      # No such file or directory
    except FileExistsError:
        sys.exit(errno.EEXIST)      # File exists
    except TypeError:
        sys.exit(errno.EINVAL)      # Invalid Argument
    except ValueError:
        sys.exit(errno.EINVAL)      # Invalid Argument
