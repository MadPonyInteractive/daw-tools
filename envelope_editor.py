"""
A piano roll viewer that will eventually become a piano roll editor
"""
import sys
from PyQt4 import QtGui, QtCore
global_points = []
global_axes_size = 28
#global_max_start_time = 999.0
global_viewer_width = 1000
global_viewer_height = 300

class envelope_item(QtGui.QGraphicsEllipseItem):
    '''a single point on an envelope'''
    def __init__(self, a_time, a_value):
        f_size = 15
        self.f_half_size = f_size / 2.0
        QtGui.QGraphicsEllipseItem.__init__(self, 0, 0, f_size, f_size)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.setPos(a_time - self.f_half_size, a_value - self.f_half_size)
        self.setBrush(QtGui.QColor(255, 0, 0))
        f_pen = QtGui.QPen()
        f_pen.setWidth(2)
        f_pen.setColor(QtGui.QColor(170, 0, 0))
        self.setPen(f_pen)
        self.o_brush = QtGui.QColor(255, 0, 0)
        self.hover_brush = QtGui.QColor(255, 200, 200)
        self.s_brush = QtGui.QColor(0, 255, 0)

        self.pressed = False

    def select(self):
        self.setSelected(True)
        self.setBrush(self.s_brush)

    def deselect(self):
        self.setSelected(False)
        self.setBrush(self.o_brush)

    def hoverEnterEvent(self, a_event):
        QtGui.QGraphicsRectItem.hoverEnterEvent(self, a_event)
        if not self.isSelected():
            self.setBrush(self.hover_brush)

    def hoverLeaveEvent(self, a_event):
        QtGui.QGraphicsRectItem.hoverLeaveEvent(self, a_event)
        if not self.isSelected():
            self.setBrush(self.o_brush)
        else:
            self.setBrush(self.s_brush)


    def mousePressEvent(self, a_event):
        QtGui.QGraphicsEllipseItem.mousePressEvent(self, a_event)
        self.setGraphicsEffect(QtGui.QGraphicsOpacityEffect())
        self.select()
        self.pressed = True

    def mouseMoveEvent(self, a_event):
        QtGui.QGraphicsEllipseItem.mouseMoveEvent(self, a_event)
        f_pos_x = self.pos().x()
        f_pos_y = self.pos().y()
        if f_pos_x < global_axes_size-self.f_half_size:
            f_pos_x = global_axes_size-self.f_half_size 
        elif f_pos_x > global_viewer_width+global_axes_size-self.f_half_size:
            f_pos_x = global_viewer_width+global_axes_size-self.f_half_size
        if f_pos_y < global_axes_size-self.f_half_size:
            f_pos_y = global_axes_size-self.f_half_size 
        elif f_pos_y > global_viewer_height+global_axes_size-self.f_half_size:
            f_pos_y = global_viewer_height+global_axes_size-self.f_half_size
        self.setPos(f_pos_x, f_pos_y)

    def mouseReleaseEvent(self, a_event):
        a_event.setAccepted(True)
        self.pressed = False
        self.setPos(self.pos())
        QtGui.QGraphicsEllipseItem.mouseReleaseEvent(self, a_event)
        self.setGraphicsEffect(None)

