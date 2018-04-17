import numpy as np
import scipy
from scipy import signal
import matplotlib.pyplot as plt
import math
import warnings
warnings.filterwarnings('ignore')

width = []
for i in range (32):
    width.append(i)

n = np.linspace(0,31,32)
x = []
y = []
for i in range(len(n)):
    x.append(10*math.cos(math.pi*n[i]/16))
    if 10*math.cos(math.pi*n[i]/16) < (-8):
        y.append(-8)
    elif 10*math.cos(math.pi*n[i]/16) > (8):
        y.append(8)
    else:
        y.append(10*math.cos(math.pi*n[i]/16))

x = np.array(x)
y = np.array(y)

x_dft = np.fft.fft(x)/32
y_dft = np.fft.fft(y)/32

for i in range (len(x_dft)):
    if x_dft[i] < 0:
        x_dft[i] *= -1
    if y_dft[i] < 0:
        y_dft[i] *= -1

plt.plot(width, x_dft, 'g')
markerline, stemlines, baseline = plt.stem(width, x_dft, 'g')
plt.title("X[k] Graph")
plt.ylabel('X[k]')
plt.xlabel('k value')
plt.show()

plt.plot(width, y_dft, 'b')
markerline, stemlines, baseline = plt.stem(width, y_dft, 'b')
plt.title("Y[k] Graph")
plt.ylabel('Y[k]')
plt.xlabel('k value')
plt.show()
