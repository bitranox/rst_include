# STDLIB
from typing import IO, Union

# OWN
import pathlib3x as pathlib

# PROJ
try:
    from . import lib_classes
    from . import lib_assemble_block
    from . import lib_check_files
except (ImportError, ModuleNotFoundError):      # pragma: no cover
    import lib_classes          # type: ignore  # pragma: no cover
    import lib_assemble_block   # type: ignore  # pragma: no cover
    import lib_check_files      # type: ignore  # pragma: no cover


def rst_str_replace(source: Union[pathlib.Path, IO[str]],  # str, file or sys.stdin
                    target: Union[pathlib.Path, IO[str], None],  # str, file or sys.stdout, or None for no Output
                    str_pattern: str,
                    str_replace: str,
                    count: int = -1,
                    source_encoding: str = 'utf-8-sig',
                    target_encoding: str = 'utf-8',
                    inplace: bool = False) -> None:

    # make sure it is pathlib3x instance
    if pathlib.Path.is_path_instance(source):
        source = pathlib.Path(source)           # type: ignore
    if pathlib.Path.is_path_instance(target):
        target = pathlib.Path(target)           # type: ignore

    path_source, path_target = lib_check_files.check_source_and_target(source, target, inplace)
    content = lib_check_files.read_input(path_source, source_encoding)
    content = content.replace(str_pattern, str_replace, count)
    lib_check_files.write_output(path_target, content, target_encoding)


def rst_inc(source: Union[pathlib.Path, IO[str]],
            target: Union[pathlib.Path, IO[str], None],
            source_encoding: str = 'utf-8-sig',
            target_encoding: str = 'utf-8',
            inplace: bool = False) -> None:

    # make sure it is pathlib3x instance
    if pathlib.Path.is_path_instance(source):
        source = pathlib.Path(source)           # type: ignore
    if pathlib.Path.is_path_instance(target):
        target = pathlib.Path(target)           # type: ignore
    path_source, path_target = lib_check_files.check_source_and_target(source, target, inplace)
    rst_file = lib_classes.RstFile(path_source, path_target, source_encoding, target_encoding)
    lib_assemble_block.create_rst_file_from_template(rst_file)
