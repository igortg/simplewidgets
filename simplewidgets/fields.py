from simplewidgets.PyQt import QtCore
import locale
import weakref
from simplewidgets.PyQt.QtGui import QLineEdit, QIntValidator, QComboBox


class BaseInputField(object):

    # _coubter is a global counter so UI fields could be created in the same order of their declarations
    # ref: http://stackoverflow.com/a/11317693/885117
    _counter = 0

    def __init__(self, initial="", label=""):
        self.order = self._counter
        BaseInputField._counter += 1
        self.label = label
        self.initial = initial
        self.simple_widget = None
        self._widget = None
        self._bindings = weakref.WeakKeyDictionary()


    def create_widget(self, parent):
        """
        Create the widget for this Field.

        :param QWidget parent: the parent widget

        :rtype: QWidget
        """
        raise NotImplementedError("create_widget")


    def update_view(self):
        """
        Update the widget contents with data

        :param data:
        """
        raise NotImplementedError("update_view")


    def get_value_from(self):
        """
        Get a data value from the given widget.
        """
        raise NotImplementedError("get_value_from")


    def bind_attribute(self, instance, attr_name):
        self._bindings[instance] = attr_name


    def create_copy(self, simple_widget):
        """
        BaseInputFields are always defined in the class level. This method is called to create a unique instance of
        the BaseInputField to each instance of a SimpleWidget.

        :param SimpleWidget simple_widget: the simple widget instance

        :rtype: BaseInputField
        """
        import copy
        field_instance = copy.copy(self)
        field_instance.simple_widget = weakref.proxy(simple_widget)
        return field_instance



class LineTextField(BaseInputField):


    def create_widget(self, parent):
        assert self._widget is None, "create_widget() must be called only once"
        self._widget = QLineEdit(parent)
        self._widget.setText(self.initial)
        parent.connect(self._widget, QtCore.SIGNAL("editingFinished ()"), self.on_editing_finished)
        return self._widget


    def update_view(self):
        pass


    def get_value_from(self):
        return self._widget.text()


    def on_editing_finished(self):
        for instance, attr_name in self._bindings.items():
            setattr(instance, attr_name, self._widget.text())


class IntField(LineTextField):

    def create_widget(self, parent):
        self._widget = widget = QLineEdit(parent)
        widget.setValidator(QIntValidator(widget))
        self._widget.setText(str(self.initial))
        return widget


    def update_view(self):
        pass


    def get_value_from(self):
        return locale.atoi(self._widget.text())


class ChoiceField(BaseInputField):
    """
    A SimpleWidget field that displays a Combo with the given choices
    """


    def __init__(self, choices, initial="", label=""):
        super(ChoiceField, self).__init__(initial, label)
        self._choices = choices


    def create_widget(self, parent):
        self._widget = QComboBox(parent)
        self.update_view()
        return self._widget


    def update_view(self):
        choices = self._get_choices()
        self._widget.clear()
        self._widget.addItems([choice[1] for choice in choices])
        if self.initial:
            values = [choice[0] for choice in choices]
            self._widget.setCurrentIndex(values.index(self.initial))


    def get_value_from(self):
        current_text = self._widget.currentText()
        for choice_value, text in self._get_choices():
            if current_text == text:
                return choice_value


    def _get_choices(self):
        """
        Returns the field choices as a list of tuples (choice_value, choice_text).

        :rtype: list
        """
        if isinstance(self._choices, str):
            choices = getattr(self.simple_widget, self._choices)
        else:
            choices = self._choices
        assert isinstance(choices, (list, tuple)), "choices has an invalid type"
        for i, choice in enumerate(choices):
            if not isinstance(choice, (list, tuple)):
                choices[i] = (choice, str(choice))
        return choices
