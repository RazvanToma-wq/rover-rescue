# Pure-Python replacement for the "noise" package (perlin/simplex).
# TerraForge imports `noise`, so this module shadows the broken C-extension.
# API: pnoise2 / snoise2 compatible enough for TerraForge.

from __future__ import annotations
import math

def _fade(t: float) -> float:
    # 6t^5 - 15t^4 + 10t^3
    return t * t * t * (t * (t * 6 - 15) + 10)

def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def _hash2(x: int, y: int, base: int) -> float:
    # Deterministic hash -> [0, 1)
    n = x * 374761393 + y * 668265263 + base * 2147483647
    n = (n ^ (n >> 13)) * 1274126177
    n = n ^ (n >> 16)
    # 24-bit mantissa -> stable float
    return ((n & 0xFFFFFF) / 16777216.0)

def _value_noise2(x: float, y: float, base: int = 0) -> float:
    x0 = math.floor(x)
    y0 = math.floor(y)
    x1 = x0 + 1
    y1 = y0 + 1

    sx = _fade(x - x0)
    sy = _fade(y - y0)

    n00 = _hash2(x0, y0, base)
    n10 = _hash2(x1, y0, base)
    n01 = _hash2(x0, y1, base)
    n11 = _hash2(x1, y1, base)

    ix0 = _lerp(n00, n10, sx)
    ix1 = _lerp(n01, n11, sx)
    v = _lerp(ix0, ix1, sy)

    # Map [0,1) -> [-1,1)
    return v * 2.0 - 1.0

def pnoise2(
    x: float,
    y: float,
    octaves: int = 1,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    repeatx: int = 1024,
    repeaty: int = 1024,
    base: int = 0,
) -> float:
    # Simple fractal value noise with octave accumulation
    amp = 1.0
    freq = 1.0
    total = 0.0
    maxamp = 0.0

    for o in range(max(1, int(octaves))):
        # repeat params ignored (TerraForge doesn't need strict wrapping for now)
        total += _value_noise2(x * freq, y * freq, base + o * 1013) * amp
        maxamp += amp
        amp *= persistence
        freq *= lacunarity

    return total / maxamp if maxamp != 0 else 0.0

def snoise2(
    x: float,
    y: float,
    octaves: int = 1,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    repeatx: int = 1024,
    repeaty: int = 1024,
    base: int = 0,
) -> float:
    # Use same implementation; TerraForge mainly needs coherent noise.
    return pnoise2(x, y, octaves, persistence, lacunarity, repeatx, repeaty, base)
