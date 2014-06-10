from collections import namedtuple
from PySide import QtGui
from PySide.QtCore import Qt, SIGNAL
from simplewidgets.fields import BaseInputField


class BaseSimpleWidget(object):

    NUM_LAYOUT_COLS = 2

    def __init__(self):
        fields = []
        for attr_name, value in self.__class__.__dict__.items():
            if isinstance(value, BaseInputField):
                fields.append((value.order, attr_name))
                setattr(self, attr_name, value.create_copy(self))
        # Preserve the order in which Fields were declared
        self._sorted_field_names = [attr_name for _, attr_name in sorted(fields)]
        self._layout = None
        self._field_widgets = {}
        self._data_type = namedtuple("SimpleData", self._sorted_field_names)
        self.build_widget()


    def fields(self):
        return [getattr(self, field_name) for field_name in self._sorted_field_names]


    def build_widget(self, parent=None):
        self._layout = QtGui.QGridLayout(self)
        for field_name in self._sorted_field_names:
            self._create_field_line(field_name)


    def _create_field_line(self, field_name):
        field = getattr(self, field_name)
        label = QtGui.QLabel(self)
        label.setText(field.label)
        setattr(self, "{0}_label".format(field_name), label)
        row = self._layout.rowCount() + 1
        self._layout.addWidget(label, row, 0)
        widget = field.create_widget(self)
        self._layout.addWidget(widget, row, 1)
        setattr(self, "{0}_widget".format(field_name), widget)
        self._field_widgets[field_name] = widget


    def get_data(self):
        field_values = {}
        for field_name in self._sorted_field_names:
            field = getattr(self, field_name)
            widget = self._field_widgets[field_name]
            field_values[field_name] = field.get_value_from(widget)
        return self._data_type(**field_values)


    def update_view(self):
        for field in self.fields():
            field.update_view()


class SimpleWidget(BaseSimpleWidget, QtGui.QWidget):


    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        BaseSimpleWidget.__init__(self)


class SimpleDialog(BaseSimpleWidget, QtGui.QDialog):


    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        BaseSimpleWidget.__init__(self)


    def build_widget(self, parent=None):
        super(SimpleDialog, self).build_widget(parent)
        QDialogButtonBox = QtGui.QDialogButtonBox
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self._layout.addWidget(self.button_box, self._layout.rowCount() + 1, 0, 1, self.NUM_LAYOUT_COLS)
        self.connect(self.button_box, SIGNAL("accepted()"), self.accept)
        self.connect(self.button_box, SIGNAL("rejected()"), self.reject)


    def exec_accepted(self):
        return self.exec_() == QtGui.QDialog.Accepted
