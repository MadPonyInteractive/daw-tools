'''
Dial
    ! Example at the end of the module

    Interaction
        * Control + Click = set default value
        * Double Click = Input value
        * Mouse Wheel increases/decreases value
        * Mouse Wheel + Control = Corse = 2x less precision
        * Mouse Wheel + Shift   = Fine  = 2x more precision

    TODO: Alignment
    TODO: Add secondary slider/value
    TODO: Option to span from center

    TODO if needed: Keyboard Events
    TODO if needed: Steps
'''
try:
    from . main import *
except:
    from main import *
    import music_functions as mf

class Dial(QWidget):
    valueChanged = Signal(int)
    def __init__(self, minimum=0, maximum=100, default=50, parent=None):
        QWidget.__init__(self, parent=None)
        self.setCursor(Qt.SizeVerCursor)
        self.color = QColor(150,150,150)
        self.brush = QBrush(self.color)
        self.value = None
        self.inverted = False
        self._pen = QPen(Qt.white,5)
        self.mouseMoveRange = 400
        # self.setMinimumSize(20,20)
        self.maximum = maximum
        self.minimum = minimum
        self.canChange = False
        self.default = default
        self.setValue(default)
        self.displayValue = False
        self.mousePrev = None
        self.prefix = ''
        self.suffix = ''
        self.text = ''
        self.padding = 0
        self.setLayout(QGridLayout())
        # Edit Box
        self.edit = QLineEdit()
        self.edit.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.edit)
        self.layout().setAlignment(Qt.AlignCenter)

        palette = QPalette()
        palette.setColor(QPalette.Text, self.color)
        self.edit.setPalette(palette)

        # self.edit.setFixedSize(self.rect().width()*.4,self.rect().height()*.3)

        self.edit.editingFinished.connect(self.editDone)
        self.edit.hide()

        self.textFont = QFont("Times", 24, QFont.Bold)
        self.setValueFont(QFont("Times", 40, QFont.Bold))
        self.setAttribute(Qt.WA_StyledBackground)# allow setStylesheet

    def editDone(self):
        rsl = None
        try:
            rsl = int(self.edit.displayText())
        except:pass
        self.edit.hide()
        if rsl: self.setValue(rsl)

    def setRange(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
        self.update()

    def setMinimum(self, m):
        self.minimum = minimum
        self.update()

    def setMaximum(self, m):
        self.maximum = maximum
        self.update()

    def setDefaultValue(self, v):self.default = v
    def setDisplayValue(self, v=True):self.displayValue = v
    def setInverted(self, inverted):self.inverted = inverted

    def setPadding(self, padding):
        self.padding = padding
        self.update()

    def setPrefix(self, prefix):
        self.prefix = prefix
        self.update()

    def setSuffix(self, suffix):
        self.suffix = suffix
        self.update()

    def setText(self, text, font=None):
        self.text = text
        if font:self.setTextFont(font)
        self.update()

    def setTextFont(self, font):self.textFont = font
    def setValueFont(self, font):
        self.numberFont = font
        self.edit.setFont(font)

    def setMouseMoveRange(self, _range):self.mouseMoveRange = _range

    def setValue(self,v):
        if v == self.value:return
        self.value = v
        self.percentage = mf.map_val(v,self.minimum,self.maximum,0,1)
        if self.canChange: self.valueChanged.emit(self.value)
        self.update()

    def setPercent(self, percent):
        if percent == self.percentage:return
        self.percentage = percent
        value = int(mf.map_val(percent,0,1,self.minimum,self.maximum))
        if self.canChange and value != self.value:
            self.valueChanged.emit(value)
            self.value = value
        self.update()

    def setColor(self, color):
        self.color = color
        self.setBrush(QBrush(self.color))
        palette = QPalette()
        palette.setColor(QPalette.Text, self.color)
        self.edit.setPalette(palette)

    def setBrush(self, brush):
        self.brush = brush
        self.update()

    def setPen(self, pen):
        self._pen = pen
        self.update()

    def pen(self):return self._pen
    def brush(self):return self.brush

    def rect(self): return self.geometry()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self._pen)
        painter.setBrush(self.brush)
        if self.inverted:
            a = mf.map_val(self.percentage,0,1,300,0)
        else:
            a = mf.map_val(self.percentage,0,1,0,-300)
        r = self.rect()
        p = self._pen.widthF()+self.padding
        hp = p*.5

        rect = QRect(hp,hp,r.width()-p,r.height()-p)

        if self.inverted:
            painter.drawArc(rect,-60 * 16, a * 16)
        else:
            painter.drawArc(rect,-120 * 16, a * 16)
        if self.displayValue:
            painter.setFont(self.numberFont)
            painter.drawText(rect,Qt.AlignCenter,self.prefix+str(int(self.value))+self.suffix)
        painter.setFont(self.textFont)
        painter.drawText(rect,Qt.AlignBottom|Qt.AlignCenter,self.text)
        painter.end()

    def mouseMoveEvent(self, event):
        QWidget.mouseMoveEvent(self, event)
        # if event.modifiers()==Qt.ShiftModifier:
        #     print('Set value 2')
        #     return
        pos = event.position()-self.mousePrev
        p = mf.map_val(pos.y(),-self.mouseMoveRange,self.mouseMoveRange,1,-1)
        if self.percentage == p:return
        self.setPercent( min(max(self.percentage+p,0),1) )
        self.mousePrev = event.position()

    def mousePressEvent(self, event):
        QWidget.mousePressEvent(self, event)
        # if event.modifiers()==Qt.ShiftModifier|Qt.ControlModifier:
        #     print('Set default 2')
        #     return
        if event.modifiers()==Qt.ShiftModifier:print('Set value 2')
        if event.modifiers()==Qt.ControlModifier:
            self.setValue(self.default)
            return
        self.mousePrev = event.position()

    def mouseReleaseEvent(self, event):
        QWidget.mouseReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        self.edit.setText(str(self.value))
        self.edit.setFocus()
        self.edit.selectAll()
        self.edit.show()
        QWidget.mouseDoubleClickEvent(self, event)

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
        corse = event.modifiers()==Qt.ControlModifier
        fine = event.modifiers()==Qt.ShiftModifier
        amt = self.normalizeWheel(event)*0.02
        if corse:amt*=2
        elif fine:amt*=0.25
        self.setPercent(min(max(self.percentage+amt,0),1))
        QWidget.wheelEvent(self, event)

    def event(self, event):
        if (event.type()==QEvent.ShortcutOverride):
            self.edit.hide()
        if (event.type()==QEvent.Resize):
            self.canChange = False
            self.setPercent(self.percentage)
            self.edit.setFixedSize(self.rect().width()*.7,self.rect().height()*.3)
            self.canChange = True
            event.accept()
        return super(Dial, self).event(event)

if __name__ == '__main__':
    # Creating the application
    app = QApplication([])

    # Creating the display window
    window = QMainWindow()
    window.setWindowTitle('Daw Tool Dial')
    window.setMinimumSize(300,300)

    # Setting up the dial
    dial = Dial(-100,100,0)# min, max, default

    dial.setColor(QColor(0,255,0))

    dial.setText('Attack')

    dial.setDisplayValue(True)

    # Set prefixes and suffixes for number value
    dial.setPrefix('V')
    dial.setSuffix('ms')

    pen = dial.pen()
    pen.setWidth(10)
    pen.setCapStyle(Qt.RoundCap)
    dial.setPen(pen)

    dial.setPadding(20)

    dial.setStyleSheet("""
    background-color: rgb(50, 100, 50);
    border-radius:150;
    """)

    # events
    def changed(v):print('Changed:',v)
    dial.valueChanged.connect(changed)

    # Adding to the window
    window.setCentralWidget(dial)

    # Showing the window
    window.show()

    exit(app.exec())
