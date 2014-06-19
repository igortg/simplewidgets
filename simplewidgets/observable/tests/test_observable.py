import mock
from simplewidgets.observable.observable import Observable


#TODO: Create a py.test
class Demo(object):

    def call(self):
        print "a"


observed = Demo()
observable = Observable()
observable.attach(observed.call)
observable.notify()
