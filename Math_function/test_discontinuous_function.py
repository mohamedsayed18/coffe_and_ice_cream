import unittest

from discontinuous_function import discontinuous
# TODO naming convenction 
# TODO handle rational numbers
# TODO test fractions

class TestDiscontinuousFunction(unittest.TestCase):
    def test_negative_range(self):
        result = discontinuous(-5)
        self.assertEqual(result, -25)

    def test_in_range_positive(self):
        result = discontinuous(33)
        self.assertEqual(result, 21)
