import os

try:
    # for pytest
    from . import lib_classes
    from . import lib_assemble_block
    from . import lib_config_file
    from . import lib_check_files
    from . import lib_path
except ImportError:                                     # type: ignore # pragma: no cover
    # for local doctest in pycharm
    from rst_include.libs import lib_classes            # type: ignore # pragma: no cover
    from rst_include.libs import lib_assemble_block     # type: ignore # pragma: no cover
    from rst_include.libs import lib_config_file        # type: ignore # pragma: no cover
    from rst_include.libs import lib_check_files        # type: ignore # pragma: no cover
    from rst_include.libs import lib_path               # type: ignore # pragma: no cover


def rst_str_replace(source: str, target: str, old: str, new: str, count: int = -1,
                    source_encoding: str = 'utf-8-sig', target_encoding: str = 'utf-8', inplace: bool = False) -> None:
    source, target = lib_check_files.check_and_return_source_and_target(source, target, inplace)
    content = lib_check_files.read_input(source, source_encoding)
    content = content.replace(old, new, count)
    lib_check_files.write_output(target, content, target_encoding)


def rst_inc_from_config(config_file_path: str) -> None:
    save_path = lib_path.get_current_dir()
    try:
        lib_path.chdir_to_path_of_file(config_file_path)
        config_file = lib_config_file.load_config_file(config_file_path)
        rst_conf = getattr(config_file, 'rst_conf')
        l_rst_files = getattr(rst_conf, 'l_rst_files')
        lib_check_files.check_l_rst_files(l_rst_files)
        lib_assemble_block.create_l_rst_files_from_templates(l_rst_files)
    finally:
        os.chdir(save_path)


def rst_inc(source: str, target: str, source_encoding: str = 'utf-8-sig', target_encoding: str = 'utf-8', inplace: bool = False) -> None:
    source, target = lib_check_files.check_and_return_source_and_target(source, target, inplace)
    rst_file = lib_classes.RstFile(source, target, source_encoding, target_encoding)
    lib_assemble_block.create_rst_file_from_template(rst_file)
