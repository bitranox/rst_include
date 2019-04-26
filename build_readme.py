import errno
import logging
import os
from rst_include import *
from rst_include.libs import lib_log
import sys

codeclimate_link_hash = "ff3f414903627e5cfc35"
repository = 'rst_include'


def main():
    logger = logging.getLogger('create_readme')
    logger.info('create the README.rst')
    repository_dashed = 'rst_include'.replace('_', '-')

    logger.info('create help documentation files')
    os.system('"rst_inc.py -h > ./docs/rst_include_help_output.txt"')
    os.system('"rst_inc.py include -h > ./docs/rst_include_help_include_output.txt"')
    os.system('"rst_inc.py replace -h > ./docs/rst_include_help_replace_output.txt"')

    logger.info('include the include blocks')
    rst_inc(source='./docs/README_template.rst',
            target='./docs/README_template_included.rst')

    logger.info('replace repository related strings')
    rst_str_replace(source='./docs/README_template_included.rst',
                    target='./docs/README_template_repo_replaced.rst',
                    old='{repository}',
                    new=repository)
    rst_str_replace(source='./docs/README_template_repo_replaced.rst',
                    target='./docs/README_template_repo_replaced2.rst',
                    old='{repository_dashed}',
                    new=repository_dashed)
    rst_str_replace(source='./docs/README_template_repo_replaced2.rst',
                    target='./README.rst',
                    old='{codeclimate_link_hash}',
                    new=codeclimate_link_hash)

    logger.info('cleanup')
    os.remove('./docs/README_template_included.rst')
    os.remove('./docs/README_template_repo_replaced.rst')
    os.remove('./docs/README_template_repo_replaced2.rst')

    logger.info('done')
    sys.exit(0)


if __name__ == '__main__':
    try:
        lib_log.setup_logger()
        main()
    except FileNotFoundError:
        # see https://www.thegeekstuff.com/2010/10/linux-error-codes for error codes
        sys.exit(errno.ENOENT)      # No such file or directory
    except FileExistsError:
        sys.exit(errno.EEXIST)      # File exists
    except TypeError:
        sys.exit(errno.EINVAL)      # Invalid Argument
    except ValueError:
        sys.exit(errno.EINVAL)      # Invalid Argument
