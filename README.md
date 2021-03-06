SimpleWidgets
=============

Rapidly build GUI with Python and Qt

### Simple Example

The above code construct a dialog, waits for the user input and return window contents in a `namedtuple`.

```python
from PyQt4.QtGui import QApplication
from simplewidgets.fields import LineTextField, IntField, ChoiceField
from simplewidgets.simplewidget import SimpleDialog

class DemoDialog(SimpleDialog):
    name = LineTextField(label="Name")
    age = IntField(30, label="Age")
    gender = ChoiceField(["Male", "Female"], initial="Female", label="Gender")

app = QApplication([])
demo = DemoDialog()
if demo.exec_accepted():
    data = demo.get_data()
```
      
![Simple Example](doc/simple-example.png)

    print data
    >> SimpleData(name=u'', age=30, gender='Female')


[![Build Status](https://travis-ci.org/igortg/simplewidgets.svg?branch=master)](https://travis-ci.org/igortg/simplewidgets)

