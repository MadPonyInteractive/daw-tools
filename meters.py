'''
Meter
'''
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from daw_tools import Meter

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
