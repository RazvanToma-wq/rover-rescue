import numpy as np


def generate_heightmap(
    width: int,
    height: int,
    seed: int | None = None
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    heightmap = rng.random((height, width), dtype=np.float32)
    return heightmap
