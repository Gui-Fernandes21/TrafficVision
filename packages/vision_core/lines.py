import math


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
          raise ValueError('Missing Key')

    return


def to_pixels(point: list, width: float, height: float):
    return


def line_in_pixels(line: list, width: float, height: float):
    return
