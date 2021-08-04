try:
    from . main import *
    from . import music_functions as mf
    from . grid import Grid
except:
    from main import *
    import music_functions as mf
    from grid import Grid

class Playhead(QGraphicsView):
    playPosChanged = Signal(float)
    def __init__(self, height=30, grid=None):
        QGraphicsView.__init__(self)
        if not grid:
            warnings.warn("No 'Grid' passed, creating one.")
            try:
                grid = Grid(bpm=60,bars=1)
            except:
                raise ValueError("Couldn't import the grid module!")
        self.grid = grid
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.height = height
        self.playPos = 0
        self.setBackgroundBrush(QColor(60,60,60))
        self.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.drawLines()
        self.drawPlayHead()
        self.setPlayPos()
        self.grid.widthChanged(self.redraw)
        self.grid.timeSignatureChanged(self.redraw)
        self.grid.quantizeChanged(self.redraw)

        self.grid.setQuantize(value='1/8',_type='straight')

    def redraw(self,w):
        self.scene.clear()
        self.drawLines()
        self.drawPlayHead()
        self.setPlayPos()

    def drawLines(self):
        pos = self.grid.getPositions()
        for p in pos['bars']: self.drawGridLine('bar', p, self.height*.8)
        for p in pos['beats']: self.drawGridLine('beat', p, self.height*.2)
        for p in pos['quantize']: self.drawGridLine('quantize', p, self.height*.5)

    def drawGridLine(self,*a):
        # print(a[0],a[1],a[2])
        pen = QPen(Qt.white,1) if a[0] != 'quantize' else QPen(Qt.red,1)
        self.scene.addLine(a[1], 0, a[1], a[2], pen)
        if a[0] == 'bar':
            t = self.scene.addText('bar', QFont("Times", 10, QFont.Bold))
            t.setDefaultTextColor(Qt.white)
            t.setPos(a[1],self.height*.4)

    def drawPlayHead(self):
        self.playHead = self.scene.addLine(0, 0, 0, self.rect().height(), QPen(Qt.red,3))
        self.playHead.setZValue(3)

    def setPlayPos(self, pos=None):
        if pos != None:self.playPos = pos
        pos = D(self.playPos)*self.grid.frameWidth()
        self.playHead.setLine(pos, 0, pos, self.rect().height())

    def mousePressEvent(self, event):
        mp = D(event.position().x())
        quantize_list = self.grid.getQuantizeList()
        mp = mf.get_closest_number(mp, quantize_list)
        mp = mf.map_val(mp,0,self.grid.width(),0,self.grid.frames())
        self.setPlayPos(mp)
        self.playPosChanged.emit(self.playPos)

if __name__ == '__main__':
    # Creating the application
    app = QApplication([])
    # Creating the display window
    window = QMainWindow()
    window.setWindowTitle('Playhead')
    window.setMinimumSize(300,50)

    playhead = Playhead()

    # # Adding the playhead to the window
    window.setCentralWidget(playhead)

    # Showing the window
    window.show()
    exit(app.exec())

