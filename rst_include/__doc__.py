# PROJ
try:
    from . import __init__conf__
except ImportError:                 # pragma: no cover
    # imports for doctest
    import __init__conf__           # type: ignore  # pragma: no cover

__doc__ = """\

Usage:
    {shell_command} (-h | -v | -i)
    {shell_command} include [-s <sourcefile>, -t <targetfile>, -e <source_encoding>, --target_encoding=<target_encoding>, -p, -q]
    {shell_command} replace [-s <sourcefile>, -t <targetfile>, -e <source_encoding>, --target_encoding=<target_encoding>, -p, -q] <old> <new> [<count>]

Options:
    -s <sourcefile>, --source=<sourcefile>                      source file name [default: stdin]
    -t <targetfile>, --target=<targetfile>                      target file name [default: stdout]
    -e <source_encoding>, --source_encoding=<source_encoding>   source encoding [default: utf-8-sig]
    -E <target_encoding>, --target_encoding=<target_encoding>   target encoding [default: utf-8]
    -p, --inplace                                               inplace 
    -q, --quiet                                                 quiet
    -h, --help                                                  show help
    -v, --version                                               show version
    -i, --info                                                  show Info

this module exposes no other useful functions to the commandline

""".format(shell_command=__init__conf__.shell_command)


"""
{'-,': False,
 '--help': False,
 '--info': True,
 '--inplace': False,
 '--quiet': False,
 '--source': [],
 '--target': [],
 '--version': False,
 '<count>': None,
 '<new>': None,
 '<old>': None,
 'include': False,
 'replace': False}

"""