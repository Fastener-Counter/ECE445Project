# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""
#import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import serieRead_test
import sys

# win = pg.GraphicsLayoutWidget(show=True)
# win.setWindowTitle('pyqtgraph example: Scrolling Plots')


# # 1) Simplest approach -- update data in the array such that plot appears to scroll
# #    In these examples, the array size is fixed.
# p1 = win.addPlot()
# p2 = win.addPlot()
# data1 = np.random.normal(size=300)
# curve1 = p1.plot(data1)
# curve2 = p2.plot(data1)
# ptr1 = 0
# def update1():
#     global data1, ptr1
#     data1[:-1] = data1[1:]  # shift data in the array one sample left
#                             # (see also: np.roll)
#     data1[-1] = np.random.normal()
#     curve1.setData(data1)
    
#     ptr1 += 1
#     curve2.setData(data1)
#     curve2.setPos(ptr1, 0)
    

# # 2) Allow data to accumulate. In these examples, the array doubles in length   #data一直累计，越来越多，第三张图之所以scroll还是因为xrange的限制，其实data一直在增多
# #    whenever it is full. 
# win.nextRow()             #换行
# p3 = win.addPlot()
# p4 = win.addPlot()
# # Use automatic downsampling and clipping to reduce the drawing load
# p3.setDownsampling(mode='peak')
# p4.setDownsampling(mode='peak')
# p3.setClipToView(True)
# p4.setClipToView(True)
# p3.setRange(xRange=[-100, 0])
# p3.setLimits(xMax=0)
# curve3 = p3.plot()
# curve4 = p4.plot()

# data3 = np.empty(100)
# ptr3 = 0

# def update2():
#     global data3, ptr3
#     data3[ptr3] = np.random.normal()
#     ptr3 += 1
#     if ptr3 >= data3.shape[0]:
#         tmp = data3
#         data3 = np.empty(data3.shape[0] * 2)
#         data3[:tmp.shape[0]] = tmp
#     curve3.setData(data3[:ptr3])
#     curve3.setPos(-ptr3, 0)
#     curve4.setData(data3[:ptr3])


# 3) Plot in chunks, adding one new plot curve for every 100 samples ，


def update3():
    global p5, data5, data6, ptr5, curves,curves1             #函数外面的定义也适用函数里面，避免每次循环都要定义一遍

    now = pg.ptime.time()
    for c in curves:
        c.setPos(-(now-startTime), 0)           #使得之前的不断往负半轴移动，而我们始终看（-10，0），所以这个是看上去在scroll的关键！！！！
    for c in curves1:
        c.setPos(-(now-startTime), 0)           #使得之前的不断往负半轴移动，而我们始终看（-10，0），所以这个是看上去在scroll的关键！！！！
    
    i = ptr5 % chunkSize                        #表示最近一次读入分配到最近一个chunk的第i个位置
    if i == 0:   
        curve = p5.plot()                               #新的chunck放到新的plot上，这句每执行一次相当于往长布上放一小段新的plot（return的是PlotDataItem），
                                                        #这样每个循环就只用update（setdat）这一个新plot，而不用update一整个plot。而之前的不动（只有在有新的plot时去掉最早那一个）。
        curve1=p5.plot(pen=(255,0,0), name="Red curve")
                              
        curves.append(curve)  
        curves1.append(curve1)                  
        last = data5[-1]
        last1=data6[-1]
        data5 = np.empty((chunkSize+1,2))        
        data6 = np.empty((chunkSize+1,2))        
        data5[0] = last                         #2.清空chunk，把之前的最后一个放到第一个
        data6[0] = last1
        while len(curves) > maxChunks:
            c = curves.pop(0)
            p5.removeItem(c)                    #把一整段chunk一次性从plot中移除
            c = curves1.pop(0)
            p5.removeItem(c)                    #把一整段chunk一次性从plot中移除
            
    else:
        curve = curves[-1]
        curve1 = curves1[-1]
    data5[i+1,0] = now - startTime                    #定义时间轴
    data5[i+1,1] = serieRead_test.distance_data()     #读取最近一次数据
    data6[i+1,0] = now - startTime                    #定义时间轴
    data6[i+1,1] = serieRead_test.distance_data()     #读取最近一次数据
    
    curve.setData(x=data5[:i+2, 0], y=data5[:i+2, 1]) #pyqtgraph的绘图数据主要是通过setData()这个方法来转化为图形。
                                                      #后面设置了一个定时器，每隔一个时间重新调用setData()方法对图形数据curve（plot）进行设，就能够实现实时的数据可视化呈现。
                                                      #set的是最后一个chunk的0到第i个（也就是最近）的数据
    curve1.setData(x=data6[:i+2, 0], y=data6[:i+2, 1])

    ptr5 += 1                              

# update all plots
def update():
    #update1()
    #update2()
    update3()


def plot_distances(monitor):
    #win = pg.GraphicsLayoutWidget(show=True)
    monitor.win.setWindowTitle('pyqtgraph example: Scrolling Plots')
    chunkSize = 100
    # Remove chunks after we have 10
    maxChunks = 10                                
    startTime = pg.ptime.time()
    p5 = monitor.win.addPlot(colspan=2)                     #p5是一张图
    p5.setLabel('bottom', 'Time', 's')
    p5.setXRange(-10, 0)                            #由于xrange，屏幕上只能打出6个trunk左右，所以我们看不到一整段被remove，所以整个就是连续的。
    curves = []
    curves1=[]
    data5 = np.empty((chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data
    data6 = np.empty((chunkSize+1,2))               #一个chunk一共有101*2个数据，第一列为时间，第二列为data
    ptr5 = 0                                        #指针，表示最近一次读入的是第prt5个数据

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update3)
    timer.start(0)          #这个是定时器，时间间隔秒，是自动一直在运行的

if __name__ == '__main__':
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(0)          #这个是定时器，时间间隔秒，是自动一直在运行的    
    pg.mkQApp().exec_()