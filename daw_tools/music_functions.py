def map_val(val,in_start,in_end,out_start,out_end):
    return out_start + ((out_end - out_start) / (in_end - in_start)) * (val - in_start)

def get_octaves():
    return ['-2','-1','0','1','2','3','4','5','6','7','8']

def get_note_names(flat=False,reverse=False):
    if flat:
        notes = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
    else:
        notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    if reverse:notes.reverse()
    return notes

def get_note_name(note_number=0,flat=False,asTuple=False):
    notes = get_note_names(flat)
    octaves = get_octaves()
    note_index = 0
    for octave in octaves:
        for note in notes:
            if note_index == int(note_number): return (note,octave) if asTuple else note+octave
            note_index += 1

def get_note_number(note_name,octave_num=0):
    notes = get_note_names('b' in note_name)
    octaves = get_octaves()
    note_index = 0
    for octave in octaves:
        for note in notes:
            if note_name == note and str(octave_num) == octave: return note_index
            note_index += 1

def flat_to_sharp(note_name):
    flats = get_note_names(flat=True)
    sharps = get_note_names()
    if note_name not in flats:return False
    note_index = flats.index(note_name)
    return sharps[note_index]

def sharp_to_flat(note_name):
    flats = get_note_names(flat=True)
    sharps = get_note_names()
    if note_name not in sharps:return False
    note_index = sharps.index(note_name)
    return flats[note_index]
