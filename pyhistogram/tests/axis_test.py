"""Test the behavior of the Axis class"""

from pyhistogram.axis import _Axis
from pyhistogram.flow_exceptions import OverflowException, UnderflowException
import unittest


class Test_Axis(unittest.TestCase):
    def setUp(self):
        self.fake_hist = 'fake_hist'

    def test_init_with_contradictory_args(self):
        # decreasing or equal edges
        self.assertRaises(ValueError, _Axis, [2, 1], self.fake_hist)
        self.assertRaises(ValueError, _Axis, [2, 2], self.fake_hist)
        # too few edges
        self.assertRaises(ValueError, _Axis, [2, ], self.fake_hist)

    def test_number_of_created_bins(self):
        a = _Axis([1, 2], self.fake_hist)
        self.assertEqual(a.get_number_of_bins(), 1)
        a = _Axis([1, 2, 5], self.fake_hist)
        self.assertEqual(a.get_number_of_bins(), 2)

    def test_getter(self):
        a = _Axis([1, 2, 3], self.fake_hist)
        self.assertEqual(a.get_bin_centers(), [1.5, 2.5])
        self.assertEqual(a.get_bin_edges(), [1, 2, 3])

    def test_find_bin(self):
        a = _Axis([1, 2, 3], self.fake_hist)
        self.assertEqual(a.find_axis_bin(1.5), 1)
        self.assertEqual(a.find_axis_bin(1.0), 1)
        self.assertEqual(a.find_axis_bin(2.0), 2)
        # underflow
        self.assertRaises(UnderflowException, a.find_axis_bin, 0.0,)
        # overflow
        self.assertRaises(OverflowException, a.find_axis_bin, 5.0)
