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

plt.plot(width, g, 'g')
markerline, stemlines, baseline = plt.stem(width, g, 'g')
plt.title("g[n] Graph")
plt.ylabel('g[n]')
plt.xlabel('n value')
plt.show()

plt.plot(width, r, 'b')
markerline, stemlines, baseline = plt.stem(width, r, 'b')
plt.title("r[n] Graph")
plt.ylabel('r[n]')
plt.xlabel('n value')
plt.show()
