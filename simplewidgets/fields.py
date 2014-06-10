import locale
from PySide.QtGui import QLineEdit, QIntValidator


class BaseInputField(object):

    # _coubter is a global counter so UI fields are created in the same order of their declaraion
    # ref: http://stackoverflow.com/a/11317693/885117
    _counter = 0

    def __init__(self, initial="", label=""):
        self.order = self._counter
        BaseInputField._counter += 1
        self.label = label
        self.initial = initial


    def create_widget(self, parent):
        raise NotImplementedError("create_widget")


    def get_value_from(self, widget):
        raise NotImplementedError("get_value_from")


class LineTextField(BaseInputField):


    def create_widget(self, parent):
        widget = QLineEdit(parent)
        if self.initial:
            widget.setText(self.initial)
        return widget


    def get_value_from(self, widget):
        return widget.text()


class IntField(LineTextField):

    def create_widget(self, parent):
        widget = QLineEdit(parent)
        widget.setValidator(QIntValidator(widget))
        if self.initial:
            widget.setText(str(self.initial))
        return widget


    def get_value_from(self, widget):
        return locale.atoi(widget.text())
