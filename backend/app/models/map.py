from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class MapData:
    width: int
    height: int
    terrain: np.ndarray
    heightmap: np.ndarray
