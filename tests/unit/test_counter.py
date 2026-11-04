import unittest

from vision_core import counter

WIDTH, HEIGHT = 1920, 1080


def _valid_line():
  return {
    "id": "gate_a",
    "a": [0.1, 0.6],
    "b": [0.9, 0.6],
    "positive_label": "in",
    "negative_label": "out",
    "deadband_px": 5,
  }


class TestCounter(unittest.TestCase):
  def test_line_counter(self):
    count = counter.LineCounter(_valid_line(), WIDTH, HEIGHT, 500)
    self.assertIsNotNone(count)

  def test_line_constructor(self):
    with self.assertRaises(ValueError):
      counter.LineCounter(_valid_line(), WIDTH, HEIGHT, "500")


if __name__ == "__main__":
  unittest.main()
