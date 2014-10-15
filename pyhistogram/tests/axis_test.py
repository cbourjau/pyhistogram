"""Test the behavior of the Axis class"""

from pyhistogram.axis import _Axis
from pyhistogram.hist import Hist1D
from pyhistogram.flow_exceptions import OverflowException, UnderflowException

import unittest
from datetime import datetime


class Test_Axis(unittest.TestCase):
    def setUp(self):
        self.hist = Hist1D(10, 0, 1)

    def test_init_with_contradictory_args(self):
        # decreasing or equal edges
        self.assertRaises(ValueError, _Axis, self.hist, [2, 1])
        self.assertRaises(ValueError, _Axis, self.hist, [2, 2])
        # too few edges
        self.assertRaises(ValueError, _Axis, self.hist, [2, ])

    def test_number_of_created_bins(self):
        a = _Axis(self.hist, [1, 2])
        self.assertEqual(a.nbins, 1)
        a = _Axis(self.hist, [1, 2, 5])
        self.assertEqual(a.nbins, 2)

    def test_getter(self):
        a = _Axis(self.hist, [1, 2, 3])
        self.assertEqual(a.get_bin_centers(), [1.5, 2.5])
        self.assertEqual(a.get_bin_edges(), [1, 2, 3])

    def test_find_bin(self):
        a = _Axis(self.hist, [1, 2, 3])
        self.assertEqual(a.find_axis_bin(1.5), 1)
        self.assertEqual(a.find_axis_bin(1.0), 1)
        self.assertEqual(a.find_axis_bin(2.0), 2)
        # underflow
        self.assertRaises(UnderflowException, a.find_axis_bin, 0.0,)
        # overflow
        self.assertRaises(OverflowException, a.find_axis_bin, 5.0)

    def test_find_bin_datetime(self):
        a = _Axis(self.hist, [datetime(2014, 1, 1, 12, 0),
                              datetime(2014, 1, 1, 13, 0),
                              datetime(2014, 1, 1, 14, 0)])
        self.assertEqual(a.find_axis_bin(datetime(2014, 1, 1, 12, 0)), 1)
        self.assertEqual(a.find_axis_bin(datetime(2014, 1, 1, 12, 30)), 1)
        # underflow
        self.assertRaises(UnderflowException, a.find_axis_bin,
                          datetime(2014, 1, 1, 10, 0))
        # overflow
        self.assertRaises(OverflowException, a.find_axis_bin,
                          datetime(2014, 1, 1, 15, 0))


class Test_Axis_strings(unittest.TestCase):
        def setUp(self):
            self.hist = Hist1D(['My', 'name', 'is', 'Bond'])

        def test_find_bin(self):
            [self.hist.fill(s) for s in ['James', 'Bond']]
            v = [(b.x.regex, b.value) for b in self.hist.bins()]
            self.assertEqual(v,
                             [('My', 0), ('name', 0), ('is', 0), ('Bond', 1)])
            [self.hist.fill(s) for s in ['NAME', 'bond']]
            v = [(b.x.regex, b.value) for b in self.hist.bins()]
            self.assertEqual(v,
                             [('My', 0), ('name', 1), ('is', 0), ('Bond', 2)])
