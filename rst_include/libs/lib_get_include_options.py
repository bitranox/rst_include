# STDLIB
from typing import List, Tuple, Union

# OWN
import lib_log_utils
import pathlib3x as pathlib

try:
    # for pytest
    from .lib_classes import Block, SourceLine
    from . import lib_block_options
    from . import lib_source_line
    from . import lib_test
except ImportError:                                 # pragma: no cover
    # for local doctest in pycharm
    from lib_classes import Block, SourceLine       # type: ignore # pragma: no cover
    import lib_block_options                        # type: ignore # pragma: no cover
    import lib_source_line                          # type: ignore # pragma: no cover
    import lib_test                                 # type: ignore # pragma: no cover


def get_include_options(block: Block) -> None:
    """
    >>> block = lib_test.get_test_block_ok()
    >>> get_include_options(block)
    """
    get_include_filename(block)
    get_include_file_code(block)
    get_include_file_encoding(block)
    get_include_file_start_line(block)
    get_include_file_end_line(block)
    get_include_file_start_after(block)
    get_include_file_end_before(block)
    get_include_block_pass_through_options(block)
    get_include_block_additional_content(block)
    # save memory
    block.l_source_lines = block.l_source_lines[:1]  # we still need the first line to get line numbers for error messages
    get_blanks_to_add_to_content(block)


def get_include_block_pass_through_options(block: Block) -> List[SourceLine]:
    """
    >>> block = lib_test.get_test_block_ok()
    >>> pass_through_options = get_include_block_pass_through_options(block)
    >>> assert pass_through_options[0].content == '    :pass-through1:'
    >>> assert pass_through_options[1].content == '    :pass-through2: value2'
    >>> pass_through_options[2].content   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    """
    pass_through_options = list()                       # type: List[SourceLine]
    for source_line in block.l_source_lines[1:]:
        if lib_source_line.source_line_contains_option(source_line):
            append_if_pass_through_option(source_line, pass_through_options)
        else:
            break
    block.pass_through_options = pass_through_options
    return pass_through_options


def append_if_pass_through_option(source_line: SourceLine, pass_through_options: List[SourceLine]) -> None:
    processed_option_keys = ['code', 'start-line', 'end-line', 'encoding', 'start-after', 'end-before']
    option_key = lib_block_options.get_option_key_from_source_line(source_line)
    if option_key not in processed_option_keys:
        pass_through_options.append(source_line)


def get_include_block_additional_content(block: Block) -> List[SourceLine]:
    """
    >>> block = lib_test.get_test_block_ok()
    >>> l_additional_content = get_include_block_additional_content(block)
    >>> assert l_additional_content[0].content == '    '
    >>> assert l_additional_content[1].content == ''
    >>> assert l_additional_content[2].content == '    :no-option:'
    >>> assert l_additional_content[3].content == ''
    >>> assert l_additional_content[4].content == 'additional content1'
    >>> assert l_additional_content[5].content == 'additional content2'
    >>> assert l_additional_content[6].content == 'additional content3'
    >>> assert l_additional_content[7].content == 'additional content4'
    >>> assert l_additional_content[8].content == 'additional content5'
    >>> assert l_additional_content[9].content == ''
    >>> l_additional_content[10]   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    """
    max_line = len(block.l_source_lines)
    l_additional_content = list()                       # type: List[SourceLine]
    for index in range(max_line):
        if not lib_source_line.source_line_contains_option(block.l_source_lines[index]):
            l_additional_content = block.l_source_lines[index:]
            break
    block.additional_content = l_additional_content
    return l_additional_content


