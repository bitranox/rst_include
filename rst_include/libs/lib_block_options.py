# OWN
import lib_log_utils

# PROJ
try:
    # for pytest
    from . import lib_classes
    from .lib_classes import Block, SourceLine
    from . import lib_source_line
    from . import lib_test
except ImportError:                                 # pragma: no cover
    # for local doctest in pycharm
    import lib_classes                              # type: ignore # pragma: no cover
    from lib_classes import Block, SourceLine       # type: ignore # pragma: no cover
    import lib_source_line                          # type: ignore # pragma: no cover
    import lib_test                                 # type: ignore # pragma: no cover


def get_option_value_from_block_or_raise_if_empty_or_invalid(option: str, block: Block, value_must_be_int: bool = False) -> str:

    """
    >>> block = lib_test.get_test_block_ok()
    >>> # test ok
    >>> get_option_value_from_block_or_raise_if_empty_or_invalid('code', block)
    'python'

    >>> # empty value
    >>> get_option_value_from_block_or_raise_if_empty_or_invalid('pass-through1', block)
    Traceback (most recent call last):
    ...
    ValueError: Error in File ".../README.template.rst", Line 47107: option "pass-through1" has no value

    >>> # option not found
    >>> get_option_value_from_block_or_raise_if_empty_or_invalid('no-option', block)
    Traceback (most recent call last):
    ...
    ValueError: Error in File: ".../README.template.rst", option "no-option" not found in block starting with Line: 47100

    >>> # option check type integer ok
    >>> get_option_value_from_block_or_raise_if_empty_or_invalid('start-line', block, value_must_be_int=True)
    '10'

    >>> # option check type not integer
    >>> get_option_value_from_block_or_raise_if_empty_or_invalid('start-after', block, value_must_be_int=True)
    Traceback (most recent call last):
    ...
    TypeError: Error in File ".../README.template.rst", Line 47105: option "start-after" has to be integer

    """
    log_and_raise_value_error_if_option_not_in_block(option, block)
    value = get_option_value_from_block(option, block)
    log_and_raise_if_value_of_option_in_block_is_empty(value, option, block)
    log_and_raise_if_value_of_option_in_block_must_be_int_castable_but_is_not(value, option, block, value_must_be_int)
    return value


def get_option_value_from_block(option: str, block: Block) -> str:
    """
    >>> block = lib_test.get_test_block_ok()
    >>> get_option_value_from_block('code', block)
    'python'
    >>> get_option_value_from_block('encoding', block)
    'utf-8'
    >>> get_option_value_from_block('no-option', block)
    Traceback (most recent call last):
    ...
    ValueError: Error in File: ".../README.template.rst", option "no-option" not found in block starting with Line: 47100

    """
    log_and_raise_value_error_if_option_not_in_block(option, block)
    option_value = ''
    for source_line in block.l_source_lines:                # pragma: no cover      # there will be always lines, otherwise value error would be raised
        if is_option_in_source_line(source_line, option):
            option_value = get_option_value_from_source_line(source_line)
            break
    return option_value


def get_option_value_from_source_line(source_line: SourceLine) -> str:
    option_value = source_line.content.split(':', 2)[2].strip()
    return option_value


def is_option_in_block(option: str, block: Block) -> bool:
    """
    >>> block = lib_test.get_test_block_ok()
    >>> is_option_in_block('code', block)
    True
    >>> is_option_in_block('no-option', block)
    False

    """
    for source_line in block.l_source_lines:
        if is_option_in_source_line(source_line, option):
            return True
        if not lib_source_line.source_line_contains_option(source_line):
            break
    return False


def get_source_line_number_for_option(option: str, block: Block) -> int:
    """
    >>> block = lib_test.get_test_block_ok()
    >>> get_source_line_number_for_option('code', block)
    47101
    >>> get_source_line_number_for_option('encoding', block)
    47102
    >>> get_source_line_number_for_option('no-option', block)
    Traceback (most recent call last):
      ...
    ValueError: Error in File: ".../README.template.rst", option "no-option" not found in block starting with Line: 47100
    """
    log_and_raise_value_error_if_option_not_in_block(option, block)
    line_number = 0
    for source_line in block.l_source_lines:                    # pragma: no cover    # there are always lines, otherwise Value Error is raised
        if is_option_in_source_line(source_line, option):
            line_number = source_line.line_number
            break
    return line_number


def is_option_in_source_line(source_line: SourceLine, option: str) -> bool:
    """
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='   :code:')
    >>> is_option_in_source_line(source_line, 'code')
    True
    >>> is_option_in_source_line(source_line, 'encoding')
    False

    """
    option_marked = ':' + option + ':'
    if source_line.content.strip().startswith(option_marked):
        return True
    else:
        return False


def get_option_key_from_source_line(source_line: SourceLine) -> str:
    """
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='   :code:')
    >>> get_option_key_from_source_line(source_line)
    'code'
    """
    key = source_line.content.split(':')[1]
    return key


def log_and_raise_value_error_if_option_not_in_block(option: str, block: Block) -> None:
    if not is_option_in_block(option, block):
        s_error = 'Error in File: "{file}", option "{option}" not found in block starting with Line: {line}'.format(
            file=block.source,
            option=option,
            line=block.l_source_lines[0].line_number)
        lib_log_utils.log_error(s_error)
        raise ValueError(s_error)


def log_and_raise_if_value_of_option_in_block_is_empty(value: str, option: str, block: Block) -> None:
    if not value:
        line_number = get_source_line_number_for_option(option, block)
        s_error = 'Error in File "{source_file}", Line {line_number}: option "{option}" has no value'.format(
            source_file=block.source,
            line_number=line_number,
            option=option)
        lib_log_utils.log_error(s_error)
        raise ValueError(s_error)


def log_and_raise_if_value_of_option_in_block_must_be_int_castable_but_is_not(value: str, option: str, block: Block, value_must_be_int: bool) -> None:
    if value_must_be_int and not value.isdigit():
        line_number = get_source_line_number_for_option(option, block)
        s_error = 'Error in File "{source_file}", Line {line_number}: option "{option}" has to be integer'.format(
            source_file=block.source,
            line_number=line_number,
            option=option)
        lib_log_utils.log_error(s_error)
        raise TypeError(s_error)
