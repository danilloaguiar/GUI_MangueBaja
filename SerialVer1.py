rom struct import unpack
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import threading
import serial
import time

ID = 55
serial_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyACM1']
SIZE = 60
FORMAT = 'hhhhhhhhhhhhhhhhhhhhhhhhHHBBI'

rpm = deque(100*[0], 100)
speed = deque(100*[0], 100)
accx = deque(400*[0], 400)
accy = deque(400*[0], 400)
accz = deque(400*[0], 400)

class Receiver(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name = name)
        self.com = self.connectSerial(serial_ports)
        # print(f'Connected into {self.com}')

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
            time.sleep(.1)
    
    def checkData(self):
        c = 0
        while c != b')':
            c = self.com.read()
            print(f'trying, {c}')
        msg = self.com.read(60)
        # self.com.flush()
        # msg = bytearray(b'')
        # while len(msg) < SIZE:
        #     c = self.com.read()
        #     if c == ID:
        #         msg = bytearray(b'')
        #     else:
        #         msg += c
        # print(msg)
        pckt = unpack(FORMAT, msg)
        # print('begin')  
        rpm.append(pckt[24]*5000/65536)
        speed.append(pckt[25]*60/65536)
        accx.append(pckt[0]/16384)
        accy.append(pckt[1]/16384)
        accz.append(pckt[2]/16384)
        accx.append(pckt[6]/16384)
        accy.append(pckt[7]/16384)
        accz.append(pckt[8]/16384)
        accx.append(pckt[12]/16384)
        accy.append(pckt[13]/16384)
        accz.append(pckt[14]/16384)
        accx.append(pckt[18]/16384)
        accy.append(pckt[19]/16384)
        accz.append(pckt[20]/16384)
        # print('end')
        # print(msg)
        print(pckt)
        # print(pckt[24])
        # print(pckt[27])
# with open('ex.bin', 'rb')HHBHHB as f:
#     msg = f.read()
#     pckt = unpack('24h2HB2HB5B', msg)
#     print(pckt)

# for i in range(10):

if __name__ == "__main__":
    r = Receiver(name = 'serial_port')
    r.start()
    t_10hz = np.linspace(-10, 0, 100)
    t_imu = np.linspace(-20, 0, 400)
    rpm_plt = plt.subplot2grid((2, 2), (0, 0))
    speed_plt = plt.subplot2grid((2, 2), (0, 1))
    imu_plt = plt.subplot2grid((2, 2), (1, 0), colspan=2)
    
    while True:
        rpm_plt.clear()
        speed_plt.clear()
        imu_plt.clear()
        
        rpm_plt.plot(t_10hz, rpm, 'c-')
        rpm_plt.set_title('Rotação do motor')
        rpm_plt.set_xlim(-10, 0)
        rpm_plt.set_ylim(0, 5000)

        speed_plt.plot(t_10hz, speed, 'k-')
        speed_plt.set_title('Velocidade')
        speed_plt.set_xlim(-10, 0)
        speed_plt.set_ylim(0, 60)

        imu_plt.plot(t_imu, accx, 'b-', label='Eixo X')
        imu_plt.plot(t_imu, accy, 'r-', label='Eixo Y')
        imu_plt.plot(t_imu, accz, 'g-', label='Eixo Z')
        imu_plt.set_title('Aceleração')
        imu_plt.set_xlim(-20, 0)
        imu_plt.set_ylim(-2, 2)
        imu_plt.legend()
        # print(accx)
        
        plt.pause(0.1)