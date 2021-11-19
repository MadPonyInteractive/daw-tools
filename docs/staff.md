# Class: Staff
### Staff(time_signature=(4,4), beats=0, bars=0, bpm=120, fps=24)
> Module: staff.py
>
> Inherits: _PySide6.QtCore.QObject_

[Back Home](index.md)

***

## Signals
> Staff.widthChanged(float(width in pixels))
>
> Staff.timeSignatureChanged(tuple(BeatsPerBar, BeatDuration))
>
> Staff.bpmChanged(float(BPM))
>
> Staff.quantizeChanged(object(Quantize Inner Class))
>
> Staff.changed()

### Signal Usage
```python
staff = Staff()

def userFunction(width):
  print(width)

staff.widthChanged.connect(userFunction)
staff.beats += 4

>>> 200.0
```

***

## Methods

### Staff.setBpm(bpm)

  * Parameters

    * **bpm** - _float or int_

    `Sets the staff BPM`

### Staff.bpm()

  * Return type

  _float or int_

  `Returns current BPM`

### Staff.setTimeSignature(time_sig)

  * Parameters

    **time_sig** - _tuple or string_

  `Sets the time signature`

```python
Staff.setTimeSignature('4/4')
# or
Staff.setTimeSignature(4,4)
```

### Staff.timeSignature(asString=False)

  * Parameters
    * **asString** - _boolean_

  * Return type
    * _tuple or string_

  `Returns current time signature as tuple or as string if True is passed`

### Staff.setBeatsPerBar()

  * Parameters


  * Return type


### Staff.beatsPerBar()

  * Parameters


  * Return type


### Staff.setBeatDuration()

  * Parameters


  * Return type


### Staff.beatDuration()

  * Parameters


  * Return type


### Staff.setPps()

  * Parameters


  * Return type


### Staff.pps()

  * Parameters


  * Return type


### Staff.width()

  * Parameters


  * Return type


### Staff.seconds()

  * Parameters


  * Return type


### Staff.setFps()

  * Parameters


  * Return type


### Staff.fps()

  * Parameters


  * Return type


### Staff.frames()

  * Parameters


  * Return type






Text can be **bold**, _italic_, ~~strikethrough~~ or `keyword`.
