"""
The Axis class functions allows quick access to information about the histograms
binnings etc.
"""
from pyhistogram.flow_exceptions import (OverflowException,
                                         UnderflowException)
from pyhistogram.utils import convert_to_dtype
from datetime import datetime
from calendar import timegm
import re


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
    return v_conv


def _establish_dtype(v):
    """v: value or list of values to be used as edges for the axis
    return: type of the values ['numerical'|'datetime'|'regex']"""
    if isinstance(v, (list, tuple)):
        v = list(v)
    if all(isinstance(x, (float, int)) for x in v):
        return 'numerical'
    elif all(isinstance(x, datetime) for x in v):
        return 'datetime'
    elif all(isinstance(x, str) for x in v):
        return 'regex'
    else:
        raise ValueError('Inconsitancy in given types')


class _Axis(object):
    # Are the edges datetimes in unix format or numerical values
    def __init__(self, hist, *args):
        """
        args: either one argument: bin_edges
              or  three arguments: nbins, lowerset, highest
        hist: the parent-histogram of this axis
        """
        self.hist = hist
        # variable bin width or string of regexes
        if len(args) == 1:
            self.dtype = _establish_dtype(args[0])
            if self.dtype == 'datetime' or self.dtype == 'numerical':
                self.edges = _convert_datetimes_to_unix_time(args[0])
                # check if edges are sane
                if len(self.edges) < 2:
                    raise ValueError('Too few edges given')
                if not strictly_increasing(self.edges):
                    raise ValueError('Bin edges not monotonically increasing')
            if self.dtype == 'regex':
                self.edges = [re.compile(s, re.IGNORECASE) for s in args[0]]
                # append an empty string to mimic the last (excluded) edge of the hist
                self.edges.append('')

        # fixed bin widths
        elif len(args) == 3:
            nbins = args[0]
            self.dtype = _establish_dtype(args[1:])
            if self.dtype == 'datetime' or self.dtype == 'numerical':
                lower = _convert_datetimes_to_unix_time(args[1])
                upper = _convert_datetimes_to_unix_time(args[2])
                width = float(upper - lower) / nbins
                self.edges = [lower + n * width for n in range(nbins + 1)]
            if self.dtype == 'regex':
                raise ValueError('Regex bins only support with list initialisation')
        else:
            raise TypeError('Wrong number of arguments given')

        # Register the appropriate bin finder for this dtype
        if self.dtype == 'regex':
            self.find_axis_bin = self._find_axis_bin_regex
        else:
            self.find_axis_bin = self._find_axis_bin_numerical


    @property
    def nbins(self):
        return len(self.edges) - 1

    def get_bin_centers(self):
        return convert_to_dtype(
            [l + (u - l) / 2.0 for l, u in zip(self.edges, self.edges[1:])],
            self.dtype)

    def get_bin_regex(self, i):
        return self.edges[i-1]

    def get_bin_edges(self, convert=True):
        if convert:
            return convert_to_dtype(self.edges, self.dtype)
        else:
            return self.edges

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

    def _find_axis_bin_numerical(self, v):
        """ Find the bin of this axis containing v.
        This is not the global bin number of the histogram!
        returns bin_num or raises exceptions for over/under flow
        """
        # generator returning the first match for an index
        v = _convert_datetimes_to_unix_time(v)
        gen = (i for i, (l, u) in enumerate(zip(self.edges, self.edges[1:])) if l <= v < u)
        try:
            index = gen.next()
        except StopIteration:
            # underflow:
            if v < self.edges[0]:
                raise UnderflowException
            else:
                raise OverflowException
        return index + 1

    def _find_axis_bin_regex(self, s):
        """Find the bin with regex matching the string s
        return: axis_binnummber or raises exception if no match is found"""
        # generator returns indices of matches
        # exclude the last bin edge (empty string)
        gen = (i for i, rx in enumerate(self.edges[:-1]) if rx.match(s))
        try:
            index = gen.next()
        except StopIteration:
            raise OverflowException
        return index + 1


def strictly_increasing(L):
    return all(x < y for x, y in zip(L, L[1:]))
