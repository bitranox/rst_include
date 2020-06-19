# STDLIB
import pathlib
from typing import IO, Union

from . import lib_classes
from . import lib_assemble_block
from . import lib_check_files


def rst_str_replace(source: Union[str, pathlib.Path, IO[str]],  # str, file or sys.stdin
                    target: Union[str, pathlib.Path, IO[str]],  # str, file or sys.stdout
                    str_pattern: str,
                    str_replace: str,
                    count: int = -1,
                    source_encoding: str = 'utf-8-sig',
                    target_encoding: str = 'utf-8',
                    inplace: bool = False) -> None:

    path_source, path_target = lib_check_files.check_source_and_target(source, target, inplace)
    content = lib_check_files.read_input(path_source, source_encoding)
    content = content.replace(str_pattern, str_replace, count)
    lib_check_files.write_output(path_target, content, target_encoding)


def rst_inc(source: Union[str, pathlib.Path, IO[str]],
            target: Union[str, pathlib.Path, IO[str]],
            source_encoding: str = 'utf-8-sig',
            target_encoding: str = 'utf-8',
            inplace: bool = False) -> None:

    path_source, path_target = lib_check_files.check_source_and_target(source, target, inplace)
    rst_file = lib_classes.RstFile(path_source, path_target, source_encoding, target_encoding)
    lib_assemble_block.create_rst_file_from_template(rst_file)
