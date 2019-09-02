import errno                            # this we need tor main() in __main__.py probably for commandline entry point - to check
import sys                              # this we need tor main() in __main__.py probably for commandline entry point - to check
import logging                          # this we need tor main() in __main__.py probably for commandline entry point - to check
import pathlib


# from .libs.lib_classes import RstFile
# from .libs.lib_classes import RstConf
# from .libs.lib_main import rst_str_replace
# from .libs.lib_main import rst_inc


def get_version() -> str:
    with open(str(pathlib.Path(__file__).parent / 'version.txt'), mode='r') as version_file:
        version = version_file.readline()
    return version


__title__ = 'rst_include'
__version__ = get_version()
__name__ = 'rst_include'
