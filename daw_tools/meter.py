'''
Meter
'''
if __name__ == '__main__':
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    import music_functions as mf
else:
    from . main import *

class Meter(QGraphicsView):
    def __init__(self, _min=0, _max=10, parent=None):
        QGraphicsView.__init__(self, parent=None)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.setFrameShape(QFrame.NoFrame)
        self.setScene(QGraphicsScene())
        self.minimum = _min
        self.maximum = _max
        self.rectAmt = _max-_min
        self.redPercent = 0.9
        self.yellowPercent = 0.7
        self.redColor = Qt.red
        self.yellowColor = Qt.yellow
        self.greenColor = Qt.green
        self.offColor = Qt.gray
        self.value = 0
        self.pen = QPen(Qt.black,.5)
        self.rects = []
        self.addRects()

    def setRedColor(self,c):
        self.redColor = c
        self.update()
    def setYellowColor(self,c):
        self.yellowColor = c
        self.update()
    def setGreenColor(self,c):
        self.greenColor = c
        self.update()
    def setOffColor(self,c):
        self.offColor = c
        self.update()

    def setRedPercent(self,p):
        self.redPercent = p
        self.update()

    def setYellowPercent(self,p):
        self.yellowPercent = p
        self.update()

    def setPen(self, p):
        self.pen = p
        for r in self.rects: r.setPen(self.pen)
        self.update()

    def setValue(self, v):
        self.value = v
        self.update()

    def addRects(self):
        for i in range(self.rectAmt):
            self.rects.append(QGraphicsRectItem(0,0,0,0))
            self.rects[i].setPen(self.pen)
            self.scene().addItem(self.rects[i])

    def update(self):
        w = self.rect().width()
        h = self.rect().height() / self.rectAmt
        for i in range(self.rectAmt-1,-1,-1):
            x = 0
            y = ((self.rectAmt-i)-1) * h
            self.rects[i].setRect(0,0,w,h)
            self.rects[i].setPos(x,y)
            if i<self.value:
                if i>=int(self.rectAmt*self.redPercent): self.rects[i].setBrush(self.redColor)
                elif i>=int(self.rectAmt*self.yellowPercent): self.rects[i].setBrush(self.yellowColor)
                else: self.rects[i].setBrush(self.greenColor)
            else:self.rects[i].setBrush(self.offColor)

    def showEvent(self, event):
        QGraphicsView.showEvent(self, event)

    def resizeEvent(self, event):
        self.setSceneRect(self.rect())
        self.update()
        QGraphicsView.resizeEvent(self, event)

if __name__ == '__main__':
    # Creating the application
    app = QApplication([])

    # Creating the display window
    window = QWidget()
    window.setWindowTitle('Daw Tool Meter')
    window.setMinimumSize(300,100)
    window.setStyleSheet("""
    background-color: rgb(80, 80, 80);
    """)

    # Window layout
    l = QGridLayout()

    # Setting up meter 1
    meter1 = Meter(0,100)
    meter1.setPen(Qt.NoPen)
    policy = QSizePolicy()
    policy.setVerticalStretch(QSizePolicy.Minimum)
    meter1.setSizePolicy(policy)
    meter1.setFixedWidth(20)
    l.addWidget(meter1,0,1)

    # Setting up meter 2
    meter2 = Meter(0,10)
    meter2.setFixedWidth(20)
    l.addWidget(meter2,0,2)

    # Setting up meter 3
    meter3 = Meter(0,200)
    meter3.setFixedWidth(20)
    meter3.setRedPercent(0.7)
    meter3.setYellowPercent(0.4)
    meter3.setRedColor(QColor(220, 135, 50))
    meter3.setYellowColor(QColor(123, 89, 191))
    meter3.setGreenColor(QColor(123, 158, 191))
    meter3.setOffColor(Qt.black)
    l.addWidget(meter3,0,3)

    vSlider = QSlider(Qt.Vertical)
    vSlider.setRange(0,100)
    def changed(v):
        meter1.setValue(v)
        meter2.setValue(v*.1)
        meter3.setValue(v*2)
    vSlider.valueChanged.connect(changed)
    l.addWidget(vSlider,0,0)


    # Adding layout to the window
    window.setLayout(l)

    # Showing the window
    window.show()

    exit(app.exec())
