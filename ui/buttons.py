from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MyButton(QPushButton):
     def __init__(self,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding))
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

          
     def __init__(self,*args, **kwargs):
          super().__init__(*args, **kwargs)
          layout_buttons=QVBoxLayout()
          layout_buttons.setSpacing(0)
          layout_buttons.setContentsMargins(0,0,0,0)  
#          self.setMinimumWidth(200)
          self.btn_stop=MyButton("Stop")
          self.btn_stop.setObjectName("stop")
          self.btn_stop.setEnabled(False)
          self.btn_stop.clicked.connect(self.do_stop)
          layout_buttons.addWidget(self.btn_stop)          

          self.btn_pause=MyButton("Pause")
          self.btn_pause.setEnabled(False)
          self.btn_pause.clicked.connect(self.do_pause)
          layout_buttons.addWidget(self.btn_pause)          

          self.btn_home=MyButton("Home")
          self.btn_home.clicked.connect(self.do_home)
          layout_buttons.addWidget(self.btn_home)          

          self.btn_change=MyButton("Change")
          self.btn_change.clicked.connect(self.do_change)
          layout_buttons.addWidget(self.btn_change)          

          self.btn_calibrate=MyButton("Calibrate")
          self.btn_calibrate.clicked.connect(self.do_calib)
          layout_buttons.addWidget(self.btn_calibrate)          

          self.setLayout(layout_buttons)

     def setStates(self,states):
          self.states=states
