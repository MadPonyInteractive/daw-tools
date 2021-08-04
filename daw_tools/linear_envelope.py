'''
An interactive linear (no curves) envelope

It is meant to integrate with timelines

Interaction:
    * DoubleClick to add points
    * RightClick on points to remove them
    * LeftClick+Drag a point to move it and any selected points
    * LeftClick+Drag to select multiple points (selection box)
    * Ctrl+LeftClick+Drag to add multiple points to selection (selection box)
    * Ctrl+LeftClick on point to add/remove to/from selected points
    * Ctrl+A to select all points
    * Shift+A to de-select all points
    * Ctrl+Shift+A Invert point selection
    * Delete key will remove selected points
'''
try:
    from . main import *
except:
    from main import *
    from envelope_point import Point as EnvPoint
    from grid import Grid

class Envelope(QGraphicsView):
    positionChanged = Signal(dict)
    def __init__(self, minimum = -100, maximum = 100, grid=None):
        QGraphicsView.__init__(self)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.setRenderHint(QPainter.Antialiasing)
        self.setFrameShape(QFrame.NoFrame)
        self.setScene(QGraphicsScene())
        if not grid:
            warnings.warn("No 'Grid' passed, creating one.")
            try:
                grid = Grid(bpm=60,bars=2)
            except:
                raise ValueError("Couldn't import the grid module!")
        self.grid = grid
        self.grid.widthChanged(self.adjustPointsX)
        # self.grid.timeSignatureChanged(self.redraw)
        # self.grid.quantizeChanged(self.redraw)
        # Init vars
        self.points = []
        self.pointToMove = None
        self.startPoint = None
        self.endPoint = None
        self.minimum = minimum
        self.maximum = maximum
        self.pointRadius = 15
        self.useSnapping = True
        self.snapValue = 10
        # Path Item and path
        self.pathItem = QGraphicsPathItem()
        self.pathItem.setPen(QPen(Qt.gray,  5, Qt.SolidLine))# Path line pen
        self.pathItem.setZValue(1)
        # self.pathItem.setCursor(Qt.PointingHandCursor)
        self.scene().addItem(self.pathItem)
        self.path = QPainterPath()
        # Drag Selection Box
        self.selectBox = QGraphicsRectItem()
        self.selectBox.setBrush(QColor(255,255,255,80))
        self.selectBox.setPen(Qt.NoPen)
        self.selectBox.hide()
        self.selectBox.setData(0,[])# points inside the selection
        self.scene().addItem(self.selectBox)
        # Points Brushes and Pens
        self.selectedBrush = QBrush(QGradient.DustyGrass)# https://webgradients.com/
        self.selectedPen = QPen(Qt.gray,  2, Qt.SolidLine)
        self.deSelectedBrush = QBrush(QGradient.CleanMirror)# https://webgradients.com/
        self.deSelectedPen = QPen(Qt.gray,  2, Qt.SolidLine)
        # Set Start and End Points
        self.startPoint = self.addPoint(0,0)
        self.endPoint = self.addPoint(float(self.grid.width()),0)
        self.startPoint.setLockX(True)
        self.endPoint.setLockX(True)
        # Default (value 0) horizontal line
        self.defLine = QGraphicsLineItem()
        self.defLine.setPen(QPen(QColor(0,0,0,80),1))
        self.scene().addItem(self.defLine)
        # Crosshair
        self.useCrosshair = True
        self.crossH = QGraphicsLineItem()
        self.crossH.setPen(QPen(Qt.white,1))
        self.scene().addItem(self.crossH)
        self.crossV = QGraphicsLineItem()
        self.crossV.setPen(QPen(Qt.white,1))
        self.scene().addItem(self.crossV)
        # Quantize
        self.useQuantize = True
        self.QuantizePen = QPen(QColor(255,255,255,80),1)
        self.positionChanged.connect(self.pointMoved)

    # Setters ###############################################
    def setSelectedBrush(self,b):
        for point in self.points:
            point.setSelectedBrush(b)
            self.selectedBrush = b
    def setSelectedPen(self,p):
        for point in self.points:
            point.setSelectedPen(p)
            self.selectedPen = p
    def setDeSelectedBrush(self,b):
        for point in self.points:
            point.setDeSelectedBrush(b)
            self.deSelectedBrush = b
    def setDeSelectedPen(self,p):
        for point in self.points:
            point.setDeSelectedPen(p)
            self.deSelectedPen = p

    def setUseCrosshair(self, b=True): self.useCrosshair = b
    def setUseSnapping(self, b=True): self.useSnapping = b
    def setUseQuantize(self, b=True): self.useQuantize = b
    def setMinimum(self,v): self.minimum = v
    def setMaximum(self,v): self.maximum = v
    def setPointRadius(self,v): self.pointRadius = v
    def setSnapValue(self,v): self.snapValue = v
    def addPoint(self, x, value):
        y=mf.map_val(value,self.maximum,self.minimum,0,self.rect().height())
        return self._addPoint(x,y)

    def movePoint(self, point, x, value):
        y=mf.map_val(value,self.maximum,self.minimum,0,self.rect().height())
        point.moveTo(x,y)
        self.drawPath()

    def deletePoint(self, point):
        if point == self.startPoint or point == self.endPoint: return
        if point not in self.points: return
        self.points.remove(point)
        self.scene().removeItem(point)

    # Getters ################################################
    def getValueAtX(self,x):
        point0 = None # Previous point in current pixel position
        point1 = None # Next point in current pixel position
        for i, point in enumerate(self.points):
            if point.x() > x:
                point0 = self.points[i-1]
                point1 = point
                break
        if not point0: point0 = point1
        if not point0: return self.getCenter()
        xVal = mf.map_val(x,point0.x(),point1.x(),0,1)# get x percent between point0 and point1
        yVal = mf.map_val(xVal,0,1,point0.y(),point1.y())# get y at x
        return mf.map_val(yVal,0,self.rect().height(),self.maximum,self.minimum)

    def getCenter(self): return mf.map_val(0,self.minimum,self.maximum,self.height(),0)

    # Internal functions #####################################
    @staticmethod
    def isPoint(item): return 'Point' in str(type(item))

    def height(self):
        hs = self.horizontalScrollBar()
        return self.rect().height()-hs.height() if hs.isVisible() else self.rect().height()

    def adjustPointsY(self):
        for point in self.points:
            y = mf.map_val(point.normals()[1],0,1,0,self.height())
            point.setYBounds(0,self.height())
            point.setY(y)
        self.drawPath()

    def adjustPointsX(self,w):
        if self.useQuantize: self.drawQuantizeLines()
        gridWidth = float(self.grid.width())
        self.setSceneRect(0,0,gridWidth,self.rect().height()-self.horizontalScrollBar().height())
        for point in self.points:
            x = mf.map_val(point.normals()[0],0,1,0,gridWidth)
            point.setXBounds(0,gridWidth)
            point.setX(x)
        self.drawPath()

    def quantizeLines(self):
        for i in self.scene().items():
            if i.data(0) == 'quantizeLine':yield i

    def drawQuantizeLines(self):
        qList = self.grid.getQuantizeList()
        for i in self.quantizeLines(): self.scene().removeItem(i)
        for q in qList:
            line = QGraphicsLineItem()
            line.setPen(self.QuantizePen)
            line.setData(0,'quantizeLine')
            line.setLine(q,0,q,self.height())
            self.scene().addItem(line)

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
        # Append last point
        self.points.append(self.endPoint)
        # Add Last path element
        self.path.lineTo(self.endPoint.x(),self.endPoint.y())
        # Set the new path
        self.pathItem.setPath(self.path)

    def deleteSelectedPoints(self):
        for point in self.items():
            if self.isPoint(point) and point.isSelected():self.deletePoint(point)
        self.drawPath()

    def _addPoint(self, x, y):
        point = EnvPoint(self.pointRadius,self)
        point.setBounds(0,0,float(self.grid.width()),self.height())
        point.setSelectedBrush(self.selectedBrush)
        point.setSelectedPen(self.selectedPen)
        point.setDeSelectedBrush(self.deSelectedBrush)
        point.setDeSelectedPen(self.deSelectedPen)
        point.moveTo(x,y)
        self.points.append(point)
        self.scene().addItem(point)
        self.drawPath()
        return point

    def updateCrosshair(self, event):
        if self.useCrosshair:
            p = event.position()
            item = self.pointToMove or self.itemAt(p.x(),p.y())
            if self.isPoint(item):
                self.crossH.show()
                self.crossV.show()
                self.crossH.setLine(0,item.y(),self.rect().width(),item.y())
                self.crossV.setLine(item.x(),0,item.x(),self.height())
            else:
                self.crossH.hide()
                self.crossV.hide()

    def deSelectPoints(self):
        for item in self.scene().items():
            if self.isPoint(item):item.setSelected(False)

    def selectAllPoints(self):
        for item in self.scene().items():
            if self.isPoint(item):item.setSelected(True)

    def invertPointSelection(self):
        for item in self.scene().items():
            if self.isPoint(item):item.toggleSelected()

    def setSnapLists(self):
        self.pointToMove.setSnapXList([])
        self.pointToMove.setSnapYList([])
        # X Snapping (Grid Quantize)
        if self.useQuantize:
            for i in self.quantizeLines(): self.pointToMove.snapListX.append(i.line().x1())
        # Y Snapping
        if self.useSnapping:
            self.pointToMove.snapListY.append(self.getCenter())
            for p in self.pointToMove.getDeSelectedSiblings(): self.pointToMove.snapListY.append(p.y())

    # Events ###############################################
    def pointMoved(self, d):
        pass

    def mouseMoveEvent(self, event):
        QGraphicsView.mouseMoveEvent(self, event)
        if self.selectBox.isVisible():
            # Draw Selection Box
            x = event.position().x()
            y = event.position().y()
            sb = self.selectBox
            h=w=0
            if x > sb.x():
                w = x-sb.x()
                x = 0
            else:
                w = sb.x()-x
                x = x-sb.x()
            if y > sb.y():
                h = y-sb.y()
                y = 0
            else:
                h = sb.y()-y
                y = y-sb.y()
            sb.setRect(x,y,w,h)
            # toggle select all point items inside the select box
            currInList = sb.collidingItems()
            prevInList = self.selectBox.data(0)
            for item in currInList:
                if self.isPoint(item):
                    if item not in prevInList:
                        item.setSelected(True)
                        prevInList.append(item)
                        self.selectBox.setData(0, prevInList)
            for item in self.items():
                if self.isPoint(item) and item not in currInList:
                    if item in prevInList:
                        prevInList.remove(item)
                        self.selectBox.setData(0, prevInList)
                        item.setSelected(not item.isSelected())
            return
        self.updateCrosshair(event)
        self.drawPath()

    def mousePressEvent(self, event):
        QGraphicsView.mousePressEvent(self, event)
        p = event.position()
        item = self.itemAt(p.x(),p.y())
        if self.isPoint(item):
            if event.button() == Qt.LeftButton:
                if event.modifiers()==Qt.ControlModifier:
                    for i in self.prevSelectedItems:i.setSelected(True)
                else:
                    self.pointToMove = item
                    self.setSnapLists()
            elif event.button() == Qt.RightButton:
                self.deletePoint(item)
                self.drawPath()
            return
        self.selectBox.setData(0, [])
        self.selectBox.show()
        self.selectBox.setRect(0,0,5,5)
        self.selectBox.setPos(p.x(),p.y())

    def mouseDoubleClickEvent(self, event):
        QGraphicsView.mouseDoubleClickEvent(self, event)
        p = event.position()
        self.pointToMove = self._addPoint(p.x(),p.y())
        # self.setSnapLists()

    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)
        if self.pointToMove: self.pointToMove = None
        self.prevSelectedItems = self.scene().selectedItems()
        # if not len(self.scene().selectedItems()):self.deSelectPoints()
        self.updateCrosshair(event)
        self.selectBox.hide()
        # Delete points with same position
        for item in self.items():
            for otherItem in self.items():
                if self.isPoint(otherItem) and otherItem!=item:
                    if item.x() == otherItem.x() and item.y() == otherItem.y():
                        self.deletePoint(item)
        self.drawPath()

    def resizeEvent(self, event):
        gridWidth = float(self.grid.width())
        self.setSceneRect(0,0,gridWidth,self.rect().height()-self.horizontalScrollBar().height())
        midHeight = self.getCenter()
        self.defLine.setLine(0,midHeight,self.rect().right(),midHeight)
        if self.useQuantize: self.drawQuantizeLines()
        self.adjustPointsY()
        QGraphicsView.resizeEvent(self, event)

    def keyPressEvent(self, event):
        QGraphicsView.keyPressEvent(self, event)
        # Delete selected
        if event.key()==Qt.Key_Delete:
            self.deleteSelectedPoints()
        # Ctrl+Shift+A (Invert Selection)
        if event.modifiers()==(Qt.ShiftModifier|Qt.ControlModifier) and event.key()==Qt.Key_A:
            self.invertPointSelection()
        # Ctrl+A (Select All)
        elif event.modifiers()==Qt.ControlModifier and event.key()==Qt.Key_A:
            self.selectAllPoints()
        # Shift+A (De-Select All)
        elif event.modifiers()==Qt.ShiftModifier and event.key()==Qt.Key_A:
            self.deSelectPoints()

        # Grid Tests
        if event.key()==Qt.Key_Plus:
            newBpm = self.grid.bpm()+10
            print('BPM:',newBpm)
            self.grid.setBpm(newBpm)
        if event.key()==Qt.Key_Minus:
            newBpm = self.grid.bpm()-10
            print('BPM:',newBpm)
            self.grid.setBpm(newBpm)


if __name__ == '__main__':
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

    env = Envelope()
    env.setStyleSheet("""
    background-color: rgb(80, 80, 80);
    """)
    # Setting brush for all de-selected points
    env.setDeSelectedBrush(QBrush(Qt.blue))
    # Adding some points with a sin function
    # also settings this points de-selected brush as addPoint() returns the point
    for i in range(80): env.addPoint((i+5)*9,math.sin(i)*15).setDeSelectedBrush(QBrush(QColor(255,0,0)))
    # adding and storing a point in a variable
    point = env.addPoint(25,100)# x=25, value=100
    # moving point to x=250, value=-100
    env.movePoint(point, 250, -100)
    # setting point de-selected Pen (outline)
    point.setDeSelectedPen(QPen(Qt.yellow,5))
    # setting point selected Pen (outline)
    point.setSelectedPen(QPen(Qt.red,10))

    l.addWidget(env,1,0)

    # Adding layout to the window
    window.setLayout(l)

    # Showing the window
    window.show()

    exit(app.exec())
