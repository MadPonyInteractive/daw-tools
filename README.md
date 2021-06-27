daw-tools
=======

This project was initially forked from [seq-gui](https://github.com/rhetr/seq-gui)

The initial aim is to provide PyQt/PySide widgets to aid on daw type projects.

The project is build using PySide but can easly be ported to PyQt.


Current Versions and dependencies
* Python Version 3.9
* PySide Version 6.0.3

! Current widgets are functional but are under development and still need a lot of work.



CURRENT WIDGETS
---------------
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
### PIANO ROLL

![piano_roll](https://user-images.githubusercontent.com/30872066/122611228-db5ead00-d078-11eb-8678-571a2a7754eb.png)
### GRAPHICAL ENVELOPE

![Envelope](https://user-images.githubusercontent.com/30872066/122611627-8e2f0b00-d079-11eb-81fa-a340c0b7a997.png)
### TIMELINE

![timeline](https://user-images.githubusercontent.com/30872066/122611648-971fdc80-d079-11eb-80e2-85a475aa0793.png)





ROAD MAP
--------
### Make piano roll modular
* Break piano, note editor and playhead into separate widgets for better reusability

### Improvements 
* Improve Piano Roll
* Improve Envelope
* Improve Timeline

### Future Widgets
* Envelope with dials
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

Will keep updating this project when possible