def get_include_filename(block: Block) -> Tuple[pathlib.Path, pathlib.Path]:
    """
    >>> block = lib_test.get_test_block_ok()

    >>> # test include Filename OK
    >>> get_include_filename(block)
    (...Path('include1.py'), ...Path('.../tests/include1.py'))

    >>> # test Error no include Filename given
    >>> block = lib_test.get_test_block_no_include_filename()
    >>> get_include_filename(block)
    Traceback (most recent call last):
    ...
    FileNotFoundError: Error in File ".../README.template.rst", Line 47100: no include filename

    >>> # test Error include File does not exist
    >>> block = lib_test.get_test_block_include_filename_not_existing()
    >>> get_include_filename(block)
    Traceback (most recent call last):
    ...
    FileNotFoundError: Error in File ".../README.template.rst", Line 47100: include File "not_existing.file" does not exist

    """
    include_line = block.l_source_lines[0].content
    include_filename = include_line.split('.. include::')[1].strip()
    if not include_filename:
        s_error = 'Error in File "{source_file}", Line {line_number}: no include filename'.format(
            source_file=block.source, line_number=block.l_source_lines[0].line_number)
        lib_log_utils.log_error(s_error)
        raise FileNotFoundError(s_error)

    path_include_file = pathlib.Path(include_filename)

    if path_include_file.is_absolute():
        path_include_file_absolut = path_include_file.resolve()
    else:
        if isinstance(block.source, pathlib.Path):
            path_include_file_absolut = (pathlib.Path(block.source).parent / path_include_file).resolve()
        else:
            path_include_file_absolut = (pathlib.Path.cwd() / path_include_file).resolve()

    if not path_include_file_absolut.is_file():
        s_error = 'Error in File "{source_file}", Line {line_number}: include File "{include_filename}" does not exist'.format(
            source_file=block.source,
            line_number=block.l_source_lines[0].line_number,
            include_filename=path_include_file)
        lib_log_utils.log_error(s_error)
        raise FileNotFoundError(s_error)
    block.include_filename = path_include_file
    block.include_filename_absolut = path_include_file_absolut
    return path_include_file, path_include_file_absolut


def get_include_file_code(block: Block) -> str:
    """
    >>> # test code set to python
    >>> block = lib_test.get_test_block_ok()
    >>> get_include_file_code(block)
    'python'
    >>> assert block.include_file_code == 'python'

    >>> # test code not set
    >>> block = lib_test.get_test_block_code_not_set()
    >>> get_include_file_code(block)
    ''
    >>> assert block.include_file_code == ''

    >>> # test code invalid
    >>> block = lib_test.get_test_block_code_invalid()
    >>> get_include_file_code(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47101: option "code" has no value
    """

    code = ''
    if lib_block_options.is_option_in_block('code', block):
        code = lib_block_options.get_option_value_from_block_or_raise_if_empty_or_invalid('code', block)
    block.include_file_code = code
    return code


def get_include_file_encoding(block: Block) -> str:
    """
    >>> block = lib_test.get_test_block_ok()
    >>> # test encoding set to utf-8
    >>> get_include_file_encoding(block)
    'utf-8'
    >>> assert block.include_file_encoding == 'utf-8'

    >>> # test encoding not set
    >>> block = lib_test.get_test_block_encoding_not_set()
    >>> get_include_file_encoding(block)
    'utf-8-sig'
    >>> assert block.include_file_encoding == 'utf-8-sig'

    >>> # test encoding invalid
    >>> block = lib_test.get_test_block_encoding_invalid()
    >>> get_include_file_encoding(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47102: option "encoding" has no value
    """

    encoding = block.include_file_encoding
    if lib_block_options.is_option_in_block('encoding', block):
        encoding = lib_block_options.get_option_value_from_block_or_raise_if_empty_or_invalid('encoding', block)
    block.include_file_encoding = encoding
    return encoding


def get_include_file_start_line(block: Block) -> Union[int, None]:
    """
    >>> block = lib_test.get_test_block_ok()
    >>> # test start-line set to 10
    >>> get_include_file_start_line(block)
    10
    >>> assert block.include_file_start_line == 10

    >>> # test start-line not set
    >>> block = lib_test.get_test_block_start_line_not_set()
    >>> get_include_file_start_line(block)

    >>> assert block.include_file_start_line is None

    >>> # test start-line invalid
    >>> block = lib_test.get_test_block_start_line_invalid()
    >>> get_include_file_start_line(block)      # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47103: option "start-line" has no value

    >>> # test start-line not integer
    >>> block = lib_test.get_test_block_start_line_not_integer()
    >>> get_include_file_start_line(block)      # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    TypeError: Error in File ".../README.template.rst", Line 47103: option "start-line" has to be integer

    """

    include_file_start_line = block.include_file_start_line
    if lib_block_options.is_option_in_block('start-line', block):
        include_file_start_line = int(lib_block_options.get_option_value_from_block_or_raise_if_empty_or_invalid('start-line', block, value_must_be_int=True))
    block.include_file_start_line = include_file_start_line
    return include_file_start_line


