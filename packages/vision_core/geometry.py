import math

def side(a: list, b: list, p: list) -> float:
    """
    INPUT:
      - point a: list [x, y]
      - point b: list [x, y]
      - point p: list [x, y]

    Returns the 2D cross product of the vector from a to b and the vector from a to p.

    Output meaning:
        1. Positive means to the right of a→b on screen, because y points down.
        2. 0 means that p lies on the infinite line though 'a' and 'b' and possibily beyond its ends. 
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
    
    Output meaning:
        1. Positive means to the right of a→b on screen, because y points down.
    """

    cross = side(a, b, p)
    ab_dist = math.hypot(b[0] - a[0], b[1] - a[1])

    if ab_dist == 0:
        raise ValueError('ab needs to be a real line with length')

    return cross / ab_dist


def segments_intersect(p1: list, p2: list, q1: list, q2: list) -> bool:
    """
    p1 and p2 are the points of the position of a car between two frames
    q1 and q2 are the points of the crossing line.

    Check whether p1→p2 crosses q1→q2.

    q1 and q2 must be a real line not a single point

    Denominator being 0 means it's touching the line collinear overlap count as intersecting.
    Touching an endpoint also counts as a intersection not just collinear overlap.
    """

    if q1[0] == q2[0] and q1[1] == q2[1]:
        raise ValueError("q1 and q2 must be a real line not a single point")

    p1x, p1y = p1[:2]
    q1x, q1y = q1[:2]

    # l = line
    l1x = p2[0] - p1x
    l1y = p2[1] - p1y
    l2x = q2[0] - q1x
    l2y = q2[1] - q1y

    denominator = l1x * l2y - l1y * l2x

    if denominator == 0:
        p1_side = side(q1, q2, p1)
        p2_side = side(q1, q2, p2)

        if p1_side == 0 and p2_side == 0:
            result = _check_overlap(p1, p2, q1, q2)
            return result

        return False

    # vector from p1 to q1
    dx = q1x - p1x
    dy = q1y - p1y

    # t	- Position of the intersection along the car’s movement
    # u - Position of the intersection along the crossing line
    t = (dx * l2y - dy * l2x) / denominator
    u = (dx * l1y - dy * l1x) / denominator
    return 0 <= t <= 1 and 0 <= u <= 1


def _check_overlap(p1: list, p2: list, q1: list, q2: list) -> bool:
    """Assuming colinear, check if lines overlap"""
    return max(min(p1[0], p2[0]), min(q1[0], q2[0])) <= min(max(p1[0], p2[0]), max(q1[0], q2[0])) and max(
        min(p1[1], p2[1]), min(q1[1], q2[1])) <= min(max(p1[1], p2[1]), max(q1[1], q2[1]))
