# Rover Rescue

Rover Rescue is an interactive pathfinding game where you help a rover navigate challenging terrain by adjusting terrain difficulty and constraints in real time.

The project runs fully **locally** and consists of:
- a **FastAPI backend** (terrain generation and pathfinding)
- a **TypeScript + Canvas frontend** (visualization and interaction)

---

## How the Game Works

1. A terrain map is generated as a grid.
2. Each cell represents a **biome**:
   - grass
   - sand
   - hill
   - mountain
   - snow
   - water
3. Each biome has a different **movement cost**.
4. You select:
   - a **start position** (Place Rover)
   - a **goal position** (Place X)
5. The backend computes the optimal path using the **A\*** algorithm.
6. The path is rendered on the map in real time.

Every interaction immediately updates the route, allowing you to experiment with different strategies.

---

## Terrain Cost Sliders

The game includes interactive sliders that let you control how difficult each terrain type is for the rover.

Each slider represents the movement cost of a terrain:
- Lower value means the rover prefers this terrain
- Higher value means the rover avoids this terrain

### Available Sliders
- Grass – easiest terrain by default  
- Sand – moderately slow  
- Hill – harder to traverse  
- Mountain – very expensive  
- Snow – most difficult terrain  

### Water Traversal

Water behaves differently from other terrains:
- If **Allow Water** is OFF, water is completely blocked  
- If **Allow Water** is ON, water becomes traversable with a low cost  

This allows you to:
- Force land-only routes  
- Or enable risky shortcuts across water  

### Real-Time Recalculation

Whenever you:
- Move a slider  
- Toggle water  
- Change start or goal positions  

The path is recomputed instantly, showing how terrain costs affect the optimal route.

---

## Features

- Procedurally generated terrain maps  
- A* pathfinding algorithm  
- Interactive terrain cost sliders  
- Optional water traversal  
- Real-time canvas rendering  
- Fast local performance  
- Visual route and distance feedback  

---

## Play Locally (Recommended)

This is the best way to play the game.  
No lag, no online services, and no deployment required.

### Requirements

You need:
- Git
- Python 3.10 or newer
- Node.js 18 or newer

Check installed versions:
```bash
git --version
python --version
node --version
```

---

## Running the Game Locally

### 1. Clone the Repository
```bash
git clone https://github.com/RazvanToma-wq/rover-rescue.git
cd rover-rescue
```

### 2. Start the Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend will run at:
```
http://127.0.0.1:8000
```

### 3. Start the Frontend
Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```

The game will be available at:
```
http://localhost:5173
```
