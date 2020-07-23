# STDLIB
from io import TextIOWrapper
from typing import List, IO, Tuple, Union

# OWN
import lib_log_utils
import pathlib3x as pathlib

# PROJECT
try:
    # for pytest
    from . import lib_classes
    from .lib_classes import RstFile, SourceLine
    from . import lib_test
except (ImportError, ModuleNotFoundError):          # pragma: no cover
    # for local doctest in pycharm
    import lib_classes                              # type: ignore # pragma: no cover
    from lib_classes import RstFile, SourceLine     # type: ignore # pragma: no cover
    import lib_test                                 # type: ignore # pragma: no cover


def check_source_and_target(source: Union[pathlib.Path, IO[str]],
                            target: Union[pathlib.Path, IO[str], None],
                            in_place: bool) -> Tuple[Union[pathlib.Path, IO[str]], Union[pathlib.Path, IO[str], None]]:
    """

    >>> # Setup
    >>> path_test_dir = pathlib.Path(__file__).parent.parent.parent / 'tests'
    >>> path_test_file_exists = path_test_dir / 'include1.py'
    >>> path_test_file_not_exists = path_test_dir / 'does_not_exist.py'

    >>> # create TextIOWrapper Object
    >>> import io, os
    >>> output = io.BytesIO()
    >>> wrapper = io.TextIOWrapper(output, encoding = 'utf8', line_buffering=True)
    >>> assert wrapper.write('test sys_stdin') == 14
    >>> assert wrapper.seek(0, 0) == 0

    >>> # test source = sys.stdin, target=sys.stdout, in_place = False
    >>> source, target = check_source_and_target(wrapper, wrapper, in_place=False)

    >>> # test source = file, in_place = True
    >>> source, target = check_source_and_target(source=path_test_file_exists, target=None, in_place=True)

    >>> # test source = sys.stdin, in_place=True
    >>> source, target = check_source_and_target(source=wrapper, target=None, in_place=True)
    Traceback (most recent call last):
    ...
    SyntaxError: if You use option --inplace You need to specify a input file

    """
    log_and_raise_if_source_file_not_ok(source)
    if in_place:
        if not isinstance(source, pathlib.Path):
            raise SyntaxError('if You use option --inplace You need to specify a input file')
        elif isinstance(target, pathlib.Path) and (target == source):
            lib_log_utils.log_warning('if You use option --inplace You dont need to specify the target file, its ignored')
        elif target and not isinstance(source, TextIOWrapper):
            raise SyntaxError('You used option --inplace and specified a target file different from the input file')
        target = source
    else:
        log_and_raise_if_source_file_equals_target_file(source, target)
        log_warning_if_target_file_exist(target)

    if isinstance(target, TextIOWrapper):
        lib_log_utils.log_settings.quiet = True

    return source, target


def log_and_raise_if_source_file_not_ok(source: Union[str, pathlib.Path, IO[str]]) -> None:
    """

    >>> # Setup
    >>> path_test_dir = pathlib.Path(__file__).parent.parent.parent / 'tests'
    >>> path_test_file_exists = path_test_dir / 'include1.py'
    >>> path_test_file_not_exists = path_test_dir / 'does_not_exist.py'

    >>> # create TextIOWrapper Object
    >>> import io, os
    >>> output = io.BytesIO()
    >>> wrapper = io.TextIOWrapper(output, encoding = 'utf8', line_buffering=True)
    >>> assert wrapper.write('test sys_stdin') == 14
    >>> assert wrapper.seek(0, 0) == 0

    >>> # test file exists
    >>> log_and_raise_if_source_file_not_ok(path_test_file_exists)

    >>> # test file not exists
    >>> log_and_raise_if_source_file_not_ok(path_test_file_not_exists)
    Traceback (most recent call last):
    ...
    FileNotFoundError: RST File ".../tests/does_not_exist.py" does not exist

    >>> # test source is sys.stdin
    >>> log_and_raise_if_source_file_not_ok(wrapper)

    >>> # test source is str
    >>> log_and_raise_if_source_file_not_ok('test')

    """

    if isinstance(source, pathlib.Path):
        if not source.is_file():
            error_message = 'RST File "{source}" does not exist'.format(source=source)
            lib_log_utils.log_error(error_message)
            raise FileNotFoundError(error_message)


