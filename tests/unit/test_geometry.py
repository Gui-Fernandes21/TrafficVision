import unittest
import sys
import os

module_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "packages", "vision_core")
)
sys.path.append(module_path)

import geometry


class TestGeometry(unittest.TestCase):

    def test_side_returns_float(self):
        result = geometry.side([0, 0], [10, 0], [5, 5])
        self.assertEqual(type(result), float)

    def test_side_correct_positive(self):
        result = geometry.side([0, 0], [10, 0], [5, 5])
        self.assertEqual(result, float(50))

    def test_side_correct_negative(self):
        result = geometry.side([0, 0], [10, 0], [5, -5])
        self.assertEqual(result, float(-50))

    def test_side_correct_zero(self):
        result = geometry.side([0, 0], [10, 0], [20, 0])
        self.assertEqual(result, float(0))

    def test_side_correct_swap(self):
        result = geometry.side([0, 0], [10, 0], [5, 5])
        result_swapped = geometry.side([10, 0], [0, 0], [5, 5])
        self.assertEqual(result_swapped, -result)

    def test_signed(self):
        result = geometry.signed_distance([0, 0], [10, 0], [5, 5])
        self.assertEqual(type(result), float)


if __name__ == "__main__":
    unittest.main()
