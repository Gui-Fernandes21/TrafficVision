from vision_core import geometry, lines


class LineCounter:
  def __init__(self, line: dict, width: int, height: int, max_gap_ms):
    self.a_px, self.b_px = lines.line_in_pixels(
      line, width, height
    )  # line_in_pixels is also used to validate the line

    self.line_id = line["id"]
    self.positive_label = line["positive_label"]
    self.negative_label = line["negative_label"]
    self.deadband_px = line["deadband_px"]

    if not type(max_gap_ms) in (int, float) or max_gap_ms < 0:
      raise ValueError("`max_gap_ms` must be an int or float, not a bool, and positive")

    self.max_gap_ms = max_gap_ms

    self._tracks = {}  # track_id -> {"side": ..., "point": ..., "last_seen_ms": ...}
    self._counted = set()  # track_ids already counted on this line

  def update(self, track_id: str, point: list, media_time_ms: int) -> None | dict:
    if type(track_id) != str or len(track_id) < 1:
      raise ValueError("The ID of the track needs to be defined")
    
    track = self._tracks[track_id]
    
    if track is None:
      side_of_track = geometry.signed_distance(self.a_px, self.b_px, point)
      label = None
      
      if side_of_track < 0:
        label = self.positive_label
      elif side_of_track > 0:
        label = self.negative_label
      
      self._tracks[track_id] = {
        "side": label,
        "last_seen_point": point,
        "last_seen_ms": media_time_ms,
      }

    time_gap = track["last_seen_ms"] - media_time_ms

    if time_gap > self.max_gap_ms:
      self.forget(track_id=track_id)
      
  def _compute_labe(self) -> str:
    return ''
    
  def _check_crossed(self) -> bool:
    return False

  def forget(self, track_id: str) -> None:
    if len(track_id) < 1:
      raise ValueError("`track_id` cannot be empty!")

    del self._tracks[track_id]
