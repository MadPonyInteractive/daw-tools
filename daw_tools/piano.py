'''
A piano widget to integrate in piano rolls, instruments, etc

Key Shortcuts and interaction
- Scroll     = Mouse Wheel or Up/Down/Left/Right/Page Up/Down/Home/End
- Scale      = Mouse Wheel + Control Modifier
- Press Key  = LMB
- Piano Roll = LMB + Mouse move

Features
    * Custom ScrollBar and Zoom Slider for easy integration with other widgets
    * Set a scale and all keys not in scale will be locked
    * Easily set hovered, pressed and locked color
    * Display notes as sharps (#) or flats (b)
    * Lock/UnLock single key or key range
    * Horizontal and Vertical orientation
    * Black or white keyboard
    * Note tool tips
    * And more...
'''
if __name__ == '__main__':
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    import music_functions as mf
else:
    try:
        from . main import *
    except:
        from main import *

class PianoKeyItem(QGraphicsRectItem):
    def __init__(self, width, height, note_number, parent, isHorizontal=False):
        QGraphicsRectItem.__init__(self, 0, 0, width, height, parent)
        self.isHorizontal = isHorizontal
        self.width = width
        self.height = height
        self.padding = 2
        # self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.colors = {
            'hover' : QColor(200, 0, 0),
            'pressed' : QColor(255, 100, 100),
            'locked' : QColor(150, 150, 150),
            'black' : QColor(0, 0, 0),
            'white' : QColor(255, 255, 255)
        }
        self.note_number = note_number
        self.note, self.octave = mf.get_note_name(note_number,asTuple=True)
        self.isBlack = '#' in self.note
        self.velocity = 127
        self.input = None
        self._showToolTip = False
        self.pressed = False
        self.hovered = False
        self.locked = False
        self.allwayDisplayNote = False
        self.showNotesOnHover = True

        self.font = QFont()
        self.font.setPointSize(10)
        if self.isBlack:
            self.text = self.note
        else:
            self.text = '{}{}'.format(self.note,self.octave)

        self.label = QGraphicsSimpleTextItem('', self)
        self.label.setBrush(self.colors['black'])
        self.label.setFont(self.font)

        self.setText(self.text)
        self.hideNote()
        self.setIsBlack(self.isBlack)

    def setShowNotesOnHover(self,state=True):
        self.showNotesOnHover = state

    def setShowToolTip(self,state=True):
        self._showToolTip = state
        if state:
            self.setToolTip(self.text)
        else:
            self.setToolTip('')

    def setFlat(self,flat=True):
        if flat:
            rsl = mf.sharp_to_flat(self.note)
        else:
            rsl = mf.flat_to_sharp(self.note)
        if rsl:
            self.note = rsl
            if self.isBlack:
                self.setText(self.note)
            else:
                self.setText('{}{}'.format(self.note,self.octave))
        self.hideNote()
        if self._showToolTip: self.setShowToolTip()

    def setColor(self, state, color):
        self.colors[state] = color

    def setBlackKeyboard(self, isBlack=True):
        if isBlack:
            self.colors['white'] = QColor(0, 0, 0)
            self.colors['black'] = QColor(255, 255, 255)
        else:
            self.colors['white'] = QColor(255, 255, 255)
            self.colors['black'] = QColor(0, 0, 0)
        self.setPen(QPen(self.colors['black']))
        if not self.locked and not self.pressed and not self.hovered:
            self.setDefaultColor()

    def setIsBlack(self,black=True):
        if black:
            self.setBrush(self.colors['black'])
            self.label.setBrush(self.colors['white'])
            self.setZValue(1.0)
        else:
            self.setBrush(self.colors['white'])
            self.label.setBrush(self.colors['black'])
            self.setZValue(0.0)
        self.isBlack = black

    def setDefaultColor(self):
        if self.locked:
            self.setBrush(self.colors['locked'])
            return
        if self.isBlack:
            self.setBrush(self.colors['black'])
            self.label.setBrush(self.colors['white'])
        else:
            self.setBrush(self.colors['white'])
            self.label.setBrush(self.colors['black'])

    def setLocked(self, locked=True):
        self.locked = locked
        if locked:
            self.setBrush(self.colors['locked'])
        else:
            self.setDefaultColor()

    def adjustTextPos(self):
        tSize = self.label.boundingRect()
        if self.isHorizontal:
            self.label.setPos(self.padding*2, self.height-tSize.height()-self.padding)
        else:
            self.label.setPos(self.width-tSize.width()-self.padding, self.height-tSize.height())

    def setText(self, text):
        self.text = text
        self.label.setText(text)
        self.adjustTextPos()

    def setFontSize(self,size):
        self.font.setPointSize(size)
        self.label.setFont(self.font)
        self.adjustTextPos()

    def setFont(self,font):
        self.font = font
        self.label.setFont(self.font)
        self.adjustTextPos()

    def showNote(self):
        if self.showNotesOnHover: self.label.setText(self.text)

    def hideNote(self):
        if not self.allwayDisplayNote: self.label.setText('')

    def displayNote(self, display=True, notes=[]):
        def setIt():
            self.allwayDisplayNote = display
            if display:
                self.label.setText(self.text)
            else:
                self.label.setText('')
        if len(notes):
            if self.note in notes:
                setIt()
                return
            else: return False
        else: setIt()


    def press(self,pressed):
        if self.locked:return
        if self.pressed: self.unPress()
        if type(pressed) == dict:
            self.velocity = pressed.get('velocity',None) or 100
            self.input = pressed.get('input',None) or 'code'# midi | code | mouse
        else:
            self.input = 'code'
        self.emitPressEvent()

    def unPress(self):
        if self.locked:return
        self.mouseRelease()

    ## Events #########################################
    def emitPressEvent(self):
        self.pressed = True
        self.setBrush(self.colors['pressed'])
        self.scene().key_pressed({
            'midi':self.note_number,
            'note':self.note,
            'octave':self.octave,
            'velocity':self.velocity,
            'input':self.input
            })

    def emitUnPressEvent(self):
        if self.locked:return
        self.pressed = False
        self.setDefaultColor()
        self.scene().key_unpressed({
            'midi':self.note_number,
            'note':self.note,
            'octave':self.octave,
            'velocity':self.velocity,
            'input':self.input
            })
        self.input = None

    def emitEnterEvent(self):
        self.scene().key_enter({'note':self.note,'octave':self.octave})

    def mouseEnter(self):
        self.showNote()
        self.emitEnterEvent()
        if self.locked:return
        if self.hovered:return
        self.setBrush(self.colors['hover'])
        self.hovered = True

    def mouseLeave(self):
        self.hideNote()
        if self.locked:return
        if self.pressed:
            self.emitUnPressEvent()
        else: self.setDefaultColor()
        self.hovered = False

    def mousePress(self):
        if self.locked:return
        self.input = 'mouse'
        self.emitPressEvent()

    def mouseRelease(self):
        if self.pressed: self.emitUnPressEvent()
        if self.hovered: self.setBrush(self.colors['hover'])

