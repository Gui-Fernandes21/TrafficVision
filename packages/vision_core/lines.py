from enum import Enum
import math


def validate_line(line: dict) -> None:
    line_attributes = [
        "id",
        "a",
        "b",
        "positive_label",
        "negative_label",
        "deadband_px",
    ]

    for i, att in enumerate(line_attributes):
        contain = line.__contains__(line_attributes[i])

        if not contain:
            raise ValueError(f"Missing Key {att}")

    if line["id"] == "" or not isinstance(line["id"], str):
        raise ValueError("id has to be a string and cannot be empty")
      
    if not isinstance(line['a'], list) or not isinstance(line['b'], list):
        raise ValueError('point a and b need to be lists')
      
    point_a, point_b = list(line["a"]), list(line["b"])

    if len(point_a) != 2 or len(point_b) != 2:
        raise ValueError("points a and b need to have 2 coordinates")

    if not all(type(coord) in (float, int) for coord in point_a + point_b):
        raise ValueError("coordinates need to be a float or a integer")

    if not all(coord >= 0.0 and coord <= 1.0 for coord in point_a + point_b):
        raise ValueError("coordinates need to be in range 0 to 1")

    if point_a == point_b:
        raise ValueError("The line has zero length")

    if type(line["deadband_px"]) not in (float, int) or line["deadband_px"] < 0:
        raise ValueError("deadband_px is negative or not a number")

    if not isinstance(line["positive_label"], str) or not isinstance(line["negative_label"], str):
        raise ValueError("Labels must be strings")

    if len(line["positive_label"]) < 1 or len(line["negative_label"]) < 1:
        raise ValueError("Labels must not be empty")

    if line["positive_label"] == line["negative_label"]:
        raise ValueError("Labels cannot be the same")


def validate_lines(lines: [dict]) -> None:
    if not isinstance(lines, list) or len(lines) < 1:
        raise ValueError('lines should be a list and cannot be empty')

    for line in lines:
        validate_line(line)
    
    unique_ids = {line["id"] for line in lines}

    if len(unique_ids) != len(lines):
        raise ValueError("Line IDs must be unique")


def to_pixels(point: list, width: float, height: float) -> list:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive, got {} x {}".format(width, height))

    output = [point[0] * width, point[1] * height]
    return output


def line_in_pixels(line: dict, width: float, height: float) -> list:
    validate_line(line)

    a_px = to_pixels(line["a"], width, height)
    b_px = to_pixels(line["b"], width, height)

    return [a_px, b_px]
