"""Test the behavior of the Bin_container class"""

from pyhistogram.bin_container import Bin_container
import unittest


class Test_bin_container(unittest.TestCase):
    def test_init_with_contradictory_args(self):
        self.assertRaises(ValueError, Bin_container, -1)
        self.assertRaises(ValueError, Bin_container, 1, 1, 2)

    def test_1D(self):
        bc = Bin_container(2)
        self.assertEqual(bc.nbins, 2)
        self.assertEqual(bc.get_global_bin_from_ijk(1), 1)

    def test_2D(self):
        bc = Bin_container(2, 2)
        self.assertEqual(bc.nbins, 4)
        self.assertEqual(bc.get_global_bin_from_ijk(2, 1), 2)
        self.assertEqual(bc.get_global_bin_from_ijk(1, 2), 3)
        self.assertEqual(bc.get_global_bin_from_ijk(2, 2), 4)

    def test_3D(self):
        bc = Bin_container(2, 2, 2)
        self.assertEqual(bc.nbins, 8)
        self.assertEqual(bc.get_global_bin_from_ijk(2, 1, 1), 2)
        self.assertEqual(bc.get_global_bin_from_ijk(1, 2, 1), 3)
        self.assertEqual(bc.get_global_bin_from_ijk(1, 1, 2), 5)
        self.assertEqual(bc.get_global_bin_from_ijk(2, 2, 2), 8)
        
    def test_set_bin_contents_1d(self):
        bc = Bin_container(2)
        bc.set_bin_content(1, 3)

    def test_get_ijk_from_global_bin(self):
        # 1D
        bc = Bin_container(20)
        ijk = (5, 1, 1)
        gidx = bc.get_global_bin_from_ijk(*ijk)
        self.assertEqual(bc.get_ijk_from_global_bin(gidx), ijk)

        #2D
        bc = Bin_container(20, 5)
        ijk = (3, 2, 1)
        gidx = bc.get_global_bin_from_ijk(*ijk)
        self.assertEqual(bc.get_ijk_from_global_bin(gidx), ijk)

        #3D
        bc = Bin_container(20, 5, 5)
        ijk = (3, 2, 2)
        gidx = bc.get_global_bin_from_ijk(*ijk)
        self.assertEqual(bc.get_ijk_from_global_bin(gidx), ijk)
