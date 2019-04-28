from rst_include.libs import lib_classes
from rst_include.libs.lib_classes import RstFile, SourceLine
from rst_include.libs import lib_test

import logging
import os
import sys
from typing import Any


def check_l_rst_files(l_rst_files: [RstFile]) -> None:
    """
    >>> test_dir = lib_test.get_test_dir()

    >>> # test no rst files given
    >>> l_rst_files = []
    >>> check_l_rst_files(l_rst_files=l_rst_files)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileNotFoundError: No RST Files given in conf rst_file

    >>> # test rst_file does not exist
    >>> l_rst_files = [lib_classes.RstFile(source='does_not_exist.template.rst', target='does_not_exist.rst')]
    >>> check_l_rst_files(l_rst_files=l_rst_files)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileNotFoundError: RST File "does_not_exist.template.rst" does not exist

    >>> # test rst_file source equals target
    >>> l_rst_files = [lib_classes.RstFile(source=test_dir+'/test1_no_includes_template.rst', target=test_dir+'/test1_no_includes_template.rst')]
    >>> check_l_rst_files(l_rst_files=l_rst_files)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileExistsError: RST File ".../test1_no_includes_template.rst": source and target must not be the same

    >>> # test warning target File exists
    >>> l_rst_files = [lib_classes.RstFile(source=test_dir+'/test1_no_includes_template.rst', target=test_dir+'/test1_no_includes_result.rst')]
    >>> check_l_rst_files(l_rst_files=l_rst_files)

    """
    log_and_raise_if_no_files_given(l_rst_files)
    for rst_file in l_rst_files:
        check_source_and_target(rst_file.source, rst_file.target)


def log_and_raise_if_no_files_given(l_rst_files: [RstFile]) -> None:
    """
    >>> # test no rst_file given
    >>> log_and_raise_if_no_files_given([])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileNotFoundError: No RST Files given in conf rst_file

    >>> # test rst_file given
    >>> l_rst_files = [lib_classes.RstFile(source='does_not_exist.template.rst', target='does_not_exist.rst')]
    >>> log_and_raise_if_no_files_given(l_rst_files = l_rst_files)
    """
    logger = logging.getLogger('check_conf_empty')
    if not l_rst_files:
        error_message = 'No RST Files given in conf rst_file'
        logger.error(error_message)
        raise FileNotFoundError(error_message)


def check_source_and_target(source: str, target: str) -> None:
    """
    >>> check_source_and_target(sys.stdin, sys.stdout)
    """
    log_and_raise_if_source_file_not_ok(source)
    log_and_raise_if_source_file_equals_target_file(source, target)
    log_warning_if_target_file_exist(target)


def log_and_raise_if_source_file_not_ok(source: str) -> None:
    """
    >>> test_dir = lib_test.get_test_dir()

    >>> # test source file ok
    >>> log_and_raise_if_source_file_not_ok( test_dir + '/include1.py')

    >>> # test source is sys.stdin
    >>> log_and_raise_if_source_file_not_ok(sys.stdin)

    >>> # test source file does not exist
    >>> log_and_raise_if_source_file_not_ok('does_not_exist')
    Traceback (most recent call last):
    ...
    FileNotFoundError: RST File "does_not_exist" does not exist

    """
    logger = logging.getLogger('check_conf_source_exist')
    if source != sys.stdin:
        if not file_exists(source):
            error_message = 'RST File "{source}" does not exist'.format(source=source)
            logger.error(error_message)
            raise FileNotFoundError(error_message)


def log_and_raise_if_source_file_equals_target_file(source: str, target: str) -> None:
    """
    >>> # check input sys.stdin, output sys.stdout
    >>> log_and_raise_if_source_file_equals_target_file(sys.stdin, sys.stdout)

    >>> # check not same file
    >>> log_and_raise_if_source_file_equals_target_file('source', 'target')

    >>> # check same file
    >>> log_and_raise_if_source_file_equals_target_file('source', 'source')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileExistsError: RST File "source": source and target must not be the same

    """
    logger = logging.getLogger('check_conf_source_equals_target')
    if source == target:
        error_message = 'RST File "{source}": source and target must not be the same'.format(source=source)
        logger.error(error_message)
        raise FileExistsError(error_message)


def log_warning_if_target_file_exist(target: str) -> None:
    """
    >>> log_warning_if_target_file_exist(target='README.rst')
    >>> log_warning_if_target_file_exist(sys.stdout)

    """
    if target != sys.stdout:
        logger = logging.getLogger('warn_target_exists')
        if file_exists(target):
            logger.warning('RST File "{target}" exists and will be overwritten'.format(target=target))


