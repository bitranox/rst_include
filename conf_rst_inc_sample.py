from rst_include import *

# set config here
rst_conf = RstConf()

# paths absolute, or relative to the location of the config file
# the notation for relative files is like on windows or linux - not like in python.
# so You might use ../../some/directory/some_document.rst to go two levels back.
# avoid absolute paths since You never know where the program will run.
rst_conf.l_rst_files = [RstFile(source='./rst_include/tests/test1_no_includes_template.rst',
                                target='./rst_include/tests/test1_no_includes_result.rst',
                                # default = utf-8-sig because it can read utf-8 and utf-8-sig
                                source_encoding='utf-8-sig',
                                # default = utf-8
                                target_encoding='utf-8'
                                ),
                        RstFile(source='./rst_include/tests/test2_include_samedir_template.rst',
                                target='./rst_include/tests/test2_include_samedir_result.rst'),
                        RstFile(source='./rst_include/tests/test3_include_subdir_template.rst',
                                target='./rst_include/tests/test3_include_subdir_result.rst'),
                        RstFile(source='./rst_include/tests/test4_include_nocode_template.rst',
                                target='./rst_include/tests/test4_include_nocode_result.rst')]
