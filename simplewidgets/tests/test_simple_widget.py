from PySide.QtCore import Qt

from simplewidgets.fields import LineTextField, IntField, ChoiceField
from simplewidgets.simple_widget import SimpleWidget, SimpleDialog
from mock import Mock


class DemoObject(object):

    def __init__(self):
        self.name = "Bates"
        self.age = 32
        self.sex = "Male"
        self.dynamic = 0


class DemoWidget(SimpleWidget):

    name = LineTextField(label="Name")
    age = IntField(30, label="Age")
    sex = ChoiceField(["Male", "Female"], initial="Female", label="Sex")
    dynamic = ChoiceField("dynamic_choices", label="Dynamic")


    def __init__(self):
        self.dynamic_choices = range(10)
        super(DemoWidget, self).__init__()


class DemoDialog(SimpleDialog):

    name = LineTextField(label="Name")


class DemoBindWidget(DemoWidget):

    name = LineTextField(label="Name")


    def set_data(self, data):
        self.bind_data("name", data, "name")




def test_simple_widget(qtbot):
    widget = DemoWidget()
    qtbot.addWidget(widget)
    widget.show()
    qtbot.keyClicks(widget.name_widget, "John")
    widget.age_widget.clear()
    qtbot.keyClicks(widget.age_widget, "45")
    data = widget.get_data()
    assert data[0] == "John"
    assert data.age == 45
    assert data.sex == "Female"
    assert data.dynamic == "0"
    widget.dynamic_choices = range(10, 20)
    widget.update_view()
    data = widget.get_data()
    assert data.dynamic == "10"


def test_simple_dialog(qtbot):
    widget = DemoDialog()
    widget.accept = Mock()
    widget.reject = Mock()
    qtbot.addWidget(widget)
    widget.show()
    qtbot.keyClick(widget, Qt.Key_Enter)
    assert widget.accept.called
    widget.show()
    qtbot.keyClick(widget, Qt.Key_Escape)
    assert widget.reject.called


def  test_bind_data(qtbot):
    widget = DemoBindWidget()
    demo_object = DemoObject()
    widget.set_data(demo_object)
    qtbot.addWidget(widget)
    widget.show()
    qtbot.keyClicks(widget.get_field_widget("name"), "John Doe")
    qtbot.keyClick(widget.get_field_widget("name"), Qt.Key_Enter)
    assert demo_object.name == "John Doe"

