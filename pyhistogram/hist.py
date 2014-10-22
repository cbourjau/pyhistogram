"""
The Hist classes are the entry point for the user for creating and using the histogram
"""

from pyhistogram.axis import Axis
from pyhistogram.bin_container import Bin_container
from pyhistogram.flow_exceptions import OverflowException, UnderflowException
from pyhistogram.bin_proxy import Bin_proxy
from pyhistogram.utils import isbasictype

from copy import deepcopy


class Hist(object):
    def __init__(self, *args):
        """Initialization of a one dimensional histogram

        A histogram can either be specified in two ways:
            1. By the number of bins, lower and upper bound. The equidistant
               bin edges will be calculated automatically.
            2. By specifying the bin edges explicitly.

        Parameters
        ----------
        Fixed width:
        args : array_like
               The first element must be an int (number of bins), the second
               and third may be either int or float or datetime
        Variable width:
        args : array_like
               Array like object of length one. The first and only element is
               of type list or tuple with elements of type int or float or
               datetime
        """
        self.axes = []
        itargs = iter(args)
        for arg0 in itargs:
            # variable bin width
            if isinstance(arg0, (list, tuple)):
                edges = arg0
                self.axes.append(Axis(self, edges))
            # fixed bin width
            else:
                try:
                    nbins, lower, upper = arg0, itargs.next(), itargs.next()
                except StopIteration:
                    raise TypeError('Wrong number of arguments given')
                self.axes.append(Axis(self, nbins, lower, upper))

        # shortcuts for x, y and z axis
        try:
            self.Xaxis = self.axes[0]
            self.Yaxis = self.axes[1]
            self.Zaxis = self.axes[2]
        except IndexError:
            pass

        self.Bin_container = Bin_container(*[a.nbins for a in self.axes])

        # if len(self.axes) > 1:
        #     raise NotImplemented('Only 1 dimensions are currently supported')

        # no fancy stuff, increment this if overflow happens on any axes
        self.overflow = 0

    def fill(self, x, y=None, z=None, weight=1):
        """Function for adding content to the histogram.

        The bin containing the given x coordinate will be incremented with
        the value given as weight.

        Parameters
        ----------
        x, y, z : int or float or datetime or string
            The given type has to be compatible to the type used when
            initializing the histogram. y and z only have to be
            specified if the histogram is of
            corresponding dimensionality.
        weight : int or float
            value by which the content of the bin containing the given
            coordinates is increased.

        Example
        -------
        >>> h = Hist(10, 0, 1)
        >>> h.fill(2.5, weight=0.5)
        """
        try:
            # bin numbers start at 1
            xbin_number = self.Xaxis.find_axis_bin(x)
            ybin_number = self.Yaxis.find_axis_bin(y) if y else 1
            zbin_number = self.Zaxis.find_axis_bin(z) if z else 1
        except (UnderflowException, OverflowException):
            self.overflow += 1
        else:
            gbin_number = self.Bin_container.get_global_bin_from_ijk(
                xbin_number, ybin_number, zbin_number)
            self.Bin_container.fill_bin(gbin_number, weight=weight)

    def get_overflow(self):
        """Return overflow of the entire histogram.

        No differentiation between individual axes nor under and overflow
        is implemented, yet.

        Return
        ------
        int :
           The number of times the histogram was filled with coordinates
           not matching any bins
        """
        return self.overflow

    def bins(self):
        """A iterator for all the bins in the histogram.

        Return
        ------
        Bin_proxy:
           A class giving easy access to all the information of this bin.
        """
        n_total = self.Bin_container.nbins
        # remember, gidx starts at 1!
        for gidx in range(1, n_total+1):
            yield Bin_proxy(self, gidx)

    def get_dimensions(self):
        """Returns the number of dimensions of this histogram.

        Return
        ------
        int
        """
        return len(self.axes)

    def plot(self, **kwargs):
        """Plot the current histogram.

        This requires matplotlib to be installed. All the given keywords
        are passed to the bar() function of matplotlib.

        Parameters
        ----------
        kwargs : dict
           are passed on to the bar() function of matplotlib.

        Return
        ------
        matplotlib.patches.Rectangle :
           This is the return value of the bar() function
        """
        try:
            import matplotlib.pyplot as plt
            from matplotlib import dates
        except ImportError:
            print 'matplotlib is needed for plotting functionality'
            return None
        values = [bin.value for bin in self.bins()]
        if self.Xaxis.dtype == 'datetime':
            centers = dates.date2num([bin.x.center for bin in self.bins()])
            edges = dates.date2num(self.Xaxis.get_bin_edges())
            widths = [c_right - c_left for
                      c_right, c_left in zip(edges[1:], edges[:-1])]
            ret = plt.bar(centers, values, width=widths,
                          align='center', **kwargs)
            plt.gca().xaxis_date()
            plt.gcf().autofmt_xdate()
        elif self.Xaxis.dtype == 'numerical':
            centers = [bin.x.center for bin in self.bins()]
            width = [bin.x.width for bin in self.bins()]
            ret =  plt.bar(centers, values, align='center', width=width, **kwargs)
        else:
            centers = range(len(values))
            names = [b.x.regex for b in self.bins()]
            width = 1
            ret = plt.bar(centers, values, align='center', width=width, **kwargs)
            ax = plt.gca()
            ax.set_xticks([x for x in range(len(centers))])
            ax.set_xticklabels(
                names, rotation=45, rotation_mode="anchor", ha="right")
        return ret

    def check_compatibility(self, other, precision=1E-7):
        """
        Test whether two histograms are considered compatible by the number of
        dimensions, number of bins along each axis, and optionally the bin
        edges.

        Parameters
        ----------
        other : histogram
           A rootpy histogram
        precision : float, optional (default=1E-7)
           The value below which differences between floats are treated as
           nil when comparing bin edges.

        Raises
        ------
        TypeError
           If the histograms dimensions or axis types do not match.
        ValueError
           If the histogram sizes, number of bins along an axis or
           the bin edges do not match.
        """
        if self.get_dimensions() != other.get_dimensions():
            raise TypeError("histogram dimensionalities do not match")
        for i, (ax1, ax2) in enumerate(zip(self.axes, other.axes)):
            if ax1.nbins != ax2.nbins:
                raise ValueError(
                    "Numbers of bins along axis {0:d} do not match".format(i))
            if ax1.get_type() != ax2.get_type():
                raise TypeError(
                    "Types of axis {0:d} are incompatible ({1}, {2})".format(
                        i, ax1.get_type(), ax2.get_type()))
            if ((ax1.get_type != 'regex')
                and not all([abs(l - r) < precision for l, r in zip(
                    ax1.get_bin_edges(convert=False),
                    ax2.get_bin_edges(convert=False))])):
                raise ValueError(
                    "Edges do not match along axis {0:d}".format(i))
            if ((ax1.get_type == 'regex')
                and not all([l.pattern == r.pattern for l, r in zip(
                    ax1.get_bin_edges(convert=False),
                    ax2.get_bin_edges(convert=False))])):
                raise ValueError(
                    "Edges do not match along axis {0:d}".format(i))

    def compatible(self, other, precision=1E-7):
        try:
            self.check_compatibility(other, precision=precision)
        except (TypeError, ValueError):
            return False
        return True

    def __add__(self, other):
        copy = deepcopy(self)
        copy += other
        return copy

    def __iadd__(self, other):
        self.check_compatibility(other)
        if isbasictype(other):
            if other != 0:
                for bin in self.bins():
                    bin.value += other
        else:
            # The bins were found to be compatible, so we can just
            # iterate through all of them adding them one by one
            for b_this, b_other in zip(self.bins(), other.bins()):
                b_this += b_other
        return self

    def __sub__(self, other):
        copy = deepcopy(self)
        copy -= other
        return copy

    def __isub__(self, other):
        self.check_compatibility(other)
        if isbasictype(other):
            if other != 0:
                for bin in self.bins():
                    bin.value -= other
        else:
            # The bins were found to be compatible, so we can just
            # iterate through all of them adding them one by one
            for b_this, b_other in zip(self.bins(), other.bins()):
                b_this -= b_other
        return self

    def __mul__(self, other):
        copy = deepcopy(self)
        copy *= other
        return copy

    def __imul__(self, other):
        self.check_compatibility(other)
        if isbasictype(other):
            if other != 0:
                for bin in self.bins():
                    bin.value *= other
        else:
            # The bins were found to be compatible, so we can just
            # iterate through all of them adding them one by one
            for b_this, b_other in zip(self.bins(), other.bins()):
                b_this *= b_other
        return self

    def __div__(self, other):
        copy = deepcopy(self)
        copy /= other
        return copy

    def __idiv__(self, other):
        self.check_compatibility(other)
        if isbasictype(other):
            if other != 0:
                for bin in self.bins():
                    bin.value /= other
        else:
            # The bins were found to be compatible, so we can just
            # iterate through all of them adding them one by one
            for b_this, b_other in zip(self.bins(), other.bins()):
                b_this /= b_other
        return self


def Hist1D(*args, **kwargs):
    from warnings import warn
    warn("Hist1D is deprecated in favor of Hist")
    return Hist(*args, **kwargs)
