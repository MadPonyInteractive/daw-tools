"""
A piano roll viewer/editor

"""

from PyQt4 import QtGui, QtCore

global_note_height = 10
global_note_count = 120
global_piano_keys_width = 34
global_header_height = 20

#things that get changed
global_total_height = 1000
global_grid_width = 0
global_snap = True
global_snap_value = 0
global_time_sig = [6.0, 4.0]
global_quantize_val = '1/8'

def setQuantize(value):
    global global_quantize_val
    '''accepts a string'''
    try:
        val = map(float, value.split('/'))
        if len(val) == 1:
            quantize(val[0])
            global_quantize_val = value
        elif len(val) == 2:
            quantize(val[0] / val[1])
            global_quantize_val = value
        print global_quantize_val
    except:
        pass

def quantize(value):
    global global_snap
    global global_snap_value
    if not value:
        global_snap = False
        global_snap_value = None
    else:
        global_snap = True
        global_snap_value = \
                250. * value #/ global_time_sig[0] * global_time_sig[1] * value


def enforce_bounds(pos):
    if pos.x() < global_piano_keys_width:
        pos.setX(global_piano_keys_width)
    elif pos.x() > global_piano_keys_width + global_grid_width:
        pos.setX(global_piano_keys_width + global_grid_width)
    if pos.y() < global_header_height:
        pos.setY(global_header_height)
    elif pos.y() > global_total_height:
        pos.setY(global_total_height)
    return pos

def snap(pos_x, pos_y = None):
    if global_snap:
        pos_x = int((pos_x - global_piano_keys_width) / global_snap_value) \
                * global_snap_value + global_piano_keys_width
    if pos_y:
        pos_y = int((pos_y - global_header_height) / global_note_height) \
                * global_note_height + global_header_height
    return (pos_x, pos_y) if pos_y else pos_x

class note_item(QtGui.QGraphicsRectItem):
    '''a note on the pianoroll sequencer'''
    def __init__(self, length, note_height, note_num):
        QtGui.QGraphicsRectItem.__init__(self, 0, 0, length, note_height)
        clearpen = QtGui.QPen(QtGui.QColor(0,0,0,0))
        self.setPen(clearpen)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.o_brush = QtGui.QColor(100, 0, 0)
        self.hover_brush = QtGui.QColor(200, 200, 100)
        self.s_brush = QtGui.QColor(200, 100, 100)

        self.setBrush(self.o_brush)
        self.note_height = note_height
        self.note_num = note_num
        self.pressed = False
        self.moving_diff = False

    def paint(self, painter, option, widget=None):
        paint_option = option
        paint_option.state &= ~QtGui.QStyle.State_Selected
        QtGui.QGraphicsRectItem.paint(self, painter, paint_option, widget)

    def setSelected(self, boolean):
        QtGui.QGraphicsRectItem.setSelected(self, boolean)
        if boolean: self.setBrush(self.s_brush)
        else: self.setBrush(self.o_brush)

    def hoverEnterEvent(self, event):
        QtGui.QGraphicsRectItem.hoverEnterEvent(self, event)
        if not self.isSelected():
            self.setBrush(self.hover_brush)

    def hoverLeaveEvent(self, event):
        QtGui.QGraphicsRectItem.hoverLeaveEvent(self, event)
        if not self.isSelected():
            self.setBrush(self.o_brush)
        elif self.isSelected():
            self.setBrush(self.s_brush)

    def mousePressEvent(self, event):
        QtGui.QGraphicsRectItem.mousePressEvent(self, event)
        self.setSelected(True)
        self.pressed = True

    def mouseMoveEvent(self, event):
        pass

    def moveEvent(self, event):
        #have to fix offset problem
        offset = event.scenePos() - event.lastScenePos()
        self.move_pos = self.scenePos() + offset
        if self.moving_diff:
            self.move_pos +=  QtCore.QPointF(self.moving_diff[0],self.moving_diff[1])
        pos = enforce_bounds(self.move_pos)
        pos_x, pos_y = pos.x(), pos.y()
        pos_sx, pos_sy = snap(pos_x, pos_y)
        self.moving_diff = (pos_x-pos_sx, pos_y-pos_sy)
        self.setPos(pos_sx, pos_sy)

    def mouseReleaseEvent(self, event):
        QtGui.QGraphicsRectItem.mouseReleaseEvent(self, event)
        self.pressed = False
        if event.button() == QtCore.Qt.LeftButton:
            (pos_x, pos_y,) = snap(self.pos().x(), self.pos().y())
            self.setPos(pos_x, pos_y)
            new_note_start = (pos_x - global_piano_keys_width) * 0.001 * 4.0
            new_note_num = int(global_note_count - (pos_y - global_header_height) / global_note_height)
            self.moving_diff = False
            #print("note start: " + str(new_note_start))
            #print("MIDI number: " + str(new_note_num))

