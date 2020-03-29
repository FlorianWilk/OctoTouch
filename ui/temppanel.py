from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import ui.buttons

class MyTemps(QWidget):

     def __init__(self,*args,**kwargs):
          super().__init__(*args, **kwargs)
          #self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))

          layout=QHBoxLayout()
          layout.setSpacing(0)
          layout.setContentsMargins(0,0,0,0)          
          self.setMaximumHeight(150)
          self.setLayout(layout)
          self.hotend_label=QLabel("0°")
          self.hotend_label.setObjectName("hotend_temp")
          self.hotend_label.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))

          layout.addWidget(self.hotend_label,1)

          self.bed_label=QLabel("0°")
          self.bed_label.setObjectName("bed_temp")
          self.bed_label.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
          layout.addWidget(self.bed_label,1)

     def setTemps(self,temps):
          if len(temps["bed"])==2:
              bed_actual,bed_target=(temps["bed"])
              self.bed_label.setText(str(bed_actual)+"°")
          if len(temps["tool"])==2:
            tool_actual,tool_target=(temps["tool"])
            self.hotend_label.setText(str(tool_actual)+"°")
