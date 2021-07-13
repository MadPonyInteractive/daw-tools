'''
Range Slider
    A basic range slider with 2 handles
    Accepts and outputs range values from 0 to 1
    The output is a dictionary as such:
    {
        'start':0.0,
        'end':1.0,
        'range':1.0
    }

    ! Example at the end of the module

    Still under construction:
        TODO: Grabbing the range/fill still causes some issues
                Find a better solution for it
        TODO: Implement Vertical orientation
        TODO if needed: Wheel and Keyboard Events
'''
if __name__ == '__main__':
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from decimal import Decimal as D
    from decimal import ROUND_HALF_UP
    import music_functions as mf
else:
    try:
        from . main import *
    except:
        from main import *

class RangeSliderItem(QGraphicsRectItem):
    def __init__(self, rangeStart=0.0, rangeEnd=1.0, parent=None):
        QGraphicsRectItem.__init__(self, 0, 0, 10, 10, parent=None)
        self.setAcceptHoverEvents(True)
        self.rangeStart = rangeStart
        self.rangeEnd = rangeEnd
        self.lastRange =[rangeStart,rangeEnd]
        self.noPen = QPen(QColor(0,0,0,0))
        self.setBrush(QColor(0,0,0,0))
        self.setPen(self.noPen)
        self.handleColor = QColor(100,100,100)
        self.rangeColor = QColor(180,180,180)
        self.handle_l = None
        self.handle_r = None
        self.handle_l_grabbed = False
        self.handle_r_grabbed = False
        self.range_grabbed = False
        self.range = None
        self.rangeY = 0
        self.crossed = False
        self.out =  {'start':0.0,'end':0.0,'range':0.0}
        self.callbacks = []
        self.rangeHeight = 0
        self.handleSize = [40,0]
        self.precision = 0.001
        self.steps = 0
        self.step_list = []
        self.step_size = None
        self.drawRange()
        self.drawLeftHandle()
        self.drawRightHandle()

    # def showEvent(self, event):
    #     self.setHandleSize(self.handleSize[0],self.handleSize[1] or self.height())
    #     return super(RangeSliderItem, self).showEvent(event)

    # Setters #####################################
    def setRange(self, rangeStart, rangeEnd):
        ''' 0.0 to 1.0 range '''
        self.setRangeStart(rangeStart)
        self.setRangeEnd(rangeEnd)

    def setRangeStart(self, l, reset=False):
        ''' 0.0 to 1.0 range '''
        if not reset:self.lastRange[0]=l
        self.rangeStart = self.mapI(l)
        x = self.rangeStart-D(self.handleSize[0]*.5)
        self.handle_l.setX(x)
        self.setHandles()

    def setRangeEnd(self, r, reset=False):
        ''' 0.0 to 1.0 range '''
        if not reset:self.lastRange[1]=r
        self.rangeEnd = self.mapI(r)
        x = self.rangeEnd-D(self.handleSize[0]*.5)
        self.handle_r.setX(x)
        self.setHandles()

    def resetRange(self):
        w = self.handleSize[0]
        h = self.handleSize[1] or self.height()
        self.handle_l.setRect(0,0,w,h)
        self.handle_r.setRect(0,0,w,h)
        for i, c in enumerate(self.handle_l.childItems()):
            c.setRect(0,0,w*.5,h)
            c.setPos(i*w*.5,0)
        for i, c in enumerate(self.handle_r.childItems()):
            c.setRect(0,0,w*.5,h)
            c.setPos(i*w*.5,0)
        self.setRangeStart(self.lastRange[0],True)
        self.setRangeEnd(self.lastRange[1],True)
        self.makeStepList()

    def setHandleSize(self, w, h):
        self.handleSize = [w,h]
        self.handle_l.setRect(0,0,w,h)
        self.handle_r.setRect(0,0,w,h)
        for i, c in enumerate(self.handle_l.childItems()):
            c.setRect(0,0,w*.5,h)
            c.setPos(i*w*.5,0)
        for i, c in enumerate(self.handle_r.childItems()):
            c.setRect(0,0,w*.5,h)
            c.setPos(i*w*.5,0)
        self.setHandles()

    def setHandleWidth(self, w):
        self.setHandleSize(w,self.handleSize[1])

    def setHandleHeight(self, h):
        self.setHandleSize(self.handleSize[0],h)

    def setFillHeight(self, h):
        self.rangeHeight = h
        r = self.range.rect()
        self.range.setRect(0,0,r.width(),h)

    def setFillY(self, y):
        self.rangeY = y
        self.range.setY(y)

    def setPrecision(self, precision):
        self.precision = precision

    def setSteps(self, steps):
        self.steps = steps
        self.makeStepList()

    def setStepSize(self, size):
        self.step_size = size
        self.makeStepList()

    def setRightHandleColor(self, color):
        self.handle_l.childItems()[0].childItems()[0].setBrush(color)
        self.handle_r.childItems()[0].childItems()[0].setBrush(color)

    def setRightHandleBgColor(self, color):
        self.handle_l.childItems()[0].setBrush(color)
        self.handle_r.childItems()[0].setBrush(color)

    def setRightHandleFont(self, font):
        self.handle_l.childItems()[0].childItems()[0].setFont(font)
        self.handle_r.childItems()[0].childItems()[0].setFont(font)

    def setRightHandleText(self, text):
        self.handle_l.childItems()[0].childItems()[0].setText(text)
        self.handle_r.childItems()[0].childItems()[0].setText(text)

    def setLeftHandleColor(self, color):
        self.handle_l.childItems()[1].childItems()[0].setBrush(color)
        self.handle_r.childItems()[1].childItems()[0].setBrush(color)

    def setLeftHandleBgColor(self, color):
        self.handle_r.childItems()[1].setBrush(color)
        self.handle_l.childItems()[1].setBrush(color)

    def setLeftHandleFont(self, font):
        self.handle_r.childItems()[1].childItems()[0].setFont(font)
        self.handle_l.childItems()[1].childItems()[0].setFont(font)

    def setLeftHandleText(self, text):
        self.handle_r.childItems()[1].childItems()[0].setText(text)
        self.handle_l.childItems()[1].childItems()[0].setText(text)

    # Getters ######################################
    def getFill(self):return self.range
    def getStepSize(self):return self.width()/self.steps
    def isCrossed(self):return self.crossed

    # Internal Functions ###########################
    def width(self):
        return self.rect().width()

    def height(self):
        return self.rect().height()

    def mapI(self,val):
        x =  0 + ((D(str(self.width())) - 0) / (1 - 0)) * (D(str(val)) - 0)
        return x.quantize(D(str(self.precision)), ROUND_HALF_UP)

    def mapP(self,val):
        half_handle = self.handleSize[0]*0.5
        x = 0 + ((1 - 0) / (D(str(self.width())) - 0)) * (D(str(val)) - 0)
        return x.quantize(D(str(self.precision)), ROUND_HALF_UP)

    def makeInsideRect(self, parent, text, x):
        ''' RectItems inside handles'''
        rect = QGraphicsRectItem(0,0,self.handleSize[0]*.5,self.handleSize[1] or self.height(),parent)
        rect.setPos(x,0)
        rect.setBrush(self.handleColor)
        rect.setPen(self.noPen)
        rect.setZValue(3)
        txt = QGraphicsSimpleTextItem(text,rect)
        txt.setBrush(Qt.white)
        font = QFont()
        font.setPointSize(12)
        txt.setFont(font)

    def drawLeftHandle(self):
        self.handle_l = QGraphicsRectItem(0,0,self.handleSize[0],self.handleSize[1] or self.height(),self)
        self.handle_l.setBrush(QColor(0,0,0,0))
        self.handle_l.setPen(self.noPen)
        self.handle_l.setZValue(2)
        self.handle_l.setHandlesChildEvents(True)
        self.makeInsideRect(self.handle_l,'',0)# child 0
        self.makeInsideRect(self.handle_l,'',self.handleSize[0]*.5)# child 1

    def drawRightHandle(self):
        self.handle_r = QGraphicsRectItem(0,0,self.handleSize[0],self.handleSize[1] or self.height(),self)
        self.handle_r.setX(self.width()-self.handleSize[0])
        self.handle_r.setBrush(QColor(0,0,0,0))
        self.handle_r.setPen(self.noPen)
        self.handle_r.setZValue(2)
        self.handle_r.setHandlesChildEvents(True)
        self.makeInsideRect(self.handle_r,'',0)# child 0
        self.makeInsideRect(self.handle_r,'',self.handleSize[0]*.5)# child 1

    def drawRange(self):
        height = self.rangeHeight or self.height()
        self.range = QGraphicsRectItem(0,0,self.width(),height,self)
        self.range.setBrush(self.rangeColor)
        self.range.setPen(self.noPen)
        self.range.setZValue(1)

    def setHandles(self, mouse=False):
        half_handle = self.handleSize[0]*0.5
        xl = min(self.handle_r.x()+half_handle, self.handle_l.x()+half_handle)
        xr = max(self.handle_r.x()+half_handle, self.handle_l.x()+half_handle)
        if self.handle_l.x() > self.handle_r.x():
            self.crossed = True
            self.handle_l.childItems()[0].show()
            self.handle_l.childItems()[1].hide()
            self.handle_r.childItems()[1].show()
            self.handle_r.childItems()[0].hide()
        else:
            self.crossed = False
            self.handle_l.childItems()[1].show()
            self.handle_l.childItems()[0].hide()
            self.handle_r.childItems()[0].show()
            self.handle_r.childItems()[1].hide()
        rg = (xr-xl)
        self.range.setRect(0,0,rg,self.rangeHeight or self.height())
        self.range.setPos(xl,self.rangeY)
        out = {
            'start':float(str(self.mapP(xl))),
            'end':float(str(self.mapP(xr))),
            'range':float(str(self.mapP(rg)))
        }
        precisionReached = False
        p = self.precision
        if abs(self.out['start'] - out['start']) > p:precisionReached = True
        if abs(self.out['end'] - out['end']) > p:precisionReached = True
        if abs(self.out['range'] - out['range']) > p:precisionReached = True
        if precisionReached:self.out = out
        else:return
        if mouse:self.lastRange = [out['start'],out['end']]
        for callback in self.callbacks:
            if callback[0] == 'rangeChanged': callback[1](self.out)

    def makeStepList(self):
        if self.step_size==None and not self.steps:return
        if self.steps:self.step_size = self.width()/self.steps
        full_width = self.width()
        self.step_list = []
        width = 0
        while width <= full_width:
            self.step_list.append(width)
            width += self.step_size

    # Event Callbacks ##############################
    def rangeChanged(self,func):
        self.callbacks.append(('rangeChanged',func))

    def finishedEditting(self,func):
        self.callbacks.append(('finishedEditting',func))

    # Mouse Events #######################################
    def hoverMoveEvent(self, event):
        if self.handle_r.isUnderMouse():self.setCursor(Qt.SizeHorCursor)
        elif self.handle_l.isUnderMouse():self.setCursor(Qt.SizeHorCursor)
        elif self.range.isUnderMouse():self.setCursor(Qt.SizeAllCursor)
        else:self.setCursor(Qt.ArrowCursor)
        QGraphicsRectItem.hoverMoveEvent(self, event)

    def getBounds(self, val, handle=False):
        if handle:
            half_handle = self.handleSize[0]*.5
            return max(min(val,self.width()-half_handle),-half_handle)
        else:
            return max(min(val,self.width()),0)

    def mouseMoveEvent(self, event):
        half_handle = D(self.handleSize[0]*.5)
        if self.step_size:
            def getStepBound(h=None):
                mouse_pos=D(event.pos().x())
                xVal = D(mf.get_closest_number(mouse_pos, self.step_list))
                if h:
                    w=D(abs(self.lPrevX-self.rPrevX)*0.5)
                    if self.crossed:
                        w = xVal-w if h == 'r' else xVal+w
                    else:
                        w = xVal+w if h == 'r' else xVal-w

                    if mouse_pos < 0:
                        w = w+mouse_pos
                    elif mouse_pos > self.width():
                        extra = D(mouse_pos)-D(self.width())
                        w = w+extra

                    w = mf.get_closest_number(w, self.step_list)
                    return D(self.getBounds(w))
                else:
                    return D(self.getBounds(xVal))
        if self.handle_r_grabbed or self.handle_l_grabbed and not self.step_size:
            x = D(self.getBounds(event.pos().x()))
        if self.handle_r_grabbed:
            if self.step_size:
                x = getStepBound()
                self.handle_r.setX(x-half_handle)
            else:
                self.handle_r.setX(x-half_handle)
        elif self.handle_l_grabbed:
            if self.step_size:
                x = getStepBound()
                self.handle_l.setX(x-half_handle)
            else:
                self.handle_l.setX(x-half_handle)
        elif self.range_grabbed:
            x = event.pos().x()-self.prevMouseX
            if self.step_size:
                lx = getStepBound('l')
                rx = getStepBound('r')
                x = event.pos().x()
                self.handle_l.setX(lx-half_handle)
                self.handle_r.setX(rx-half_handle)
            else:
                lx = self.getBounds(x+self.lPrevX,True)
                rx = self.getBounds(x+self.rPrevX,True)
                self.handle_l.setX(lx)
                self.handle_r.setX(rx)
        else:return
        if self.step_size:self.prevMouseX = x
        self.setHandles(True)

    def mousePressEvent(self, event):
        self.prevMouseX = event.pos().x()
        self.rPrevX = self.handle_r.x()
        self.lPrevX = self.handle_l.x()
        if self.handle_r.isUnderMouse():
            self.handle_r_grabbed = True
            self.handle_r.setZValue(3)
            self.handle_l.setZValue(2)
        elif self.handle_l.isUnderMouse():
            self.handle_l_grabbed = True
            self.handle_l.setZValue(3)
            self.handle_r.setZValue(2)
        elif self.range.isUnderMouse():self.range_grabbed = True

    def mouseReleaseEvent(self, event):
        self.handle_r_grabbed = False
        self.handle_l_grabbed = False
        self.range_grabbed = False
        QGraphicsRectItem.mouseReleaseEvent(self, event)
        for callback in self.callbacks:
            if callback[0] == 'finishedEditting':callback[1](self.out)

