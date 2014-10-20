class Bin_proxy(object):
    """The bin proxy is a convenient interface for getting additional information about each bin when iterating through several bins of the histogram. 

    The bin proxy is created for each bin yielded by h.bins(), e.g.:::

      >>> for bin in h.bins():
      ...     print bin.center
    """
    def __init__(self, hist, gidx):
        """Initialization of a new Bin_proxy.

        Parameters
        ----------
        hist : pyhistogram.Hist1D
           Parent histogram to which this bin belongs
        gidx : int
           Global bin index
        """
        self.hist = hist
        self.gidx = gidx
        self.ijk = self.axial_indices

    @property
    def axial_indices(self):
        """Returns the axial indices (i, j, k) for this bin.

        This function always returns three indices regardless of the histograms dimensionality.

        Return
        ------
        tuple :
           Tuple of the three axial indices (i, j, k)
        """
        return self.hist.Bin_container.get_ijk_from_global_bin(self.gidx)

    @property
    def x(self):
        """Provides an entry point for retrieving x-axis specific information from this bin.

        Return
        ------
        pyhistogram.bin_proxy.bi
        """
        return self.axis_bininfo(0, self.ijk[0])

    @property
    def y(self):
        """Provides an entry point for retrieving y-axis specific information from this bin.

        Return
        ------
        pyhistogram.bin_proxy.bi
        """
        return self.axis_bininfo(1, self.ijk[1])

    @property
    def z(self):
        """Provides an entry point for retrieving z-axis specific information from this bin.

        Return
        ------
        pyhistogram.bin_proxy.bi
        """
        return self.axis_bininfo(2, self.ijk[2])

    @property
    def value(self):
        """Return the value of this bin.

        Return
        ------
        float
        """
        return self.hist.Bin_container.get_bin_content(self.gidx)

    @value.setter
    def value(self, v):
        """Replace the bin's value with the given value v.

        Parameters
        ----------
        v : int or float
           New value of this bin
        """
        self.hist.Bin_container.set_bin_content(self.gidx, v)

    @property
    def error(self):
        """Return the error of this bin.

        Return
        ------
        float
        """
        return self.hist.Bin_container.get_bin_error(self.idx)

    @error.setter
    def error(self, e):
        """Replace the bin's error with the given value v.

        Parameters
        ----------
        v : int or float
           New value of this bin
        """
        return self.hist.Bin_container.set_bin_error(self.idx)

    @property
    def effective_entries(self):
        """
        Number of effective entries in this bin.
        The number of unweighted entries this bin would need to
        contain in order to have the same statistical power as this
        bin with possibly weighted entries, estimated by:

            (sum of weights) ** 2 / (sum of squares of weights)

        """
        sum_w2 = self.sum_w2
        if sum_w2 == 0:
            return abs(self.value)
        return (self.value ** 2) / sum_w2

    def __iadd__(self, other):
        self.value += other.value
        self.sum_w2 += other.sum_w2
        return self

    def __imul__(self, other):
        self.value *= other.value
        self.sum_w2 *= other.sum_w2
        return self

    def __idiv__(self, other):
        self.value /= other.value
        self.sum_w2 /= other.sum_w2
        return self

    def __repr__(self):
        return '{0}({1}, {2})'.format(
            self.__class__.__name__, self.hist, self.gidx)

    def axis_bininfo(self, ax, ax_idx):
        if self.hist.axes[ax].dtype != 'regex':
            class Bin_info:
                """Interface to axis specific information for a given bin.

                Attributes
                ----------
                axis : pyhistogram.Axis
                   Axis from which this Bin_info class was created
                low : float or datetime
                   Lower edge of this bin.
                center : float or datetime
                   Center of this bin.
                high : float or datetime
                   Upper edge of this bin.
                width : float or datetime.timedelta
                   Width of this bin.
                """
                axis = self.hist.axes[ax]
                low = axis.get_bin_low_edge(ax_idx)
                center = axis.get_bin_center(ax_idx)
                high = axis.get_bin_up_edge(ax_idx)
                width = axis.get_bin_width(ax_idx)
            return Bin_info
        else:
            class Bin_info:
                """Interface to axis specific information for a given bin.

                Attributes
                ----------
                axis : pyhistogram.Axis
                   Axis from which this Bin_info class was created
                regex : str
                   Regex pattern of this bin
                """
                axis = self.hist.axes[ax]
                regex = axis.get_bin_regex(ax_idx).pattern
            return Bin_info
