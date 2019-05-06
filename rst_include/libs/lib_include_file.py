import logging
import sys
from typing import List

try:
    from rst_include.libs.lib_classes import Block
    from rst_include.libs import lib_get_include_options
    from rst_include.libs import lib_list
    from rst_include.libs import lib_str
    from rst_include.libs import lib_test
except ImportError:  # pragma: no cover
    from .lib_classes import Block
    from . import lib_get_include_options
    from . import lib_list
    from . import lib_str
    from . import lib_test


def read_include_file(block: Block) -> List[str]:
    """
    >>> block = lib_test.get_test_block_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> content = read_include_file(block)
    >>> assert content[0] == 'def my_include():'
    >>> assert content[1] == '    pass'
    >>> content[2]    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    >>> assert block.include_file_lines == ['def my_include():', '    pass']

    >>> block.include_filename_absolut='non_existing_file'
    >>> content = read_include_file(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    OSError: Error in File "...", Line 47100: File read Error "[Errno ...] No such file or directory: 'non_existing_file'"


    """

    logger = logging.getLogger('read_include_file')

    try:
        with open(block.include_filename_absolut, mode='r', encoding=block.include_file_encoding) as include_file:
            include_file_lines = include_file.readlines()
            include_file_lines = [line.rstrip() for line in include_file_lines]
            include_file_lines = lib_list.strip_list_of_strings(include_file_lines)
            block.include_file_lines = include_file_lines
        return include_file_lines

    except Exception:
        exc_info = sys.exc_info()[1]
        s_error = 'Error in File "{source_file}", Line {line_number}: File read Error "{exc_info}"'.format(
            source_file=block.source_file_name,
            line_number=block.l_source_lines[0].line_number,
            exc_info=exc_info)
        logger.error(s_error)
        raise IOError(s_error)


def process_include_file_lines(block: Block) -> None:
    """
    >>> block = lib_test.read_include_file_2()
    >>> process_include_file_lines(block)
    >>> assert block.include_file_sliced_content == 'def my_include2_2():\\n    pass\\n\\n    pass'
    """
    slice_include_file_lines(block)
    slice_include_file_markers(block)


def slice_include_file_lines(block: Block) -> None:
    """
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_lines = ['\\n'] + block.include_file_lines   # add an empty line in front and end
    >>> slice_include_file_lines(block)
    >>> block.include_file_lines  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    ['def my_include2_1():', '    pass', '', ... 'def my_include2_3():', '    pass']
    """
    block.include_file_lines = block.include_file_lines[block.include_file_start_line:block.include_file_end_line]
    block.include_file_lines = lib_list.strip_list_of_strings(block.include_file_lines)


def slice_include_file_markers(block: Block) -> None:
    """
    >>> # test ok
    >>> block = lib_test.read_include_file_2()
    >>> slice_include_file_lines(block)
    >>> slice_include_file_markers(block)
    >>> assert block.include_file_sliced_content == 'def my_include2_2():\\n    pass\\n\\n    pass'

    >>> # test start_after not found, start_line_ and end_line set
    >>> block = lib_test.read_include_file_2()
    >>> slice_include_file_lines(block)
    >>> block.include_file_start_after = 'start_after_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : start-after "start_after_not_found" not found between start_line: 6 and end_line: 25

    >>> # test start_after not found, start_line NOT set, end_line set
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_start_line=None
    >>> slice_include_file_lines(block)
    >>> block.include_file_start_after = 'start_after_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : start-after "start_after_not_found" not found before end-line: 25

    >>> # test start_after not found, start_line set, end_line NOT set
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_end_line=None
    >>> slice_include_file_lines(block)
    >>> block.include_file_start_after = 'start_after_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : start-after "start_after_not_found" not found after start-line: 6

    >>> # test start_after not found, start_line NOT set, end_line NOT set
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_start_line=None
    >>> block.include_file_end_line=None
    >>> slice_include_file_lines(block)
    >>> block.include_file_start_after = 'start_after_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : start-after "start_after_not_found" not found

    >>> # test end_before not found, start_line_ and end_line set
    >>> block = lib_test.read_include_file_2()
    >>> slice_include_file_lines(block)
    >>> block.include_file_end_before = 'end_before_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : end-before "end_before_not_found" not found between start_line: 6 and end_line: 25 after start-after: # start-marker


    >>> # test end_before not found, start_line NOT set, end_line set
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_start_line=None
    >>> slice_include_file_lines(block)
    >>> block.include_file_end_before = 'end_before_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : end-before "end_before_not_found" not found before end-line: 25 after start-after: # start-marker


    >>> # test end_before not found, start_line set, end_line NOT set
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_end_line=None
    >>> slice_include_file_lines(block)
    >>> block.include_file_end_before = 'end_before_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : end-before "end_before_not_found" not found after start-line: 6 after start-after: # start-marker


    >>> # test end_before not found, start_line NOT set, end_line NOT set
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_start_line=None
    >>> block.include_file_end_line=None
    >>> slice_include_file_lines(block)
    >>> block.include_file_end_before = 'end_before_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : end-before "end_before_not_found" not found after start-after: # start-marker

    """
    content = '\n'.join(block.include_file_lines)
    # save memory
    del block.include_file_lines

    if block.include_file_start_after:
        log_and_raise_if_start_after_not_found_in_string(content, block)
        content = content.split(block.include_file_start_after, 1)[1]

    if block.include_file_end_before:
        log_and_raise_if_end_before_not_found_in_string(content, block)
        content, tail = content.split(block.include_file_end_before, 1)

    content = lib_str.strip_multiline_string(content)
    block.include_file_sliced_content = content


def log_and_raise_if_start_after_not_found_in_string(content, block: Block) -> None:
    logger = logging.getLogger('slice_include_file_start_after')
    if block.include_file_start_after not in content:
        s_error = 'Error in File "{source_file}", Line {line_number}: include File "{include_filename}" : start-after "{start_after}" not found'.format(
            source_file=block.source_file_name,
            line_number=block.l_source_lines[0].line_number,
            include_filename=block.include_filename,
            start_after=block.include_file_start_after)
        s_error = s_error + get_additional_error_string(block)
        logger.error(s_error)
        raise ValueError(s_error)


def log_and_raise_if_end_before_not_found_in_string(content, block: Block) -> None:
    logger = logging.getLogger('slice_include_file_end_before')
    if block.include_file_end_before not in content:
        s_error = 'Error in File "{source_file}", Line {line_number}: include File "{include_filename}" : end-before "{end_before}" not found'.format(
            source_file=block.source_file_name,
            line_number=block.l_source_lines[0].line_number,
            include_filename=block.include_filename,
            end_before=block.include_file_end_before)
        s_error = s_error + get_additional_error_string(block)
        s_error = s_error + get_additional_error_string_start_after(block)
        logger.error(s_error)
        raise ValueError(s_error)


def get_additional_error_string(block: Block) -> str:
    s_error = ''
    if block.include_file_start_line and block.include_file_end_line:
        s_error = s_error + ' between start_line: {start_line} and end_line: {end_line}'.format(
            start_line=block.include_file_start_line, end_line=block.include_file_end_line)
    elif block.include_file_start_line:
        s_error = s_error + ' after start-line: {start_line}'.format(start_line=block.include_file_start_line)
    elif block.include_file_end_line:
        s_error = s_error + ' before end-line: {end_line}'.format(end_line=block.include_file_end_line)
    return s_error


def get_additional_error_string_start_after(block: Block) -> str:
    s_error = ''
    if block.include_file_start_after:
        s_error = s_error + ' after start-after: {start_after}'.format(start_after=block.include_file_start_after)
    return s_error
