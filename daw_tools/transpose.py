try:
    from . main import *
    from . import music_functions as mf
    from . grid import Grid
except:
    from main import *
    import music_functions as mf
    from grid import Grid

class Transpose(QWidget):
    playPosChanged = Signal(float)
    playStateChanged = Signal(bool)
    loopCheckedChanged = Signal(bool)
    timeSignatureChanged = Signal(tuple)
    widthChanged = Signal(float)
    bpmChanged = Signal(float)
    quantizeChanged = Signal(dict)

    ticker = Signal()
    def __init__(self, externalClock = False):
        QWidget.__init__(self)
        self.grid = Grid(bars=4,time_signature=(4,4))
        self.playing = False
        self.scrubType = 'frame' # frame | beat | bar
        self.frame = 0
        self.timeline = None
        self.loop = False
        self.loopRange = (0,self.frames())
        self.grid.timeSignatureChanged(self.timeChanged)
        self.grid.widthChanged(self._widthChanged)
        self.grid.bpmChanged(self._bpmChanged)
        self.grid.quantizeChanged(self._quantizeChanged)
        self.setExternalClock(externalClock)

    # Grid Redirects
    def setTimeSignature(self, time_sig):self.grid.setTimeSignature(time_sig)
    def setBeatsPerBar(self, bpb):self.grid.setBeatsPerBar(bpb)
    def setBeatDuration(self, bd):self.grid.setBeatDuration(bd)
    def setBpm(self, bpm):self.grid.setBpm(bpm)
    def setQuantize(self, *args, **kwargs):self.grid.setQuantize(*args, **kwargs)
    def frames(self):return int(self.grid.frames())
    def beats(self):return int(self.grid.beats())
    def bars(self):return int(self.grid.bars())


    def framesTillCurrentBar(self):
        return int(self.currentBar()-1)*self.grid.framesInBar()

    def framesTillCurrentBeat(self):
        return int(self.currentBeat()-1)*self.grid.framesInBeat()

    def nextBarFrame(self):
        extra_frames = self.frame-self.framesTillCurrentBar()
        return self.grid.framesInBar()-extra_frames

    def prevBarFrame(self):
        return self.frame-self.framesTillCurrentBar()

    def nextBeatFrame(self):
        extra_frames = self.frame-self.framesTillCurrentBeat()
        return self.grid.framesInBeat()-extra_frames

    def prevBeatFrame(self):
        return self.frame-self.framesTillCurrentBeat()

    def nextQuantize(self):
        ''' Returns next frame position according to current quantization value '''
        pass
        # extra_frames = self.frame-self.framesTillCurrentQuantize()
        # return min(self.grid.framesInQuantize()-extra_frames,self.frames())

    def prevQuantize(self):
        ''' Returns previous frame position according to current quantization value '''
        pass
        # return max(self.frame-self.framesTillCurrentQuantize(),0)

    def getScrub(self,direction='forward'):
        if self.scrubType   == 'frame':return 1
        elif self.scrubType == 'beat' :
            currentBeat = self.currentBeat()
            if currentBeat != int(currentBeat):# has decimal numbers?
                if direction=='forward':
                    return self.nextBeatFrame()
                else:
                    return self.prevBeatFrame()
            return self.grid.framesInBeat()
        elif self.scrubType == 'bar'  :
            currentBar = self.currentBar()
            if currentBar != int(currentBar):# has decimal numbers?
                if direction=='forward':
                    return self.nextBarFrame()
                else:
                    return self.prevBarFrame()
            return self.grid.framesInBar()

    def setScrubType(self, scrub):
        ''' frame | beat | bar '''
        self.scrubType = scrub

    def currentFrame(self):
        return self.frame

    def currentPixel(self):
        return self.frame*self.grid.frameWidth()

    def currentBar(self):
        return self.frame/self.grid.framesInBar()+1 # we add 1 because we start at Bar 1

    def currentBeat(self):
        return self.frame/self.grid.framesInBeat()+1 # we add 1 because we start at Beat 1

    def currentMillisecond(self):
        return self.frame*mf.frame_length(self.grid.fps())

    def currentSecond(self):
        return self.currentMillisecond()*D(0.001)

    def setExternalClock(self, val):
        self.externalClock = val
        if val:
            if self.timeline:
                self.timeline.stop()
                self.timeline = None
        else:
            self.timeline = QTimeLine()
            self.timeline.setEasingCurve(QEasingCurve.Linear)
            self.timeline.setUpdateInterval(5)
            self.timeline.setLoopCount(0)
            self.timeline.frameChanged.connect(self.tick)
            self.setTimeline()
            self.timeline.start()

    def setTimeline(self):
        if self.externalClock: return
        self.timeline.setDuration(int(self.grid.seconds()*1000))
        self.timeline.setFrameRange(0, self.frames())

    def tick(self):
        self.ticker.emit()
        if self.playing:
            self.frame += 1
            self.setPlayPos()

    def play(self):
        if self.playing:
            self.pause()
            return
        self.playing = True
        self.playStateChanged.emit(self.playing)
        if self.frame == self.frames():self.toStart()

    def pause(self):
        if not self.playing:return
        self.playing = False
        self.playStateChanged.emit(self.playing)

    def toStart(self):
        if self.loop:
            if self.loopRange[0] == 0:
                self.frame = 0
            else:
                if self.frame != self.loopRange[0]:
                    self.frame = self.loopRange[0]
                else:
                    self.frame = 0
        else:
            self.frame = 0
        self.setPlayPos()

    def advancePos(self):
        self.frame += self.getScrub()
        self.frame = min(self.frame,self.frames())
        self.setPlayPos()

    def reversePos(self):
        self.frame -= self.getScrub('back')
        self.frame = max(self.frame,0)
        self.setPlayPos()

    def setPlayPos(self, frame=None):
        if frame != None: self.frame = D(frame)
        self.playPosChanged.emit(self.frame)
        if self.loop:
            if self.frame >= self.loopRange[1]:self.frame = self.loopRange[0]
        elif self.frame == self.frames():
            self.pause()
            # self.toStart()

    def setLoop(self, loop=None):
        if loop != None:
            self.loop = loop
        else:# toggle
            self.loop = not self.loop
        self.loopCheckedChanged.emit(self.loop)

    def setLoopRange(self, *a):
        self.loopRange = (a[0],a[1])

    def setLoopLeft(self, v):
        self.loopRange[0] = v

    def setLoopRight(self, v):
        self.loopRange[1] = v

    # # Grid Events
    def timeChanged(self, ts):
        self.setPlayPos()
        print('hello')
        self.timeSignatureChanged.emit(ts)
    def _widthChanged(self, gw):
        self.setPlayPos()
        self.widthChanged.emit(gw)
    def _bpmChanged(self, bpm):
        self.setPlayPos()
        self.bpmChanged.emit(bpm)
    def _quantizeChanged(self, q):
        self.setPlayPos()
        self.quantizeChanged.emit(q)

    # QEvents
    def event(self, event):
        # print(event.type())
        # Key Shortcuts
        if (event.type()==QEvent.KeyPress):
            # print(event.key())
            if event.key()==Qt.Key_Space:self.play()
            elif event.key()==Qt.Key_Period:self.toStart()
            elif event.key()==Qt.Key_Plus:self.advancePos()
            elif event.key()==Qt.Key_Minus:self.reversePos()
            elif event.key()==QKeySequence("/"):self.setLoop()
            event.accept()
        return super(Transpose, self).event(event)

