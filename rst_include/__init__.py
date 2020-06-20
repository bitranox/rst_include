# this needs to come after the module imports, otherwise circular import under windows
from .rst_include import build
from . import __init__conf__                            # valid relative Import
__title__ = __init__conf__.title
__version__ = __init__conf__.version
__name__ = __init__conf__.name
__url__ = __init__conf__.url
__author__ = __init__conf__.author
__author_email__ = __init__conf__.author_email
__shell_command__ = __init__conf__.shell_command
