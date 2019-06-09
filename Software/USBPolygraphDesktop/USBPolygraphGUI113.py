'''
**********************************************************
  USB POLYGRAPH SOFTWARE VERSION 1.13 - GUI (2/2)
  First released to the public on MAY 2019
  Written by JuanGg on JUNE 2018
  https://juangg-projects.blogspot.com/
This work is licensed under GNU General Public License v3.0
***********************************************************
'''
# Import modules
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
import pyqtgraph as pg


# MainWindow class
class MainWindow(QtWidgets.QWidget):

    # Class constructor
    def __init__(self):
        super().__init__()
        print("Initializing gui...", end="")

        self.vbox1_width = 120
        self.vbox3_width = 100

        # Initialize all widgets and layouts
        self.init_hbox1()
        self.init_vbox1()
        self.init_vbox2()
        self.init_vbox3()
        self.init_hbox2()
        self.init_hbox3()
        self.init_vbox4()

        self.setLayout(v_box4)

        # Name of the window
        self.setWindowTitle("USB Polygraph Software - V.1.13 - Juan Gg")

        self.show()

        print("OK")

    def init_vbox1(self):  # Left side buttons menu.
        self.logo_lbl = QtWidgets.QLabel()
        self.logo_lbl.setPixmap(QtGui.QPixmap("logo.png"))

        self.help_btn = QtWidgets.QPushButton("Help")

        self.ser_start_btn = QtWidgets.QPushButton("Start")
        self.ser_stop_btn = QtWidgets.QPushButton("Stop")

        self.load_qtns_btn = QtWidgets.QPushButton("Load question set")

        self.new_exam_btn = QtWidgets.QPushButton("New exam")
        self.open_exam_btn = QtWidgets.QPushButton("Open exam")

        self.exam_advance_btn = QtWidgets.QPushButton(">")
        self.exam_reverse_btn = QtWidgets.QPushButton("<")

        # Organize widgets in labeled groups.
        serialGb = QGroupBox("Connection")
        serialVBox = QVBoxLayout()
        serialVBox.addLayout(h_box1)
        serialVBox.addWidget(self.ser_connect_btn)
        serialVBox.addWidget(self.ser_start_btn)
        serialVBox.addWidget(self.ser_stop_btn)
        serialGb.setLayout(serialVBox)

        newExamGb = QGroupBox("Record Exam")
        newExamVBox = QVBoxLayout()
        newExamVBox.addWidget(self.new_exam_btn)
        newExamVBox.addWidget(self.load_qtns_btn)
        newExamGb.setLayout(newExamVBox)

        openExamGb = QGroupBox("Open Exam")
        openExamVBox = QVBoxLayout()
        openExamVBox.addWidget(self.open_exam_btn)
        openExamVBox.addWidget(self.exam_advance_btn)
        openExamVBox.addWidget(self.exam_reverse_btn)
        openExamGb.setLayout(openExamVBox)

        serialGb.setFixedWidth(self.vbox1_width)
        openExamGb.setFixedWidth(self.vbox1_width)
        newExamGb.setFixedWidth(self.vbox1_width)

        global v_box1
        v_box1 = QtWidgets.QVBoxLayout()
        v_box1.addWidget(self.logo_lbl)
        self.logo_lbl.setMaximumWidth(self.vbox1_width)
        self.logo_lbl.setMaximumHeight(self.vbox1_width * 1.5)
        v_box1.addWidget(self.help_btn)

        v_box1.addWidget(serialGb)
        v_box1.addWidget(newExamGb)
        v_box1.addWidget(openExamGb)

    def init_vbox2(self):  # Graphs
        self.brt_plot = pg.PlotWidget()
        self.gsr_plot = pg.PlotWidget()
        self.hrt_plot = pg.PlotWidget()

        global v_box2
        v_box2 = QtWidgets.QVBoxLayout()
        v_box2.addWidget(self.brt_plot)
        v_box2.addWidget(self.gsr_plot)
        v_box2.addWidget(self.hrt_plot)

    def init_vbox3(self): # Right side menu & displays.
        self.brt_scale_btn = QtWidgets.QPushButton("Reset Scale")
        self.gsr_scale_btn = QtWidgets.QPushButton("Reset Scale")
        self.hrt_scale_btn = QtWidgets.QPushButton("Reset Scale")

        self.hrt_beep_btn = QtWidgets.QPushButton("Beep ON")

        self.brt_lcd = QLCDNumber(self)
        self.gsr_lcd = QLCDNumber(self)
        self.hrt_lcd = QLCDNumber(self)

        self.brt_lcd.setSegmentStyle(2)
        self.gsr_lcd.setSegmentStyle(2)
        self.hrt_lcd.setSegmentStyle(2)

        # Organize widgets in labeled groups.
        bpmGb = QGroupBox("BPM")
        bpmVBox = QVBoxLayout()
        bpmVBox.addWidget(self.brt_lcd)
        bpmVBox.addWidget(self.brt_scale_btn)
        bpmGb.setLayout(bpmVBox)

        gsrGb = QGroupBox("GSR")
        gsrVBox = QVBoxLayout()
        gsrVBox.addWidget(self.gsr_lcd)
        gsrVBox.addWidget(self.gsr_scale_btn)
        gsrGb.setLayout(gsrVBox)

        ppmGb = QGroupBox("PPM")
        ppmVBox = QVBoxLayout()
        ppmVBox.addWidget(self.hrt_lcd)
        ppmVBox.addWidget(self.hrt_beep_btn)
        ppmVBox.addWidget(self.hrt_scale_btn)
        ppmGb.setLayout(ppmVBox)

        bpmGb.setFixedWidth(self.vbox3_width)
        gsrGb.setFixedWidth(self.vbox3_width)
        gsrGb.setFixedWidth(self.vbox3_width)

        global v_box3
        v_box3 = QtWidgets.QVBoxLayout()

        v_box3.addWidget(bpmGb)
        v_box3.addWidget(gsrGb)
        v_box3.addWidget(ppmGb)

    def init_vbox4(self):  # Contains everything.
        global v_box4
        v_box4 = QtWidgets.QVBoxLayout()
        v_box4.addLayout(h_box2)
        v_box4.addLayout(h_box3)

    def init_hbox1(self):  # Contains port label and line edit.
        self.port_lbl = QtWidgets.QLabel("Port:")
        self.port_name_le = QtWidgets.QLineEdit()
        self.ser_connect_btn = QtWidgets.QPushButton("Connect")

        global h_box1
        h_box1 = QtWidgets.QHBoxLayout()
        h_box1.addWidget(self.port_lbl)
        h_box1.addWidget(self.port_name_le)
        self.port_lbl.setMaximumWidth(self.vbox1_width * 0.2)
        self.port_name_le.setMaximumWidth(self.vbox1_width * 0.8)

    def init_hbox2(self):  # Contains left & riht menu and graphs
        global h_box2
        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addLayout(v_box1)
        h_box2.addLayout(v_box2)
        h_box2.addLayout(v_box3)

    def init_hbox3(self): # Contains question label and time lcd
        f1 = QtGui.QFont("Default", 16)
        f2 = QtGui.QFont("Default", 32)

        self.question_lbl = QtWidgets.QLabel("No questions loaded")
        self.sec_min_lbl = QtWidgets.QLabel(":")
        self.question_lbl.setFont(f1)
        self.sec_min_lbl.setFont(f2)

        self.min_lcd = QLCDNumber(self)
        self.sec_lcd = QLCDNumber(self)

        self.sec_lcd.setSegmentStyle(2)
        self.min_lcd.setSegmentStyle(2)

        self.sec_lcd.setDigitCount(2)
        self.min_lcd.setDigitCount(2)

        self.sec_lcd.setMinimumHeight(50)
        self.sec_lcd.setMaximumWidth(80)
        self.sec_min_lbl.setMaximumWidth(10)
        self.min_lcd.setMaximumWidth(80)

        qtnGb = QGroupBox("Question")
        qtnHBox = QHBoxLayout()
        qtnHBox.addWidget(self.question_lbl)
        qtnGb.setLayout(qtnHBox)

        timeGb = QGroupBox("Time")
        timeHBox = QHBoxLayout()
        timeHBox.addWidget(self.min_lcd)
        timeHBox.addWidget(self.sec_min_lbl)
        timeHBox.addWidget(self.sec_lcd)
        timeGb.setLayout(timeHBox)

        timeGb.setFixedWidth(200)

        global h_box3
        h_box3 = QtWidgets.QHBoxLayout()

        h_box3.addWidget(qtnGb)
        h_box3.addWidget(timeGb)


# Enable the gui to be run by itself if needed & make the code reusable

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
