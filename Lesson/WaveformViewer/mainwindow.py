# This Python file uses the following encoding: utf-8
import array
import binascii
from ctypes import *
import glob
import os
from pathlib import Path
import struct
import sys

import cv2
import numba
import numpy as np

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import QFile, Qt, QRect, QPoint, QObject, Slot, Signal, QThread
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QClipboard, QImage, QPixmap, QFont

import pyqtgraph as pg
import pyqtgraph.exporters

'''-------------------------------------------------------------
        Servo signal format structure
-------------------------------------------------------------'''
class WaveformHeader(LittleEndianStructure):
    _fields_ = (
        ('HeaderSize', c_int16),      #   0
        ('HeaderVer', c_int16),       #   2
        ('DataSize', c_uint32),       #   4
        ('FS', c_float),              #   8
        ('Year', c_uint16),           #  12
        ('Month', c_byte),            #  14
        ('Date',  c_byte),            #  15
        ('Hour',  c_byte),            #  16
        ('Minute',  c_byte),          #  17
        ('Second',  c_byte),          #  18
        ('MilSecond',  c_byte),       #  19
        ('Reserved',  c_char * 108),  #  20
    )


'''-------------------------------------------------------------
       Class Waveform
-------------------------------------------------------------'''
class Waveform():
    def __init__(self):
        self.Header = WaveformHeader()
        self.Signal = np.array(0)              #--- Waveform
        self.Time = np.array(0)                #--- Time line
        self.FftSignal = np.array(0)           #--- Servo signal after fft
        self.Frequency = np.array(0)           #--- Frequency
        self.SampleN = self.Header.DataSize
        self.FS = self.Header.FS
        self.Data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.wData = np.array(self.Data)
        if self.FS == 0.0:
            self.FS = 1/46694

    def read(self, FileName):
        """read waveform data of binary format

        Args:
            FileName (str): File name for read
        """
        with open(FileName , "rb") as rf:
            rf.readinto(self.Header)
            #if self.Header.HeaderSize!=128 or self.Header.HeaderVer!=0:
            #    logger.error('Unsupported data format in reading servo signal!')
            #    ProgramExit(1)

            self.SampleN = int(self.Header.DataSize/2)
            self.Data = array.array('h',[0]*self.SampleN)
            rf.readinto(self.Data)
            if sys.byteorder != 'little':
                self.Data.byteswap()

        self.wData = np.array(self.Data)
        self.Signal = np.array(self.wData / 4096 * 18.1)
        self.Time = np.arange(0, self.SampleN*self.FS, self.FS)

    def save(self, FileName):
        """save waveform data of binary format

        Args:
            FileName (str): File Name for save
        """
        with open(FileName, "wb") as wf:
            wf.write(self.Header)
            fmt = f"{str(len(self.wData))}h"
            print(len(self.wData))
            self.Data = struct.pack(fmt, *list(self.wData))
            wf.write(self.Data)

    def setData(self, values, fs=0.001):
        """set Data

        Args:
            values (np.ndarray): set graph data
            fs (float, optional): sample frequency. Defaults to 0.001.
        """
        self.FS = fs
        self.SampleN = len(values)
        self.Signal = values
        self.Time = np.arange(0, self.SampleN*self.FS, self.FS)
        self.fft()

    def fft(self):
        """fft processing for signal
        """
        self.FftSignal = np.fft.fft(self.Signal, norm='ortho')
        # self.FftAmp = np.sqrt(self.FftSignal.real**2 + self.FftSignal.imag**2)
        self.FftAmp = np.abs(self.FftSignal)
        self.Frequency = np.fft.fftfreq(self.SampleN, d=self.FS)/1000


