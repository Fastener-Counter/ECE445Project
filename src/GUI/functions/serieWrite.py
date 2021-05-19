import sys
import socket

def send(text):
    if True:                #USB
        if text='start':
            
    else:
        text = text + '!'
        print(text)
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect(("192.168.4.1", 333))
        print('fail to connect')
        tcp.send(text.encode())
        time.sleep(50/1000)
        tcp.close()