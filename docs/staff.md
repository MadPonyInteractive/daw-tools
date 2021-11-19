# Class: Staff
### Staff(time_signature=(4,4), beats=0, bars=0, bpm=120, fps=24)
#### Inherits: PySide6.QtCore.QObject

***
[Back Home](index.md)

***

## Signals
Staff.widthChanged(float(width in pixels))

Staff.timeSignatureChanged(tuple)

Staff.bpmChanged(float)

Staff.quantizeChanged(object)

Staff.changed()

### Usage
```python
staff = Staff()

def userFunction(width):
  print(width)

staff.widthChanged.connect(userFunction)
```


