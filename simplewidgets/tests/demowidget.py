from __future__ import unicode_literals
from simplewidgets.simplewidget import SimpleWidget
from simplewidgets.fields import InnerWidget
from simplewidgets.PyQt.QtGui import QWidget
from simplewidgets.fields import LineTextField, IntField, ChoiceField, Button
from simplewidgets.simplewidget import BaseSimpleWidget


class GroupData(SimpleWidget):

    age = IntField(30, label="Age")
    sex = ChoiceField([(0, "Male"), (1, "Female")], initial=1, label="Sex")
    education = ChoiceField(["Undergrad", "Grad"], initial="Grad", label="Education")


class DemoWidget(QWidget, BaseSimpleWidget):

    full_name = LineTextField(label="Name")
    profile = InnerWidget(GroupData)
    dynamic = ChoiceField("dynamic_choices", label="Dynamic")
    apply = Button("Apply", "apply_")


    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._dynamic_choices = ["A", "B", "C"]
        self.setup_ui()


    @property
    def dynamic_choices(self):
        return self._dynamic_choices


    @dynamic_choices.setter
    def dynamic_choices(self, choices):
        self._dynamic_choices = choices


    def apply_(self):
        pass