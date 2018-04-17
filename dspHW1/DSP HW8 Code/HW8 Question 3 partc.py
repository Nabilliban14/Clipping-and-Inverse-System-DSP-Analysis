import numpy as np
import scipy
from scipy import signal
import matplotlib.pyplot as plt
import math
import warnings
warnings.filterwarnings('ignore')

width = []
for i in range (256):
    width.append(i)

#getting y[n]
n = np.linspace(0,255,256)
x = []
for i in range(len(n)):
    x.append(math.cos(17/64*math.pi*i) + 2*math.sin(23/32*math.pi*i))

x = np.array(x)
b = [1,-5/6,1/6]
a = [1]
y = scipy.signal.lfilter(b,a,x)

#getting r[n]
g = []
w = []
for i in range(len(n)):
    g.append(3*(1/2)**i - 2*(1/3)**i)
    if (i < 8):
        w.append(1)
    else:
        w.append(0)

g = np.array(g)
w = np.array(w)
r = g*w

#getting x_hat
x_hat = np.convolve(r,y)
x_hat.resize(256)

plt.plot(width, y, 'g')
markerline, stemlines, baseline = plt.stem(width, y, 'g')
plt.title("y[n] Graph")
plt.ylabel('y[n]')
plt.xlabel('n value')
plt.show()

plt.plot(width, x, 'b')
markerline, stemlines, baseline = plt.stem(width, x, 'b')
plt.title("x[n] Graph")
plt.ylabel('x[n]')
plt.xlabel('n value')
plt.show()

plt.plot(width, x_hat - x, 'r')
markerline, stemlines, baseline = plt.stem(width, x_hat - x, 'r')
plt.title("x-hat[n] - x[n] Graph")
plt.ylabel('x_hat[n] - x[n]')
plt.xlabel('n value')
plt.show()