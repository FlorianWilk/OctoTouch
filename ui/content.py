from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui.basic import *
from ui.content_idle import *
from ui.content_print import *

class MyContent(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        label_wilklabs = QLabel("WILK LABS - PrinterControl V0.1 Alpha")
        label_wilklabs.setObjectName("titlebar")
        layout.addWidget(label_wilklabs)

        stack_layout = QStackedWidget()
        self.stack_layout = stack_layout

        self.idle_content = MyIdleContent()
        stack_layout.addWidget(self.idle_content)

        self.print_content = MyPrintContent()
        stack_layout.addWidget(self.print_content)

        layout.addWidget(stack_layout)
        self.stack_layout.setCurrentIndex(0)
        self.data = None

    def updateUI(self, data):
        if not data["state_flags"]['printing']:
            self.stack_layout.setCurrentIndex(0)
        else:
            self.stack_layout.setCurrentIndex(1)
        self.print_content.updateUI(data)
        self.idle_content.updateUI(data)

    def setData(self, data):
        self.data = data
        self.updateUI(self.data)
