# STDLIB
from typing import List

# OWN
import lib_list
import pathlib3x as pathlib

try:
    # for pytest
    from .lib_classes import Block
    from .lib_classes import SourceLine
    from . import lib_classes
    from . import lib_source_line
except ImportError:                             # pragma: no cover
    # for local doctest in pycharm
    from lib_classes import Block               # type: ignore # pragma: no cover
    from lib_classes import SourceLine          # type: ignore # pragma: no cover
    import lib_classes                          # type: ignore # pragma: no cover
    import lib_source_line                      # type: ignore # pragma: no cover


def is_include_block(block: Block) -> bool:
    """
    >>> source = pathlib.Path('some_source_file.txt')
    >>> block = lib_classes.Block(source=source)
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='something')
    >>> block.l_source_lines.append(source_line)
    >>> is_include_block(block)
    False

    >>> block = lib_classes.Block(source=source)
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='.. include::')
    >>> block.l_source_lines.append(source_line)
    >>> is_include_block(block)
    True

    >>> block = lib_classes.Block(source=source)
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='.. include:: some_file.txt')
    >>> block.l_source_lines.append(source_line)
    >>> is_include_block(block)
    True

    >>> # Test empty Block
    >>> block = lib_classes.Block(source=source)
    >>> is_include_block(block)
    False

    """
    if block.l_source_lines:
        if lib_source_line.source_line_starts_with_include_statement(block.l_source_lines[0]):
            return True
    return False


def get_block_source_lines_joined(l_source_lines: List[SourceLine]) -> str:
    """
    >>> l_source_lines = list()
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='aa')
    >>> l_source_lines.append(source_line)
    >>> source_line = lib_classes.SourceLine(line_number=4712, content='bb')
    >>> l_source_lines.append(source_line)
    >>> content = get_block_source_lines_joined(l_source_lines)
    >>> assert content == 'aa\\nbb'
    """
    lines = list()
    for source_line in l_source_lines:
        lines.append(source_line.content)
    lines = lib_list.ls_strip_list(lines)
    content = '\n'.join(lines)
    return content
