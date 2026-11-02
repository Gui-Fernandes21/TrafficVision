from enum import Enum
import math

class labels(Enum):
    IN = "in"
    OUT = "out"

def validate_line(line: dict) -> None | ValueError:
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
            raise ValueError(f'Missing Key ${att}')

    if line['id'] == "" or not isinstance(line['id'], str):
        raise ValueError(f"id has to be a string and cannot be empty")

    point_a, point_b = list(line["a"]), list(line["b"])

    if len(point_a) != 2 or len(point_b) != 2:
        raise ValueError('points a and b need to have 2 coordinates')

    if not all(isinstance(coord, float) for coord in point_a + point_b):
        raise ValueError("coordinates need to be all floats")

    if not all(coord >= 0.0 and coord <= 1.0 for coord in point_a+point_b):
        raise ValueError("coordinates need to be in range 0 to 1")

    if point_a == point_b:
        raise ValueError("The line has zero length")

    if type(line["deadband_px"]) is not int or line['deadband_px'] < 0:
        raise ValueError("deadband_px is negative or not a number")

    if line["positive_label"] not in labels or line["negative_label"] not in labels:
        raise ValueError('Label unsupported')

    if line["positive_label"] == line["negative_label"]:
        raise ValueError("Labels cannot be the same")


def to_pixels(point: list, width: float, height: float):
    return


def line_in_pixels(line: list, width: float, height: float):
    return
