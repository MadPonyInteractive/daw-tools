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
from daw_tools import LinearEnvelope
import math
app = QApplication([])

# Creating the display window
window = QWidget()
window.setWindowTitle('Daw Tools Linear Envelope')
window.setMinimumWidth(822)
window.setStyleSheet("""
background-color: rgb(60, 60, 60);
""")

# Window layout
l = QGridLayout()

env = LinearEnvelope()
env.setStyleSheet("""
background-color: rgb(80, 80, 80);
""")
# Setting brush for all de-selected points
env.setDeSelectedBrush(QBrush(Qt.blue))
# Adding some points with a sin function
# also settings this points de-selected brush as addPoint() returns the point
for i in range(80): env.addPoint((i+5)*9,math.sin(i)*15).setDeSelectedBrush(QBrush(QColor(255,0,0)))
# adding and storing a point in a variable
point = env.addPoint(200,-80)
# setting point de-selected Pen (outline)
point.setDeSelectedPen(QPen(Qt.yellow,5))
# setting point selected Pen (outline)
point.setSelectedPen(QPen(Qt.red,10))
# moving stored points need to happen after the envelope is shown
env.movePoint(point, 200, 80)# ! This does not work here
l.addWidget(env,1,0)

# Adding layout to the window
window.setLayout(l)

# Showing the window
window.show()

exit(app.exec())
