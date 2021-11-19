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

***

### Staff.setBpm(bpm)

* Parameters

  * **bpm** - `float or int`

Sets the staff BPM

***

### Staff.bpm()

* Return type

  * `float or int`

Returns current BPM

***

### Staff.setTimeSignature(time_sig)

* Parameters

  * **time_sig** - `tuple or string`

Sets the time signature (beats per bar, beat duration)

```python
Staff.setTimeSignature('4/4')
# or
Staff.setTimeSignature(4,4)
```

***

### Staff.timeSignature(asString=False)

* Parameters

  * **asString** - `boolean`

* Return type

  * `tuple or string`

Returns current time signature as tuple or as string if True is passed

***

### Staff.setBeatsPerBar(bpb)

* Parameters

  * **bpb** - `int`

Sets the time signature beats per bar

***

### Staff.beatsPerBar()

* Return type
  * `int`

Returns the time signature beats per bar

***

### Staff.setBeatDuration(bd)

* Parameters

  * **bd** - `int`

Sets the time signature beats duration

***

### Staff.beatDuration()

* Return type

  * `int`

Returns the time signature beats duration

***

### Staff.setPps(pps)

* Parameters

  * **pps** - `float or int`

Sets pixels per second

This can be used for zooming but you probably wont need it

***

### Staff.pps()

* Return type

  * `float or int`

Returns pixels per second (how many pixels in 1 second)

***

### Staff.width()

* Return type

  * `float`

Returns how many pixels in the whole staff

***

### Staff.seconds()

* Return type

  * `float`

Returns how many seconds in staff

***

### Staff.setFps(fps)

* Parameters

  * **fps** - `int`

Sets the Frames per second

***

### Staff.fps()

* Return type

  * `int`

Returns frames per second

***

### Staff.frames()

* Return type

  * `int`

Returns how many frames in staff

## Inner Classes

***




Text can be **bold**, _italic_, ~~strikethrough~~ or `keyword`.
