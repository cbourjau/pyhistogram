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

class _Bin_container(object):
    def __init__(self, nxbins, nybins=1, nzbins=1):
        # check input values
        if (nxbins < 1 or nybins < 1 or nzbins < 1) or (nybins == 1 and nzbins > 1):
            raise ValueError('Invalid number of bins given')
        self.I, self.J, self.K = nxbins, nybins, nzbins
        # Each bin has (value, error)
        self._bins = [[0, 0]] * self.I*self.J*self.K

    def get_nglobal(self):
        return len(self._bins)

    def find_global_bin_from_ijk(self, i, j=1, k=1):
        """i, j, k the bin numbers on the x, y and z axis. They are element of [1, N]
        where N is I, J, or K respectivly
        """
        return ((k - 1) * self.J + j - 1) * self.I + i

    def fill_bin(self, global_bin_number, weight=1):
        self._bins[global_bin_number][0] += weight

    def _get_bin_contents(self, with_errors=False):
        # if 1D:
        if self.J == self.K == 1:
            if with_errors:
                return self._bins
            else:
                return [v[0] for v in self._bins]

        # if 2D or 3D
        else:
            raise NotImplementedError

            
