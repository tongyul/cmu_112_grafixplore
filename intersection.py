from __future__ import annotations
from custom_types import R2, P3, R2Pair

def floatNear(a: float, b: float, epsilon: float) -> bool:
    return abs(a - b) <= epsilon

def p3FromR2(x: R2) -> P3:
    return x + (1,)

r2ToP3 = p3FromR2  # alias

def r2FromP3(x: P3) -> R2 | None:
    x1,x2,x3 = x
    if floatNear(x3, 0, 1E-10): return None
    return (x1/x3, x2/x3)

p3ToR2 = r2FromP3  # alias

def subR2(a: R2, b: R2) -> R2:
    a1,a2 = a
    b1,b2 = b
    return (a1 - b1, a2 - b2)

def dotR2(a: R2, b: R2) -> float:
    a1,a2 = a
    b1,b2 = b
    return a1*b1 + a2*b2

def scaleR2(a: R2, scalar: float) -> R2:
    a1,a2 = a
    return (a1*scalar, a2*scalar)

def crossP3(a: P3, b: P3) -> P3:
    a1,a2,a3 = a
    b1,b2,b3 = b
    # c = a x b
    c1 = a2*b3 - a3*b2
    c2 = a3*b1 - a1*b3
    c3 = a1*b2 - a2*b1
    return (c1,c2,c3)

def intersection(line1: R2Pair, line2: R2Pair) -> R2 | None:
    # takes line1, line2 as pairs of R2 coords; returns intersection point in R2
    return r2FromP3(crossP3(
        crossP3(*map(p3FromR2, line1)),
        crossP3(*map(p3FromR2, line2)),
    ))

def projCoefR2(a: R2, b: R2) -> float:
    # given R2 vectors a and b, returns x̂ = a⋅b / a⋅a
    return dotR2(a, b) / dotR2(a, a)

def projectionR2(a: R2, b: R2) -> R2:
    # given R2 vectors a and b, returns x̂a (see `projCoefR2`)
    return scaleR2(a, projCoefR2(a, b))

def pathSegCollision(path: R2Pair, seg: R2Pair) -> float | None:
    # similar to `intersection`, but returns the position of intersection
    # relative to the length of `path` if there is intersection, otherwise None
    # e.g.
    # intersection( ((0,1),(5,1)), ((2,0),(2,3)) ) == (2,1)
    # pathSegCollision( ((0,1),(5,1)), ((2,0),(2,3)) ) == 0.4
    inter = intersection(path, seg)
    if inter is None: return None

    pathStart, pathEnd = path
    segStart, segEnd = seg
    positionOnPath = projCoefR2(
        subR2(pathEnd, pathStart), subR2(inter, pathStart))
    positionOnSeg = projCoefR2(
        subR2(segEnd, segStart), subR2(inter, segStart))

    if (0.0 <= positionOnPath <= 1.0) and (0.0 <= positionOnSeg <= 1.0):
        return positionOnPath
    else:
        return None
