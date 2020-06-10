""" Build the README.rst either locally, or on Github for tagged commits.

Usage:
    build_docs.py <TRAVIS_REPO_SLUG>
    build_docs.py (-h | --help)

The TRAVIS_REPO_SLUG has following Format : "github_username/github_repository"

Options:
    -h --help   Show this screen
"""

# STDLIB
import datetime
import errno
import logging
import pathlib
import sys
from typing import Dict

# ext
from docopt import docopt       # type: ignore

# OWN
import lib_log_utils            # type: ignore
import rst_include              # type: ignore

# PROJ
import project_conf


def main(args: Dict[str, str]) -> None:

    rst_template = pathlib.Path('./.docs/README_template.rst')
    rst_template_tmp = pathlib.Path('./.docs/README_template_tmp.rst')
    rst_target = pathlib.Path('./README.rst')

    # noinspection PyBroadException
    try:
        lib_log_utils.log_info('create the README.rst')
        travis_repo_slug = args['<TRAVIS_REPO_SLUG>']
        repository = travis_repo_slug.split('/')[1]
        repository_dashed = repository.replace('_', '-')

        """
        paths absolute, or relative to the location of the config file
        the notation for relative files is like on windows or linux - not like in python.
        so You might use ../../some/directory/some_document.rst to go two levels back.
        avoid absolute paths since You never know where the program will run.
        """

        if project_conf.badges_with_jupiter:
            rst_include.rst_str_replace(source=rst_template, target=rst_template_tmp, old='{try_in_jupyter}', new='.. include:: ./try_in_jupyter.rst')
        else:
            rst_include.rst_str_replace(source=rst_template, target=rst_template_tmp, old='{try_in_jupyter}', new='')

        lib_log_utils.log_info('include the include blocks')
        rst_include.rst_inc(source=rst_template_tmp, target=rst_target)

        lib_log_utils.log_info('replace repository related strings')
        rst_include.rst_str_replace(source=rst_target, target='', old='{repository_slug}', new=travis_repo_slug, inplace=True)
        rst_include.rst_str_replace(source=rst_target, target='', old='{repository}', new=repository, inplace=True)
        rst_include.rst_str_replace(source=rst_target, target='', old='{double_underline_repository}', new='=' * len(repository), inplace=True)
        rst_include.rst_str_replace(source=rst_target, target='', old='{repository_dashed}', new=repository_dashed, inplace=True)
        rst_include.rst_str_replace(source=rst_target, target='', old='{last_update_yyyy}', new=str(datetime.date.today().year + 1), inplace=True)
        rst_include.rst_str_replace(source=rst_target, target='', old='{codeclimate_link_hash}', new=project_conf.codeclimate_link_hash, inplace=True)

        lib_log_utils.log_info('done')
        sys.exit(0)
    finally:
        rst_template_tmp.unlink(missing_ok=True)


if __name__ == '__main__':

    if sys.version_info < (3, 6):
        lib_log_utils.log_error('only Python Versions from 3.6 are supported')
        sys.exit(1)

    lib_log_utils.add_stream_handler()          # type: ignore      # in order to pass mypy in the lib_log_utils package
    try:
        _args = docopt(__doc__)
        main(_args)
    except FileNotFoundError:
        # see https://www.thegeekstuff.com/2010/10/linux-error-codes for error codes
        sys.exit(errno.ENOENT)      # No such file or directory
    except FileExistsError:
        sys.exit(errno.EEXIST)      # File exists
    except TypeError:
        sys.exit(errno.EINVAL)      # Invalid Argument
    except ValueError:
        sys.exit(errno.EINVAL)      # Invalid Argument