class MyPlotWidget(pg.PlotWidget):
    """
    https://pyqtgraph.readthedocs.io/en/latest/widgets/plotwidget.html?highlight=PlotWidget
    """
    def __init__(self, parent, xtitle="", ytitle="", *args, **kwargs):
        self.parent = parent
        self.__xlabel = xtitle
        self.__ylabel = ytitle
        self.verticalLayout = QVBoxLayout(self.parent)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graph = pg.PlotWidget(self.parent)
        self.graph.setObjectName("graph")
        self.pi = self.graph.plotItem
        self.pi.setLabels(bottom = self.__xlabel, left = self.__ylabel)
        self.verticalLayout.addWidget(self.graph)
        self.clipboard = QApplication.clipboard()

    def plot(self, x=[], y=[], clear=False, color="b", style=Qt.SolidLine):
        """plot graph

        Args:
            x (list, optional): datas for x-axis. Defaults to [].
            y (list, optional): datas for y-axis. Defaults to [].
            clear (bool, optional): if this option is set, plot area is cleared before plot. Defaults to False.
            color (str, optional): line color. Defaults to "b".
            style (Qt.SolidLine, optional): line style. Defaults to Qt.SolidLine.
        """
        pen = pg.mkPen(color = color, style = style)
        if (len(x) == 0) | (len(y) == 0):
            frq = 4.0
            duration = 1.0
            samples = 1001
            x = np.linspace(0, duration, samples)
            rad = np.linspace(0, 2 * np.pi * frq, samples)
            y = np.cos(rad)
        elif len(x) != len(y):
            raise("size Error")
        if clear == True:
            self.graph.clear()
        self.graph.plot(x, y, pen=pen)

    def xaxis(self, title):
        """xaxis setting

        Args:
            title (str): x-axis title
        """
        self.__xlabel = title
        font = QFont("Times New Roman", 7)
        self.graph.getAxis("bottom").tickFont = font
        self.pi.setLabels(bottom = self.__xlabel)


    def yaxis(self, title):
        """yaxis setting

        Args:
            title (str): y-axis title
        """
        font = QFont("Times New Roman", 7)
        self.graph.getAxis("left").tickFont = font
        self.pi.setLabels(left = self.__ylabel)

    def save(self):
        """save image to file 
        """
        exporter = pg.exporters.ImageExporter(self.graph.plotItem)
        exporter.parameters()["width"] = 480
        fileName = QFileDialog().getSaveFileName(self, "Save File",
                                   "./graph01.png",
                                   "Images (*.png *.xpm *.jpg)")[0]
        exporter.export(fileName)

    def setfont(self):
        """set font for axis
        """
        ## 4 軸ラベルのフォントを設定する
        fontCss = {'font-family': "Times New Roman, メイリオ", 'font-size': '10.5pt', "color": "black"}
        self.graph.getAxis('bottom').setLabel(**fontCss)
        self.graph.getAxis('left').setLabel(**fontCss)

    def clip(self):
        """copy image to clipboard
        """
        exporter = pg.exporters.ImageExporter(self.graph.plotItem)
        exporter.parameters()["width"] = 480
        exporter.export("clipimage.png")
        self.image = QImage("clipimage.png")
        self.clipboard.setImage(self.image)

    def clear(self):
        """clear graph
        """
        self.graph.clear()

    @property
    def xtitle(self):
        """title of x-axis

        Returns:
            str: x-axis title
        """
        return self.__xtitle

    @xtitle.setter
    def xtitle(self, title):
        self.__xtitle = title

    @property
    def ytitle(self):
        """title of y-axis

        Returns:
            str: y-axis title
        """
        return self.__ytitle

    @xtitle.setter
    def ytitle(self, title):
        self.__ytitle = title


