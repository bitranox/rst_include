# -*- coding: utf-8 -*-

try:
    from . import lib_classes
    from . import lib_block
    from . import lib_check_files
    from . import lib_get_include_options
    from . import lib_include_file
    from . import lib_path
    from . import lib_source_line
    from . import lib_test
except ImportError:
    # this we need for local doctest
    import lib_classes
    import lib_block
    import lib_check_files
    import lib_get_include_options
    import lib_include_file
    import lib_path
    import lib_source_line
    import lib_test


def create_l_rst_files_from_templates(l_rst_files):
    # type: ([lib_classes.RstFile]) -> None
    """
    >>> # test files without include
    >>> test_dir = lib_test.get_test_dir()
    >>> source = test_dir + '/test1_no_includes_template.rst'
    >>> target = test_dir + '/test1_no_includes_result.rst'
    >>> expected = test_dir + '/test1_no_includes_expected.rst'
    >>> l_rst_files = [lib_classes.RstFile(source, target)]
    >>> create_l_rst_files_from_templates(l_rst_files)
    >>> assert lib_test.compare_results_equal(expected, target)

    """
    for rst_file in l_rst_files:
        create_rst_file_from_template(rst_file)


def create_rst_file_from_template(rst_file):
    # type: (lib_classes.RstFile) -> None
    l_source_lines = lib_check_files.read_source_lines(rst_file.source, rst_file.source_encoding)
    l_blocks = lib_source_line.divide_source_line_in_blocks(rst_file.source, source_lines=l_source_lines)
    content = assemble_blocks(l_blocks)
    lib_check_files.write_output(rst_file.target, content, rst_file.target_encoding)


def assemble_blocks(l_blocks):
    # type: ([lib_classes.Block]) -> str
    content = ''
    for block in l_blocks:
        if lib_block.is_include_block(block):
            content += create_content_from_include(block)
        else:
            content += lib_block.get_block_source_lines_joined(block.l_source_lines)
            # save memory
            del block.l_source_lines
    return content


def create_content_from_include(block):
    # type: (lib_classes.Block) -> str
    lib_get_include_options.get_include_options(block)
    lib_include_file.read_include_file(block)
    lib_include_file.process_include_file_lines(block)
    content = assemble_include_block(block)
    content += assemble_additional_content(block)
    return content


def assemble_additional_content(block):
    # type: (lib_classes.Block) -> str
    """
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> assemble_additional_content(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '\\n    :no-option:\\nadditional content1...additional content5\\n\\n'

    """
    delete_leading_empty_additional_content_lines(block)
    delete_trailing_empty_additional_content_lines(block)
    content = ''
    l_content = [source_line.content.rstrip() for source_line in block.additional_content]
    if l_content:
        content = '\n' + '\n'.join(l_content) + '\n\n'
    # save memory
    del block.additional_content
    return content


def delete_leading_empty_additional_content_lines(block):
    while len(block.additional_content) and not block.additional_content[0].content.strip():
        block.additional_content = block.additional_content[1:]


def delete_trailing_empty_additional_content_lines(block):
    while len(block.additional_content) and not block.additional_content[-1].content.strip():
        block.additional_content = block.additional_content[0:-1]


def assemble_include_block(block):
    # type: (lib_classes.Block) -> str
    """
    >>> # test :code: python
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> include_file = lib_include_file.read_include_file(block)
    >>> lib_include_file.process_include_file_lines(block)
    >>> assemble_include_block(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.. code-block:: python\\n    :pass-through1:...        pass\\n\\n'

    >>> # test :code: ''
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> include_file = lib_include_file.read_include_file(block)
    >>> block.include_file_code = ''
    >>> lib_include_file.process_include_file_lines(block)
    >>> assemble_include_block(block)
    '\\ndef my_include2_2():\\n    pass\\n\\n    pass\\n'

    """
    content = get_block_header(block) + '\n'
    set_number_of_blanks_to_add(block)
    content = content + get_include_lines_content(block) + '\n'
    return content


def get_block_header(block):
    # type: (lib_classes.Block) -> str
    """
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> include_file = lib_include_file.read_include_file(block)
    >>> lib_include_file.process_include_file_lines(block)

    >>> # test :code: python
    >>> get_block_header(block)
    '.. code-block:: python\\n    :pass-through1:\\n    :pass-through2: value2\\n'

    >>> # test :code: ''
    >>> block.include_file_code = ''
    >>> get_block_header(block)
    ''
    """
    content = ''
    if block.include_file_code:
        content_lines = list()
        content_lines.append('.. code-block:: {code}'.format(code=block.include_file_code))
        content_lines = content_lines + [pass_through_option.content for pass_through_option in block.pass_through_options]
        content = '\n'.join(content_lines) + '\n'
    return content


def set_number_of_blanks_to_add(block):
    # type: (lib_classes.Block) -> int
    """
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> include_file = lib_include_file.read_include_file(block)
    >>> lib_include_file.process_include_file_lines(block)

    >>> # test :code: python
    >>> set_number_of_blanks_to_add(block)
    4

    >>> # test :code: ''
    >>> block.include_file_code = ''
    >>> set_number_of_blanks_to_add(block)
    0

    """
    # if there is no :code: given. we import the file as it is
    if not block.include_file_code:
        block.include_file_number_of_blanks_to_add_to_content = 0
    return block.include_file_number_of_blanks_to_add_to_content


def get_include_lines_content(block):
    # type: (lib_classes.Block) -> str
    """
    >>> # test :code: python
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> include_file = lib_include_file.read_include_file(block)
    >>> lib_include_file.process_include_file_lines(block)
    >>> number_of_blanks_to_add = set_number_of_blanks_to_add(block)
    >>> get_include_lines_content(block)
    '    def my_include2_2():\\n        pass\\n\\n        pass\\n'

    >>> # test :code: ''
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> include_file = lib_include_file.read_include_file(block)
    >>> lib_include_file.process_include_file_lines(block)
    >>> block.include_file_code = ''
    >>> number_of_blanks_to_add = set_number_of_blanks_to_add(block)
    >>> get_include_lines_content(block)
    'def my_include2_2():\\n    pass\\n\\n    pass'

    """
    if block.include_file_number_of_blanks_to_add_to_content:
        blanks_to_add = ' ' * block.include_file_number_of_blanks_to_add_to_content
        l_sliced_content = block.include_file_sliced_content.split('\n')
        # save memory
        del block.include_file_sliced_content

        l_content_blanks_added = list()
        for content_line in l_sliced_content:
            if content_line.strip():
                content_line = blanks_to_add + content_line.rstrip() + '\n'
            else:
                content_line = '\n'
            l_content_blanks_added.append(content_line)
        content = ''.join(l_content_blanks_added)
    else:
        content = block.include_file_sliced_content
        # save memory
        del block.include_file_sliced_content
    return content
