import unittest
import math

from vision_core import lines

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

    def test_validate_lines_list_contents(self):
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


if __name__ == '__main__': 
 unittest.main() 
