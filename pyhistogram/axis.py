"""
The Axis class functions allows quick access to information about the histograms
binnings etc.
"""
from pyhistogram.flow_exceptions import (OverflowException,
                                         UnderflowException)


class _Axis(object):
    def __init__(self, edges, hist):
        """
        edges: The bin edges along this axis
        hist: the parent-histogram of this axis
        """
        # check if edges are sane
        if len(edges) < 2:
            raise ValueError('Too few edges given')
        if not strictly_increasing(edges):
            raise ValueError('Bin edges not monotonically increasing')
        # does the number of values (if) given, match the number of bins?
        self.__edges = edges
        self._hist = hist

    def get_number_of_bins(self):
        return len(self.__edges) - 1

    def get_bin_centers(self):
        return [l + (u - l) / 2.0 for l, u in zip(self.__edges, self.__edges[1:])]

    def get_bin_edges(self):
        return self.__edges

    def get_bin_low_edge(self, i):
        return self.get_bin_edges()[i-1]

    def get_bin_up_edge(self, i):
        return self.get_bin_edges()[i]

    def get_bin_center(self, i):
        low = self.get_bin_low_edge(i)
        high = self.get_bin_up_edge(i)
        return low + (high - low) / 2.0

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
