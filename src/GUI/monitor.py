from PyQt5 import QtWidgets,QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import pyqtgraph as pg
import ui_monitor
import numpy as np
import sys
import cv2

class monitor_window(QtWidgets.QDialog, ui_monitor.Ui_window):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        ui_monitor.Ui_window.__init__(self)
        self.setupUi(self)
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win1 = pg.GraphicsLayoutWidget(show=True)
        self.win2 = pg.GraphicsLayoutWidget(show=True)
        self.verticalLayout.addWidget(self.win)  # 添加绘图部件到线图部件的网格布局层
        self.verticalLayout_6.addWidget(self.win1) 
        self.verticalLayout_2.addWidget(self.win2) 




        # self.thread=reading_thread

        
        self.ptr = 0                                        #指针，表示最近一次读入的是第prt5个数据
        self.startTime = pg.ptime.time()
        self.chunkSize = 100
        # Remove chunks after we have 10
        self.maxChunks = 10  

            
        self.win.setWindowTitle('distances plots')                              
        self.p = self.win.addPlot()                     #p是一张图
        self.p.setLabel('bottom', 'Time', 's')
        self.p.setXRange(-10, 0)                            #由于xrange，屏幕上只能打出6个trunk左右，所以我们看不到一整段被remove，所以整个就是连续的。
        self.dist_curves1 = []
        self.dist_curves2=[]
        self.dist_curves3=[]
        self.dist_data1 = np.empty((self.chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data
        self.dist_data2 = np.empty((self.chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data
        self.dist_data3 = np.empty((self.chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data

        self.win1.setWindowTitle('sum Plots')                          
        self.p1 = self.win1.addPlot()                     #p是一张图
        self.p1.setLabel('bottom', 'Time', 's')
        self.p1.setXRange(-10, 0)                            #由于xrange，屏幕上只能打出6个trunk左右，所以我们看不到一整段被remove，所以整个就是连续的。
        self.sum_curves1=[]
        self.sum_curves2=[]
        self.sum_curves3=[]
        self.sum_data1 = np.empty((self.chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data
        self.sum_data2 = np.empty((self.chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data
        self.sum_data3 = np.empty((self.chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data

        self.win2.setWindowTitle('total sum and threshold')                          
        self.p2 = self.win2.addPlot()                     #p是一张图
        self.p2.setLabel('bottom', 'Time', 's')
        self.p2.setXRange(-10, 0)                            #由于xrange，屏幕上只能打出6个trunk左右，所以我们看不到一整段被remove，所以整个就是连续的。
        self.Tsum_curves1=[]
        self.thre_curves2=[]
        self.Tsum_data1 = np.empty((self.chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data
        self.thre_data2 = np.empty((self.chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data


        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update1)
        self.timer.start(0)

        self.timer1 = pg.QtCore.QTimer()
        self.timer1.timeout.connect(self.update2)
        self.timer1.start(0)

        self.timer2 = pg.QtCore.QTimer()
        self.timer2.timeout.connect(self.update3)
        self.timer2.start(0)

        self.timer3 = pg.QtCore.QTimer()
        self.timer3.timeout.connect(self.update4)
        self.timer3.start(0)


    #slot function for receiving data from reading thread
    def receivedata(self, thread_data):
        self.data=thread_data
        print(self.data)

    def update1(self):
        now = pg.ptime.time()
        for c in self.dist_curves1:
            c.setPos(-(now-self.startTime), 0)           
        for c in self.dist_curves2:
            c.setPos(-(now-self.startTime), 0)           
        for c in self.dist_curves3:
            c.setPos(-(now-self.startTime), 0)           #使得之前的不断往负半轴移动，而我们始终看（-10，0），所以这个是看上去在scroll的关键！！！！  
        
        i = self.ptr % self.chunkSize                        #表示最近一次读入分配到最近一个chunk的第i个位置
        if i == 0:   
            dist_curve1 = self.p.plot(pen='g')                               #新的chunck放到新的plot上，这句每执行一次相当于往长布上放一小段新的plot（return的是PlotDataItem），
                                                            #这样每个循环就只用update（setdat）这一个新plot，而不用update一整个plot。而之前的不动（只有在有新的plot时去掉最早那一个）。
            dist_curve2 =self.p.plot(pen='r')
            dist_curve3=self.p.plot(pen='b')
                                
            self.dist_curves1.append(dist_curve1)  
            self.dist_curves2.append(dist_curve2)    
            self.dist_curves3.append(dist_curve3)                     
            last1 = self.dist_data1[-1]
            last2 = self.dist_data2[-1]
            last3 = self.dist_data3[-1]
            self.dist_data1 = np.empty((self.chunkSize+1,2))        
            self.dist_data2 = np.empty((self.chunkSize+1,2))      
            self.dist_data3 = np.empty((self.chunkSize+1,2))   
            self.dist_data1[0] = last1                       #2.清空chunk，把之前的最后一个放到第一个
            self.dist_data2[0] = last2
            self.dist_data3[0] = last3

            while len(self.dist_curves1) > self.maxChunks:
                c = self.dist_curves1.pop(0)
                self.p.removeItem(c)                   
                c = self.dist_curves2.pop(0)
                self.p.removeItem(c)       
                c = self.dist_curves3.pop(0)
                self.p.removeItem(c)                    #把一整段chunk一次性从plot中移除
                
        else:
            dist_curve1 = self.dist_curves1[-1]
            dist_curve2 = self.dist_curves2[-1]
            dist_curve3 = self.dist_curves3[-1]

        

        self.dist_data1[i+1,0] = now - self.startTime                    #定义时间轴
        self.dist_data1[i+1,1] = self.data[0]     #读取最近一次数据
        self.dist_data2[i+1,0] = now - self.startTime                    #定义时间轴
        self.dist_data2[i+1,1] = self.data[1]        #读取最近一次数据
        self.dist_data3[i+1,0] = now - self.startTime                    #定义时间轴
        self.dist_data3[i+1,1] = self.data[2]        #读取最近一次数据
    
        dist_curve1.setData(x=self.dist_data1[:i+2, 0], y=self.dist_data1[:i+2, 1]) #pyqtgraph的绘图数据主要是通过setData()这个方法来转化为图形。
                                                        #后面设置了一个定时器，每隔一个时间重新调用setData()方法对图形数据curve（plot）进行设，就能够实现实时的数据可视化呈现。
                                                        #set的是最后一个chunk的0到第i个（也就是最近）的数据
        dist_curve2.setData(x=self.dist_data2[:i+2, 0], y=self.dist_data2[:i+2, 1])
        dist_curve3.setData(x=self.dist_data3[:i+2, 0], y=self.dist_data3[:i+2, 1])

        self.ptr += 1      


    def update2(self):
        now = pg.ptime.time()
        for c in self.sum_curves1:
            c.setPos(-(now-self.startTime), 0)           
        for c in self.sum_curves2:
            c.setPos(-(now-self.startTime), 0)           
        for c in self.sum_curves3:
            c.setPos(-(now-self.startTime), 0)           #使得之前的不断往负半轴移动，而我们始终看（-10，0），所以这个是看上去在scroll的关键！
        
        i = self.ptr % self.chunkSize                        #表示最近一次读入分配到最近一个chunk的第i个位置
        if i == 0:   
            sum_curve1 = self.p1.plot(pen='g')                               #新的chunck放到新的plot上，这句每执行一次相当于往长布上放一小段新的plot（return的是PlotDataItem），
                                                            #这样每个循环就只用update（setdat）这一个新plot，而不用update一整个plot。而之前的不动（只有在有新的plot时去掉最早那一个）。
            sum_curve2 = self.p1.plot(pen='r')
            sum_curve3 = self.p1.plot(pen='b')
                                
            self.sum_curves1.append(sum_curve1)  
            self.sum_curves2.append(sum_curve2)    
            self.sum_curves3.append(sum_curve3)                     
            last1 = self.sum_data1[-1]
            last2 = self.sum_data2[-1]
            last3 = self.sum_data3[-1]
            self.sum_data1 = np.empty((self.chunkSize+1,2))        
            self.sum_data2 = np.empty((self.chunkSize+1,2))      
            self.sum_data3 = np.empty((self.chunkSize+1,2))   
            self.sum_data1[0] = last1                       #2.清空chunk，把之前的最后一个放到第一个
            self.sum_data2[0] = last2
            self.sum_data3[0] = last3

            while len(self.sum_curves1) > self.maxChunks:
                c = self.sum_curves1.pop(0)
                self.p1.removeItem(c)                   
                c = self.sum_curves2.pop(0)
                self.p1.removeItem(c)       
                c = self.sum_curves3.pop(0)
                self.p1.removeItem(c)                    #把一整段chunk一次性从plot中移除
                
        else:
            sum_curve1 = self.sum_curves1[-1]
            sum_curve2 = self.sum_curves2[-1]
            sum_curve3 = self.sum_curves3[-1]

        

        self.sum_data1[i+1,0] = now - self.startTime                    #定义时间轴
        self.sum_data1[i+1,1] = self.data[7]     #读取最近一次数据
        self.sum_data2[i+1,0] = now - self.startTime                    #定义时间轴
        self.sum_data2[i+1,1] = self.data[8]        #读取最近一次数据
        self.sum_data3[i+1,0] = now - self.startTime                    #定义时间轴
        self.sum_data3[i+1,1] = self.data[9]        #读取最近一次数据
    
        sum_curve1.setData(x=self.sum_data1[:i+2, 0], y=self.sum_data1[:i+2, 1]) #pyqtgraph的绘图数据主要是通过setData()这个方法来转化为图形。
                                                        #后面设置了一个定时器，每隔一个时间重新调用setData()方法对图形数据curve（plot）进行设，就能够实现实时的数据可视化呈现。
                                                        #set的是最后一个chunk的0到第i个（也就是最近）的数据
        sum_curve2.setData(x=self.sum_data2[:i+2, 0], y=self.sum_data2[:i+2, 1])
        sum_curve3.setData(x=self.sum_data3[:i+2, 0], y=self.sum_data3[:i+2, 1])


    def update3(self):
        now = pg.ptime.time()
        for c in self.Tsum_curves1:
            c.setPos(-(now-self.startTime), 0)           
        for c in self.thre_curves2:
            c.setPos(-(now-self.startTime), 0)           
        
        i = self.ptr % self.chunkSize                        #表示最近一次读入分配到最近一个chunk的第i个位置
        if i == 0:   
            Tsum_curve1 = self.p2.plot(pen='y')                               #新的chunck放到新的plot上，这句每执行一次相当于往长布上放一小段新的plot（return的是PlotDataItem），
                                                            #这样每个循环就只用update（setdat）这一个新plot，而不用update一整个plot。而之前的不动（只有在有新的plot时去掉最早那一个）。
            thre_curve2 = self.p2.plot(pen='r')
                                
            self.Tsum_curves1.append(Tsum_curve1)  
            self.thre_curves2.append(thre_curve2)    
            last1 = self.Tsum_data1[-1]
            last2 = self.thre_data2[-1]
            self.Tsum_data1 = np.empty((self.chunkSize+1,2))        
            self.thre_data2 = np.empty((self.chunkSize+1,2))      
            self.Tsum_data1[0] = last1                       #2.清空chunk，把之前的最后一个放到第一个
            self.thre_data2[0] = last2

            while len(self.Tsum_curves1) > self.maxChunks:
                c = self.Tsum_curves1.pop(0)
                self.p2.removeItem(c)                   
                c = self.thre_curves2.pop(0)
                self.p2.removeItem(c)       
                
        else:
            Tsum_curve1 = self.Tsum_curves1[-1]
            thre_curve2 = self.thre_curves2[-1]

        

        self.Tsum_data1[i+1,0] = now - self.startTime                    #定义时间轴
        self.Tsum_data1[i+1,1] = self.data[10]     #读取最近一次数据
        self.thre_data2[i+1,0] = now - self.startTime                    #定义时间轴
        self.thre_data2[i+1,1] = self.data[11]        #读取最近一次数据

    
        Tsum_curve1.setData(x=self.Tsum_data1[:i+2, 0], y=self.Tsum_data1[:i+2, 1]) #pyqtgraph的绘图数据主要是通过setData()这个方法来转化为图形。
                                                        #后面设置了一个定时器，每隔一个时间重新调用setData()方法对图形数据curve（plot）进行设，就能够实现实时的数据可视化呈现。
                                                        #set的是最后一个chunk的0到第i个（也就是最近）的数据
        thre_curve2.setData(x=self.thre_data2[:i+2, 0], y=self.thre_data2[:i+2, 1])


    def update4(self):
        if self.data[4]==1:
            self.label_3.setPixmap(QPixmap("on.png"))
        else: 
            self.label_3.setPixmap(QPixmap("off.png"))
        if self.data[5]==1:
            self.label_7.setPixmap(QPixmap("on.png"))
        else:
            self.label_7.setPixmap(QPixmap("off.png"))
        if self.data[6]==1:
            self.label_8.setPixmap(QPixmap("on.png"))
        else:
            self.label_8.setPixmap(QPixmap("off.png"))

        
        self.lcdNumber.display(self.data[3])

        

        


# 运行函数
thread_data=[10,10,10]
def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = monitor_window(thread_data)
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


    