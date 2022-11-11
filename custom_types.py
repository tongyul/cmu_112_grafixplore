from __future__ import annotations
from typing import Literal

R2 = tuple[float, float]
R3 = tuple[float, float, float]
P3 = R3
R2Pair = tuple[R2, R2]

CoordMode = Literal["absolute", "relative", "display"]
