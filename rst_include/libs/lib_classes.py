class RstFile(object):
    def __init__(self, source: str, target: str, source_encoding: str = 'utf-8-sig', target_encoding: str = 'utf-8') -> None:
        self.source = source
        self.source_encoding = source_encoding
        self.target = target
        self.target_encoding = target_encoding


class RstConf(object):
    def __init__(self):
        self.l_rst_files = []


class SourceLine(object):
    def __init__(self, line_number: int = 0, content: str = ''):
        self.line_number = line_number
        self.content = content


class Block(object):
    def __init__(self, source_file_name: str):
        self.is_include_block = False
        self.source_file_name = source_file_name
        self.l_source_lines = []

        self.include_filename = ''
        self.include_filename_absolut = ''
        self.include_file_code = ''
        self.include_file_encoding = 'utf-8-sig'
        self.include_file_start_line = None  # Union[str, None]
        self.include_file_end_line = None  # Union[int, None]
        self.include_file_start_after = ''
        self.include_file_end_before = ''
        self.include_file_lines = list()
        self.include_file_sliced_content = ''
        self.include_file_number_of_blanks_to_add_to_content = 0
        self.pass_through_options = list()  # [SourceLine]
        self.additional_content = list()    # [SourceLine]
