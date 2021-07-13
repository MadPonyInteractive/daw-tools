from PySide6.QtCore import QRect, QRectF
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
# from . main import *

class widget(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)

        self.setGeometry(QRect(100, 100, 600, 250))

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(QRectF())

        self.scene.setBackgroundBrush(QColor(90, 90, 90))

        self.setScene(self.scene)

        for i in range(5):
            self.item = QGraphicsEllipseItem(i*75, 10, 60, 40)
            self.scene.addItem(self.item)

