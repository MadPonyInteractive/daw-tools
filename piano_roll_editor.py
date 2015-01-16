"""
A piano roll viewer/editor
"""
from PyQt4 import QtGui, QtCore
global_piano_roll_snap = True
global_piano_roll_grid_width = 1000.0
global_piano_roll_grid_max_start_time = 999.0
global_piano_roll_note_height = 10
global_piano_roll_snap_value = global_piano_roll_grid_width / 64.0
global_piano_roll_note_count = 120
global_piano_keys_width = 34
global_piano_roll_header_height = 20
global_piano_roll_total_height = 1000 #this gets changed

global_piano_roll_quantize_choices = ['None','1/4','1/3','1/2','1']

def piano_roll_quantize(a_index):
    global global_piano_roll_snap_value
    global global_piano_roll_snap
    if a_index == 0:
        global_piano_roll_snap = False
    elif a_index == 1:
        global_piano_roll_snap_value = global_piano_roll_grid_width / 16.0
        global_piano_roll_snap = True
    elif a_index == 2:
        global_piano_roll_snap_value = global_piano_roll_grid_width / 12.0
        global_piano_roll_snap = True
    elif a_index == 3:
        global_piano_roll_snap_value = global_piano_roll_grid_width / 8.0
        global_piano_roll_snap = True
    elif a_index == 4:
        global_piano_roll_snap_value = global_piano_roll_grid_width / 4.0
        global_piano_roll_snap = True

def snap(a_pos_x, a_pos_y = None):
    if global_piano_roll_snap:
        f_pos_x = int((a_pos_x - global_piano_keys_width) / global_piano_roll_snap_value) * global_piano_roll_snap_value + global_piano_keys_width
    if a_pos_y:
        f_pos_y = int((a_pos_y - global_piano_roll_header_height) / global_piano_roll_note_height) * global_piano_roll_note_height + global_piano_roll_header_height
        return (f_pos_x, f_pos_y)
    else:
        return f_pos_x


class note_item(QtGui.QGraphicsRectItem):
    '''a note on the pianoroll sequencer'''
    def __init__(self, a_length, a_note_height, a_note_num):
        QtGui.QGraphicsRectItem.__init__(self, 0, 0, a_length, a_note_height)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.o_brush = QtGui.QColor(100, 0, 0)
        self.hover_brush = QtGui.QColor(200, 200, 100)
        self.s_brush = QtGui.QColor(200, 100, 100)
        self.setBrush(self.o_brush)
        self.note_height = a_note_height
        self.note_num = a_note_num
        self.pressed = False
        self.selected = False

    def select(self):
        self.setSelected(True)
        self.selected = True
        self.setBrush(self.s_brush)

    def deselect(self):
        self.setSelected(False)
        self.selected = False
        self.setBrush(self.o_brush)

    def hoverEnterEvent(self, a_event):
        QtGui.QGraphicsRectItem.hoverEnterEvent(self, a_event)
        if not self.selected:
            self.setBrush(self.hover_brush)

    def hoverLeaveEvent(self, a_event):
        QtGui.QGraphicsRectItem.hoverLeaveEvent(self, a_event)
        if not self.selected:
            self.setBrush(self.o_brush)
        elif self.selected:
            self.setBrush(self.s_brush)

    def mousePressEvent(self, a_event):
        a_event.setAccepted(True)
        QtGui.QGraphicsRectItem.mousePressEvent(self, a_event)
        self.select()
        self.pressed = True

    def mouseMoveEvent(self, a_event):
        QtGui.QGraphicsRectItem.mouseMoveEvent(self, a_event)
        f_pos_x = self.pos().x()
        f_pos_y = self.pos().y()
        if f_pos_x < global_piano_keys_width:
            f_pos_x = global_piano_keys_width
        elif f_pos_x > global_piano_roll_grid_max_start_time:
            f_pos_x = global_piano_roll_grid_max_start_time
        if f_pos_y < global_piano_roll_header_height:
            f_pos_y = global_piano_roll_header_height
        elif f_pos_y > global_piano_roll_total_height:
            f_pos_y = global_piano_roll_total_height
        (f_pos_x, f_pos_y,) = snap(f_pos_x, f_pos_y)
        self.setPos(f_pos_x, f_pos_y)

    def mouseReleaseEvent(self, a_event):
        a_event.setAccepted(True)
        QtGui.QGraphicsRectItem.mouseReleaseEvent(self, a_event)
        self.pressed = False
        if a_event.button() == QtCore.Qt.LeftButton:
            (f_pos_x, f_pos_y,) = snap(self.pos().x(), self.pos().y())
            self.setPos(f_pos_x, f_pos_y)
            f_new_note_start = (f_pos_x - global_piano_keys_width) * 0.001 * 4.0
            f_new_note_num = int(global_piano_roll_note_count - (f_pos_y - global_piano_roll_header_height) / global_piano_roll_note_height)
            #print "note start: ", str(f_new_note_start)
            print "MIDI number: ", str(f_new_note_num)


