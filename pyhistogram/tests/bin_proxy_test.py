from pyhistogram import Hist1D
from pyhistogram.bin_proxy import Bin_proxy
from pyhistogram.utils import UTC

import unittest
from datetime import datetime


class Test_Bin_proxy(unittest.TestCase):

    def test_properties(self):
        h = Hist1D(10, 0, 10)
        bp = Bin_proxy(h, 1)
        self.assertEqual(bp.axial_indices, (1, 1, 1))
        self.assertEqual(bp.x.low, 0)
        self.assertEqual(bp.x.center, 0.5)
        self.assertEqual(bp.x.high, 1)
        self.assertEqual(bp.x.width, 1)
        self.assertEqual(bp.value, 0)

    def test_operations(self):
        h = Hist1D(10, 0, 10)
        bp1 = Bin_proxy(h, 1)
        bp1.value = 1
        bp1.value += 1
        self.assertEqual(bp1.value, 2)
        bp1.value *= 2
        self.assertEqual(bp1.value, 4)
        bp2 = Bin_proxy(h, 2)
        bp1.value, bp2.value = (2, 2)
        bp1.sum_w2, bp2.sum_w2 = (2, 2)

        bp1 += bp2
        self.assertEqual(bp1.value, 4)
        bp1 *= bp2
        self.assertEqual(bp1.value, 8)
        bp1 /= bp2
        self.assertEqual(bp1.value, 4)

    def test_iterating_through_edges(self):
        h = Hist1D(5, 0, 5)
        self.assertEqual([b.x.low for b in h.bins()], [0, 1, 2, 3, 4])
        self.assertEqual([b.x.high for b in h.bins()], [1, 2, 3, 4, 5])
        self.assertEqual([b.x.center for b in h.bins()], [.5, 1.5, 2.5, 3.5, 4.5])

    def test_iterating_through_edges_with_datetime(self):
        h = Hist1D(4, datetime(2014, 1, 1, 12, 0), datetime(2014, 1, 1, 16, 0))
        utc = UTC()
        self.assertEqual(h.Xaxis.get_bin_edges(),
                         [datetime(2014, 1, 1, 12, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 13, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 14, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 15, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 16, 0, tzinfo=utc)])
