from __future__ import annotations
from pathlib import Path
from typing import Final


PROJDIR: Final = Path(__file__).resolve().parent
RCSDIR: Final = PROJDIR/'resources'
TXRDIR: Final = RCSDIR/'textures'
MAPDIR: Final = RCSDIR/'maps'
