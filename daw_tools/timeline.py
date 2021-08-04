'''
This module name might be misleading for lack of a better term.

In it's essence it is a viewport for arrange able items.

It is meant for multiple applications:
* A piano roll viewport where you can arrange its notes
* A timeline viewport where you can arrange patterns and change track order
* A sequencer viewport

'''
try:
    from . main import *
    from . import music_functions as mf
    from . grid import Grid
except:
    from main import *
    import music_functions as mf
    from grid import Grid


class TimelineItem(QGraphicsRectItem):
    def __init__(self, width, height, parent):
        QGraphicsRectItem.__init__(self, 0, 0, width, height, parent)
        self.setZValue(2)


class TimelineScene(QGraphicsScene):
    def __init__(self,grid):
        QGraphicsScene.__init__(self)
        self.grid = grid
        self.gridRect = None
        self.pens = {
            'bar': QPen(QColor(255, 255, 255, 120), 3),
            'quantize': QPen(QColor(255, 255, 255, 80), 2),
            'beat': QPen(QColor(255, 255, 255, 40)),
            'play_head': QPen(QColor(255, 0, 0, 200),3),
            'clear': QPen(QColor(0, 0, 0, 0),0)
        }
        self.playHead = None
        self.playHeadSpeed = 10
        self.playPos = 0
        self.playing = False
        self.height = 0
        self.rows = []
        self.row_height = 50
        self.columns = {}
        self.setSceneRect(0,0,self.grid.width(),self.row_height)
        self.drawPlayHead()

    def setPlayPos(self, pos=None):
        if pos != None:self.playPos = pos
        # self.grid.pixelMultiplier()
        pos = D(self.playPos)*self.grid.frameWidth()
        self.playHead.setLine(pos, 0, pos, self.views()[0].rect().height())

    def drawPlayHead(self):
        self.playHead = QGraphicsLineItem(0, 0, 0, self.height, self.gridRect)
        self.playHead.setPen(self.pens['play_head'])
        self.playHead.setZValue(3)
        self.addItem(self.playHead)

    def drawGridLine(self,*a):
        line = QGraphicsLineItem(0, 0, 0, a[2], self.gridRect)
        pen = self.pens[a[0]]
        line.setPos(a[1], 0)
        line.setPen(pen)

    def drawGrid(self):
        # print('Drawing Grid')
        if self.gridRect: self.removeItem(self.gridRect)
        # Grid container
        self.gridRect = QGraphicsRectItem(0, 0, self.grid.width(), self.height)
        self.gridRect.setPen(self.pens['clear'])
        self.gridRect.setZValue(1.0)
        self.addItem(self.gridRect)
        # Draw Lines
        pos = self.grid.getPositions()
        for p in pos['bars']: self.drawGridLine('bar', p, self.height)
        for p in pos['quantize']: self.drawGridLine('quantize', p, self.height)
        for p in pos['beats']: self.drawGridLine('beat', p, self.height)

    def addColumn(self,col_id,pos=0,width=100,opacity=1.0):
        self.columns[col_id] = {
            'pos':pos,
            'width':width,
            'opacity':opacity,
            'row_items':[]
        }
        for row_num, row in enumerate(self.rows):
            row_item = self.makeRowItem(row,pos,width,opacity)
            # row_item.setData(0,col_id)# Might come in handy
            self.columns[col_id]['row_items'].append(row_item)
            self.addItem(row_item)

    def removeColumn(self,col_id):
        if not self.columns.get(col_id,False): return False
        for row in self.columns[col_id]['row_items']: self.removeItem(row)
        del self.columns[col_id]

    def setColumn(self,col_id,pos=None,width=None,opacity=None):
        if not self.columns.get(col_id,False): return
        if pos:     self.columns[col_id]['pos'] = pos
        if width:   self.columns[col_id]['width'] = width
        if opacity: self.columns[col_id]['opacity'] = opacity
        for row in self.columns[col_id]['row_items']:
            r = row.rect()
            if pos: row.setPos(pos,r.y())
            if width: row.setRect(r.x(), r.y(), width, self.row_height)
            if opacity: row.setOpacity(opacity)

    def makeRowItem(self, r, x, w, opacity):
        row = QGraphicsRectItem(0, 0, w, self.row_height)
        row.setPos(x,r['y'])
        row.setOpacity(opacity)
        row.setBrush(r['color'])
        row.setPen(r['border_color'])
        return row

    def addRow(self, *args):
        '''
        Adds a new row and calls adjustSize
        If an integer is passed in *args it will insert the row
        at the given position and re order/position the rows bellows
        *args
        QColor
        int(Row Number)
        '''
        color = None
        row_num = None
        for arg in args:
            if type(arg) == int:
                row_num = arg
            else: color = arg
        color = color or QColor(100, 100, 100)
        row_amt = len(self.rows)
        row_num = row_num or row_amt
        if row_num != row_amt:
            # Adjust rows position below the inserted row
            for i, r in enumerate(self.rows):
                if i >= row_num: r['y'] += self.row_height
            self.adjustColRowPos()
        row = {
            'y':row_num*self.row_height,
            'color':color,
            'border_color':QPen(QColor(0,0,0,255))# Dev: or self.pens['clear'] or Allow for customization?
        }
        self.rows.insert(row_num,row)
        # If we already have columns, we add row_items to each column respectively
        for col in self.columns.values():
            row_item = self.makeRowItem(row,col['pos'],col['width'],col['opacity'])
            col['row_items'].insert(row_num,row_item)
            self.addItem(row_item)
        self.adjustSize()

    def removeRow(self, row_num):
        for col in self.columns.values():
            self.removeItem(col['row_items'][row_num])
            col['row_items'].pop(row_num)
        row = self.rows[row_num]
        self.rows.pop(row_num)
        self.adjustRowPos()
        self.adjustSize()

    def moveRow(self, from_row, to_row):
        for col in self.columns.values():
            row = col['row_items'][from_row]
            col['row_items'].pop(from_row)
            col['row_items'].insert(to_row,row)
        row = self.rows[from_row]
        self.rows.pop(from_row)
        self.rows.insert(to_row,row)
        self.adjustRowPos()

    def adjustRowPos(self):
        ''' Adjust the y pos for rows '''
        for i, r in enumerate(self.rows): r['y'] = self.row_height*i
        self.adjustColRowPos()

    def adjustColRowPos(self):
        ''' Adjust the y pos for rows in all columns '''
        for col in self.columns.values():
            for i, row_item in enumerate(col['row_items']):
                row_item.setPos(col['pos'],self.rows[i]['y'])

    def resized(self, view, singleColumn=False):
        ''' Adjusts the rows width when in single row mode and the scene height '''
        self.adjustSize(view)
        # Adjust single row width
        if not singleColumn:return
        for col in self.columns.values():
            col['width'] = self.width
            for row in col['row_items']:
                r = row.rect()
                row.setRect(r.x(), r.y(), self.width, self.row_height)

    def columnsHeight(self):
        return self.row_height*len(self.rows)

    def adjustSize(self, view=None):
        ''' Adjusts the SceneRect size '''
        view = view or self.views()[0].rect()
        self.width = max(view.width(),self.grid.width())
        self.height = max(view.height(),self.columnsHeight())
        self.setSceneRect(0,0,self.width,self.height)
        self.adjustGrid()

    def adjustGrid(self):
        ''' Adjust grid lines and play head height '''
        # Draw Grid if not drawn yet
        if not self.gridRect:
            self.drawGrid()
            return
        self.setPlayPos()
        # Adjust Grid Lines
        lines = self.gridRect.childItems()
        for l in lines: l.setLine(0, 0, 0, self.height)
        self.gridRect.setRect(0, 0, self.grid.width(), self.height)

