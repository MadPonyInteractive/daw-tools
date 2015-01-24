seq-gui
=======

Three PyQt components that could be useful if you wanted to make a midi/audio sequencer. it's a work in progress so it's pretty unrefined but the basics are sort of there. 

one intention is to be used in [Carla](https://github.com/falkTX/Carla) as a standalone single-loop sequencer (work is being done on that)

TODO/WISHLIST
-------------
* fix bounds enforcement and errors
* fix quantization/default length to be note lengths
* properly tie note information to note_items
* implement loop-around-from-beginning notes
* implement changing note length (front and back)
* figure out how to get rid of global variables... the main thing right now is that the individual `note_items` are currently relying on `snap()` so if I can figure out how to move them solely via the `piano_roll` i could get rid of the global vars. this might also be related to the multi-dragging issue
* expose scaling
* disable ghost note and insertion when hovering over the piano and existing notes
* refine the rest of the UI (e.g. auto escape comboboxes)
* start making keyboard shorcuts

WON'T GET DONE FOR A WHILE (but would be nice eventually)
---------------------------------------------------------
### piano
* cut, copy, paste
* set default view to be ~halfway down page (around c3)
* velocity editor
* pitchbend (will be overlayed envelope)
* fix piano playing

### envelope
* marquee, basically c/p the stuff done in the pianoroll
* change behavior so it's easier to make sawtooths
* clicking the line selects the two points it connects
