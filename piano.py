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
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from daw_tools import Piano, mf

# Example Piano implementation
class PianoWidget(QWidget):
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

# Main window to switch between vertical and horizontal Pianos
class main_window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        l = QVBoxLayout()
        box = QComboBox()
        box.addItems(['horizontal','vertical'])
        l.addWidget(box)

        self.mainWidget=PianoWidget('horizontal',self)
        self.mainWidget.show()
        l.addWidget(self.mainWidget)
        self.mainWidget.show()

        def changeWidget(i):
            self.mainWidget.setParent(None)
            self.mainWidget=PianoWidget(i,self)
            l.addWidget(self.mainWidget)
            self.mainWidget.show()
        box.currentTextChanged.connect(changeWidget)

        self.setLayout(l)

app = QApplication([])
mainWindow = main_window()
mainWindow.show()
exit(app.exec())