class VerticalPianoScene(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        self.keys = []
        self.container = None

        ## dimensions
        self.padding = 2

        ## piano dimensions
        self.note_height = 50
        self.octave_height = 7 * self.note_height
        self.height = (self.octave_height * 10) + (self.note_height*5)
        self.width = 100
        self.setSceneRect(0,0,self.width,self.height)
        self.drawPiano()

    def drawPiano(self):
        keys_width = self.width - self.padding
        self.container = QGraphicsRectItem(0, 0, self.width, self.height)
        self.container.setPos(0, 0)
        self.addItem(self.container)
        pos = 0
        for i in range(127,-1,-1):
            note_name = mf.get_note_name(i)
            note_width = keys_width
            note_height = self.note_height
            note_pos = pos
            # Black notes
            if '#' in note_name:
                note_width *= 0.65
                note_height *= 0.5
                if 'G' in note_name:                     note_pos -= note_height * 0.5
                if 'D' in note_name or 'A' in note_name: note_pos -= note_height * 0.6
                if 'C' in note_name or 'F' in note_name: note_pos -= note_height * 0.4
            else: pos+=note_height
            key = PianoKeyItem(note_width, note_height, i, self.container)
            key.setPos(0, note_pos)
            if 'C' in note_name and '#' not in note_name: key.displayNote()
            self.keys.append(key)

    # Keys Functions #####################
    def get_key(self, key):
        if type(key) == dict:
            for k in self.keys:
                if str(k.octave) == str(key['octave']) and str(k.note) == str(key['note']): return k
        for k in self.keys:
            if int(k.note_number) == int(key): return k
        return None

    # Key Events #########################
    def key_pressed(self,key):
        self.views()[0].key_pressed(key)

    def key_unpressed(self,key):
        self.views()[0].key_unpressed(key)

    def key_enter(self,key):
        self.views()[0].key_enter(key)

class HorizontalPianoScene(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        self.keys = []
        self.container = None

        ## dimensions
        self.padding = 2

        ## piano dimensions
        self.note_width = 50
        self.octave_w = 7 * self.note_width
        self.width = (self.octave_w * 10) + (self.note_width*5)
        self.height = 100
        self.setSceneRect(0,0,self.width,self.height)
        self.drawPiano()

    def drawPiano(self):
        keys_h = self.height - self.padding
        self.container = QGraphicsRectItem(0, 0, self.width, keys_h)
        self.container.setPos(0, 0)
        self.addItem(self.container)
        pos = 0
        for i in range(128):
            note_name = mf.get_note_name(i)
            note_h = keys_h
            note_w = self.note_width
            note_pos = pos
            # Black notes
            if '#' in note_name:
                note_h *= 0.65
                note_w *= 0.5
                if 'G' in note_name:                     note_pos -= note_w * 0.5
                if 'D' in note_name or 'A' in note_name: note_pos -= note_w * 0.6
                if 'C' in note_name or 'F' in note_name: note_pos -= note_w * 0.4
            else: pos+=note_w
            key = PianoKeyItem(note_w, note_h, i, self.container, True)
            key.setPos(note_pos, 0)
            if 'C' in note_name and '#' not in note_name: key.displayNote()
            self.keys.append(key)

    # Keys Functions #####################
    def get_key(self, key):
        if type(key) == dict:
            for k in self.keys:
                if str(k.octave) == str(key['octave']) and str(k.note) == str(key['note']): return k
        for k in self.keys:
            if int(k.note_number) == int(key): return k
        return None

    # Key Events #########################
    def key_pressed(self,key):
        self.views()[0].key_pressed(key)

    def key_unpressed(self,key):
        self.views()[0].key_unpressed(key)

    def key_enter(self,key):
        self.views()[0].key_enter(key)

class Piano(QGraphicsView):
    pressed = Signal(dict)
    unPressed = Signal(dict)
    enter = Signal(dict)
    velocityChanged = Signal(int)
    def __init__(self,orientation='vertical'):
        QGraphicsView.__init__(self)
        self.isHorizontal = False if orientation == 'vertical' else True
        self.piano = HorizontalPianoScene() if self.isHorizontal else VerticalPianoScene()
        self.setScene(self.piano)

        self._scaleY = 1
        self.lastPos = 0
        self.hovered = None
        self.music_scale = []
        self.lockedKeys = set([])
        self.zoomSlider = None
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if self.isHorizontal:
            self.setFixedHeight(self.piano.height-self.piano.padding)
            self.verticalScrollBar().setEnabled(False)
        else:
            self.setFixedWidth(self.piano.width-self.piano.padding)
            self.horizontalScrollBar().setEnabled(False)

    # UI Functions ###########################################
    def setZoom(self, y):
        sceneRect = self.mapToScene(self.rect()).boundingRect()
        if self.isHorizontal:
            _min = mf.map_val(sceneRect.width()*self._scaleY,0,self.piano.width,0,1)
        else:
            _min = mf.map_val(sceneRect.height()*self._scaleY,0,self.piano.height,0,1)
        self.resetTransform()
        self._scaleY = mf.map_val(y,0,99,_min,1)
        if self.isHorizontal:
            self.scale(self._scaleY, 1)
        else:
            self.scale(1, self._scaleY)

    # Piano Functions ########################################
    def setFontSize(self, size):
        for key in self.piano.keys:
            key.setFontSize(size)

    def setShowNotesOnHover(self,state=True):
        for key in self.piano.keys:
            key.setShowNotesOnHover(state)

    def setShowToolTip(self,state=True):
        for key in self.piano.keys:
            key.setShowToolTip(state)

    def setFlat(self,state=True):
        for key in self.piano.keys:
            key.setFlat(state)

    def setDisplayNotes(self,state,notes=[]):
        for key in self.piano.keys:
            key.displayNote(state,notes)

    def setScale(self,scale):
        if len(self.music_scale): self.clearScale()
        self.music_scale = scale
        if not len(self.music_scale):return
        for key in self.piano.keys:
            if key.note not in scale: key.setLocked()

    def clearScale(self):
        self.music_scale = []
        for key in self.piano.keys:
            if key.note_number not in self.lockedKeys: key.setLocked(False)

    # midi only
    def lockRange(self,_from,to):
        for key in self.piano.keys:
            if key.note_number >= _from and key.note_number <= to:
                key.setLocked()
                self.lockedKeys.add(key.note_number)

    # midi only
    def unLockRange(self,_from,to):
        for key in self.piano.keys:
            if len(self.lockedKeys):
                if key.note_number >= _from and key.note_number <= to:
                    if key.note_number in self.lockedKeys: self.lockedKeys.remove(key.note_number)
                    key.setLocked(False)
        self.setScale(self.music_scale)

    def setLockedKey(self,_key,_set=True):
        key = self.piano.get_key(_key)
        if key:
            if _set:
                self.lockedKeys.add(key.note_number)
                key.setLocked()
            else:
                if key.note_number in self.lockedKeys:
                    self.lockedKeys.remove(key.note_number)
                    key.setLocked(False)
                    self.setScale(self.music_scale)

    def setBlackKeyboard(self,state=True):
        for key in self.piano.keys:
            key.setBlackKeyboard(state)

    def press(self,pressed):
        key = self.piano.get_key(pressed)
        if key: key.press(pressed)

    def unPress(self,pressed):
        key = self.piano.get_key(pressed)
        if key: key.unPress()

    def clearPressed(self):
        for key in self.piano.keys:
            if key.pressed: key.unPress()

    def keyMatch(self,keyA,keyB):
        return keyA['note'] == keyB['note'] and keyA['octave'] == keyB['octave']

    def setColor(self,state,color):
        for key in self.piano.keys:
            key.setColor(state,color)

    def setScrollBar(self,scrollBar):
        if self.isHorizontal:
            self.setHorizontalScrollBar(scrollBar)
        else:
            self.setVerticalScrollBar(scrollBar)

    def setZoomSlider(self,slider):
        self.zoomSlider = slider

    # Signals ###############################################
    def key_pressed(self,key):
        self.pressed.emit(key)

    def key_unpressed(self,key):
        self.unPressed.emit(key)

    def key_enter(self,key):
        self.enter.emit(key)

    # Events #################################################
    def setVelocity(self,key,event):
        if self.isHorizontal:
            key.velocity = min(int(mf.map_val(event.position().y(),0,key.height*.8,0,127)),127)
        else:
            key.velocity = min(int(mf.map_val(event.position().x(),0,key.width*.6,0,127)),127)

    def getKeyUnderMouse(self, event):
        key =  self.itemAt(event.position().x(),event.position().y())
        # Check if key or key text
        if 'QGraphicsSimpleTextItem' in str(type(key)):
            key = key.parentItem()
        if 'PianoKeyItem' in str(type(key)):
            return key
        else: return False

    def event(self, event):
        # print(event.type())
        # Mouse Leave Event
        if (event.type()==QEvent.Leave):
            self.mouseLeave()
            event.accept()
        # Auto Focus
        if (event.type()==QEvent.Enter):
            self.setFocus(Qt.MouseFocusReason)
            event.accept()
        # Double Click Event
        if (event.type()==QEvent.MouseButtonDblClick):
            self.mousePressEvent(event)
            event.accept()
        return super(Piano, self).event(event)

    def mouseLeave(self):
        if self.hovered:
            self.hovered.mouseLeave()
        self.hovered = None

    def mouseReleaseEvent(self, event):
        if self.hovered and event.button() == Qt.LeftButton:
            self.hovered.mouseRelease()
        QGraphicsView.mouseReleaseEvent(self, event)

    def mousePressEvent(self, event):
        key = self.getKeyUnderMouse(event)
        if key:
            if not key.pressed and event.button() == Qt.LeftButton and self.hovered:
                self.setVelocity(key, event)
                key.mousePress()
        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        key = self.getKeyUnderMouse(event)
        if key:
            leftMouseBtnPressed = QApplication.mouseButtons() == Qt.LeftButton
            # Update Velocity on mouse pressed notes
            if self.hovered:
                if self.hovered.input == 'mouse':
                    self.setVelocity(self.hovered, event)
                    self.velocityChanged.emit(max(self.hovered.velocity,0))
            # new hovered key
            if self.hovered != key:
                if self.hovered:
                    self.hovered.mouseLeave()
                    self.hovered = None
                if key.input == None:
                    key.mouseEnter()
                    self.setVelocity(key, event)
                    if leftMouseBtnPressed: key.mousePress()
                    self.hovered = key
                else:
                    self.enter.emit({'note':key.note,'octave':key.octave})
        QGraphicsView.mouseMoveEvent(self, event)

    def normalizeWheel(self, event):
        '''
        Normalize wheel event values
        '''
        numPixels = event.pixelDelta()
        numDegrees = event.angleDelta() / 8
        if not numPixels.isNull():
            return numPixels.y()
        elif not numDegrees.isNull():
            numSteps = numDegrees / 15
            return numSteps.y()

    def wheelEvent(self, event):
        zoom = event.modifiers()==Qt.ControlModifier
        scroll = event.modifiers()==Qt.NoModifier
        self.mouseLeave()# trigger mouseLeave so we don't get stuck keys when scrolling
        if zoom or scroll:
            scrollAmt = self.normalizeWheel(event)
            if zoom:
                if self.zoomSlider:
                    scrollBar = self.zoomSlider
                else:# User did not provide a slider
                    # Create a slider for zooming
                    self.zoomSlider = scrollBar = QSlider()
                    self.zoomSlider.setValue(99)
                    self.zoomSlider.valueChanged.connect(self.setZoom)
            else:# Scroll
                scrollBar = self.horizontalScrollBar()
                QGraphicsView.wheelEvent(self, event)
            # Avoid vertical scrolling while zooming
            if zoom or self.isHorizontal:
                scrollBy = scrollBar.singleStep()*scrollAmt
                scrollPos = scrollBar.sliderPosition()
                scrollBar.setValue(scrollBy+scrollPos)

    # def keyPressEvent(self, event):
    #     print(event.key()==Qt.Key_Alt)

# Bellow code can be erased
# It is only present for example purposes
#   when loading the file by it self
if __name__ == '__main__':
    class main_Piano(QWidget):
        def __init__(self,orientation,parent):
            QWidget.__init__(self)

            # Adding the Piano
            self.piano = Piano(orientation)

            self.isHorizontal = True if orientation == 'horizontal' else False

            if self.isHorizontal:
                parent.resize(QSize(1000, 800))
            else:
                parent.resize(QSize(450, 800))

            # Main Layout
            l = QHBoxLayout()
            l.addWidget(self.piano)

            # Widgets Layout
            l2 = QVBoxLayout()

            # little function to add lines
            def addLine():
                line = QFrame()
                line.setMidLineWidth(5)
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                l2.addWidget(line)

            checkBoxLayout = QGridLayout()
            # Use black keyboard ####################################################
            def setBlackKeyboard(i):
                self.piano.setBlackKeyboard(i)
            blackKeyboardBtn = QCheckBox('Use black keyboard')
            blackKeyboardBtn.clicked.connect(setBlackKeyboard)
            checkBoxLayout.addWidget(blackKeyboardBtn,0,0)

            # Show Notes On Hover ####################################################
            def setShowNotesOnHover(i):
                self.piano.setShowNotesOnHover(i)
            showNotesOnHoverBtn = QCheckBox('Show Notes On Hover')
            showNotesOnHoverBtn.setChecked(True)
            showNotesOnHoverBtn.clicked.connect(setShowNotesOnHover)
            checkBoxLayout.addWidget(showNotesOnHoverBtn,0,1)

            # Show ToolTip ####################################################
            def setShowToolTip(i):
                self.piano.setShowToolTip(i)
            showToolTipBtn = QCheckBox('Show ToolTip')
            showToolTipBtn.clicked.connect(setShowToolTip)
            checkBoxLayout.addWidget(showToolTipBtn,1,0)

            # Set Flat Keys ####################################################
            def setFlat(i):
                self.piano.setFlat(i)
            setFlatBtn = QCheckBox('Set Flat Keys')
            setFlatBtn.clicked.connect(setFlat)
            checkBoxLayout.addWidget(setFlatBtn,1,1)

            # Set Display Notes ################################################
            def setDisplayNotes(i):
                self.piano.setDisplayNotes(i)
            setDisplayNotesBtn = QCheckBox('Set Display Notes')
            setDisplayNotesBtn.clicked.connect(setDisplayNotes)
            checkBoxLayout.addWidget(setDisplayNotesBtn,2,0)

            # Set Display Only C Notes #########################################
            def setDisplayCNotes(i):
                self.piano.setDisplayNotes(i,['C'])
            setDisplayCNotesBtn = QCheckBox('Set Display C Notes')
            setDisplayCNotesBtn.setChecked(True)
            setDisplayCNotesBtn.clicked.connect(setDisplayCNotes)
            checkBoxLayout.addWidget(setDisplayCNotesBtn,2,1)

            l2.addLayout(checkBoxLayout)
            addLine()

            # Colors ###########################################################
            colorsLayout = QHBoxLayout()
            self.color = Qt.green
            def setHoverColor(btn,_type):
                color = QColorDialog.getColor(self.color, self)
                if color.isValid():
                    btn.setText('Set '+_type)
                    btn.setStyleSheet('background-color: '+color.name()+';')
                    self.piano.setColor(_type,color)
                    self.color = color

            # Set Hover Color
            hoveredColorButton = QPushButton("Set hover color")
            hoveredColorButton.clicked.connect(lambda: setHoverColor(hoveredColorButton,'hover'))
            colorsLayout.addWidget(hoveredColorButton)

            # Set Pressed Color
            pressedColorButton = QPushButton("Set pressed color")
            pressedColorButton.clicked.connect(lambda: setHoverColor(pressedColorButton,'pressed'))
            colorsLayout.addWidget(pressedColorButton)

            # Set Locked Color
            lockedColorButton = QPushButton("Set locked color")
            lockedColorButton.clicked.connect(lambda: setHoverColor(lockedColorButton,'locked'))
            colorsLayout.addWidget(lockedColorButton)

            l2.addLayout(colorsLayout)
            addLine()

            # Scale Restriction #######################################
            scaleLayout = QFormLayout()
            scaleLayout.addWidget(QLabel('Scale Lock:'))
            def setScale(scale):
                if scale == 'Chromatic':
                    self.piano.clearScale()
                elif scale == 'C Major':
                    self.piano.setScale(['C','D','E','F','G','A','B'])
                elif scale == 'C Minor':
                    self.piano.setScale(['C','D','D#','F','G','G#','A#'])
            scaleSelect = QComboBox()
            scaleSelect.addItems(['Chromatic','C Major','C Minor'])
            scaleSelect.currentTextChanged.connect(setScale)
            scaleLayout.addWidget(scaleSelect)
            l2.addLayout(scaleLayout)
            addLine()

            # Lock/Unlock Key #########################################################
            l2.addWidget(QLabel('Lock/Unlock a Key'))
            lockKeyLayout = QHBoxLayout()
            lockKeyBox = QComboBox()
            lockKeyBox.addItems( map(str, range(120)) )
            lockKeyLock = QPushButton('Lock')
            lockKeyUnLock = QPushButton('UnLock')
            lockKeyLayout.addWidget(lockKeyBox)
            lockKeyLayout.addWidget(lockKeyLock)
            lockKeyLayout.addWidget(lockKeyUnLock)
            lockKeyLock.clicked.connect(lambda: self.piano.setLockedKey(lockKeyBox.currentIndex()))
            lockKeyUnLock.clicked.connect(lambda: self.piano.setLockedKey(lockKeyBox.currentIndex(),False))
            l2.addLayout(lockKeyLayout)
            addLine()


            # Lock/Unlock Key Range #####################################################
            l2.addWidget(QLabel('Lock/Unlock a Range'))
            lockRangeLayout = QHBoxLayout()
            lockRangeLayout.setAlignment(Qt.AlignLeft)
            lockFrom = QComboBox()
            lockFrom.addItems( map(str, range(120)) )
            lockTo = QComboBox()
            lockTo.addItems( map(str, range(120)) )
            lockTo.setCurrentIndex(45)
            lockRangeBtn = QPushButton('Lock Range')
            unlockRangeBtn = QPushButton('UnLock Range')
            lockRangeLayout.addWidget(QLabel('From:'))
            lockRangeLayout.addWidget(lockFrom)
            lockRangeLayout.addWidget(QLabel('To:'))
            lockRangeLayout.addWidget(lockTo)
            lockRangeLayout.addWidget(lockRangeBtn)
            lockRangeLayout.addWidget(unlockRangeBtn)
            lockRangeBtn.clicked.connect(lambda: self.piano.lockRange(lockFrom.currentIndex(),lockTo.currentIndex()))
            unlockRangeBtn.clicked.connect(lambda: self.piano.unLockRange(lockFrom.currentIndex(),lockTo.currentIndex()))
            l2.addLayout(lockRangeLayout)
            addLine()


            # Scroll Bar ###########################################################
            # Mouse Wheel also scrolls
            if self.isHorizontal:
                slidersLayout = QVBoxLayout()
                scrollBar = QScrollBar(Qt.Horizontal)
            else:
                slidersLayout = QHBoxLayout()
                scrollBar = QScrollBar(Qt.Vertical)
            self.piano.setScrollBar(scrollBar)#
            slidersLayout.addWidget(scrollBar)

            # Zoom Slider #########################################################
            # Control Modifier + Mouse Wheel also zooms
            if self.isHorizontal:
                zoomSlider = QSlider(Qt.Horizontal)
            else:
                zoomSlider = QSlider(Qt.Vertical)
            zoomSlider.setValue(99)
            self.piano.setZoomSlider(zoomSlider)#
            zoomSlider.valueChanged.connect(self.piano.setZoom)
            slidersLayout.addWidget(zoomSlider)

            slidersLayout.addItem( QSpacerItem(200, 40, QSizePolicy.Minimum, QSizePolicy.Expanding) )
            l2.addLayout(slidersLayout)

            # Note Label ##########################################################
            noteLabel = QLabel('Hovered Note: None')
            def EnterKey(key):
                noteLabel.setText('Hovered Note: ' + key['note'] + str(key['octave']))
            self.piano.enter.connect(EnterKey)
            l2.addWidget(noteLabel)

            # Velocity Label #########################################################
            velLabel = QLabel('Velocity changed: 0')
            def newVelocity(velocity):
                velLabel.setText('Velocity changed: ' + str(velocity) )
            self.piano.velocityChanged.connect(newVelocity)
            l2.addWidget(velLabel)
            addLine()

            # Note Press Label ####################################################
            self.pressedKeys = []
            def formatKey(key):
                return key['note'] + str(key['octave']) + ' | velocity:' + str(key['velocity']) + ' | midi: ' + str(key['midi']) + ' | input: ' + key['input']

            notePressLabel = QLabel('Pressed Notes: None')
            def updatePressedKeys():
                outputStr = 'Pressed Notes: \n'
                if not len(self.pressedKeys):
                    notePressLabel.setText(outputStr+'None')
                    return
                for key in self.pressedKeys:
                    outputStr += formatKey(key) + '\n'
                notePressLabel.setText(outputStr)
            def PressedKey(key):
                # print('Press',key)
                self.pressedKeys.append(key)
                updatePressedKeys()
            self.piano.pressed.connect(PressedKey)
            l2.addWidget(notePressLabel)

            # Note Un-Press Label ###################################################
            noteUnPressLabel = QLabel('Released Note: None')
            def UnPressedKey(key):
                # print('UnPress',key)
                outputStr = 'Released Note: \n' + formatKey(key)
                for i, pKey in enumerate(self.pressedKeys):
                    if self.piano.keyMatch(key,pKey):
                        self.pressedKeys.pop(i)
                        break
                noteUnPressLabel.setText(outputStr)
                updatePressedKeys()
            self.piano.unPressed.connect(UnPressedKey)
            l2.addWidget(noteUnPressLabel)
            addLine()

            # Press/Un-press Keys with code #################################################
            l2.addWidget(QLabel('Press/Un-Press Keys with Code'))
            l3 = QHBoxLayout()
            noteBox = QComboBox()
            noteBox.addItems(mf.get_note_names())
            octaveBox = QComboBox()
            octaveBox.addItems(mf.get_octaves())
            # Press button
            pressNoteBtn = QPushButton('Press')
            def pressNote():
                self.piano.press({
                    'note':noteBox.currentText(),
                    'octave':int(octaveBox.currentText()),
                    'velocity':100
                })
                # You can also use midi notes
                # self.piano.press(48)# C3
            pressNoteBtn.clicked.connect(pressNote)
            # Un-press Button
            unPressNoteBtn = QPushButton('Un Press')
            def un_pressNote():
                self.piano.unPress({
                    'note':noteBox.currentText(),
                    'octave':int(octaveBox.currentText())
                })
                # You can also use midi notes
                # self.piano.unPress(48)# C3
            unPressNoteBtn.clicked.connect(un_pressNote)
            # Clear Button
            clearNoteBtn = QPushButton('Clear All')
            clearNoteBtn.clicked.connect(self.piano.clearPressed)

            l3.addWidget(noteBox)
            l3.addWidget(octaveBox)
            l3.addWidget(pressNoteBtn)
            l3.addWidget(unPressNoteBtn)
            l3.addWidget(clearNoteBtn)
            l2.addLayout(l3)


            l.addLayout(l2)
            self.setLayout(l)

    class main_window(QWidget):
        def __init__(self):
            QWidget.__init__(self)
            l = QVBoxLayout()
            box = QComboBox()
            box.addItems(['horizontal','vertical'])
            l.addWidget(box)

            self.mainWidget=main_Piano('horizontal',self)
            self.mainWidget.show()
            l.addWidget(self.mainWidget)
            self.mainWidget.show()

            def changeWidget(i):
                self.mainWidget.setParent(None)
                self.mainWidget=main_Piano(i,self)
                l.addWidget(self.mainWidget)
                self.mainWidget.show()
            box.currentTextChanged.connect(changeWidget)

            self.setLayout(l)

    app = QApplication([])
    mainWindow = main_window()
    mainWindow.show()
    exit(app.exec())

