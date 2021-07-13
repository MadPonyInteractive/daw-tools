if __name__ == '__main__':
    import music_functions as mf
    from decimal import Decimal as D
else:
    try:
        from . main import mf
        from . main import D
    except:
        from main import mf
        from main import D

class Grid:
    '''
    A musical grid composed by beats and bars based on BPM and Time Signature
    '''
    def __init__(self, time_signature = (4,4), bpm = 120, beats = 0, bars = 0, fps = 24):
        self.callbacks = {
            'widthChanged':[],
            'timeSignatureChanged':[],
            'bpmChanged':[],
            'quantizeChanged':[]
        }
        self.time_sig = self.strToTuple(time_signature)
        self._bpm = bpm
        # self.time_sig[0] = Beats in a bar
        # self.time_sig[1] = Beats in a whole note
        self.pixel_mul = 100 # Pixel multiplier (used to calculate whole_note_width)
        self.min_beats = 0 # Minimum amount of beats allowed in grid
        self.whole_note_width = 0 # in pixels whole note
        self.whole_note_seconds = 0 # in seconds whole note
        self.whole_note_frames = 0 # in frames whole note
        self._bars = 0 # Amount of bars
        self._beats = 0# Amount of extra beats added to the existing bars
        self._fps = fps# Frames per second
        self.quantize = {
            'value':   16,         # 1 4 8 16 32 64
            'type':   'straight', # straight | tuplet | swing
            'tuplet_L': 3,      # tuplet left divisor 3:
            'tuplet_R': 2,      # tuplet right divisor :2
            'percent': 100         # 20 40 60 80 100
        }
        self.quantize_active = True
        self.addBars(bars)
        self.addBeats(beats)
        self.setWholeNoteSize() # i.e. a 4/4 at 120 bpm = self.pixel_mul * 2 seconds = 200 pixels

    def __repr__(self):
        return f"""Class: Grid
        Time Signature:{self.timeSignature(asString=True)}
        Bars:{self._bars}
        Extra Beats:{self._beats}
        Seconds:{self.seconds()}
        Frames:{self.frames()}
        BPM:{self._bpm}
        Fps:{self._fps}
        Pixel Width:{self.width()}px"""

    # Signals ##########################################
    def widthChanged(self, callback):
        self.callbacks['widthChanged'].append(callback)

    def timeSignatureChanged(self, callback):
        self.callbacks['timeSignatureChanged'].append(callback)

    def bpmChanged(self, callback):
        self.callbacks['bpmChanged'].append(callback)

    def quantizeChanged(self, callback):
        self.callbacks['quantizeChanged'].append(callback)

    def call(self, callback):
        if callback not in self.callbacks: return
        if callback == 'widthChanged':
            to_call = self.width()
        elif callback == 'timeSignatureChanged':
            to_call = self.time_sig
        elif callback == 'bpmChanged':
            to_call = self._bpm
        elif callback == 'quantizeChanged':
            to_call = self.quantize
        else: return
        for c in self.callbacks[callback]:
            c(to_call)

    # Internal Functions ###############################
    def adjustBeatsBars(self):
        all_beats = self.beats()
        self._bars = int(all_beats / self.time_sig[0])# add/remove extra bars
        self._beats = all_beats % self.time_sig[0]# adjust extra beats

    @staticmethod
    def strToTuple(string):
        return tuple(map(int, string.split('/'))) if type(string) == str else string

    # Getters ##########################################
    def timeSignature(self, asString=False):
        return f'{self.time_sig[0]}/{self.time_sig[1]}' if asString else self.time_sig

    def frameWidth(self):
        return self.width()/self.frames()

    def framesInBeat(self):
        return self.frames()/self.beats()

    def framesInBar(self):
        return self.frames()/self.bars()

    def beatWidth(self):
        return self.whole_note_width / self.time_sig[1]

    def barWidth(self):
        return self.beatWidth() * self.time_sig[0]

    def bpm(self):
        return self._bpm

    def beats(self, all=True):
        '''
        beats() All beats in grid
        beats(False) Only extra beats in grid that don't form a full bar
        '''
        return (self._bars*self.time_sig[0]) + self._beats if all else self._beats

    def extraBeats(self):
        return self.beats(False)

    def bars(self):
        return self._bars

    def getPositions(self):
        '''
        Returns an dictionary containing 4 arrays with pixel positions
        {'bars':[],'half_bars':[],'beats':[],'quantize'  : []}
        '''
        output = {
            'bars'      : [],
            'beats'     : [],
            'quantize'  : []
        }

        beats = self.beats()
        if not beats: return output

        beat_per_bar, beat_per_whole = self.timeSignature()
        beat_width = self.beatWidth()
        bar_width = self.barWidth()
        q = self.quantize
        max_width = D(self.width())

        width = D('0.0')
        while width <= max_width:
            output['bars'].append(width)
            # print('b',(width,))
            width += bar_width

        width = D('0.0')
        while width <= max_width:
            if width not in output['bars']: output['beats'].append(width)
            # print('b',(width,))
            width += beat_width

        if not self.quantize_active: return output
        if q['type'] == 'straight':
            qWidth = self.whole_note_width / D(q['value'])
        elif q['type'] == 'tuplet':
            qWidth = mf.tuplet_width(self.whole_note_width, q['value'], q['tuplet_L'], q['tuplet_R'])
        elif q['type'] == 'swing':
            qWidth = mf.swing_width(self.whole_note_width, q['value'], q['percent'])

        width = D('0.0')
        if q['type'] == 'swing':
            note_toggle = 0
            while width <= max_width:
                if round(width) not in output['bars'] and round(width) not in output['beats']:
                    output['quantize'].append(width)
                width += qWidth[note_toggle]
                note_toggle = 1 if note_toggle == 0 else 0
        else:
            while width <= max_width:
                if round(width) not in output['bars'] and round(width) not in output['beats']:
                    output['quantize'].append(width)
                    # print('q',(width,))
                width += qWidth

        return output

    def getQuantizeList(self):
        '''
        Returns a list with pixel positions for quantization
        '''
        quantize = []
        beats = self.beats()
        if not beats: return []
        q = self.quantize
        max_width = self.width()
        if q['type'] == 'straight':
            qWidth = self.whole_note_width / D(q['value'])
        elif q['type'] == 'tuplet':
            qWidth = mf.tuplet_width(self.whole_note_width, q['value'], q['tuplet_L'], q['tuplet_R'])
        elif q['type'] == 'swing':
            qWidth = mf.swing_width(self.whole_note_width, q['value'], q['percent'])
        width = D('0.0')
        if q['type'] == 'swing':
            note_toggle = 0
            while width <= max_width:
                quantize.append(width)
                width += qWidth[note_toggle]
                note_toggle = 1 if note_toggle == 0 else 0
        else:
            while round(width) <= max_width:
                quantize.append(width)
                # print('q2',(width,))
                width += qWidth
        return quantize

    def pixelMultiplier(self):
        return self.pixel_mul

    def fps(self):
        return self._fps

    def width(self):
        ''' Returns grid width in pixels '''
        return self.beatWidth() * self.beats()

    def seconds(self):
        ''' Returns how many seconds in grid '''
        return mf.beat_lenght(self._bpm, self.time_sig)*self.beats()

    def frames(self):
        ''' Returns how many frames in grid '''
        return self._fps*self.seconds()

    # def measures(self):
    #     bars = f"{self._bars:05d}"
    #     return f"{bars}{}{}{}"

    # Setters ##########################################
    def setQuantize(self, value=None, _type=None, tuplet_L=None, tuplet_R=None, percent=None):
        # value = '1/16'
        # _type = 'straight' | 'tuplet' | 'swing'
        # All others = integers
        changed = False
        if value != None:
            _,value = value.split('/')
            self.quantize['value'] = value
            changed = True
        if _type != None:
            self.quantize['type'] = _type
            changed = True
        if tuplet_L != None:
            self.quantize['tuplet_L'] = tuplet_L
            changed = True
        if tuplet_R != None:
            self.quantize['tuplet_R'] = tuplet_R
            changed = True
        if percent != None:
            self.quantize['percent'] = percent
            changed = True
        if changed: self.call('quantizeChanged')


    def setWholeNoteSize(self):
        self.whole_note_seconds = mf.whole_lenght(self._bpm)
        self.whole_note_width = self.whole_note_seconds*self.pixel_mul
        self.whole_note_frames = mf.frame_length(self._fps) / self.whole_note_seconds
        self.call('widthChanged')

    def addBeats(self, beats):
        ''' Adds beats to the grid'''
        self._beats += beats
        self.adjustBeatsBars()
        if beats != self._beats: self.call('widthChanged')

    def removeBeats(self, beats):
        ''' Removes beats from the grid'''
        all_beats = self.beats()
        if not all_beats: return # no beats to remove
        beats = min(all_beats,beats)
        self._beats -= beats
        self.adjustBeatsBars()
        self._bars = max(self._bars,0)# make sure we don't fall bellow 0
        if self._bars:# we still have bars
            self._beats = max(self._beats,0)# make sure we don't fall bellow 0
        else:# No bars at all
            self._beats = max(self._beats,self.min_beats)# make sure we don't fall bellow self.min_beats
        if beats != self._beats: self.call('widthChanged')

    def addBars(self, bars):
        ''' Adds bars to the grid'''
        self._bars += bars
        self.call('widthChanged')

    def removeBars(self, bars):
        ''' Removes bars from the grid'''
        self._bars = max(self._bars-bars,0)
        if bars != self._bars: self.call('widthChanged')

    def setTimeSignature(self, time_sig):
        time_sig = self.strToTuple(time_sig)
        if self.time_sig == time_sig: return
        self.time_sig = time_sig
        self.call('timeSignatureChanged')
        self.call('widthChanged')

    def setBeatsPerBar(self, bpb):
        self.setTimeSignature( (int(bpb),self.time_sig[1]) )

    def setBeatDuration(self, bd):
        ''' Set beats per whole note aka:beat duration '''
        self.setTimeSignature( (self.time_sig[0],int(bd)) )

    def setBpm(self, bpm):
        if self._bpm == bpm: return
        self._bpm = bpm
        self.call('bpmChanged')
        self.setWholeNoteSize()

    def setFps(self, fps):
        self._fps = fps
        self.setWholeNoteSize()

    def setPixelMultiplier(self, pixel_mul):
        if self.pixel_mul == pixel_mul: return
        self.pixel_mul = pixel_mul
        self.setWholeNoteSize()