class envelope_editor(QtGui.QGraphicsView):
    '''the envelope editor'''
    def __init__(self, a_item_length = 4, a_grid_div = 16):
        self.item_length = float(a_item_length)
        self.steps = 127.0
        self.grid_div = a_grid_div
        global_axes_size = 28
        self.beat_width = global_viewer_width / self.item_length
        self.value_width = self.beat_width / self.grid_div
        self.lines = []
        QtGui.QGraphicsView.__init__(self)
        self.scene = QtGui.QGraphicsScene(self)
        #self.scene.setBackgroundBrush(QtGui.QColor(100, 100, 100))
        self.scene.setBackgroundBrush(QtGui.QColor(200,200,200))
        self.scene.mousePressEvent = self.sceneMousePressEvent
        self.scene.mouseMoveEvent = self.sceneMouseMoveEvent
        self.scene.mouseReleaseEvent = self.sceneMouseReleaseEvent
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setScene(self.scene)
        self.draw_axes()
        self.draw_grid()
        self.draw_endpoints(0.0,64)
        self.draw_endpoints(3.99,64)

        self.insert_mode = False
        self.selected_points = [] #could just iterate over global_points for isSelected() but what the hell

    def keyPressEvent(self, a_event):
        QtGui.QGraphicsView.keyPressEvent(self, a_event)
        if a_event.key() == QtCore.Qt.Key_B:
            if not self.insert_mode:
                self.insert_mode = True
            else:
                self.insert_mode = False
        if a_event.key() == QtCore.Qt.Key_Delete or a_event.key() == QtCore.Qt.Key_Backspace:
            #for point in self.selected_points:
            for point in global_points:
                if point.isSelected():
                    point.deselect()
                    self.scene.removeItem(point)
                    global_points.remove(point)
                    self.connect_points()
                    

    def sceneMousePressEvent(self, a_event):
        QtGui.QGraphicsScene.mousePressEvent(self.scene, a_event)
        if not any(point.isSelected() for point in global_points):
            if self.insert_mode:
                f_pos_x = a_event.scenePos().x()
                f_pos_y = a_event.scenePos().y()
                f_time = (f_pos_x - global_axes_size) / self.beat_width
                f_value = self.steps - (f_pos_y - global_axes_size) * self.steps / global_viewer_height
                print f_time,",", f_value
                self.draw_point(f_time, f_value)
        else:
            for point in global_points:
                point.deselect()

    def sceneMouseMoveEvent(self, a_event):
        QtGui.QGraphicsScene.mouseMoveEvent(self.scene, a_event)
        if any(point.isSelected() for point in global_points):
        #if self.scene.mouseGrabberItem():
            self.connect_points()

    def sceneMouseReleaseEvent(self, a_event):
        QtGui.QGraphicsScene.mouseReleaseEvent(self.scene, a_event)

    def draw_axes(self):
        self.x_axis = QtGui.QGraphicsRectItem(0, 0, global_viewer_width, global_axes_size)
        self.x_axis.setPos(global_axes_size, 0)
        self.scene.addItem(self.x_axis)
        self.y_axis = QtGui.QGraphicsRectItem(0, 0, global_axes_size, global_viewer_height)
        self.y_axis.setPos(0, global_axes_size)
        self.scene.addItem(self.y_axis)

    def draw_grid(self):
        f_beat_pen = QtGui.QPen()
        f_beat_pen.setWidth(2)
        f_line_pen = QtGui.QPen()
        f_line_pen.setColor(QtGui.QColor(0, 0, 0, 40))
        f_labels = [0,'127',0,'64',0,'0']
        for i in range(1, 6):
            f_line = QtGui.QGraphicsLineItem(0, 0, global_viewer_width, 0, self.y_axis)
            f_line.setPos(global_axes_size, global_viewer_height * (i - 1) / 4)
            if i % 2:
                f_label = QtGui.QGraphicsSimpleTextItem(f_labels[i], self.y_axis)
                f_label.setPos(1, global_viewer_height * (i - 1) / 4)
                f_label.setBrush(QtCore.Qt.white)
            if i == 3:
                f_line.setPen(f_beat_pen)

        for i in range(0, int(self.item_length) + 1):
            f_beat = QtGui.QGraphicsLineItem(0, 0, 0, global_viewer_height + global_axes_size - f_beat_pen.width(), self.x_axis)
            f_beat.setPos(self.beat_width * i, 0.5 * f_beat_pen.width())
            f_beat.setPen(f_beat_pen)
            if i < self.item_length:
                f_number = QtGui.QGraphicsSimpleTextItem(str(i), self.x_axis)
                f_number.setPos(self.beat_width * i + 5, 2)
                f_number.setBrush(QtCore.Qt.white)
                for j in range(0, self.grid_div):
                    f_line = QtGui.QGraphicsLineItem(0, 0, 0, global_viewer_height, self.x_axis)
                    if float(j) == self.grid_div / 2.0:
                        f_line.setLine(0, 0, 0, global_viewer_height)
                        f_line.setPos(self.beat_width * i + self.value_width * j, global_axes_size)
                    else:
                        f_line.setPos(self.beat_width * i + self.value_width * j, global_axes_size)
                        f_line.setPen(f_line_pen)

    def set_zoom(self, a_scale):
        self.scale(a_scale, 1.0)

    def clear_drawn_items(self):
        self.scene.clear()
        self.draw_axes()
        self.draw_grid()

    def connect_points(self):
        if self.lines:
            for i in range(len(self.lines)):
                self.scene.removeItem(self.lines[i])

        if len(global_points) > 1:
            self.lines = (len(global_points) - 1) * [None]
            global_points.sort(key=lambda point: point.pos().x())
            f_line_pen = QtGui.QPen()
            f_line_pen.setColor(QtGui.QColor(200, 50, 50))
            f_line_pen.setWidth(4)
            for i in range(1, len(global_points)):
                #f_start_x = global_axes_size
                #f_start_y = global_axes_size+(global_viewer_height/2.0)
                #f_end_x = global_axes_size+global_viewer_width
                #f_end_y = global_axes_size+(global_viewer_height/2.0)
                f_start_x = global_points[(i - 1)].pos().x()
                f_start_y = global_points[(i - 1)].pos().y()
                f_end_x = global_points[i].pos().x()
                f_end_y = global_points[i].pos().y()
                f_pos_x = f_end_x - f_start_x
                f_pos_y = f_end_y - f_start_y
                f_line = QtGui.QGraphicsLineItem(0, 0, f_pos_x, f_pos_y)
                f_line.setPos(7.5 + f_start_x, 7.5 + f_start_y)
                f_line.setPen(f_line_pen)
                self.scene.addItem(f_line)
                self.lines[i - 1] = f_line

    def draw_point(self, a_time, a_value):
        f_time = global_axes_size + self.beat_width * a_time
        f_value = global_axes_size + global_viewer_height / self.steps * (self.steps - a_value)
        f_point = envelope_item(f_time, f_value)
        global_points.append(f_point)
        self.scene.addItem(f_point)
        self.connect_points()

    def draw_endpoints(self, a_time, a_value):
        f_time = global_axes_size + self.beat_width * a_time
        f_value = global_axes_size + global_viewer_height / self.steps * (self.steps - a_value)
        f_point = envelope_item(f_time, f_value)
        f_point.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        global_points.append(f_point)
        self.scene.addItem(f_point)
        self.connect_points()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    view = envelope_editor()
    view.draw_point(2, 127)
    view.draw_point(3, 64)
    view.draw_point(0, 0)
    view.draw_point(1, 54)
    view.show()
    sys.exit(app.exec_())
