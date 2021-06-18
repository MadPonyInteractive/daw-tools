daw-tools
=======

This project was initially forked from [seq-gui](https://github.com/rhetr/seq-gui)

The project is build for PySide 6 users.
The initial aim is to provide PyQt/PySide widgets to aid on daw type projects.

Currenct widgets work but are under development and need a lot of work.

CURRENT WIDGETS
---------------
* Piano Roll
* Envelope Editor
* Timeline

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
