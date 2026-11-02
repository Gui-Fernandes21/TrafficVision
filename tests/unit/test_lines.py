import unittest
import math

from vision_core import lines

WIDTH, HEIGHT = 1920, 1080
class TestLines(unittest.TestCase):

    def test_validate_lines_valid_input(self):
        input_line = {
            "id": "gate_a",
            "a": [0.1, 0.6],
            "b": [0.9, 0.5],
            "positive_label": "in",
            "negative_label": "out",
            "deadband_px": 5,
        }
        output = lines.validate_line(input_line)
        self.assertIsNone(output)

    def test_validate_lines_missing_key(self):
        with self.assertRaises(ValueError):
            input_line = {
            "id": "gate_a",
            "a": [0.1, 0.6],
            "positive_label": "in",
            "negative_label": "out",
            "deadband_px": 5,
        }
            output = lines.validate_line(input_line)

    def test_validate_lines_invalid_id(self):
        with self.assertRaises(ValueError):
            input_line = {
                "id": "",
                "a": [0.1, 0.6],
                "b": [0.1, 0.6],
                "positive_label": "in",
                "negative_label": "out",
                "deadband_px": 5,
            }
            output = lines.validate_line(input_line)

    def test_validate_lines_list_length(self):
        with self.assertRaises(ValueError):
            input_line = {
                "id": "someid",
                "a": [0.1, 0.2, 0.2],
                "b": [0.1, 0.2],
                "positive_label": "in",
                "negative_label": "out",
                "deadband_px": 5,
            }
            output = lines.validate_line(input_line)

    def test_validate_lines_list_type(self):
        with self.assertRaises(ValueError):
            input_line = {
                "id": "someid",
                "a": [0.1, 0.2],
                "b": [0.1, 1],
                "positive_label": "in",
                "negative_label": "out",
                "deadband_px": 5,
            }
            output = lines.validate_line(input_line)

    def test_validate_lines_list_type_string(self):
        with self.assertRaises(ValueError):
            input_line = {
                "id": "someid",
                "a": [0.1, 0.2],
                "b": [0.1, "x"],
                "positive_label": "in",
                "negative_label": "out",
                "deadband_px": 5,
            }
            output = lines.validate_line(input_line)

    def test_validate_lines_list_range(self):
        with self.assertRaises(ValueError):
            input_line = {
                "id": "someid",
                "a": [0.1, 0.2],
                "b": [0.1, 1.1],
                "positive_label": "in",
                "negative_label": "out",
                "deadband_px": 5,
            }
            output = lines.validate_line(input_line)

    def test_validate_lines_length(self):
        with self.assertRaises(ValueError):
            input_line = {
                "id": "someid",
                "a": [0.1, 0.2],
                "b": [0.1, 0.2],
                "positive_label": "in",
                "negative_label": "out",
                "deadband_px": 5,
            }
            output = lines.validate_line(input_line)

    def test_validate_deadband_type(self):
        with self.assertRaises(ValueError):
            input_line = {
                "id": "someid",
                "a": [0.1, 0.2],
                "b": [0.1, 0.34],
                "positive_label": "in",
                "negative_label": "out",
                "deadband_px": "5",
            }
            output = lines.validate_line(input_line)

    def test_validate_deadband_range(self):
        with self.assertRaises(ValueError):
            input_line = {
                "id": "someid",
                "a": [0.1, 0.2],
                "b": [0.1, 0.34],
                "positive_label": "in",
                "negative_label": "out",
                "deadband_px": -5,
            }
            output = lines.validate_line(input_line)

    def test_validate_line_not_supported_labels(self):
        with self.assertRaises(ValueError):
            input_line = {
                "id": "someid",
                "a": [0.1, 0.2],
                "b": [0.5, 0.9],
                "positive_label": "out",
                "negative_label": "ontop",
                "deadband_px": 5,
            }
            output = lines.validate_line(input_line)

    def test_validate_line_same_labels(self):
        with self.assertRaises(ValueError):
            input_line = {
                "id": "someid",
                "a": [0.1, 0.2],
                "b": [0.5, 0.9],
                "positive_label": "in",
                "negative_label": "in",
                "deadband_px": 5,
            }
            output = lines.validate_line(input_line)

    def test_pixels_return(self):
        output = lines.to_pixels([0.1, 0.6], WIDTH, HEIGHT)
        self.assertIsInstance(output, list)

    def test_pixels_range(self):
        with self.assertRaises(ValueError):
            output = lines.to_pixels([0.1, 0.6], -WIDTH, HEIGHT)

    def test_pixels_correct_computation(self):
        output1 = lines.to_pixels([0.1, 0.6], WIDTH, HEIGHT)
        output2 = lines.to_pixels([0.0, 0.0], 0, 0)
        output3 = lines.to_pixels([1, 1], WIDTH, HEIGHT)

        self.assertEqual(output1, [192.0, 648.0])
        self.assertEqual(output2, [0.0, 0.0])
        self.assertEqual(output3, [1920.0, 1080.0])

    def test_line_in_pixels_output_type(self):
        line = {
            "id": "some_id",
            "a": [0.1, 0.6],
            "b": [0.9, 0.6],
            "positive_label": "in",
            "negative_label": "out",
            "deadband_px": 5,
        }
        output = lines.line_in_pixels(line, WIDTH, HEIGHT)
        self.assertIsInstance(output, list)
        self.assertIsInstance(output[0], list)
        self.assertIsInstance(output[1], list)

    def test_line_in_pixels_output_length(self):
        line = {
            "id": "some_id",
            "a": [0.1, 0.6],
            "b": [0.9, 0.6],
            "positive_label": "in",
            "negative_label": "out",
            "deadband_px": 5,
        }
        output = lines.line_in_pixels(line, WIDTH, HEIGHT)

        self.assertEqual(len(output), 2)
        self.assertEqual(len(output[0]), 2)
        self.assertEqual(len(output[1]), 2)

    def test_line_in_pixels_output(self):
        line = {
            "id": "some_id",
            "a": [0.1, 0.6],
            "b": [0.9, 0.6],
            "positive_label": "in",
            "negative_label": "out",
            "deadband_px": 5,
        }
        a_px, b_px = lines.line_in_pixels(line, WIDTH, HEIGHT)
        self.assertEqual(a_px, [192.0, 648.0])
        self.assertEqual(b_px, [1728.0, 648.0])


if __name__ == "__main__":
    unittest.main()