class Timeline(QGraphicsView):
    def __init__(self, grid=None):
        QGraphicsView.__init__(self)
        if not grid:
            warnings.warn("No 'Grid' passed, creating one.")
            try:
                grid = Grid()
            except:
                raise ValueError("Couldn't import the grid module!")
        self.setScene(TimelineScene(grid))
        self.setBackground()
        self.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.singleColumn = False
        self.columns_added = 0
        self.scene().grid.widthChanged(self.resized)

    def __repr__(self):
        return f"""Class: Timeline
        Rows:{len(self.scene().rows)}
        Columns:{len(self.scene().columns)}"""

    def setBackground(self, color=None):
        ''' QColor '''
        color = color or QColor(30,30,30)
        self.setBackgroundBrush(color)

    def setSingleColumn(self, singleColumn=True): self.singleColumn = singleColumn

    # Scene Redirects
    def tick(self):self.scene().tick()
    def setExternalClock(self, val=True):self.scene().setExternalClock(val)
    def grid(self):return self.scene().grid
    def addRow(self, *args):self.scene().addRow(*args)
    def removeRow(self,row):self.scene().removeRow(row)
    def moveRow(self,*args):self.scene().moveRow(*args)
    def addItem(self, data):self.scene().addItem(data)
    def removeItem(self, data):self.scene().removeItem(data)
    def setRowWidth(self, width):self.scene().setRowWidth(width)
    def removeColumn(self,col_id):self.scene().removeColumn(col_id)
    def setColumn(self,*args, **kwargs):self.scene().setColumn(*args, **kwargs)
    # Indirect Scene Redirects
    def setRowHeight(self, height=50):self.scene().row_height = height
    def addColumn(self,col_id,pos=0,width=100,opacity=1.0):
        if self.singleColumn and self.columns_added:return False
        self.columns_added += 1
        self.scene().addColumn(col_id,pos,width,opacity)
    def resized(self):
        self.scene().resized(self.rect(), self.singleColumn)
    def event(self, event):
        # print(event.type())
        # Resize Event
        if (event.type()==QEvent.Resize):
            self.resized()
            event.accept()
        return super(Timeline, self).event(event)

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    app = QApplication([])

    import grid
    main_grid = grid.Grid(bars=3,beats=1,time_signature='4/4',bpm=120)

    tl = Timeline(main_grid)

    print(tl.grid())
    # tl.setFixedSize(900,900)# PySide6 QGraphicsView methods are available

    # setSingleColumn only allows for 1 column to be set
    # This is useful for when working with a pattern timeline
    # For sequencers or piano rolls (pattern contents) it should not be set
    # tl.setSingleColumn()

    tl.setRowHeight(50)
    tl.addRow(QColor(100,100,100))
    tl.addRow(QColor(80,80,80))
    tl.addRow(QColor(100,100,100))
    tl.addRow(QColor(80,80,80))
    tl.addRow(QColor(100,100,100))
    tl.addRow(QColor(80,80,80))
    tl.addRow(QColor(100,100,100))
    tl.addRow(QColor(100,100,100))
    tl.addRow(QColor(80,80,80))
    tl.addRow(QColor(100,100,100))
    tl.addRow(QColor(80,80,80))
    tl.addRow(QColor(100,100,100))

    tl.addColumn(col_id='Track 1',pos=0,width=200,opacity=1)

    # Add/Remove/Set Columns test
    # tl.addColumn(col_id,pos,width,opacity)
    QTimer.singleShot(500,lambda: tl.addColumn(col_id='Track 2',pos=300,width=200,opacity=1))
    # tl.setColumn(col_id,pos,width,opacity)
    QTimer.singleShot(500,lambda: tl.setColumn(col_id='Track 1',opacity=.2))
    # tl.removeColumn(col_id)
    QTimer.singleShot(1500,lambda: tl.removeColumn('Track 1'))


    # Add/Move/Remove Rows Test
    QTimer.singleShot(1000,lambda: tl.addRow(QColor(100,0,0),6))
    QTimer.singleShot(2000,lambda: tl.moveRow(6,2))
    QTimer.singleShot(3000,lambda: tl.removeRow(2))

    print(tl)


    tl.show()
    exit(app.exec())
