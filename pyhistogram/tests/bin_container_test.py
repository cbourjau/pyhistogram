"""Test the behavior of the Bin_container class"""

from pyhistogram.bin_container import _Bin_container
import unittest


class Test_bin_container(unittest.TestCase):
    def test_init_with_contradictory_args(self):
        self.assertRaises(ValueError, _Bin_container, -1)
        self.assertRaises(ValueError, _Bin_container, 1, 1, 2)

    def test_1D(self):
        bc = _Bin_container(2)
        self.assertEqual(bc.get_nglobal(), 2)
        self.assertEqual(bc.find_global_bin_from_ijk(1), 1)

    def test_2D(self):
        bc = _Bin_container(2, 2)
        self.assertEqual(bc.get_nglobal(), 4)
        self.assertEqual(bc.find_global_bin_from_ijk(2, 1), 2)
        self.assertEqual(bc.find_global_bin_from_ijk(1, 2), 3)
        self.assertEqual(bc.find_global_bin_from_ijk(2, 2), 4)

    def test_3D(self):
        bc = _Bin_container(2, 2, 2)
        self.assertEqual(bc.get_nglobal(), 8)
        self.assertEqual(bc.find_global_bin_from_ijk(2, 1, 1), 2)
        self.assertEqual(bc.find_global_bin_from_ijk(1, 2, 1), 3)
        self.assertEqual(bc.find_global_bin_from_ijk(1, 1, 2), 5)
        self.assertEqual(bc.find_global_bin_from_ijk(2, 2, 2), 8)
        

    def test_get_bin_contents_1d(self):
        
