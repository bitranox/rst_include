from rst_include.libs import lib_classes
from rst_include.libs.lib_classes import Block, SourceLine

from rst_include.libs import lib_get_include_options
from rst_include.libs import lib_include_file
from rst_include.libs import lib_path
from rst_include.libs import lib_assemble_block

import logging
import os


def run_template_tests() -> None:
    l_sources = [get_test_dir() + '/test1_no_includes_template.rst',
                 get_test_dir() + '/test2_include_samedir_template.rst',
                 get_test_dir() + '/test3_include_subdir_template.rst',
                 get_test_dir() + '/test4_include_nocode_template.rst']

    for source in l_sources:
        result = source.replace('template', 'result')
        expected = source.replace('template', 'expected')
        rst_file = lib_classes.RstFile(source=source, target=result)
        lib_assemble_block.create_rst_file_from_template(rst_file)
        assert compare_results_equal(expected=expected, result=result)


def run_template_tests_not_supported() -> None:
    l_sources = [get_test_dir() + '/test5_not_supported_template.rst']

    for source in l_sources:
        result = source.replace('template', 'result')
        expected = source.replace('template', 'expected')
        rst_file = lib_classes.RstFile(source=source, target=result)
        lib_assemble_block.create_rst_file_from_template(rst_file)
        assert not compare_results_equal(expected=expected, result=result)


def compare_results_equal(expected: str, result: str,
                          expected_file_encoding: str = 'utf-8-sig', result_file_encoding: str = 'utf-8-sig'):
    """
    >>> test_dir = get_test_dir()
    >>> expected_file = test_dir + '/test_compare_file_original.txt'
    >>> compare_results_equal(expected_file, test_dir + '/test_compare_file_result_equal.txt')
    True
    >>> compare_results_equal(expected_file, test_dir + '/test_compare_file_result_different.txt')
    False
    >>> compare_results_equal(expected_file, test_dir + '/test_compare_file_result_longer.txt')
    False
    >>> compare_results_equal(expected_file, test_dir + '/test_compare_file_result_shorter.txt')
    False

    """

    logger = logging.getLogger('compare_results')

    with open(expected, mode='r', encoding=expected_file_encoding) as f_expected_file:
        l_expected_lines = f_expected_file.readlines()

    with open(result, mode='r', encoding=result_file_encoding) as f_result_file:
        l_result_lines = f_result_file.readlines()

    len_expected_lines = len(l_expected_lines)
    len_result_lines = len(l_result_lines)

    min_lines = min(len_expected_lines, len_result_lines)

    if len_expected_lines != len_result_lines:
        logger.error('Different Size, Expected File {expected_file}: {len_expected_lines} Lines, Result File {result_file}: {len_result_lines} Lines'.format(
            expected_file=expected,
            len_expected_lines=len_expected_lines,
            result_file=result,
            len_result_lines=len_result_lines))

    for index in range(min_lines):
        if l_expected_lines[index] != l_result_lines[index]:
            logger.error('Difference, Expected File {expected_file}, Line {index}: "{original_line}"'.format(
                expected_file=expected,
                index=index,
                original_line=l_expected_lines[index].replace('\n', '<ret>')))

            logger.error('Difference, Result   File {result_file}, Line {index}: "{result_line}"'.format(
                result_file=result,
                index=index,
                result_line=l_result_lines[index].replace('\n', '<ret>')))

            return False

    if len_expected_lines != len_result_lines:
        return False
    else:
        return True


def read_include_file_2() -> Block:
    block = get_test_block_include2_ok()
    lib_get_include_options.get_include_options(block)
    lib_include_file.read_include_file(block)
    return block