class MainWindow(QMainWindow):
    __folder = None
    __filepath = None
    waveform = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()
        self.waveform = Waveform()
        """
        frq = 4.0
        duration = 1.0
        samples = 1001
        x = np.linspace(0, duration, samples)
        rad = np.linspace(0, 2 * np.pi * frq, samples)
        y = np.cos(rad)
        """
        data = Waveform()
        rad = np.linspace(0, 2 * np.pi * 10, 1001)
        values = np.sin(rad[:1000])
        fs = 1/1000
        data.setData(values, fs)
        self.graph01.plot(data.Time, data.Signal)
        self.graph02.plot(data.Frequency[:500], data.FftAmp[:500])

        self.image = QImage()
        self.clip = QApplication.clipboard()
        self.__ui.show()

    def load_ui(self):
        """load user interface
        """
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "qWaveformViewer.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.__ui = loader.load(ui_file, self)
        ui_file.close()

        self.graph01 = MyPlotWidget(self.__ui.openGLWidget, "time(ms)", "Voltage(mV)")
        self.graph02 = MyPlotWidget(self.__ui.openGLWidget_2, "frequency(kHz)", "Amplitude")

        self.__ui.actionFOLDER.triggered.connect(self.getFolder)
        self.__ui.actionREAD.triggered.connect(self.readFile)
        self.__ui.actionSAVE.triggered.connect(self.saveFile)
        self.__ui.actionQUIT.triggered.connect(self.quit)
        self.__ui.pushButton_FOLDER.clicked.connect(self.getFolder)
        self.__ui.pushButton_SAVE1.clicked.connect(self.graph01.save)
        self.__ui.pushButton_SAVE2.clicked.connect(self.graph02.save)
        self.__ui.pushButton_CLIP1.clicked.connect(self.graph01.clip)
        self.__ui.pushButton_CLIP2.clicked.connect(self.graph02.clip)
        self.__ui.pushButton_CLIP.clicked.connect(self.copyClipBoard)

        self.__ui.listWidget.itemClicked.connect(self.h_lw)


    def getFolder(self):
        """set selected folder's files to listwidget
        """
        self.__folder = QFileDialog().getExistingDirectory()
        self.__ui.listWidget.clear()
        for filepath in glob.glob(f"{self.__folder}\*.*"):
            folder, fname = os.path.split(filepath)
            # item = QListWidgetItem.setText(fname)
            if ".bin" in fname or ".csv" in fname:
                self.__ui.listWidget.addItem(fname)

    def readFile(self):
        """read File
        """
        self.__filepath = QFileDialog().getOpenFileName()[0]
        fext = os.path.splitext(self.__filepath)[1]
        if fext == ".bin":
            self.waveform.read(self.__filepath)
            self.waveform.fft()
            self.plotClear()
            self.plot1(self.waveform.Time, self.waveform.Signal)
            n = int(self.waveform.SampleN/2)
            self.plot2(self.waveform.Frequency[:n], self.waveform.FftAmp[:n])

    def saveFile(self):
        """save File
        """
        self.__filepath = QFileDialog().getSaveFileName()[0]
        self.waveform.save(self.__filepath)

    def h_lw(self, item):
        """handle of listwidget

        Args:
            item (QListWidgetItem): selected item
        """
        fname = item.text()
        fpath = os.path.join(self.__folder, fname)
        self.waveform.read(fpath)
        self.waveform.fft()
        self.graph01.plot(self.waveform.Time, self.waveform.Signal, clear=True)
        n = int(len(self.waveform.Frequency)/2)
        self.graph02.plot(self.waveform.Frequency[:n], self.waveform.FftAmp[:n], clear=True)

    def copyClipBoard(self, fr=None):
        """copy image to clipboard

        Args:
            fr ([type], optional): [description]. Defaults to None.
        """
        fr = self.__ui.frame_2
        width = fr.geometry().width()
        height = fr.geometry().height()
        print(fr.geometry())
        print(width, height)
        # self.image = QImage(width, height, QImage.Format_RGB32)
        self.image = QPixmap(width, height)
        self.image.copy(rect=fr.geometry())
        self.image.save("clipboard_0.png", "PNG")
        self.clip.setPixmap(self.image)

    def quit(self):
        print("quit")

    @property
    def ui(self):
        return self.__ui

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
