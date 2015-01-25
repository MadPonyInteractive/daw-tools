seq-gui
=======

Three PyQt components that could be useful if you wanted to make a midi/audio sequencer. it's a work in progress so it's pretty unrefined but the basics are sort of there. 

one intention is to be used in [Carla](https://github.com/falkTX/Carla) as a standalone single-loop sequencer (work is being done on that)

TODO/WISHLIST
-------------
* quantization is confusing for nonstandard note lengths
* implement loop-around-from-beginning notes
* disable ghost note and insertion when hovering over the piano and existing notes
* refine the rest of the UI (e.g. auto escape comboboxes)
* start making keyboard shorcuts
* anchor piano and measure indicator

WON'T GET DONE FOR A WHILE (but would be nice eventually)
---------------------------------------------------------
### piano
* cut, copy, paste
* undo/redo
* velocity editor
* pitchbend (will be overlayed envelope)
* fix piano playing

### envelope
* marquee, basically c/p the stuff done in the pianoroll
* change behavior so it's easier to make sawtooths
* clicking the line selects the two points it connects
