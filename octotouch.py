#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is OctoTouch in a very early stage

import traceback
import json
import threading
import sys
import signal
import time
from octorest import OctoRest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import asyncio
import websocket
import octotouch_ui

from ui.buttons import *
from ui.temppanel import *
from ui.content import *

ask = False
host = "http://printerpi.local:5000"
show_time_units = False


def convertMillis(millis):
    if millis is None:
        return "unknown"
    seconds = round(int((millis) % 60), 2)
    minutes = round(int((millis/(60)) % 60), 2)
    hours = round(int((millis/(60*60)) % 24), 2)
    s = ""
    u = None
    if hours > 0:
        s = s+'{:02d}:'.format(hours)
        u = "h"
    if minutes > 0:
        s = '{}{:02d}:'.format(s, minutes)
        if u is None:
            u = "m"
    if u is None:
        u = "s"
    s = '{}{:02d}'.format(s, seconds)
    if show_time_units:
     return s+u
    else: 
     return s

class PIUI(object):

    def __init__(self):
        self.octo_url = host
        self.octo_key = "0bd8c77e808a8e5e3c53ce13696317fa"
        self.client = None
        self.app = None
        self.data = {}

        self.content_widget = None
        self.tempt_content = None
        self.main_buttons = None
        self.layout_main = None
        self.client = self.init_client()

        self.data = {
            "state_flags": {},
            "state_text": "",
            "bed_temps": "",
            "tool_temps": "",
            "est_print_time": "",
            "filament_length": "",
            "filament_volument": "",
            "filename": "",
            "progress_completion": "",
            "print_time": "",
            "print_time_left": "",

            "temperatures": {"bed": 0, "tool": 0},
        }

        self.uri = "ws://printerpi.local:5000/sockjs/websocket"
        self.ws = websocket.WebSocketApp(self.uri,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.wst = threading.Thread(target=self.ws.run_forever)
        self.wst.daemon = True
        self.wst.start()
        self.build_ui()

    def on_message(self, msgstr):
        try:
            msg = json.loads(msgstr)
            print("-Message " + str(msg))
            if not "current" in msg:  # Hisotry / timelapse / event
                return
            state = msg['current']['state']
            self.data['state_flags'] = state['flags']
            self.data['state_text'] = state['text']
            d_temp = msg['current']['temps']
            if len(d_temp) > 0:
                d_temp = d_temp[0]
                d_temp_bed = d_temp['bed']
                self.data['bed_temps'] = d_temp_bed['actual'], d_temp_bed['target']
                d_temp_tool = d_temp['tool0']
                self.data['tool_temps'] = d_temp_tool['actual'], d_temp_tool['target']
                self.data['temperatures'] = {
                    'bed': self.data['bed_temps'], 'tool': self.data['tool_temps']}

            # job infos
            d_job = msg['current']['job']
            self.data['est_print_time'] = d_job['estimatedPrintTime']
            if d_job and d_job['filament'] and d_job['filament']['tool0']:
                self.data['filament_length'] = d_job['filament']['tool0']['length']
                self.data['filament_volume'] = d_job['filament']['tool0']['volume']
            self.data['filename'] = d_job['file']['display']

            self.data['progress_completion'] = msg['current']['progress']['completion']
            self.data['print_time'] = msg['current']['progress']['printTime']
            self.data['print_time_left'] = msg['current']['progress']['printTimeLeft']
            # print(job_info)
            # print(printer)
            print(self.data)
            self.update_ui()
        except Exception as ex:

            traceback.print_exc()
            print(ex)
            print(str(ex)+str(sys.exc_info()[-1].tb_lineno))

    def on_error(self, err):
        print("Error " + err)

    def on_close(self):
        print("Close")

    def init_client(self):
        while True:
            try:
                client = OctoRest(url=self.octo_url, apikey=self.octo_key)
                return client
            except Exception as ex:
                print(ex)
                time.sleep(10)

    def buttonclicked(self, i):
        try:
            if i == 0:
                QApplication.exit(3)
                self.client.home()
            elif i == 1:
                self.client.cancel()
            if i == 2:
                self.client.toggle()
            if i == 3:
                self.client.gcode("M109 S190\nG91\nG1 E-550 F4000\nM18 E")
                input("Press Enter to continue...")
                self.client.gcode("G1 E550 F2000\nM104 S0\nG90\nM18")


# Changer filament GCode
# M109 S190
# G91
# G1 E-550 F4000
# M18 E
# Keypress
# G1 E550 F2000
# M104 S0
# G90
# M84

            if i == 4:
                self.client.gcode("G28")
                print(self.client.gcode("G29"))
            else:
                print("Not implemented yet")
        except Exception as ex:
            print("Error" + str(ex))

    def build_ui(self):
        self.app = QApplication(sys.argv)
        self.app.setOverrideCursor(Qt.BlankCursor)
        app = self.app
        w = QWidget()
        sshFile = "./style.css"
        with open(sshFile, "r") as fh:
            app.setStyleSheet(fh.read())

        w.showFullScreen()
        w.setWindowTitle('OctoTouch')

        # Left / Right for MainButtons

        layout_main = QHBoxLayout()
        self.layout_main = layout_main
        layout_main.setSpacing(0)
        layout_main.setContentsMargins(0, 0, 0, 0)
        # Layout for Content / Temps
        layout_content = QVBoxLayout()
        layout_content.setSpacing(0)
        layout_content.setContentsMargins(0, 0, 0, 0)

        buttons = MyMainButtons()
        buttons.clicked.connect(self.buttonclicked)
        self.main_buttons = buttons
        layout_main.addLayout(layout_content)
        layout_main.addWidget(buttons)

        main_content = MyContent()
        temp_content = MyTemps()
        self.temp_content = temp_content
        self.main_content = main_content
        layout_content.addWidget(main_content)
        layout_content.addWidget(temp_content)

        w.setLayout(layout_main)
        w.show()

        timer = QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(100)
        sys.exit(app.exec_())

    def update_ui(self):
        data = self.data
        self.temp_content.setTemps(data["temperatures"])
        self.main_buttons.setStates(data["state_flags"])
        self.main_content.setData(data)


def sigint_handler(*args):
    sys.stderr.write('\r')
    if ask and QMessageBox.question(None, '', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
        QApplication.quit()
    else:
        QApplication.quit()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    piui = PIUI()
