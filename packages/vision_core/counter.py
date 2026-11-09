import typing

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

    if not type(max_gap_ms) in (int, float) or max_gap_ms <= 0:
      raise ValueError("`max_gap_ms` must be an int or float, not a bool, and positive")

    self.max_gap_ms = max_gap_ms

    self._tracks = {}  # track_id -> {"side": ..., "point": ..., "last_seen_ms": ...}
    self._counted = set()  # track_ids already counted on this line

  def update(self, track_id: int, point: list, media_time_ms: int) -> typing.Optional[dict]: # noqa
    """
    Checks if time gap exceeds and resets the _tracks[track_id].

    Tracks can only cross the line ONCE.

    Labeling logic
      1. Only attribute labels if track goes past the deadband.
      2. If label was None and changes to a positive or negative label, should not count.
      3. If Label existed and is now currently None, do not update label.
      4. Count as crossing if label was defined and now is changing to the opposite label.
    """
    
    # -------------------------------------------------------------------------
    # Defensive coding check
    # -------------------------------------------------------------------------
    if type(track_id) != int:
      raise TypeError("The ID needs to be an integer")

    # -------------------------------------------------------------------------
    # Calculating the distance 
    # Extracting the track from the list of tracks
    # -------------------------------------------------------------------------

    track = self._tracks.get(track_id)
    dist = geometry.signed_distance(self.a_px, self.b_px, point)
    is_outside_band = (dist > self.deadband_px or dist < -self.deadband_px)
    
    # -------------------------------------------------------------------------
    # If NEW track, just create one and return None
    # -------------------------------------------------------------------------
    direction = self._compute_label(dist)

    if track is None:
      self._tracks[track_id] = {
        "side": direction,
        "last_seen_point": point,
        "last_seen_ms": media_time_ms,
      }
      return

    # -------------------------------------------------------------------------
    # Check if time gap exceeds the limit, and reset if it does and returns.
    # -------------------------------------------------------------------------
    time_gap = media_time_ms - track["last_seen_ms"]
    
    if time_gap > self.max_gap_ms:
      del self._tracks[track_id]
      
      self._tracks[track_id] = {
        "side": direction,
        "last_seen_point": point,
        "last_seen_ms": media_time_ms,
      }
      return

    # -------------------------------------------------------------------------
    # only update ms INSIDE of the deadband
    # -------------------------------------------------------------------------
    if not is_outside_band:
      track['last_seen_ms'] = media_time_ms
      return 
    
    # -------------------------------------------------------------------------
    # check for collision and track is outside of the deadband
    # -------------------------------------------------------------------------
    print(track['side'],track['last_seen_point'], dist)
    if is_outside_band:
      # If there's no side, that means that the track was 'born' inside the deadband
      if track["side"] == None:
        self._tracks[track_id] = {
          "side": direction,
          "last_seen_point": point,
          "last_seen_ms": media_time_ms,
        }
        return
      
      # Check if the side has changed since the last stable side
      # Check if track has not already been counted for this line
      if track['side'] != direction and track_id not in self._counted:
        intersect = geometry.segments_intersect(point, track["last_seen_point"], self.a_px, self.b_px)
        
        if intersect:
          self._counted.add(track_id) 
          self._tracks[track_id] = { 
            "side": direction, 
            "last_seen_point": point,  
            "last_seen_ms": media_time_ms, 
          }
          
          return {
            "track_id": track_id, 
            "line_id": self.line_id, 
            "direction": direction, 
            "media_time_ms": media_time_ms,
          }
    track['side'] = direction
    track['last_seen_point'] = point
        
  def forget(self, track_id: int) -> None:
    if track_id < 0:
      raise ValueError("input a valid `track_id`!")
    
    if track_id > len(self._tracks):
      raise ValueError('Out of Range `track_id`')

    if type(track_id) != int:
      raise TypeError('`track_id` needs to be an integer')
    
    del self._tracks[track_id]
    self._counted.discard(track_id)

  def _compute_label(self, dist: float) -> str:
    label = None

    if dist < -self.deadband_px:
      label = self.negative_label
    elif dist > self.deadband_px:
      label = self.positive_label

    return label
