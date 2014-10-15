"""The bin proxy is a convinient interface for getting additional information
about each bin when iterating through several bins of the histogram.
E.g.:
for bin in h.bins():
    print bin.center
"""


class Bin_proxy(object):
    """
    The bin proxy is created for each bin yielded
    by h.bins()
    """

    def __init__(self, hist, gidx):
        self.hist = hist
        self.gidx = gidx
        self.ijk = self.axial_indices

    @property
    def axial_indices(self):
        """return the axial indices for this bin"""
        return self.hist.Bin_container.get_ijk_from_global_bin(self.gidx)

    @property
    def x(self):
        return self.axis_bininfo(0, self.ijk[0])

    @property
    def y(self):
        return self.axis_bininfo(1, self.ijk[1])

    @property
    def z(self):
        return self.axis_bininfo(2, self.ijk[2])

    @property
    def value(self):
        return self.hist.Bin_container.get_bin_content(self.gidx)

    @value.setter
    def value(self, v):
        return self.hist.Bin_container.set_bin_content(self.gidx, v)

    @property
    def error(self):
        return self.hist.Bin_container.get_bin_error(self.idx)

    @error.setter
    def error(self, e):
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
            class bi:
                axis = self.hist.axes[ax]
                low = axis.get_bin_low_edge(ax_idx)
                center = axis.get_bin_center(ax_idx)
                high = axis.get_bin_up_edge(ax_idx)
                width = axis.get_bin_width(ax_idx)
            return bi
        else:
            class bi:
                axis = self.hist.axes[ax]
                regex = axis.get_bin_regex(ax_idx).pattern
            return bi
