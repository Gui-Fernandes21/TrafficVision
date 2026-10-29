import math

def cross_product_3d(a: list, b: list) -> list:
    """Calculates the cross product of two 3D vectors."""
    c = [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]
    return c


def side(a: list, b: list, p: list) -> float:
    """
    INPUT: 
      - vector a: list [x, y]
      - vector b: list [x, y]
      - vector p: list [x, y]
    
    Returns the 2D cross product of the vector from a to b and the vector from a to p.
    """
    
    ab = [0, 0]
    ap = [0, 0]

    ab[0] = b[0] - a[0]
    ab[1] = b[1] - a[1]

    ap[0] = p[0] - a[0]
    ap[1] = p[1] - a[1]

    result = (ab[0] * ap[1]) - (ab[1] * ap[0])

    return float(result)

def signed_distance(a: list, b: list, p: list) -> float:
    """
    This returns side(a, b, p) divided by the length of a→b
    """

    cross = side(a, b, p)
    ab_dist = math.hypot(b[0] - a[0], b[1] - a[1])

    if ab_dist == 0:
        raise ValueError

    return cross / ab_dist


def segments_intersect(p1: list, p2: list, q1: list, q2: list) -> bool:
    """
    p1 and p2 are the vectors of the position of a car between two frames
    q1 and q2 are the points of the crossing line.
    
    Check whether p1→p2 crosses q1→q2.
    """
    p1x, p1y = p1[:2]
    q1x, q1y = q1[:2]

    # l = line
    l1x = p2[0] - p1x
    l1y = p2[1] - p1y
    l2x = q2[0] - q1x
    l2y = q2[1] - q1y

    denominator = l1x * l2y - l1y * l2x

    if denominator == 0:
        result = check_overlap(p1,p2,q1,q2)
        return result

    # vector from p1 to q1
    dx = q1x - p1x
    dy = q1y - p1y

    # t	- Position of the intersection along the car’s movement
    # u - Position of the intersection along the crossing line
    t = (dx * l2y - dy * l2x) / denominator
    u = (dx * l1y - dy * l1x) / denominator
    return 0 <= t <= 1 and 0 <= u <= 1


def check_overlap(p1: list, p2: list, q1: list, q2: list) -> bool:
    """Assuming colinear, check if lines overlap"""
    return max(min(p1[0], p2[0]), min(q1[0], q2[0])) <= min(max(p1[0], p2[0]), max(q1[0], q2[0])) and max(
        min(p1[1], p2[1]), min(q1[1], q2[1])) <= min(max(p1[1], p2[1]), max(q1[1], q2[1]))
