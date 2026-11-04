from vision_core import lines


class LineCounter:
  def __init__(self, line: dict, width: int, height: int, max_gap_ms):
    lines.validate_line(line)
    
    self.line_id = line['id']
    self.positive_label = line['positive_label']
    self.negative_label = line['negative_label']
    self.deadband_px = line['deadband_px']
    
    self.line_coords = lines.line_in_pixels(line, width, height)

    if not type(max_gap_ms) in (int, float) or max_gap_ms < 0:
      raise ValueError("`max_gap_ms` must be an int or float, not a bool, and positive")

    self.max_gap_ms = max_gap_ms

    self._tracks = {}  # track_id -> {"side": ..., "point": ..., "last_seen_ms": ...}
    self._counted = set()  # track_ids already counted on this line

  def update(track_id: str, point: list, media_time_ms: int) -> None | dict:

    return
  
  def forget(track_id: str) -> None:
    
    return
