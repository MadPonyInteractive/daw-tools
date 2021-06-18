'''
Based on and credit to: https://github.com/rhetr/seq-gui

- A basic timeline

'''
import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
colors = [Qt.blue, Qt.green, Qt.red, Qt.yellow]

class timeline_item(QGraphicsRectItem):
    def __init__(self, a_length, a_height, a_name, a_track_num, a_y_pos):
        QGraphicsRectItem.__init__(self, 0, 0, a_length, a_height)
        self.label = QGraphicsSimpleTextItem(a_name, parent=self)
        self.label.setPos(10, 5)
        self.label.setBrush(Qt.white)
        self.label.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.track_num = a_track_num
        self.mouse_y_pos = a_y_pos

    def mouseDoubleClickEvent(self, a_event):
        # QGraphicsRectItem.mouseDoubleClickEvent(self, a_event)
        print ("Here's where we'll open the item properties dialog for track " + str(self.track_num))

    def mousePressEvent(self, a_event):
        # QGraphicsRectItem.mousePressEvent(self, a_event)
        self.setGraphicsEffect(QGraphicsOpacityEffect())

    def mouseMoveEvent(self, a_event):
        QGraphicsRectItem.mouseMoveEvent(self, a_event)
        f_pos = self.pos().x()
        if f_pos < 0:
            f_pos = 0
        self.setPos(f_pos, self.mouse_y_pos)

    def mouseReleaseEvent(self, a_event):
        # QGraphicsRectItem.mouseReleaseEvent(self, a_event)
        self.setGraphicsEffect(None)
        f_pos_x = self.pos().x()
        self.setPos(f_pos_x, self.mouse_y_pos)
        print (str(f_pos_x))

class timeline(QGraphicsView):
    def __init__(self, a_item_length = 4, a_region_length = 8, a_bpm = 140.0, a_px_per_region = 100, total_tracks = 5, total_regions = 300):
        self.item_length = float(a_item_length)
        self.region_length = float(a_region_length)
        QGraphicsView.__init__(self)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QColor(90, 90, 90))
        self.setScene(self.scene)
        self.audio_items = []
        self.track = 0
        self.gradient_index = 0
        self.set_bpm(a_bpm)
        self.px_per_region = a_px_per_region
        self.total_regions = total_regions
        self.viewer_size = self.px_per_region * self.total_regions
        self.header_height = 20
        self.total_tracks = total_tracks
        self.item_height = 65
        self.padding = 2
        self.draw_headers()
        self.draw_grid()

    def set_zoom(self, a_scale):
        """ a_scale == number from 1.0 to 6.0 """
        self.scale(a_scale, 1.0)

    def set_bpm(self, a_bpm):
        self.bps = a_bpm / 60.0
        self.beats_per_region = self.item_length * self.region_length
        self.regions_per_second = self.bps / self.beats_per_region

    def f_seconds_to_regions(self, a_track_seconds):
        """converts seconds to regions"""
        return a_track_seconds * self.regions_per_second

    def draw_headers(self):
        f_header = QGraphicsRectItem(0, 0, self.viewer_size, self.header_height)
        self.scene.addItem(f_header)
        for i in range(0, self.total_regions):
            f_number = QGraphicsSimpleTextItem('%d' % i, f_header)
            f_number.setFlag(QGraphicsItem.ItemIgnoresTransformations)
            f_number.setPos(self.px_per_region * i, 2)
            f_number.setBrush(Qt.white)

    def draw_grid(self):
        f_pen = QPen()
        for i in range(1, self.total_tracks + 1):
            f_line = QGraphicsLineItem(0, 0, self.viewer_size, 0)
            f_line.setPos(0, self.header_height + self.padding + self.item_height * i)
            self.scene.addItem(f_line)

    def draw_item_seconds(self, a_start_region, a_start_bar, a_start_beat, a_seconds, a_name, a_track_num):
        f_start = (a_start_region + (a_start_bar * self.item_length + a_start_beat) / self.beats_per_region) * self.px_per_region
        f_length = self.f_seconds_to_regions(a_seconds) * self.px_per_region
        self.draw_item(f_start, f_length, a_name, a_track_num)

    def draw_item_musical_time(self, a_start_region, a_start_bar, a_start_beat, a_end_region, a_end_bar, a_end_beat, a_seconds, a_name, a_track_num):
        f_start = (a_start_region + (a_start_bar * self.item_length + a_start_beat) / self.beats_per_region) * self.px_per_region
        f_length = (a_end_region + (a_end_bar * self.item_length + a_end_beat) / self.beats_per_region) * self.px_per_region - f_start
        f_length_seconds = self.f_seconds_to_regions(a_seconds) * self.px_per_region
        if f_length_seconds < f_length:
            f_length = f_length_seconds
        self.draw_item(f_start, f_length, a_name, a_track_num)

    def clear_drawn_items(self):
        self.track = 0
        self.gradient_index = 0
        self.audio_items = []
        self.scene.clear()
        self.draw_headers()

    def draw_item(self, a_start, a_length, a_name, a_track_num):
        """a_start in seconds, a_length in seconds"""
        f_track_num = self.header_height + self.padding + self.item_height * self.track
        f_audio_item = timeline_item(a_length, self.item_height, a_name, a_track_num, f_track_num)
        self.audio_items.append(f_audio_item)
        f_audio_item.setPos(a_start, f_track_num)
        f_audio_item.setBrush(colors[self.gradient_index])
        self.gradient_index += 1
        if self.gradient_index >= len(colors):
            self.gradient_index = 0
        self.scene.addItem(f_audio_item)
        self.track += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = timeline(total_tracks=8)
    for i in range(8):
        view.draw_item_musical_time(0, 0, 0, i + 1, 0, 0, 120, 'Item-' + str(i), i)

    view.set_zoom(2.0)
    view.show()
    sys.exit(app.exec_())
