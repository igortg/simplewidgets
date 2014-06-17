try:
    from PySide.QtGui import *
except ImportError:
    try:
        from PyQt4.QtGui import *
    except ImportError:
        raise RuntimeError("No Python-Qt bindings found")
