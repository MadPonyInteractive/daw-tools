---
layout: default
title: DStaff
parent: staff.py
grand_parent: Modules
nav_order: 1
---

# DawTools.DStaff

The [DStaff](staff.html#class-dawtoolsdstaff) class provides a surface to manage musical timing. [More...](staff.html#detailed-description)

| Inheritance            |                 |
|:-----------------------|:----------------|
| [PySide6.QtCore.QObject](https://doc.qt.io/qtforpython/PySide6/QtCore/QObject.html?highlight=qobject#PySide6.QtCore.PySide6.QtCore.QObject) | DawTools.DStaff |


***

| Functions |
|:----------|
|def [setBpm(bpm)](staff.html#dawtoolsdstaffsetbpmbpm)|
|def [bpm()](staff.html#dawtoolsdstaffbpm)|
|def [setTimeSignature()](staff.html#dawtoolsdstaffsettimesignaturetime_sig)|
|def [timeSignature()](staff.html#dawtoolsdstafftimesignatureasstringfalse)|
|def [setBeatsPerBar()](staff.html#dawtoolsdstaffsetbeatsperbarbpb)|
|def [beatsPerBar()](staff.html#dawtoolsdstaffbeatsperbar)|
|def [setBeatDuration()](staff.html#dawtoolsdstaffsetbeatdurationbd)|
|def [beatDuration()](staff.html#dawtoolsdstaffbeatduration)|
|def [setPps()](staff.html#dawtoolsdstaffsetppspps)|
|def [pps()](staff.html#dawtoolsdstaffpps)|
|def [width()](staff.html#dawtoolsdstaffwidth)|
|def [seconds()](staff.html#dawtoolsdstaffseconds)|
|def [setFps()](staff.html#dawtoolsdstaffsetfpsfps)|
|def [fps()](staff.html#dawtoolsdstafffps)|
|def [frames()](staff.html#dawtoolsdstaffframes)|

| Inner Classes |
|:--------------|
|class [DStaff.Quantize](staff.html#inner-class-dawtoolsdstaffquantize)|
|class [DStaff.Beats](staff.html#inner-class-dawtoolsdstaffbeats)|
|class [DStaff.Bars](staff.html#inner-class-dawtoolsdstaffbars)|
|class [DStaff.Beat](staff.html#inner-class-dawtoolsdstaffbeat)|
|class [DStaff.Bar](staff.html#inner-class-dawtoolsdstaffbar)|
|class [DStaff.Frame](staff.html#inner-class-dawtoolsdstaffframe)|
|class [DStaff.Sample](staff.html#inner-class-dawtoolsdstaffsample)|
|class [DStaff.WholeNote](staff.html#inner-class-dawtoolsdstaffwholenote)|

| Signals | Return |
|:--------|:-------|
|widthChanged()| float( Staff width in pixels )|
|timeSignatureChanged()| tuple(int(left_divisor), int(right_divisor)) |
|bpmChanged()| float(bpm)|
|quantizeChanged()| object(DStaff.Quantize) |
|changed()| None|

[More on signals](/signals.html)

## Detailed Description

DawTools is a music based project and as such, several of its widgets and classes
depend heavily on musical timing calculations.

The DawTools.DStaff class aims to facilitate a structure that takes care of musical unit
calculations such as beats per minute (BPM), frames per second (FPS), pixels per second or
how many pixels should represent a second (PPS), samples (hertz) how many samples should
be in 1 second, how long is a whole note, time signature, etc...

All widgets and classes that need some sort of timing depend on this class for their calculations.

In most projects you will only need 1 instance of this class and then pass it to any dependent
classes or widgets. Then by changing this class settings , all connected widgets will respond
appropriately.

In a big project like a digital audio workstation (daw) for example, you may need several instances.
Perhaps you will have the track timeline/viewport independent of the piano roll. Or you
might need a separate staff for a sequencer.


***

### class DawTools.DStaff()
* Parameters

  * **time_signature** - `tuple or string` -> default = (4,4) '4/4'
  * **beats** - `int` -> default = 0
  * **bars** - `int` -> default = 0
  * **bpm** - `float or int` -> default = 120
  * **fps** - `int` -> default = 24

Constructs a DStaff object.

***

### DawTools.DStaff.setBpm(bpm)
* Parameters

  * **bpm** - `float or int`

Sets the staff BPM

***

### DawTools.DStaff.bpm()
* Return type

  * `float or int`

Returns current BPM

***

### DawTools.DStaff.setTimeSignature(time_sig)
* Parameters

  * **time_sig** - `tuple or string`

Sets the time signature (beats per bar, beat duration)

```python
DawTools.DStaff.setTimeSignature('4/4')
# or
DawTools.DStaff.setTimeSignature(4,4)
```

***

### DawTools.DStaff.timeSignature(asString=False)
* Parameters

  * **asString** - `boolean`

* Return type

  * `tuple or string`

Returns current time signature as tuple or as string if True is passed

***

### DawTools.DStaff.setBeatsPerBar(bpb)
* Parameters

  * **bpb** - `int`

Sets the time signature beats per bar

***

### DawTools.DStaff.beatsPerBar()
* Return type
  * `int`

Returns the time signature beats per bar

***

### DawTools.DStaff.setBeatDuration(bd)
* Parameters

  * **bd** - `int`

Sets the time signature beats duration

***

### DawTools.DStaff.beatDuration()
* Return type

  * `int`

Returns the time signature beats duration

***

### DawTools.DStaff.setPps(pps)
* Parameters

  * **pps** - `float or int`

Sets pixels per second

This can be used for zooming but you probably wont need it

***

### DawTools.DStaff.pps()
* Return type

  * `float or int`

Returns pixels per second (how many pixels in 1 second)

***

### DawTools.DStaff.width()
* Return type

  * `float`

Returns how many pixels in the whole staff

***

### DawTools.DStaff.seconds()
* Return type

  * `float`

Returns how many seconds in staff

***

### DawTools.DStaff.setFps(fps)
* Parameters

  * **fps** - `int`

Sets the Frames per second

***

### DawTools.DStaff.fps()
* Return type

  * `int`

Returns frames per second

***

### DawTools.DStaff.frames()
* Return type

  * `int`

Returns how many frames in staff

***

## Inner Class DawTools.DStaff.Beats

| Functions |
|:----------|
| def add()|
| def remove()|
| def clear()|
| def set()|
| def extra()|

***

### Inner Class DawTools.DStaff.Beats()
* Return type

  * `int`

Returns the current amount of beats in staff.

```python
staff = DStaff(beats=4)

print(staff.beats())
# >>> 4
```

***

### Inner Class DawTools.DStaff.Beats
* Return type

  * `iterator`

Returns an iterator with pixel X positions

```python
staff = DStaff(beats=4)

for pixelX in staff.beats:
  print(pixelX)
# >>> 0.0
# >>> 50.0
# >>> 100.0
# >>> 150.0
```

### Usage

You can add or remove beats using the following methods

```python
staff = DStaff(beats=4)

staff.beats+=2
print(staff.beats())
# >>> 6

staff.beats.add(2)
print(staff.beats())
# >>> 8

staff.beats-=2
print(staff.beats())
# >>> 6

staff.beats.remove(2)
print(staff.beats())
# >>> 4
```

You can also use the .clear() and .set() methods

```python
staff = DStaff()

print(staff.beats.set(4))
print(staff.beats())
# >>> 4

print(staff.beats.clear())
print(staff.beats())
# >>> 0
```

The .extra() method will return any extra beats that don't fit in the current bars

```python
staff = DStaff(bars=1,beats=5)

print(staff.beats())
# >>> 9
print(staff.bars())
# >>>2
print(staff.beats.extra())
# >>> 1
```

Notice in the example above that we added 1 bar and 5 beats on initialization.
Because the staff default time signature is 4/4, 1 bar contains 4 beats.

So (1 bar = 4 beats) + 5 beats = 2 bars and 9 beats in staff, leaving 1 extra beat.

### Listing Beats and Bars

Inner Class DawTools.DStaff.Bars and the DawTools.DStaff.Quantize inner classes have a handy iterator for retrieving pixel positions.

```python
staff = DStaff(bars=2)

print(list(staff.beats))
# >>> [Decimal('0.0'), Decimal('50.0'), Decimal('100.0'), Decimal('150.0'), Decimal('200.0'), Decimal('250.0'), Decimal('300.0'), Decimal('350.0')]

print(list(staff.bars))
# >>> [Decimal('0.0'), Decimal('200.0')]
```

Notice the retrieved values are in a decimal format for high float precision.

This is very useful for placing measurement lines and positioning items on a UI.

***

## Inner Class DawTools.DStaff.Bars

This inner class has the same methods and works in the same way as the
[DawTools.DStaff.Beats](staff.html#inner-class-dawtoolsdstaffbeats)
class with the exception of the .extra() method for beats.

| Functions |
|:----------|
| def add()   |
| def remove()|
| def clear()|
| def set()|

***

## Inner Class DawTools.DStaff.Quantize

This inner class is responsible for all the quantization in DawTools.DStaff.

It provides methods to set and retrieve quantization values as well a list of
pixel X positions when iterated.

| Functions |
|:----------|
| def [setValue()](staff.html#dawtoolsdstaffquantizesetvaluevalue)|
| def [value()](staff.html#dawtoolsdstaffquantizevalue)|
| def [setType()](staff.html#dawtoolsdstaffquantizesettype_type)|
| def [type()](staff.html#dawtoolsdstaffquantizetype)|
| def [setTuplet()](staff.html#dawtoolsdstaffquantizesettuplettuplet)|
| def [tuplet()](staff.html#dawtoolsdstaffquantizetuplet)|
| def [setSwingPercent()](staff.html#dawtoolsdstaffquantizesetswingpercentpercent)|
| def [swingPercent()](staff.html#dawtoolsdstaffquantizeswingpercent)|
| def [ms()](staff.html#dawtoolsdstaffquantizems)|
| def [seconds()](staff.html#dawtoolsdstaffquantizeseconds)|
| def [pixels()](staff.html#dawtoolsdstaffquantizepixels)|
| def [frames()](staff.html#dawtoolsdstaffquantizeframes)|
| def [samples()](staff.html#dawtoolsdstaffquantizesamples)|


### Inner Class DawTools.DStaff.Quantize()
* Return type

  * `int`

Returns the current quantize value.

```python
staff = DStaff()

print(staff.quantize())
# >>> 8
```

***

### Inner Class DawTools.DStaff.Quantize
* Return type

  * `iterator`

Returns an iterator with pixel X positions

```python
staff = DStaff(beats=2)

for pixelX in staff.quantize:
  print(pixelX)

# >>> 0.0
# >>> 25.00
# >>> 50.00
# >>> 75.00
# >>> 100.0
```

When called, it retrieves the current quantize value but you can also get it by calling the .value() method.

```python
staff = DStaff(bars=2)

print(staff.quantize())
# >>> 8

staff.quantize.setValue(4)
print(staff.quantize.value())
# >>> 4

print(staff.quantize)
# >>> DawTools.DStaff->Inner Class: Quantize
# >>> Type: Straight
# >>> Value: 1/4
```

Like the DawTools.DStaff.Beat and DawTools.DStaff.Bar the DawTools.DStaffQuantize inner class can also retrieve a list of

pixel position using list(staff.quantize) or simply iterating with a for loop.

```python
staff = DStaff(beats=1)

print(list(staff.quantize))
# >>> [Decimal('0.0'), Decimal('25.00'), Decimal('50.0')]

for pixelXPos in staff.quantize:
  print(pixelXPos)
# >>> 0.0
# >>> 25.00
# >>> 50.0
```

### Tuplets & Swing

Its important to have a clear understanding of how tuplets and swing work in music.

The default quantize type is 'straight' but can easily be changed to 'tuplet' or 'swing' using the .setType() method.

```python
staff = DStaff()

staff.quantize.setType('tuplet')
staff.quantize.setValue(16)

print(staff.quantize)
# >>> DawTools.DStaff->Inner Class: Quantize
# >>> Type: Tuplet
# >>> Value: 1/16
# >>> Tuplet: (3,2)
```

The above is a 1/16 triplet

With the .setTuplet() method you can use triplets (3,2), duplets (2,3), quintuplets (5,4),
sextuplets (6,4), septuplets (7,4), nonuplets (9,8) and other weird tuplets you may fancy.

```python
staff = DStaff()

staff.quantize.setType('tuplet')
staff.quantize.setValue(4)# 1/4
staff.quantize()# 4
staff.quantize.setTuplet(5,4)# A Quintuplet

print(staff.quantize)
# >>> DawTools.DStaff->Inner Class: Quantize
# >>> Type: Tuplet
# >>> Value: 1/4
# >>> Tuplet: (5,4)
```

If you think that was overwhelming, get ready for the swing beast.

Just kidding is not that complicated... not XD

```
A swing with a percentage of 0% works just like a straight quantize
but once we start increasing that percentage things start getting a little funky
as the quantization position starts shifting forward in time, with the first position
moving closer to the next beat and the second further away.
```

For this reason the DawTools.DStaff.Quantize methods(when in swing type) return a tuple
containing the first quantize position and the second position with its distance from the first.

Sounds confusing but once you retrieve a swing list and draw lines on a ui it will all make sense.

```python
staff = DStaff(beats=2)

staff.quantize.setType('swing')
staff.quantize.setValue(4)# 1/4
staff.quantize.setSwingPercent(60)

for pixelXPos in staff.quantize:
  print(pixelXPos)
# >>> 0.0
# >>> 53.33333333333333333333333333
# >>> 100.0

staff.quantize.setSwingPercent(80)
for pixelXPos in staff.quantize:
  print(pixelXPos)
# >>> 0.0
# >>> 59.99999999999999999999999999
# >>> 100.0

print(staff.quantize)
# >>> DawTools.DStaff->Inner Class: Quantize
# >>> Type: Swing
# >>> Value: 1/4
# >>> Swing Percent: 80

```

As you can see that second value keeps drifting away as we increase the swing percentage.


### DawTools.DStaff.quantize.setValue(value)
* Parameters

  * **value** - `int`

Sets the quantize value

***

### DawTools.DStaff.quantize.value()
* Return type

  * `int`

Returns the quantize value

***

### DawTools.DStaff.quantize.setType(_type)
* Parameters

  * **_type** - `str('straight') str('tuplet') str('swing')`

Sets the quantize type

***

### DawTools.DStaff.quantize.type()
* Return type

  * `string`

Returns the quantize type

***

### DawTools.DStaff.quantize.setTuplet(tuplet)
* Parameters

  * **tuplet** - `int(left_divisor), int(right_divisor)`


Sets the quantize tuplet divisors

***

### DawTools.DStaff.quantize.tuplet()
* Return type

  * `tuplet`

Returns the quantize tuplet divisors

***

### DawTools.DStaff.quantize.setSwingPercent(percent)
* Parameters

  * **percent** - `int`


Sets the quantize swing percentage

***

### DawTools.DStaff.quantize.swingPercent()
* Return type

  * `int`

Returns the quantize swing percentage

***

### DawTools.DStaff.quantize.ms()
* Return type

  * `float` or `tuple` if swing type

Returns how many milliseconds in 1 quantize unit
When the quantize type is set to swing, it returns a
tuple(ms till first,ms from first till second)

***

### DawTools.DStaff.quantize.seconds()
* Return type

  * `float` or `tuple` if swing type

Returns how many seconds in 1 quantize unit
When the quantize type is set to swing, it returns a
tuple(seconds till first,seconds from first till second)

***

### DawTools.DStaff.quantize.pixels()
* Return type

  * `float` or `tuple` if swing type

Returns how many pixels in 1 quantize unit
When the quantize type is set to swing, it returns a
tuple(pixels till first,pixels from first till second)

***

### DawTools.DStaff.quantize.frames()
* Return type

  * `float` or `tuple` if swing type

Returns how many frames in 1 quantize unit
When the quantize type is set to swing, it returns a
tuple(frames till first,frames from first till second)

***

### DawTools.DStaff.quantize.samples()
* Return type

  * `float` or `tuple` if swing type

Returns how many samples in 1 quantize unit
When the quantize type is set to swing, it returns a
tuple(samples till first,samples from first till second)

***

### DawTools.DStaff.quantize.__iter__()
* Return type

  * `iterator`

Returns a list with pixel positions for quantization

***

As you may have noticed the last few DawTools.DStaff.Quantize methods
are helper methods to find out how many of 1 thing is in the other.

| Functions | Return |
|:----------|:-------|
|def ms()| Milliseconds in Quantize|
|def seconds()| Seconds in Quantize|
|def pixels()| Pixels in Quantize|
|def frames()| Frames in Quantize|
|def samples()| Samples in Quantize|

```python
staff = DStaff(beats=2)
print(staff.quantize.ms())
print(staff.quantize.seconds())
print(staff.quantize.pixels())
print(staff.quantize.frames())
print(staff.quantize.samples())
```

We have the same thing for the last Inner Classes bellow

***

## Inner Class DawTools.DStaff.WholeNote

| Functions | Return |
|:----------|:-------|
|def ms()| Milliseconds in WholeNote|
|def seconds()| Seconds in WholeNote|
|def pixels()| Pixels in WholeNote|
|def frames()| Frames in WholeNote|
|def samples()| Samples in WholeNote|
|def beats()| Beats in WholeNote|
|def bars()| Bars in WholeNote|

```python
staff = DStaff()
print(staff.wholeNote.ms())
print(staff.wholeNote.seconds())
print(staff.wholeNote.pixels())
print(staff.wholeNote.frames())
print(staff.wholeNote.samples())
print(staff.wholeNote.beats())
print(staff.wholeNote.bars())
```

***

## Inner Class DawTools.DStaff.Bar

| Functions | Return |
|:----------|:-------|
|def ms()| Milliseconds in Bar|
|def seconds()| Seconds in Bar|
|def pixels()| Pixels in Bar|
|def frames()| Frames in Bar|
|def samples()| Samples in Bar|
|def wholeNotes()| Whole Notes in Bar|
|def beats()| Beats in Bar|

```python
staff = DStaff()
print(staff.bar.ms())
print(staff.bar.seconds())
print(staff.bar.pixels())
print(staff.bar.frames())
print(staff.bar.samples())
print(staff.bar.wholeNotes())
print(staff.bar.beats())
```

***

## Inner Class DawTools.DStaff.Beat

| Functions | Return |
|:----------|:-------|
|def ms()| Milliseconds in Beat|
|def seconds()| Seconds in Beat|
|def pixels()| Pixels in Beat|
|def frames()| Frames in Beat|
|def samples()| Samples in Beat|
|def wholeNotes()| Whole Notes in Beat|
|def bars()| Bars in Beat|

```python
staff = DStaff()
print(staff.beat.ms())
print(staff.beat.seconds())
print(staff.beat.pixels())
print(staff.beat.frames())
print(staff.beat.samples())
print(staff.beat.wholeNotes())
print(staff.beat.bars())
```

***

## Inner Class DawTools.DStaff.Frame

| Functions | Return |
|:----------|:-------|
|def ms()| Milliseconds in Frame|
|def seconds()| Seconds in Frame|
|def pixels()| Pixels in Frame|
|def samples()| Samples in Frame|
|def wholeNotes()| Whole Notes in Frame|
|def beats()| Beats in Frame|
|def bars()| Bars in Frame|

```python
staff = DStaff()
print(staff.frame.ms())
print(staff.frame.seconds())
print(staff.frame.pixels())
print(staff.frame.samples())
print(staff.frame.wholeNotes())
print(staff.frame.beats())
print(staff.frame.bars())
```

***

## Inner Class DawTools.DStaff.Sample

| Functions | Return |
|:----------|:-------|
|def ms()| Milliseconds in Sample|
|def seconds()| Seconds in Sample|
|def pixels()| Pixels in Sample|
|def frames()| Frames in Sample|
|def wholeNotes()| Whole Notes in Sample|
|def beats()| Beats in Sample|
|def bars()| Bars in Sample|

```python
staff = DStaff()
print(staff.sample.ms())
print(staff.sample.seconds())
print(staff.sample.pixels())
print(staff.sample.frames())
print(staff.sample.wholeNotes())
print(staff.sample.beats())
print(staff.sample.bars())
```

