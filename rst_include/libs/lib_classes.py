# STDLIB
from typing import List, IO, Union

# OWN
import pathlib3x as pathlib


class RstFile(object):
    def __init__(self,
                 source: Union[pathlib.Path, IO[str]],
                 # if target = None, then the Output will be just returned as Text and not written anywere
                 target: Union[pathlib.Path, IO[str], None],
                 source_encoding: str = 'utf-8-sig',
                 target_encoding: str = 'utf-8'):
        self.source = source
        self.source_encoding = source_encoding
        self.target = target
        self.target_encoding = target_encoding


class SourceLine(object):
    def __init__(self, line_number: int = 0, content: str = ''):
        self.line_number = line_number
        self.content = content


class Block(object):
    def __init__(self, source: Union[str, pathlib.Path, IO[str]]):
        self.is_include_block = False
        self.source = source                            # either pathlib.Path of the source file, or "str" or "sys.stdin"
        self.l_source_lines = []                        # type: List[SourceLine]

        self.include_filename = pathlib.Path()
        self.include_filename_absolut = pathlib.Path()
        self.include_file_code = ''
        self.include_file_encoding = 'utf-8-sig'
        self.include_file_start_line = None             # type: Union[int, None]
        self.include_file_end_line = None               # type: Union[int, None]
        self.include_file_start_after = ''              # type: str
        self.include_file_end_before = ''               # type: str
        self.include_file_lines = list()                # type: List[str]    # lines of the include file, rstripped, without \n
        self.include_file_sliced_content = ''           # str , lines of the include file, rstripped, ending without \n
        self.include_file_number_of_blanks_to_add_to_content = 0
        self.pass_through_options = list()              # type: List[SourceLine]
        self.additional_content = list()                # type: List[SourceLine]
