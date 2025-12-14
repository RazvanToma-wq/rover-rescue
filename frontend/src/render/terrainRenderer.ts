import { ctx, canvas } from "./canvas";
import type { BiomeMap } from "../api/types";
import { state } from "../input/state";

const COLORS: Record<number, string> = {
  0: "#1e88e5", // water
  1: "#f4e04d", // sand
  2: "#43a047", // grass
  3: "#fb8c00", // hill
  4: "#424242", // mountain
  5: "#ffffff", // snow
};

function drawCross(cx: number, cy: number, size: number, color: string) {
  ctx.strokeStyle = color;
  ctx.lineWidth = Math.max(4, size * 0.25);
  ctx.beginPath();
  ctx.moveTo(cx - size, cy - size);
  ctx.lineTo(cx + size, cy + size);
  ctx.moveTo(cx + size, cy - size);
  ctx.lineTo(cx - size, cy + size);
  ctx.stroke();
}

export function renderTerrain(map: BiomeMap) {
  const cw = canvas.clientWidth;
  const ch = canvas.clientHeight;

  ctx.clearRect(0, 0, cw, ch);
  const scale = Math.min(cw / map.width, ch / map.height);

  const drawW = map.width * scale;
  const drawH = map.height * scale;

  const offsetX = (cw - drawW) / 2;
  const offsetY = (ch - drawH) / 2;

  const tile = scale;


  for (let y = 0; y < map.height; y++) {
    for (let x = 0; x < map.width; x++) {
      ctx.fillStyle = COLORS[map.biomes[y][x]];
      ctx.fillRect(
        offsetX + x * tile,
        offsetY + y * tile,
        tile + 0.5,
        tile + 0.5
      );
    }
  }

  // --- Path ---
  if (state.path.length >= 2) {
    ctx.strokeStyle = "red";
    ctx.lineWidth = Math.max(4, tile * 0.9);
    ctx.lineJoin = "round";
    ctx.lineCap = "round";

    ctx.beginPath();
    const [sx, sy] = state.path[0];
    ctx.moveTo(
      offsetX + (sx + 0.5) * tile,
      offsetY + (sy + 0.5) * tile
    );

    for (let i = 1; i < state.path.length; i++) {
      const [x, y] = state.path[i];
      ctx.lineTo(
        offsetX + (x + 0.5) * tile,
        offsetY + (y + 0.5) * tile
      );
    }
    ctx.stroke();
  }

  const crossSize = Math.max(14, tile * 2.2); 

  if (state.start) {
    drawCross(
      offsetX + (state.start[0] + 0.5) * tile,
      offsetY + (state.start[1] + 0.5) * tile,
      crossSize,
      "#00bfff"
    );
  }

  if (state.end) {
    drawCross(
      offsetX + (state.end[0] + 0.5) * tile,
      offsetY + (state.end[1] + 0.5) * tile,
      crossSize,
      "#ff3333"
    );
  }
}
