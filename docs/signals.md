---
layout: default
title: Signals
nav_order: 4
---

# Signals

DawTools uses PySide Signals to maintain consistency across development.

Any class that has Signals functions pretty much like any other PySide or PyQt object with signals.

You can use the .connect() and .disconnect() methods to add callbacks to a signal.

### Signal Usage
```python
staff = DStaff()

def userFunction(width):
  print(width)

staff.widthChanged.connect(userFunction)
staff.beats += 4

# >>> 200.0
```

Find out more @ [PySide6.QtCore.QObject](https://doc.qt.io/qtforpython/PySide6/QtCore/QObject.html?highlight=qobject#PySide6.QtCore.PySide6.QtCore.QObject)
