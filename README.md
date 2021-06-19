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
* Piano Roll

![piano_roll](https://user-images.githubusercontent.com/30872066/122611228-db5ead00-d078-11eb-8678-571a2a7754eb.png)
* Envelope Editor

![Envelope](https://user-images.githubusercontent.com/30872066/122611627-8e2f0b00-d079-11eb-81fa-a340c0b7a997.png)
* Timeline

![timeline](https://user-images.githubusercontent.com/30872066/122611648-971fdc80-d079-11eb-80e2-85a475aa0793.png)





FUTURE INTERGRATIONS
--------------------
### Midi Engine (maybe mingus)
* Ability to play/import/export midi files
* Chord and Melody generation
* Arpeggiator

### Audio Engine (maybe py-audio or pyo)
* Ability to record/import/export audio files




REASON
------
I've been producing/composing/mixing music for over 20 years and programming for 10.

I decided to move forward with a little project I long been dreaming of for music composition and came across seq-gui.
I found seq-gui very interesting and decided to fork it as it had not been updated for 7 years.

The industry standard for building audio applications seems to be [JUCE](https://juce.com/) at the moment.
But JUCE uses C++, a language that makes me physically ill just looking at it :D

Considering my idea does not need all the intricacies that JUCE offers, I'm going with python.

Will keep updating this project when possible
