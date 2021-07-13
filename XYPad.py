'''
XYPad
    A XYPad
    Accepts and outputs range values from 0 to 1
    The input/output is a tuple as such: (x position,y position)
'''
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from daw_tools import VerticalLabel, BasicSlider, XYPad

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

# BaiscSlider(orientation=Qt.Horizontal, radius=0, value=0.5, parent=None)
ySlider = BasicSlider(Qt.Vertical,8)
ySlider.setColor(Qt.green)
ySlider.setStyleSheet("background-color: rgb(50, 100, 50);border-radius:8;")
def setPadY(v): pad.setYValue(v)
ySlider.valueChanged.connect(setPadY)
l.addWidget(ySlider,1,0)

# BaiscSlider(orientation=Qt.Horizontal, radius=0, value=0.5, parent=None)
xSlider = BasicSlider(Qt.Horizontal,8)
xSlider.setColor(Qt.green)
xSlider.setStyleSheet("background-color: rgb(50, 100, 50);border-radius:8;")
xSlider.setValue(0.5)
def setPadX(v): pad.setXValue(v)
xSlider.valueChanged.connect(setPadX)
l.addWidget(xSlider,2,1)

# XYPad events
def changed(v):
    print('Changed:',v)
    x = v[0]
    y = v[1]
    xSlider.setValue(x)
    ySlider.setValue(y)
    hLabel.setText(f'Horizontal {round(x,2)}')
    vLabel.setText(f'Vertical {round(y,2)}')
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
