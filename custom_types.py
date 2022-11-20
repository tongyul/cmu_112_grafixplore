from __future__ import annotations
from typing import Literal

R2 = tuple[float, float]
R3 = tuple[float, float, float]
P3 = R3
R2Pair = tuple[R2, R2]

CoordMode = Literal["absolute", "relative", "display"]
# to be used with a grid coordinate system;
# - absolute: return absolute coordinates relative to world origin
# - relative: return relative coordinates, in case global coordinates are
#   subject to floating point imprecision (reserved)
# - display: return coordinate relative to camera? then we'll need a camera
