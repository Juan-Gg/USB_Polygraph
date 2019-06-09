'''
**********************************************************
  USB POLYGRAPH SOFTWARE VERSION 1.13 - LOGIC (1/2)
  First released to the public on MAY 2019
  Written by JuanGg on JUNE 2018
  https://juangg-projects.blogspot.com/
This work is licensed under GNU General Public License v3.0
***********************************************************
'''
# Import modules
import serial
import os
import sys
from PyQt5 import QtWidgets
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QFileDialog, QMessageBox

import winsound

from USBPolygraphGUI113 import MainWindow


class PolygraphLogic(MainWindow):
    def __init__(self):

        MainWindow.__init__(self)
        print("Initializing logic...", end="")

        self.demo_mode()
        self.set_defaults()
        self.initialize_graphs()
        self.reset_graphs()
        self.reset_exam_variables()
        self.reset_qtn_ans_markers()
        self.set_btn_functions()

        print("OK")

    # #################################################################
    #                      SETUP FUNCTIONS                            #
    # #################################################################

    def demo_mode(self):  # Display real-time data without recording.
        self.record_exam_data = False
        self.acquisition_mode = True
        self.view_exam_mode = False

    def exam_mode(self):  # Displays real-time data and records it.
        self.record_exam_data = True
        self.acquisition_mode = True
        self.view_exam_mode = False

    def view_mode(self):  # Displays data being read from a n exam file.
        self.record_exam_data = False
        self.acquisition_mode = False
        self.view_exam_mode = True

    def set_defaults(self): # Set initial values.
        # Port
        self.port_name_le.setText("com8")
        # LCDs
        self.min_lcd.display(00)
        self.sec_lcd.display(00)
        # Graphs
        self.graphs_length = 600
        self.graph_running = False
        # Rate calculations:
        self.hrt_was_below_th = True
        self.hrt_prev_above = 0
        self.hrt_last_above = 0
        self.hrt_prev_rates = [0] * 10
		
        self.brt_was_below_th = False
        self.brt_prev_above = 0
        self.brt_last_above = 0

        # Sounds
        self.hrt_sound = False

        # Graphs question and ans markers.
        self.brt_qtn_reg = []
        self.gsr_qtn_reg = []
        self.hrt_qtn_reg = []

        self.brt_ans_lin = []
        self.gsr_ans_lin = []
        self.hrt_ans_lin = []

    def reset_graphs(self):  # Clears all data from graphs.
        self.time_pos = 0
        self.brt_data = [0] * self.graphs_length
        self.gsr_data = [0] * self.graphs_length
        self.hrt_data = [0] * self.graphs_length
        self.plot_data([0, 0, 0], True)

    def reset_qtn_ans_markers(self):  # Removes all question and answer markers from graphs.

        for i in range(len(self.brt_qtn_reg)):
            self.brt_plot.removeItem(self.brt_qtn_reg[i])
            self.gsr_plot.removeItem(self.gsr_qtn_reg[i])
            self.hrt_plot.removeItem(self.hrt_qtn_reg[i])
        for j in range(len(self.brt_ans_lin)):
            self.brt_plot.removeItem(self.brt_ans_lin[j])
            self.gsr_plot.removeItem(self.gsr_ans_lin[j])
            self.hrt_plot.removeItem(self.hrt_ans_lin[j])

        self.brt_qtn_reg = []
        self.gsr_qtn_reg = []
        self.hrt_qtn_reg = []

        self.brt_ans_lin = []
        self.gsr_ans_lin = []
        self.hrt_ans_lin = []

        self.num_qtns = 0
        self.start_qtn_pos = 0

        self.qtn_asked = False
        self.qtn_being_asked = False
        self.ans_answered = True

        self.accept_questions = False

        self.qtns_file_name = ''
        self.qtns_loaded = False
        self.qtns_list = []

    def reset_exam_variables(self): # Erases all previous recorded data.
        self.exam_file_name = ''

        self.exam_brt_data = []
        self.exam_gsr_data = []
        self.exam_hrt_data = []

        self.exam_qtn_markers_start = []
        self.exam_qtn_markers_end = []
        self.exam_qtn_markers_lbl = []

        self.exam_answer_markers_pos = []
        self.exam_answer_markers_lbl = []

    def initialize_graphs(self):  # Defines graphs sizes, colours, etc.
        self.brt_data = [0] * self.graphs_length
        self.gsr_data = [0] * self.graphs_length
        self.hrt_data = [0] * self.graphs_length
        self.brt_plot2 = self.brt_plot.plot(self.brt_data, pen=pg.mkPen('c', width=1))
        self.gsr_plot2 = self.gsr_plot.plot(self.gsr_data, pen=pg.mkPen('g', width=1))
        self.hrt_plot2 = self.hrt_plot.plot(self.hrt_data, pen=pg.mkPen('r', width=1))
        self.brt_plot.showGrid(x=True, y=True, alpha=1)
        self.gsr_plot.showGrid(x=True, y=True, alpha=1)
        self.hrt_plot.showGrid(x=True, y=True, alpha=1)
        self.brt_plot.setLabel(axis="left", text="BREATH")
        self.gsr_plot.setLabel(axis="left", text="GSR")
        self.hrt_plot.setLabel(axis="left", text="PULSE")
        self.brt_reset_scale()
        self.gsr_reset_scale()
        self.hrt_reset_scale()

    def set_btn_functions(self):  # Defines what function is called upon the press of a button.
        self.help_btn.clicked.connect(self.show_help)

        self.ser_connect_btn.clicked.connect(self.ser_connect)
        self.ser_start_btn.clicked.connect(lambda: self.start_stop(True))
        self.ser_stop_btn.clicked.connect(lambda: self.start_stop(False))

        self.brt_scale_btn.clicked.connect(self.brt_reset_scale)
        self.gsr_scale_btn.clicked.connect(self.gsr_reset_scale)
        self.hrt_scale_btn.clicked.connect(self.hrt_reset_scale)

        self.load_qtns_btn.clicked.connect(self.load_qtns)

        self.open_exam_btn.clicked.connect(self.open_exam)

        self.new_exam_btn.clicked.connect(self.new_exam)

        self.hrt_beep_btn.clicked.connect(self.hrt_beep)

        self.exam_advance_btn.clicked.connect(self.exam_view_advance_graphs)
        self.exam_reverse_btn.clicked.connect(self.exam_view_reverse_graphs)

    # #################################################################
    #                      LOGIC FUNCTIONS                            #
    # #################################################################

    # ################ Open exam file & exam view mode ############################

    def open_exam(self):
        sender = self.open_exam_btn

        if self.new_exam_btn.text() == "Close / Save":
            self.end_exam()
        if self.graph_running:
            self.start_stop(False)

        self.reset_exam_variables()
        self.reset_qtn_ans_markers()
        self.reset_graphs()

        if sender.text() == "Open exam":
            self.exam_file_name = QFileDialog.getOpenFileName(self,'Open File',os.getenv('HOME'),"Text files (*.txt)")

            if self.exam_file_name[0] != "":

                self.record_exam_data = False
                self.acquisition_mode = False
                self.view_exam_mode = True
                try:
                    with open(self.exam_file_name[0], 'r') as f:
                        exam_file_list = f.read().split('\n')
                        exam_file_list = exam_file_list[2][1:-1].split('][')
                        try:
                            self.exam_brt_data = [int(x) for x in exam_file_list[0].split(', ')]
                            self.exam_gsr_data = [int(x) for x in exam_file_list[1].split(', ')]
                            self.exam_hrt_data = [int(x) for x in exam_file_list[2].split(', ')]
                        except ValueError:
                            self.exam_brt_data = []
                            self.exam_gsr_data = []
                            self.exam_hrt_data = []

                        try:
                            self.exam_qtn_markers_start = [int(x) for x in exam_file_list[3].split(', ')]
                            self.exam_qtn_markers_end = [int(x) for x in exam_file_list[4].split(', ')]
                            self.exam_qtn_markers_lbl = exam_file_list[5].split(', ')
                        except ValueError:
                            self.exam_qtn_markers_start = []
                            self.exam_qtn_markers_end = []
                            self.exam_qtn_markers_lbl = []

                        try:
                            self.exam_answer_markers_pos = [int(x) for x in exam_file_list[6].split(', ')]
                            self.exam_answer_markers_lbl = exam_file_list[7].split(', ')
                        except ValueError:
                            self.exam_answer_markers_pos = []
                            self.exam_answer_markers_lbl = []

                    sender.setText("Close exam")

                except:
                    self.show_error_message("Invalid exam file")

            else:
                print("No file chosen")

        else:
            sender.setText("Open exam")
            self.question_lbl.setText("No questions loaded")
            self.record_exam_data = False
            self.acquisition_mode = True
            self.view_exam_mode = False

            self.update()

    # Advance and reverse graphs in exam view mode.
    def exam_view_reverse_graphs(self):
        if self.view_exam_mode:
            for i in range(10):  # Make advance and reverse faster.
                self.update()
                if self.time_pos > 0:
                    self.time_pos -= 1
                    self.plot_data([self.exam_brt_data[self.time_pos - 1], self.exam_gsr_data[self.time_pos - 1],
                                    self.exam_hrt_data[self.time_pos - 1]], False)
                else:
                    print("Time = 0")

    def exam_view_advance_graphs(self):
        if self.view_exam_mode:
            for i in range(10):
                self.update()
                if self.time_pos < (len(self.exam_brt_data)):
                    self.time_pos += 1
                    self.plot_data([self.exam_brt_data[self.time_pos - 1], self.exam_gsr_data[self.time_pos - 1],
                                    self.exam_hrt_data[self.time_pos - 1]], True)
                else:
                    print("End of exam data")

    # Add and update qtn and ans markers during exam view mode
    def exam_view_add_qtn_ans_markers(self):
        for i in self.exam_qtn_markers_end:
            if i == self.time_pos:
                index = self.exam_qtn_markers_end.index(i)
                self.add_qtn_marker(self.exam_qtn_markers_start[index], i, self.exam_qtn_markers_lbl[index])

        for i in self.exam_answer_markers_pos:
            if i == self.time_pos:
                index = self.exam_answer_markers_pos.index(i)
                self.add_ans_marker(i, self.exam_answer_markers_lbl[index])

    # ################ Saving exam data & record exam mode #########################
    def new_exam(self):
        if self.open_exam_btn.text() == "Close exam":
            self.open_exam()
        sender = self.sender()
        if sender.text() == "New exam":
            self.reset_exam_variables()
            self.exam_file_name = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'),"Text files (*.txt)")
            if self.exam_file_name[0] != "":
                self.exam_mode()
                self.reset_graphs()
                self.reset_qtn_ans_markers()
                sender.setText("Close / Save")
        else:
            self.end_exam()

    # ################ Finalize exam and save data to a file #########################
    def end_exam(self):
        if self.record_exam_data:
            self.add_ans_marker(self.time_pos, "EXAM END")
            self.qtn_being_asked = True
            self.qtn_asked = False
            self.question_lbl.setText("--End of the Exam--")
            self.start_stop(False)

            self.accept_questions = False

            # Marks exam end and avoids repetition of "EXAM END" label when reading file.
            self.exam_brt_data.append(0)
            self.exam_gsr_data.append(0)
            self.exam_hrt_data.append(0)

            with open(self.exam_file_name[0], 'w') as f: # Write all data to the file.
                f.write("----Exam file----\n")
                f.write("Includes brt, gsr & hrt data, and position & label of questions and answers\n")

                f.write(str(self.exam_brt_data))
                f.write(str(self.exam_gsr_data))
                f.write(str(self.exam_hrt_data))

                f.write(str(self.exam_qtn_markers_start))
                f.write(str(self.exam_qtn_markers_end))
                f.write(str(self.exam_qtn_markers_lbl))

                f.write(str(self.exam_answer_markers_pos))
                f.write(str(self.exam_answer_markers_lbl))

            self.demo_mode()
            self.new_exam_btn.setText("New exam")

    # ################ Record data into lists to be latter saved #########################
    def record_plot_data(self, reading):  # Records graph data.
        try:
            self.exam_brt_data.append(reading[0])
            self.exam_gsr_data.append(reading[1])
            self.exam_hrt_data.append(reading[2])

        except:
            self.exam_brt_data.append(0)
            self.exam_gsr_data.append(0)
            self.exam_hrt_data.append(0)

    def record_qtns_data(self, start, end, label):  # Records question markers data.
        self.exam_qtn_markers_start.append(start)
        self.exam_qtn_markers_end.append(end)
        self.exam_qtn_markers_lbl.append(label)

    def record_ans_data(self, pos, label):  # Record answer markers data.
        self.exam_answer_markers_pos.append(pos)
        self.exam_answer_markers_lbl.append(label)

    # ############### Question File Handling ##############################

    # Uses the QFileDialog to get the name and the location of the question file
    def load_qtns(self):
        if self.record_exam_data:
            self.qtns_file_name = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'),
                                                              "Text files (*.txt)")

            if self.qtns_file_name[0] != "":
                with open(self.qtns_file_name[0], 'r') as f:
                    self.qtns_list = f.read().split('\n')
                if len(self.qtns_list) >= 3:
                    self.question_lbl.setText(self.qtns_list[2])
                    print("Question set: " + str(self.qtns_file_name[0]) + " loaded")

                    self.accept_questions = True
                    self.qtn_asked = False
                    self.qtn_being_asked = False
                    self.num_qtns = 0
                    self.ans_answered = True
                else:
                    self.show_error_message("Invalid question file")
            else:
                print("No file chosen")
        else:
            self.show_error_message("No questions can be loaded outside exam mode")

    # Reads the questions file and returns the next question
    def get_next_qtn(self):
        try:
            if self.view_exam_mode:
                qtn_text = self.exam_qtn_markers_lbl[self.num_qtns - 1][1:-1]
            else:
                qtn_text = self.qtns_list[2 + self.num_qtns]
            if qtn_text != "":
                return qtn_text
            else:
                self.accept_questions = False
                self.qtn_asked = True
                return "---End of the questions---"
        except:
            return "No Question File"

    # ################# Question & answer markers ######################

    # Adds question marker at required position
    def add_qtn_marker(self, start, stop, label):
        self.brt_qtn_reg.append(pg.LinearRegionItem(values=[start, stop], movable=False))

        self.gsr_qtn_reg.append(pg.LinearRegionItem(values=[start, stop], movable=False))
        pg.InfLineLabel(self.gsr_qtn_reg[self.num_qtns].lines[1], label, position=0.5, rotateAxis=(1, 0))

        self.hrt_qtn_reg.append(pg.LinearRegionItem(values=[start, stop], movable=False))

        self.brt_plot.addItem(self.brt_qtn_reg[self.num_qtns])
        self.gsr_plot.addItem(self.gsr_qtn_reg[self.num_qtns])
        self.hrt_plot.addItem(self.hrt_qtn_reg[self.num_qtns])

        self.num_qtns += 1

    # Ads answer marker at required position
    def add_ans_marker(self, position, lbl):
        if self.qtn_asked or lbl == "EXAM END" or self.view_exam_mode:

            if self.record_exam_data:
                self.record_ans_data(position, lbl)

            self.brt_ans_lin.append(pg.InfiniteLine(pos=position, movable=False, angle=90,
                                       labelOpts={'position': 0.5, 'color': (200, 200, 100),
                                                  'fill': (200, 200, 200, 50), 'movable': False}))
            self.gsr_ans_lin.append(pg.InfiniteLine(pos=position, movable=False, angle=90, label=lbl,
                                       labelOpts={'position': 0.5, 'color': (200, 200, 100),
                                                  'fill': (200, 200, 200, 50), 'movable': False}))
            self.hrt_ans_lin.append(pg.InfiniteLine(pos=position, movable=False, angle=90,
                                       labelOpts={'position': 0.5, 'color': (200, 200, 100),
                                                  'fill': (200, 200, 200, 50), 'movable': False}))

            if lbl != "EXAM END" or not self.qtn_asked:
                self.question_lbl.setText(self.get_next_qtn())

            self.brt_plot.addItem(self.brt_ans_lin[-1])
            self.gsr_plot.addItem(self.gsr_ans_lin[-1])
            self.hrt_plot.addItem(self.hrt_ans_lin[-1])

            self.qtn_asked = False
            self.ans_answered = True

    # Removes questions and answer markers when they reach the end of the graph
    def rem_qtn_ans_markers(self):
        for i in range(len(self.gsr_qtn_reg)):
            if (self.gsr_qtn_reg[i].getRegion()[0] < (self.time_pos - self.graphs_length)) or \
                    (self.gsr_qtn_reg[i].getRegion()[1] > self.time_pos):
                self.brt_plot.removeItem(self.brt_qtn_reg[i])
                self.gsr_plot.removeItem(self.gsr_qtn_reg[i])
                self.hrt_plot.removeItem(self.hrt_qtn_reg[i])

        for j in range(len(self.gsr_ans_lin)):
            if (self.gsr_ans_lin[j].getXPos() < (self.time_pos - self.graphs_length)) or \
                    (self.gsr_ans_lin[j].getXPos() > self.time_pos):
                self.brt_plot.removeItem(self.brt_ans_lin[j])
                self.gsr_plot.removeItem(self.gsr_ans_lin[j])
                self.hrt_plot.removeItem(self.hrt_ans_lin[j])

    # Handles question marker timing and region
    def update_qtn_marker(self):
        if self.graph_running and self.accept_questions:
            if self.qtn_being_asked:
                qtn_lbl = self.get_next_qtn()
                if self.record_exam_data:
                    self.record_qtns_data(self.start_qtn_pos, self.time_pos, qtn_lbl)
                if len(qtn_lbl) > 38:
                    qtn_lbl = qtn_lbl[:35] + "..."

                self.add_qtn_marker(self.start_qtn_pos, self.time_pos, qtn_lbl)
                self.qtn_being_asked = False
                self.qtn_asked = True

            elif self.ans_answered:
                self.start_qtn_pos = self.time_pos
                self.qtn_being_asked = True
                self.ans_answered = False

    # ################# Arduino and serial port ##########################

    # Connect with arduino
    def ser_connect(self):
        global arduino
        sender = self.sender()
        if sender.text() == "Connect":
            try:
                arduino = serial.Serial(self.port_name_le.text(), '115200')
                self.ser_connect_btn.setText("Disconnect")
            except:
                self.show_error_message("Port not found")
        else:
            try:
                arduino.write(b'000')
                arduino.close()
            except:
                self.show_error_message("Polygraph was not connected")
            self.ser_connect_btn.setText("Connect")

    # Start or stop arduino transmission
    def start_stop(self, start):
        if self.ser_connect_btn.text() == "Disconnect":
            global arduino
            if start:
                try:
                    arduino.write(b'111')
                    self.graph_running = True
                except:
                    self.show_error_message("Polygraph not connected")
                    arduino.close()
                    self.ser_connect_btn.setText("Connect")
            else:
                try:
                    arduino.write(b'000')
                except:
                    self.show_error_message("Polygraph not connected")
                    arduino.close()
                    self.ser_connect_btn.setText("Connect")
                self.graph_running = False

    # Loop that reads serial port from arduino
    def arduino_read(self):

        if self.ser_connect_btn.text() == "Disconnect" and arduino.in_waiting > 18:
            reading = self.to_list(str(arduino.read(arduino.in_waiting)))
            self.plot_data(reading, True)
            self.time_pos += 1

            if self.record_exam_data:
                self.record_plot_data(reading)

    # Convert the string sent by the arduino to a python list.
    def to_list(self, string):
        try:
            str_list = string[string.index('(') + 1:string.index(')')].split(",")
            return [int(x) for x in str_list]
        except ValueError:
            print("ERROR-to_list")

    # ################## Graphing and scales ################################

    # Plot data and update data lists
    def plot_data(self, data_plot, forward):
        try:
            if forward:
                self.brt_data[:- 1] = self.brt_data[1:]
                self.brt_data[-1] = data_plot[0]

                self.gsr_data[:- 1] = self.gsr_data[1:]
                self.gsr_data[-1] = data_plot[1]

                self.hrt_data[:-1] = self.hrt_data[1:]
                self.hrt_data[-1] = data_plot[2]

            else:
                self.brt_data[1:] = self.brt_data[:-1]
                self.gsr_data[1:] = self.gsr_data[:-1]
                self.hrt_data[1:] = self.hrt_data[:-1]

                if self.time_pos > self.graphs_length:
                    self.brt_data[0] = data_plot[0]
                    self.gsr_data[0] = data_plot[1]
                    self.hrt_data[0] = data_plot[2]

            self.brt_plot2.setData(self.brt_data)
            self.brt_plot2.setPos(int(self.time_pos - self.graphs_length), 0)

            self.gsr_plot2.setData(self.gsr_data)
            self.gsr_plot2.setPos(int(self.time_pos - self.graphs_length), 0)

            self.hrt_plot2.setData(self.hrt_data)
            self.hrt_plot2.setPos(int(self.time_pos - self.graphs_length), 0)


            # Calculate and display rates & values on displays

            # Breath rate:
            brt_max = max(self.brt_data[-50:])
            brt_min = min(self.brt_data[-50:])
            brt_amp = brt_max - brt_min
            brt_up_th = brt_min + 0.55 * brt_amp
            brt_low_th = brt_min + 0.45 * brt_amp

            if data_plot[0] > brt_up_th and self.brt_was_below_th:
                self.brt_prev_above = self.brt_last_above
                self.brt_last_above = self.time_pos
                self.brt_was_below_th = False

            elif data_plot[0] < brt_low_th:
                self.brt_was_below_th = True

            if (self.brt_last_above - self.brt_prev_above) != 0:
                brt_rate = abs(600 / (self.brt_last_above - self.brt_prev_above))
            else:
                brt_rate = 0

            self.brt_lcd.display(int(brt_rate))

            self.gsr_lcd.display(data_plot[1])

            # Heart rate:
            hrt_max = max(self.hrt_data[-30:])
            hrt_min = min(self.hrt_data[-30:])
            hrt_amp = hrt_max - hrt_min
            hrt_up_th = hrt_min + 0.55*hrt_amp
            hrt_low_th = hrt_min + 0.45*hrt_amp

            if data_plot[2] > hrt_up_th and self.hrt_was_below_th:
                self.hrt_prev_above = self.hrt_last_above
                self.hrt_last_above = self.time_pos
                self.hrt_was_below_th = False
                
                # Play sound if beep enabled and sufficient amplitude for a valid reading.
                if self.hrt_sound and 30 < hrt_amp < 600:
                    winsound.PlaySound('heart_beep.wav', winsound.SND_ASYNC)

            elif data_plot[2] < hrt_low_th:
                self.hrt_was_below_th = True
             
            # Calculate heart rate
            if 30 < hrt_amp < 600:
                if (self.hrt_last_above - self.hrt_prev_above) != 0:
                    curr_rate = abs(600/(self.hrt_last_above - self.hrt_prev_above))
					
                    self.hrt_prev_rates[:-1] = self.hrt_prev_rates[1:]
                    self.hrt_prev_rates[-1] = curr_rate
					
                    # Just adding some averaging in 
                    hrt_rate = int(sum(self.hrt_prev_rates)/len(self.hrt_prev_rates))
                else:
                    hrt_rate = 0
            else:
                hrt_rate = 0

            self.hrt_lcd.display(hrt_rate)

        except:
            print("ERROR-plot_data")

    # Pulse-Marking beep on/off
    def hrt_beep(self):
        if self.hrt_beep_btn.text() == "Beep ON":
            self.hrt_sound = True
            self.hrt_beep_btn.setText("Beep OFF")
        else:
            self.hrt_sound = False
            self.hrt_beep_btn.setText("Beep ON")

    # Reset graph scales
    def brt_reset_scale(self):
        self.brt_plot.setRange(yRange=[0, 1023])

    def gsr_reset_scale(self):
        self.gsr_plot.setRange(yRange=[0, 1023])

    def hrt_reset_scale(self):
        self.hrt_plot.setRange(yRange=[0, 1023])

    # Updates time shown on the "lcd" display
    def update_time_display(self):
        minutes = int(self.time_pos / 600)
        seconds = int((self.time_pos % 600.0) / 10)

        self.min_lcd.display(minutes)
        self.sec_lcd.display(seconds)

    # ############### Update timers & key presses ################

    # Handles key presses
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Q:  # Adds question marker (start, end)
            self.update_qtn_marker()
        elif key == Qt.Key_Y:  # Adds "YES" answer marker.
            self.add_ans_marker(self.time_pos, "YES")
        elif key == Qt.Key_N:  # Adds "NO" answer marker.
            self.add_ans_marker(self.time_pos, "NO")
        elif key == Qt.Key_E:  # Ends exam and saves file.
            self.end_exam()
        elif key == Qt.Key_Left:  # On exam view mode, backs up graphs.
            self.exam_view_reverse_graphs()
        elif key == Qt.Key_Right:  # On exam view mode, advances graphs.
            self.exam_view_advance_graphs()

    # Updates all needed functions 20 times per second
    def update(self):
        if self.acquisition_mode:
            try:
                self.arduino_read()
                self.update_time_display()
                self.rem_qtn_ans_markers()
            finally:
                timer.singleShot(50, self.update)
        if self.view_exam_mode:
            self.exam_view_add_qtn_ans_markers()
            self.update_time_display()
            self.rem_qtn_ans_markers()

    # Displays an additional window with instructions and information.
    def show_help(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setWindowTitle("Help")
        msg.setText("Quick start guide:")
        msg.setInformativeText("1) Connect with polygraph:"
                               "\n -Enter port name."
                               "\n -Press Connect."
                               "\n -Use Start and Stop to start and stop the transmission."
                               "\n\n2) Record an exam:"
                               "\n -Create a .txt question file: 2 lines for notes and each question in a new line. "
                               "\n -Press the New exam button and chose a file name, press Save."
                               "\n -Click Load question set and choose the question file."
                               "\n -Connect and press Start."
                               "\n -Press Q key, read question and press again. Press Y and N for answer markers."
                               "\n -Questions will automatically update."
                               "\n -Press E key or click Close/Save to end the exam."
                               "\n\n3) Open exam:"
                               "\n -Click Open exam and choose file."
                               "\n -Use arrow keys or < > buttons to move through the file."
                               "\n -Press Close exam to exit."
                               "\n\n4) Miscellaneous:"
                               "\n -To zoom in the graph, use ctrl and mouse."
                               "\n -To return to auto-scaling, click the A button on the bottom left of each graph."
                               "\n -For fixed scale, click Reset scale."
                               "\n -To enable or disable the pulse Beep, click Beep ON or Beep OFF.")

        msg.setDetailedText("USB Polygraph Software V.1.13 by Juan Gg on June 2018 \n" +
                            "\nThis work is licensed under GNU General Public License v3.0" +
                            "\n\nhttps://juangg-projects.blogspot.com/")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    # Shows the user a pop-up window with the error message.
    def show_error_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


# Create an instance of the class and start the program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    timer = QtCore.QTimer()
    pLogic = PolygraphLogic()
    pLogic.update()
    sys.exit(app.exec_())
