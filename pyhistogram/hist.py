"""
The Hist classes are the entry point for the user for creating and using the histogram
"""

from pyhistogram.axis import _Axis
from pyhistogram.bin_container import _Bin_container


class Hist1D(object):
    def __init__(self, *args):
        """
        Fixed width:
        args = (nbins, lower, higher)
        Variable width:
        args = ([edges])
        """
        # compute edges for fixed width case
        if len(args) == 3:
            nbins, lower, upper = args
            width = nbins / float(upper - lower)
            edges = [lower + n * width for n in range(nbins + 1)]

        # compute number of bins for variable bin size case
        elif len(args) == 1:
            edges = args[0]
            nbins = len(edges) - 1

        # raise exception if none of these cases was found
        else:
            raise TypeError('Wrong number of arguments given')
        self.Xaxis = _Axis(edges)
        self._Bin_container = _Bin_container(nbins)

    def fill(self, v, weight=1):
        xbin_number = self.Xaxis.find_axis_bin(v)
        if xbin_number == 0 or xbin_number == self.Xaxis.get_number_of_bins() + 1:
            assert(0)  # overflow handling not implemented
        gbin_number = self._Bin_container.find_global_bin_from_ijk(xbin_number)
        self._Bin_container.fill_bin(gbin_number)

    def get_bin_contents():
        pass
