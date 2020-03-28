from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MyButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding))
#          self.setMinimumWidth(200)
        self.setAutoFillBackground(False)

#  - PLA/PETG/TPU
#  - Stop
#  - Pause / Resume
#  - HOME
#  - Eject / Present
#  - Filament Change -> Hot -> Retract -> Wait -> Extrude -> Cold
#  - Show Bed Levels


class MyMainButtons(QWidget):

    clicked = pyqtSignal(int)

    def do_home(self):
        self.clicked.emit(0)

    def do_stop(self):
        self.clicked.emit(1)

    def do_pause(self):
        self.clicked.emit(2)

    def do_change(self):
        self.clicked.emit(3)

    def do_calib(self):
        self.clicked.emit(4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout_buttons=None

    def setStates(self, states):
        self.states = states

    def setMenu(self,menu):
        if not self.layout_buttons is None:
            self.layout_buttons.setParent(None)

        layout_buttons = QVBoxLayout()
        layout_buttons.setSpacing(0)
        layout_buttons.setContentsMargins(0, 0, 0, 0)
#          self.setMinimumWidth(200)

        for m in menu:
            self.btn_stop = MyButton(m["label"])
            self.btn_stop.setObjectName(m["label"])
            self.btn_stop.clicked.connect(m["func"])
            layout_buttons.addWidget(self.btn_stop)

        self.setLayout(layout_buttons)
        self.layout_buttons=layout_buttons


