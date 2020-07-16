# STDLIB
from typing import List, Tuple

# OWN
import lib_log_utils
import pathlib3x as pathlib


# PROJECT
try:
    # for pytest
    from . import lib_test
except ImportError:                     # pragma: no cover
    # for local doctest in pycharm
    import lib_test                     # type: ignore # pragma: no cover


def compare_results_equal(expected_file: pathlib.Path, result_file: pathlib.Path,
                          file_expected_encoding: str = 'utf-8-sig', file_result_encoding: str = 'utf-8-sig') -> bool:
    """
    >>> # Setup test
    >>> path_test_dir = pathlib.Path(__file__).parent.parent.parent / 'tests'
    >>> expected_file = path_test_dir / 'test_compare_file_original.txt'
    >>> compare_results_equal(expected_file, path_test_dir / 'test_compare_file_result_equal.txt')
    True
    >>> compare_results_equal(expected_file, path_test_dir / 'test_compare_file_result_different.txt')
    False
    >>> compare_results_equal(expected_file, path_test_dir / 'test_compare_file_result_longer.txt')
    False
    >>> compare_results_equal(expected_file, path_test_dir / 'test_compare_file_result_shorter.txt')
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


def read_files_into_lines(expected_file: pathlib.Path,
                          result_file: pathlib.Path,
                          expected_file_encoding: str = 'utf-8-sig',
                          result_file_encoding: str = 'utf-8-sig') -> Tuple[List[str], List[str]]:

    with open(str(expected_file), mode='r', encoding=expected_file_encoding) as f_expected_file:
        l_expected_lines = f_expected_file.readlines()

    with open(str(result_file), mode='r', encoding=result_file_encoding) as f_result_file:
        l_result_lines = f_result_file.readlines()

    return l_expected_lines, l_result_lines


def log_file_lengths_not_equal(expected_file: pathlib.Path, result_file: pathlib.Path, len_expected_lines: int, len_result_lines: int) -> None:
    lib_log_utils.log_error('Different Size, Expected File {expected_file}: {len_expected_lines} '
                            'Lines, Result File {result_file}: {len_result_lines} Lines'.format(expected_file=expected_file,
                                                                                                len_expected_lines=len_expected_lines,
                                                                                                result_file=result_file,
                                                                                                len_result_lines=len_result_lines))


def log_difference_expected_line(expected_file: pathlib.Path, line_number: int, expected_line: str) -> None:
    lib_log_utils.log_error('Difference, Expected File {expected_file}, Line {line_number}: "{expected_line}"'.format(
        expected_file=expected_file,
        line_number=line_number,
        expected_line=expected_line.replace('\n', '<ret>')))


def log_difference_result_line(result_file: pathlib.Path, line_number: int, result_line: str) -> None:
    lib_log_utils.log_error('Difference, Result   File {result_file}, Line {line_number}: "{result_line}"'.format(
        result_file=result_file,
        line_number=line_number,
        result_line=result_line.replace('\n', '<ret>')))
