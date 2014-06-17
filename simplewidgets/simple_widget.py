from collections import namedtuple, OrderedDict
import warnings
from simplewidgets.PyQt import QtGui, QtCore
from simplewidgets.fields import BaseInputField


class BaseSimpleWidget(object):

    NUM_LAYOUT_COLS = 2

    def __init__(self):
        self._fields = OrderedDict()
        fields_order = []
        #TODO: create Fields declared in base classes
        for attr_name, value in self.__class__.__dict__.items():
            if isinstance(value, BaseInputField):
                fields_order.append((value.order, attr_name, value))
                self._check_base_attributes_override(attr_name)
        for _, field_name, field in sorted(fields_order):
            self._fields[field_name] = field.create_copy(self)
        # Preserve the order in which Fields were declared
        self._layout = None
        self._field_widgets = {}
        self._data_type = namedtuple("SimpleData", self._fields.keys())
        self.build_widget()


    def fields(self):
        return self._fields.values()


    def build_widget(self, parent=None):
        self._layout = QtGui.QGridLayout(self)
        for field_name in self._fields:
            self._create_field_line(field_name)


    def _create_field_line(self, field_name):
        field = self._fields[field_name]
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
        for field_name in self._fields:
            field = getattr(self, field_name)
            widget = self._field_widgets[field_name]
            field_values[field_name] = field.get_value_from(widget)
        return self._data_type(**field_values)


    def update_view(self):
        for field in self.fields():
            field.update_view()


    def get_field_widget(self, attr_name):
        #TODO: fix protected access
        return self._fields[attr_name]._widget


    def bind_data(self, field_name, instance, attr_name):
        self._fields[field_name].bind_attribute(instance, attr_name)


    def _check_base_attributes_override(self, attr_name):
        """
        Check if a Field declaration is overriding some base class attribute (It's common to declare a `size`
        field which override `QWidget.size` function)

        :param attr_name: the field name
        """
        for base_class in self.__class__.__bases__:
            if hasattr(base_class, attr_name):
                warnings.warn("Field {0} is overwriting attribute from {1}".format(attr_name, base_class.__name__))


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
        self.connect(self.button_box, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(self.button_box, QtCore.SIGNAL("rejected()"), self.reject)


    def exec_accepted(self):
        return self.exec_() == QtGui.QDialog.Accepted
