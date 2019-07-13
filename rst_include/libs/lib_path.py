import os
import platform


def get_is_windows() -> bool:
    return platform.system().lower() == 'windows'


is_windows = get_is_windows()


def is_relative_path(doc_file_name: str) -> bool:
    """
    >>> is_relative_path('/test/test.txt')
    False
    >>> is_relative_path('//main/install')
    False

    >>> result = is_relative_path('c:/test/test.txt')
    >>> if is_windows:
    ...    assert result == False
    ... else:
    ...    assert result == True

    >>> result = is_relative_path('D:/test/test.txt')
    >>> if is_windows:
    ...    assert result == False
    ... else:
    ...    assert result == True

    >>> is_relative_path('.test/test.txt')
    True
    >>> is_relative_path('test/test.txt')
    True
    >>> is_relative_path('./test/test.txt')
    True
    >>> is_relative_path('....../test/test.txt')
    True

    """
    dirname = strip_and_replace_backslashes(os.path.dirname(doc_file_name))  # windows : /test
    abspath = strip_and_replace_backslashes(os.path.abspath(dirname))        # windows : C:/test
    if not path_starts_with_windows_drive_letter(dirname):
        abspath = substract_windows_drive_letter(abspath)
    if dirname != abspath:
        return True
    else:
        return False


def get_current_dir() -> str:
    """
    >>> path = get_current_dir()
    """
    current_dir = os.path.abspath(os.curdir)
    current_dir = strip_and_replace_backslashes(current_dir)
    return current_dir


def is_windows_network_unc(path: str) -> bool:
    """
    >>> is_windows_network_unc('/test')
    False
    >>> is_windows_network_unc('c:/test')
    False
    >>> is_windows_network_unc('//install/main')
    True
    """
    path = strip_and_replace_backslashes(path)
    if path.startswith('//'):
        return True
    else:
        return False


def substract_windows_drive_letter(path: str) -> str:
    """
    >>> substract_windows_drive_letter('//main/install')
    '//main/install'
    >>> substract_windows_drive_letter('/test')
    '/test'
    >>> substract_windows_drive_letter('c:\\\\test')
    '/test'
    """
    path = strip_and_replace_backslashes(path)
    if path_starts_with_windows_drive_letter(path):
        path = path[2:]
    return path


def path_starts_with_windows_drive_letter(path: str) -> bool:
    """
    >>> path_starts_with_windows_drive_letter('//main/install')
    False
    >>> path_starts_with_windows_drive_letter('/test')
    False
    >>> path_starts_with_windows_drive_letter('c:\\\\test')
    True
    """
    path = strip_and_replace_backslashes(path)
    if path[1:].startswith(':/'):
        return True
    else:
        return False


def strip_and_replace_backslashes(path: str) -> str:
    """
    >>> strip_and_replace_backslashes('c:\\\\test')
    'c:/test'
    >>> strip_and_replace_backslashes('\\\\\\\\main\\\\install')
    '//main/install'
    """
    path = path.strip().replace('\\', '/')
    return path


def get_absolute_path(path: str) -> str:
    """
    >>> get_absolute_path('./test.py')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../test.py'
    """
    path = os.path.abspath(path.strip())
    path = strip_and_replace_backslashes(path)
    return path


def get_absolute_dirname(path: str) -> str:
    """
    >>> get_absolute_dirname('./test.py')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '...rst_include...'
    """
    absolute_filename = get_absolute_path(path)
    absolute_dirname = os.path.dirname(absolute_filename)
    absolute_dirname = strip_and_replace_backslashes(absolute_dirname)
    return absolute_dirname


def chdir_to_path_of_file(file: str) -> None:
    if file:
        absolute_dirname = get_absolute_dirname(file)
        os.chdir(absolute_dirname)


def get_absolute_path_relative_from_path(path: str, path2: str) -> str:
    """
    if the first path is relative, on windows the drive will be the current drive.
    this is necessary because WINE gives drive "Z" back !

    >>> # path1 absolut, path2 relativ
    >>> get_absolute_path_relative_from_path('c:/a/b/c/some-file.txt', './d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/b/c/d/test.txt'
    >>> # path1 relativ, path2 relativ
    >>> get_absolute_path_relative_from_path('./a/b/c/some-file.txt', './d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/b/c/d/test.txt'
    >>> # path1 absolut, path2 absolut
    >>> get_absolute_path_relative_from_path('c:/a/b/c/some-file.txt', 'c:/d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../d/test.txt'
    >>> # path1 relativ, path2 absolut
    >>> get_absolute_path_relative_from_path('./a/b/c/some-file.txt', 'c:/d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../d/test.txt'
    >>> # path one level back
    >>> get_absolute_path_relative_from_path('c:/a/b/c/some-file.txt', '../d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/b/d/test.txt'
    >>> # path two levels back
    >>> get_absolute_path_relative_from_path('./a/b/c/some_file.txt', '../../d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/d/test.txt'
    >>> result = get_absolute_path_relative_from_path('./a/b/c/some_file.txt', '/f/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> result = substract_windows_drive_letter(result)
    >>> assert result.lower() == '/f/test.txt'

    """

    if is_relative_path(path2):
        base_path = os.path.abspath(os.path.dirname(path))
        result_path = get_absolute_path(base_path + '/' + path2)
    else:
        result_path = get_absolute_path(path2)
    return result_path
