from typing import Union


class RstFile(object):
    def __init__(self, source, target, source_encoding='utf-8-sig', target_encoding='utf-8'):
        # type: (str, str, str, str) -> None
        self.source = source                        # type: str
        self.source_encoding = source_encoding      # type: str
        self.target = target                        # type: str
        self.target_encoding = target_encoding      # type: str


class RstConf(object):
    def __init__(self):
        self.l_rst_files = []                       # type: [RstFile]


class SourceLine(object):
    def __init__(self, line_number=0, content=''):
        # type: (int, str) -> None
        self.line_number = line_number
        self.content = content


class Block(object):
    def __init__(self, source_file_name):
        # type: (str) -> None
        self.is_include_block = False                               # type: int
        self.source_file_name = source_file_name                    # type: str
        self.l_source_lines = []                                    # type: [SourceLine]

        self.include_filename = ''                                  # type: str
        self.include_filename_absolut = ''                          # type: str
        self.include_file_code = ''                                 # type: str
        self.include_file_encoding = 'utf-8-sig'                    # type: str
        self.include_file_start_line = None                         # type: Union[int, None]
        self.include_file_end_line = None                           # type: Union[int, None]
        self.include_file_start_after = ''                          # type: str
        self.include_file_end_before = ''                           # type: str
        self.include_file_lines = list()                            # type: [str]
        self.include_file_sliced_content = ''                       # type: str
        self.include_file_number_of_blanks_to_add_to_content = 0    # type: int
        self.pass_through_options = list()                          # type: [SourceLine]
        self.additional_content = list()                            # type: [SourceLine]
