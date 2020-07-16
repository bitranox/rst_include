# STDLIB
from typing import List, Union, IO

# OWN
import pathlib3x as pathlib

# PROJ
try:
    # for pytest
    from . import lib_classes
    from .lib_classes import Block, SourceLine
except ImportError:                                 # pragma: no cover
    # for local doctest in pycharm
    import lib_classes                              # type: ignore # pragma: no cover
    from lib_classes import Block, SourceLine       # type: ignore # pragma: no cover


def divide_source_line_in_blocks(path_source_file: Union[str, pathlib.Path, IO[str]], source_lines: List[SourceLine]) -> List[Block]:
    """
    return blocks  - each block starts with ".." and ends with a line that does not begin with tab or blank
    or begins with .. (another block)
    trailing blank lines are part of the block

    >>> path_source_file = pathlib.Path('some_source_file')
    >>> divide_source_line_in_blocks(path_source_file, source_lines=[])
    []

    >>> # test ['a']
    >>> source_lines = list()
    >>> source_lines.append(lib_classes.SourceLine(line_number=4711, content='This is a test'))
    >>> source_lines.append(lib_classes.SourceLine(line_number=4712, content='a new block will only occur'))
    >>> source_lines.append(lib_classes.SourceLine(line_number=4713, content='on .. include:: some_file.txt:'))
    >>> source_lines.append(lib_classes.SourceLine(line_number=4714, content='.. include:: some_file.py'))
    >>> source_lines.append(lib_classes.SourceLine(line_number=4715, content='    :code: python'))
    >>> source_lines.append(lib_classes.SourceLine(line_number=4716, content='.. include:: some_file.yaml'))
    >>> source_lines.append(lib_classes.SourceLine(line_number=4717, content='    :code: yaml'))
    >>> blocks = divide_source_line_in_blocks(path_source_file, source_lines)
    >>> assert blocks[0].source == path_source_file
    >>> assert blocks[0].l_source_lines[0].line_number == 4711
    >>> assert blocks[0].l_source_lines[0].content == 'This is a test'
    >>> assert blocks[0].l_source_lines[1].line_number == 4712
    >>> assert blocks[0].l_source_lines[1].content == 'a new block will only occur'
    >>> assert blocks[1].source == path_source_file
    >>> assert blocks[1].l_source_lines[0].line_number == 4714
    >>> assert blocks[1].l_source_lines[0].content == '.. include:: some_file.py'
    >>> assert blocks[1].l_source_lines[1].line_number == 4715
    >>> assert blocks[1].l_source_lines[1].content == '    :code: python'
    >>> assert blocks[2].l_source_lines[0].line_number == 4716
    >>> assert blocks[2].l_source_lines[0].content == '.. include:: some_file.yaml'
    >>> assert blocks[2].l_source_lines[1].line_number == 4717
    >>> assert blocks[2].l_source_lines[1].content == '    :code: yaml'

    """
    blocks = list()                               # type: List[Block]
    block = lib_classes.Block(path_source_file)   # type: Block
    for source_line in source_lines:
        if source_line_starts_with_include_statement(source_line):
            append_non_empty_block(block, blocks)
            block = lib_classes.Block(path_source_file)
        block.l_source_lines.append(source_line)
    append_non_empty_block(block, blocks)
    return blocks


def append_non_empty_block(block: Block, blocks: List[Block]) -> None:
    if block.l_source_lines:
        blocks.append(block)


def source_line_starts_with_include_statement(source_line: SourceLine) -> bool:
    """
    >>> source_line_starts_with_include_statement(lib_classes.SourceLine(line_number=4711, content='.. some comment or other block\\n'))
    False
    >>> source_line_starts_with_include_statement(lib_classes.SourceLine(line_number=4711, content='.. include:: test_include.py\\n'))
    True
    """

    if source_line.content.startswith('.. include::'):
        return True
    else:
        return False


def source_line_contains_option(source_line: SourceLine) -> bool:
    """
    >>> # TEST
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='  :code: python ')
    >>> source_line_contains_option(source_line)
    True

    >>> source_line = lib_classes.SourceLine(line_number=4711, content='  :line-numbers:')
    >>> source_line_contains_option(source_line)
    True

    >>> source_line = lib_classes.SourceLine(line_number=4711, content='.. include::')
    >>> source_line_contains_option(source_line)
    True
    >>> source_line = lib_classes.SourceLine(line_number=4711, content=' :not an option:')
    >>> source_line_contains_option(source_line)
    False
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='')
    >>> source_line_contains_option(source_line)
    False
    >>> source_line = lib_classes.SourceLine(line_number=4711, content=' :not an option')
    >>> source_line_contains_option(source_line)
    False

    """
    line = source_line.content.strip()
    if not line:
        return False
    if line.count(':') < 2:
        return False
    option = line.split(':')[1]
    if ' ' in option:
        return False
    return True
