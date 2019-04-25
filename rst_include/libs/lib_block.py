# -*- coding: utf-8 -*-

try:
    from . import lib_classes
    from .lib_classes import Block
    from .lib_classes import SourceLine
    from . import lib_source_line
except ImportError:
    # this we need for local doctest
    import lib_classes
    from lib_classes import Block
    from lib_classes import SourceLine
    import lib_source_line


def is_include_block(block):
    # type: (Block) -> bool
    """
    >>> block = lib_classes.Block(source_file_name='some_source_file.txt')
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='something')
    >>> block.l_source_lines.append(source_line)
    >>> is_include_block(block)
    False

    >>> block = lib_classes.Block(source_file_name='some_source_file.txt')
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='.. include::')
    >>> block.l_source_lines.append(source_line)
    >>> is_include_block(block)
    True

    >>> block = lib_classes.Block(source_file_name='some_source_file.txt')
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='.. include:: some_file.txt')
    >>> block.l_source_lines.append(source_line)
    >>> is_include_block(block)
    True

    """
    if block.l_source_lines:
        if lib_source_line.is_source_line_include_block_start(block.l_source_lines[0]):
            return True
    return False


def get_block_source_lines_joined(l_source_lines):
    # type: ([SourceLine]) -> str
    """
    >>> l_source_lines = list()
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='aa\\n')
    >>> l_source_lines.append(source_line)
    >>> source_line = lib_classes.SourceLine(line_number=4712, content='bb\\n')
    >>> l_source_lines.append(source_line)
    >>> content = get_block_source_lines_joined(l_source_lines)
    >>> assert content == 'aa\\nbb\\n'
    """
    lines = list()
    for source_line in l_source_lines:
        lines.append(source_line.content)
    content = ''.join(lines)
    return content
