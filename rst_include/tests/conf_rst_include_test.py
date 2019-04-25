import rst_include.libs.lib_classes as lib_classes

# set config here
rst_conf = lib_classes.RstConf()

rst_conf.l_rst_files = [
    lib_classes.RstFile(source='test1_no_includes_template.rst',
                        target='test1_no_includes_result.rst',
                        source_encoding='utf-8-sig',  # default = utf-8-sig because it can read utf-8 and utf-8-sig
                        target_encoding='utf-8'      # default = utf-8
                        ),
    lib_classes.RstFile(source='test2_include_samedir_template.rst',
                        target='test2_include_samedir_result.rst'),
    lib_classes.RstFile(source='test3_include_subdir_template.rst',
                        target='test3_include_subdir_result.rst'),
    lib_classes.RstFile(source='test4_include_nocode_template.rst',
                        target='test4_include_nocode_result.rst'),
    ]
