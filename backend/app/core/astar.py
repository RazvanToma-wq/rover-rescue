import heapq
from typing import Dict, List, Tuple

# 8-direction movement (dx, dy, distance multiplier)
DIRS = [
    (1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
    (1, 1, 1.4142), (1, -1, 1.4142), (-1, 1, 1.4142), (-1, -1, 1.4142),
]


def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """Octile distance heuristic (correct for 8-direction grids)."""
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return (dx + dy) + (1.4142 - 2.0) * min(dx, dy)


def astar(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    costs: Dict[int, float],
):
    width = len(grid[0])
    height = len(grid)

    # Water blocking logic
    water_cost = costs.get(0, float("inf"))

    def is_blocked(x: int, y: int) -> bool:
        if grid[y][x] == 0 and water_cost == float("inf"):
            return True
        return False

    open_set: List[Tuple[float, Tuple[int, int]]] = []
    heapq.heappush(open_set, (0.0, start))

    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], float] = {start: 0.0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        cx, cy = current

        for dx, dy, move_cost in DIRS:
            nx, ny = cx + dx, cy + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if is_blocked(nx, ny):
                continue

            # Prevent diagonal corner cutting
            if dx != 0 and dy != 0:
                if is_blocked(cx + dx, cy) or is_blocked(cx, cy + dy):
                    continue

            terrain = grid[ny][nx]
            terrain_cost = costs.get(terrain)

            if terrain_cost is None or terrain_cost == float("inf"):
                continue

            step_cost = terrain_cost * move_cost
            tentative = g_score[current] + step_cost

            if tentative < g_score.get((nx, ny), float("inf")):
                came_from[(nx, ny)] = current
                g_score[(nx, ny)] = tentative
                f = tentative + heuristic((nx, ny), goal)
                heapq.heappush(open_set, (f, (nx, ny)))

    return []
