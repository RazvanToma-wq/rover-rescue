import random
from app.models.map import MapData

def generate_map(width: int, height: int) -> MapData:
    terrain = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            r = random.random()
            if r < 0.65:
                terrain[y][x] = 0  # grass
            elif r < 0.85:
                terrain[y][x] = 1  # dirt
            else:
                terrain[y][x] = 3  # rock

    for _ in range(12): 
        cx = random.randint(0, width - 1)
        cy = random.randint(0, height - 1)
        radius = random.randint(6, 14)

        for y in range(height):
            for x in range(width):
                if (x - cx) ** 2 + (y - cy) ** 2 < radius ** 2:
                    terrain[y][x] = 2  # water

    def neighbors(x, y):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    yield terrain[ny][nx]

    for _ in range(2):  
        new = [[terrain[y][x] for x in range(width)] for y in range(height)]
        for y in range(height):
            for x in range(width):
                counts = {0:0,1:0,2:0,3:0}
                for n in neighbors(x, y):
                    counts[n] += 1
                new[y][x] = max(counts, key=counts.get)
        terrain = new

    return MapData(width=width, height=height, terrain=terrain)
