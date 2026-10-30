import unittest
import sys
import os

# module_path = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "..", "..", "packages", "vision_core")
# )
# sys.path.append(module_path)

from vision_core import geometry

import math


class TestGeometry(unittest.TestCase):

    def test_side_returns_float(self):
        result = geometry.side([0, 0], [10, 0], [5, 5])
        self.assertIsInstance(result, float)

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
        self.assertIsInstance(result, float)

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
        self.assertIsInstance(result, bool)

    def test_segments_clean_intersection(self):
        result = geometry.segments_intersect([5, -5], [5, 5], [0, 0], [10, 0])
        self.assertTrue(result)

    def test_segments_stop_on_line(self):
        result = geometry.segments_intersect([5, -5], [5, 0], [0, 0], [10, 0])
        self.assertTrue(result)

    def test_segments_past_intersection(self):
        result = geometry.segments_intersect([15, -5], [15, 5], [0, 0], [10, 0])
        self.assertFalse(result)

    def test_segments_colinear_not_overlaping(self):
        result = geometry.segments_intersect([12, 0], [20, 0], [0, 0], [10, 0])
        self.assertFalse(result)

    def test_segments_colinear_overlaping(self):
        result = geometry.segments_intersect([5, 0], [15, 0], [0, 0], [10, 0])
        self.assertTrue(result)

    def test_segments_passes_endpoint(self):
        result = geometry.segments_intersect([10, -5], [10, 5], [0, 0], [10, 0])
        self.assertTrue(result)

    def test_segments_zero_on_line(self):
        result = geometry.segments_intersect([5, 0], [5, 0], [0, 0], [10, 0])
        self.assertTrue(result)

    def test_segments_non_overlap_horizontal_line(self):
        result = geometry.segments_intersect([0, 1], [10, 11], [0, 0], [10, 10])
        self.assertFalse(result)

    def test_segments_horizontal_line_not_touch(self):
        result = geometry.segments_intersect([5, 1], [5, 1], [0, 0], [10, 10])
        self.assertFalse(result)                                              

    def test_segments_horizontal_line_not_touch_swapped(self):
        with self.assertRaises(ValueError):
            result = geometry.segments_intersect([0, 0], [10, 10], [5, 1], [5, 1])


if __name__ == "__main__":
    unittest.main()
