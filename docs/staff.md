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

***

## Inner Classes

The Staff class has several inner classes that provide a consistent way to access their parameters

***

## Staff.Beats

Calling this inner class will return the full amount of beats in the staff

```python
staff = Staff(beats=4)

print(staff.beats())
>>> 4
```

You can add or remove beats using the following methods

```python
staff = Staff(beats=4)

staff.beats+=2
print(staff.beats())
>>> 6

staff.beats.add(2)
print(staff.beats())
>>> 8

staff.beats-=2
print(staff.beats())
>>> 6

staff.beats.remove(2)
print(staff.beats())
>>> 4
```

You can also use the .clear() and .set() methods

```python
staff = Staff()

print(staff.beats.set(4))
print(staff.beats())
>>> 4

print(staff.beats.clear())
print(staff.beats())
>>> 0
```

The .extra() method will return any extra beats that don't fit in the current bars

```python
staff = Staff(bars=1,beats=5)

print(staff.beats())
>>> 9
print(staff.bars())
>>>2
print(staff.beats.extra())
>>> 1
```

Notice in the example above that we added 1 bar and 5 beats on initialization.

Because the staff default time signature is 4/4, 1 bar contains 4 beats.

So (1 bar = 4 beats) + 5 beats = 2 bars and 9 beats in staff, leaving 1 extra beat.

* Listing Beats and Bars

Both the Staff.Beats and the Staff.Bars inner classes have a handy iterator for retrieving pixel positions.

```python
staff = Staff(bars=2)

print(list(staff.beats))
>>> [Decimal('0.0'), Decimal('50.0'), Decimal('100.0'), Decimal('150.0'), Decimal('200.0'), Decimal('250.0'), Decimal('300.0'), Decimal('350.0')]

print(list(staff.bars))
>>> [Decimal('0.0'), Decimal('200.0')]
```

Notice the retrieved values are in a decimal format for high float precision.

This is very useful for placing measurement lines and positioning items on a UI.

***

## Staff.Bars

This inner class has the same methods as the Staff.Beats class 

with the exception of the .extra() method for beats.

***



Text can be **bold**, _italic_, ~~strikethrough~~ or `keyword`.
