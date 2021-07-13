from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
# import daw_tools
from daw_tools import BasicSlider, RangeSlider

# Creating the application
app = QApplication([])

# Creating the display window
window = QWidget()
window.setWindowTitle('Daw Tools Sliders')
window.setMinimumSize(300,50)
window.setStyleSheet("""
background-color: rgb(60, 60, 60);
""")

# Window layout
l = QGridLayout()

# Function for labels
def makeLabel(text):
    label = QLabel(text)
    label.setStyleSheet("color: #fff;")
    return label

# Slider events
def changed(v):print('Slider Changed:',v)
def done(v):print('Slider Done:',v)

# Basic Slider Horizontal
hSlider = BasicSlider(Qt.Horizontal)
hSlider.setFixedHeight(30)
hSlider.valueChanged.connect(changed)
hSlider.finishedEditting.connect(done)
hSlider.setColor(QColor(255,80,80))
hSlider.setStyleSheet("background-color: rgb(130,30,30);")
l.addWidget(makeLabel('Basic Slider \n Horizontal'),0,0)
l.addWidget(hSlider,0,1)

# Basic Rounded Slider Horizontal
hSliderRound = BasicSlider(Qt.Horizontal, 10)
hSliderRound.setFixedHeight(30)
hSliderRound.valueChanged.connect(changed)
hSliderRound.finishedEditting.connect(done)
hSliderRound.setColor(QColor(255,200,0))
hSliderRound.setStyleSheet("background-color: rgb(130,100,0);border-radius:10;")
l.addWidget(makeLabel('Basic Slider \n Horizontal'),1,0)
l.addWidget(hSliderRound,1,1)

# Basic Slider Vertical
vSlider = BasicSlider(Qt.Vertical,10)
vSlider.setFixedHeight(300)
vSlider.valueChanged.connect(changed)
vSlider.finishedEditting.connect(done)
vSlider.setColor(QColor(0,255,0))
vSlider.setStyleSheet("background-color: rgb(50, 100, 50);border-radius:10;")
l.addWidget(makeLabel('Basic Slider \n Vertical'),2,0)
l.addWidget(vSlider,2,1)

# Range Slider
rSlider = RangeSlider(0.2,0.8)
rSlider.setFixedHeight(30)
rSlider.rangeChanged.connect(changed)
rSlider.finishedEditting.connect(done)
rSlider.setStyleSheet("background-color: rgb(80, 80, 80);")
l.addWidget(makeLabel('Range Slider'),3,0)
l.addWidget(rSlider,3,1)

# Range Slider 2
rSlider2 = RangeSlider(0.2,0.8)
rSlider2.setFixedHeight(60)
rSlider2.setStyleSheet("background-color: rgb(80, 80, 80);")
# rSlider2.setRange(0.2,0.8)# start range, end range
# rSlider2.setRangeStart(0.2)
# rSlider2.setRangeEnd(0.8)
rSlider2.setHandleSize(70,25)# width, height
# rSlider2.setHandleWidth(70)
# rSlider2.setHandleHeight(25)
# rSlider2.setFillHeight(45)
# rSlider2.setFillY(30)
rSlider2.setPrecision(0.01)
rSlider2.setSteps(10)
# rSlider2.setStepSize(30)
font = QFont('Serif',14,1,True)
# Left Handle
rSlider2.setLeftHandleBgColor(QColor(120,0,0))
rSlider2.setLeftHandleColor(Qt.white)# Text color
rSlider2.setLeftHandleFont(font)
rSlider2.setLeftHandleText('L')
# Right Handle
rSlider2.setRightHandleBgColor(QColor(0,120,0))
rSlider2.setRightHandleColor(Qt.white)# Text color
rSlider2.setRightHandleFont(font)
rSlider2.setRightHandleText('R')
# Change background
rSlider2.setBackgroundBrush(QColor(0,60,0))
# get the fill bar
f = rSlider2.getFill()
f.setBrush(QColor(0,255,0))# Set fill color
# Event Callback
def changeR2(d):
    print('Range Slider 2 Changed:',d)
    rSlider2.setLeftHandleText(round(d['start']*100))
    rSlider2.setRightHandleText(round(d['end']*100))
    if rSlider2.isCrossed():# checking crossed range
        f.setBrush(Qt.red)
    else:
        f.setBrush(Qt.green)
rSlider2.rangeChanged.connect(changeR2)
rSlider2.finishedEditting.connect(done)
l.addWidget(makeLabel('Range Slider 2 '),4,0)
l.addWidget(rSlider2,4,1)

# Adding layout to the window
window.setLayout(l)

# Showing the window
window.show()

exit(app.exec())
