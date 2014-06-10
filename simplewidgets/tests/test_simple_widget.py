from PySide.QtCore import Qt

from simplewidgets.fields import LineTextField, IntField, ChoiceField
from simplewidgets.simple_widget import SimpleWidget, SimpleDialog
from mock import Mock


class DemoWidget(SimpleWidget):

    name = LineTextField(label="Name")
    age = IntField(30, label="Age")
    sex = ChoiceField(["Male", "Female"], initial="Female", label="Sex")
    dynamic = ChoiceField("dynamic_choices", label="Dynamic")


    def __init__(self):
        super(DemoWidget, self).__init__()
        self.dynamic_choices = range(10)



class DemoDialog(SimpleDialog):

    name = LineTextField(label="Name")


def test_simple_widget(qtbot):
    demo = DemoWidget()
    widget = demo.build_widget()
    qtbot.addWidget(widget)
    widget.show()
    qtbot.keyClicks(widget.name_widget, "John")
    widget.age_widget.clear()
    qtbot.keyClicks(widget.age_widget, "45")
    data = demo.get_data()
    assert data[0] == "John"
    assert data.age == 45
    assert data.sex == "Female"
    assert data.dynamic == "0"
    demo.dynamic_choices = range(10, 20)
    demo.update_view()
    data = demo.get_data()
    assert data.dynamic == "10"


def test_simple_dialog(qtbot):
    demo = DemoDialog()
    widget = demo.build_widget()
    widget.accept = Mock()
    widget.reject = Mock()
    qtbot.addWidget(widget)
    widget.show()
    qtbot.keyClick(widget, Qt.Key_Enter)
    assert widget.accept.called
    widget.show()
    qtbot.keyClick(widget, Qt.Key_Escape)
    assert widget.reject.called
