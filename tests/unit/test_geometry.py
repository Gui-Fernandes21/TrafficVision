import unittest
import sys
import os

module_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "packages", "vision_core")
)
sys.path.append(module_path)

import geometry
import math

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

    def test_signed_type(self):
        result = geometry.signed_distance([0, 0], [10, 0], [5, 5])
        self.assertEqual(type(result), float)

    def test_signed_division_by_zero(self):
        with self.assertRaises(ValueError):
            result = geometry.signed_distance([10, 0], [10, 0], [5, 5])

    def test_signed_output_1(self):
        result = geometry.signed_distance([0, 0], [10, 0], [5, 5])
        self.assertEqual(result, 5.0)

    def test_signed_output_diff_length(self):
        result = geometry.signed_distance([0, 0], [100, 0], [5, 5])
        self.assertEqual(result, 5.0)

    def test_signed_output_2(self):
        result = geometry.signed_distance([0, 0], [10, 10], [10, 0])
        self.assertAlmostEqual(result, -5 * math.sqrt(2))

    def test_signed_on_line(self):
        result = geometry.signed_distance([0, 0], [10, 0], [5, 0])
        self.assertAlmostEqual(result, 0)

    def test_signed_on_line_not_intersect(self):
        result = geometry.signed_distance([0, 0], [10, 0], [15, 0])
        self.assertAlmostEqual(result, 0)

    def test_segments_return_type(self):
        result = geometry.segments_intersect([0, 0], [0, 0], [10, 0], [5, 5])
        self.assertEqual(type(result), bool)

    def test_segments_clean_intersection(self):
        result = geometry.segments_intersect([5, -5], [5, 5], [0, 0], [10, 0])
        self.assertEqual(result, True)

    def test_segments_stop_on_line(self):
        result = geometry.segments_intersect([5, -5], [5, 0], [0, 0], [10, 0])
        self.assertEqual(result, True)

    def test_segments_past_intersection(self):
        result = geometry.segments_intersect([15, -5], [15, 5], [0, 0], [10, 0])
        self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
