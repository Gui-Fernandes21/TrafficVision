import math


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
    
    return 0.0

def distance(a: list, b: list) -> float:
    return 0.0