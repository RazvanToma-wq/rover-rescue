from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from typing import Any, Dict, List, Tuple

from app.core.astar import astar

router = APIRouter()

DEFAULT_COSTS: Dict[int, float] = {
    0: 1.0,  # water (will be overridden depending on allow_water)
    1: 2.0,  # sand
    2: 1.0,  # grass
    3: 3.0,  # hill
    4: 5.0,  # mountain
    5: 8.0,  # snow
}


class MissionRequest(BaseModel):
    grid: List[List[int]]
    start: Tuple[int, int]
    goal: Tuple[int, int]

    allow_water: bool = False

    costs: Dict[Any, Any] = Field(default_factory=dict)

    @field_validator("costs", mode="before")
    @classmethod
    def normalize_costs(cls, v):
        if v is None:
            return DEFAULT_COSTS.copy()

        if not isinstance(v, dict):
            if isinstance(v, list):
                out: Dict[int, float] = {}
                for i, val in enumerate(v):
                    if val is None:
                        continue
                    try:
                        out[int(i)] = float(val)
                    except Exception:
                        pass
                merged = DEFAULT_COSTS.copy()
                merged.update(out)
                return merged
            return DEFAULT_COSTS.copy()

        out: Dict[int, float] = {}
        for k, val in v.items():
            if val is None:
                continue
            try:
                ik = int(k)
                fv = float(val)
                out[ik] = fv
            except Exception:
                continue

        merged = DEFAULT_COSTS.copy()
        merged.update(out)
        return merged


@router.post("/mission/route")
def compute_route(data: MissionRequest):
    costs = dict(data.costs)

    if data.allow_water:
        costs[0] = 1.0
    else:
        costs[0] = float("inf")

    path = astar(data.grid, data.start, data.goal, costs)

    return {
        "path": path,
        "distance": len(path),
    }