if __name__ == '__main__':
    # grid = Grid(time_signature='4/4',beats=1,bars=0)
    grid = Grid(bars=1)

    def timeChanged(d):
        print('time signature changed:',d)
    def widthChanged(d):
        print('full width changed:',d)
    def bpmChanged(d):
        # Time to change note and pattern width
        print('bpm changed:',d)
    grid.timeSignatureChanged(timeChanged)
    grid.widthChanged(widthChanged)
    grid.bpmChanged(bpmChanged)

    # grid.setTimeSignature('2/4')
    # grid.setPixelMultiplier(50)
    # grid.setBpm(60)

    # print(grid.pixelMultiplier())
    # print(grid.beatWidth())
    # print(grid.barWidth())

    # print(grid.beats())

    # grid.removeBeats(17)
    # grid.removeBars(3)
    # print(grid.extraBeats(), grid.bars())
    # print(grid.timeSignature(asString=True))
    # print(grid.timeSignature())
    print(grid)
    print(grid.seconds())
    print(grid.frames())
    print(grid.frameWidth())
    print(grid.width())
# def setTimeSig(self, time_sig):
#     self.time_sig = list(map(float, time_sig.split('/'))) if type(time_sig) == str else time_sig
#     self.setWholeNoteSize()
#     return
#     self.bar_width = self.whole_note_width * self.time_sig[0]/self.time_sig[1]
#     self.max_note_length = self.bars * self.time_sig[0]/self.time_sig[1]
#     self.width = self.bar_width * self.bars
#     self.setGridDiv(self.quantization)

# def setGridDiv(self, div=None):
#     # if not div:
#     val = list(map(int, div.split('/'))) if type(div) == str else div
#     if len(val) < 3:
#         self.quantization = div
#         self.div = val[0] if len(val)==1 else val[1]
#         self.value_width = self.whole_note_width / float(self.div) if self.div else None
#         self.setQuantize(div)

# def setQuantize(self, quantization):
#     val = list(map(float, quantization.split('/'))) if type(quantization) == str else quantization
#     if len(val) == 1:
#         self.quantize(val[0])
#         self.quantization = quantization
#     elif len(val) == 2:
#         self.quantize(val[0] / val[1])
#         self.quantization = quantization

# def setBars(self, bars):
#     return
#     self.bars = float(bars)
#     self.max_note_length = self.bars * self.time_sig[0]/self.time_sig[1]
#     self.width = self.bar_width * self.bars

# def quantize(self, value):
#     self.snap_value = float(self.whole_note_width) * value if value else None
