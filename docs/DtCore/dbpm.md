---
layout: default
title: DBpm
parent: DtCore
# nav_order: 1
---

# DawTools.DtCore.DBpm

The [DBpm]() class provides a surface to convert DNoteValue objects to seconds. [More...](dbpm.html#detailed-description)

| Inheritance            |
|:-----------------------|
| DawTools.DtCore.DBpm   |

***

| Attributes|                  |
|:----------|:-----------------|
| value     | float(bpm value) |

| Methods |
|:----------|
|def \_\_add\_\_()|
|def \_\_sub\_\_()|
|def \_\_mul\_\_()|
|def \_\_truediv\_\_()|
|def \_\_eq\_\_()|
|def \_\_ge\_\_()|
|def \_\_gt\_\_()|
|def \_\_le\_\_()|
|def \_\_lt\_\_()|
|def [\_\_call\_\_(DNoteValue)]()|
|def [seconds(DNoteValue)]()|
|def [secondsPerNote()]()|

## Detailed Description
This @dataclass can be used for simple conversions from a DawTools.DtCore.DNoteValue object to a
DawTools.DtCore.DSeconds object for retrieval of seconds in a note value.

It is also meant to be used with DawTools.DtCore.DMeter

```python
bpm = DBpm(120)

note_value = DNoteValue('1/1')
seconds_object = bpm(note_value)

print(seconds_object)# DSeconds(value=Decimal('2'))

seconds = seconds_object()
print(seconds)# 2

milliseconds = seconds_object.ms()
print(milliseconds)# 2000
```

***

### @dataclass DawTools.DtCore.DBpm(value)
* Parameters

  * **value** - `float` -> default = 120

Constructs a DBpm object.

***

### DawTools.DtCore.DBpm.seconds(noteValue)
* Parameters

  * **noteValue** - `DawTools.DtCore.DNoteValue`

* Return type

  * `DawTools.DtCore.DSeconds`

Returns DSeconds object with seconds in noteValue

***

### DawTools.DtCore.DBpm.secondsPerNote()
* Return type

  * `Decimal`

Returns seconds in 1 whole note

***

### DawTools.DtCore.DBpm.\_\_call\_\_(value=None)
Sets DBpm.value If value is of type float or int

* Parameters

  * **value** - `int`
  * **value** - `float`
  * **value** - `DawTools.DtCore.DNoteValue`

* Return type

  * `float`
  * `DawTools.DtCore.DSeconds`

Returns current DBpm.value | If **value** is of type None, float or int
Return seconds in value    | If **value** is of type DNoteValue


```python
bpm = DBpm(120)

# Retrieving value
print(bpm())# 120

# Setting value
print(bpm(60))# 60

print(bpm)# DBpm(value=60)

# Retrieving DNoteValue as a DSeconds object
print(bpm(DNoteValue('1/1')))# DSeconds(value=Decimal('4'))
```
