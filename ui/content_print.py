from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui.basic import *
from ui.utils import *


class MyPrintContent(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setObjectName("print_content")

        self.state = MyBigLabel("Printing")
        self.state.setObjectName("state")
        layout.addWidget(self.state)

        self.completion = MyBigLabel("")
        self.completion.setObjectName("completion")
        layout.addWidget(self.completion)

        self.time_left = MyBigLabel("no print time left yet")
        self.time_left.setObjectName("time_left")
        layout.addWidget(self.time_left)

        self.filament_total = MyBigLabel("-")
#          layout.addWidget(self.filament_total)
        layout.addStretch(1)

    def updateUI(self, data):
        # print(data)
        if not data["print_time_left"] is None:
            timeleft = convertMillis(data['print_time_left'])+" left"
            self.time_left.setText(timeleft)
        if not data["filament_length"] is None:
            filamenttotal = str(
                int(data['filament_length']/1000))+" m Filament"
            self.filament_total.setText(filamenttotal)
        if not data["print_time"] is None:
            state = "Printing - " + convertMillis(data['print_time'])
            self.state.setText(state)
        if not data["progress_completion"] is None:
            completion = "{:.0f}% done".format(data["progress_completion"])
            self.completion.setText(completion)
