#!/usr/bin/python
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plt

from random import gauss
from pyhistogram import Hist

# adapted from http://wiki.scipy.org/Cookbook/Histograms

h = Hist(50, 0, 5, 50, 0, 6)

# Next we create a histogram H with random bin content
for i in range(100000):
    h.fill(gauss(2.5, 1), gauss(3, 1))
nx, ny = h.Xaxis.nbins, h.Yaxis.nbins
H = np.ndarray(shape=(nx, ny), dtype=float)
X = np.ndarray(shape=(nx+1, ny+1), dtype=float)
Y = np.ndarray(shape=(nx+1, ny+1), dtype=float)
for b in h.bins():
    H[b.x.axis_bin_number-1][b.y.axis_bin_number-1] = b.value
    X[b.x.axis_bin_number-1][b.y.axis_bin_number-1] = b.x.low
    Y[b.x.axis_bin_number-1][b.y.axis_bin_number-1] = b.y.low
# filling the edges
X[nx, :] = h.Xaxis.get_bin_edges()[-1]
X[:, ny] = h.Xaxis.get_bin_edges()
Y[nx, :] = h.Yaxis.get_bin_edges()
Y[:, ny] = h.Yaxis.get_bin_edges()[-1]

#ml.rcParams['image.cmap'] = 'gist_heat'

fig = plt.figure()

# pcolormesh is useful for displaying exact bin edges
ax = fig.add_subplot(111)
ax.set_title('pcolormesh:\nexact bin edges')
plt.pcolormesh(X, Y, H)
ax.set_aspect('equal')


# Finally we add a color bar
cax = fig.add_axes([0.12, 0.1, 0.78, 0.4])
cax.get_xaxis().set_visible(False)
cax.get_yaxis().set_visible(False)
cax.patch.set_alpha(0)
cax.set_frame_on(False)
plt.colorbar(ax=cax)
plt.tight_layout()
plt.show()
