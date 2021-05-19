import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QMdiSubWindow, QApplication
from PyQt5.QtCore import QTime, pyqtSignal, QStringListModel, QDate

from PyQt5.QtWidgets import QMessageBox

import ui_controller 
import monitor

import time
import functions.connection, functions.multithread



class mainWindow(QtWidgets.QMainWindow, ui_controller.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)  # 创建主界面对象
        ui_controller.Ui_MainWindow.__init__(self)#主界面对象初始化
        self.setupUi(self)

#        self.stop_progress=True                 #线程状态，初始化为停止
        #实例化一个进程
        # self.stop_progress=True
        self.conn_choice=self.comboBox_2.currentText()                       #连接选项
        self.run_thread=functions.multithread.RunThreand(parent=None, conn_type=self.conn_choice)


    

        #信号
        self.pushButton.clicked.connect(self.clear)         #clear
        self.pushButton_2.clicked.connect(self.start)       #start
        self.pushButton_3.clicked.connect(self.stop)        #stop
        self.pushButton_5.clicked.connect(self.monitor)        #monitor


    #start,stop,clear
    def start(self, start_value=0):
        # self.stop_progress=False
        self.progress_value=int(self.lineEdit_2.text())
        self.run_thread.resume() #start
        # self.connection.write('start')
        # self.run_thread.start()
        self.run_thread.counter_value.connect(self.set_number)


    def stop(self):
        # self.stop_progress=True
        
        self.run_thread.stop()

    def clear(self):
        # self.stop_progress=True
        self.run_thread.clear()

    # def end(self):
    #     self.run_thread.endjob()

    #display count:把number放到line_edit里
    def set_number(self,counter):
        # if not self.stop_progress:
            self.lineEdit_2.setText(str(counter))

    #monitor window
    def monitor(self):
        self.MonitorWindow=monitor.monitor_window()
        self.MonitorWindow.show()
        self.run_thread.all_data.connect(self.MonitorWindow.receivedata)
        # self.run_thread.all_data.connect(self.send)


    
    def send(self,data_from_thread):
        self.data=data_from_thread
        print(self.data)


            


    




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) #创建一个application
    window = mainWindow()#创建QT对象
    window.show()#QT对象显示
    sys.exit(app.exec_())

