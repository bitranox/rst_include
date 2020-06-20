# STDLIB
import errno
from io import TextIOWrapper, TextIOBase
import pathlib
import sys
from typing import Tuple, Union, IO

# EXT
import click

# OWN
import lib_log_utils                # type: ignore

# PROJECT
try:
    import rst_include.__init__conf__
    import rst_include.libs.lib_main as lib_main
except (ImportError, ModuleNotFoundError):              # pragma: no cover
    import __init__conf__           # type: ignore      # pragma: no cover
    from libs import lib_main       # type: ignore      # pragma: no cover


# CONSTANTS
CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def get_version_commandline() -> str:
    with open(str(pathlib.Path(__file__).parent / 'version.txt'), mode='r') as version_file:
        version = version_file.readline()
    return version


def build(path_rst_source_file: pathlib.Path, path_rst_target_file: pathlib.Path, travis_repo_slug: str) -> None:

    # noinspection PyBroadException
    lib_log_utils.log_info('create the README.rst')
    repository = travis_repo_slug.split('/')[1]
    repository_dashed = repository.replace('_', '-')

    """
    paths absolute, or relative to the location of the config file
    the notation for relative files is like on windows or linux - not like in python.
    so You might use ../../some/directory/some_document.rst to go two levels back.
    avoid absolute paths since You never know where the program will run.
    """

    lib_log_utils.log_info('include the include blocks')
    lib_main.rst_inc(source=path_rst_source_file, target=path_rst_target_file)

    lib_log_utils.log_info('replace repository related strings')
    lib_main.rst_str_replace(source=path_rst_target_file, target='',
                             str_pattern='{{rst_include.repository_slug}}', str_replace=travis_repo_slug, inplace=True)
    lib_main.rst_str_replace(source=path_rst_target_file, target='',
                             str_pattern='{{rst_include.repository}}', str_replace=repository, inplace=True)
    lib_main.rst_str_replace(source=path_rst_target_file, target='',
                             str_pattern='{{rst_include.double_underline_repository}}', str_replace='=' * len(repository), inplace=True)
    lib_main.rst_str_replace(source=path_rst_target_file, target='',
                             str_pattern='{{rst_include.repository_dashed}}', str_replace=repository_dashed, inplace=True)
    lib_log_utils.log_info('done')


def include(source: str, target: str, quiet: bool, inplace: bool, source_encoding: str, target_encoding: str) -> None:
    lib_log_utils.add_stream_handler()

    target, quiet = adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace)

    path_source: Union[pathlib.Path, IO[str]]
    path_target: Union[pathlib.Path, IO[str]]

    if source == '-':
        path_source = sys.stdin
    else:
        path_source = pathlib.Path(source)

    if target == '-':
        path_target = sys.stdout
        quiet = True
    else:
        path_target = pathlib.Path(target)

    lib_log_utils.BannerSettings.quiet = quiet
    lib_main.rst_inc(source=path_source, target=path_target, source_encoding=source_encoding, target_encoding=target_encoding, inplace=inplace)


def replace(source: str, target: str, str_pattern: str, str_replace: str, count: int,
            quiet: bool, inplace: bool, source_encoding: str, target_encoding: str) -> None:

    target, quiet = adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace)

    path_source: Union[pathlib.Path, IO[str]]
    path_target: Union[pathlib.Path, IO[str]]

    if source == '-':
        path_source = sys.stdin
    else:
        path_source = pathlib.Path(source)

    if target == '-':
        path_target = sys.stdout
        quiet = True
    else:
        path_target = pathlib.Path(target)

    lib_log_utils.add_stream_handler()
    lib_log_utils.BannerSettings.quiet = quiet
    lib_main.rst_str_replace(source=path_source, target=path_target, str_pattern=str_pattern, str_replace=str_replace, count=count,
                             source_encoding=source_encoding, target_encoding=target_encoding, inplace=inplace)


def adjust_cli_parameters(target: str, quiet: bool, inplace: bool) -> Tuple[str, bool]:
    """
    Returns adjusted target and quiet, because we have to be quiet when target = '-'
    >>> target = 'test'
    >>> quiet = False
    >>> inplace = False
    >>> assert adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace) == ('test', False)

    >>> inplace = True
    >>> assert adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace) == ('', False)

    >>> target = '-'
    >>> inplace = True
    >>> assert adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace) == ('', False)

    >>> target = '-'
    >>> inplace = False
    >>> assert adjust_cli_parameters(target=target, quiet=quiet, inplace=inplace) == ('-', True)


    """
    if inplace:
        target = ''

    if target == '-':
        quiet = True

    return target, quiet


def main() -> None:
    """
    >>> main()
    """
    pass


def info() -> None:
    """
    >>> info()  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Info for ...

    """
    __init__conf__.print_info()


@click.group(help=__init__conf__.title, context_settings=CLICK_CONTEXT_SETTINGS)
@click.version_option(version=__init__conf__.version,
                      prog_name=__init__conf__.shell_command,
                      message='{} version %(version)s'.format(__init__conf__.shell_command))
def cli_main() -> None:         # pragma: no cover
    main()                              # pragma: no cover


@cli_main.command('info', context_settings=CLICK_CONTEXT_SETTINGS)
def cli_info() -> None:                     # pragma: no cover
    """ get program informations """
    info()                                  # pragma: no cover


@cli_main.command('include', context_settings=CLICK_CONTEXT_SETTINGS)
@click.argument('source', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, allow_dash=True))
@click.argument('target', type=click.Path(exists=False, file_okay=True, dir_okay=False, readable=False, resolve_path=True, allow_dash=True))
@click.option('-q', '--quiet', is_flag=True)
@click.option('-i', '--inplace', is_flag=True, help='TARGET is discarded, use "-"')
@click.option('-e', '--source_encoding', default='utf8-sig', help='default: utf8-sig')
@click.option('-E', '--target_encoding', default='utf8', help='default: utf8')
def cli_include(source: str, target: str, quiet: bool, inplace: bool, source_encoding: str, target_encoding: str) -> None:  # pragma: no cover
    """ \b
        include the include files,
        use "-" for stdin as SOURCE and
            "-" for stdout as TARGET """
    include(source=source, target=target, quiet=quiet, inplace=inplace, source_encoding=source_encoding, target_encoding=target_encoding)   # pragma: no cover


@cli_main.command('replace', context_settings=CLICK_CONTEXT_SETTINGS)
@click.argument('source', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, allow_dash=True))
@click.argument('target', type=click.Path(exists=False, file_okay=True, dir_okay=False, readable=False, resolve_path=True, allow_dash=True))
@click.argument('str_pattern')
@click.argument('str_replace')
@click.option('-c', '--count', type=int, default=-1)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-i', '--inplace', is_flag=True, help='TARGET is discarded, use "-"')
@click.option('-e', '--source_encoding', default='utf8-sig', help='default: utf8-sig')
@click.option('-E', '--target_encoding', default='utf8', help='default: utf8')
def cli_replace(source: str, target: str, str_pattern: str, str_replace: str, count: int,
                quiet: bool, inplace: bool, source_encoding: str, target_encoding: str) -> None:  # pragma: no cover
    """ replace <str_pattern> with <str_replace> <count> times """
    replace(source=source, target=target, str_pattern=str_pattern, str_replace=str_replace, count=count,
            quiet=quiet, inplace=inplace, source_encoding=source_encoding, target_encoding=target_encoding)


# entry point if main
if __name__ == '__main__':
    try:
        cli_main()
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
