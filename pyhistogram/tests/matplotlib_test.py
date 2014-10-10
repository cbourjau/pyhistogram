from pyhistogram import Hist1D
import numpy as np
import matplotlib.pyplot as plt

h = Hist1D(20, -5, 5)
sample = np.random.normal(size=500)
for v in sample:
    h.fill(v)
h.plot()
plt.show()
