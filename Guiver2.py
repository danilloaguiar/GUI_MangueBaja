from struct import unpack
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import threading
import serial
import time

ID = 11
serial_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyACM1']
SIZE = 8
FORMAT = '<LBHB'

value1 = deque(20*[0], 20)
time = deque(20*[0], 20)

class Receiver(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name = name)
        self.com = self.connectSerial(serial_ports)
        print(f'Connected into {self.com}')

    def connectSerial(self, USB_PORT):
        for usb in USB_PORT:
            try:
                com = serial.Serial(f'{usb}', 115200)
            except:
                print("Tentativa...")
                com = []
            if com:
                break
        
        if not com:
            raise Exception("Não há nenhuma porta serial disponível")
        else:
            return com

    def run(self):
        self.com.flush()

        while True:
            self.checkData()
    
    def checkData(self):
        c = 0
        while c != b'\xff':
            c = self.com.read()
            #print(f'trying, {c}')
        msg = self.com.read(SIZE)
        #print(msg)
        pckt = list(unpack(FORMAT, msg))
        #print(pckt)
        value1.append(pckt[2])
        time.append(pckt[0])
        print(value1, time)


        





if __name__ == "__main__":
    box = Receiver(name = 'serial_port')
    box.start()

    while 1:
        plt.title('TELEMETRY SIGNAL')  
        #plt.axis((i-10,i+1,0,1))
        plt.plot(time, value1, marker="h", color='k')
        #plt.set_xlim(-10, 0)
        #plt.set_ylim(0, 1000)
        plt.xlabel("tempo")
        plt.ylabel("amplitude")
        plt.xlim(-10 + time[-1], time[-1])
        plt.ylim(100, 1000)
        plt.grid(True)
        plt.pause(0.1)






