from math import sqrt
import numpy as np

class Bin_container(object):
    """
    This class provides access to the histogram's bins without creating the need for the user to know anything about the internal storage mechanisms. Bins are organized in one long array with a unique mapping from the axis bin numbers i, j, k to the global bin number b. It is important to remember that each of these indices starts at 1 not 0.

    Having I bins along the x-axis, J bins along the y-axis and K bins along the z-axis, the mapping from the xyz bin numbers (i, j, k) to the global bin number b is given by:::

      b = (k-1)*(J-1)*I + (j-1)*I + i

    Thus, in case of a 2D histogram (k=K=1; j>1) this reduces to:::

      b = (j-1)*I + i

    and for a 1D histogram (k=K=1=j=J=1):::

      b = i

    The bin container class does not deal with the finding of bins in user defined units. It exclusively deals with bin numbers and leaves the user defined bin sizes and units to the axis class.
"""

    def __init__(self, nxbins, nybins=0, nzbins=0):
        """Initialization of the Bin_container.

        Parameters
        ----------
        nxbins, nybins, nzbins : int
           Number of bins along each axis. Must be greater than 1
        """
        if  ((nybins < 1 and nzbins > 0)):
            raise ValueError('z-axis specified without y-axis.')
        if nybins == 0 and nzbins == 0:
            self.values = np.zeros((nxbins, ))
        elif nybins != 0 and nzbins == 0:
            self.values = np.zeros((nxbins, nybins))
        elif nybins != 0 and nzbins != 0:
            self.values = np.zeros((nxbins, nybins, nzbins))
        self.I, self.J, self.K = nxbins, nybins, nzbins
        # Each bin has (value, sum_w2)
        self._bins = [[0, 0] for i in range(self.I*self.J*self.K)]


    @property
    def nbins(self):
        """Returns the total number of bins of in this histogram

        Return
        ------
        int
        """
        return reduce(lambda x, y: x*y, self.values.shape)

    def fill_bin(self, indices, weight=1):
        """Increment the value of the given bin by the given weight

        Parameters
        ----------
        indices : tuple
           axis bin numbers i, j, k

        Return
        ------
        None
        """
        # remember the -1 to convert bin number to index!
        # import ipdb; ipdb.set_trace()
        self.values[indices] += weight

    def get_bin_content(self, indices):
        """Returns the content of a given bin.

        Parameters
        ----------
        indices : tuple
           axis bin numbers i, j, k

        Return
        ------
        float
        """
        # remember, gidx starts at 1!
        return self.values[indices]

    def set_bin_content(self, indices, v):
        """Replaces the content of a bin with the given value.

        Parameters
        ----------
        indices : tuple
           axis bin numbers i, j, k
        v : float
           New content of this bin
        """
        self.values[indices] = v
