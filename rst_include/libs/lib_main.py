# STDLIB
import os

# OWN
import lib_path

try:
    # for pytest
    from . import lib_classes
    from . import lib_assemble_block
    from . import lib_check_files
except ImportError:                                     # type: ignore # pragma: no cover
    # for local doctest in pycharm
    from rst_include.libs import lib_classes            # type: ignore # pragma: no cover
    from rst_include.libs import lib_assemble_block     # type: ignore # pragma: no cover
    from rst_include.libs import lib_check_files        # type: ignore # pragma: no cover


def rst_str_replace(source: str, target: str, old: str, new: str, count: int = -1,
                    source_encoding: str = 'utf-8-sig', target_encoding: str = 'utf-8', inplace: bool = False) -> None:
    source, target = lib_check_files.check_and_return_source_and_target(source, target, inplace)
    content = lib_check_files.read_input(source, source_encoding)
    content = content.replace(old, new, count)
    lib_check_files.write_output(target, content, target_encoding)


def rst_inc(source: str, target: str, source_encoding: str = 'utf-8-sig', target_encoding: str = 'utf-8', inplace: bool = False) -> None:
    source, target = lib_check_files.check_and_return_source_and_target(source, target, inplace)
    rst_file = lib_classes.RstFile(source, target, source_encoding, target_encoding)
    lib_assemble_block.create_rst_file_from_template(rst_file)
