from fastapi import APIRouter
import random
import math

router = APIRouter()

# Biome IDs (frontend-friendly)
WATER = 0
SAND = 1
GRASS = 2
HILL = 3
MOUNTAIN = 4
SNOW = 5


# -------------------------------------------------
# Fast deterministic hash noise
# -------------------------------------------------

def _hash2i(ix: int, iy: int, seed: int) -> float:
    n = ix * 374761393 + iy * 668265263 + seed * 1442695041
    n = (n ^ (n >> 13)) * 1274126177
    n = n ^ (n >> 16)
    return (n & 0xFFFFFFFF) / 4294967296.0


def _smoothstep(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)


def value_noise_2d(x: float, y: float, seed: int) -> float:
    x0 = int(x)
    y0 = int(y)
    x1 = x0 + 1
    y1 = y0 + 1

    sx = _smoothstep(x - x0)
    sy = _smoothstep(y - y0)

    n00 = _hash2i(x0, y0, seed)
    n10 = _hash2i(x1, y0, seed)
    n01 = _hash2i(x0, y1, seed)
    n11 = _hash2i(x1, y1, seed)

    ix0 = n00 + (n10 - n00) * sx
    ix1 = n01 + (n11 - n01) * sx
    return ix0 + (ix1 - ix0) * sy


def fbm(x: float, y: float, seed: int, octaves: int, lacunarity=2.0, gain=0.5) -> float:
    value = 0.0
    amp = 1.0
    freq = 1.0
    max_amp = 0.0

    for _ in range(octaves):
        value += value_noise_2d(x * freq, y * freq, seed) * amp
        max_amp += amp
        amp *= gain
        freq *= lacunarity

    return value / max_amp


def rolling_hills(x: float, y: float, seed: int) -> float:
    return fbm(x * 0.6, y * 0.6, seed + 77, octaves=2)


def ridged(x: float, y: float, seed: int) -> float:
    n = fbm(x, y, seed, octaves=4)
    n = 1.0 - abs(2.0 * n - 1.0)
    return n * n


def smooth_range(edge0: float, edge1: float, x: float) -> float:
    if edge0 == edge1:
        return 0.0
    t = (x - edge0) / (edge1 - edge0)
    t = max(0.0, min(1.0, t))
    return _smoothstep(t)


# -------------------------------------------------
# Hill mask (creates hill-only regions)
# -------------------------------------------------

def hill_mask(nx: float, ny: float, seed: int) -> float:
    return fbm(nx * 0.9, ny * 0.9, seed + 999, octaves=2)


# -------------------------------------------------
# TerraForge-style height
# -------------------------------------------------

def terraforge_height(nx: float, ny: float, seed: int) -> float:
    wx = nx + (fbm(nx * 2.0, ny * 2.0, seed + 101, 2) - 0.5) * 0.30
    wy = ny + (fbm(nx * 2.0, ny * 2.0, seed + 202, 2) - 0.5) * 0.30

    cont = fbm(wx * 0.75, wy * 0.75, seed + 1, 3)
    cont = smooth_range(0.45, 0.72, cont)

    if cont <= 0.0:
        return 0.0

    elev = fbm(wx * 3.0, wy * 3.0, seed + 2, 4)
    hills = rolling_hills(wx, wy, seed)
    mtn = ridged(wx * 2.2, wy * 2.2, seed + 3)

    peak_boost = smooth_range(0.65, 0.85, mtn)
    mtn = min(1.0, mtn + peak_boost * 0.25)

    hmask = hill_mask(wx, wy, seed)
    hill_boost = smooth_range(0.45, 0.75, hmask) * 0.25

    land = (
        0.40 * elev +
        0.30 * hills +
        0.30 * mtn +
        hill_boost
    )

    return max(0.0, min(1.0, cont * land))


# -------------------------------------------------
# FAST MAP GENERATION (CACHED + SAMPLED)
# -------------------------------------------------

_MAP_CACHE = {}
@router.get("/map/generate")
def generate_map(width: int =1600, height: int = 900, seed: int | None = None):
    if seed is None:
        seed = random.randint(0, 10_000_000)

    # Hard clamp to prevent accidental huge requests
    width = max(32, min(width, 600))
    height = max(32, min(height, 600))

    cache_key = (width, height, seed)
    if cache_key in _MAP_CACHE:
        return _MAP_CACHE[cache_key]

    # ---- COARSE PASS (speed) ----
    # Generate at lower resolution, then upscale to requested size.
    step = max(1, min(width, height) // 140)  # ~140x140 work budget
    cw = (width + step - 1) // step
    ch = (height + step - 1) // step

    inv_w = 1.0 / cw
    inv_h = 1.0 / ch
    scale = 4.0

    total = cw * ch

    # ---- TARGET RATIOS (same as your intent) ----
    WATER_RATIO = 0.25
    GRASS_RATIO = 0.40
    HILL_RATIO_OF_GRASS = 0.15
    HILL_RATIO = GRASS_RATIO * HILL_RATIO_OF_GRASS
    MOUNTAIN_RATIO = HILL_RATIO * 0.35
    SNOW_RATIO = MOUNTAIN_RATIO * 0.15

    # ---- SAMPLE HEIGHTS (on coarse grid) ----
    sampled_land = []
    for y in range(ch):
        ny = y * inv_h
        for x in range(cw):
            nx = x * inv_w
            h = terraforge_height(nx * scale, ny * scale, seed)
            if h > 0.0:
                sampled_land.append(h)

    sampled_land.sort()
    if not sampled_land:
        sampled_land = [0.01]

    land_est = int((1.0 - WATER_RATIO) * total) or 1

    def idx(r):
        return min(len(sampled_land) - 1, int(r * total * len(sampled_land) / land_est))

    grass_level = sampled_land[idx(GRASS_RATIO)]
    hill_level = sampled_land[idx(GRASS_RATIO + HILL_RATIO)]
    mountain_level = sampled_land[idx(GRASS_RATIO + HILL_RATIO + MOUNTAIN_RATIO)]
    snow_level = sampled_land[idx(GRASS_RATIO + HILL_RATIO + MOUNTAIN_RATIO + SNOW_RATIO)]

    beach_band = grass_level * 0.08

    coarse = [[WATER] * cw for _ in range(ch)]

    for y in range(ch):
        ny = y * inv_h
        row = coarse[y]
        for x in range(cw):
            nx = x * inv_w
            h = terraforge_height(nx * scale, ny * scale, seed)

            if h <= 0.0:
                b = WATER
            elif h < beach_band:
                b = SAND
            elif h < grass_level:
                b = GRASS
            elif h < hill_level:
                b = HILL
            elif h < mountain_level:
                b = MOUNTAIN
            else:
                snow_noise = value_noise_2d(nx * 10.0, ny * 10.0, seed + 555)
                b = SNOW if (h >= snow_level and snow_noise > 0.70) else MOUNTAIN

            row[x] = b

    # ---- UPSCALE (nearest neighbor) ----
    biome_map = [[WATER] * width for _ in range(height)]
    for y in range(height):
        cy = min(ch - 1, y // step)
        out_row = biome_map[y]
        src_row = coarse[cy]
        for x in range(width):
            cx = min(cw - 1, x // step)
            out_row[x] = src_row[cx]

    result = {"width": width, "height": height, "biomes": biome_map, "seed": seed}
    _MAP_CACHE[cache_key] = result
    return result
