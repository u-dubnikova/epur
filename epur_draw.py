from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from epur_data import EpurData
import math
import itertools
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
        if len(self.data.rods) == 0:
            return
        w = self.geometry().width()
        h = self.geometry().height()
        h0 = self.geometry().height()/10
        d0 = w/20
        w1 = w*0.9

        rh_max = max([math.sqrt(l[1]) for l in self.data.rods])
        rl = sum([l[0] for l in self.data.rods])
        lmin = min([l[0] for l in self.data.rods])

        x = d0
        dh = 3*h/25

        for ([l,a],s) in zip(self.data.rods[:-1],self.data.nodes):
            dx = l*w1/rl
            dy = math.sqrt(a)*dh/(2*rh_max)
            self.paint.drawRect(x,h0-dy,dx,dy*2)
            x += dx
            if s == None or s == 0: continue
            self.paint.drawLine(x,h0-dh*0.75,x,h0+dh*0.75)
            rx = (lmin/4 if s>0 else -lmin/4)*w1/rl
            for ay in [-dh*0.75,dh*0.75]:
                self.paint.drawLine(x,h0+ay,x+rx,h0+ay)
                for ty in [0.9*ay, 1.1*ay]:
                    self.paint.drawLine(x+rx,h0+ay,x+0.9*rx,h0+ty)
        [l,a] = self.data.rods[-1]
        dy = math.sqrt(a)*dh/(2*rh_max)
        dx = d0+w1-x
        self.paint.drawRect(x,h0-dy,dx,dy*2)

        if self.data.twosided or self.data.nodes[-1] == 0: 
            return
        x += dx
        self.paint.drawLine(x,h0,w,h0)
        rx = w-x
        ay = rx/10
        if self.data.nodes[-1] < 0:
            x = w
            rx = -rx
        for ty in [-ay, ay]:
            self.paint.drawLine(x+rx,h0,x+0.9*rx,h0+ty)


            
        

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
            if self.data.twosided:
                self.DrawRight()
            self.DrawRods() 
        self.paint.end()