def get_test_block_ok() -> Block:
    source_file_name = get_test_dir() + '/README.template.rst'
    block = Block(source_file_name)
    block.l_source_lines = [
        SourceLine(line_number=47100, content='.. include:: include1.py'),
        SourceLine(line_number=47101, content='    :code: python'),
        SourceLine(line_number=47102, content='    :encoding: utf-8'),
        SourceLine(line_number=47103, content='    :start-line: 10'),
        SourceLine(line_number=47104, content='    :end-line: 25'),
        SourceLine(line_number=47105, content='    :start-after: # start-marker'),
        SourceLine(line_number=47106, content='    :end-before: # end-marker'),
        SourceLine(line_number=47107, content='    :pass-through1:'),
        SourceLine(line_number=47108, content='    :pass-through2: value2'),
        SourceLine(line_number=47209, content='    '),
        SourceLine(line_number=47210, content=''),
        SourceLine(line_number=47211, content='    :no-option:'),
        SourceLine(line_number=47212, content=''),
        SourceLine(line_number=47213, content='additional content1'),
        SourceLine(line_number=47214, content='additional content2'),
        SourceLine(line_number=47215, content='additional content3'),
        SourceLine(line_number=47216, content='additional content4'),
        SourceLine(line_number=47217, content='additional content5'),
        SourceLine(line_number=47218, content='')
    ]
    return block


def get_test_block_include2_ok() -> Block:
    block = get_test_block_ok()
    block.l_source_lines[0].content = '.. include:: include2.py'
    block.l_source_lines[3].content = '    :start-line: 6'
    block.l_source_lines[4].content = '    :end-line: 25'
    return block


def get_test_block_no_include_filename() -> Block:
    block = get_test_block_ok()
    block.l_source_lines[0].content = '.. include:: '
    return block


def get_test_block_include_filename_not_existing() -> Block:
    block = get_test_block_ok()
    block.l_source_lines[0].content = '.. include:: not_existing.file'
    return block


def get_test_block_code_not_set() -> Block:
    block = get_test_block_ok()
    block.l_source_lines.pop(1)
    return block


def get_test_block_code_invalid() -> Block:
    block = get_test_block_ok()
    block.l_source_lines[1].content = '    :code: '
    return block


def get_test_block_encoding_not_set() -> Block:
    block = get_test_block_ok()
    block.l_source_lines.pop(2)
    return block


def get_test_block_encoding_invalid() -> Block:
    block = get_test_block_ok()
    block.l_source_lines[2].content = '    :encoding: '
    return block


def get_test_block_start_line_not_set() -> Block:
    block = get_test_block_ok()
    block.l_source_lines.pop(3)
    return block


def get_test_block_start_line_invalid() -> Block:
    block = get_test_block_ok()
    block.l_source_lines[3].content = '    :start-line: '
    return block


def get_test_block_start_line_not_integer() -> Block:
    block = get_test_block_ok()
    block.l_source_lines[3].content = '    :start-line: not_integer'
    return block


def get_test_block_end_line_not_set() -> Block:
    block = get_test_block_ok()
    block.l_source_lines.pop(4)
    return block


def get_test_block_end_line_invalid() -> Block:
    block = get_test_block_ok()
    block.l_source_lines[4].content = '    :end-line: '
    return block


def get_test_block_end_line_not_integer() -> Block:
    block = get_test_block_ok()
    block.l_source_lines[4].content = '    :end-line: not_integer'
    return block


def get_test_block_start_after_not_set() -> Block:
    block = get_test_block_ok()
    block.l_source_lines.pop(5)
    return block


def get_test_block_start_after_invalid() -> Block:
    block = get_test_block_ok()
    block.l_source_lines[5].content = '    :start-after: '
    return block


def get_test_block_end_before_not_set() -> Block:
    block = get_test_block_ok()
    block.l_source_lines.pop(6)
    return block


def get_test_block_end_before_invalid() -> Block:
    block = get_test_block_ok()
    block.l_source_lines[6].content = '    :end-before: '
    return block


def get_test_dir() -> str:
    """
    >>> test_dir = get_test_dir()
    >>> assert test_dir.split('rst_include')[-1] == '/tests'

    """
    test_dir = get_rst_include_dir() + '/rst_include/tests'
    return test_dir


def get_rst_include_dir() -> str:
    rst_include_dir = lib_path.get_current_dir().split('rst_include', 1)[0]
    rst_include_dir = os.path.join(rst_include_dir, 'rst_include')
    rst_include_dir = lib_path.strip_and_replace_backslashes(rst_include_dir)
    return rst_include_dir


def import_test() -> bool:
    """
    >>> import_test()
    True
    """
    return True


def remove_file_silent(path: str) -> None:
    if os.path.isfile(path):
        os.remove(path)
