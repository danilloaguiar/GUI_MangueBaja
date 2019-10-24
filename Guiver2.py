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

pckt = []
value1 = deque(100*[0], 100)
time = deque(100*[0], 100)

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
        pckt = unpack(FORMAT, msg)
        print(pckt)
        #self.updateData()

    def updateData(self):
        value1.append(pckt[2])
        time.append(pckt[0])
        print(value1, time)


        




class grafs():
    def __init__(self, car):
        self.rpm_plt = plt.subplot2grid((2, 2), (0, 0))
        self.speed_plt = plt.subplot2grid((2, 2), (0, 1))
        self.imu_plt = plt.subplot2grid((2, 2), (1, 0), colspan=2)
    def update(self, msg):
        print("ola")


if __name__ == "__main__":
    box = Receiver(name = 'serial_port')
    box.start()
    plt.title('TELEMETRY SIGNAL') 

    