def get_include_file_end_line(block: Block) -> Union[int, None]:
    """
    >>> block = lib_test.get_test_block_ok()
    >>> # test end-line set to 25
    >>> get_include_file_end_line(block)
    25
    >>> assert block.include_file_end_line == 25

    >>> # test end-line not set
    >>> block = lib_test.get_test_block_end_line_not_set()
    >>> get_include_file_end_line(block)

    >>> assert block.include_file_end_line is None

    >>> # test end-line invalid
    >>> block = lib_test.get_test_block_end_line_invalid()
    >>> get_include_file_end_line(block)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47104: option "end-line" has no value

    >>> # test end-line not integer
    >>> block = lib_test.get_test_block_end_line_not_integer()
    >>> get_include_file_end_line(block)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    TypeError: Error in File ".../README.template.rst", Line 47104: option "end-line" has to be integer
    """

    include_file_end_line = block.include_file_end_line
    if lib_block_options.is_option_in_block('end-line', block):
        include_file_end_line = int(lib_block_options.get_option_value_from_block_or_raise_if_empty_or_invalid('end-line', block, value_must_be_int=True))
    block.include_file_end_line = include_file_end_line
    return include_file_end_line


def get_include_file_start_after(block: Block) -> str:
    """
    >>> block = lib_test.get_test_block_ok()

    >>> # test start-after set to 'start-marker'
    >>> get_include_file_start_after(block)
    '# start-marker'
    >>> assert block.include_file_start_after == '# start-marker'

    >>> # test start-after not_set
    >>> block = lib_test.get_test_block_start_after_not_set()
    >>> get_include_file_start_after(block)
    ''

    >>> # test start-after invalid
    >>> block = lib_test.get_test_block_start_after_invalid()
    >>> get_include_file_start_after(block)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47105: option "start-after" has no value

    """

    include_file_start_after = block.include_file_start_after
    if lib_block_options.is_option_in_block('start-after', block):
        include_file_start_after = lib_block_options.get_option_value_from_block_or_raise_if_empty_or_invalid('start-after', block)
    block.include_file_start_after = include_file_start_after
    return include_file_start_after


def get_include_file_end_before(block: Block) -> str:
    """
    >>> # test end-before set to 'end-marker'
    >>> block = lib_test.get_test_block_ok()
    >>> get_include_file_end_before(block)
    '# end-marker'
    >>> assert block.include_file_end_before == '# end-marker'

    >>> # test end-before not set
    >>> block = lib_test.get_test_block_end_before_not_set()
    >>> get_include_file_end_before(block)
    ''

    >>> # test end-before invalid
    >>> block = lib_test.get_test_block_end_before_invalid()
    >>> get_include_file_end_before(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47106: option "end-before" has no value
    """

    include_file_end_before = block.include_file_end_before
    if lib_block_options.is_option_in_block('end-before', block):
        include_file_end_before = lib_block_options.get_option_value_from_block_or_raise_if_empty_or_invalid('end-before', block)
    block.include_file_end_before = include_file_end_before
    return include_file_end_before


def get_blanks_to_add_to_content(block: Block) -> int:
    if block.pass_through_options:
        number_of_blanks_to_add_to_content = len(block.pass_through_options[0].content) - len(block.pass_through_options[0].content.lstrip())
    else:
        number_of_blanks_to_add_to_content = 4
    block.include_file_number_of_blanks_to_add_to_content = number_of_blanks_to_add_to_content
    return number_of_blanks_to_add_to_content
