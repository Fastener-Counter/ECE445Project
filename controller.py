#QAbstractButton -QPushButton的使用
from PyQt5.QtWidgets import  QPushButton,QVBoxLayout,QWidget,QApplication
from PyQt5.QtGui import QIcon,QPixmap

import sys
import socket
import time

def send(text):
    text = text + '!'
    print(text)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect(("192.168.4.1", 333))
    tcp.send(text.encode())
    time.sleep(50/1000)
    tcp.close()

class WindowClass(QWidget):
    def __init__(self,parent=None):
        super(WindowClass, self).__init__(parent)
        self.btn_1=QPushButton("start")
        self.btn_2=QPushButton("stop")
        self.btn_3=QPushButton("clear")#快捷建设置，ALT+大写首字母
        # self.btn_4 = QPushButton("Btn_4")

        self.btn_1.setFixedHeight(100)
        self.btn_2.setFixedHeight(100)
        self.btn_3.setFixedHeight(100)

        # self.btn_1.setCheckable(True)#设置已经被点击
        # self.btn_1.toggle()#切换按钮状态
        # self.btn_1.clicked.connect(self.btnState)
        self.btn_1.clicked.connect(lambda :self.wichBtn(self.btn_1))

        #self.btn_2.setIcon(QIcon('./image/add_16px_1084515_easyicon.net.ico'))#按钮按钮
        # self.btn_2.setIcon(QIcon(QPixmap('./image/baidu.png')))
        # self.btn_2.setEnabled(False)#设置不可用状态
        self.btn_2.clicked.connect(lambda :self.wichBtn(self.btn_2))

        # self.btn_3.setDefault(True)#设置该按钮式默认状态的
        self.btn_3.clicked.connect(lambda :self.wichBtn(self.btn_3))

        # self.btn_4.clicked.connect(lambda :self.wichBtn(self.btn_4))

        self.resize(600,400)
        layout=QVBoxLayout()
        layout.addWidget(self.btn_1)
        layout.addWidget(self.btn_2)
        layout.addWidget(self.btn_3)
        # layout.addWidget(self.btn_4)

        self.setLayout(layout)

    # def btnState(self):
    #     if self.btn_1.isChecked():
    #         print("Btn_1被单击")
    #     else:
    #         print("Btn_1未被单击")
    def wichBtn(self,btn):
        send(btn.text())

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=WindowClass()
    win.show()
    sys.exit(app.exec_())