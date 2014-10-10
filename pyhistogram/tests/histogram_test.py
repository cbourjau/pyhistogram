from pyhistogram.hist import Hist1D
import unittest


class Test_Hist_1D(unittest.TestCase):
    def test_init_fixed_width(self):
        h = Hist1D(4, 0, 4)
        self.assertEqual(h.Xaxis.get_bin_edges(), [0, 1, 2, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 1.5, 2.5, 3.5])
        self.assertEqual(h.Xaxis.get_number_of_bins(), 4)

        # float sized bins:
        h = Hist1D(4, 0, 1)
        self.assertEqual(h.Xaxis.get_bin_centers(), [0.125, 0.375, 0.625, 0.875])
        

    def test_init_variable_width(self):
        h = Hist1D([0, 1, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_edges(), [0, 1, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 2.0, 3.5])
        self.assertEqual(h.Xaxis.get_number_of_bins(), 3)

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