def file_exists(file: str) -> bool:
    """
    >>> test_dir = lib_test.get_test_dir()

    >>> assert file_exists('does not exist') == False
    >>> assert file_exists(test_dir + '/include1.py') == True
    """
    return os.path.isfile(file)


def read_input(source: Any, encoding: str = 'utf-8-sig') -> str:
    """
    >>> test_dir = lib_test.get_test_dir()

    >>> # read from input file
    >>> assert read_input(test_dir + '/test_read.rst') == 'test file'

    >>> # read from sys.stdin
    >>> test_file_name = test_dir + '/test_read.rst'
    >>> test_file = open(test_file_name, 'r', encoding='utf-8-sig')
    >>> assert read_input(test_file) == 'test file'
    >>> test_file.close()

    """
    if isinstance(source, str):
        with open(source, encoding=encoding, mode='r') as sourcefile:
            content = sourcefile.read()
    else:
        content = source.read()
    return content


def read_source_lines(source: Any, encoding: str = 'utf-8-sig') -> [SourceLine]:
    """
    >>> test_dir = lib_test.get_test_dir()

    >>> # read from input file
    >>> l_source_lines = read_source_lines(test_dir + '/test_read.rst')
    >>> assert l_source_lines[0].line_number == 0
    >>> assert l_source_lines[0].content == 'test file'

    >>> target_file = test_dir + '/write_test.txt'
    >>> write_output(target_file,'test!"§$%&/()=?*#öäüÖÄÜ€\\ntest!"§$%&/()=?*#öäüÖÄÜ€')
    >>> l_source_lines = read_source_lines(target_file)
    >>> assert l_source_lines[0].line_number == 0
    >>> assert l_source_lines[0].content == 'test!"§$%&/()=?*#öäüÖÄÜ€'
    >>> assert l_source_lines[1].line_number == 1
    >>> assert l_source_lines[1].content == 'test!"§$%&/()=?*#öäüÖÄÜ€'

    >>> # read from sys.stdin
    >>> test_file_name = test_dir + '/test_read.rst'
    >>> test_file = open(test_file_name, 'r', encoding='utf-8-sig')
    >>> l_source_lines = read_source_lines(test_file)
    >>> test_file.close()
    >>> assert l_source_lines[0].line_number == 0
    >>> assert l_source_lines[0].content == 'test file'


    """

    if isinstance(source, str):
        with open(source, encoding=encoding, mode='r') as sourcefile:
            content_lines = sourcefile.readlines()
    else:
        content_lines = source.readlines()

    l_source_lines = list()
    line_number = 0
    for content in content_lines:
        source_line = lib_classes.SourceLine()
        source_line.line_number = line_number
        source_line.content = content.rstrip()
        line_number = line_number + 1
        l_source_lines.append(source_line)
    return l_source_lines


def write_output(target: Any, content: str, encoding: str = 'utf-8') -> None:
    """
    >>> test_dir = lib_test.get_test_dir()

    >>> # write to file
    >>> target_file = test_dir + '/write_test.txt'
    >>> write_output(target_file,'test!"§$%&/()=?*#öäüÖÄÜ€\\ntest!"§$%&/()=?*#öäüÖÄÜ€')
    >>> l_source_lines = read_source_lines(target_file)
    >>> assert l_source_lines[0].line_number == 0
    >>> assert l_source_lines[0].content == 'test!"§$%&/()=?*#öäüÖÄÜ€'
    >>> assert l_source_lines[1].line_number == 1
    >>> assert l_source_lines[1].content == 'test!"§$%&/()=?*#öäüÖÄÜ€'

    >>> # write to stdout
    >>> target_file_name = test_dir + '/write_test.txt'
    >>> target_file_object = open(target_file_name, mode='w', encoding='utf-8')
    >>> write_output(target_file_object,'test!"§$%&/()=?*#öäüÖÄÜ€\\ntest!"§$%&/()=?*#öäüÖÄÜ€')
    >>> target_file_object.close()
    >>> l_source_lines = read_source_lines(target_file_name)
    >>> assert l_source_lines[0].line_number == 0
    >>> assert l_source_lines[0].content == 'test!"§$%&/()=?*#öäüÖÄÜ€'
    >>> assert l_source_lines[1].line_number == 1
    >>> assert l_source_lines[1].content == 'test!"§$%&/()=?*#öäüÖÄÜ€'


    """

    if isinstance(target, str):
        with open(target, encoding=encoding, mode='w') as file:
            file.write(content)
    else:
        target.write(content)
