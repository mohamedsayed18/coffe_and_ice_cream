import unittest

from discontinuous_function import discontinuous


class TestDiscontinuousFunction(unittest.TestCase):
    def test_out_of_range_negative_raiseError(self):
        with self.assertRaises(ValueError):
            discontinuous(-20)

    def test_first_section(self):
        self.assertEqual(discontinuous(-10), -100)
        self.assertEqual(discontinuous(-6.5), -42.25)
        self.assertEqual(discontinuous(-2), -4)

    def test_mid_section(self):
        self.assertEqual(discontinuous(-1.5), -5)
        self.assertEqual(discontinuous(0), 1)
        self.assertEqual(discontinuous(9), -0.8)

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            discontinuous(-1)

    def test_out_of_range_ten(self):
        with self.assertRaises(ValueError):
            discontinuous(10)

    def test_in_range_positive(self):
        self.assertAlmostEqual(discontinuous(10.1), 1.9, places=1)
        self.assertEqual(discontinuous(25), 13)
        self.assertEqual(discontinuous(35), 23)

    def test_out_of_range_positive_raiseError(self):
        with self.assertRaises(ValueError):
            discontinuous(35.01)
