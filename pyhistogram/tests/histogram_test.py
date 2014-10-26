from pyhistogram.hist import Hist
from pyhistogram.utils import UTC
import unittest
from datetime import datetime


class Test_Hist_1D(unittest.TestCase):
    def test_init_fixed_width(self):
        h = Hist(4, 0, 4)
        self.assertEqual(h.Xaxis.get_bin_edges(), [0, 1, 2, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 1.5, 2.5, 3.5])
        self.assertEqual(h.Xaxis.nbins, 4)

        # float sized bins:
        h = Hist(4, 0, 1)
        self.assertEqual(h.Xaxis.get_bin_centers(),
                         [0.125, 0.375, 0.625, 0.875])

    def test_init_variable_width(self):
        h = Hist([0, 1, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_edges(), [0, 1, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 2.0, 3.5])
        self.assertEqual(h.Xaxis.nbins, 3)

    def test_fill_1D(self):
        h = Hist(4, 0, 4)
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
        h = Hist(4, datetime(2014, 1, 1, 12, 0), datetime(2014, 1, 1, 16, 0))
        utc = UTC()
        self.assertEqual(h.Xaxis.get_bin_edges(),
                         [datetime(2014, 1, 1, 12, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 13, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 14, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 15, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 16, 0, tzinfo=utc)])

    def test_hist_creation_with_regex(self):
        h = Hist(['str1', 'str2', 'str3', 'str4'])
        patterns = [r.pattern for r in h.Xaxis.get_bin_regexes()]
        self.assertEqual(patterns, ['str1', 'str2', 'str3', 'str4'])
        failed = False
        # unicode string type
        try: 
            h = Hist([u'str1'])
        except:
            failed = True
        self.assertFalse(failed)

    def test_filling_with_weights(self):
        h = Hist(4, 0, 4)
        h.fill(2.1, weight=2)
        self.assertEqual([b.value for b in h.bins()], [0, 0, 2, 0])
        start, end = datetime(2014, 1, 1, 12, 0), datetime(2014, 1, 1, 16, 0)
        h = Hist(4, start, end)
        h.fill(start, weight=2)
        self.assertEqual([b.value for b in h.bins()], [2, 0, 0, 0])


class Test_Hist_2D(unittest.TestCase):
    def test_init_fixed_width(self):
        h = Hist(4, 0, 4,
                 4, 0, 1)
        self.assertEqual(h.Xaxis.get_bin_edges(), [0, 1, 2, 3, 4])
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 1.5, 2.5, 3.5])
        self.assertEqual(h.Xaxis.nbins, 4)
        self.assertEqual(h.Yaxis.get_bin_centers(), [0.125, 0.375, 0.625, 0.875])
        self.assertEqual(h.Yaxis.nbins, 4)

    def test_integral(self):
        h2d = Hist(4, 0, 1, 4, 0, 1)
        self.assertEqual(h2d.get_integral(), 0)
        h2d.fill(.5, .5)
        self.assertEqual(h2d.get_integral(), 1)
        h2d.fill(.5, .5, weight=3)
        self.assertEqual(h2d.get_integral(), 4)

    def test_projection(self):
        h2d = Hist(4, 0, 1, 5, 0, 1)
        h2d.fill(.5, .5)
        h1d = h2d.get_projection(axis=0)  # along x-axis
        self.assertEqual(h1d.get_shape(), (5,))
        self.assertEqual(h1d.get_integral(), 1)
        h1d = h2d.get_projection(axis=1)  # along y-axis
        self.assertEqual(h1d.get_shape(), (4,))
        self.assertEqual(h1d.get_integral(), 1)


