import numpy as np
import matplotlib.pyplot as plt
i =0
j=0



def graf1():
        global i
        Y = np.random.random() 
        Y2 =  np.random.random() 
        Y3 = 0.8 - (np.random.random() * 0.03)
        x.append(i)
        x2.append(i)
        x3.append(i)
        y.append(Y)
        y2.append(Y2)
        y3.append(Y3)
        i += 1  
        plt.subplot(2, 1, 1)
        plt.axis((i-20,i+1,0,1))
        plt.plot(x, y, color='k', label='Signal 1')
        plt.plot(x2, y2, color='blue', label='signal 2')
        plt.plot(x3, y3, color='red',label='signal 3')
        plt.xlabel("Time(s)")
        plt.ylabel("Signal Amplitude")
        if i == 1:
                plt.legend()
        plt.grid(False)
        plt.pause(0.1)

def graf2():
        global j
        S = np.random.random()
        S2 = np.random.random()
        S3 = 0.5
        r.append(j)
        r2.append(j)
        r3.append(j)
        s.append(S)
        s2.append(S2)
        s3.append(S3)
        j+=1
        plt.subplot(2, 1, 2)
        plt.axis((j-20,j+1,0,1))
        plt.plot(s, r, color='k', label='X')
        plt.plot(s2, r2, color='blue', label='Y')
        plt.plot(s3, r3, color='red',label='Z')
        plt.xlabel("Time(s)")
        plt.ylabel("G force")
        if j == 1:
                plt.legend()
        plt.grid(False)
        plt.pause(0.1)
x = []
y = []
x2 = []
y2 = []
x3 = []
y3 = []
r = []
s = []
r2 = []
s2 = []
r3 = []
s3 = []

while 1:
    graf1()
    graf2()
plt.show()  