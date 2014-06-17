try:
    from PySide import *
except ImportError:
    try:
        from PyQt4 import *
    except ImportError:
        raise RuntimeError("No Python-Qt bindings found")