class piano_key_item(QtGui.QGraphicsRectItem):
    def __init__(self, width, height, parent):
        QtGui.QGraphicsRectItem.__init__(self, 0, 0, width, height, parent)
        clearpen = QtGui.QPen(QtGui.QColor(0,0,0,50))
        self.setPen(clearpen)
        self.width = width
        self.height = height
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.hover_brush = QtGui.QColor(200, 0, 0)
        self.click_brush = QtGui.QColor(255, 100, 100)
        self.pressed = False

    def hoverEnterEvent(self, event):
        QtGui.QGraphicsRectItem.hoverEnterEvent(self, event)
        self.o_brush = self.brush()
        self.setBrush(self.hover_brush)

    def hoverLeaveEvent(self, event):
        if self.pressed:
            self.pressed = False
            self.setBrush(self.hover_brush)
        QtGui.QGraphicsRectItem.hoverLeaveEvent(self, event)
        self.setBrush(self.o_brush)

    #def mousePressEvent(self, event):
    #    self.pressed = True
    #    self.setBrush(self.click_brush)

    def mouseMoveEvent(self, event):
        """this may eventually do something"""
        pass

    def mouseReleaseEvent(self, event):
        self.pressed = False
        QtGui.QGraphicsRectItem.mouseReleaseEvent(self, event)
        self.setBrush(self.hover_brush)

