===========
pyhistogram
===========

**This is an early release which is not yet battle-hardened. Please file an issue over at github if you encounter problems**

What is pyhistogram
===================

pyhistogram is a pure python package for easy handling of histogram data. It offers much more functionality than pythons build-in 'collections' feature. 

pyhistogram interface is heavily inspired by the excellent rootpy package which, however, depends on the gigantic particle physics ROOT framework - an dependency hardly justifiable for small projects. At the moment pyhistogram has no dependencies at all. Matplotlib is optional if one wants to use the built in plotting features. Than also means that this packages performance is nowhere near to that of the rootpy/ROOT solution, but should be sufficient for most use cases. In any case, it is quite possible that numpy might be added as an dependency in the future to use some of its features and to give this package a performance boost. 

Currently, pyhistogram only supports one dimensional histograms but is designed with higher dimensions in mind.


Taking it for a spin:
=====================

The following shows some, but by far not all features. A proper documentation is on the todo list but for now I can recommend tacking a look at the unittests.

Installing pyhistogram:
-----------------------
::

   $ pip install pyhistogram


Creating  histograms:
---------------------
::

  from pyhistogram import Hist1D

  # 1D histogram with fixed-width bins
  h1d = Hist1D(5, -2, 4)
  # variable-width bins
  h1d = Hist1D([-10, -3.2, 5.2, 35.])


Histograms can be filled in loops:
----------------------------------
::

  >>> import random
  >>> h = Hist1D(10, -4, 12)
  >>> for i in xrange(1000):
  >>>     h.fill(random.gauss(4, 3))

And one can easily iterate through all the bins:
------------------------------------------------

::

  >>> h = Hist1D(4, 0, 4)
  >>> h.fill(1)
  >>> [b.value for b in h.bins()]
  [1, 0, 0, 0]
  
  

A weight can be associated to each value in a 2-tuple:
------------------------------------------------------
::

  >>> h = Hist1D(4, 0, 4)
  >>> h.fill((1, weight=0.5)
  >>> [b.value for b in h.bins()]
  [0.5, 0, 0, 0]
  


datetime support is also no-brainer:
------------------------------------
::

  from datetime import datetim
  h = Hist1D(4, datetime(2014, 1, 1, 12, 0), datetime(2014, 1, 1, 16, 0))
  h.fill(datetime(2014, 1, 1, 13, 0))


And even word frequencies (based on regex) are all there for your convenience:
------------------------------------------------------------------------------
::

   >>> hist = Hist1D(['My', 'name', 'is', 'Bond'])
   >>> [hist.fill(s) for s in ['James', 'Bond']]
   >>> [(b.x.regex, b.value) for b in self.hist.bins()]
   [('My', 0), ('name', 0), ('is', 0), ('Bond', 1)]
   



If matplotlib is available, a histogram can also be plotted conveniently:
-------------------------------------------------------------------------
::

  from pyhistogram import Hist1D
  import numpy as np
  import matplotlib.pyplot as plt
  
  h = Hist1D(20, -5, 5)
  sample = np.random.normal(size=500)
  for v in sample:
   h.fill(v)
   h.plot()
   plt.show()


Running the included unit tests (for (pyhistogram) developers):
::

   $ nosetests pyhistogram
