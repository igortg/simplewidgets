from collections import namedtuple
from PySide import QtGui
from PySide.QtCore import Qt, SIGNAL
from simplewidgets.fields import BaseInputField


class _SimpleWidgetMeta(type):

    def __new__(mcs, name, bases, class_dict):
        fields = []
        full_dict = {}
        full_dict.update(class_dict)
        for base in bases:
            full_dict.update(base.__dict__)
        for attr_name, value in full_dict.items():
            if isinstance(value, BaseInputField):
                fields.append((value.order, attr_name))
        class_dict["_ui_fields"] = [field_name for _, field_name in sorted(fields)]
        return type.__new__(mcs, name, bases, class_dict)


class SimpleWidget(object):

    __metaclass__ = _SimpleWidgetMeta

    NUM_LAYOUT_COLS = 2

    def __init__(self):
        self._layout = None
        for field_name in self._ui_fields:
            field = getattr(self, field_name)
            setattr(self, field_name, field.create_copy(self))
        self._field_widgets = {}
        self._data_type = namedtuple("SimpleData", self._ui_fields)


    def fields(self):
        return [getattr(self, field_name) for field_name in self._ui_fields]


    def _instancialize_widget(self, parent):
        return QtGui.QWidget(parent)


    def build_widget(self, parent=None):
        widget = self._instancialize_widget(parent)
        self._layout = QtGui.QGridLayout(widget)
        for field_name in self._ui_fields:
            self._create_field_line(widget, field_name)
        return widget


    def _create_field_line(self, parent, field_name):
        field = getattr(self, field_name)
        label = QtGui.QLabel(parent)
        label.setText(field.label)
        setattr(parent, "{0}_label".format(field_name), label)
        row = self._layout.rowCount() + 1
        self._layout.addWidget(label, row, 0)
        widget = field.create_widget(parent)
        self._layout.addWidget(widget, row, 1)
        setattr(parent, "{0}_widget".format(field_name), widget)
        self._field_widgets[field_name] = widget


    def get_data(self):
        field_values = {}
        for field_name in self._ui_fields:
            field = getattr(self, field_name)
            widget = self._field_widgets[field_name]
            field_values[field_name] = field.get_value_from(widget)
        return self._data_type(**field_values)


    def update_view(self):
        for field in self.fields():
            field.update_view()


class SimpleDialog(SimpleWidget):


    def _instancialize_widget(self, parent):
        return QtGui.QDialog(parent)


    def build_widget(self, parent=None):
        QDialogButtonBox = QtGui.QDialogButtonBox
        widget = super(SimpleDialog, self).build_widget(parent)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, widget)
        self._layout.addWidget(self.button_box, self._layout.rowCount() + 1, 0, 1, self.NUM_LAYOUT_COLS)
        widget.connect(self.button_box, SIGNAL("accepted()"), widget.accept)
        widget.connect(self.button_box, SIGNAL("rejected()"), widget.reject)
        return widget


    def exec_accepted(self, parent=None):
        widget = self.build_widget(parent)
        return widget.exec_() == QtGui.QDialog.Accepted
