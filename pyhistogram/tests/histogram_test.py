from pyhistogram.hist import Hist1D
from pyhistogram.utils import UTC
import unittest
from datetime import datetime


class Test_Hist_1D(unittest.TestCase):
    def test_init_fixed_width(self):
        h = Hist1D(4, 0, 4)
        self.assertEqual(h.Xaxis.get_bin_edges(), [0, 1, 2, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 1.5, 2.5, 3.5])
        self.assertEqual(h.Xaxis.nbins, 4)

        # float sized bins:
        h = Hist1D(4, 0, 1)
        self.assertEqual(h.Xaxis.get_bin_centers(),
                         [0.125, 0.375, 0.625, 0.875])

    def test_init_variable_width(self):
        h = Hist1D([0, 1, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_edges(), [0, 1, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 2.0, 3.5])
        self.assertEqual(h.Xaxis.nbins, 3)

    def test_fill_1D(self):
        h = Hist1D(4, 0, 4)
        h.fill(2.1)
        self.assertEqual([b.value for b in h.bins()], [0, 0, 1, 0])
        h.fill(3.1)
        h.fill(3.1)
        self.assertEqual([b.value for b in h.bins()], [0, 0, 1, 2])

        # over_flow:
        h.fill(4.1)
        self.assertEqual([b.value for b in h.bins()], [0, 0, 1, 2])
        self.assertEqual(h.get_overflow(), 1)

        # under_flow:
        h.fill(-1)
        self.assertEqual([b.value for b in h.bins()], [0, 0, 1, 2])
        self.assertEqual(h.get_overflow(), 2)

    def test_hist_creation_with_datetime(self):
        h = Hist1D(4, datetime(2014, 1, 1, 12, 0), datetime(2014, 1, 1, 16, 0))
        utc = UTC()
        self.assertEqual(h.Xaxis.get_bin_edges(),
                         [datetime(2014, 1, 1, 12, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 13, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 14, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 15, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 16, 0, tzinfo=utc)])

    def test_filling_with_weights(self):
        h = Hist1D(4, 0, 4)
        h.fill(2.1, weight=2)
        self.assertEqual([b.value for b in h.bins()], [0, 0, 2, 0])
        start, end = datetime(2014, 1, 1, 12, 0), datetime(2014, 1, 1, 16, 0)
        h = Hist1D(4, start, end)
        h.fill(start, weight=2)
        self.assertEqual([b.value for b in h.bins()], [2, 0, 0, 0])