class Test_Hist_3D(unittest.TestCase):
    def test_init_fixed_width(self):
        h = Hist(4, 0, 4,
                 4, 0, 1,
                 4, 0, 1)
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 1.5, 2.5, 3.5])
        self.assertEqual(h.Xaxis.nbins, 4)
        self.assertEqual(h.Yaxis.get_bin_centers(), [0.125, 0.375, 0.625, 0.875])
        self.assertEqual(h.Yaxis.nbins, 4)
        self.assertEqual(h.Zaxis.get_bin_centers(), [0.125, 0.375, 0.625, 0.875])
        self.assertEqual(h.Zaxis.nbins, 4)

    def test_projection(self):
        h3d = Hist(4, 0, 1, 5, 0, 1, 6, 0, 1)
        h3d.fill(.5, .5, .5)
        h2d = h3d.get_projection(axis=0)  # along x-axis
        self.assertEqual(h2d.get_shape(), (5, 6))
        self.assertEqual(h2d.get_integral(), 1)
        h2d = h3d.get_projection(axis=1)  # along y-axis
        self.assertEqual(h2d.get_shape(), (4, 6))
        self.assertEqual(h2d.get_integral(), 1)
        h2d = h3d.get_projection(axis=2)  # along z-axis
        self.assertEqual(h2d.get_shape(), (4, 5))
        self.assertEqual(h2d.get_integral(), 1)

    def test_init_with_fixed_and_variable_bin_sizes(self):
        h = Hist(4, 0, 4,
                 [0, .25, .5, .75, 1],
                 4, 0, 1)
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 1.5, 2.5, 3.5])
        self.assertEqual(h.Xaxis.nbins, 4)
        self.assertEqual(h.Yaxis.get_bin_centers(), [0.125, 0.375, 0.625, 0.875])
        self.assertEqual(h.Yaxis.nbins, 4)
        self.assertEqual(h.Zaxis.get_bin_centers(), [0.125, 0.375, 0.625, 0.875])
        self.assertEqual(h.Zaxis.nbins, 4)

        h = Hist(4, 0, 4,
                 [0, .25, .5, .75, 1],
                 [0, .25, .5, .75, 1])
        self.assertEqual(h.Xaxis.get_bin_centers(), [.5, 1.5, 2.5, 3.5])
        self.assertEqual(h.Xaxis.nbins, 4)
        self.assertEqual(h.Yaxis.get_bin_centers(), [0.125, 0.375, 0.625, 0.875])
        self.assertEqual(h.Yaxis.nbins, 4)
        self.assertEqual(h.Zaxis.get_bin_centers(), [0.125, 0.375, 0.625, 0.875])
        self.assertEqual(h.Zaxis.nbins, 4)

    def test_intit_with_mixed_types_3D(self):
        h = Hist(2, datetime(2014, 1, 1, 12, 0), datetime(2014, 1, 1, 14, 0),
                 ['str1', 'str2', 'str3', 'str4'],
                 4, 0, 1)
        utc = UTC()
        self.assertEqual(h.Xaxis.get_bin_edges(),
                         [datetime(2014, 1, 1, 12, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 13, 0, tzinfo=utc),
                          datetime(2014, 1, 1, 14, 0, tzinfo=utc)])
        v = [r.pattern for r in h.Yaxis.get_bin_regexes()]
        self.assertEqual(v, ['str1', 'str2', 'str3', 'str4'])
        self.assertEqual(h.Zaxis.get_bin_centers(),
                         [0.125, 0.375, 0.625, 0.875])

    def test_fill_with_mixed_types_3D(self):
        h = Hist(2, datetime(2014, 1, 1, 12, 0), datetime(2014, 1, 1, 14, 0),
                 ['str1', 'str2'],
                 2, 0, 1)
        h.fill(x=datetime(2014, 1, 1, 13, 0),
               y='str2', z=0.0)
        # the one filled bin:
        v = [(b.x.low, b.y.regex, b.z.low) for b in h.bins() if b.value==1]
        self.assertEqual(len(v), 1)
        utc = UTC()
        self.assertEqual(v, [(datetime(2014, 1, 1, 13, 0, tzinfo=utc),
                              'str2', 0.0)])

    def test_regex_callable_on_every_bin(self):
        h = Hist(2, datetime(2014, 1, 1, 12, 0), datetime(2014, 1, 1, 14, 0),
                   ['str1', 'str2', 'str3', 'str4'],
                   4, 0, 1)
        try:
            [b.y.regex for b in h.bins()]
        except:
            self.assertTrue(False)


class Test_Hist_compatibilities(unittest.TestCase):
    def test_hists_with_wrong_dimensions(self):
        h1d = Hist(4, 0, 1)
        h2d = Hist(4, 0, 1, 4, 0, 1)
        self.assertRaises(TypeError, h1d.check_compatibility, h2d)
        self.assertRaises(TypeError, h2d.check_compatibility, h1d)

    def test_hists_with_right_dim_wrong_nbins(self):
        h1 = Hist(4, 0, 1)
        h2 = Hist(5, 0, 1)
        self.assertRaises(ValueError, h1.check_compatibility, h2)
        self.assertRaises(ValueError, h2.check_compatibility, h1)

    def test_wrong_dtype(self):
        h1 = Hist(4, 0, 1)
        h2 = Hist(['quite', 'cool', 'regex', 'hist'])
        self.assertRaises(TypeError, h1.check_compatibility, h2)
        self.assertRaises(TypeError, h2.check_compatibility, h1)

    def test_compatible_hists(self):
        h1 = Hist(4, 0, 1, 4, 0, 1)
        h2 = Hist(4, 0, 1, 4, 0, 1)
        nothing_raised = True
        try:
            h1.check_compatibility(h2)
            h2.check_compatibility(h1)
        except:
            nothing_raised = False
        self.assertTrue(nothing_raised)


