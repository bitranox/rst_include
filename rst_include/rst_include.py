# STDLIB
import errno
import pathlib
import sys
from typing import Dict, Union

# EXT
from docopt import docopt

# OWN
import lib_log_utils

# PROJECT
# imports for local pytest
try:
    from .__doc__ import __doc__
    from . import __init__conf__
    from .libs import lib_main
except ImportError:                                     # type: ignore # pragma: no cover
    # imports for doctest local
    from __doc__ import __doc__     # type: ignore  # pragma: no cover
    import __init__conf__           # type: ignore  # pragma: no cover
    from libs import lib_main                           # type: ignore # pragma: no cover


def get_version_commandline() -> str:
    with open(str(pathlib.Path(__file__).parent / 'version.txt'), mode='r') as version_file:
        version = version_file.readline()
    return version


def main(docopt_args: Dict[str, Union[bool, str, None]]) -> None:
    """
    >>> # Setup tests
    >>> args = dict()
    >>> args['--version'] = False
    >>> args['--info'] = False
    >>> args['include'] = False
    >>> args['replace'] = False
    >>> args['--source'] = 'stdin'
    >>> args['--target'] = 'stdout'
    >>> args['--source_encoding'] = 'utf-8-sig'
    >>> args['--target_encoding'] = 'utf-8'
    >>> args['--inplace'] = False
    >>> args['--quiet'] = False
    >>> args['<old>'] = None
    >>> args['<new>'] = None
    >>> args['<count>'] = None

    >>> # Test Version
    >>> args['--version'] = True
    >>> args['--info'] = False
    >>> main(docopt_args=args)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    version: ...


    >>> # Test Info
    >>> args['--version'] = False
    >>> args['--info'] = True
    >>> main(docopt_args=args)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    information for ...

    >>> # Test no args given
    >>> args['--version'] = False
    >>> args['--info'] = False
    >>> main(docopt_args=args)

    >>> # Setup Include Test 1
    >>> path_doc_dir = pathlib.Path(__file__).parent.parent / '.docs'
    >>> path_source_file = path_doc_dir / 'README_template.rst'
    >>> path_target_file = path_doc_dir / 'README_doctest.rst'
    >>> path_target_file.unlink(missing_ok=True)
    >>> args = dict()
    >>> args['--version'] = False
    >>> args['--info'] = False
    >>> args['include'] = True
    >>> args['replace'] = False
    >>> args['--source'] = str(path_source_file)
    >>> args['--target'] = str(path_target_file)
    >>> args['--source_encoding'] = 'utf-8-sig'
    >>> args['--target_encoding'] = 'utf-8'
    >>> args['--inplace'] = False
    >>> args['--quiet'] = False
    >>> args['<old>'] = None
    >>> args['<new>'] = None
    >>> args['<count>'] = None

    >>> # Test Include 1
    >>> main(docopt_args=args)

    >>> # teardown Test Include 1
    >>> path_target_file.unlink(missing_ok=True)

    >>> # Setup Include Test 2
    >>> path_test_dir = pathlib.Path(__file__).parent.parent / 'tests'
    >>> path_source_file = path_test_dir / 'test1_no_includes_template.rst'
    >>> path_target_file = path_test_dir / 'test1_no_includes_result.rst'
    >>> path_expected_file = path_test_dir / 'test1_no_includes_expected.rst'
    >>> path_target_file.unlink(missing_ok=True)
    >>> args = dict()
    >>> args['--version'] = False
    >>> args['--info'] = False
    >>> args['include'] = True
    >>> args['replace'] = False
    >>> args['--source'] = str(path_source_file)
    >>> args['--target'] = str(path_target_file)
    >>> args['--source_encoding'] = 'utf-8-sig'
    >>> args['--target_encoding'] = 'utf-8'
    >>> args['--inplace'] = False
    >>> args['--quiet'] = False
    >>> args['<old>'] = None
    >>> args['<new>'] = None
    >>> args['<count>'] = None

    >>> # Test Include 2
    >>> main(docopt_args=args)
    >>> assert path_target_file.read_text() == path_expected_file.read_text()

    >>> # teardown Test Include 2
    >>> path_target_file.unlink(missing_ok=True)

    >>> # Setup Replace Test
    >>> path_test_dir = pathlib.Path(__file__).parent.parent / 'tests'
    >>> path_source_file = path_test_dir / 'test1_no_includes_template.rst'
    >>> path_target_file = path_test_dir / 'test1_no_includes_result.rst'
    >>> path_expected_file = path_test_dir / 'test1_no_includes_expected_replace.rst'
    >>> path_target_file.unlink(missing_ok=True)

    >>> args = dict()
    >>> args['--version'] = False
    >>> args['--info'] = False
    >>> args['include'] = False
    >>> args['replace'] = True
    >>> args['--source'] = str(path_source_file)
    >>> args['--target'] = str(path_target_file)
    >>> args['--source_encoding'] = 'utf-8-sig'
    >>> args['--target_encoding'] = 'utf-8'
    >>> args['--inplace'] = False
    >>> args['--quiet'] = False
    >>> args['<old>'] = '='
    >>> args['<new>'] = '*'
    >>> args['<count>'] = '-1'

    >>> # Test replace
    >>> main(docopt_args=args)
    >>> assert path_target_file.read_text() == path_expected_file.read_text()

    >>> # teardown Test Replace
    >>> path_target_file.unlink(missing_ok=True)

    """
    try:
        if docopt_args['--version']:
            __init__conf__.print_version()
            return

        elif docopt_args['--info']:
            __init__conf__.print_info()
            return

        # get the docopt commandline values

        inplace = docopt_args['--inplace']
        quiet = docopt_args['--quiet']

        source = docopt_args['--source']
        if source == 'stdin':
            source = sys.stdin
        else:
            source = pathlib.Path(source)

        target = docopt_args['--target']
        if target == 'stdout':
            target = sys.stdout
            quiet = True
        else:
            target = pathlib.Path(target)

        source_encoding = docopt_args['--source_encoding']
        target_encoding = docopt_args['--target_encoding']

        if docopt_args['<count>']:
            count = int(docopt_args['<count>'])
        else:
            count = -1

        if docopt_args['<old>']:
            old = str(docopt_args['<old>'])
        else:
            old = ''

        if docopt_args['<new>']:
            new = str(docopt_args['<new>'])
        else:
            new = ''

        # set logging
        lib_log_utils.add_stream_handler()
        lib_log_utils.BannerSettings.quiet = quiet

        # do the thing
        if docopt_args['replace']:
            lib_main.rst_str_replace(source=source, target=target, old=old, new=new, count=count,
                                     source_encoding=source_encoding, target_encoding=target_encoding, inplace=inplace)
        elif docopt_args['include']:
            lib_main.rst_inc(source=source, target=target, source_encoding=source_encoding, target_encoding=target_encoding, inplace=inplace)

    except FileNotFoundError:
        # see https://www.thegeekstuff.com/2010/10/linux-error-codes for error codes
        # No such file or directory
        sys.exit(errno.ENOENT)      # pragma: no cover
    except FileExistsError:
        # File exists
        sys.exit(errno.EEXIST)      # pragma: no cover
    except TypeError:
        # Invalid Argument
        sys.exit(errno.EINVAL)      # pragma: no cover
        # Invalid Argument
    except ValueError:
        sys.exit(errno.EINVAL)      # pragma: no cover


# entry point via commandline
def main_commandline() -> None:
    """
    >>> main_commandline()  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    docopt.DocoptExit: ...

    """
    docopt_args = docopt(__doc__)
    main(docopt_args)       # pragma: no cover


# entry point if main
if __name__ == '__main__':
    main_commandline()
