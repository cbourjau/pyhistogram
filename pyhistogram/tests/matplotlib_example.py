from pyhistogram import Hist1D
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# h = Hist1D(20, -5, 5)
# sample = np.random.normal(size=500)
# for v in sample:
#     h.fill(v)
# h.plot()
# plt.show()

h = Hist1D(4, datetime(2014, 1, 1, 12, 0), datetime(2014, 1, 1, 16, 0))
h.fill(datetime(2014, 1, 1, 12, 0))
h.plot()
plt.gcf().autofmt_xdate()
plt.show()


# import datetime
# import random
# import matplotlib.pyplot as plt

# # make up some data
# x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]
# y = [i+random.gauss(0,1) for i,_ in enumerate(x)]

# # plot
# plt.bar(x,y)
# # beautify the x-labels
# plt.gcf().autofmt_xdate()

# plt.show()
