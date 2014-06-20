SimpleWidgets
=============

Rapidly build GUI with Python and Qt

### Simple Example

The above code construct a dialog, waits for the user input and return window contents in a `namedtuple`.

```python
from PySide.QtGui import QApplication
from simplewidgets.fields import LineTextField, IntField, ChoiceField
from simplewidgets.simple_widget import SimpleDialog

class DemoDialog(SimpleDialog):
    name = LineTextField(label="Name")
    age = IntField(30, label="Age")
    sex = ChoiceField(["Male", "Female"], initial="Female", label="Sex")

app = QApplication([])
demo = DemoDialog()
if demo.exec_accepted():
    data = demo.get_data()
```
      
![Simple Example](doc/simple-example.png)

    print data
    >> SimpleData(name=u'', age=30, sex='Female')


[![Build Status](https://travis-ci.org/itghisi/simplewidgets.svg?branch=master)](https://travis-ci.org/itghisi/simplewidgets)