class piano_roll(QtGui.QGraphicsScene):

    '''the piano roll'''
    def __init__(self, time_sig = [4.,4.], num_measures = 4, grid_div = 4):
        QtGui.QGraphicsScene.__init__(self)
        global global_total_height
        global global_grid_width

        self.mousePos = QtCore.QPointF()

        self.padding = 2

        #width stuff
        self.time_sig = time_sig
        self.num_measures = float(num_measures)


        self.full_note_width = 250
        self.measure_width = self.full_note_width * self.time_sig[0]/self.time_sig[1]
        self.grid_width = self.measure_width * self.num_measures
        global_grid_width = self.grid_width
        self.grid_div = grid_div
        self.default_length = 1. / self.grid_div
        self.grid_div_str =  '1/8'
        self.value_width = self.measure_width / float(self.grid_div)

        #height stuff
        self.end_octave = 8
        self.start_octave = -2
        self.notes_in_octave = 12
        self.total_notes = (self.end_octave - self.start_octave) * self.notes_in_octave + 1
        self.note_height = global_note_height
        self.octave_height = self.notes_in_octave * self.note_height
        self.header_height = global_header_height
        self.piano_height = self.note_height * self.total_notes
        self.piano_width = global_piano_keys_width - self.padding
        self.piano_height = self.note_height * self.total_notes
        global_total_height = self.piano_height - self.note_height + global_header_height

        self.setBackgroundBrush(QtGui.QColor(100, 100, 100))
        self.notes = []
        self.selected_notes = []
        self.piano_keys = []
        self.ghost_vel = 100
        self.marquee_select = False
        self.insert_mode = False
        self.place_ghost = False
        self.ghost_note = None
        self.draw_piano()
        self.draw_header()
        self.draw_grid()

    # -------------------------------------------------------------------------
    # Callbacks

    def setTimeSig(self, time_sig):
        global global_time_sig
        global global_grid_width
        try:
            new_time_sig = map(float, time_sig.split('/'))
            if len(new_time_sig)==2:
                self.time_sig = new_time_sig
                global_time_sig = self.time_sig

                self.measure_width = self.full_note_width * self.time_sig[0]/self.time_sig[1]
                self.grid_width = self.measure_width * self.num_measures
                global_grid_width = self.grid_width
                self.value_width = self.measure_width / float(self.grid_div)

                self.setGridDiv()
                print 'y'
                self.refresh_scene()
        except:
            pass

    def setMeasures(self, measures):
        global global_grid_width
        try:
            self.num_measures = float(measures)
            self.grid_width = self.measure_width * self.num_measures
            global_grid_width = self.grid_width
            self.refresh_scene()
        except:
            pass

    def setDefaultLength(self, length):
        try:
            v = map(float, length.split('/'))
            if len(v) < 3:
                self.default_length = \
                        1 if len(v)==1 else \
                        v[0] / v[1]
                self.make_ghostnote(self.mousePos.x(), self.mousePos.y())
        except:
            pass

    def setGridDiv(self, div=None):
        if not div: div = self.grid_div_str
        try:
            val = map(int, div.split('/'))
            if len(val) < 3:
                self.grid_div_str = div
                self.grid_div = 1 if len(val)==1 else val[1]
                self.value_width = self.measure_width / float(self.grid_div)

                setQuantize(div)

                self.refresh_scene()
        except:
            pass


    # -------------------------------------------------------------------------
    # Event Callbacks

    def keyPressEvent(self, event):
        QtGui.QGraphicsScene.keyPressEvent(self, event)
        if event.key() == QtCore.Qt.Key_B:
            if not self.insert_mode:
                self.insert_mode = True
                self.make_ghostnote(self.mousePos.x(), self.mousePos.y())
            elif self.insert_mode:
                self.insert_mode = False
                if self.place_ghost: self.place_ghost = False
                self.removeItem(self.ghost_note)
                self.ghost_note = None
        if event.key() in (QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace):
            self.notes = [note for note in self.notes if note not in self.selected_notes]
            map(self.removeItem, self.selected_notes)

    def mousePressEvent(self, event):
        QtGui.QGraphicsScene.mousePressEvent(self, event)
        if not (any(key.pressed for key in self.piano_keys) 
                or any(note.pressed for note in self.notes)):
            for note in self.selected_notes:
                note.setSelected(False)
            self.selected_notes = []

            if event.button() == QtCore.Qt.LeftButton:
                if self.insert_mode:
                    self.place_ghost = True
                else:
                    self.marquee_select = True
                    self.marquee_rect = QtCore.QRectF(event.scenePos().x(), event.scenePos().y(), 1, 1)
                    self.marquee = QtGui.QGraphicsRectItem(self.marquee_rect)
                    self.marquee.setBrush(QtGui.QColor(255, 255, 255, 100))
                    self.addItem(self.marquee)
        else:
            for s_note in self.notes:
                if s_note.pressed and s_note in self.selected_notes:
                    break
                elif s_note.pressed and s_note not in self.selected_notes:
                    for note in self.selected_notes:
                        note.setSelected(False)
                    self.selected_notes = [s_note]
                    break
            for note in self.selected_notes:
                note.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        QtGui.QGraphicsScene.mouseMoveEvent(self, event)
        self.mousePos = event.scenePos()
        if not (any((key.pressed for key in self.piano_keys))):
            m_pos = event.scenePos()
            if self.insert_mode and self.place_ghost: #placing a note
                m_width = self.ghost_rect.x() + self.ghost_rect_orig_width
                if m_pos.x() > m_width:
                    m_new_x = snap(m_pos.x())
                    self.ghost_rect.setRight(m_new_x)
                    self.ghost_note.setRect(self.ghost_rect)
                #self.adjust_note_vel(event)
            else:
                m_pos = self.enforce_bounds(m_pos)
                    
                if self.insert_mode: #ghostnote follows mouse around
                    (m_new_x, m_new_y) = snap(m_pos.x(), m_pos.y())
                    self.ghost_rect.moveTo(m_new_x, m_new_y)
                    try:
                        self.ghost_note.setRect(self.ghost_rect)
                    except RuntimeError:
                        self.ghost_note = None
                        self.make_ghostnote(m_new_x, m_new_y)

                elif self.marquee_select:
                    marquee_orig_pos = event.buttonDownScenePos(QtCore.Qt.LeftButton)
                    if marquee_orig_pos.x() < m_pos.x() and marquee_orig_pos.y() < m_pos.y():
                        self.marquee_rect.setBottomRight(m_pos)
                    elif marquee_orig_pos.x() < m_pos.x() and marquee_orig_pos.y() > m_pos.y():
                        self.marquee_rect.setTopRight(m_pos)
                    elif marquee_orig_pos.x() > m_pos.x() and marquee_orig_pos.y() < m_pos.y():
                        self.marquee_rect.setBottomLeft(m_pos)
                    elif marquee_orig_pos.x() > m_pos.x() and marquee_orig_pos.y() > m_pos.y():
                        self.marquee_rect.setTopLeft(m_pos)
                    self.marquee.setRect(self.marquee_rect)
                    self.selected_notes = []
                    for item in self.collidingItems(self.marquee):
                        if item in self.notes:
                            self.selected_notes.append(item)

                    for note in self.notes:
                        if note in self.selected_notes: note.setSelected(True)
                        else: note.setSelected(False)

                elif not self.marquee_select: #move selected
                    if QtCore.Qt.LeftButton == event.buttons():
                        for note in self.selected_notes:
                            note.moveEvent(event)

    def mouseReleaseEvent(self, event):
        QtGui.QGraphicsScene.mouseReleaseEvent(self, event)
        if not (any((key.pressed for key in self.piano_keys)) or any((note.pressed for note in self.notes))):
            if event.button() == QtCore.Qt.LeftButton:
                if self.place_ghost and self.insert_mode:
                    self.place_ghost = False
                    note_start = self._get_note_start_from_x(self.ghost_rect.x())
                    note_num = self._get_note_num_from_y(self.ghost_rect.y())
                    note_length = self._get_note_length_from_x(self.ghost_rect.width())
                    self.draw_note(note_num, note_start, note_length, self.ghost_vel)

                    self.make_ghostnote(self.mousePos.x(), self.mousePos.y())

                elif self.marquee_select:
                    self.marquee_select = False
                    self.removeItem(self.marquee)
        elif not self.marquee_select:
            for n in self.selected_notes:
                n.mouseReleaseEvent(event)

    # -------------------------------------------------------------------------
    # Internal Functions

    def draw_header(self):
        self.header = QtGui.QGraphicsRectItem(0, 0, self.grid_width, self.header_height)
        #self.header.setZValue(1.0)
        self.header.setPos(self.piano_width + self.padding, 0)
        self.addItem(self.header)

    def draw_piano(self):
        labels = ('B','Bb','A','Ab','G','Gb','F','E','Eb','D','Db','C')
        black_notes = (2,4,6,9,11)
        piano_label = QtGui.QFont()
        piano_label.setPointSize(8)
        self.piano = QtGui.QGraphicsRectItem(0, 0, self.piano_width, self.piano_height)
        self.piano.setPos(0, self.header_height)
        self.addItem(self.piano)

        key = piano_key_item(self.piano_width, self.note_height, self.piano)
        label = QtGui.QGraphicsSimpleTextItem('C8', key)
        label.setPos(4, 0)
        label.setFont(piano_label)
        key.setBrush(QtGui.QColor(255, 255, 255))
        for i in range(self.end_octave - self.start_octave, self.start_octave - self.start_octave, -1):
            for j in range(self.notes_in_octave, 0, -1):
                key = piano_key_item(self.piano_width, self.note_height, self.piano)
                key.setPos(0, self.note_height * j + self.octave_height * (i - 1))
                if j == 12:
                    label = QtGui.QGraphicsSimpleTextItem('%s%d' % (labels[(j - 1)], self.end_octave - i), key)
                    label.setPos(4, 0)
                    label.setFont(piano_label)
                if j in black_notes:
                    key.setBrush(QtGui.QColor(0, 0, 0))
                else:
                    key.setBrush(QtGui.QColor(255, 255, 255))
                self.piano_keys.append(key)

    def draw_grid(self):
        black_notes = [2,4,6,9,11]
        for i in range(self.end_octave - self.start_octave, self.start_octave - self.start_octave, -1):
            for j in range(self.notes_in_octave, 0, -1):
                clearpen = QtGui.QPen(QtGui.QColor(0,0,0,0))
                scale_bar = QtGui.QGraphicsRectItem(0, 0, self.grid_width, self.note_height, self.piano)
                scale_bar.setPos(self.piano_width + self.padding, self.note_height * j + self.octave_height * (i - 1))
                scale_bar.setPen(clearpen)
                if j not in black_notes:
                    scale_bar.setBrush(QtGui.QColor(120,120,120))
        beat_pen = QtGui.QPen()
        beat_pen.setWidth(2)
        line_pen = QtGui.QPen()
        line_pen.setColor(QtGui.QColor(0, 0, 0, 40))
        for i in range(0, int(self.num_measures) + 1):
            beat = QtGui.QGraphicsLineItem(0, 0, 0, self.piano_height + self.header_height - beat_pen.width(), self.header)
            beat.setPos(self.measure_width * i, 0.5 * beat_pen.width())
            beat.setPen(beat_pen)
            if i < self.num_measures:
                number = QtGui.QGraphicsSimpleTextItem('%d' % (i + 1), self.header)
                number.setPos(self.measure_width * i + 5, 2)
                number.setBrush(QtCore.Qt.white)
                for j in range(0, self.grid_div):
                    line = QtGui.QGraphicsLineItem(0, 0, 0, self.piano_height, self.header)
                    line.setZValue(1.0)
                    if float(j) == self.grid_div / 2.0:
                        line.setLine(0, 0, 0, self.piano_height)
                        line.setPos(self.measure_width * i + self.value_width * j, self.header_height)
                    else:
                        line.setPos(self.measure_width * i + self.value_width * j, self.header_height)
                        line.setPen(line_pen)

    def refresh_scene(self):
        map(self.removeItem, self.notes)
        self.selected_notes = []
        self.clear()
        self.draw_piano()
        self.draw_header()
        self.draw_grid()
        #for note in self.notes:
            #if note.pos().x() > self.grid_width:
        map(self.addItem, self.notes)

    def clear_drawn_items(self):
        self.clear()
        self.notes = []
        self.selected_notes = []
        self.draw_piano()
        self.draw_header()
        self.draw_grid()

    def make_ghostnote(self, pos_x, pos_y):
        """creates the ghostnote that is placed on the scene before the real one is."""
        if self.ghost_note:
            self.removeItem(self.ghost_note)
        #length = self._get_note_x_length(1./self.grid_div)
        length = self.measure_width * self.default_length
        (start, note) = snap(pos_x, pos_y)
        self.ghost_rect = QtCore.QRectF(start, note, length, self.note_height)
        self.ghost_rect_orig_width = self.ghost_rect.width()
        self.ghost_note = QtGui.QGraphicsRectItem(self.ghost_rect)
        self.ghost_note.setBrush(QtGui.QColor(230, 221, 45, 100))
        self.addItem(self.ghost_note)

    def draw_note(self, note_num, note_start=None, note_length=None, note_velocity=None):
        """note_num is the midi number, note_start is in range(0,num_measures*time_sig[0]), note_length is in beats, note_velocity is 0-127"""
        #might be good to have this i don't know though
        info = (note_num, note_start, note_length, note_velocity)

        note_start = note_start % (self.num_measures * self.time_sig[0])

        start = self._get_note_x_start(note_start)
        print self.time_sig[0]
        if note_length > self.time_sig[0] / self.time_sig[1] * self.num_measures:
            note_length = self.time_sig[0] / self.time_sig[1] * self.num_measures + 0.25
            print note_length
        length = self._get_note_x_length(note_length)
        note_y_pos = self._get_note_y_pos(note_num)

        note = note_item(length, self.note_height, note_num)
        note.setPos(start, note_y_pos)
        #f_vel_opacity = QtGui.QGraphicsOpacityEffect()
        #f_vel_opacity.setOpacity(note_velocity * 0.007874016 * 0.6 + 0.3)
        #note.setGraphicsEffect(f_vel_opacity)

        self.addItem(note)
        self.notes.append(note)

    # -------------------------------------------------------------------------
    # Helper Functions

    def adjust_note_vel(self, event):
        return
        m_pos = event.scenePos()
        #bind velocity to vertical mouse movement
        self.ghost_vel = self.ghost_vel + (event.lastScenePos().y() - m_pos.y())/10
        if self.ghost_vel < 0:
            self.ghost_vel = 0
        elif self.ghost_vel > 127:
            self.ghost_vel = 127

        m_width = self.ghost_rect.x() + self.ghost_rect_orig_width
        if m_pos.x() < m_width:
            m_pos.setX(m_width)
        m_new_x = snap(m_pos.x())
        self.ghost_rect.setRight(m_new_x)
        self.ghost_note.setRect(self.ghost_rect)

    def enforce_bounds(self, pos):
        if pos.x() < self.piano_width:
            pos.setX(self.piano_width)
        elif pos.x() > self.grid_width + self.piano_width:
            pos.setX(self.grid_width + self.piano_width)
        if pos.y() < self.header_height:
            pos.setY(self.header_height)
        return pos

    def _get_note_start_from_x(self, note_x):
        return (note_x - self.piano_width - self.padding) / (self.grid_width / self.num_measures / self.time_sig[0])


    def _get_note_x_start(self, note_start):
        return self.piano_width + self.padding + \
                (self.grid_width / self.num_measures / self.time_sig[0]) * note_start

    def _get_note_x_length(self, note_length):
        return float(self.time_sig[1]) / self.time_sig[0] * note_length * self.grid_width / self.num_measures

    def _get_note_length_from_x(self, note_x):
        return float(self.time_sig[0]) / self.time_sig[1] * self.num_measures / self.grid_width \
                * note_x


    def _get_note_y_pos(self, note_num):
        return self.header_height + self.note_height * (self.total_notes - note_num - 1)

    def _get_note_num_from_y(self, note_y_pos):
        return -(((note_y_pos - self.header_height) / self.note_height) - self.total_notes + 1)


