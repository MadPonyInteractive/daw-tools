'''
A helper class for creating ellipse items
    Mainly used for points in envelopes

You can lock axis by using setLockX(bool) and setLockY(bool)
The moveTo(x,y), moveBy(x,y), moveX(x) and moveY(y) methods will respect the locks
You can still use setPos(x,y), setX(x) and setY(y) methods to set the default locked positions
    as these ignore the setLockX and setLockY methods

You should set bounds by using setBounds(x,y,width,height)
All move and set methods will respect bounds

The mouseMove event will snap the grabbed item to the snap lists but not it's selected siblings

'''
if __name__ == '__main__':
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    import music_functions as mf
    from decimal import Decimal as D
else:
    try:
        from . main import *
    except:
        from main import *

class Point(QGraphicsEllipseItem):
    def __init__(self, radius=30, parent=None):
        QGraphicsEllipseItem.__init__(self, -radius*.5, -radius*.5, radius, radius, parent=None)
        self.parent = parent
        self.radius = radius
        self.selectedBrush = QBrush(QGradient.DustyGrass)# https://webgradients.com/
        self.selectedPen = QPen(Qt.gray,  2, Qt.SolidLine)
        self.deSelectedBrush = QBrush(QGradient.CleanMirror)# https://webgradients.com/
        self.deSelectedPen = QPen(Qt.gray,  2, Qt.SolidLine)
        self.setBrush(self.deSelectedBrush)
        self.setPen(self.deSelectedPen)
        self.setZValue(2)
        self.setFlags(self.ItemClipsToShape|self.ItemSendsGeometryChanges|self.ItemIsSelectable)
        self.setCursor(Qt.ArrowCursor)# Setting cursor forces mouse move on QGraphicsView
        self._prevState = False
        self.useSnapping = True
        self.lockX = False
        self.lockY = False
        self.bounds = {}
        self.snapListX = []
        self.snapListY = []
        self.snapValue = 15
        self.pressed = False
        self.changedPrevPos = None
        self.prevPos = None
        self.nX = None
        self.nY = None

    def value(self): return self.data(3)
    def setSnapValue(self, v): self.snapValue = v
    def setLockX(self, b): self.lockX = b
    def setLockY(self, b): self.lockY = b
    def setUseSnapping(self,b): self.useSnapping = b
    def setSnapXList(self,snapList): self.snapListX = snapList
    def setSnapYList(self,snapList): self.snapListY = snapList

    def setSelectedBrush(self,b):
        self.selectedBrush = b
        if self.isVisible(): self.setSelected(self.isSelected())
    def setSelectedPen(self,p):
        self.selectedPen = p
        if self.isVisible(): self.setSelected(self.isSelected())
    def setDeSelectedBrush(self,b):
        self.deSelectedBrush = b
        if self.isVisible(): self.setSelected(self.isSelected())
    def setDeSelectedPen(self,p):
        self.deSelectedPen = p
        if self.isVisible(): self.setSelected(self.isSelected())

    def setSelection(self,b):
        if b:
            self.setBrush(self.selectedBrush)
            self.setPen(self.selectedPen)
        else:
            self.setBrush(self.deSelectedBrush)
            self.setPen(self.deSelectedPen)
        self._prevState = b

    def toggleSelected(self):self.setSelected(not self.isSelected())

    def prevState(self):return self._prevState

    def normals(self):
        nX = D(str(mf.map_val(self.x(),0,self.bounds['w'],0,1)))
        nY = D(str(mf.map_val(self.y(),0,self.bounds['h'],0,1)))
        return (float(nX), float(nY))

    def paint(self, painter, option, w=None):
        option.state = QStyle.State_None
        QGraphicsEllipseItem.paint(self, painter, option, w)
        # return super(Point, self).paint(painter,option)

    def isSibling(self, item): return 'Point' in str(type(item)) and item != self

    def getSiblings(self):
        for item in self.scene().items():
            if self.isSibling(item): yield item

    def getSelectedSiblings(self):
        for item in self.getSiblings():
            if item.isSelected(): yield item

    def getDeSelectedSiblings(self):
            for item in self.getSiblings():
                if not item.isSelected(): yield item

    def setBounds(self,*a):
        if type(a[0])==int or type(a[0])==float:
            self.bounds['x'] = a[0]
            self.bounds['y'] = a[1]
            self.bounds['w'] = a[2]
            self.bounds['h'] = a[3]
        else:
            self.bounds['x'], self.bounds['y'], self.bounds['w'], self.bounds['h'] = a[0].x(), a[0].y(), a[0].width(), a[0].height()

    def setXBounds(self, x, w):
        self.bounds['x'] = x
        self.bounds['w'] = w

    def setYBounds(self, y, h):
        self.bounds['y'] = y
        self.bounds['h'] = h

    def withinBounds(self,point):
        return point.x() <= self.bounds['w'] and point.x() >= self.bounds['x'] \
        and point.y() <= self.bounds['h'] and point.y() >= self.bounds['y']

    def withinXBounds(self,point):
        return point.x() <= self.bounds['w'] and point.x() >= self.bounds['x']

    def withinYBounds(self,point):
        return point.y() <= self.bounds['h'] and point.y() >= self.bounds['y']

    def filterXY(self,a):
        if type(a[0])==int or type(a[0])==float:
            x = a[0]
            y = a[1]
        else:
            x, y = a[0].x(), a[0].y()
        return x,y

    def moveX(self,x):
        if self.lockX: return
        self.moveTo(x,self.y())

    def moveY(self,y):
        if self.lockY: return
        self.moveTo(self.x(),y)

    def moveTo(self,*a):
        x,y = self.filterXY(a)
        if self.lockX and self.lockY: return
        elif self.lockX: self.setY(y)
        elif self.lockY: self.setX(x)
        else: self.setPos(x,y)

    def moveBy(self,*a):
        x,y = self.filterXY(a)
        x += self.x()
        y += self.y()
        self.moveTo(x,y)

    def mouseMoveEvent(self, event):
        QGraphicsEllipseItem.mouseMoveEvent(self, event)
        if self.pressed:
            mousePos = event.scenePos()
            movedBy = event.pos()

            # X snap
            if len(self.snapListX) and self.useSnapping:
                snap = mf.get_closest_number(mousePos.x(),self.snapListX)
                if abs(mousePos.x()-snap)<self.snapValue:mousePos.setX(snap)
            # Y snap
            if len(self.snapListY) and self.useSnapping:
                snap = mf.get_closest_number(mousePos.y(),self.snapListY)
                if abs(mousePos.y()-snap)<self.snapValue:mousePos.setY(snap)

            self.moveTo(mousePos)
            for s in self.getSelectedSiblings():
                offset = (mousePos-self.prevMousePos)+s.prevPos
                x = max(min(offset.x(),s.bounds['w']),s.bounds['x'])
                y = max(min(offset.y(),s.bounds['h']),s.bounds['y'])
                s.moveTo(x,y)

    def mousePressEvent(self, event):
        self.pressed = True
        self.prevPos = self.pos()
        self.prevMousePos = event.scenePos()
        for s in self.getSelectedSiblings():s.prevPos = s.pos()
        QGraphicsEllipseItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.pressed = False
        QGraphicsEllipseItem.mouseReleaseEvent(self, event)

    def itemChange(self, change , value):
        # print(change)
        if change == self.ItemPositionChange and self.scene():
            x = value.x()
            y = value.y()
            if len(self.bounds):
                x = min(max(x,self.bounds['x']),self.bounds['w'])
                y = min(max(y,self.bounds['y']),self.bounds['h'])
            value.setX(x)
            value.setY(y)
            if self.changedPrevPos == value:return value
            if self.parent != None:
                if hasattr(self.parent, 'positionChanged'):
                    self.parent.positionChanged.emit({'point':self,'pos':value})
            self.changedPrevPos = value
            return value
        if change == self.ItemSelectedHasChanged:self.setSelection(value)
        if change == self.ItemVisibleHasChanged:
            if value: self.setSelection(self.isSelected())
        return super(Point, self).itemChange(change, value)
