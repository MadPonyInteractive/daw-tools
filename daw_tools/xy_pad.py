'''
XYPad
    A XYPad
    Accepts and outputs range values from 0 to 1
    The input/output is a tuple as such:
        (x position,y position)
    ! Example at the end of the module

    TODO if needed: Wheel and Keyboard Events
'''
if __name__ == '__main__':
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from PySide6.QtOpenGLWidgets import *
    import music_functions as mf
else:
    try:
        from . main import *
    except:
        from main import *

class XYPad(QGraphicsView):
    valueChanged = Signal(tuple)
    finishedEditting = Signal(tuple)
    def __init__(self, x=0.0, y=0.0, openGL=False, parent=None):
        QGraphicsView.__init__(self, parent=None)
        self.setScene(QGraphicsScene())
        if openGL:# OPEN GL (Takes way too much GPU and/or CPU)
            self.gl = QOpenGLWidget()
            self.format = QSurfaceFormat()
            self.format.setSamples(4)
            self.format.setSwapInterval(0)# V-Sync (0 = more gpu less cpu | 1 = balance)
            self.gl.setFormat(self.format)
            self.setViewport(self.gl)
        self.setRenderHint(QPainter.Antialiasing)
        self.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        self.setInteractive(False)
        self.circle = None
        self.circleRadius = 20
        self.circleOutline = 2
        self.position = (0,0)
        self.percentage = (x,y)
        self.canChange = False
        self.drawCircle()

    def __repr__(self):
        return f''' XYPad
        Accepts and outputs range values from 0 to 1

        Constructor kwargs
        __init__(float(x position), float(y position), bool(use OpenGL), object(parent))

        Methods:
        setValues(float(x position), float(y position))
        setXValue(float(x position))
        setYValue(float(y position))

        Signals
        valueChanged.conncet(tuple)
        finishedEditting.conncet(tuple)
        '''

    def redraw(self):
        self.setCircle(self.percentage)

    def setValues(self,x,y):
        self.setCircle((x,y))

    def setXValue(self,x):
        self.setCircle((x,self.percentage[1]))

    def setYValue(self,y):
        self.setCircle((self.percentage[0],y))

    def getCircle(self):
        return self.circle

    def drawCircle(self):
        self.circle = QGraphicsEllipseItem(0,0,self.circleRadius,self.circleRadius)
        self.circle.setPen(QPen(QColor(Qt.white),self.circleOutline))
        self.circle.setBrush(QColor(Qt.gray))
        self.scene().addItem(self.circle)

    def setCircle(self, pos, mouse=False):
        width = self.rect().width()-self.circleRadius-self.circleOutline
        height = self.rect().height()-self.circleRadius-self.circleOutline
        if mouse:
            offset = self.circleRadius*.5 - self.circleOutline
            x = pos.x() - offset
            y = pos.y() - offset
            x = min(max(x,0),width)
            y = min(max(y,0),height)
        else:
            self.percentage = (pos[0],pos[1])
            x = mf.map_val(pos[0],0,1,0,width)
            y = mf.map_val(pos[1],1,0,0,height)

        if self.position == (x,y):return
        self.circle.setPos(x,y)
        self.position = (x,y)
        if mouse:
            x = mf.map_val(x,0,width,0,1)
            y = mf.map_val(y,height,0,0,1)
            self.percentage = (x,y)
        if self.canChange: self.valueChanged.emit(self.percentage)

    def mouseMoveEvent(self, event):
        self.setCircle(event.position(),True)
        QGraphicsView.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        self.setCircle(event.position(),True)
        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.finishedEditting.emit(self.percentage)
        QGraphicsView.mouseReleaseEvent(self, event)

    # def showEvent(self, event):
    #     if self.percentage != (0.0,0.0):
    #         self.setCircle(self.percentage)
    #         self.canChange = True
    #     QGraphicsView.showEvent(self, event)

    def event(self, event):
        # print(event.type())
        if (event.type()==QEvent.Resize):
            self.redraw()
            self.canChange = True
            event.accept()
        return super(XYPad, self).event(event)

if __name__ == '__main__':
    # Creating the application
    app = QApplication([])

    # Creating the display window
    window = QWidget()
    # window = QMainWindow()
    window.setWindowTitle('XYPad')
    window.setMinimumSize(300,300)

    # Creating a layout
    l = QGridLayout()

    hLabel = QLabel('Horizontal Label')
    hLabel.setAlignment(Qt.AlignCenter)
    l.addWidget(hLabel,0,1)

    from vertical_label import VerticalLabel
    vLabel = VerticalLabel('Vertical Label')
    vLabel.setFixedWidth(15)
    vLabel.setAlignment(Qt.AlignCenter)
    l.addWidget(vLabel,1,3)

    # Setting up the XYPad
    pad = XYPad(0.5,0.5)# initial (x,y) values

    pad.setStyleSheet("""
    border-radius: 12px;
    background-color: rgb(50, 100, 50);
    """)

    # Changing the circle
    padCircle = pad.getCircle()
    padCircle.setBrush(QColor(0,255,0))


    ySlider = QSlider(Qt.Vertical)
    ySlider.setMaximum(100)
    ySlider.setValue(50)
    def setPadY(v): pad.setYValue(v*0.01)
    ySlider.valueChanged.connect(setPadY)
    l.addWidget(ySlider,1,0)


    xSlider = QSlider(Qt.Horizontal)
    xSlider.setMaximum(100)
    xSlider.setValue(50)
    def setPadX(v): pad.setXValue(v*0.01)
    xSlider.valueChanged.connect(setPadX)
    l.addWidget(xSlider,2,1)


    # XYPad events
    def changed(v):
        print('Changed:',v)
        x = int(round(v[0],2)*100)
        y = int(round(v[1],2)*100)
        xSlider.setValue(x)
        ySlider.setValue(y)
        hLabel.setText(f'Horizontal {x}')
        vLabel.setText(f'Vertical {y}')
    pad.valueChanged.connect(changed)

    def done(v):print('Done:',v)
    pad.finishedEditting.connect(done)

    l.addWidget(pad,1,1)

    # Adding the XYPad to the window
    # window.setCentralWidget(pad)
    window.setLayout(l)

    # Showing the window
    window.show()

    # Changing the values later
    # pad.setValues(0.5,0.8)
    # pad.setXValue(0.2)
    # pad.setYValue(0.8)

    exit(app.exec())
