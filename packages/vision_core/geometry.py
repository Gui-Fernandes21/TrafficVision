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
    px, py = p1[:2]
    qx, qy = q1[:2]

    rx = p2[0] - px
    ry = p2[1] - py
    sx = q2[0] - qx
    sy = q2[1] - qy

    denominator = rx * sy - ry * sx

    if denominator == 0:
        print('lines are parallel')
        return False

    dx = qx - px
    dy = qy - py

    t = (dx * sy - dy * sx) / denominator
    u = (dx * ry - dy * rx) / denominator

    return 0 <= t <= 1 and 0 <= u <= 1
