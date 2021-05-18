from time import sleep
import serial
from . import Qmessage

def connectTo(conn_type='USB'):
    if conn_type=='USB':
        connection=USBconnection()
        return connection
    if conn_type=='wireless':
        connection=Wificonnection()
        return connection


class USBconnection():
    def __init__(self): 
        self.port='/dev/cu.usbmodem141201'
        self.data=[0,0,0,0,0,0,0,0,0,0]

    def connect(self):
        self.port_status = True
        try:
            self.ser = serial.Serial(self.port,9600) # Establish the connection on a specific port  timeout = 2?
        except OSError:
            self.port_status = False
        print('port_status:',self.port_status)
        return self.port_status

    def disconnect(self):
        pass

    def get_data(self):
        # try:
        data_read=self.ser.readline().decode('utf-8') # Read the newest output from the Arduino
        # print(data_read)
        data=[float(i)for i in data_read.split(',')]
        # except:
            # print('read fail or float error')
        return data

    def write(self,commend):
        if self.port_status==False:
            Qmessage.error_message()
        else:
            # try:
            if commend=='start':
                self.ser.write(b"1")
                print('start')
            if commend=='stop':
                self.ser.write(b"2")
            if commend=='clear':
                self.ser.write(b"3")#转换为ASCII码方便发送
            # except:
    #     print('read fail or float error')





class Wificonnection():
    def __init__(self): 
        self.port='/dev/tty.usbmodem143201'
        self.data=[0,0,0,0,0,0,0,0,0,0]
