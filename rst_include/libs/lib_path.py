# -*- coding: utf-8 -*-

import os


def is_relative_path(doc_file_name):
    # type: (str) -> bool
    """
    >>> is_relative_path('c:/test/test.txt')
    False
    >>> is_relative_path('/test/test.txt')
    False
    >>> is_relative_path('.test/test.txt')
    True
    >>> is_relative_path('test/test.txt')
    True
    >>> is_relative_path('./test/test.txt')
    True
    >>> is_relative_path('....../test/test.txt')
    True

    """
    doc_file_name = replace_backslashes(doc_file_name)
    if doc_file_name[1:3] == ':/':
        return False
    if doc_file_name.startswith('/'):
        return False
    return True


def get_current_dir():
    # type: () -> str
    """
    >>> path = get_current_dir()
    """
    current_dir = os.path.abspath(os.curdir)
    current_dir = replace_backslashes(current_dir)
    return current_dir


def replace_backslashes(path):
    # type: (str) -> str
    """
    >>> replace_backslashes('c:\\\\test')
    'c:/test'
    """

    path = path.replace('\\', '/')
    return path


def get_absolute_path(path):
    # type: (str) -> str
    """
    >>> get_absolute_path('./test.py')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../test.py'
    """
    path = os.path.abspath(path.strip())
    path = replace_backslashes(path)
    return path


def get_absolute_dirname(path):
    # type: (str) -> str

    """
    >>> get_absolute_dirname('./test.py')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '...rst_include...'
    """
    absolute_filename = get_absolute_path(path)
    absolute_dirname = os.path.dirname(absolute_filename)
    absolute_dirname = replace_backslashes(absolute_dirname)
    return absolute_dirname


def chdir_to_path_of_file(file):
    if file:
        absolute_dirname = get_absolute_dirname(file)
        os.chdir(absolute_dirname)


def get_absolute_path_relative_from_path(path, path2):
    # type: (str, str) -> str
    """
    >>> get_absolute_path_relative_from_path('somefile.txt', './test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../test.txt'
    >>> get_absolute_path_relative_from_path('./a/b/c/', './test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/b/c/test.txt'
    >>> get_absolute_path_relative_from_path('./a/b/c/', './d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/b/c/d/test.txt'
    >>> get_absolute_path_relative_from_path('./a/b/c/some_file.txt', './d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/b/c/d/test.txt'
    >>> get_absolute_path_relative_from_path('./a/b/c/some_file.txt', '../d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/b/d/test.txt'
    >>> get_absolute_path_relative_from_path('./a/b/c/some_file.txt', '../../d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/d/test.txt'
    >>> result = get_absolute_path_relative_from_path('./a/b/c/some_file.txt', '/f/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> assert result.lower() == 'c:/f/test.txt' or result == '/f/test.txt'      # on wine the drive letter is lowercase

    """

    if not is_relative_path(path2):
        result_path = get_absolute_path(path2)
    else:
        base_path = os.path.abspath(os.path.dirname(path))
        result_path = get_absolute_path(base_path + '/' + path2)
    return result_path
