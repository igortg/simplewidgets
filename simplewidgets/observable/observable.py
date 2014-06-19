from simplewidgets.observable.weakmethod import WeakMethod


class Observable(object):
    """
    Implementation of Observer pattern based on recipes published at

        * http://code.activestate.com/recipes/131499-observer-pattern/
        * http://en.wikipedia.org/wiki/Observer_pattern

    """



    def __init__(self):
        self._observers = []


    def attach(self, observer):
        self._observers.append(WeakMethod(observer))


    def detach(self, observer):
        for weakref in self._observers:
            if weakref.ref() is observer:
                break
        else:
            raise ValueError("Callable not attached")
        self._observers.remove(weakref)


    def notify(self, *args, **kw):
        for observer in self._observers:
            observer(*args, **kw)
