import logging
from typing import List, Tuple
logger = logging.getLogger('compare_results')

try:
    # for pytest
    from . import lib_test
except ImportError:                             # type: ignore # pragma: no cover
    # for local doctest in pycharm
    from rst_include.libs import lib_test       # type: ignore # pragma: no cover


def compare_results_equal(expected_file: str, result_file: str,
                          file_expected_encoding: str = 'utf-8-sig', file_result_encoding: str = 'utf-8-sig') -> bool:
    """
    >>> test_dir = lib_test.get_test_dir()
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

    is_files_equal = True
    l_expected_lines, l_result_lines = read_files_into_lines(expected_file, result_file, file_expected_encoding, file_result_encoding)
    len_expected_lines = len(l_expected_lines)
    len_result_lines = len(l_result_lines)
    if len_expected_lines != len_result_lines:
        is_files_equal = False
        log_file_lengths_not_equal(expected_file, result_file, len_expected_lines, len_result_lines)

    min_lines = min(len_expected_lines, len_result_lines)
    for line_number in range(min_lines):
        expected_line = l_expected_lines[line_number]
        result_line = l_result_lines[line_number]
        if expected_line != result_line:
            is_files_equal = False
            log_difference_expected_line(expected_file, line_number, expected_line)
            log_difference_result_line(result_file, line_number, result_line)

    return is_files_equal


def read_files_into_lines(expected_file: str,
                          result_file: str,
                          expected_file_encoding: str = 'utf-8-sig',
                          result_file_encoding: str = 'utf-8-sig') -> Tuple[List[str], List[str]]:

    with open(expected_file, mode='r', encoding=expected_file_encoding) as f_expected_file:
        l_expected_lines = f_expected_file.readlines()

    with open(result_file, mode='r', encoding=result_file_encoding) as f_result_file:
        l_result_lines = f_result_file.readlines()

    return l_expected_lines, l_result_lines


def log_file_lengths_not_equal(expected_file: str, result_file: str, len_expected_lines: int, len_result_lines: int) -> None:
    logger.error('Different Size, Expected File {expected_file}: {len_expected_lines} Lines, Result File {result_file}: {len_result_lines} Lines'.format(
        expected_file=expected_file,
        len_expected_lines=len_expected_lines,
        result_file=result_file,
        len_result_lines=len_result_lines))


def log_difference_expected_line(expected_file: str, line_number: int, expected_line: str) -> None:
    logger.error('Difference, Expected File {expected_file}, Line {line_number}: "{expected_line}"'.format(
        expected_file=expected_file,
        line_number=line_number,
        expected_line=expected_line.replace('\n', '<ret>')))


def log_difference_result_line(result_file: str, line_number: int, result_line: str) -> None:
    logger.error('Difference, Result   File {result_file}, Line {line_number}: "{result_line}"'.format(
        result_file=result_file,
        line_number=line_number,
        result_line=result_line.replace('\n', '<ret>')))
