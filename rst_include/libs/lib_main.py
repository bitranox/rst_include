# STDLIB
from io import TextIOWrapper
import pathlib
from typing import Union

try:
    # for pytest
    from . import lib_classes
    from . import lib_assemble_block
    from . import lib_check_files
except ImportError:                                     # type: ignore # pragma: no cover
    # for local doctest in pycharm
    import lib_classes                                  # type: ignore # pragma: no cover
    import lib_assemble_block                           # type: ignore # pragma: no cover
    import lib_check_files                              # type: ignore # pragma: no cover


def rst_str_replace(source: Union[str, pathlib.Path, TextIOWrapper],   # str, file or sys.stdin
                    target: Union[str, pathlib.Path, TextIOWrapper],   # str, file or sys.stdout
                    old: str,
                    new: str,
                    count: int = -1,
                    source_encoding: str = 'utf-8-sig',
                    target_encoding: str = 'utf-8',
                    inplace: bool = False) -> None:

    source, target = lib_check_files.check_source_and_target(source, target, inplace)
    content = lib_check_files.read_input(source, source_encoding)
    content = content.replace(old, new, count)
    lib_check_files.write_output(target, content, target_encoding)


def rst_inc(source: Union[str, pathlib.Path, TextIOWrapper],
            target: Union[str, pathlib.Path, TextIOWrapper],
            source_encoding: str = 'utf-8-sig',
            target_encoding: str = 'utf-8',
            inplace: bool = False) -> None:

    source, target = lib_check_files.check_source_and_target(source, target, inplace)
    rst_file = lib_classes.RstFile(source, target, source_encoding, target_encoding)
    lib_assemble_block.create_rst_file_from_template(rst_file)
