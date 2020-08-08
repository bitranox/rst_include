# STDLIB
from collections import OrderedDict
from typing import List, Union, IO


# OWN
import lib_list
import lib_log_utils
import pathlib3x as pathlib

try:
    # for pytest
    from .lib_classes import Block, RstFile
    from . import lib_assemble_block
    from . import lib_get_include_options
    from . import lib_str
    from . import lib_test
except (ImportError, ModuleNotFoundError):      # pragma: no cover
    # for local doctest in pycharm
    from lib_classes import Block, RstFile      # type: ignore # pragma: no cover
    import lib_assemble_block                   # type: ignore # pragma: no cover
    import lib_get_include_options              # type: ignore # pragma: no cover
    import lib_str                              # type: ignore # pragma: no cover
    import lib_test                             # type: ignore # pragma: no cover


class IncludeTrace(object):
    def __init__(self, path_source_file: Union[str, pathlib.Path, IO[str]], line_number: int):
        self.path_source_file = path_source_file
        self.line_number = line_number


includes_stack = OrderedDict()                        # type: OrderedDict[pathlib.Path, IncludeTrace]


def read_include_file(block: Block) -> List[str]:
    """
    >>> block = lib_test.get_test_block_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> content = read_include_file(block)
    >>> assert content[0] == 'def my_include() -> None:'
    >>> assert content[1] == '    pass'
    >>> content[2]    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    >>> assert block.include_file_lines == ['def my_include() -> None:', '    pass']

    >>> block.include_filename_absolut=pathlib.Path('non_existing_file')
    >>> content = read_include_file(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    OSError: Error in File ".../tests/README.template.rst", Line 47100: File not found : "non_existing_file"

    """

    try:
        if not block.include_filename_absolut.is_file():
            raise FileNotFoundError()

        if block.include_filename_absolut in includes_stack:
            raise RuntimeError('Recursion detected')

        includes_stack[block.include_filename_absolut] = IncludeTrace(block.source, block.l_source_lines[0].line_number)

        rst_file = RstFile(source=block.include_filename_absolut, target=None, source_encoding=block.include_file_encoding)
        content = lib_assemble_block.create_rst_file_from_template(rst_file)
        include_file_lines = content.split('\n')
        include_file_lines = right_strip_lines_from_list(include_file_lines)
        include_file_lines = delete_empty_lines_from_list(include_file_lines)
        block.include_file_lines = include_file_lines
        includes_stack.popitem()
        return include_file_lines

    except FileNotFoundError:
        s_error = 'Error in File "{source_file}", Line {line_number}: File not found : '\
                  '"{include_file}"'.format(source_file=block.source,
                                            line_number=block.l_source_lines[0].line_number,
                                            include_file=block.include_filename_absolut)
        lib_log_utils.log_traceback.log_exception_traceback(s_error)
        raise IOError(s_error)


def delete_empty_lines_from_list(source_lines: List[str]) -> List[str]:
    source_lines_without_empty_lines = [str(element) for element in lib_list.ls_strip_list(source_lines)]
    return source_lines_without_empty_lines


def right_strip_lines_from_list(source_lines: List[str]) -> List[str]:
    right_striped_lines = [line.rstrip() for line in source_lines]
    return right_striped_lines


def process_include_file_lines(block: Block) -> None:
    """
    >>> block = lib_test.read_include_file_2()
    >>> process_include_file_lines(block)
    >>> assert block.include_file_sliced_content == 'def my_include2_2() -> None:\\n    pass\\n\\n    pass'
    """
    slice_include_file_lines(block)
    slice_include_file_markers(block)


def slice_include_file_lines(block: Block) -> None:
    """
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_lines = ['\\n'] + block.include_file_lines   # add an empty line in front and end
    >>> slice_include_file_lines(block)
    >>> block.include_file_lines  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    ['def my_include2_1() -> None:', '    pass', '', ... 'def my_include2_3() -> None:', '    pass']
    """
    block.include_file_lines = block.include_file_lines[block.include_file_start_line:block.include_file_end_line]
    block.include_file_lines = lib_list.ls_strip_list(block.include_file_lines)


def slice_include_file_markers(block: Block) -> None:
    """
    >>> # test ok
    >>> block = lib_test.read_include_file_2()
    >>> slice_include_file_lines(block)
    >>> slice_include_file_markers(block)
    >>> assert block.include_file_sliced_content == 'def my_include2_2() -> None:\\n    pass\\n\\n    pass'

    >>> # test start_after not found, start_line_ and end_line set
    >>> block = lib_test.read_include_file_2()
    >>> slice_include_file_lines(block)
    >>> block.include_file_start_after = 'start_after_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : start-after "start_after_not_found" not found ...

    >>> # test start_after not found, start_line NOT set, end_line set
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_start_line=None
    >>> slice_include_file_lines(block)
    >>> block.include_file_start_after = 'start_after_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : start-after "start_after_not_found" not found ...

    >>> # test start_after not found, start_line set, end_line NOT set
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_end_line=None
    >>> slice_include_file_lines(block)
    >>> block.include_file_start_after = 'start_after_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : start-after "start_after_not_found" not found ...

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
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : end-before "end_before_not_found" not found ...


    >>> # test end_before not found, start_line NOT set, end_line set
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_start_line=None
    >>> slice_include_file_lines(block)
    >>> block.include_file_end_before = 'end_before_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : end-before "end_before_not_found" not found ...


    >>> # test end_before not found, start_line set, end_line NOT set
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_end_line=None
    >>> slice_include_file_lines(block)
    >>> block.include_file_end_before = 'end_before_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : end-before "end_before_not_found" not found ...


    >>> # test end_before not found, start_line NOT set, end_line NOT set
    >>> block = lib_test.read_include_file_2()
    >>> block.include_file_start_line=None
    >>> block.include_file_end_line=None
    >>> slice_include_file_lines(block)
    >>> block.include_file_end_before = 'end_before_not_found'
    >>> slice_include_file_markers(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47100: include File "include2.py" : end-before "end_before_not_found" not found ...

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


def log_and_raise_if_start_after_not_found_in_string(content: str, block: Block) -> None:
    if block.include_file_start_after not in content:
        s_error = 'Error in File "{source_file}", Line {line_number}: include File "{include_filename}" : start-after "{start_after}" not found'.format(
            source_file=block.source,
            line_number=block.l_source_lines[0].line_number,
            include_filename=block.include_filename,
            start_after=block.include_file_start_after)
        s_error = s_error + get_additional_error_string(block)
        lib_log_utils.log_error(s_error)
        raise ValueError(s_error)


def log_and_raise_if_end_before_not_found_in_string(content: str, block: Block) -> None:
    if block.include_file_end_before not in content:
        s_error = 'Error in File "{source_file}", Line {line_number}: include File "{include_filename}" : end-before "{end_before}" not found'.format(
            source_file=block.source,
            line_number=block.l_source_lines[0].line_number,
            include_filename=block.include_filename,
            end_before=block.include_file_end_before)
        s_error = s_error + get_additional_error_string(block)
        s_error = s_error + get_additional_error_string_start_after(block)
        lib_log_utils.log_error(s_error)
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
