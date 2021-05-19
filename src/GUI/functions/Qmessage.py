
from PyQt5.QtWidgets import QMessageBox

def error_message():
    msgBox = QMessageBox()
    msgBox.setWindowTitle('error prompt')
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("error")
    msgBox.setStandardButtons(QMessageBox.Retry | QMessageBox.Abort | QMessageBox.Ignore)
    msgBox.setDefaultButton(QMessageBox.Retry)
    msgBox.setDetailedText('details:no port found')
    reply = msgBox.exec() 
    if reply == QMessageBox.Retry:
        pass
    elif reply == QMessageBox.Abort:
        pass
    else:
        pass
