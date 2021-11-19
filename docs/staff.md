# Class: Staff
### Staff(time_signature=(4,4), beats=0, bars=0, bpm=120, fps=24)
> module: staff.py
> Inherits: PySide6.QtCore.QObject

[Back Home](index.md)

***

## Signals
> Staff.widthChanged(float(width in pixels))
>
> Staff.timeSignatureChanged(tuple)
>
> Staff.bpmChanged(float)
>
> Staff.quantizeChanged(object)
>
> Staff.changed()

### Usage
```python
staff = Staff()

def userFunction(width):
  print(width)

staff.widthChanged.connect(userFunction)
staff.beats += 4
```

Text can be **bold**, _italic_, ~~strikethrough~~ or `keyword`.
