# PROJECT

try:
    from .main import build
except (ImportError, ModuleNotFoundError):              # pragma: no cover
    from main import build          # type: ignore      # pragma: no cover

# this needs to come after the module imports, otherwise circular import under windows
# import rst_include.__init__conf__ as __init__conf__   # valid absolute import
# from rst_include import __init__conf__                # valid absolute import
from . import __init__conf__                            # valid relative Import
__title__ = __init__conf__.title
__version__ = __init__conf__.version
__name__ = __init__conf__.name
__url__ = __init__conf__.url
__author__ = __init__conf__.author
__author_email__ = __init__conf__.author_email
__shell_command__ = __init__conf__.shell_command
