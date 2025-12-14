import "./styles/main.css";

import { canvas, setTopOffset } from "./render/canvas";
import { renderTerrain } from "./render/terrainRenderer";
import { fetchMap } from "./api/client";
import { createPlacementControls, TOPBAR_HEIGHT } from "./input/placementControls";
import { enableClickPlacement, setMap } from "./input/clickHandler";
import { state } from "./input/state";

document.body.style.overflow = "auto";

const app = document.getElementById("app")!;
app.appendChild(canvas);

async function loadAndRenderMap() {
  const map = await fetchMap();
  setMap(map);
  renderTerrain(map);
}

async function main() {
  setTopOffset(TOPBAR_HEIGHT);

  enableClickPlacement();
  await loadAndRenderMap();

  createPlacementControls({
    onNewMap: async () => {
      await loadAndRenderMap();
    },
  });
}

await main();
