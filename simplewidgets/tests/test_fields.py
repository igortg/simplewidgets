from simplewidgets.fields import IntField, ChoiceField
from simplewidgets.simple_widget import SimpleWidget


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



def test_field_copy():
    field = IntField("initial", "label")
    clone = field.create_copy(SimpleWidget())
    assert clone.initial == field.initial
    assert clone.label == field.label
