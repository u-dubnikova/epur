from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from epur_data import EpurData
import math
class EpurDraw(QWidget):
    def __init__(self, parent = None, Data = None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.data = Data
    def SetData(self,Data):
        self.data = Data
    def DrawLeft(self):
        d0 = self.geometry().width()/20
        dh = self.geometry().height()/5
        self.paint.drawLine(d0,0,d0,dh)
        for i in range(5):
            self.paint.drawLine(d0,i*dh/5,0,(i+1)*dh/5)
    def DrawRight(self):
        w = self.geometry().width()
        d0 = self.geometry().width()/20
        dh = self.geometry().height()/5

        self.paint.drawLine(w-d0,0,w-d0,dh)
        for i in range(5):
            self.paint.drawLine(w-d0,(i+1)*dh/5,w,i*dh/5)
    def DrawRods(self):
        w = self.geometry().width()
        h = self.geometry().height()
        h0 = self.geometry().height()/10
        d0 = w/20
        w1 = w*0.9

        rh_max = max([math.sqrt(l[1]) for l in self.data.data])
        rl = sum([l[0] for l in self.data.data])

        x = d0
        dh = 3*h/25

        for [l,a] in self.data.data:
            dx = l*w1/rl
            print(l,dx,w1)
            dy = math.sqrt(a)*dh/(2*rh_max)
            self.paint.drawRect(x,h0-dy,dx,dy*2)
            x += dx

    def paintEvent(self, event):
        if self.parent != None:
            self.setGeometry(0,0,self.parent.geometry().width(), self.parent.geometry().height())
        self.paint = QPainter()
        self.paint.begin(self)
        self.paint.setBrush(Qt.black);
        self.paint.drawRect(event.rect());
        if self.data != None:
            self.paint.setPen(Qt.white);
            self.DrawLeft()
            print(self.data)
            if self.data.twosided:
                self.DrawRight()
            self.DrawRods() 
        self.paint.end()