class piano_roll_view(QtGui.QGraphicsView):
    def __init__(self, time_sig = [4,4], num_measures = 4, grid_div = 4):
        QtGui.QGraphicsView.__init__(self)
        self.piano = piano_roll(time_sig, num_measures, grid_div) 
        self.setScene(self.piano)
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.o_transform = self.transform()
        self.zoom_x = 1
        self.zoom_y = 1

    def setZoomX(self, scale_x):
        self.setTransform(self.o_transform)
        self.zoom_x = 1 + scale_x / float(99)
        self.scale(self.zoom_x, self.zoom_y)

    def setZoomY(self, scale_y):
        self.setTransform(self.o_transform)
        self.zoom_y = 1 + scale_y / float(99)
        self.scale(self.zoom_x, self.zoom_y)

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    main = QtGui.QWidget()
    view = piano_roll_view(global_time_sig, num_measures = 5, grid_div=8)
    setQuantize(global_quantize_val)

    timeSigLabel = QtGui.QLabel(QtCore.QString('time signature'))
    timeSigLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
    timeSigLabel.setMaximumWidth(100)
    timeSigBox = QtGui.QComboBox()
    timeSigBox.setEditable(True)
    timeSigBox.setMaximumWidth(100)
    timeSigBox.addItems(
            map(QtCore.QString,
                ('1/4', '2/4', '3/4', '4/4', '5/4', '6/4', '12/8')
                ))
    timeSigBox.setCurrentIndex(5)

    measureLabel = QtGui.QLabel(QtCore.QString('measures'))
    measureLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
    measureLabel.setMaximumWidth(100)
    measureBox = QtGui.QComboBox()
    measureBox.setMaximumWidth(100)
    measureBox.addItems(
            map(QtCore.QString,
                map(str,
                    range(1,17)
                    )))
    measureBox.setCurrentIndex(4)

    defaultLengthLabel = QtGui.QLabel(QtCore.QString('default length'))
    defaultLengthLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
    defaultLengthLabel.setMaximumWidth(100)
    defaultLengthBox = QtGui.QComboBox()
    defaultLengthBox.setEditable(True)
    defaultLengthBox.setMaximumWidth(100)
    defaultLengthBox.addItems(
            map(QtCore.QString,
                ('1/16', '1/15', '1/12', '1/9', '1/8', '1/6', '1/4', '1/3', '1/2', '1')
                ))
    defaultLengthBox.setCurrentIndex(4)

    quantizeLabel = QtGui.QLabel(QtCore.QString('quantize'))
    quantizeLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
    quantizeLabel.setMaximumWidth(100)
    quantizeBox = QtGui.QComboBox()
    quantizeBox.setEditable(True)
    quantizeBox.setMaximumWidth(100)
    quantizeBox.addItems(
            map(QtCore.QString,
                ('0', '1/16', '1/15', '1/12', '1/9', '1/8', '1/6', '1/4', '1/3', '1/2', '1')
                ))
    quantizeBox.setCurrentIndex(5)

    hSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
    hSlider.setTracking(True)

    vSlider = QtGui.QSlider(QtCore.Qt.Vertical)
    vSlider.setTracking(True)
    vSlider.setInvertedAppearance(True)
    vSlider.setMaximumHeight(500)
    #vSlider.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

    timeSigBox.currentIndexChanged[QtCore.QString].connect(view.piano.setTimeSig)
    measureBox.currentIndexChanged[QtCore.QString].connect(view.piano.setMeasures)
    defaultLengthBox.currentIndexChanged[QtCore.QString].connect(view.piano.setDefaultLength)
    quantizeBox.currentIndexChanged[QtCore.QString].connect(view.piano.setGridDiv)
    hSlider.valueChanged.connect(view.setZoomX)
    vSlider.valueChanged.connect(view.setZoomY)

    hBox = QtGui.QHBoxLayout()

    hBox.addWidget(timeSigLabel)
    hBox.addWidget(timeSigBox)
    hBox.addWidget(measureLabel)
    hBox.addWidget(measureBox)
    hBox.addWidget(defaultLengthLabel)
    hBox.addWidget(defaultLengthBox)
    hBox.addWidget(quantizeLabel)
    hBox.addWidget(quantizeBox)
    hBox.addWidget(hSlider)

    viewBox = QtGui.QHBoxLayout()
    viewBox.addWidget(vSlider)
    viewBox.addWidget(view)
    viewBox.setSpacing(0)
    viewBox.setMargin(0)
    viewBox.setContentsMargins(0,0,0,0)
    

    layout = QtGui.QVBoxLayout()

    layout.addLayout(hBox)
    layout.addLayout(viewBox)
    #layout.addWidget(view)

    main.setLayout(layout)

    view.piano.draw_note(72, 0, 0.25, 20)
    view.piano.draw_note(73, 1, 0.25, 20)
    view.piano.draw_note(74, 2, 0.25, 20)
    view.piano.draw_note(75, 3, 0.25, 20)
    view.piano.draw_note(76, 4, 0.25, 20)
    #view.piano.draw_note(76, 18, 0.25, 20)
    #view.piano.draw_note(76, 19, 0.25, 20)
    #view.piano.draw_note(76, 20, 0.25, 20)
    main.show()
    sys.exit(app.exec_())
