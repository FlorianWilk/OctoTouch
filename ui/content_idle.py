from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui.basic import *


class MyIdleContent(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setObjectName("idle_content")
        idle_label = MyBigLabel("Waiting for Things")
        idle_label.setObjectName("state")
        layout.addWidget(idle_label)

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
        try:
            state = str(data['filename'])
            self.state.setText(state)
            timetotal = convertMillis(data['print_time'])+" total"
            filamenttotal = str(
                int(data['filament_length']/1000))+" m Filament"
            self.time_total.setText(timetotal)
            self.filament_total.setText(filamenttotal)
        except Exception as ex:
            print(ex)
            self.time_total.setText("No PrintTime available")
            self.filament_total.setText("No Filament was used")

