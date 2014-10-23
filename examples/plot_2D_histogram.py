"""
Example on how a 2D histogram may be plotted with matplotlib
============================================================

The example is adapted from http://wiki.scipy.org/Cookbook/Histograms
"""

import numpy as np
import matplotlib.pyplot as plt

from random import gauss
from pyhistogram import Hist

h = Hist(40, -1, 1, 50, -1, 1)
for i in range(10000):
    h.fill(gauss(.6, .3), gauss(.6, .4))
    h.fill(gauss(-.6, .3), gauss(-.6, .4), weight=-1)

H = h.get_content()
x, y = h.Xaxis.get_bin_edges(), h.Yaxis.get_bin_edges()
X, Y = np.meshgrid(x, y)
fig = plt.figure()

ax = fig.add_subplot(111)
ax.set_title('2D histogram of two Gaussians')

# H needs to be transposed!
plt.pcolormesh(X, Y, H.T)
ax.set_ylim((y[0], y[-1]))
ax.set_aspect('auto')

# Finally we add a color bar
cax = fig.add_axes([0.1, 0.1, .95, .8])
cax.get_xaxis().set_visible(False)
cax.get_yaxis().set_visible(False)
cax.patch.set_alpha(0)
cax.set_frame_on(False)
plt.colorbar(ax=cax)
plt.show()
