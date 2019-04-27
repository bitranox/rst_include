from rst_include.libs import lib_classes
from rst_include.libs import lib_assemble_block
from rst_include.libs import lib_config_file
from rst_include.libs import lib_check_files
from rst_include.libs import lib_path

import os


def rst_str_replace(source: str, target: str, old: str, new: str, count: int = -1,
                    source_encoding: str = 'utf-8-sig', target_encoding: str = 'utf-8') -> None:
    lib_check_files.check_source_and_target(source, target)
    content = lib_check_files.read_input(source, source_encoding)
    content = content.replace(old, new, count)
    lib_check_files.write_output(target, content, target_encoding)


def rst_inc_from_config(config_file_path: str) -> None:
    save_path = lib_path.get_current_dir()
    try:
        lib_path.chdir_to_path_of_file(config_file_path)
        config_file = lib_config_file.load_config_file(config_file_path)
        l_rst_files = config_file.rst_conf.l_rst_files
        lib_check_files.check_l_rst_files(l_rst_files)
        lib_assemble_block.create_l_rst_files_from_templates(l_rst_files)
    finally:
        os.chdir(save_path)


def rst_inc(source: str, target: str, source_encoding: str = 'utf-8-sig', target_encoding: str = 'utf-8') -> None:
    lib_check_files.check_source_and_target(source, target)
    rst_file = lib_classes.RstFile(source, target, source_encoding, target_encoding)
    lib_assemble_block.create_rst_file_from_template(rst_file)
