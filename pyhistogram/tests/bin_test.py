"""Test the behavior of the Bin class"""

from pyhistogram.bin import _Bin
import unittest


class Test_bin(unittest.TestCase):

    def test_init_with_insufficient_args(self):
        self.assertRaises(TypeError, _Bin)
        # giving only lower_edge
        self.assertRaises(TypeError, _Bin, 1)

    def test_init_with_contradicting_args(self):
        # lower > upper edge
        self.assertRaises(ValueError, _Bin, 2, 1)

    def test_bin_data(self):
        b = _Bin(0, 1)
        self.assertEqual(b.lower_edge, 0)
        self.assertEqual(b.upper_edge, 1)
        self.assertEqual(b.center, 0.5)
        b = _Bin(-2, -1)
        self.assertEqual(b.center, -1.5)

    def test_bin_initialize_with_no_content(self):
        b = _Bin(0, 1)
        self.assertEqual(b.content, 0)

    def test_bin_initialize_with_content(self):
        b = _Bin(0, 1, 5)
        self.assertEqual(b.content, 5)
