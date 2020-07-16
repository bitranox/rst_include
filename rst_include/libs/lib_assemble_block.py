# STDLIB
from typing import List, IO, Union

# OWN
import lib_list
import pathlib3x as pathlib


try:
    # for pytest
    from . import lib_classes
    from .lib_classes import Block
    from .lib_classes import RstFile
    from .lib_classes import SourceLine
    from . import lib_block
    from . import lib_check_files
    from . import lib_get_include_options
    from . import lib_include_file
    from . import lib_source_line
    from . import lib_str
    from . import lib_test
    from . import lib_test_compare_results
except ImportError:                             # pragma: no cover
    # for local doctest in pycharm
    import lib_classes                          # type: ignore # pragma: no cover
    from lib_classes import Block               # type: ignore # pragma: no cover
    from lib_classes import RstFile             # type: ignore # pragma: no cover
    from lib_classes import SourceLine          # type: ignore # pragma: no cover
    import lib_block                            # type: ignore # pragma: no cover
    import lib_check_files                      # type: ignore # pragma: no cover
    import lib_get_include_options              # type: ignore # pragma: no cover
    import lib_include_file                     # type: ignore # pragma: no cover
    import lib_source_line                      # type: ignore # pragma: no cover
    import lib_str                              # type: ignore # pragma: no cover
    import lib_test                             # type: ignore # pragma: no cover
    import lib_test_compare_results             # type: ignore # pragma: no cover


def create_l_rst_files_from_templates(l_rst_files: List[RstFile]) -> None:
    """
    >>> # Setup
    >>> path_test_dir = pathlib.Path(__file__).parent.parent.parent / 'tests'
    >>> path_source_file = path_test_dir / 'test1_no_includes_template.rst'
    >>> path_target_file = path_test_dir / 'test1_no_includes_result.rst'
    >>> path_expected_file = path_test_dir / 'test1_no_includes_expected.rst'

    >>> # test
    >>> l_rst_files = [lib_classes.RstFile(path_source_file, path_target_file)]
    >>> create_l_rst_files_from_templates(l_rst_files)
    >>> assert lib_test_compare_results.compare_results_equal(path_expected_file, path_target_file)

    >>> # Teardown
    >>> path_target_file.unlink()


    """
    for rst_file in l_rst_files:
        create_rst_file_from_template(rst_file)


def create_rst_file_from_template(rst_file: RstFile) -> str:
    l_source_lines = lib_check_files.read_source_lines(rst_file.source, rst_file.source_encoding)
    content = process_source_lines(path_source_file=rst_file.source, source_lines=l_source_lines)
    lib_check_files.write_output(rst_file.target, content, rst_file.target_encoding)
    return content


def process_source_lines(path_source_file: Union[str, pathlib.Path, IO[str]], source_lines: List[SourceLine]) -> str:
    l_blocks = lib_source_line.divide_source_line_in_blocks(path_source_file=path_source_file, source_lines=source_lines)
    content = assemble_blocks(l_blocks)
    content = '\n\n'.join((content, ''))
    return content


def assemble_blocks(l_blocks: List[Block]) -> str:
    content = ''
    for block in l_blocks:
        if lib_block.is_include_block(block):
            str_include_block = create_content_from_include(block)
            content = lib_str.join_if_not_empty('\n\n', content, str_include_block)
        else:
            str_standard_block = lib_block.get_block_source_lines_joined(block.l_source_lines)
            content = lib_str.join_if_not_empty('\n\n', content, str_standard_block)
        # save memory
        del block.l_source_lines
    return content


def create_content_from_include(block: Block) -> str:
    lib_get_include_options.get_include_options(block)
    lib_include_file.read_include_file(block)
    lib_include_file.process_include_file_lines(block)
    str_include_block = assemble_include_block(block)
    str_additional_content = assemble_additional_content(block)
    str_include = lib_str.join_if_not_empty('\n\n', str_include_block, str_additional_content)
    return str_include


def assemble_additional_content(block: Block) -> str:
    """
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> assemble_additional_content(block)
    '    :no-option:\\n\\nadditional content1...\\nadditional content5'

    """
    l_content = [source_line.content.rstrip() for source_line in block.additional_content]
    l_content = lib_list.ls_strip_list(l_content)
    content = '\n'.join(l_content)
    # save memory
    del block.additional_content
    return content


def assemble_include_block(block: Block) -> str:
    """
    >>> # test :code: python
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> include_file = lib_include_file.read_include_file(block)
    >>> lib_include_file.process_include_file_lines(block)
    >>> assemble_include_block(block)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.. code-block:: python\\n    :pass-through1:...        pass'

    >>> # test :code: ''
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> include_file = lib_include_file.read_include_file(block)
    >>> block.include_file_code = ''
    >>> lib_include_file.process_include_file_lines(block)
    >>> assemble_include_block(block)
    'def my_include2_2() -> None:\\n    pass\\n\\n    pass'
    """
    block_header = get_block_header(block)
    intended_include_lines_content = get_intended_include_lines_content(block)
    content = lib_str.join_if_not_empty('\n\n', block_header, intended_include_lines_content)
    return content


def get_block_header(block: Block) -> str:
    """
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> include_file = lib_include_file.read_include_file(block)
    >>> lib_include_file.process_include_file_lines(block)

    >>> # test :code: python
    >>> get_block_header(block)
    '.. code-block:: python\\n    :pass-through1:\\n    :pass-through2: value2'

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
        content = '\n'.join(content_lines)
    return content


def set_number_of_blanks_to_add(block: Block) -> int:
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


def get_intended_include_lines_content(block: Block) -> str:
    """
    >>> # test :code: python
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> include_file = lib_include_file.read_include_file(block)
    >>> lib_include_file.process_include_file_lines(block)
    >>> number_of_blanks_to_add = set_number_of_blanks_to_add(block)
    >>> get_intended_include_lines_content(block)
    '    def my_include2_2() -> None:\\n        pass\\n\\n        pass'

    >>> # test :code: ''
    >>> block = lib_test.get_test_block_include2_ok()
    >>> lib_get_include_options.get_include_options(block)
    >>> include_file = lib_include_file.read_include_file(block)
    >>> lib_include_file.process_include_file_lines(block)
    >>> block.include_file_code = ''
    >>> number_of_blanks_to_add = set_number_of_blanks_to_add(block)
    >>> get_intended_include_lines_content(block)
    'def my_include2_2() -> None:\\n    pass\\n\\n    pass'

    """
    set_number_of_blanks_to_add(block)
    if block.include_file_number_of_blanks_to_add_to_content:
        content = add_indention_to_include_file_content(block)
    else:
        content = block.include_file_sliced_content
    # save memory
    del block.include_file_sliced_content
    return content


def add_indention_to_include_file_content(block: Block) -> str:
    """
    >>> block=Block(source='some_file')
    >>> block.include_file_number_of_blanks_to_add_to_content = 4
    >>> block.include_file_sliced_content = 'abc\\n\\ndef'
    >>> add_indention_to_include_file_content(block)
    '    abc\\n\\n    def'
    """
    blanks_to_add = ' ' * block.include_file_number_of_blanks_to_add_to_content
    l_sliced_content = block.include_file_sliced_content.split('\n')
    l_sliced_content = [''.join((blanks_to_add, line)).rstrip() for line in l_sliced_content]
    content = '\n'.join(l_sliced_content)
    return content
