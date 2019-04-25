try:
    from . import lib_classes
except ImportError:
    # this we need for local doctest
    import lib_classes


def divide_source_line_in_blocks(source_file_name, source_lines):
    # type: (str, [lib_classes.SourceLine]) -> [lib_classes.Block]
    """
    return blocks  - each block starts with ".." and ends with a line that does not begin with tab or blank
    or begins with .. (another block)
    trailing blank lines are part of the block

    >>> source_file_name = 'some_source_file'
    >>> divide_source_line_in_blocks(source_file_name, source_lines=[])
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
    >>> blocks = divide_source_line_in_blocks(source_file_name, source_lines)
    >>> assert blocks[0].source_file_name == 'some_source_file'
    >>> assert blocks[0].l_source_lines[0].line_number == 4711
    >>> assert blocks[0].l_source_lines[0].content == 'This is a test'
    >>> assert blocks[0].l_source_lines[1].line_number == 4712
    >>> assert blocks[0].l_source_lines[1].content == 'a new block will only occur'
    >>> assert blocks[1].source_file_name == 'some_source_file'
    >>> assert blocks[1].l_source_lines[0].line_number == 4714
    >>> assert blocks[1].l_source_lines[0].content == '.. include:: some_file.py'
    >>> assert blocks[1].l_source_lines[1].line_number == 4715
    >>> assert blocks[1].l_source_lines[1].content == '    :code: python'
    >>> assert blocks[2].l_source_lines[0].line_number == 4716
    >>> assert blocks[2].l_source_lines[0].content == '.. include:: some_file.yaml'
    >>> assert blocks[2].l_source_lines[1].line_number == 4717
    >>> assert blocks[2].l_source_lines[1].content == '    :code: yaml'

    """
    blocks = list()                   # type: [lib_classes.Block]
    block = lib_classes.Block(source_file_name)   # type: lib_classes.Block
    for source_line in source_lines:
        if is_source_line_include_block_start(source_line):
            if block.l_source_lines:
                blocks.append(block)
            block = lib_classes.Block(source_file_name)
        block.l_source_lines.append(source_line)
    if block.l_source_lines:
        blocks.append(block)
    return blocks


def is_source_line_include_block_start(source_line):
    # type: (lib_classes.SourceLine) -> bool
    """
    >>> is_source_line_include_block_start(lib_classes.SourceLine(line_number=4711, content='.. some comment or other block\\n'))
    False
    >>> is_source_line_include_block_start(lib_classes.SourceLine(line_number=4711, content='.. include:: test_include.py\\n'))
    True
    """

    if source_line.content.startswith('.. include::'):
        return True
    else:
        return False


def is_source_line_block_option(source_line):
    # type: (lib_classes.SourceLine) -> bool
    """
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='  :code: python ')
    >>> is_source_line_block_option(source_line)
    True

    >>> source_line = lib_classes.SourceLine(line_number=4711, content='  :line-numbers:')
    >>> is_source_line_block_option(source_line)
    True

    >>> source_line = lib_classes.SourceLine(line_number=4711, content='.. include::')
    >>> is_source_line_block_option(source_line)
    True
    >>> source_line = lib_classes.SourceLine(line_number=4711, content=' :not an option:')
    >>> is_source_line_block_option(source_line)
    False
    >>> source_line = lib_classes.SourceLine(line_number=4711, content='')
    >>> is_source_line_block_option(source_line)
    False
    >>> source_line = lib_classes.SourceLine(line_number=4711, content=' :not an option')
    >>> is_source_line_block_option(source_line)
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
