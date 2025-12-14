import { canvas } from "../render/canvas";
import { renderTerrain } from "../render/terrainRenderer";
import type { BiomeMap } from "../api/types";
import { state } from "./state";
import type { PlacementMode } from "./state";
import { resizeCanvasToMap } from "../render/canvas";

let enabled = false;

export function setMap(map: BiomeMap) {
  state.map = map;
  state.start = null;
  state.end = null;
  state.path = [];

  resizeCanvasToMap(map.width, map.height);
}

export function setPlacementMode(m: PlacementMode) {
  state.mode = m;
}

export function clearPlacement() {
  state.start = null;
  state.end = null;
  state.path = [];
  if (state.map) renderTerrain(state.map);
}

export function enableClickPlacement() {
  if (enabled) return;
  enabled = true;

  canvas.addEventListener("click", (e) => {
    if (!state.map || !state.mode) return;

    const rect = canvas.getBoundingClientRect();
    const map = state.map;

    const x = Math.floor((e.clientX - rect.left) * (map.width / rect.width));
    const y = Math.floor((e.clientY - rect.top) * (map.height / rect.height));

    if (x < 0 || y < 0 || x >= map.width || y >= map.height) return;

    if (state.mode === "start") state.start = [x, y];
    if (state.mode === "end") state.end = [x, y];

    renderTerrain(map);
  });
}
