import sys
collect_ignore = []
if sys.version_info < (3, 5):
    collect_ignore.append("build_docs.py")
