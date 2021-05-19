from PyQt5 import QtCore
import time

from PyQt5.QtWidgets import QMessageBox
from . import connection, Qmessage

class  RunThreand(QtCore.QThread):
    counter_value=QtCore.pyqtSignal(int)   #定义一个向主窗口传输当前计数值的signal, 如果要定义自己的信号,则必须将它们定义为类变量（不需要通过实例变量，直接类变量访问）
    all_data=QtCore.pyqtSignal(list)   #定义一个向主窗口传输当前计数值的signal, 如果要定义自己的信号,则必须将它们定义为类变量（不需要通过实例变量，直接类变量访问）
    def __init__(self, parent = None, conn_type='USB',port='usbmodem143201'):
        super(RunThreand, self).__init__(parent) #设置默认属性

        self.count=0
        self.run=True
        self.conn_type=conn_type
        self.port=port
        self.port_state=False
        self.monitoring=False


    def estb_connection(self):
        self.connection=connection.connectTo(self.conn_type,self.port)
        self.port_state=self.connection.connect()
        if self.port_state==True:
            print('connected')


    def run(self):

        # while self.is_running==True:
        #     self.connection.write('start')

        while self.run:                 
            self.data=self.connection.get_data()
            # print(self.data)
            counter=self.data[3]
            
            self.counter_value.emit(counter) #发送一个新增信号(有self)
            self.all_data.emit(self.data)

            while not self.run:
                    time.sleep(0)               #this is very important 
        #         # print('stoping')
                
        # # print('printing')
        #     if self.monitoring==True:
        #         self.monitor_window.update(data)
    

    def resume(self):
        if self.port_state==False:#重连
            self.estb_connection()
        self.connection.write('start')
        self.run = True
        self.start()
    
    def clear(self):
        #向arduino发送clear信号
        self.connection.write('clear')
        self.connection.write('start')

    def stop(self):
        #向arduino发送停止信号,stop arduino:
        self.connection.write('stop')
        #pause
        self.run = False
    

    
    def endjob(self): 
        self.terminate()
    
    # def plot(self,monitor_window):
    #     self.monitor_window=monitor_window
    #     #print(self.monitor_window is monitor_window) 返回true，shallow copy
    #     self.monitor_window.show()
    #     if self.connection.port_status:
    #         self.monitoring=True

    #     else:
    #         Qmessage.error_message()


