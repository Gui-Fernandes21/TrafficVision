import unittest
import math

from vision_core import lines

WIDTH, HEIGHT = 1920, 1080


def valid_line():
    return {
        "id": "gate_a",
        "a": [0.1, 0.6],
        "b": [0.9, 0.6],
        "positive_label": "in",
        "negative_label": "out",
        "deadband_px": 5,
    }


class TestLines(unittest.TestCase):

    def test_validate_lines_valid_input(self):
        input_line = valid_line()
        output = lines.validate_line(input_line)
        self.assertIsNone(output)

    def test_validate_line_missing_key(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            del input_line["b"]
            output = lines.validate_line(input_line)

    def test_validate_line_not_dictionary(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            output = lines.validate_line([*input_line])

    def test_validate_line_invalid_id(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            input_line['id'] = ""
            output = lines.validate_line(input_line)

    def test_validate_line_list_length(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            input_line['a'] = [0.1, 0.2, 0.2]
            output = lines.validate_line(input_line)

    def test_validate_line_valid_int(self):
        input_line = valid_line()
        input_line['b'] = [0.1, 1]
        output = lines.validate_line(input_line)
        self.assertEqual(output, None)

    def test_validate_line_list_type(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            input_line["b"] = [0.1, True]
            output = lines.validate_line(input_line)

    def test_validate_line_list_type_string(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            input_line["b"] = [0.1, "x"]
            output = lines.validate_line(input_line)

    def test_validate_line_list_range(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            input_line["b"] = [0.1, 1.1]
            output = lines.validate_line(input_line)

    def test_validate_line_length(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            input_line['a'] = input_line['b']
            output = lines.validate_line(input_line)

    def test_validate_deadband_type(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            input_line["deadband_px"] = "5"
            output = lines.validate_line(input_line)

    def test_validate_deadband_type_float(self):
        input_line_int = valid_line()
        input_line_int["deadband_px"] = 5

        input_line_float = valid_line()
        input_line_float["deadband_px"] = 2.5

        output_int = lines.validate_line(input_line_int)
        output_float = lines.validate_line(input_line_float)

        self.assertEqual(output_int, None)
        self.assertEqual(output_float, None)

    def test_validate_deadband_range(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            input_line["deadband_px"] = -5
            output = lines.validate_line(input_line)

    def test_validate_line_label_type(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            input_line["positive_label"] = 1
            output = lines.validate_line(input_line)

    def test_validate_line_label_empty(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            input_line["positive_label"] = ''
            output = lines.validate_line(input_line)

    def test_validate_line_same_labels(self):
        with self.assertRaises(ValueError):
            input_line = valid_line()
            input_line['positive_label'] = input_line['negative_label']
            output = lines.validate_line(input_line)

    def test_validate_lines_same_ids(self):
        with self.assertRaises(ValueError):
            input_line1 = valid_line()
            input_line2 = valid_line()
            output = lines.validate_lines([input_line1, input_line2])

    def test_validate_lines_empty(self):
        with self.assertRaises(ValueError):
            output = lines.validate_lines([])

    def test_validate_lines_undefined(self):
        with self.assertRaises((ValueError, TypeError)):
            output = lines.validate_lines()

    def test_validate_lines_type_list(self):
        with self.assertRaises(ValueError):
            input_line1 = valid_line()
            input_line2 = valid_line()
            output = lines.validate_lines((input_line1, input_line2))

    def test_pixels_return(self):
        output = lines.to_pixels([0.1, 0.6], WIDTH, HEIGHT)
        self.assertIsInstance(output, list)

    def test_pixels_range(self):
        with self.assertRaises(ValueError):
            output = lines.to_pixels([0.1, 0.6], -WIDTH, HEIGHT)

    def test_pixels_zero_width(self):
        with self.assertRaises(ValueError):
            lines.to_pixels([0.5, 0.5], 0, HEIGHT)

    def test_pixels_zero_height(self):
        with self.assertRaises(ValueError):
            lines.to_pixels([0.5, 0.5], WIDTH, 0)

    def test_pixels_correct_computation(self):
        output1 = lines.to_pixels([0.1, 0.6], WIDTH, HEIGHT)
        output2 = lines.to_pixels([0.0, 0.0], WIDTH, HEIGHT)
        output3 = lines.to_pixels([1, 1], WIDTH, HEIGHT)

        self.assertEqual(output1, [192.0, 648.0])
        self.assertEqual(output2, [0.0, 0.0])
        self.assertEqual(output3, [1920.0, 1080.0])

    def test_line_in_pixels_output_type(self):
        line = valid_line()
        output = lines.line_in_pixels(line, WIDTH, HEIGHT)
        self.assertIsInstance(output, list)
        self.assertIsInstance(output[0], list)
        self.assertIsInstance(output[1], list)

    def test_line_in_pixels_output_length(self):
        line = valid_line()
        output = lines.line_in_pixels(line, WIDTH, HEIGHT)

        self.assertEqual(len(output), 2)
        self.assertEqual(len(output[0]), 2)
        self.assertEqual(len(output[1]), 2)

    def test_line_in_pixels_output(self):
        line = valid_line()
        line["a"]=[0.1, 0.6]
        line["b"]=[0.9, 0.6]
        a_px, b_px = lines.line_in_pixels(line, WIDTH, HEIGHT)
        self.assertEqual(a_px, [192.0, 648.0])
        self.assertEqual(b_px, [1728.0, 648.0])


if __name__ == "__main__":
    unittest.main()
