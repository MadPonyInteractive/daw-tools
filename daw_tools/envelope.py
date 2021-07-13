if __name__ == '__main__':
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from operator import itemgetter
    import music_functions as mf
else:
    try:
        from . main import *
    except:
        from main import *

class Point(QGraphicsEllipseItem):
    def __init__(self, radius=30, parent=None):
        QGraphicsEllipseItem.__init__(self, -radius*.5, -radius*.5, radius, radius, parent=None)
        self.setBrush(QBrush(QGradient.CleanMirror))# https://webgradients.com/
        self.setPen(QPen(Qt.gray,  2, Qt.SolidLine))
        self.setCursor(Qt.OpenHandCursor)

class Envelope(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.setRenderHint(QPainter.Antialiasing)
        self.setFrameShape(QFrame.NoFrame)
        self.setBackgroundBrush(QColor(255, 90, 90))# to remove
        self.setScene(QGraphicsScene())
        # Init vars
        self.points = []
        self.itemToMove = None
        self.startPoint = None
        self.endPoint = None
        self.minimum = -100
        self.maximum = 100
        self.snapValue = 10
        self.pointRadius = 15
        # Path Item and path
        self.pathItem = QGraphicsPathItem()
        self.pathItem.setPen(QPen(Qt.gray,  5, Qt.SolidLine))# Path line pen
        self.pathItem.setZValue(1)
        self.scene().addItem(self.pathItem)
        self.path = QPainterPath()
        # Start and End Points
        self.startPoint = self.addPoint(self.rect().left(),self.getCenter())
        self.endPoint = self.addPoint(self.rect().right(),self.getCenter())
        # Lines
        self.midLine = QGraphicsLineItem()
        self.midLine.setPen(QPen(Qt.black,1))
        self.scene().addItem(self.midLine)

    def getCenter(self):
        return mf.map_val(0,self.minimum,self.maximum,self.rect().height(),0)

    # def adjustPoints(self):
    #     prevWidth = self.endPoint.x()

    #     def prevToNew(x,y):
    #         mf.map_val(x,point0.x(),point1.x(),0,1)

    #     for point in self.points:
    #         # use prevWidth to calculate new positioning !

    def drawPath(self):
        if not self.startPoint or not self.endPoint:return
        # Clear path elements
        self.path.clear()
        # Add First path element
        self.path.moveTo(self.startPoint.x(),self.startPoint.y())
        # Create a temporary list with points
        pos = []
        for i, point in enumerate(self.points):
            if point == self.endPoint or point == self.startPoint:continue
            pos.append({'x':point.x(),'y':point.y(),'point':point})
        # Clear points list
        self.points.clear()
        # Append first point
        self.points.append(self.startPoint)
        # Re-order temporary list by x position
        x = itemgetter('x')
        pos.sort(key=x)
        # loop the temporary list and append
        # in between points and elements
        for i, p in enumerate(pos):
            self.points.append(p['point'])# append points
            self.path.lineTo(p['x'],p['y'])# add elements
            # self.path.addEllipse(p['x']-10,p['y']-10,20,20)
        # Append last point
        self.points.append(self.endPoint)
        # Add Last path element
        self.path.lineTo(self.endPoint.x(),self.endPoint.y())
        # Set the new path
        self.pathItem.setPath(self.path)

    def addPoint(self, x, y):
        point = Point(self.pointRadius,self)
        self.scene().addItem(point)
        point.setPos(x,y)
        point.setZValue(2)
        self.points.append(point)
        self.drawPath()
        return point

    def getValueAtX(self,x):
        point0 = None
        point1 = None
        for i, point in enumerate(self.points):
            if point.x() > x:
                point0 = self.points[i-1]
                point1 = point
                break
        if not point0: point0 = point1
        if not point0: return self.getCenter()
        xVal = mf.map_val(x,point0.x(),point1.x(),0,1)# get x percent between point0 and point1
        yVal = mf.map_val(xVal,0,1,point0.y(),point1.y())# get y at x
        return mf.map_val(yVal,0,self.rect().height()-1,self.maximum,self.minimum)

    def mouseMoveEvent(self, event):
        print(self.getValueAtX(event.position().x()), event.position().y())

        if self.itemToMove:
            p = event.position()
            x = min(max(p.x(),0),self.rect().right())
            y = min(max(p.y(),0),self.rect().bottom())
            if self.itemToMove == self.startPoint:x = self.rect().left()
            if self.itemToMove == self.endPoint:x = self.rect().right()
            center = self.getCenter()
            y = y if y+self.snapValue < center or y-self.snapValue > center else center
            self.itemToMove.setPos(x,y)
            self.drawPath()
        QGraphicsView.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        p = event.position()
        item = self.itemAt(p.x(),p.y())
        if 'Point' in str(type(item)):
            if event.button() == Qt.LeftButton:
                self.itemToMove = item
            elif event.button() == Qt.RightButton:
                if item == self.startPoint or item == self.endPoint: return
                self.points.remove(item)
                self.scene().removeItem(item)
                self.drawPath()
            return
        self.itemToMove = self.addPoint(p.x(),p.y())
        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.itemToMove:
            self.itemToMove = None
        self.drawPath()
        QGraphicsView.mouseReleaseEvent(self, event)

    def showEvent(self, event):
        self.startPoint.setPos(self.rect().left(),self.getCenter())
        self.endPoint.setPos(self.rect().right(),self.getCenter())
        self.drawPath()
        QGraphicsView.showEvent(self, event)

    def resizeEvent(self, event):
        self.setSceneRect(self.rect())
        midHeight = self.getCenter()
        self.midLine.setLine(0,midHeight,self.rect().right(),midHeight)
        # self.pathItem.setPos(0,midHeight)
        # self.drawPath()
        QGraphicsView.resizeEvent(self, event)

if __name__ == '__main__':
    app = QApplication([])
    main_window = Envelope()
    main_window.setMinimumSize(800,400)
    main_window.show()
    exit(app.exec())
