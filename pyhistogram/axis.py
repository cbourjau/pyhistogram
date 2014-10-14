"""
The Axis class functions allows quick access to information about the histograms
binnings etc.
"""
from pyhistogram.flow_exceptions import (OverflowException,
                                         UnderflowException)
from pyhistogram.utils import convert_to_dtype
from datetime import datetime
from calendar import timegm


def _convert_datetimes_to_unix_time(v):
    """Convert the given value or list of values to unix time stamps,
    if appropriate.
    return: v_converted, dtype ['numerical'|'datetime']
    """
    if isinstance(v, list) and isinstance(v[0], datetime):
        v_conv = []
        dtype = 'datetime'
        for a in v:
            v_conv.append(timegm(a.timetuple()))
    elif isinstance(v, datetime):
        v_conv = timegm(v.timetuple())
        dtype = 'datetime'
    else:
        v_conv = v
        dtype = 'numerical'
    return v_conv, dtype


class _Axis(object):
    # Are the edges datetimes in unix format or numerical values
    def __init__(self, hist, *args):
        """
        args: either one argument: bin_edges
              or  three arguments: nbins, lowerset, highest
        hist: the parent-histogram of this axis
        """
        self.hist = hist
        if len(args) == 1:
            edges, self.dtype = _convert_datetimes_to_unix_time(args[0])
            # check if edges are sane
            if len(edges) < 2:
                raise ValueError('Too few edges given')
            if not strictly_increasing(edges):
                raise ValueError('Bin edges not monotonically increasing')
            # does the number of values (if) given, match the number of bins?
            self.__edges = edges

        elif len(args) == 3:
            nbins = args[0]
            lower, self.dtype = _convert_datetimes_to_unix_time(args[1])
            upper, dtype2 = _convert_datetimes_to_unix_time(args[2])
            if self.dtype != dtype2:
                TypeError('Two incompatible histogram borders were given')
            width = float(upper - lower) / nbins
            edges = [lower + n * width for n in range(nbins + 1)]
            self.__edges = edges
        else:
            raise TypeError('Wrong number of arguments given')

    @property
    def nbins(self):
        return len(self.__edges) - 1

    def get_bin_centers(self):
        return convert_to_dtype(
            [l + (u - l) / 2.0 for l, u in zip(self.__edges, self.__edges[1:])],
            self.dtype)

    def get_bin_edges(self, convert=True):
        if convert:
            return convert_to_dtype(self.__edges, self.dtype)
        else:
            return self.__edges

    def get_bin_low_edge(self, i, convert=True):
        return self.get_bin_edges(convert)[i-1]

    def get_bin_up_edge(self, i, convert=True):
        return self.get_bin_edges(convert)[i]

    def get_bin_center(self, i):
        low = self.get_bin_low_edge(i, convert=False)
        high = self.get_bin_up_edge(i, convert=False)
        return convert_to_dtype(low + (high - low) / 2.0, self.dtype)

    def get_bin_width(self, i):
        low = self.get_bin_low_edge(i)
        high = self.get_bin_up_edge(i)
        return high - low

    def find_axis_bin(self, v):
        """ Find the bin of this axis containing v.
        This is not the global bin number of the histogram!
        returns bin_num or raises exceptions for over/under flow
        """
        # generator returning the first match for an index
        v, _ = _convert_datetimes_to_unix_time(v)
        gen = (i for i, (l, u) in enumerate(zip(self.__edges, self.__edges[1:])) if l <= v < u)
        try:
            index = gen.next()
        except StopIteration:
            # underflow:
            if v < self.__edges[0]:
                raise UnderflowException
            else:
                raise OverflowException
        return index + 1
    

def strictly_increasing(L):
    return all(x < y for x, y in zip(L, L[1:]))
