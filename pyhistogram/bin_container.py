from math import sqrt


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

    def __init__(self, nxbins, nybins=1, nzbins=1):
        """Initialization of the Bin_container.

        Parameters
        ----------
        nxbins, nybins, nzbins : int
           Number of bins along each axis. Must be greater than 1
        """
        if (nxbins < 1 or nybins < 1 or nzbins < 1) or (
                (nybins == 1 and nzbins > 1)):
            raise ValueError('Invalid number of bins given')
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
        return len(self._bins)

    def get_global_bin_from_ijk(self, i, j=1, k=1):
        """Returns the global bin number given the axis bin numbers.
        
        The axis bin numbers are denoted as i, j, k for the x, y and z axis respectively. They are element of [1, N] where N is I, J, or K respectively.

        Parameters
        ----------
        i : int
           Local bin number of the x axis
        j,k : int, optional
           Local bin numbers of the y and z axis. (Default 1)

        Return
        ------
        int
        """
        return ((k - 1) * self.J + j - 1) * self.I + i

    def get_ijk_from_global_bin(self, gidx):
        """Returns the local bin numbers for each axis given the global bin number.

        Parameters
        ----------
        gidx : int
           Global bin number

        Return
        ------
        tuple :
           The three axis bin numbers (i, j, k)
        """
        # imagine a 3d block of bins curled up in a 1D array with above formular.
        # Work with mod to find the "layer of the current bin
        z_level, rem = divmod(gidx, self.I*self.J)
        # check if the last level is exactly full or if the next level is started:
        k = z_level + 1 if rem > 0 else z_level

        y_level, rem = divmod(rem, self.I)
        j = y_level + 1 if rem > 0 else y_level

        i = rem if rem > 0 else self.I
        return i, j, k

    def fill_bin(self, gidx, weight=1):
        """Increment the value of the given bin by the given weight

        Parameters
        ----------
        gidx : int
           Global bin number

        Return
        ------
        None
        """
        # remember the -1 to convert bin number to index!
        self._bins[gidx - 1][0] += weight

    def get_bin_content(self, gidx):
        """Returns the content of a given bin.

        Parameters
        ----------
        gidx : int
           Global bin number

        Return
        ------
        float
        """
        # remember, gidx starts at 1!
        return self._bins[gidx-1][0]

    def set_bin_content(self, gidx, v):
        """Replaces the content of a bin with the given value.

        Parameters
        ----------
        gidx : int
           Global bin number
        v : float
           New content of this bin
        """
        self._bins[gidx-1][0] = v

    def get_bin_error(self, gidx):
        """Returns the error of a given bin.

        Parameters
        ----------
        gidx : int
           Global bin number

        Return
        ------
        float
        """
        return sqrt(self._bins[gidx][1])

    def set_bin_error(self, gidx, e):
        """Replaces the error of a bin with the given value.

        Parameters
        ----------
        gidx : int
           Global bin number
        e : float
           New error of this bin
        """
        self._bins[gidx][1] = e
