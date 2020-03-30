from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui.basic import *
from ui.utils import *
import sys, random

class MyMesh(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        self.setMaximumSize(200,200)
        self.setMinimumHeight(200)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
        self.points=[]

    def paintEvent( self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
    
    def getXY(self,x,y,z):
        return (y/2.0+x/2)*2+self.width()/2, (-y/2+x/2-z*20.0)/2+self.height()/2

    def setPoints(self,points):
        self.points=[float(p) for p in points]
        av=sum(self.points) / len(self.points) 
        self.points=[av-p for p in self.points]

    def drawPoints(self, qp):
        if not len(self.points) == 9:
            return
        xs=[-110,0,110]
        ys=[-110,0,110]
        zs=self.points
        ps=[]
        i=0
        qp.setPen(QColor(255,255,255))
        qp.setFont(QFont('Arial', 10))
        for yy in ys:
            for xx in xs:
                
                ps.append(self.getXY(xx,yy,zs[i]))
                        
                x,y=self.getXY(xx,yy,-2)
                qp.drawText(x,y, "{:.2f}".format(zs[i]))  
                i+=1
        ll=["LF","RF","LB","RB"]
        xl=len(xs)
        yl=len(ys)
        qp.setPen(QColor(255,255,255))
        qp.setFont(QFont('Arial', 12,weight=QFont.Bold))        
        lxs=[(xs[0],ys[0]),(xs[xl-1],ys[0]),(xs[0],ys[yl-1]),(xs[xl-1],ys[yl-1])]
        pen = QPen(QColor(27,92,193), 2, Qt.SolidLine)
        i=0
        for p in lxs:
            xx,yy=p
            x,y=self.getXY(xx,yy,0)
            qp.drawText(x-10,y-10,ll[i])
            i+=1
        qp.setPen(pen)
        # x lines

        for o in range(yl):
            for i in range(xl-1):
                x1,y1=ps[i+o*xl]
                x2,y2=ps[i+1+o*xl]
                qp.drawLine(x1,y1,x2,y2)
        # y lines
        pen.setStyle(Qt.DashLine)
        for o in range(xl):
            for i in range(yl-1):
                x1,y1=ps[i*xl+o]
                x2,y2=ps[(i+1)*xl+o]
                qp.drawLine(x1,y1,x2,y2)



        pen.setStyle(Qt.DotLine)
        pen.setStyle(Qt.DashDotDotLine)
        pen.setStyle(Qt.CustomDashLine)

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

        self.mesh_widget=MyMesh(self)
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

    def setMesh(self,mesh):
        self.mesh_widget.setPoints(mesh)

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

