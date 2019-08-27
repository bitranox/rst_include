# this __init__.py is only meant for local package development
try:
    from .rst_include import *
# this we need for pip install --install-option test
except ImportError:
    import rst_include
