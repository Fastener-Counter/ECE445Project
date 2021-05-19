#用原来线程
#用原来线程+pyqtremote.
#用主线程+pyqtremote

from PyQt5 import QtWidgets,QtCore
import pyqtgraph as pg
import ui_monitor
import numpy as np
import sys

class monitor_window(QtWidgets.QDialog, ui_monitor.Ui_window):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        ui_monitor.Ui_window.__init__(self)
        self.setupUi(self)
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win2 = pg.GraphicsLayoutWidget(show=True)
        self.verticalLayout.addWidget(self.win)  # 添加绘图部件到线图部件的网格布局层
        self.verticalLayout_2.addWidget(self.win2) 
        # self.thread=reading_thread

            
        self.win.setWindowTitle('pyqtgraph example: Scrolling Plots')
        self.chunkSize = 100
        # Remove chunks after we have 10
        self.maxChunks = 10                                
        self.startTime = pg.ptime.time()
        self.p5 = self.win.addPlot(colspan=2)                     #p5是一张图
        self.p5.setLabel('bottom', 'Time', 's')
        self.p5.setXRange(-10, 0)                            #由于xrange，屏幕上只能打出6个trunk左右，所以我们看不到一整段被remove，所以整个就是连续的。
        self.curves = []
        self.curves1=[]
        self.data5 = np.empty((self.chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data
        self.data6 = np.empty((self.chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data
        self.ptr5 = 0                                        #指针，表示最近一次读入的是第prt5个数据

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(0)
    
    def receivedata(self, thread_data):
        self.data=thread_data
        #print(self.data)

    def update(self):
        now = pg.ptime.time()
        for c in self.curves:
            c.setPos(-(now-self.startTime), 0)           #使得之前的不断往负半轴移动，而我们始终看（-10，0），所以这个是看上去在scroll的关键！！！！
        for c in self.curves1:
            c.setPos(-(now-self.startTime), 0)           #使得之前的不断往负半轴移动，而我们始终看（-10，0），所以这个是看上去在scroll的关键！！！！
        
        i = self.ptr5 % self.chunkSize                        #表示最近一次读入分配到最近一个chunk的第i个位置
        if i == 0:   
            curve = self.p5.plot()                               #新的chunck放到新的plot上，这句每执行一次相当于往长布上放一小段新的plot（return的是PlotDataItem），
                                                            #这样每个循环就只用update（setdat）这一个新plot，而不用update一整个plot。而之前的不动（只有在有新的plot时去掉最早那一个）。
            curve1=self.p5.plot(pen=(255,0,0), name="Red curve")
                                
            self.curves.append(curve)  
            self.curves1.append(curve1)                  
            last = self.data5[-1]
            last1=self.data6[-1]
            self.data5 = np.empty((self.chunkSize+1,2))        
            self.data6 = np.empty((self.chunkSize+1,2))        
            self.data5[0] = last                         #2.清空chunk，把之前的最后一个放到第一个
            self.data6[0] = last1
            while len(self.curves) > self.maxChunks:
                c = self.curves.pop(0)
                self.p5.removeItem(c)                    #把一整段chunk一次性从plot中移除
                c = self.curves1.pop(0)
                self.p5.removeItem(c)                    #把一整段chunk一次性从plot中移除
                
        else:
            curve = self.curves[-1]
            curve1 = self.curves1[-1]
        

        self.data5[i+1,0] = now - self.startTime                    #定义时间轴
        self.data5[i+1,1] = self.data[0]     #读取最近一次数据
        self.data6[i+1,0] = now - self.startTime                    #定义时间轴
        self.data6[i+1,1] = self.data[1]        #读取最近一次数据
    
        curve.setData(x=self.data5[:i+2, 0], y=self.data5[:i+2, 1]) #pyqtgraph的绘图数据主要是通过setData()这个方法来转化为图形。
                                                        #后面设置了一个定时器，每隔一个时间重新调用setData()方法对图形数据curve（plot）进行设，就能够实现实时的数据可视化呈现。
                                                        #set的是最后一个chunk的0到第i个（也就是最近）的数据
        curve1.setData(x=self.data6[:i+2, 0], y=self.data6[:i+2, 1])

        self.ptr5 += 1      

# 运行函数
thread_data=[10,10,10]
def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = monitor_window(thread_data)
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()