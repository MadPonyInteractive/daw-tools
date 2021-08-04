'''
Dial
    Interaction
        * Control + Click = Default value
        * Double Click = Input value
        * Mouse Wheel increases/decreases value
        * Mouse Wheel + Control = Corse = 2x less precision
        * Mouse Wheel + Shift   = Fine  = 2x more precision

    TODO: Add secondary slider/value
    TODO: Option to span from center
    TODO: Alignment

    TODO if needed: Keyboard Events
    TODO if needed: Steps
'''

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from daw_tools import Dial
from daw_tools import mf

# Creating the application
app = QApplication([])

# Creating the display window
window = QWidget()
window.setWindowTitle('Daw Tools Dials')
window.setMinimumSize(300,300)
window.setStyleSheet("""
background-color: rgb(60, 60, 60);
""")

# Window layout
l = QGridLayout()

# Function for labels
def makeLabel(text):
    label = QLabel(text)
    label.setStyleSheet("color: #fff;")
    label.setAlignment(Qt.AlignCenter)
    return label

# Dial events
def changed(v):print('Dial Changed:',v)

# Default Dial
dDial = Dial()
dDial.setFixedSize(50,50)
dDial.valueChanged.connect(changed)
l.addWidget(makeLabel('Default Dial'),0,0)
l.addWidget(dDial,1,0)

# Value Dial
vDial = Dial()
vDial.setFixedSize(50,50)
vDial.setDisplayValue(True)
vDial.setValueFont(QFont("Times", 12, QFont.Bold))
vDial.valueChanged.connect(changed)
l.addWidget(makeLabel('Value Dial'),0,1)
l.addWidget(vDial,1,1)

# Text Dial
tDial = Dial()
tDial.setFixedSize(100,100)
tDial.setRange(0,200)# setMinimum() and setMaximum() also available
tDial.setValue(10)
tDial.setDefaultValue(100)
tDial.setMouseMoveRange(50)# Click and drag distance
tDial.setText('Attack', QFont("Times", 8, QFont.Bold))
tDial.valueChanged.connect(changed)
l.addWidget(makeLabel('Text Dial'),2,0)
l.addWidget(tDial,3,0)

# Other Dial
oDial = Dial(-100,100,0)# min, max, default
oDial.setFixedSize(100,100)
oDial.setValueFont(QFont("Times", 12, QFont.Bold))
oDial.setDisplayValue(True)# display the value
oDial.setPrefix('V')# value Prefix
oDial.setSuffix('ms')# value Suffix
oDial.setInverted(True)
oDial.setTextFont(QFont("Times", 7))
oDial.setText('Decay')
oDial.setPadding(10)
oDial.setStyleSheet("""
background-color: rgb(50, 100, 50);
border-radius:50;
""")
# Style the pen/bar
pen = oDial.pen()
pen.setWidth(10)
pen.setCapStyle(Qt.RoundCap)
oDial.setPen(pen)
oDial.valueChanged.connect(changed)
l.addWidget(makeLabel('Other Dial'),2,1)
l.addWidget(oDial,3,1)

# Adding layout to the window
window.setLayout(l)

# Showing the window
window.show()

exit(app.exec())