class RangeSlider(QGraphicsView):
    rangeChanged = Signal(dict)
    finishedEditting = Signal(dict)
    def __init__(self, rangeStart=0, rangeEnd=1, parent=None):
        QGraphicsView.__init__(self, parent=None)
        self.setScene(QGraphicsScene())
        self.slider = RangeSliderItem(rangeStart,rangeEnd,self)
        self.slider.rangeChanged(self._rangeChanged)
        self.slider.finishedEditting(self._finishedEditting)
        self.scene().addItem(self.slider)
        self.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        # self.setBackgroundBrush(QColor(60,60,60))
        self.resizing = False

    def __repr__(self):
        return f''' Range Slider
        A basic range slider with 2 handles
        '''

    def _rangeChanged(self,r):
        if self.isVisible() and not self.resizing: self.rangeChanged.emit(r)
    def _finishedEditting(self,r):
        if self.isVisible() and not self.resizing: self.finishedEditting.emit(r)
    def setPrecision(self,p):self.slider.setPrecision(p)
    def setHandleSize(self,w,h):self.slider.setHandleSize(w,h)
    def setHandleWidth(self,w):self.slider.setHandleWidth(w)
    def setHandleHeight(self,h):self.slider.setHandleHeight(h)
    def setRange(self,s,e):self.slider.setRange(s,e)
    def setRangeStart(self,s):self.slider.setRangeStart(s)
    def setRangeEnd(self,e):self.slider.setRangeEnd(e)
    def getFill(self):return self.slider.getFill()
    def isCrossed(self):return self.slider.isCrossed()
    def setFillHeight(self,h):self.slider.setFillHeight(h)
    def setFillY(self,y):self.slider.setFillY(y)
    def setSteps(self,steps):self.slider.setSteps(steps)
    def setLeftHandleColor(self,color):self.slider.setLeftHandleColor(color)
    def setRightHandleColor(self,color):self.slider.setRightHandleColor(color)
    def setLeftHandleBgColor(self,color):self.slider.setLeftHandleBgColor(color)
    def setRightHandleBgColor(self,color):self.slider.setRightHandleBgColor(color)
    def setLeftHandleFont(self,font):self.slider.setLeftHandleFont(font)
    def setRightHandleFont(self,font):self.slider.setRightHandleFont(font)
    def setLeftHandleText(self,text):self.slider.setLeftHandleText(str(text))
    def setRightHandleText(self,text):self.slider.setRightHandleText(str(text))
    def setStepSize(self,size):self.slider.setStepSize(size)

    def event(self, event):
        # print(event.type())
        if (event.type()==QEvent.Resize):
            self.resizing = True
            self.setSceneRect(self.rect())
            self.slider.setRect(self.rect())
            self.slider.resetRange()
            event.accept()
            self.resizing = False
        return super(RangeSlider, self).event(event)

