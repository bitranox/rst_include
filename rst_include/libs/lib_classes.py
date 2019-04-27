from typing import Union


class RstFile(object):
    def __init__(self, source: str, target: str, source_encoding: str = 'utf-8-sig', target_encoding: str = 'utf-8') -> None:
        self.source: str = source
        self.source_encoding: str = source_encoding
        self.target: str = target
        self.target_encoding: str = target_encoding


class RstConf(object):
    def __init__(self):
        self.l_rst_files: [RstFile] = []


class SourceLine(object):
    def __init__(self, line_number: int = 0, content: str = ''):
        self.line_number: int = line_number
        self.content: str = content


class Block(object):
    def __init__(self, source_file_name: str):
        self.is_include_block: bool = False
        self.source_file_name: str = source_file_name
        self.l_source_lines: [SourceLine] = []

        self.include_filename: str = ''
        self.include_filename_absolut: str = ''
        self.include_file_code: str = ''
        self.include_file_encoding: str = 'utf-8-sig'
        self.include_file_start_line: Union[str, None] = None
        self.include_file_end_line: Union[int, None] = None
        self.include_file_start_after: str = ''
        self.include_file_end_before: str = ''
        self.include_file_lines: [str] = list()
        self.include_file_sliced_content: [str] = ''
        self.include_file_number_of_blanks_to_add_to_content: int = 0
        self.pass_through_options: [SourceLine] = list()
        self.additional_content: [SourceLine] = list()
