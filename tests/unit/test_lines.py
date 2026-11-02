import unittest
import math

from vision_core import lines

class TestLines(unittest.TestCase):
    # SKELETON
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



if __name__ == '__main__': 
 unittest.main() 
