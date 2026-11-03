import unittest

from vision_core import counter, lines


class TestCounter(unittest.TestCase):
  def test_line_counter(self):
    count = counter.LineCounter(lines.line_in_pixels)
    self.assertEqual(count, True)


if __name__ == "__main__":
  unittest.main()
