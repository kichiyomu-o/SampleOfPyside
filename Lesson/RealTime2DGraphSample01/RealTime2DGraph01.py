# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'thermal_test.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import os
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

CURRENT_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
drive_letters = ["D:","E:","F:","G:","H:","I:","J:","K:","L:","M:","N:","O:","P:","Q:","R:","S:","T:"]
drive_serials = ["" for i in range(len(drive_letters))]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(864, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")

        checkBox_name = [f'checkBox_{drive_letter.replace(":","")}' for drive_letter in drive_letters]
        self.checkBoxes = [QCheckBox(self.frame_2) for drive_letter in drive_letters]
        for num, drive_letter in enumerate(drive_letters):
            drive_serial = drive_serials[num]
            self.checkBoxes[num].setObjectName(checkBox_name[num])
            if num == 0:
                sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
                sizePolicy2.setHorizontalStretch(0)
                sizePolicy2.setVerticalStretch(0)
                sizePolicy2.setHeightForWidth(self.checkBoxes[num].sizePolicy().hasHeightForWidth())
            self.checkBoxes[num].setSizePolicy(sizePolicy2)
            self.verticalLayout.addWidget(self.checkBoxes[num])
            self.checkBoxes[num].setText(QCoreApplication.translate("MainWindow", drive_letter+drive_serial, None))

        self.pushButton_transfer = QPushButton(self.frame_2)
        self.pushButton_transfer.setObjectName(u"pushButton_transfer")
        sizePolicy2.setHeightForWidth(self.pushButton_transfer.sizePolicy().hasHeightForWidth())
        self.pushButton_transfer.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.pushButton_transfer)

        self.pushButton_start = QPushButton(self.frame_2)
        self.pushButton_start.setObjectName(u"pushButton_start")
        sizePolicy2.setHeightForWidth(self.pushButton_start.sizePolicy().hasHeightForWidth())
        self.pushButton_start.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.pushButton_start)

        self.pushButton_stop = QPushButton(self.frame_2)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        sizePolicy2.setHeightForWidth(self.pushButton_stop.sizePolicy().hasHeightForWidth())
        self.pushButton_stop.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.pushButton_stop)

        self.horizontalLayout.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.graphicsView = pg.GraphicsLayoutWidget(self.frame_3)
        # self.graphicsView = QGraphicsView(self.frame_3)
        self.graphicsView.setObjectName(u"graphicsView")

        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy4)

        self.graphicsView.setWindowTitle('pyqtgraph example: Scrolling Plots')

        self.p4 = self.graphicsView.addPlot()
        self.p4.setDownsampling(mode='peak')
        self.p4.setClipToView(True)
        self.curve4 = self.p4.plot()

        self.data3 = np.empty(100)
        self.ptr3 = 0

        self.verticalLayout_3.addWidget(self.graphicsView)

        self.horizontalLayout.addWidget(self.frame_3)

        self.verticalLayout_2.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 864, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_transfer.setText(QCoreApplication.translate("MainWindow", u"\u30c7\u30fc\u30bf\u8ee2\u9001", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"\u958b\u59cb", None))
        self.pushButton_stop.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))

        self.pushButton_transfer.clicked.connect(self.transfer_action)
        self.pushButton_start.clicked.connect(self.start_action)
        self.pushButton_stop.clicked.connect(self.stop_action)
        
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.loop)
        self.timer.start()

    # retranslateUi

    def transfer_action(self):
        print("transfer_action")

    def start_action(self):
        print("start_action")

    def stop_action(self):
        self.update2()
        print("stop_action")
        self.timer.stop()

    def update2(self):
        print("update")
        self.data3[self.ptr3] = np.random.normal()
        self.ptr3 += 1
        if self.ptr3 >= self.data3.shape[0]:
            tmp = self.data3
            self.data3 = np.empty(self.data3.shape[0] * 2)
            self.data3[:tmp.shape[0]] = tmp
        self.curve4.setData(self.data3[:self.ptr3])

    def loop(self):
        self.update2()


class Data():
    pass


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    pg.exec()

    sys.exit(app.exec_())
