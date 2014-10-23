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
    """Convert the given datetime or list of datetimes to unix time stamps.

    If v is not a datetime, return it unchanged

    Parameters
    ----------
    v : datetime
       The datetime to be converted. Its assumed that it is given in utc.
       If it is not of type datetime, return the value unchanged

    Return
    ------
    int (if datetime was given) or initial type of v
    """
    if isinstance(v, list) and isinstance(v[0], datetime):
        v_conv = []
        for a in v:
            v_conv.append(timegm(a.timetuple()))
    elif isinstance(v, datetime):
        v_conv = timegm(v.timetuple())
    else:
        v_conv = v
    return v_conv


def _establish_dtype(v):
    """Returns the type of the bin edges on this axis

    Parameters
    ----------
    v : str or int or float or datetime or list
       Value or list of values to be used as edges for the axis

    Return
    ------
    str :
       {'numerical'|'datetime'|'regex'}
    """
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


def _strictly_increasing(L):
    return all(x < y for x, y in zip(L, L[1:]))


class Axis(object):
    """The Axis is the container for all the functions specific to one
    particular dimension of the histogram.

    E.g. the type of the edge values, number of bins etc.
    """
    def __init__(self, hist, *args):
        """
        Initialization of a new axis

        Parameters
        ----------
        hist : Hist
           The histogram to which this axis belongs
        args : array_like
           Either:
              * Only element of type list it gives the bin edges
              * Three elements: nbins (int), lowest bound, highest bound

        Example
        -------
        Initialization with bin edges

        >>> ax = Axis(hist, [1, 4, 9])
        >>> ax = Axis(hist, ['My', 'name', 'is', 'Bond']])

        Initialization with number of bins (10), lowest (0) and highest bound (1)

        >>> ax = Axis(hist, 10, 0, 1)

        """
        self.hist = hist
        # variable bin width or string of regexes
        if len(args) == 1:
            self.dtype = _establish_dtype(args[0])
            if self.dtype == 'datetime' or self.dtype == 'numerical':
                self._edges = _convert_datetimes_to_unix_time(args[0])
                # check if edges are sane
                if len(self._edges) < 2:
                    raise ValueError('Too few edges given')
                if not _strictly_increasing(self._edges):
                    raise ValueError('Bin edges not monotonically increasing')
            if self.dtype == 'regex':
                self._edges = [re.compile(s, re.IGNORECASE) for s in args[0]]
                # append an empty string to mimic the last (excluded) edge of the hist
                self._edges.append('')

        # fixed bin widths
        elif len(args) == 3:
            nbins = args[0]
            self.dtype = _establish_dtype(args[1:])
            if self.dtype == 'datetime' or self.dtype == 'numerical':
                lower = _convert_datetimes_to_unix_time(args[1])
                upper = _convert_datetimes_to_unix_time(args[2])
                width = float(upper - lower) / nbins
                self._edges = [lower + n * width for n in range(nbins + 1)]
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
        """Returns the number of bins along this axis.

        Return
        ------
        int
        """
        return len(self._edges) - 1

    def get_bin_centers(self):
        """Returns the centers of the bins along this axis.

        This function is not available if the axis is of type 'regex'.

        Return
        ------
        array_like
        """
        return convert_to_dtype(
            [l + (u - l) / 2.0 for l, u in zip(self._edges, self._edges[1:])],
            self.dtype)

    def get_bin_regexes(self):
        """Returns the regexes (not the patterns) of the bins along this axis.

        This function is only available for axes of the type 'regex'.

        Return
        ------
        array_like
        """
        # exclude the empty string as the last edge
        return self._edges[:(self.nbins)]

    def get_bin_regex(self, i):
        """Return the regex for the respective bin on this axis.

        This function is not available if the axis is of type datetime, numerical

        Parameters
        ----------
        i : int
           Axis bin number

        Return
        ------
        array_like
        """
        return self._edges[i]

    def get_bin_edges(self, convert=True):
        """Returns the edges of the bins along this axis.

        This function is not available if the axis is of type 'regex'.

        Parameters
        ----------
        convert : bool
           If true, the returned value will be converted to the appropriate type of the axis (e.g. datetime)

        Return
        ------
        array_like :
           The length of this array is nbins + 1
        """
        if convert:
            return convert_to_dtype(self._edges, self.dtype)
        else:
            return self._edges

    def get_bin_low_edge(self, i, convert=True):
        """Returns only the lower bin edges of the bins along this axis.

        This function is not available if the axis is of type 'regex'.

        Parameters
        ----------
        convert : bool
           If true, the returned value will be converted to the appropriate type of the axis (e.g. datetime)

        Return
        ------
        array_like
        """
        return self.get_bin_edges(convert)[i]

    def get_bin_up_edge(self, i, convert=True):
        """Returns only the upper bin edge of for a given axis-bin number.

        This function is not available if the axis is of type 'regex'.

        Parameters
        ----------
        convert : bool
           If true, the returned value will be converted to the appropriate
           type  of the axis (e.g. datetime)

        Return
        ------
        array_like
        """
        return self.get_bin_edges(convert)[i+1]

    def get_bin_center(self, i):
        """Returns the center of the given bin, if appropriate converted
        to the axis's type.

        This function is not available if the axis is of type 'regex'.

        Parameters
        ----------
        i : int
           Axis bin number

        Return
        ------
        float or datetime
        """
        low = self.get_bin_low_edge(i, convert=False)
        high = self.get_bin_up_edge(i, convert=False)
        return convert_to_dtype(low + (high - low) / 2.0, self.dtype)

    def get_bin_width(self, i):
        """Returns the width of the given bin in the appropriate type.

        This function is not available if the axis is of type 'regex'.

        Parameters
        ----------
        i : int
           Axis bin number

        Return
        ------
        float or datetime
        """
        low = self.get_bin_low_edge(i)
        high = self.get_bin_up_edge(i)
        return high - low

    def get_type(self):
        """Returns the type of the axis.

        Return:
        str :
           {'numerical', 'datetime', 'regex'}
        """
        return self.dtype

    def _find_axis_bin_numerical(self, v):
        """ Find the bin of this axis containing v.
        This is not the global bin number of the histogram!
        returns bin_num or raises exceptions for over/under flow
        """
        # generator returning the first match for an index
        v = _convert_datetimes_to_unix_time(v)
        gen = (i for i, (l, u) in
               enumerate(zip(self._edges, self._edges[1:])) if l <= v < u)
        try:
            index = gen.next()
        except StopIteration:
            # underflow:
            if v < self._edges[0]:
                raise UnderflowException
            else:
                raise OverflowException
        return index + 1

    def _find_axis_bin_regex(self, s):
        """Find the bin with regex matching the string s
        return: axis_binnummber or raises exception if no match is found"""
        # generator returns indices of matches
        # exclude the last bin edge (empty string)
        gen = (i for i, rx in enumerate(self._edges[:-1]) if rx.match(s))
        try:
            index = gen.next()
        except StopIteration:
            raise OverflowException
        return index + 1
