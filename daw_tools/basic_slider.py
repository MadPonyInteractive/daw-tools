'''
Basic Slider
    Accepts and outputs range values from 0 to 1

    ! Example at the end of the module

    Interaction
        * Mouse Wheel increases/decreases value
        * Mouse Wheel + Control = Corse = 2x less precision
        * Mouse Wheel + Shift   = Fine  = 2x more precision

    TODO if needed: Keyboard Events
    TODO if needed: Steps
'''
try:
    from . main import *
except:
    from main import *
    import music_functions as mf

class BasicSlider(QWidget):
    valueChanged = Signal(tuple)
    finishedEditting = Signal(tuple)
    def __init__(self, orientation=Qt.Horizontal, radius=0, value=0.5, parent=None):
        QWidget.__init__(self, parent=None)
        self.isH = True if orientation == Qt.Horizontal else False
        if self.isH:self.setCursor(Qt.SizeHorCursor)
        else: self.setCursor(Qt.SizeVerCursor)
        self.percentage = value
        self.value = self.geometry().height()
        self.color = QColor(150,150,150)
        self.brush = QBrush(self.color)
        self.pen = Qt.NoPen
        self.radius = radius
        self.fillRect = QRect(0,0,20,20)
        self.setMinimumSize(20,20)
        self.canChange = None
        self.fixRadiusX = False
        self.fixRadiusY = False
        self.setAttribute(Qt.WA_StyledBackground)# allow setStylesheet

    def setColor(self, color):
        self.color = color
        self.setBrush(QBrush(self.color))

    def setBrush(self, brush):
        self.brush = brush
        self.update()

    def setPen(self, pen):
        self.pen = pen
        self.update()

    def setRadius(self, radius):
        self.radius = radius
        self.update()

    def rect(self):
        return self.geometry()

    def setFillRect(self,x,y,w,h):
        self.fillRect = QRect(x,y,w,h)

    def redraw(self):
        self.setValue(self.percentage)

    def paintEvent(self, event):
        # print(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)

        if self.isH:
            fillRect = QRect(
                self.fillRect.x(),
                self.fillRect.y()+self.radius*.5,
                self.fillRect.width(),
                self.fillRect.height()-self.radius
                ) if self.fixRadiusX else self.fillRect
        else:
            fillRect = QRect(
                self.fillRect.x()+self.radius*.5,
                self.fillRect.y(),
                self.fillRect.width()-self.radius,
                self.fillRect.height()
                ) if self.fixRadiusY else self.fillRect

        painter.drawRoundedRect(QRect(fillRect),self.radius,self.radius,Qt.AbsoluteSize)
        painter.end()

    def setValue(self, pos, mouse=False):
        if pos == None:return
        width = self.rect().width()
        height = self.rect().height()
        if mouse:
            x = pos.x()
            y = pos.y()
            x = min(max(x,0),width)
            y = min(max(y,0),height)
        else:
            self.percentage = pos
            x = mf.map_val(pos,0,1,0,width)
            y = mf.map_val(pos,0,1,height,0)

        if self.isH:
            self.setFillRect(0,0,x,height)
        else:
            h=y
            y = mf.map_val(y,height,0,0,height)
            self.setFillRect(0,h,width,y)

        if mouse:
            if self.percentage == x or self.percentage == y:return
            if self.isH:
                p = mf.map_val(x,0,width,0,1)
                if self.percentage == p:return
                self.percentage = p
            else:
                p = mf.map_val(y,height,0,1,0)
                if self.percentage == p:return
                self.percentage = p
        if self.isH:
            if abs(x) <= self.radius:
                self.fixRadiusX = True
            else:self.fixRadiusX = False
        else:
            if abs(y) <= self.radius:
                self.fixRadiusY = True
            else:self.fixRadiusY = False

        self.update()
        if self.canChange:self.valueChanged.emit(self.percentage)

    def mouseMoveEvent(self, event):
        self.setValue(event.position(),True)
        QWidget.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        self.setValue(event.position(),True)
        QWidget.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.finishedEditting.emit(self.percentage)
        QWidget.mouseReleaseEvent(self, event)

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
        self.setValue(min(max(self.percentage+amt,0),1))
        QWidget.wheelEvent(self, event)

    def event(self, event):
        # print(event.type())
        if (event.type()==QEvent.Resize):
            self.canChange = False
            self.redraw()
            self.canChange = True
            event.accept()
        return super(BasicSlider, self).event(event)

if __name__ == '__main__':
    # Creating the application
    app = QApplication([])

    # Creating the display window
    window = QMainWindow()
    window.setWindowTitle('Basic Slider')
    window.setMinimumSize(300,800)

    # Setting up the slider
    # slider = BasicSlider(Qt.Horizontal,10)
    slider = BasicSlider(Qt.Vertical,10)

    slider.setColor(QColor(0,255,0))

    slider.setStyleSheet("""
    background-color: rgb(50, 100, 50);
    border-radius:10;
    """)

    # events
    def changed(v):
        print('Changed:',v)
    slider.valueChanged.connect(changed)

    def done(v):print('Done:',v)
    slider.finishedEditting.connect(done)

    # Adding to the window
    window.setCentralWidget(slider)

    # Showing the window
    window.show()

    exit(app.exec())
