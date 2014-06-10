from simplewidgets.fields import IntField
from simplewidgets.simple_widget import SimpleWidget


def test_field_copy():
    field = IntField("initial", "label")
    clone = field.create_copy(SimpleWidget())
    assert clone.initial == field.initial
    assert clone.label == field.label