from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui.basic import *
from ui.utils import *


class MyIdleContent(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setObjectName("idle_content")
        self.idle_label = MyBigLabel("Printer is offline")
        self.idle_label.setObjectName("state")
        layout.addWidget(self.idle_label)

        self.state = MyBigLabel("")
        self.state.setObjectName("last_print")
        self.state.setWordWrap(True)
        layout.addWidget(self.state)

        self.time_total = MyBigLabel("")
        layout.addWidget(self.time_total)

        self.filament_total = MyBigLabel("")
        layout.addWidget(self.filament_total)
        layout.addStretch(1)

    def updateUI(self, data):

        if "state_flags" in data and data["state_flags"]["operational"]==True:
            self.idle_label.setText("Ready for printing")
        else:
            self.idle_label.setText("Printer is offline")
        try:
            if not data["filename"] is None:
                state = str(data['filename'])
                self.state.setText(state)
            if not data["print_time"] is None:
                timetotal = convertMillis(data['print_time'])+" total"
                self.time_total.setText(timetotal)
            if not data["filament_length"] is None:                
                filamenttotal = str(
                    int(data['filament_length']/1000))+" m Filament"
                self.filament_total.setText(filamenttotal)
        except Exception as ex:
            print(ex)
            self.time_total.setText("No PrintTime available")
            self.filament_total.setText("No Filament was used")

