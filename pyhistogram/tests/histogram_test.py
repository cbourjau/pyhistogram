from pyhistogram.hist import Hist1D
import unittest


class Test_Hist_1D(unittest.TestCase):
    def test_init_fixed_width(self):
        h = Hist1D(4, 0, 4)
        self.assertEqual(h.Xaxis.get_bin_edges(), [0, 1, 2, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 1.5, 2.5, 3.5])
        self.assertEqual(h.Xaxis.get_number_of_bins(), 4)

    def test_init_variable_width(self):
        h = Hist1D([0, 1, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_edges(), [0, 1, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 2.0, 3.5])
        self.assertEqual(h.Xaxis.get_number_of_bins(), 3)

    def test_fill(self):
        h = Hist1D(4, 0, 4)
        h.fill(2.1)
        self.assertEqual(h.get_bin_contents(), [0, 0, 1, 0])
        
    
