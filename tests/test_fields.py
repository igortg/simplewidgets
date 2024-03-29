import pytest
from unittest import mock
import locale
from simplewidgets.PyQt.QtCore import Qt
from simplewidgets.fields import IntField, ChoiceField, NumberField, InnerWidget, Button
from simplewidgets.simplewidget import SimpleWidget
from demowidget import DemoWidget


def test_choice_field(qtbot):
    field = ChoiceField([(0xF, "0F"), (0x10, "10")], initial=0xF)
    combo = field.create_widget(None)
    qtbot.addWidget(combo)
    combo.show()
    assert "0F" == combo.itemText(0)
    assert "10" == combo.itemText(1)
    assert field.get_value_from() == 0xF
    combo.setCurrentIndex(1)
    assert field.get_value_from() == 0x10


def test_int_field(qtbot):
    change_mock = mock.Mock()

    def int_changed():
        change_mock()

    field = IntField(10)
    field.on_editing_finished.attach(int_changed)
    widget = field.create_widget(None)
    qtbot.addWidget(widget)
    widget.show()
    qtbot.keyClicks(widget, "20")
    qtbot.keyClick(widget, Qt.Key_Return)
    change_mock.assert_called_once_with()


def test_float_field(qtbot):
    field = NumberField(23.2, display_format="%.2f")
    widget = field.create_widget(None)
    assert widget.text() == "23.20"
    widget.clear()
    qtbot.keyClicks(widget, "13.4")
    qtbot.keyClick(widget, Qt.Key_Return)
    assert field.get_value_from() == 13.4


def test_group_field(qtbot):
    field = InnerWidget(DemoWidget)
    widget = field.create_widget(None)
    widget.show()
    data = field.get_value_from()
    assert isinstance(data, tuple)
    assert len(data) == 3


def test_button(qtbot):
    slot = mock.Mock()
    control = Button("Apply", slot)
    widget = control.create_widget(None)
    widget.show()
    qtbot.mouseClick(widget, Qt.LeftButton)
    slot.assert_called_with()


def has_locale(loc):
    original = locale.getlocale()
    try:
        locale.setlocale(locale.LC_ALL, loc)
        return  True
    except locale.Error:
        return False
    finally:
        locale.setlocale(locale.LC_ALL, original)


@pytest.mark.skipif("not has_locale('Portuguese_Brazil.1252')")
def test_float_field_i18n(qtbot):
    original = locale.getlocale()
    locale.setlocale(locale.LC_ALL, "Portuguese_Brazil.1252")
    try:
        field = NumberField(23.2, display_format="%.2f")
        widget = field.create_widget(None)
        assert widget.text() == "23,20"
        widget.clear()
        qtbot.keyClicks(widget, "13,4")
        qtbot.keyClick(widget, Qt.Key_Return)
        assert field.get_value_from() == 13.4
    finally:
        locale.setlocale(locale.LC_ALL, original)




def test_field_copy():
    field = IntField("initial", "label")
    clone = field.create_copy(SimpleWidget())
    assert clone.initial == field.initial
    assert clone.label == field.label
