pyhistogram
===========

__This is currently pre-alpha software! The API will change and things are probably not going to work for you yet!__


pyhistogram is a python package for easy handling of histogram data. It offers much more functionality than pythons build in cummulative features. 

pyhistogram is heavily inspired by the excellent rootpy package which, however, depends on the ROOT framework.

# Examples #

A few examples probably best demonstrate what pyhistogram is all about!

## Creating  histograms ##

```python
from pyhistogram import Hist1D, Hist2D, Hist3D

# 1D histogram with fixed-width bins
h1d = Hist1D(5, -2, 4)
# variable-width bins
h1d = Hist1D([-10, -3.2, 5.2, 35.])

# 2D histogram with fixed-width bins; 10 along x and 5 along y
h2d = Hist2D(10, 0, 1, 5, -2, 4)
# 3 variable-width bins along x and 4 fixed-width bins along y
h2d = Hist2D([10, 30, 100, 1000], 4, 10, 33.5)

# 3D histogram with fixed-width bins
h3d = Hist3D(100, 0, 1, 20, 5.8, 7.2, 1e4, -10, 1)
# fixed-width bins along x and z and variable-width bins along y
h3d = Hist3D(5, 0, 1, [-20, 5, 50, 1e3], 10, 0, 1)
```

Histograms can be filled either in loops:

```python
import random
from pyhistogram import Hist1D

h = Hist(10, -4, 12)
for i in xrange(1000):
    h.fill(random.gauss(4, 3))
```

...or from iterables:


```python
from pyhistogram import Hist1D
h = Hist(10, 0, 10)
a = [1,3,6,9,3]
h.fill_array(a)
```

a weight can be associated to each value in a 2-tuple:

```python
import random
from pyhistogram import Hist1D

h = Hist(3, 0, 3)
for i in xrange(1000):
    h.fill((random.gauss(4, 3), random.rand()))

# and for itrables:
a = [(1, random.rand()), (3, random.rand()), (6, random.rand())]
h.fill(a)
```

Information about the histogram can be accessed in a number of ways:

```python
>>> from pyhistogram import Hist1D
>>> h = Hist(3, 0, 3)
>>> h.x_axis.get_bin_centers()
[.5, 1.5, 2.5]
>>> h.x_axis.get_bin_edges()
[0, 1, 2, 3]
>>> h.fill_array([.5, .5, 1.5, 3.5])
>>> h.x_axis.get_bin_contents()
[2, 0, 0]
>>> h.x_axis.get_bin_contents(with_overflow=True)
[0, 2, 0, 0, 1]
```


