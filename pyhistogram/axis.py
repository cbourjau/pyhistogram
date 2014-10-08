"""
The Axis class functions allows quick access to information about the histograms
binnings etc.
"""


class _Axis(object):
    def __init__(self, edges):
        # check if edges are sane
        if len(edges) < 2:
            raise ValueError('Too few edges given')
        if not strictly_increasing(edges):
            raise ValueError('Bin edges not monotonically increasing')
        # does the number of values (if) given, match the number of bins?
        self.__edges = edges

    def get_number_of_bins(self):
        return len(self.__edges) - 1

    def get_bin_centers(self):
        return [l + (u - l) / 2.0 for l, u in zip(self.__edges, self.__edges[1:])]

    def get_bin_edges(self):
        return self.__edges

    def find_axis_bin(self, v):
        """ Find the bin of this axis containing v.
        This is not the global bin number of the histogram!
        returns bin_num
        0 represents underflow, nbins+1 overflow
        """
        # generator returning the first match for an index
        gen = (i for i, (l, u) in enumerate(zip(self.__edges, self.__edges[1:])) if l <= v < u)
        index = gen.next()
        return index + 1

    
def strictly_increasing(L):
    return all(x < y for x, y in zip(L, L[1:]))
