from PyQt5.QtWidgets import (
    QWidget, QApplication, QProgressBar, QMainWindow,
    QHBoxLayout, QPushButton
)

from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot, QThread
)
import time


class WorkerSignals(QObject):
    progress = pyqtSignal(int)


class JobRunner(QThread):
    
    signals = WorkerSignals()
    
    def __init__(self):
        super().__init__()
        
        self.is_paused = False
        
    #@pyqtSlot()
    def run(self):
        n=0
        for n in range(1000):
            self.signals.progress.emit(n + 1)
            time.sleep(0.1)
            
            while self.is_paused:
                time.sleep(0)
                
    def pause(self):
        self.is_paused = True
        
    def resume(self):
        if not self.isRunning():
            self.start()
        self.is_paused = False
        
    def kill(self):
        self.start()
        try:
#            self.quit()
            self.terminate() #都没办法
        except:
            pass        #这里不加try就会卡死, resume的时候不会卡，但p只要摁了ause后按stop还是会卡死,这是为什么？sleep 必须要在terminate 后面，这里直接先start再terminate


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        # Some buttons
        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        
        btn_stop = QPushButton("Stop")
        btn_pause = QPushButton("Pause")
        btn_resume = QPushButton("Resume")
        
        l.addWidget(btn_stop)
        l.addWidget(btn_pause)
        l.addWidget(btn_resume)
        
        self.setCentralWidget(w)
       
        # Create a statusbar.
        self.status = self.statusBar()
        self.progress = QProgressBar()
        self.status.addPermanentWidget(self.progress)
        
        # Thread runner
        
        # Create a runner
        self.runner = JobRunner()
        self.runner.signals.progress.connect(self.update_progress)

        btn_stop.pressed.connect(self.runner.kill)
        btn_pause.pressed.connect(self.runner.pause)
        btn_resume.pressed.connect(self.runner.resume)
        self.show()

        
    
    def update_progress(self, n):
        self.progress.setValue(n)
        
app = QApplication([])
w = MainWindow()
app.exec_()