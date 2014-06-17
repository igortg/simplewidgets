try:
    from PySide.QtCore import *
except ImportError:
    try:
        from PyQt4.QtCore import *
    except ImportError:
        raise RuntimeError("No Python-Qt bindings found")