class Test_bin_iterator(unittest.TestCase):
    def test_bin_iterator_2D(self):
        h = Hist(3, 0, 1, 3, 0, 1)
        self.assertEqual(len([b for b in h.bins()]), 9)
        self.assertEqual([b.x.axis_bin_number for b in h.bins()],
                         [0, 0, 0, 1, 1, 1, 2, 2, 2])
        self.assertEqual([b.y.axis_bin_number for b in h.bins()],
                         [0, 1, 2, 0, 1, 2, 0, 1, 2])

    def test_bin_iterator_3D(self):
        h = Hist(3, 0, 1, 3, 0, 1, 3, 0, 1)
        self.assertEqual(len([b for b in h.bins()]), 27)
        self.assertEqual([b.x.axis_bin_number for b in h.bins()],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0,
                          1, 1, 1, 1, 1, 1, 1, 1, 1,
                          2, 2, 2, 2, 2, 2, 2, 2, 2])
        self.assertEqual([b.y.axis_bin_number for b in h.bins()],
                         [0, 0, 0, 1, 1, 1, 2, 2, 2,
                          0, 0, 0, 1, 1, 1, 2, 2, 2,
                          0, 0, 0, 1, 1, 1, 2, 2, 2])
        self.assertEqual([b.z.axis_bin_number for b in h.bins()],
                         [0, 1, 2, 0, 1, 2, 0, 1, 2,
                          0, 1, 2, 0, 1, 2, 0, 1, 2,
                          0, 1, 2, 0, 1, 2, 0, 1, 2])


class Test_Hist_add(unittest.TestCase):
    def test_1d(self):
        h1 = Hist(2, 0, 1)
        h2 = Hist(2, 0, 1)
        h1.fill(0.3)
        h2.fill(0.6)
        h3 = h1 + h2
        self.assertEqual([b.value for b in h1.bins()], [1, 0])
        self.assertEqual([b.value for b in h2.bins()], [0, 1])
        self.assertEqual([b.value for b in h3.bins()], [1, 1])
        h1 += h2
        self.assertEqual([b.value for b in h1.bins()], [1, 1])

    def test_3d(self):
        h1 = Hist(2, 0, 1, 2, 0, 1, 2, 0, 1)
        h2 = Hist(2, 0, 1, 2, 0, 1, 2, 0, 1)
        h1.fill(0, 0, 0)
        h2.fill(.9, .9, .9)
        h3 = h1 + h2
        h1 += h2
        self.assertEqual([b.value for b in h1.bins()],
                         [b.value for b in h3.bins()])


class Test_Hist_sub(unittest.TestCase):
    def test_1d(self):
        h1 = Hist(2, 0, 1)
        h2 = Hist(2, 0, 1)
        h1.fill(0.3)
        h2.fill(0.6)
        h3 = h1 - h2
        self.assertEqual([b.value for b in h1.bins()], [1, 0])
        self.assertEqual([b.value for b in h2.bins()], [0, 1])
        self.assertEqual([b.value for b in h3.bins()], [1, -1])
        h1 -= h2
        self.assertEqual([b.value for b in h1.bins()], [1, -1])

    def test_3d(self):
        h1 = Hist(2, 0, 1, 2, 0, 1, 2, 0, 1)
        h2 = Hist(2, 0, 1, 2, 0, 1, 2, 0, 1)
        h1.fill(0, 0, 0)
        h2.fill(.9, .9, .9)
        h3 = h1 - h2
        h1 -= h2
        self.assertEqual([b.value for b in h1.bins()],
                         [b.value for b in h3.bins()])


class Test_Hist_mul(unittest.TestCase):
    def test_1d(self):
        h1 = Hist(2, 0, 1)
        h2 = Hist(2, 0, 1)
        h1.fill(0.3, weight=.5)
        h1.fill(0.6, weight=.5)
        h2.fill(0.6, weight=.5)
        h3 = h1 * h2
        self.assertEqual([b.value for b in h1.bins()], [.5, .5])
        self.assertEqual([b.value for b in h2.bins()], [0, .5])
        self.assertEqual([b.value for b in h3.bins()], [0, .25])
        h1 *= h2
        self.assertEqual([b.value for b in h1.bins()], [0, .25])

    def test_3d(self):
        h1 = Hist(2, 0, 1, 2, 0, 1, 2, 0, 1)
        h2 = Hist(2, 0, 1, 2, 0, 1, 2, 0, 1)
        h1.fill(0, 0, 0)
        h2.fill(.9, .9, .9)
        h3 = h1 * h2
        h1 *= h2
        self.assertEqual([b.value for b in h1.bins()],
                         [b.value for b in h3.bins()])


class Test_Hist_div(unittest.TestCase):
    def test_1d(self):
        h1 = Hist(2, 0, 1)
        h2 = Hist(2, 0, 1)
        h1.fill(0.3, weight=.5)
        h1.fill(0.6, weight=.5)
        h2.fill(0.3, weight=.5)
        h2.fill(0.6, weight=.5)
        h3 = h1 / h2
        self.assertEqual([b.value for b in h1.bins()], [.5, .5])
        self.assertEqual([b.value for b in h2.bins()], [.5, .5])
        self.assertEqual([b.value for b in h3.bins()], [1.0, 1.0])
        h1 /= h2
        self.assertEqual([b.value for b in h1.bins()], [1.0, 1.0])

    def test_3d(self):
        h1 = Hist(2, 0, 1, 2, 0, 1, 2, 0, 1)
        h2 = Hist(2, 0, 1, 2, 0, 1, 2, 0, 1)
        for b1, b2 in zip(h1.bins(), h2.bins()):
            b1.value = 2.0
            b2.value = 4.0
        h3 = h1 / h2
        h1 /= h2
        self.assertEqual([b.value for b in h1.bins()],
                         [b.value for b in h3.bins()])
