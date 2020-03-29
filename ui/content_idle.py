from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui.basic import *
from ui.utils import *

from OpenGL.GL import *
from OpenGL.GLU import *

class glWidget(QOpenGLWidget):

    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        #super(glWidget, self).__init__(parent)
        self.setMinimumSize(100, 100)
        self.setMaximumSize(200,200)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(-2.5, 0.5, -6.0)
        glColor3f( 1.0, 1.5, 0.0 )
        glPolygonMode(GL_FRONT, GL_FILL)
        glBegin(GL_TRIANGLES)
        glVertex3f(2.0,-1.2,0.0)
        glVertex3f(2.6,0.0,0.0)
        glVertex3f(2.9,-1.2,0.0)
        glEnd()
        glFlush()

    def initializeGL(self):
        glClearDepth(1.0)              
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                    
        gluPerspective(45.0,1.33,0.1, 100.0) 
        glMatrixMode(GL_MODELVIEW)

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

        self.mesh_widget=glWidget(self)
        layout.addWidget(self.mesh_widget)

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