if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle('Transpose')

    transposeBar = Transpose()

    l = QVBoxLayout()

    tLbl = QLabel('Test')
    tLbl.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
    l.addWidget(tLbl)

    from range_slider import RangeSlider
    slider = RangeSlider()
    # slider.setSteps(transposeBar.frames())
    slider.setStepSize(transposeBar.grid.frameWidth())
    slider.setHandleSize(75,25)
    slider.setLeftHandleText('Start')
    slider.setRightHandleText('End')
    slider.setMaximumHeight(30)
    slider.setFocusPolicy(Qt.NoFocus)
    def sliderDone(r):
        totalFrames = transposeBar.frames()
        rangeStart = int(r['start']*totalFrames)
        rangeEnd = int(r['end']*totalFrames)
        print('Setting Loop Range:',rangeStart,rangeEnd,totalFrames)
        transposeBar.setLoopRange(rangeStart,rangeEnd)
    slider.finishedEditting.connect(sliderDone)
    slider.setFixedWidth(int(transposeBar.grid.width()))
    l.addWidget(slider)

    from playhead import Playhead
    playhead = Playhead(20,transposeBar.grid)
    playhead.setMaximumHeight(60)
    playhead.setFocusPolicy(Qt.NoFocus)
    # playhead.setFixedWidth(int(transposeBar.grid.width()))
    playhead.playPosChanged.connect(transposeBar.setPlayPos)
    l.addWidget(playhead)

    pgr = QProgressBar()
    pgr.setMaximum(transposeBar.frames())
    pgr.setAlignment(Qt.AlignCenter)
    pgr.setFixedWidth(int(transposeBar.grid.width()))
    l.addWidget(pgr)

    def playChanged(frame):
        # Change label
        Pixel = transposeBar.currentPixel()
        Beat = transposeBar.currentBeat()
        Bar = transposeBar.currentBar()
        Second = transposeBar.currentSecond()
        Millisecond = transposeBar.currentMillisecond()
        tLbl.setText(f'''
            Pixel  : {round(Pixel,2)}px
            Frame  : {int(frame)}
            Beat   : {round(Beat,2)}
            Bar    : {round(Bar,2)}
            Second : {round(Second,2)}
            Millisecond : {round(Millisecond,2)}
        ''')
        # Set progress bar value
        # frame = mf.map_val(frame,0,transposeBar.frames(),0,100)
        pgr.setValue(frame)
        # Set Playhead
        playhead.setPlayPos(frame)
    transposeBar.playPosChanged.connect(playChanged)

    bl = QHBoxLayout()

    backBtn = QPushButton('<<')
    backBtn.setToolTip('Back Scrub: Minus - ')
    backBtn.clicked.connect(transposeBar.reversePos)
    backBtn.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(backBtn)

    startBtn = QPushButton('|<')
    startBtn.setToolTip('To start/loop start: Period . ')
    startBtn.clicked.connect(transposeBar.toStart)
    startBtn.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(startBtn)

    playBtn = QPushButton('Play')
    playBtn.setToolTip('Play/Pause: Space Bar __ ')
    playBtn.clicked.connect(transposeBar.play)
    def playState(state):
        if state:
            playBtn.setText('Pause')
        else:
            playBtn.setText('Play')
    transposeBar.playStateChanged.connect(playState)
    playBtn.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(playBtn)

    forwardBtn = QPushButton('>>')
    forwardBtn.setToolTip('Forward Scrub: Plus + ')
    forwardBtn.clicked.connect(transposeBar.advancePos)
    forwardBtn.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(forwardBtn)

    loopCb = QCheckBox('Loop')
    loopCb.setToolTip('Loop On/Off: Forward Slash / ')
    loopCb.clicked.connect(transposeBar.setLoop)
    transposeBar.loopCheckedChanged.connect(loopCb.setChecked)
    loopCb.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(loopCb)

    scrub = QComboBox()
    scrub.addItems(['frame','beat','bar'])
    scrub.setToolTip('Scrub Type')
    def setScrub(t):
        if t == 'frame':slider.setSteps(transposeBar.frames())
        if t == 'beat':slider.setSteps(transposeBar.beats())
        if t == 'bar':slider.setSteps(transposeBar.bars())
        transposeBar.setScrubType(t)
    scrub.currentTextChanged.connect(setScrub)
    scrub.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(scrub)

    bl.addWidget(QLabel('| Time Signature:'))
    bpb = QComboBox()
    bpb.addItems(map(str,range(1,33)))
    bpb.setCurrentText(str(transposeBar.grid.timeSignature()[0]))
    bpb.setToolTip('Beats Per Bar')
    bpb.currentTextChanged.connect(transposeBar.setBeatsPerBar)
    bpb.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(bpb)

    bl.addWidget(QLabel('/'))

    bpw = QComboBox()
    bpw.addItems(['2','4','8','16','32'])
    bpw.setCurrentText(str(transposeBar.grid.timeSignature()[1]))
    bpw.setToolTip('Beats Per Whole Note')
    bpw.currentTextChanged.connect(transposeBar.setBeatDuration)
    bpw.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(bpw)

    bpmBox = QSpinBox()
    bpmBox.setRange(10,400)
    bpmBox.setValue(transposeBar.grid.bpm())
    bpmBox.setPrefix('BPM - ')
    bpmBox.setToolTip('Set Bpm')
    def setBpm(v):
        transposeBar.setBpm(v)
        QTimer.singleShot(1000,transposeBar.setFocus)
    bpmBox.valueChanged.connect(setBpm)
    bpmBox.setFocusPolicy(Qt.WheelFocus)
    bl.addWidget(bpmBox)

    bl.addWidget(QLabel('| Quantize:'))

    qtzValue = QComboBox()
    qtzValue.addItems(mf.get_quantize())
    qtzValue.setCurrentText(f"1/{transposeBar.grid.quantize['value']}")
    qtzValue.setToolTip('Quantize Value')
    qtzValue.currentTextChanged.connect(transposeBar.setQuantize)
    qtzValue.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(qtzValue)

    qtzType = QComboBox()
    qtzType.addItems(['straight','tuplet','swing'])
    qtzType.setCurrentText(transposeBar.grid.quantize['type'])
    qtzType.setToolTip('Quantize Type')
    qtzType.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(qtzType)

    qtzLeftTuplet = QComboBox()
    qtzLeftTuplet.addItems(map(str,range(1,16)))
    qtzLeftTuplet.setCurrentText(str(transposeBar.grid.quantize['tuplet_L']))
    qtzLeftTuplet.setToolTip('Quantize Left Tuple Divisor')
    def setQuantizeL(t):transposeBar.setQuantize(tuplet_L=t)
    qtzLeftTuplet.currentTextChanged.connect(setQuantizeL)
    qtzLeftTuplet.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(qtzLeftTuplet)

    tupleDiv = QLabel(':')
    bl.addWidget(tupleDiv)

    qtzRightTuplet = QComboBox()
    qtzRightTuplet.addItems(map(str,range(1,16)))
    qtzRightTuplet.setCurrentText(str(transposeBar.grid.quantize['tuplet_R']))
    qtzRightTuplet.setToolTip('Quantize Right Tuple Divisor')
    def setQuantizeR(t):transposeBar.setQuantize(tuplet_R=t)
    qtzRightTuplet.currentTextChanged.connect(setQuantizeR)
    qtzRightTuplet.setFocusPolicy(Qt.NoFocus)
    bl.addWidget(qtzRightTuplet)

    qtzSwingPercent = QSpinBox()
    qtzSwingPercent.setRange(10,100)
    qtzSwingPercent.setValue(transposeBar.grid.quantize['percent'])
    qtzSwingPercent.setSuffix('%')
    qtzSwingPercent.setToolTip('Swing Percentage')
    def setQuantizeP(p):
        transposeBar.setQuantize(percent=p)
        QTimer.singleShot(1000,transposeBar.setFocus)
    qtzSwingPercent.valueChanged.connect(setQuantizeP)
    qtzSwingPercent.setFocusPolicy(Qt.WheelFocus)
    bl.addWidget(qtzSwingPercent)

    def showHideQuantizeTypes():
        qtzLeftTuplet.hide()
        tupleDiv.hide()
        qtzRightTuplet.hide()
        qtzSwingPercent.hide()
        if transposeBar.grid.quantize['type'] == 'tuplet':
            qtzLeftTuplet.show()
            tupleDiv.show()
            qtzRightTuplet.show()
        elif transposeBar.grid.quantize['type'] == 'swing':
            qtzSwingPercent.show()

    def setQuantizeType(t):
        transposeBar.setQuantize(_type=t)
        showHideQuantizeTypes()
    qtzType.currentTextChanged.connect(setQuantizeType)

    showHideQuantizeTypes()




    # Transpose Bar Events #############################
    # transposeBar.playPosChanged.connect()
    # transposeBar.playStateChanged.connect()
    # transposeBar.loopCheckedChanged.connect()

    # Grid Events #####################################
    def timeChanged(ts):
        print('time signature changed:',ts)
    def widthChanged(gw):
        print('full width changed:',gw)
    def bpmChanged(bpm):
        # Time to change note and pattern width
        print('bpm changed:',bpm)
    def qtzChanged(q):
        print('quantize changed:',q)
    transposeBar.timeSignatureChanged.connect(timeChanged)
    transposeBar.widthChanged.connect(widthChanged)
    transposeBar.bpmChanged.connect(bpmChanged)
    transposeBar.quantizeChanged.connect(qtzChanged)

    bl.addItem(QSpacerItem(10,10,QSizePolicy.Expanding))
    l.addLayout(bl)

    l.addWidget(transposeBar)

    window.setLayout(l)
    transposeBar.setFocus()
    window.show()
    exit(app.exec())
