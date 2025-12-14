import numpy as np
from app.models.map import MapData


WATER = 0
LAND = 1
MOUNTAIN = 2
SNOW = 3


def classify_terrain(heightmap: np.ndarray) -> np.ndarray:
    terrain = np.zeros_like(heightmap, dtype=np.uint8)

    terrain[heightmap < 0.30] = WATER
    terrain[(heightmap >= 0.30) & (heightmap < 0.60)] = LAND
    terrain[(heightmap >= 0.60) & (heightmap < 0.80)] = MOUNTAIN
    terrain[heightmap >= 0.80] = SNOW

    return terrain
