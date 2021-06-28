from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication

from daw_tools import *

# from daw_tools import Test
# from daw_tools import Timeline
# from daw_tools import Envelope
# from daw_tools import PianoRoll
# from daw_tools import Piano

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setFixedSize(1200,900)

        self.test = Test()

        self.envelope = Envelope()
        self.envelope.draw_point(2, 127)
        self.envelope.draw_point(3, 64)
        self.envelope.draw_point(0, 0)
        self.envelope.draw_point(1, 54)

        self.timeline = Timeline(total_tracks=8)
        for i in range(8):
            self.timeline.draw_item_musical_time(0, 0, 0, i + 1, 0, 0, 120, 'Item-' + str(i), i)
        self.timeline.set_zoom(1)

        self.piano_roll = PianoRoll()
        self.piano_roll.piano.drawNote(71, 0, 0.50, 20)
        self.piano_roll.piano.drawNote(73, 1, 0.50, 20)
        self.piano_roll.piano.drawNote(75, 2, 0.50, 20)
        self.piano_roll.piano.drawNote(77, 3, 0.50, 20)
        self.piano_roll.piano.drawNote(79, 4, 0.50, 20)

        self.layout = QGridLayout()

        self.layout.addWidget(QLabel('TEST'),0,0)
        self.layout.addWidget(self.test,1,0)
        self.layout.addWidget(QLabel('ENVELOPE'),0,1)
        self.layout.addWidget(self.envelope,1,1)
        self.layout.addWidget(QLabel('TIMELINE'),2,0)
        self.layout.addWidget(self.timeline,3,0)
        self.layout.addWidget(QLabel('PIANO ROLL'),2,1)
        self.layout.addWidget(self.piano_roll,3,1)

        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    exit(app.exec_())