def log_and_raise_if_source_file_equals_target_file(source: Union[str, pathlib.Path, IO[str]],
                                                    target: Union[str, pathlib.Path, IO[str], None]) -> None:
    """

    >>> # Setup
    >>> path_test_dir = pathlib.Path(__file__).parent.parent.parent / 'tests'
    >>> path_test_file_exists1 = path_test_dir / 'include1.py'
    >>> path_test_file_exists2 = path_test_dir / 'include2.py'

    >>> # create TextIOWrapper Object
    >>> import io, os
    >>> output = io.BytesIO()
    >>> wrapper = io.TextIOWrapper(output, encoding = 'utf8', line_buffering=True)
    >>> assert wrapper.write('test sys_stdin') == 14
    >>> assert wrapper.seek(0, 0) == 0

    >>> # check input sys.stdin, output sys.stdout
    >>> log_and_raise_if_source_file_equals_target_file(wrapper, wrapper)

    >>> # check not same file
    >>> log_and_raise_if_source_file_equals_target_file(path_test_file_exists1, path_test_file_exists2)

    >>> # check same file
    >>> log_and_raise_if_source_file_equals_target_file(path_test_file_exists1, path_test_file_exists1)
    Traceback (most recent call last):
    ...
    FileExistsError: RST File ".../tests/include1.py": source and target must not be the same

    """

    if isinstance(source, pathlib.Path) and source == target:
        error_message = 'RST File "{source}": source and target must not be the same'.format(source=source)
        lib_log_utils.log_error(error_message)
        raise FileExistsError(error_message)


def log_warning_if_target_file_exist(path_target: Union[str, pathlib.Path, IO[str], None]) -> None:
    """
    >>> # Setup
    >>> path_test_dir = pathlib.Path(__file__).parent.parent.parent / 'tests'
    >>> path_test_file_exists = path_test_dir / 'include1.py'
    >>> path_test_file_not_exists = path_test_dir / 'does_not_exist'

    >>> # TEST
    >>> log_warning_if_target_file_exist(path_target=path_test_file_exists)
    >>> log_warning_if_target_file_exist(path_target=path_test_file_not_exists)

    """
    if isinstance(path_target, pathlib.Path):
        if path_target.is_file():
            lib_log_utils.log_warning('RST File "{target}" exists and will be overwritten'.format(target=path_target))


def read_input(source: Union[str, pathlib.Path, IO[str]], encoding: str = 'utf-8-sig') -> str:
    """
    >>> # Setup
    >>> path_test_dir = pathlib.Path(__file__).parent.parent.parent / 'tests'
    >>> path_test_file = path_test_dir / 'test_read.rst'
    >>> # create TextIOWrapper Object
    >>> import io, os
    >>> output = io.BytesIO()
    >>> wrapper = io.TextIOWrapper(output, encoding = 'utf8', line_buffering=True)
    >>> assert wrapper.write('test sys_stdin') == 14
    >>> assert wrapper.seek(0, 0) == 0

    >>> # read from string
    >>> assert read_input('test string') == 'test string'

    >>> # read from input file
    >>> assert read_input(path_test_file) == 'test file'

    >>> # read from sys.stdin
    >>> assert read_input(wrapper) == 'test sys_stdin'

    """

    if isinstance(source, pathlib.Path):
        content = source.read_text(encoding=encoding)
    elif isinstance(source, TextIOWrapper):
        content = source.read()
    elif isinstance(source, str):
        content = source
    else:
        raise TypeError('type of source not valid')
    return content


