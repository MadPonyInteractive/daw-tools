'''
 A simple widget to create vertical/rotatable labels
'''
try:
    from . main import *
except:
    from main import *

class VerticalLabel(QGraphicsView):
    valueChanged = Signal(tuple)
    finishedEditting = Signal(tuple)
    def __init__(self, text, parent=None):
        QGraphicsView.__init__(self, parent=None)
        self.setScene(QGraphicsScene())
        self.setRenderHint(QPainter.TextAntialiasing)
        # self.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        # self.setBackgroundBrush(QColor(60,60,60))
        self.setInteractive(False)
        self.font = QFont()
        self.font.setPointSize(10)
        self.label = QGraphicsSimpleTextItem(text)
        self.label.setBrush(Qt.black)
        self.label.setFont(self.font)
        self.rotate(-90)
        self.scene().addItem(self.label)

    def getLabel(self):return self.label
    def setText(self, text):return self.label.setText(text)
    def setRotation(self,rot):self.rotate(rot)
