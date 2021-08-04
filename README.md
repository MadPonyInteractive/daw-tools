daw-tools
=========

The initial aim is to provide PyQt/PySide widgets to aid on daw type projects.

The project is build using PySide but can easly be ported to PyQt by editing main.py imports.


Current Versions and dependencies
* Python Version 3.9
* PySide Version 6.1.2


USAGE
=====
Add daw_tools directory to your python project

`import daw_tools`

`piano = daw_tools.Piano()`

All the files in the top level folder are examples of how to use the already finished widgets.



At the moment each file in the daw-tools folder has an embeded example for development ease, 
this makes the library quite big in size and it will be removed as the library matures 
and the examples are all moved to the top level folder.


CURRENT WIDGETS
---------------
### METER
![image](https://user-images.githubusercontent.com/30872066/128000271-1a1a6c4a-4090-4f9e-a6d0-5a7f50c52249.png)



### DIAL
![image](https://user-images.githubusercontent.com/30872066/127852034-27d5aed8-0adc-47b7-8525-1b42ee2f51fe.png)


### LINEAR ENVELOPE
![image](https://user-images.githubusercontent.com/30872066/126156507-dcee3b27-6de8-4b98-a32a-bbde0b1b2237.png)


### PIANO
A piano widget to integrate in piano rolls, instruments, etc

* Custom ScrollBar and Zoom Slider for easy integration with other widgets
* Set a scale and all keys not in scale will be locked
* Easily set hovered, pressed and locked color
* Display notes as sharps (#) or flats (b)
* Lock/UnLock single key or key range
* Horizontal and Vertical orientation
* Black or white keyboard
* Note tool tips
* And more...

![image](https://user-images.githubusercontent.com/30872066/123536227-03a57600-d721-11eb-91f6-cbd80afbc5a3.png)
![image](https://user-images.githubusercontent.com/30872066/123536241-13bd5580-d721-11eb-93e5-e97aad3926da.png)
### SLIDERS

![image](https://user-images.githubusercontent.com/30872066/125504194-06eb83b4-fa54-430a-802c-5e93294bf629.png)

### XYPad

![image](https://user-images.githubusercontent.com/30872066/125504251-0ec78d4f-466b-4936-a2e5-e20c69e77b6b.png)

### More under construction and added soon...



ROAD MAP
--------

### Future Widgets
* Piano Roll
* Envelope with curves
* Timeline
* Transpose
* Mixer Channel
* Mixer
* Step Sequencer


REASON
------
I've been producing/composing/mixing music for over 20 years and programming for 10.

I decided to move forward with a little project I long been dreaming of for music composition and came across seq-gui.
I found seq-gui very interesting and decided to fork it as it had not been updated for 7 years.

The industry standard for building audio applications seems to be [JUCE](https://juce.com/) at the moment.
But JUCE uses C++, a language that makes me physically ill just looking at it :D

Considering my idea does not need all the intricacies that JUCE offers, I'm going with python.
So all the widgets in daw-tools will be applied in a real world application.
This means I will keep updating this project as I find bugs when implementing.

At the moment it's still in early development so I've just been updating improovements where I see fit with no branches or version control but as soon as the GRID dependent widgets are finished, version control will start.

You are welcome to participate in this project!
