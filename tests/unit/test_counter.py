import unittest

from vision_core import counter

WIDTH, HEIGHT = 100, 100
MAX_GAP_MS = 1000


def _valid_line():
  return {
    "id": "gate_a",
    "a": [0.1, 0.5],
    "b": [0.9, 0.5],
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

  def test_drives_down_through(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 20], "media_time_ms": 0},
      {"track_id": 1, "point": [50, 40], "media_time_ms": 100},
      {"track_id": 1, "point": [50, 48], "media_time_ms": 200},
      {"track_id": 1, "point": [50, 53], "media_time_ms": 300},
      {"track_id": 1, "point": [50, 70], "media_time_ms": 400},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)

    self.assertEqual(len(counts), 1)
    self.assertEqual(counts[0].get("direction"), "in")
    self.assertEqual(counts[0].get("media_time_ms"), 400)

  def test_drives_up_through(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 80], "media_time_ms": 0},
      {"track_id": 1, "point": [50, 60], "media_time_ms": 100},
      {"track_id": 1, "point": [50, 30], "media_time_ms": 200},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)

    self.assertEqual(len(counts), 1)
    self.assertEqual(counts[0].get("direction"), "out")
    self.assertEqual(counts[0].get("media_time_ms"), 200)

  def test_jitters(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 47], "media_time_ms": 0},
      {"track_id": 1, "point": [50, 52], "media_time_ms": 100},
      {"track_id": 1, "point": [50, 48], "media_time_ms": 200},
      {"track_id": 1, "point": [50, 53], "media_time_ms": 300},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)

    self.assertEqual(len(counts), 0)

  def test_starts_on_line(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 50], "media_time_ms": 0},
      {"track_id": 1, "point": [50, 52], "media_time_ms": 100},
      {"track_id": 1, "point": [50, 70], "media_time_ms": 200},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)
    self.assertEqual(len(counts), 0)

  def test_starts_after_line(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 70], "media_time_ms": 0},
      {"track_id": 1, "point": [50, 80], "media_time_ms": 100},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)
    self.assertEqual(len(counts), 0)

  def test_passes_after_line_end(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [95, 20], "media_time_ms": 0},
      {"track_id": 1, "point": [95, 80], "media_time_ms": 100},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)
    self.assertEqual(len(counts), 0)

  def test_long_gap(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 20], "media_time_ms": 0},
      {"track_id": 1, "point": [50, 80], "media_time_ms": 2000},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)
    self.assertEqual(len(counts), 0)

  def test_edge_of_gap(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 20], "media_time_ms": 0},
      {"track_id": 1, "point": [50, 80], "media_time_ms": 1000},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)

    self.assertEqual(len(counts), 1)
    self.assertEqual(counts[0].get("direction"), "in")
    self.assertEqual(counts[0].get("media_time_ms"), 1000)

  def test_stops_and_crosses(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 20], "media_time_ms": 0},
      {"track_id": 1, "point": [50, 40], "media_time_ms": 100},
    ]

    for i in range(49):
      observations.append(
        {"track_id": 1, "point": [50, 48], "media_time_ms": (100 * i) + 200}
      )

    observations.append({"track_id": 1, "point": [50, 70], "media_time_ms": 5100})

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)

    self.assertEqual(len(counts), 1)
    self.assertEqual(counts[0].get("direction"), "in")
    self.assertEqual(counts[0].get("media_time_ms"), 5100)

  def test_u_turn(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 20], "media_time_ms": 0},
      {"track_id": 1, "point": [50, 40], "media_time_ms": 100},
      {"track_id": 1, "point": [50, 70], "media_time_ms": 200},
      {"track_id": 1, "point": [50, 80], "media_time_ms": 300},
      {"track_id": 1, "point": [50, 60], "media_time_ms": 400},
      {"track_id": 1, "point": [50, 30], "media_time_ms": 500},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)

    self.assertEqual(len(counts), 1)
    self.assertEqual(counts[0].get("direction"), "in")
    self.assertEqual(counts[0].get("media_time_ms"), 200)

  def test_two_tracks(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [30, 20], "media_time_ms": 0},
      {"track_id": 1, "point": [30, 40], "media_time_ms": 100},
      {"track_id": 2, "point": [70, 20], "media_time_ms": 100},
      {"track_id": 1, "point": [30, 70], "media_time_ms": 200},
      {"track_id": 2, "point": [70, 40], "media_time_ms": 200},
      {"track_id": 2, "point": [70, 70], "media_time_ms": 300},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)

    self.assertEqual(len(counts), 2)
    self.assertEqual(counts[0].get("direction"), "in")
    self.assertEqual(counts[0].get("media_time_ms"), 200)
    self.assertEqual(counts[0].get("track_id"), 1)

    self.assertEqual(counts[1].get("direction"), "in")
    self.assertEqual(counts[1].get("media_time_ms"), 300)
    self.assertEqual(counts[1].get("track_id"), 2)

  def test_forget_function(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 20], "media_time_ms": 0},
      {"track_id": 1, "point": [50, 70], "media_time_ms": 100},
      {"track_id": 1, "point": [50, 80], "media_time_ms": 200},
      {"track_id": 1, "point": [50, 30], "media_time_ms": 300},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)
        count.forget(obs["track_id"])

    self.assertEqual(len(counts), 2)
    self.assertEqual(counts[0].get("direction"), "in")
    self.assertEqual(counts[0].get("media_time_ms"), 100)

    self.assertEqual(counts[1].get("direction"), "out")
    self.assertEqual(counts[1].get("media_time_ms"), 300)

  def test_around_end(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 20], "media_time_ms": 0},
      {"track_id": 1, "point": [95, 20], "media_time_ms": 100},
      {"track_id": 1, "point": [95, 80], "media_time_ms": 200},
      {"track_id": 1, "point": [50, 80], "media_time_ms": 300},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)

    self.assertEqual(len(counts), 0)

  def test_counted_u_turn(self):
    line = _valid_line()

    observations = [
      {"track_id": 1, "point": [50, 20], "media_time_ms": 0},
      {"track_id": 1, "point": [95,20], "media_time_ms": 100},
      {"track_id": 1, "point": [95,80], "media_time_ms": 200},
      {"track_id": 1, "point": [50,80], "media_time_ms": 300},
      {"track_id": 1, "point": [50,30], "media_time_ms": 400},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)

    self.assertEqual(len(counts), 1)
    self.assertEqual(counts[0].get("direction"), "out")
    self.assertEqual(counts[0].get("media_time_ms"), 400)
    
  def test_track_id_0(self):
    line = _valid_line()

    observations = [
      {"track_id": 0, "point": [50, 20], "media_time_ms": 0},
      {"track_id": 0, "point": [50,70], "media_time_ms": 100},
    ]

    count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
    counts = []

    for obs in observations:
      res = count.update(obs["track_id"], obs["point"], obs["media_time_ms"])
      if res:
        counts.append(res)

    count.forget(0)
    
    self.assertEqual(len(counts), 1)
    self.assertEqual(counts[0].get("direction"), "in")
    self.assertEqual(counts[0].get("media_time_ms"), 100)
    
  def test_track_id_not_available(self):
    with self.assertRaises(ValueError):      
      line = _valid_line()
      count = counter.LineCounter(line, WIDTH, HEIGHT, 1000)
      count.forget(7)

  def test_max_ms_not_empty(self):
    with self.assertRaises(ValueError):      
      line = _valid_line()
      counter.LineCounter(line, WIDTH, HEIGHT, 0)
    


if __name__ == "__main__":
  unittest.main()
