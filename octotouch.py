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

from ui.buttons import *
from ui.temppanel import *
from ui.content import *
import ui.utils

ask = False
host = "printerpi.local:5000"
style="default_style.css"

class PIUI(object):

    def act_stop(self):
        self.client.cancel()

    def act_switch(self):
        self.client.gcode("M109 S190\nG91\nG1 E-550 F4000\nM18 E")
        # self.client.gcode("G1 E550 F2000\nM104 S0\nG90\nM18")

    def act_test(self):
        pass

    def act_home(self):
        self.client.home()

    def act_present(self):
        self.client.gcode("G90\nG1 X0 Z50\nG1 Y220 F5000\n")


    def act_update(self):
        QApplication.exit(3)
    
    def act_mesh(self):
        self.client.gcode("G28\nG29\n")

    def __init__(self):
        self.octo_url = host
        self.octo_key = "0bd8c77e808a8e5e3c53ce13696317fa"
        self.client = None
        self.app = None
        self.data = {}
        self.connected=False

        self.content_widget = None
        self.tempt_content = None
        self.main_buttons = None
        self.layout_main = None
        self.client = self.init_client()
        self.logs = []
        self.mesh=[]
        self.menu_print=[{'STOP':{"func": self.act_stop}}]
        self.menu_idle=[
                        {"label":"home", "func": self.act_home},
                        {"label":"present", "func": self.act_present},
                        {'label':'change',"func": self.act_switch},
                        {"label":'test',"func":self.act_test},
                        {"label":'mesh',"func":self.act_mesh},
                        {"label":'update',"func":self.act_update}
                        ]

        # Our DataStructure
        self.data = {
            "state_flags": {},
            "state_text": "",
            "bed_temps": "",
            "tool_temps": "",
            "est_print_time": "",
            "filament_length": None,
            "filament_volument": "",
            "filename": "",
            "progress_completion": "",
            "print_time": "",
            "print_time_left": "",
            "temperatures": {"bed": [], "tool": []},
        }

        self.uri = "ws://{}/sockjs/websocket".format(host)
        self.ws = websocket.WebSocketApp(self.uri,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.wst = threading.Thread(target=self.ws.run_forever)
        self.wst.daemon = True
        self.wst.start()
        self.build_ui()

    def setConnected(self,b):
        self.connected=b
        if b == True:
            self.main_buttons.show()
            self.temp_content.show()
        else:
            self.main_buttons.hide()
            self.temp_content.hide()

    def addlog(self,log):
        self.logs+=log
        self.logs=self.logs[-10:]
        self.handle_logs()

    # Will take care of handling events for log-entries. currently only meshing needs it, so its pretty simple
    def handle_logs(self):
        t="Recv: Bilinear Leveling Grid:"
        if t in self.logs:
            i=self.logs.index(t)
            if i>0 and i< len(self.logs)-5:
                level=self.logs[i+2:i+5]
                self.mesh=[item for sublist in level for item in sublist.split(" ")[3:]]
                self.logs=self.logs[i+5:]
                self.handle_mesh(self.mesh)

    def handle_mesh(self,mesh):
        # Needs logic
        print(mesh)
        self.main_content.setMesh(mesh)

    def on_message(self, msgstr):
        try:
            msg = json.loads(msgstr)
            if "current" in msg:  # Hisotry / timelapse / event
                self.on_message_current(msg["current"])
                self.update_ui()
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            print(str(ex)+str(sys.exc_info()[-1].tb_lineno))

    def on_message_current(self,cmsg):
            state = cmsg['state']
            #print("State is "+ str(state))
            if "logs" in cmsg:
                self.addlog(cmsg["logs"])
            self.data['state_flags'] = state['flags']
            if state['flags']['operational']:
                self.setConnected(True)
            else:
                self.setConnected(False)

            self.data['state_text'] = state['text']
            current=cmsg
            if "temps" in current:
                d_temp = current['temps']
                if len(d_temp) > 0:
                    d_temp = d_temp[0]
                    if "bed" in d_temp:
                        d_temp_bed = d_temp['bed']
                        self.data['bed_temps'] = d_temp_bed['actual'], d_temp_bed['target']
                    if "tool0" in d_temp:
                        d_temp_tool = d_temp['tool0']
                        self.data['tool_temps'] = d_temp_tool['actual'], d_temp_tool['target']
                    self.data['temperatures'] = {
                        'bed': self.data['bed_temps'], 'tool': self.data['tool_temps']}

            # job infos
            if "job" in current:
                d_job = current['job']
                self.data['est_print_time'] = d_job['estimatedPrintTime']
                if d_job and d_job['filament'] and d_job['filament']['tool0']:
                    self.data['filament_length'] = d_job['filament']['tool0']['length']
                    self.data['filament_volume'] = d_job['filament']['tool0']['volume']
                self.data['filename'] = d_job['file']['display']

                self.data['progress_completion'] = cmsg['progress']['completion']
                self.data['print_time'] = cmsg['progress']['printTime']
                self.data['print_time_left'] = cmsg['progress']['printTimeLeft']


    def on_error(self, err):
        print("Error " + err)

    def on_close(self):
        print("Close")

    def init_client(self):
        print("Initializing OctoREST client...")
        while True:
            try:
                client = OctoRest(url="http://{}".format(self.octo_url), apikey=self.octo_key)
                print("Initialized OctoREST client")
                state=client.state()
                print(str(state))
                print(str(client.connection_info()))
                #
                if "Error" in state or "Closed" in state :
                    print("Printer is not connected. Trying to connect...")
                    print(client.connect())
                return client
            except Exception as ex:
                print("Initialized of OctoREST client failed. Retrying in 10secs...")
                print(ex)
                time.sleep(10)



    def build_ui(self):
        self.app = QApplication(sys.argv)
        self.app.setOverrideCursor(Qt.BlankCursor)
        app = self.app
        w = QWidget()
        sshFile = "./styles/"+style
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
        buttons.setMenu(self.menu_idle)
        self.main_buttons = buttons
        layout_main.addLayout(layout_content)
        layout_main.addWidget(buttons)

        main_content = MyContent()
        temp_content = MyTemps()
        self.temp_content = temp_content
        self.main_content = main_content
        self.main_content.setMesh(['+1.143', '+1.242', '+1.250', '+1.178', '+1.268', '+1.230', '+1.155', '+1.270', '+1.230'])
        layout_content.addWidget(main_content)
        layout_content.addWidget(temp_content)

        w.setLayout(layout_main)
        w.show()
        # We need to give Control back to Python to make CTRL-C work
        timer = QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(100)
        self.setConnected(False)
        sys.exit(self.app.exec_())


    def update_ui(self):
        data = self.data
        self.temp_content.setTemps(data["temperatures"])
        self.main_buttons.setStates(data["state_flags"])
        self.main_content.setData(data)

def sigint_handler(*args):
        QApplication.quit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    piui = PIUI()