'''
Bellow there's an usage example.
You can comment out some of the settings to test functionality
'''
if __name__ == '__main__':
    # Creating the application
    app = QApplication([])

    # Creating the display window
    window = QMainWindow()
    window.setWindowTitle('Range Slider')
    window.setMinimumSize(300,50)

    # Creating and setting up the slider
    slider = RangeSlider(0.2,0.8)# start range, end range
    # slider.setRange(0.2,0.8)# start range, end range
    # slider.setRangeStart(0.2)
    # slider.setRangeEnd(0.8)
    slider.setHandleSize(70,25)# width, height
    # slider.setHandleWidth(70)
    # slider.setHandleHeight(25)
    # slider.setFillHeight(45)
    # slider.setFillY(30)
    slider.setPrecision(0.01)
    slider.setSteps(10)
    # slider.setStepSize(30)

    # Left Handle
    slider.setLeftHandleBgColor(QColor(120,0,0))
    slider.setLeftHandleColor(QColor(255,255,255))# Text color
    fontL = QFont('Serif',14,1,True)
    slider.setLeftHandleFont(fontL)
    slider.setLeftHandleText('L')

    # Right Handle
    slider.setRightHandleBgColor(QColor(0,120,0))
    slider.setRightHandleColor(QColor(255,255,255))# Text color
    fontR = QFont('Serif',14,1,True)
    slider.setRightHandleFont(fontR)
    slider.setRightHandleText('R')

    # Change background
    slider.setBackgroundBrush(QColor(0,60,0))

    # get the fill bar
    f = slider.getFill()
    f.setBrush(QColor(0,255,0))# Set fill color

    # Event Callbacks
    def change(d):
        print('changed:',d)
        slider.setLeftHandleText(round(d['start']*100))
        slider.setRightHandleText(round(d['end']*100))
        if slider.isCrossed():# checking crossed range
            f.setBrush(Qt.red)
        else:
            f.setBrush(Qt.green)
    slider.rangeChanged.connect(change)

    def finished(d):print('finished:',d)
    slider.finishedEditting.connect(finished)


    # # Adding the slider to the window
    window.setCentralWidget(slider)

    # Showing the window
    window.show()
    exit(app.exec())
