seq-gui
=======

Three PyQt components that could be useful if you wanted to make a midi/audio sequencer. it's a work in progress so it's pretty unrefined but the basics are sort of there. 

one intention is to be used in [Carla](https://github.com/falkTX/Carla) as a standalone single-loop sequencer (work is being done one that)

TODO/WISHLIST
-------------
* fix delete behavior (which actually affects a lot of things)
* fix marquee stop on the right side
* fix multi-dragging
* implement loop-around-from-beginning notes
* implement changing note length (front and back)
* figure out how to get rid of global variables... the main thing right now is that the individual `note_items` are currently relying on `snap()` so if I can figure out how to move them solely via the `piano_roll` i could get rid of the global vars. this might also be related to the multi-dragging issue
* decide how quantization/beatgrid should be implemented (i kinda like how it is now but it introduces annoyances when switching between time signatures. another option is to implement 
* expose scaling
* refine the rest of the UI (e.g. auto escape comboboxes)

WON'T GET DONE FOR A WHILE (but would be nice eventually)
---------------------------------------------------------
### piano
* cut, copy, paste
* set default view to be ~halfway down page (around c3)
* velocity editor
* pitchbend (will be overlayed envelope)

### envelope
* marquee, basically c/p the stuff done in the pianoroll
* change behavior so it's easier to make sawtooths
* clicking the line selects the two points it connects
