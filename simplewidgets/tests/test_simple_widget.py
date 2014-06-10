from PySide.QtCore import Qt
from simplewidgets.fields import LineTextField, IntField
from simplewidgets.simple_widget import SimpleWidget, SimpleDialog
from mock import Mock


class BaseDemoWidget:

    name = LineTextField(label="Name")
    age = IntField(30, label="Age")


class DemoWidget(BaseDemoWidget, SimpleWidget):
    pass


class DemoDialog(BaseDemoWidget, SimpleDialog):
    pass


def test_simple_widget(qtbot):
    demo = DemoWidget()
    widget = demo.build_widget()
    qtbot.addWidget(widget)
    widget.show()
    qtbot.keyClicks(widget.name_widget, "John")
    widget.age_widget.clear()
    qtbot.keyClicks(widget.age_widget, "45")
    data = demo.get_data()
    assert data.name == "John"
    assert data.age == 45


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