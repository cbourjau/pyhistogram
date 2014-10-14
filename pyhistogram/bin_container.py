"""
The Bin_container is an iterable of all the bins in the histogram organized in one long array.
In this array, each object reprsents a bin and the array's index + 1 is referred to as the global
bin number.

Having I bins along the x-axis, J bins along the y-axis and K bins along the z-axis,
the mapping from the xyz bin numbers (i, j, k) to the global bin number b is given by:

b = (k-1)*(J-1)*I + (j-1)*I + i

Thus, in case of a 2D histogram (k=K=1; j>1) this reduces to:
b = (j-1)*I + i

and for a 1D histogram (k=K=1=j=J=1):
b = i


The bin container class does not deal with the finding of bins in user defined units. It exclusivly
deals with bin numbers and leaves the user defined bin sizes and units to the axis class
"""

from math import sqrt


class Bin_container(object):
    def __init__(self, nxbins, nybins=1, nzbins=1):
        # check input values
        if (nxbins < 1 or nybins < 1 or nzbins < 1) or (nybins == 1 and nzbins > 1):
            raise ValueError('Invalid number of bins given')
        self.I, self.J, self.K = nxbins, nybins, nzbins
        # Each bin has (value, sum_w2)
        self._bins = [[0, 0] for i in range(self.I*self.J*self.K)]

    @property
    def nbins(self):
        return len(self._bins)

    def get_global_bin_from_ijk(self, i, j=1, k=1):
        """i, j, k the bin numbers on the x, y and z axis. They are element of [1, N]
        where N is I, J, or K respectivly
        """
        return ((k - 1) * self.J + j - 1) * self.I + i

    def get_ijk_from_global_bin(self, gidx):
        """return (i, j, k)"""
        # imagine a 3d block of bins curled up in a 1D array with above formular.
        # Work with mod to find the "layer of the current bin
        z_level, rem = divmod(gidx, self.I*self.J)
        # check if the last level is exactly full or if the next level is started:
        k = z_level + 1 if rem > 0 else z_level

        y_level, rem = divmod(rem, self.I)
        j = y_level + 1 if rem > 0 else y_level
        # import ipdb; ipdb.set_trace()

        i = rem if rem > 0 else self.I

        return i, j, k

    def fill_bin(self, global_bin_number, weight=1):
        # remember the -1 to convert bin number to index!
        self._bins[global_bin_number - 1][0] += weight

    def get_bin_content(self, gidx):
        # remember, gidx starts at 1!
        return self._bins[gidx-1][0]

    def set_bin_content(self, gidx, v):
        """Replace the bin's content"""
        self._bins[gidx-1][0] = v

    def get_bin_error(self, gidx):
        return sqrt(self._bins[gidx][1])
            
    def set_bin_error(self, gidx, e):
        """Replace the bin's error"""
        self._bins[gidx][1] = e
