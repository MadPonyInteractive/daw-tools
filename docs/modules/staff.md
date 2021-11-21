---
layout: default
title: DStaff
parent: Modules
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
|def [setSampleRate()](staff.html#dawtoolsdstaffsetsampleratehz)|
|def [sampleRate()](staff.html#dawtoolsdstaffsamplerate)|
|def [samples()](staff.html#dawtoolsdstaffsamples)|

Each one of the bellow inner classes has a set of their own functions

| Inner Classes |
|:--------------|
|class [DStaff.Beats](staff.html#inner-class-dawtoolsdstaffbeats)|
|class [DStaff.Bars](staff.html#inner-class-dawtoolsdstaffbars)|
|class [DStaff.Quantize](staff.html#inner-class-dawtoolsdstaffquantize)|
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

[More on signals](https://madponyinteractive.github.io/daw-tools/signals.html)

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

  * **bpm** - `float or int` -> default = 120

Sets the staff BPM

***

### DawTools.DStaff.bpm()
* Return type

  * `float or int`

Returns current BPM

***

### DawTools.DStaff.setTimeSignature(time_sig)
* Parameters

  * **time_sig** - `tuple or string` -> default = 4/4

Sets the time signature (beats per bar, beat duration)

```python
DawTools.DStaff.setTimeSignature('4/4')
# or
DawTools.DStaff.setTimeSignature(4,4)
```

***

### DawTools.DStaff.timeSignature(asString)
* Parameters

  * **asString** - `boolean` -> default = False

* Return type

  * `tuple or string`

Returns current time signature as tuple or as string if True is passed

***

### DawTools.DStaff.setBeatsPerBar(bpb)
* Parameters

  * **bpb** - `int` -> default = 4

Sets the time signature beats per bar

***

### DawTools.DStaff.beatsPerBar()
* Return type
  * `int`

Returns the time signature beats per bar

***

### DawTools.DStaff.setBeatDuration(bd)
* Parameters

  * **bd** - `int` -> default = 4

Sets the time signature beats duration

***

### DawTools.DStaff.beatDuration()
* Return type

  * `int`

Returns the time signature beats duration

***

### DawTools.DStaff.setPps(pps)
* Parameters

  * **pps** - `float or int` -> default = 100

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

  * **fps** - `int` -> default = 24

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

### DawTools.DStaff.setSampleRate(hz)
* Parameters

  * **hz** - `int` -> default = 44100

Sets the Samples per second (sample rate)

***

### DawTools.DStaff.sampleRate()
* Return type

  * `int`

Returns Samples per second (sample rate)

***

### DawTools.DStaff.samples()
* Return type

  * `int`

Returns how many Samples in staff

***

## Inner Class DawTools.DStaff.Beats

This inner class is used to manage the amount of beats in the staff.
You can use it to add, remove, set and clear the amount of beats in the staff.

It also provides a handy iterator to retrieve pixel X positions for each bar.

The [DawTools.DStaff.Bars](staff.html#inner-class-dawtoolsdstaffbars) class
does not have further documentation because it works exactly like this class
apart from the extra() method that is exclusive for beats.

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

### Inner Class DawTools.DStaff.Beats.__iter__()
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

staff.beats.set(4)
print(staff.beats())
# >>> 4

staff.beats.clear()
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

| Chains |
|:----------|
| def [ms()](staff.html#dawtoolsdstaffquantizemultipliermsiterations)|
| def [seconds()](staff.html#dawtoolsdstaffquantizemultipliersecondsiterations)|
| def [pixels()](staff.html#dawtoolsdstaffquantizemultiplierpixelsiterations)|
| def [frames()](staff.html#dawtoolsdstaffquantizemultiplierframesiterations)|
| def [samples()](staff.html#dawtoolsdstaffquantizemultipliersamplesiterations)|

This inner class is responsible for all the quantization in DawTools.DStaff.
It provides methods to set and retrieve quantization values.

Like the inner classes [DawTools.DStaff.Beats](staff.html#inner-class-dawtoolsdstaffbeats)
and [DawTools.DStaff.Bars](staff.html#inner-class-dawtoolsdstaffbars) it can also be
iterated for retrieval of pixel positions.

```python
staff = DStaff(beats=2)

print(list(staff.quantize))
# >>> [Decimal('0.0'), Decimal('25.00'), Decimal('50.00'), Decimal('75.00'), Decimal('100.0')]

for pixelX in staff.quantize:
  print(pixelX)

# >>> 0.0
# >>> 25.00
# >>> 50.00
# >>> 75.00
# >>> 100.0
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

print(staff.quantize())
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

### Inner Class DawTools.DStaff.Quantize.__iter__()
* Return type

  * `iterator`

Returns an iterator with pixel X positions

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

### DawTools.DStaff.quantize(multiplier).ms(iterations)
* Parameters
  * **multiplier** - `float` -> default = 1.0
  * **iterations** - `int`

* Return type

  * `float` or `tuple` if swing type

Returns how many milliseconds in (multiplier) quantize units
If (iterations) is passed it ignores (multiplier) and returns a generator.

When the quantize type is set to swing, it returns a
tuple(ms till first,ms from first till second)

[More about DStaff chaining methods...](staff.html#dstaff-chaining-methods)

***

### DawTools.DStaff.quantize(multiplier).seconds(iterations)
* Parameters
  * **multiplier** - `float` -> default = 1.0
  * **iterations** - `int`

* Return type

  * `float` or `tuple` if swing type

Returns how many seconds in (multiplier) quantize units
If (iterations) is passed it ignores (multiplier) and returns a generator.

When the quantize type is set to swing, it returns a
tuple(seconds till first,seconds from first till second)

[More about DStaff chaining methods...](staff.html#dstaff-chaining-methods)

***

### DawTools.DStaff.quantize(multiplier).pixels(iterations)
* Parameters
  * **multiplier** - `float` -> default = 1.0
  * **iterations** - `int`

* Return type

  * `float` or `tuple` if swing type

Returns how many pixels in (multiplier) quantize units
If (iterations) is passed it ignores (multiplier) and returns a generator.

When the quantize type is set to swing, it returns a
tuple(pixels till first,pixels from first till second)

[More about DStaff chaining methods...](staff.html#dstaff-chaining-methods)

***

### DawTools.DStaff.quantize(multiplier).frames(iterations)
* Parameters
  * **multiplier** - `float` -> default = 1.0
  * **iterations** - `int`

* Return type

  * `float` or `tuple` if swing type

Returns how many frames in (multiplier) quantize units
If (iterations) is passed it ignores (multiplier) and returns a generator.

When the quantize type is set to swing, it returns a
tuple(frames till first,frames from first till second)

[More about DStaff chaining methods...](staff.html#dstaff-chaining-methods)

***

### DawTools.DStaff.quantize(multiplier).samples(iterations)
* Parameters
  * **multiplier** - `float` -> default = 1.0
  * **iterations** - `int`

* Return type

  * `float` or `tuple` if swing type

Returns how many samples in (multiplier) quantize units
If (iterations) is passed it ignores (multiplier) and returns a generator.

When the quantize type is set to swing, it returns a
tuple(samples till first,samples from first till second)

[More about DStaff chaining methods...](staff.html#dstaff-chaining-methods)

***

## Inner Class DawTools.DStaff.WholeNote

| Chains | Return |
|:----------|:-------|
|def ms()| Milliseconds in WholeNote|
|def seconds()| Seconds in WholeNote|
|def pixels()| Pixels in WholeNote|
|def frames()| Frames in WholeNote|
|def samples()| Samples in WholeNote|
|def beats()| Beats in WholeNote|
|def bars()| Bars in WholeNote|

[More about DStaff chaining methods...](staff.html#dstaff-chaining-methods)

***

## Inner Class DawTools.DStaff.Bar

| Chains | Return |
|:----------|:-------|
|def ms()| Milliseconds in Bar|
|def seconds()| Seconds in Bar|
|def pixels()| Pixels in Bar|
|def frames()| Frames in Bar|
|def samples()| Samples in Bar|
|def wholeNotes()| Whole Notes in Bar|
|def beats()| Beats in Bar|

[More about DStaff chaining methods...](staff.html#dstaff-chaining-methods)

***

## Inner Class DawTools.DStaff.Beat

| Chains | Return |
|:----------|:-------|
|def ms()| Milliseconds in Beat|
|def seconds()| Seconds in Beat|
|def pixels()| Pixels in Beat|
|def frames()| Frames in Beat|
|def samples()| Samples in Beat|
|def wholeNotes()| Whole Notes in Beat|
|def bars()| Bars in Beat|

[More about DStaff chaining methods...](staff.html#dstaff-chaining-methods)

***

## Inner Class DawTools.DStaff.Frame

| Chains | Return |
|:----------|:-------|
|def ms()| Milliseconds in Frame|
|def seconds()| Seconds in Frame|
|def pixels()| Pixels in Frame|
|def samples()| Samples in Frame|
|def wholeNotes()| Whole Notes in Frame|
|def beats()| Beats in Frame|
|def bars()| Bars in Frame|

[More about DStaff chaining methods...](staff.html#dstaff-chaining-methods)

***

## Inner Class DawTools.DStaff.Sample

| Chains | Return |
|:----------|:-------|
|def ms()| Milliseconds in Sample|
|def seconds()| Seconds in Sample|
|def pixels()| Pixels in Sample|
|def frames()| Frames in Sample|
|def wholeNotes()| Whole Notes in Sample|
|def beats()| Beats in Sample|
|def bars()| Bars in Sample|

[More about DStaff chaining methods...](staff.html#dstaff-chaining-methods)

***

## DStaff chaining methods

The best to way to explain DStaff Inner classes chain is by code examples.

In the code bellow we check how many pixels exist in 1 beat
```python
staff = DStaff()
print(staff.beat.pixels())
# >>> 50.00
```

If we want to check how many pixels exist in 2 beats:
```python
staff = DStaff()
print(staff.beat(2).pixels())
# >>> 100.00
```

If we pass in an iterations parameter we get a generator
```python
staff = DStaff()
iterations = 2
print(staff.beat.pixels(iterations))
# >>> <generator object DStaff.Beat.__gen.<locals>.<genexpr> at 0x000001A744EB2580>
```

Iterating over this generator will retrieve pixel X positions.
```python
staff = DStaff()
for pixel in staff.beat.pixels(4):
    print(pixel)
# >>> 0.0    > beat 1 at pixel 0
# >>> 50.00  > beat 2 at pixel 50
# >>> 100.00 > beat 3 at pixel 100
# >>> 150.00 > beat 4 at pixel 150
```

So far we worked with pixels in beat but all other chain methods function in the exact same way.
```python
staff = DStaff()

# Pixels in 1 whole note
print(staff.wholeNote.pixels())
# >>> 200

# Pixels in 2 whole notes
print(staff.wholeNote(2).pixels())
# >>> 400

# Pixel positions for 4 whole notes
for pixel in staff.wholeNote.pixels(4):
    print(pixel)
# >>> 0   > 1st whole note placed at pixel 0
# >>> 200 > 2nd whole note placed at pixel 200
# >>> 400 > 3rd whole note placed at pixel 400
# >>> 600 > 4th whole note placed at pixel 600

# Beats in 1 whole note
print(staff.wholeNote().beats())
# >>> 4

# Beats in 2 whole notes
print(staff.wholeNote(2).beats())
# >>> 8

# Beat position for 4 whole notes
for beat in staff.wholeNote.beats(4):
    print(beat)
# >>> 1  > 1st whole note placed at beat 1
# >>> 5  > 2nd whole note placed at beat 5
# >>> 9  > 3rd whole note placed at beat 9
# >>> 13 > 4th whole note placed at beat 13
```

