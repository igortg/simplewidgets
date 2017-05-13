# coding=utf-8
import inspect
import weakref


class WeakMethod(object):
    """
    Code snippet got from http://code.activestate.com/recipes/81253/ (author: Kristján Valur Jónsson)
    """


    def __init__(self, bound):
        if inspect.ismethod(bound):
            # Support for QObject instance methods
            self.weakself = weakref.proxy(bound.__self__)
            self.methodname = bound.__name__
        else:
            raise TypeError("Bound type not supported")


    def __call__(self, *args, **kw):
        try:
            method_ref = self.ref()
            return method_ref(*args, **kw)
        except ReferenceError:
            return None



    def ref(self):
        """
        Returns the method original reference.

        :rtype: callable
        """
        return getattr(self.weakself, self.methodname)