from decimal import Decimal as D
## Math ###########################################
def map_val(val,in_start,in_end,out_start,out_end):
    return out_start + ((out_end - out_start) / (in_end - in_start)) * (val - in_start)

def frange(x, y, t):
    while x < y:
        yield x
        x += t

def get_closest_number(num,_list):
    return min(_list, key=lambda x:abs(D(x)-D(num)))

## QUANTIZE ###########################################################################
def get_quantize():
    return ['1/1','1/2','1/4','1/8','1/16','1/32','1/64']

## NOTES AND OCTAVES ##################################################################
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

## TIMING #####################################################
def whole_lenght(bpm):
    ''' Returns how many seconds there are in 1 whole tone '''
    return (60 / (D(bpm) / 4))

def beat_lenght(bpm, time_sig):
    ''' Returns how many seconds there are in 1 beat '''
    _ , beat_duration = time_sig
    return whole_lenght(bpm) / beat_duration

def bar_length(bpm, time_sig):
    ''' Returns how many seconds there are in 1 bar '''
    beats_per_bar, beat_duration = time_sig
    return beat_lenght(bpm, time_sig) * beat_duration

def frame_length(fps):
    ''' Returns how many milliseconds in 1 frame '''
    return 1000/D(fps)

def swing_lenght(bpm, quantize, percent):
    # 120bpm 1/8 100% = 120, 8, 100
    # in swing 1/8 means there's 8 swing notes in 1 whole note
    mul = percent * 0.01
    mul1 = mul + 1
    mul2 = 2 - mul
    base_length = 1.5 * quantize
    # print(mul1,mul2,base_length)
    whole_note_lenght = whole_lenght(bpm)
    note1_length = (whole_note_lenght / (D(str(base_length))) * D(str(mul1)))
    note2_length = (whole_note_lenght / (D(str(base_length))) * D(str(mul2)))
    return note1_length, note2_length

def tuplet_lenght(bpm, quantize, divL, divR):
    # 120bpm 1/4 3:2 = 120, 4, 3, 2
    whole_note_lenght = whole_lenght(bpm)
    tuplets_in_whole_note = D(str(divL))/D(str(divR)) * D(str(quantize))
    return whole_note_lenght / tuplets_in_whole_note

def swing_width(whole_note_width, quantize, percent):
    # 1/8 100% = 120, 8, 100
    # in swing 1/8 means there's 8 swing notes in 1 whole note
    mul = percent * 0.01
    mul1 = mul + 1
    mul2 = 2 - mul
    base_length = D('1.5') * D(str(quantize))
    note1_length = (D(str(whole_note_width)) / (D(str(base_length))) * D(str(mul1)))
    note2_length = (D(str(whole_note_width)) / (D(str(base_length))) * D(str(mul2)))
    return note1_length, note2_length

def tuplet_width(whole_note_width, quantize, divL, divR):
    # 1/4 3:2 = 120, 4, 3, 2
    # tuplets_in_whole_note = (D(str(divL))/D(str(divR))) * D(str(quantize))
    tuplets_in_whole_note = D(divL/divR) * D(str(quantize))
    return D(whole_note_width) / D(tuplets_in_whole_note)

# print(swing_lenght(60, 8, 80))
# print(tuplet_lenght(60, 8, 3,2))

# a = -5.1
# if a != int(a): print('Has decimal numbers')

# Time signature | beatsPerBar / beatDuration or [beats per whole note]
# 4/8 = 4 beats in a bar / each beat is an 8th of an whole note
# 3/4 = 3 beats in a bar / each beat is an 4th of an whole note
# 1 Bar = 1 Measure

# Tuplets
# duplet    = 2:3 = 2 notes in the space of 3
# triplet   = 3:2 = 3 notes in the space of 2
# quintuple = 5:4 = 5 in 4
# sextuple  = 6:4 = 6 in 4
# septuple  = 7:8 = 6 in 8
# swing     = 100% = same as tuples but in each group of 3 notes we skip the middle one

# best way to understand tuples its looking at their duration relationship with an whole note
'''
1 whole note / 1      '1/1'
1 whole note / 2      '1/2'
1 whole note / 4      '1/4'
1 whole note / 8      '1/8'
1 whole note / 16     '1/16'
1 whole note / 32     '1/32'
1 whole note / 64     '1/64'

1 whole note / 0.6    '1/1 D'  2:3 = 0.6
1 whole note / 1.3    '1/2 D'  2:3 = 1.3

calculation examples tuplets
1/4 3:2 = 3:2 * 4 = 6   per whole note
1/8 3:2 = 3:2 * 8 = 12  per whole note
1/8 5:4 = 5:4 * 8 = 10  per whole note
1/4 7:8 = 7:8 * 4 = 3.5 per whole note

calculation examples swing
1/8 100% = 8 per whole note
base length = 3:2 * 8
1st note length = base length * 2
2nd note length = base length * 1

1/8 80% = 8 per whole note
base length = 3:2 * 8
1st note length = base length * 1.80
2nd note length = base length * 1.20

1/16 60% = 16 per whole note
base length = 3:2 * 16
1st note length = base length * 1.60
2nd note length = base length * 1.40

1/4 60% = 4 per whole note
base length = 3:2 * 4
1st note length = base length * 1.60
2nd note length = base length * 1.40


1 whole note / 1.5    '1/1 T'  3:2 = 1.5
1 whole note / 3      '1/2 T'  3:2
1 whole note / 6      '1/4 T'  3:2
1 whole note / 12     '1/8 T'  3:2
1 whole note / 24     '1/16 T' 3:2
1 whole note / 48     '1/32 T' 3:2
1 whole note / 96     '1/64 T' 3:2

1 whole note / 1.25   '1/1 Q'  5:4 = 1.25
1 whole note / 2.5    '1/2 Q'  5:4
1 whole note / 5      '1/4 Q'  5:4
1 whole note / 10     '1/8 Q'  5:4
1 whole note / 20     '1/16 Q' 5:4
1 whole note / 40     '1/32 Q' 5:4
1 whole note / 80     '1/64 Q' 5:4

1 whole note / 0.75   '1/1 Sex'6:8 = 0.75
1 whole note / 0.375  '1/2 Sex'6:8 = 0.375

1 whole note / 0.875  '1/1 S'  7:8 = 0.875
1 whole note / 1.75   '1/2 S'  7:8
1 whole note / 3.5    '1/4 S'  7:8
1 whole note / 7      '1/8 S'  7:8
1 whole note / 14     '1/16 S' 7:8
1 whole note / 28     '1/32 S' 7:8
1 whole note / 56     '1/64 S' 7:8

1 whole note /     '1/8 SW 20%'
1 whole note /     '1/8 SW 40%'
1 whole note /     '1/8 SW 60%'
1 whole note /     '1/8 SW 80%'
1 whole note /     '1/8 SW 100%'
1 whole note /     '1/16 SW 20%'
1 whole note /     '1/16 SW 40%'
1 whole note /     '1/16 SW 60%'
1 whole note /     '1/16 SW 80%'
1 whole note /     '1/16 SW 100%'

'''
