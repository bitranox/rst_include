from typing import List

try:
    from rst_include.libs.lib_classes import Block
    from rst_include.libs.lib_classes import SourceLine
    from rst_include.libs import lib_classes
    from rst_include.libs import lib_list
    from rst_include.libs import lib_source_line
except ImportError:     # pragma: no cover
    from .lib_classes import Block
    from .lib_classes import SourceLine
    from . import lib_classes
    from . import lib_list
    from . import lib_source_line


def is_include_block(block: Block) -> bool:
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
    lines = lib_list.strip_list_of_strings(lines)
    content = '\n'.join(lines)
    return content
