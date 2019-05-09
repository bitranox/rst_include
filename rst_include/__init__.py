__title__ = 'rst_include'
__version__ = '1.0.4'
__name__ = 'rst_include'

import errno
import sys
import logging
from .libs.lib_classes import RstFile
from .libs.lib_classes import RstConf
from .libs.lib_main import rst_str_replace
from .libs.lib_main import rst_inc_from_config
from .libs.lib_main import rst_inc


def main(sys_argv=sys.argv[1:]):
    from .libs import lib_args
    from .libs import lib_log
    from .libs import lib_test

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
    >>> assert lib_test_compare_results.compare_results_equal(expected_file_replace, target_file)

    >>> # test include source and target given
    >>> lib_test.remove_file_silent(target_file)
    >>> main(['include', '-s', source_file, '-t', target_file])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> assert lib_test_compare_results.compare_results_equal(expected_file, target_file)

    >>> # test default config file from current directory
    >>> save_dir = os.path.abspath(os.curdir)
    >>> test_dir = lib_test.get_test_dir()
    >>> os.chdir(test_dir)
    >>> lib_test.remove_file_silent(target_file)
    >>> main(['include', '-c'])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> assert lib_test_compare_results.compare_results_equal(expected_file, target_file)
    >>> os.chdir(save_dir)

    >>> # test load config file
    >>> lib_test.remove_file_silent(target_file)
    >>> config_file = lib_test.get_test_dir() + '/conf_rst_include_test.py'
    >>> main(['include', '-c', config_file])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> assert lib_test_compare_results.compare_results_equal(expected_file, target_file)

    """

    def handle_include_command(argparse_namespace, sys_argv):
        if lib_args.cmd_args_config_flag_given(sys_argv):
            rst_inc_from_config(argparse_namespace.config)
        else:
            rst_inc(argparse_namespace.source,
                    argparse_namespace.target,
                    argparse_namespace.source_encoding,
                    argparse_namespace.target_encoding)

    try:

        lib_log.setup_logger()
        argparse_namespace, parser = lib_args.parse_args(sys_argv)

        if lib_args.is_replace_command(argparse_namespace):
            rst_str_replace(argparse_namespace.source, argparse_namespace.target,
                            argparse_namespace.old, argparse_namespace.new, argparse_namespace.count,
                            argparse_namespace.source_encoding, argparse_namespace.target_encoding)
        elif lib_args.is_include_command(argparse_namespace):
            handle_include_command(argparse_namespace, sys_argv)
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