class piano_key_item(QtGui.QGraphicsRectItem):
    def __init__(self, width, height, parent):
        QtGui.QGraphicsRectItem.__init__(self, 0, 0, width, height, parent)
        self.width = width
        self.height = height
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.hover_brush = QtGui.QColor(200, 0, 0)
        self.click_brush = QtGui.QColor(255, 100, 100)
        self.pressed = False

    def hoverEnterEvent(self, a_event):
        QtGui.QGraphicsRectItem.hoverEnterEvent(self, a_event)
        self.o_brush = self.brush()
        self.setBrush(self.hover_brush)

    def hoverLeaveEvent(self, a_event):
        if self.pressed:
            self.pressed = False
            self.setBrush(self.hover_brush)
        QtGui.QGraphicsRectItem.hoverLeaveEvent(self, a_event)
        self.setBrush(self.o_brush)

    def mousePressEvent(self, a_event):
        self.pressed = True
        self.setBrush(self.click_brush)

    def mouseMoveEvent(self, a_event):
        """this may eventually do something"""
        pass

    def mouseReleaseEvent(self, a_event):
        self.pressed = False
        QtGui.QGraphicsRectItem.mouseReleaseEvent(self, a_event)
        self.setBrush(self.hover_brush)


class piano_roll(QtGui.QGraphicsView):
    '''the piano roll'''
    def __init__(self, a_item_length = 4, a_grid_div = 4):
        global global_piano_roll_total_height
        self.item_length = float(a_item_length)
        self.viewer_width = 1000
        self.grid_div = a_grid_div
        self.end_octave = 8
        self.start_octave = -2
        self.notes_in_octave = 12
        self.total_notes = (self.end_octave - self.start_octave) * self.notes_in_octave + 1
        self.note_height = global_piano_roll_note_height
        self.octave_height = self.notes_in_octave * self.note_height
        self.header_height = global_piano_roll_header_height
        self.piano_height = self.note_height * self.total_notes
        self.padding = 2
        self.piano_width = global_piano_keys_width - self.padding
        self.piano_height = self.note_height * self.total_notes
        global_piano_roll_total_height = self.piano_height - self.note_height + global_piano_roll_header_height
        QtGui.QGraphicsView.__init__(self)
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.mousePressEvent = self.sceneMousePressEvent
        self.scene.mouseReleaseEvent = self.sceneMouseReleaseEvent
        self.scene.mouseMoveEvent = self.sceneMouseMoveEvent
        self.scene.setBackgroundBrush(QtGui.QColor(100, 100, 100))
        self.setScene(self.scene)
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.notes = []
        self.selected_notes = []
        self.piano_keys = []
        self.ghost_vel = 100
        self.show_ghost = True
        self.marquee_select = False
        self.insert_mode = False
        self.place_ghost = False
        self.draw_piano()
        self.draw_header()
        self.draw_grid()

    def make_ghostnote(self, pos_x, pos_y):
        """creates the ghostnote that is placed on the scene before the real one is."""
        f_length = self.beat_width / 4
        (f_start, f_note,) = snap(pos_x, pos_y)
        self.ghost_rect_orig = QtCore.QRectF(f_start, f_note, f_length, self.note_height)
        self.ghost_rect = QtCore.QRectF(self.ghost_rect_orig)
        self.ghost_note = QtGui.QGraphicsRectItem(self.ghost_rect)
        self.ghost_note.setBrush(QtGui.QColor(230, 221, 45, 100))
        self.scene.addItem(self.ghost_note)

    def keyPressEvent(self, a_event):
        QtGui.QGraphicsView.keyPressEvent(self, a_event)
        if a_event.key() == QtCore.Qt.Key_B:
            if not self.insert_mode:
                self.insert_mode = True
                if self.show_ghost:
                    self.make_ghostnote(self.piano_width, self.header_height)
            elif self.insert_mode:
                self.insert_mode = False
                if self.place_ghost:
                    self.place_ghost = False
                    self.scene.removeItem(self.ghost_note)
                elif self.show_ghost:
                    self.scene.removeItem(self.ghost_note)
        if a_event.key() == QtCore.Qt.Key_Delete or a_event.key() == QtCore.Qt.Key_Backspace:
            for note in self.selected_notes:
                note.deselect()
                self.scene.removeItem(note)

    def sceneMousePressEvent(self, a_event):
        QtGui.QGraphicsScene.mousePressEvent(self.scene, a_event)
        if not (any(key.pressed for key in self.piano_keys) or any(note.pressed for note in self.notes)):
        #if not self.scene.mouseGrabberItem():
            for note in self.selected_notes:
                note.deselect()

            self.selected_notes = []
            self.f_pos = a_event.scenePos()
            if a_event.button() == QtCore.Qt.LeftButton:
                if self.insert_mode:
                    self.place_ghost = True
                else:
                    self.marquee_select = True
                    self.marquee_rect = QtCore.QRectF(self.f_pos.x(), self.f_pos.y(), 1, 1)
                    self.marquee = QtGui.QGraphicsRectItem(self.marquee_rect)
                    self.marquee.setBrush(QtGui.QColor(255, 255, 255, 100))
                    self.scene.addItem(self.marquee)
        else:
            out = False
            for note in self.notes:
                if note.pressed and note in self.selected_notes:
                    break
                elif note.pressed and note not in self.selected_notes:
                    s_note = note
                    out = True
                    break
            if out == True:
                for note in self.selected_notes:
                    note.deselect()
                self.selected_notes = [s_note]
            elif out == False:
                for note in self.selected_notes:
                    note.mousePressEvent(a_event)

    def sceneMouseMoveEvent(self, a_event):
        QtGui.QGraphicsScene.mouseMoveEvent(self.scene, a_event)
        #if not (any((key.pressed for key in self.piano_keys)) or any((note.pressed for note in self.notes))):
        if not (any((key.pressed for key in self.piano_keys))):
        #if not self.scene.mouseGrabberItem():
            m_pos = a_event.scenePos()
            if self.insert_mode and self.place_ghost: #placing a note
                #bind velocity to vertical mouse movement
                self.ghost_vel = self.ghost_vel + (a_event.lastScenePos().y() - m_pos.y())/10
                if self.ghost_vel < 0:
                    self.ghost_vel = 0
                elif self.ghost_vel > 127:
                    self.ghost_vel = 127
                #print "velocity:", self.ghost_vel

                m_width = self.ghost_rect.x() + self.ghost_rect_orig.width()
                if m_pos.x() < m_width:
                    m_pos.setX(m_width)
                m_new_x = snap(m_pos.x())
                self.ghost_rect.setRight(m_new_x)
                self.ghost_note.setRect(self.ghost_rect)
            else:
                if m_pos.x() < self.piano_width:
                    m_pos.setX(self.piano_width)
                elif m_pos.x() > self.viewer_width:
                    m_pos.setX(self.viewer_width)
                if m_pos.y() < self.header_height:
                    m_pos.setY(self.header_height)
                    
                if self.insert_mode and self.show_ghost: #ghostnote follows mouse around
                    (m_new_x, m_new_y,) = snap(m_pos.x(), m_pos.y())
                    self.ghost_rect.moveTo(m_new_x, m_new_y)
                    self.ghost_note.setRect(self.ghost_rect)
                elif self.marquee_select:
                    if self.f_pos.x() < m_pos.x() and self.f_pos.y() < m_pos.y():
                        self.marquee_rect.setBottomRight(m_pos)
                    elif self.f_pos.x() < m_pos.x() and self.f_pos.y() > m_pos.y():
                        self.marquee_rect.setTopRight(m_pos)
                    elif self.f_pos.x() > m_pos.x() and self.f_pos.y() < m_pos.y():
                        self.marquee_rect.setBottomLeft(m_pos)
                    elif self.f_pos.x() > m_pos.x() and self.f_pos.y() > m_pos.y():
                        self.marquee_rect.setTopLeft(m_pos)
                    self.marquee.setRect(self.marquee_rect)
                    self.selected_notes = []
                    for item in self.scene.collidingItems(self.marquee):
                        if item in self.notes:
                            self.selected_notes.append(item)

                    for note in self.notes:
                        if note in self.selected_notes:
                            note.select()
                        else:
                            note.deselect()

                elif not self.marquee_select:
                    for note in self.selected_notes:
                        note.mouseMoveEvent(a_event)

    def sceneMouseReleaseEvent(self, a_event):
        QtGui.QGraphicsScene.mouseReleaseEvent(self.scene, a_event)
        if not (any((key.pressed for key in self.piano_keys)) or any((note.pressed for note in self.notes))):
        #if not self.scene.mouseGrabberItem():
            if a_event.button() == QtCore.Qt.LeftButton:
                if self.place_ghost and self.insert_mode:
                    self.place_ghost = False
                    f_final_scenePos = a_event.scenePos().x()
                    f_final_scenePos = snap(f_final_scenePos)
                    f_delta = f_final_scenePos - self.ghost_rect.x()
                    if f_delta < self.beat_width / 8:
                        f_delta = self.beat_width / 4
                    f_length = f_delta / self.viewer_width * 4
                    f_start = (self.ghost_rect.x() - self.piano_width - self.padding) / self.beat_width
                    f_note = self.total_notes - (self.ghost_rect.y() - self.header_height) / self.note_height - 1
                    self.draw_note(f_note, f_start, f_length, self.ghost_vel)
                    self.ghost_rect = QtCore.QRectF(self.ghost_rect_orig)
                    self.ghost_note.setRect(self.ghost_rect)
                elif self.marquee_select:
                    self.marquee_select = False
                    self.scene.removeItem(self.marquee)
        elif not self.marquee_select:
            for n in self.selected_notes:
                n.mouseReleaseEvent(a_event)

    def draw_header(self):
        self.header = QtGui.QGraphicsRectItem(0, 0, self.viewer_width, self.header_height)
        #self.header.setZValue(1.0)
        self.header.setPos(self.piano_width + self.padding, 0)
        self.scene.addItem(self.header)
        self.beat_width = self.viewer_width / self.item_length
        self.value_width = self.beat_width / self.grid_div

    def draw_piano(self):
        f_labels = ['B','Bb','A','Ab','G','Gb','F','E','Eb','D','Db','C']
        f_black_notes = [2,4,6,9,11]
        f_piano_label = QtGui.QFont()
        f_piano_label.setPointSize(8)
        self.piano = QtGui.QGraphicsRectItem(0, 0, self.piano_width, self.piano_height)
        self.piano.setPos(0, self.header_height)
        self.scene.addItem(self.piano)
        f_key = piano_key_item(self.piano_width, self.note_height, self.piano)
        f_label = QtGui.QGraphicsSimpleTextItem('C8', f_key)
        f_label.setPos(4, 0)
        f_label.setFont(f_piano_label)
        f_key.setBrush(QtGui.QColor(255, 255, 255))
        for i in range(self.end_octave - self.start_octave, self.start_octave - self.start_octave, -1):
            for j in range(self.notes_in_octave, 0, -1):
                f_key = piano_key_item(self.piano_width, self.note_height, self.piano)
                f_key.setPos(0, self.note_height * j + self.octave_height * (i - 1))
                if j == 12:
                    f_label = QtGui.QGraphicsSimpleTextItem('%s%d' % (f_labels[(j - 1)], self.end_octave - i), f_key)
                    f_label.setPos(4, 0)
                    f_label.setFont(f_piano_label)
                if j in f_black_notes:
                    f_key.setBrush(QtGui.QColor(0, 0, 0))
                else:
                    f_key.setBrush(QtGui.QColor(255, 255, 255))
                self.piano_keys.append(f_key)

    def draw_grid(self):
        f_black_notes = [2,4,6,9,11]
        for i in range(self.end_octave - self.start_octave, self.start_octave - self.start_octave, -1):
            for j in range(self.notes_in_octave, 0, -1):
                f_scale_bar = QtGui.QGraphicsRectItem(0, 0, self.viewer_width, self.note_height, self.piano)
                f_scale_bar.setPos(self.piano_width + self.padding, self.note_height * j + self.octave_height * (i - 1))
                if j not in f_black_notes:
                    f_scale_bar.setBrush(QtGui.QColor(230, 230, 230, 100))
        f_beat_pen = QtGui.QPen()
        f_beat_pen.setWidth(2)
        f_line_pen = QtGui.QPen()
        f_line_pen.setColor(QtGui.QColor(0, 0, 0, 40))
        for i in range(0, int(self.item_length) + 1):
            f_beat = QtGui.QGraphicsLineItem(0, 0, 0, self.piano_height + self.header_height - f_beat_pen.width(), self.header)
            f_beat.setPos(self.beat_width * i, 0.5 * f_beat_pen.width())
            f_beat.setPen(f_beat_pen)
            if i < self.item_length:
                f_number = QtGui.QGraphicsSimpleTextItem('%d' % (i + 1), self.header)
                f_number.setPos(self.beat_width * i + 5, 2)
                f_number.setBrush(QtCore.Qt.white)
                for j in range(0, self.grid_div):
                    f_line = QtGui.QGraphicsLineItem(0, 0, 0, self.piano_height, self.header)
                    f_line.setZValue(1.0)
                    if float(j) == self.grid_div / 2.0:
                        f_line.setLine(0, 0, 0, self.piano_height)
                        f_line.setPos(self.beat_width * i + self.value_width * j, self.header_height)
                    else:
                        f_line.setPos(self.beat_width * i + self.value_width * j, self.header_height)
                        f_line.setPen(f_line_pen)

    def set_zoom(self, scale_x, scale_y):
        self.scale(scale_x, scale_y)

    def clear_drawn_items(self):
        self.scene.clear()
        self.draw_header()
        self.draw_piano()
        self.draw_grid()

    def draw_item(self, a_item):
        """ Draw all notes in an instance of the item class"""
        for f_notes in a_item.notes:
            self.draw_note(f_note)

    def draw_note(self, a_note, a_start=None, a_length=None, a_velocity=None):
        """a_note is the midi number, a_start is 1-4.99, a_length is in beats, a_velocity is 0-127"""
        f_start = self.piano_width + self.padding + self.beat_width * a_start
        f_length = self.beat_width * (a_length * 0.25 * self.item_length)
        f_note = self.header_height + self.note_height * (self.total_notes - a_note - 1)
        f_note_item = note_item(f_length, self.note_height, a_note)
        f_note_item.setPos(f_start, f_note)
        f_vel_opacity = QtGui.QGraphicsOpacityEffect()
        f_vel_opacity.setOpacity(a_velocity * 0.007874016 * 0.6 + 0.3)
        f_note_item.setGraphicsEffect(f_vel_opacity)
        self.scene.addItem(f_note_item)
        self.notes.append(f_note_item)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    view = piano_roll()
    view.draw_note(72, 0, 0.25, 20)
    view.show()
    sys.exit(app.exec_())
