import errno
import os
from rst_include import *
from rst_include.libs import lib_log
import sys


def main():
    repository = 'rst_include'
    repository_dashed = 'rst_include'.replace('_', '-')
    # create the help documentation files
    os.system('"rst_inc.py -h > ./docs/rst_include_help_output.txt"')
    os.system('"rst_inc.py include -h > ./docs/rst_include_help_include_output.txt"')
    os.system('"rst_inc.py replace -h > ./docs/rst_include_help_replace_output.txt"')
    # include the include blocks
    rst_inc(source='./docs/README_template.rst',
            target='./docs/README_template_included.rst')
    # replace repository strings
    rst_str_replace(source='./docs/README_template_included.rst',
                    target='./docs/README_template_repo_replaced.rst',
                    old='{repository}',
                    new=repository)
    rst_str_replace(source='./docs/README_template_repo_replaced.rst',
                    target='./README.rst',
                    old='{repository_dashed}',
                    new=repository_dashed)


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
