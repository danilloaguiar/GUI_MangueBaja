from struct import unpack
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import threading
import serial
import time

ID = 11
serial_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyACM1']
SIZE = 24
FORMAT = '<LBHHHHHHHHBBB'

time = deque(20*[0], 20)
accx = deque(20*[0], 20)
accy = deque(20*[0], 20)
accz = deque(20*[0], 20)
rpm = deque(20*[0], 20)
speed = deque(20*[0], 20)
temp = deque(20*[0], 20)
title = '' 


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
        time.append(pckt[0])
        accx.append(pckt[2])
        accy.append(pckt[3])
        accz.append(pckt[4])
        rpm.append(pckt[8])
        speed.append(pckt[9])
        temp.append(pckt[10])
        if pckt[1] == 22:
            title = 'Telemetria MB2'
        
        if pckt[1] == 11:
            title = 'Telemetria MB1'gi
        
        


        

if __name__ == "__main__":
    box = Receiver(name = 'serial_port')
    box.start()

    rpm_plt = plt.subplot2grid((3, 3), (1, 2), rowspan=2)
    speed_plt = plt.subplot2grid((3, 3), (0, 1), colspan=2)
    temp_plt = plt.subplot2grid((3, 3), (0, 0))
    imu_plt = plt.subplot2grid((3, 3), (1, 0), colspan=2, rowspan=2)
    

    while True:
        rpm_plt.clear()
        speed_plt.clear()
        imu_plt.clear()
        temp_plt.clear()


        temp_plt.plot(time, temp, 'c-')
        temp_plt.set_title('Temperatura')
        temp_plt.set_xlim(-20 + time[-1], time[-1])
        temp_plt.set_ylim(0, 90)

        rpm_plt.plot(time, rpm, 'c-')
        rpm_plt.set_title('Rotação do motor')
        rpm_plt.set_xlim(-20 + time[-1], time[-1])
        rpm_plt.set_ylim(0, 5000)

        speed_plt.plot(time, speed, 'k-')
        speed_plt.set_title('Velocidade')
        speed_plt.set_xlim(-20 + time[-1], time[-1])
        speed_plt.set_ylim(0, 80)

        imu_plt.plot(time, accx, 'b-', label='Eixo X')
        imu_plt.plot(time, accy, 'r-', label='Eixo Y')
        imu_plt.plot(time, accz, 'g-', label='Eixo Z')
        imu_plt.set_title('Aceleração')
        imu_plt.set_xlim(-20 + time[-1], time[-1])
        imu_plt.set_ylim(-10, 10)
        imu_plt.legend()
        
 
        

  

        plt.pause(0.1)

        







