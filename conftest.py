# ignore for pytest collection
collect_ignore = ['build_docs.py', 'rst_include/__main__.py']

"""
collect_ignore = ['build_docs.py',
                  'conf_rst_inc_sample.py',
                  'rst_include/tests/conf_rst_inc.py',
                  'rst_include/tests/conf_rst_include_test.py',
                  'rst_include/tests/conf_rst_include_test_attr_l_rst_files_missing.py',
                  'rst_include/rst_inc.py'
                  ]

if sys.version_info < (3, 5):
    collect_ignore.append("something")
"""
