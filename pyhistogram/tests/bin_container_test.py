"""Test the behavior of the Bin_container class"""

from pyhistogram.bin_container import Bin_container
import unittest


class Test_bin_container(unittest.TestCase):
    def test_init_with_contradictory_args(self):
        self.assertRaises(ValueError, Bin_container, -1)

    def test_1D(self):
        bc = Bin_container(2)
        self.assertEqual(bc.nbins, 2)
        self.assertEqual(bc.values.shape, (2,))

    def test_2D(self):
        bc = Bin_container(2, 2)
        self.assertEqual(bc.nbins, 4)
        self.assertEqual(bc.values.shape, (2, 2))

    def test_3D(self):
        bc = Bin_container(2, 2, 2)
        self.assertEqual(bc.nbins, 8)
        self.assertEqual(bc.values.shape, (2, 2, 2))
        
    def test_set_bin_contents_1d(self):
        bc = Bin_container(2)
        bc.set_bin_content(1, 3)
