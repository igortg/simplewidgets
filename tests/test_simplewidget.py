from __future__ import unicode_literals
from simplewidgets.PyQt.QtCore import Qt
from simplewidgets.fields import LineTextField
from simplewidgets.simplewidget import SimpleDialog
from demowidget import DemoWidget


class DemoObject(object):
    def __init__(self):
        self.name = "Bates"
        self.age = 32
        self.sex = "Male"
        self.dynamic = 0


class DemoDialog(SimpleDialog):
    full_name = LineTextField(label="Name")


class DemoBindWidget(DemoWidget):
    full_name = LineTextField(label="Name")


    def set_data(self, data):
        self.bind_data("full_name", data, "name")


def test_simple_widget(qtbot):
    widget = DemoWidget()
    qtbot.addWidget(widget)
    widget.show()
    qtbot.keyClicks(widget.full_name_widget, "John")
    age_widget = widget.profile.child_widget.age.widget
    age_widget.clear()
    qtbot.keyClicks(age_widget, "45")
    data = widget.get_data()
    assert data[0] == "John"
    assert data.profile.age == 45
    assert data.profile.sex == 1
    assert data.dynamic == "A"
    widget.dynamic_choices = ["D", "E", "F"]
    widget.update_view()
    data = widget.get_data()
    assert data.dynamic == "D"


def test_simple_dialog(qtbot):
    widget = DemoDialog()
    qtbot.addWidget(widget)
    widget.show()
    qtbot.keyClick(widget, Qt.Key_Enter)
    assert widget.result() == widget.Accepted
    widget.show()
    qtbot.keyClick(widget, Qt.Key_Escape)
    assert widget.result() == widget.Rejected


def test_bind_data(qtbot):
    widget = DemoBindWidget()
    demo_object = DemoObject()
    widget.set_data(demo_object)
    qtbot.addWidget(widget)
    widget.show()
    qtbot.keyClicks(widget.full_name.widget, "John Doe")
    qtbot.keyClick(widget.full_name.widget, Qt.Key_Enter)
    assert demo_object.name == "John Doe"


def test_initial_values(qtbot):
    widget = DemoDialog()
    widget.full_name.set_value("Test name")
    widget.show()
    assert widget.full_name.widget.text() == "Test name"
