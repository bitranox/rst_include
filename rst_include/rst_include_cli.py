# STDLIB
import sys
from typing import Optional

# EXT
import click

# OWN
import cli_exit_tools

# PROJ
try:
    from . import __init__conf__
    from . import rst_include
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    # imports for doctest
    import __init__conf__                   # type: ignore  # pragma: no cover
    import rst_include                      # type: ignore  # pragma: no cover

# CONSTANTS
CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def info() -> None:
    """
    >>> info()
    Info for ...

    """
    __init__conf__.print_info()


@click.group(help=__init__conf__.title, context_settings=CLICK_CONTEXT_SETTINGS)
@click.version_option(version=__init__conf__.version,
                      prog_name=__init__conf__.shell_command,
                      message='{} version %(version)s'.format(__init__conf__.shell_command))
@click.option('--traceback/--no-traceback', is_flag=True, type=bool, default=None, help='return traceback information on cli')
def cli_main(traceback: Optional[bool] = None) -> None:
    if traceback is not None:
        cli_exit_tools.config.traceback = traceback


@cli_main.command('info', context_settings=CLICK_CONTEXT_SETTINGS)
def cli_info() -> None:                     # pragma: no cover
    """ get program informations """
    info()                                  # pragma: no cover


@cli_main.command('include', context_settings=CLICK_CONTEXT_SETTINGS)
@click.argument('source', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, allow_dash=True))
@click.argument('target', type=click.Path(exists=False, file_okay=True, dir_okay=False, readable=False, resolve_path=True, allow_dash=True))
@click.option('-q', '--quiet', is_flag=True)
@click.option('-i', '--inplace', is_flag=True, help='TARGET is discarded, use "-"')
@click.option('-e', '--source_encoding', default='utf-8-sig', help='default: utf-8-sig')
@click.option('-E', '--target_encoding', default='utf8', help='default: utf8')
def cli_include(source: str, target: str, quiet: bool, inplace: bool, source_encoding: str, target_encoding: str) -> None:  # pragma: no cover
    """ \b
        include the include files,
        use "-" for stdin as SOURCE and
            "-" for stdout as TARGET """
    rst_include.include(source=source, target=target, quiet=quiet, inplace=inplace,
                        source_encoding=source_encoding, target_encoding=target_encoding)   # pragma: no cover


@cli_main.command('replace', context_settings=CLICK_CONTEXT_SETTINGS)
@click.argument('source', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, allow_dash=True))
@click.argument('target', type=click.Path(exists=False, file_okay=True, dir_okay=False, readable=False, resolve_path=True, allow_dash=True))
@click.argument('str_pattern')
@click.argument('str_replace')
@click.option('-c', '--count', type=int, default=-1)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-i', '--inplace', is_flag=True, help='TARGET is discarded, use "-"')
@click.option('-e', '--source_encoding', default='utf-8-sig', help='default: utf-8-sig')
@click.option('-E', '--target_encoding', default='utf8', help='default: utf8')
def cli_replace(source: str, target: str, str_pattern: str, str_replace: str, count: int,
                quiet: bool, inplace: bool, source_encoding: str, target_encoding: str) -> None:  # pragma: no cover
    """ replace <str_pattern> with <str_replace> <count> times """
    rst_include.replace(source=source, target=target, str_pattern=str_pattern, str_replace=str_replace, count=count,
                        quiet=quiet, inplace=inplace, source_encoding=source_encoding, target_encoding=target_encoding)


# entry point if main
if __name__ == '__main__':
    try:
        cli_main()
    except Exception as exc:
        cli_exit_tools.print_exception_message()
        sys.exit(cli_exit_tools.get_system_exit_code(exc))
    finally:
        cli_exit_tools.flush_streams()
