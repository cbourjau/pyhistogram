"""
===============================================
Fill a histogram with all the words from hamlet
===============================================

The following demonstrates how a histogram with regex-defined bins
may be used. Clearly, it is better to "be" than "not". The Hamlet text
is included in this package for convenient testing. You are welcome.
"""

from pyhistogram import Hist
import re
from pyhistogram.testdata import get_file  # Hamlet testdata

hist = Hist(['To', 'be', 'or', 'not'])

# Split the words up into individual words
words = re.findall('\w+', get_file().read().lower())

for w in words:
    hist.fill(w)

hist.plot()
