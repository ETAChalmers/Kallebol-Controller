# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPalette, QColor

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_test import Ui_MainWindow
from kallebol import Kallebol

import time

LCD_UPDATE_PERIOD = 100


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.kallebol = Kallebol()
        
        self.arm_state = False

        self.ui.conn_button.clicked.connect(self.setup_kallebol)
        self.ui.move_button.clicked.connect(self.read_values)
        self.ui.fast_button.clicked.connect(self.kallebol.servo.set_move_parameters)
        
        self.ui.arm_button.setCheckable(True)
        self.ui.arm_button.clicked.connect(self.arm)
        
        self.ui.conn_button.setCheckable(True)
        
        self.update_current_lcd = QTimer()
        self.update_current_lcd.setInterval(LCD_UPDATE_PERIOD)
        self.update_current_lcd.timeout.connect(self.update_current)
        
        self.ui.azi_input.setRange(-900000, 900000)
        self.ui.elev_input.setRange(10, 80)
        
        self.ui.trgt_elev_lcd.setSmallDecimalPoint(True)
        self.ui.trgt_azi_lcd.setSmallDecimalPoint(True)
        self.ui.curr_elev_lcd.setSmallDecimalPoint(True)
        self.ui.curr_azi_lcd.setSmallDecimalPoint(True)
        
        self.ui.trgt_elev_lcd.setDigitCount(6)
        self.ui.trgt_azi_lcd.setDigitCount(6)
        self.ui.curr_elev_lcd.setDigitCount(6)
        self.ui.curr_azi_lcd.setDigitCount(6)
        
        
    def setup_kallebol(self):
        try:
            self.kallebol.begin()
            self.ui.conn_button.setChecked(True)
            self.ui.conn_status_label.setText("Connected")
            self.update_current_lcd.start()
            
        except Exception as e:
            self.ui.conn_button.setChecked(False)
            self.ui.conn_status_label.setText("Failed to connect")
        
    
    def read_values(self):
        azi = self.ui.azi_input.value()
        elev = self.ui.elev_input.value()
        
        self.ui.trgt_azi_lcd.display('{:.02f}'.format(azi))
        self.ui.trgt_elev_lcd.display('{:.02f}'.format(elev))
        
        self.kallebol.move_servo(azi)
        
    def arm(self):
        if self.ui.arm_button.isChecked():
            self.ui.arm_button.setText("Disarm")
            self.kallebol.servo.energize()
        
        else:
            self.ui.arm_button.setText("Arm")
            self.kallebol.servo.denergize()
        
        
    def update_current(self):
        print("Read time")
        azi = 0
        try:
            azi = float(self.kallebol.servo.read_current_position())/840
        except Exception as e:
            print(e)
        elev = 0.0
        self.ui.curr_azi_lcd.display('{:.02f}'.format(azi))
        self.ui.curr_elev_lcd.display('{:.02f}'.format(elev))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
