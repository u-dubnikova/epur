#!/usr/bin/env python3
from PyQt5 import QtWidgets
from epur_ui import Ui_MainWindow
from epur_draw import EpurDraw
from epur_data import *
import sys
class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AppWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionLoad.triggered.connect(self.fileLoad)
        self.EpurDraw = EpurDraw(self.ui.widget)
    def fileLoad(self):
        l = QtWidgets.QFileDialog.getOpenFileName(self,"Выберите конфигурацию","","Стержни (*.epr);;Все файлы (*)")
        print(l)
        ed = LoadEpur(l[0])
        self.EpurDraw.SetData(ed)
        self.EpurDraw.repaint()

app = QtWidgets.QApplication([])
application = AppWindow()
application.show()
 
sys.exit(app.exec())