def read_source_lines(source: Union[str, pathlib.Path, IO[str]], encoding: str = 'utf-8-sig') -> List[SourceLine]:
    """

    >>> # Setup
    >>> path_test_dir = pathlib.Path(__file__).parent.parent.parent / 'tests'
    >>> path_read_test_file = path_test_dir / 'test_read.rst'
    >>> path_write_test_file = path_test_dir / 'write_test.txt'
    >>> if path_write_test_file.exists(): path_write_test_file.unlink()

    >>> # create TextIOWrapper Object
    >>> import io, os
    >>> output = io.BytesIO()
    >>> wrapper = io.TextIOWrapper(output, encoding = 'utf8', line_buffering=True)
    >>> assert wrapper.write('test sys_stdin') == 14
    >>> assert wrapper.seek(0, 0) == 0

    >>> # read from input file
    >>> l_source_lines = read_source_lines(path_read_test_file)
    >>> assert l_source_lines[0].line_number == 0
    >>> assert l_source_lines[0].content == 'test file'

    >>> assert write_output(path_write_test_file,'line0\\n line1') == 'line0\\n line1'
    >>> l_source_lines = read_source_lines(path_write_test_file)
    >>> assert l_source_lines[0].line_number == 0
    >>> assert l_source_lines[0].content == 'line0'
    >>> assert l_source_lines[1].line_number == 1
    >>> assert l_source_lines[1].content == ' line1'

    >>> # read from sys.stdin
    >>> l_source_lines = read_source_lines(wrapper)
    >>> assert l_source_lines[0].line_number == 0
    >>> assert l_source_lines[0].content == 'test sys_stdin'

    >>> # read from str
    >>> l_source_lines = read_source_lines('test from str')
    >>> assert l_source_lines[0].line_number == 0
    >>> assert l_source_lines[0].content == 'test from str'

    >>> # TEARDOWN
    >>> if path_write_test_file.exists(): path_write_test_file.unlink()

    """

    if isinstance(source, pathlib.Path):
        with open(str(source), encoding=encoding, mode='r') as sourcefile:
            content_lines = sourcefile.readlines()
    elif isinstance(source, TextIOWrapper):
        content_lines = source.readlines()
    elif isinstance(source, str):
        content_lines = source.split('\n')
    else:
        raise TypeError('unknown type of source line')

    l_source_lines = list()
    line_number = 0
    for content in content_lines:
        source_line = lib_classes.SourceLine()
        source_line.line_number = line_number
        source_line.content = content.rstrip()
        line_number = line_number + 1
        l_source_lines.append(source_line)
    return l_source_lines


def write_output(target: Union[pathlib.Path, IO[str], None], content: str, encoding: str = 'utf-8') -> str:
    """
    writes the output to the target. If the target is None, only the text will be returned
    >>> # Setup
    >>> path_test_dir = pathlib.Path(__file__).parent.parent.parent / 'tests'
    >>> path_test_write_test_file = path_test_dir / 'write_test.txt'
    >>> if path_test_write_test_file.exists(): path_test_write_test_file.unlink()
    >>> # create TextIOWrapper Object
    >>> import io, os
    >>> output = io.BytesIO()
    >>> wrapper = io.TextIOWrapper(output, encoding = 'utf8', line_buffering=True)
    >>> assert wrapper.seek(0, 0) == 0


    >>> # write to file
    >>> assert write_output(path_test_write_test_file, 'test') == 'test'
    >>> assert path_test_write_test_file.read_text() == 'test'

    >>> # write to stdout
    >>> assert write_output(wrapper, 'test') == 'test'
    >>> assert wrapper.seek(0, 0) == 0
    >>> assert wrapper.read() == 'test'

    >>> # Teardown
    >>> path_test_write_test_file.unlink(missing_ok=True)

    """

    if isinstance(target, pathlib.Path):                # write to file
        target.write_text(content, encoding=encoding)
    elif isinstance(target, TextIOWrapper):             # write to sys.stdout
        target.write(content)
    return content                                      # return text
