from struct import unpack
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import threading
import serial
import time
import pandas as pd

ID = 11
serial_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyACM1']
SIZE = 24
FORMAT = '<BHHHHHHHHBBLB'

time = deque(200*[0], 200)
accx = deque(200*[0], 200)
accy = deque(200*[0], 200)
accz = deque(200*[0], 200)
rpm = deque(200*[0], 200)
speed = deque(200*[0], 200)
temp = deque(200*[0], 200)
car = deque(200*[''], 200)



time_save = []
accx_save = []
accy_save = []
accz_save = []
rpm_save = []
speed_save = []
temp_save = []
car_save = []



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
        print(pckt)
        #print(pckt[10])
        time.append(pckt[11])
        accx.append(pckt[1])
        accy.append(pckt[2])
        accz.append(pckt[3])
        rpm.append(pckt[7])
        speed.append(pckt[8])
        temp.append(pckt[9])
        if pckt[0] == 22:
            car.append("MB2")
        if pckt[0] == 11:
            car.append("MB1")       



        time_save.append(pckt[11])
        accx_save.append(pckt[1])
        accy_save.append(pckt[2])
        accz_save.append(pckt[3])
        rpm_save.append(pckt[7])
        speed_save.append(pckt[8])
        temp_save.append(pckt[0])
        car_save.append(pckt[0]) 

        #print(accx_save)  
            
    
        data = {
        'Tempo': time_save,
        'Carro': car_save,
        'Aceleração X': accx_save,
        'Aceleração Y': accy_save,
        'Aceleração Z': accz_save, 
        'RPM': rpm_save,
        'Velocidade': speed_save,
        'Temperatura': temp_save
        }      
        csv = pd.DataFrame(data, columns=['Tempo','Carro', 'Aceleração X', 'Aceleração Y', 'Aceleração Z', 'RPM', 'Velocidade', 'Temperatura'])
        csv.to_csv('dados_telemetria.csv')

        

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


        temp_plt.plot(time, temp, 'c-', marker="h")
        temp_plt.set_title('Temperatura ' + car[-1])
        temp_plt.set_xlim(-200 + time[-1], time[-1])
        #temp_plt.set_ylim(0, 90)

        rpm_plt.plot(time, rpm, 'c-', marker="h")
        rpm_plt.set_title('Rotação do motor ' + car[-1])
        rpm_plt.set_xlim(-200 + time[-1], time[-1])
        #rpm_plt.set_ylim(0, 5000)

        speed_plt.plot(time, speed, 'k-', marker="h")
        speed_plt.set_title('Velocidade '+ car[-1])
        speed_plt.set_xlim(-200 + time[-1], time[-1])
        #speed_plt.set_ylim(0, 80)
        plt.grid(True)

        imu_plt.plot(time, accx, 'b-', marker="h", label='Eixo X')
        imu_plt.plot(time, accy, 'r-', marker="h", label='Eixo Y')
        imu_plt.plot(time, accz, 'g-', marker="h", label='Eixo Z')
        imu_plt.set_title('Aceleração ' + car[-1])
        imu_plt.set_xlim(-200 + time[-1], time[-1])
        #imu_plt.set_ylim(-10, 10)
        imu_plt.legend()

     
  

        plt.pause(0.001)