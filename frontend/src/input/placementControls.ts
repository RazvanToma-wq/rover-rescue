import { createBiomeControls, biomeCosts, allowWater } from "./biomeControls";
import { clearPlacement, setPlacementMode } from "./clickHandler";
import { state } from "./state";
import { fetchRoute } from "../api/client";
import { renderTerrain } from "../render/terrainRenderer";

export const TOPBAR_HEIGHT = 72;

export function createPlacementControls(opts: {
  onNewMap: () => void | Promise<void>;
}) {
  const bar = document.createElement("div");
  bar.id = "topbar";
  bar.style.position = "fixed";
  bar.style.top = "0";
  bar.style.left = "0";
  bar.style.right = "0";
  bar.style.height = `${TOPBAR_HEIGHT}px`;
  bar.style.display = "flex";
  bar.style.alignItems = "center";
  bar.style.gap = "14px";
  bar.style.padding = "10px 12px";
  bar.style.background = "rgba(17, 17, 17, 0.92)";
  bar.style.backdropFilter = "blur(6px)";
  bar.style.color = "white";
  bar.style.zIndex = "1000";
  bar.style.boxSizing = "border-box";
  bar.style.overflowX = "auto";

  const left = document.createElement("div");
  left.style.display = "flex";
  left.style.alignItems = "center";
  left.style.gap = "10px";

  const right = document.createElement("div");
  right.style.display = "flex";
  right.style.alignItems = "center";
  right.style.gap = "14px";

  const title = document.createElement("div");
  title.textContent = "Rover Rescue";
  title.style.fontWeight = "700";
  title.style.marginRight = "6px";
  title.style.whiteSpace = "nowrap";

  const btnNew = button("New Map", async () => {
    setActive(null);
    clearPlacement();
    await opts.onNewMap();
  });

  const btnRover = toggleButton("Place Rover", () => setPlacementMode("start"));
  const btnX = toggleButton("Place X", () => setPlacementMode("end"));

  function setActive(which: "rover" | "x" | null) {
    btnRover.dataset.active = which === "rover" ? "1" : "0";
    btnX.dataset.active = which === "x" ? "1" : "0";
    styleToggle(btnRover);
    styleToggle(btnX);

    if (which === "rover") setPlacementMode("start");
    else if (which === "x") setPlacementMode("end");
    else setPlacementMode(null);
  }

  // keep toggle state consistent
  btnRover.onclick = () => setActive(btnRover.dataset.active === "1" ? null : "rover");
  btnX.onclick = () => setActive(btnX.dataset.active === "1" ? null : "x");

  const btnClear = button("Clear", () => {
    setActive(null);
    clearPlacement();
  });

  // Calculate path ONLY when button pressed
  const btnPath = button("Calculate Path", async () => {
    if (!state.map || !state.start || !state.end) {
      alert("Place Rover and Place X first.");
      return;
    }

    try {
      const res = await fetchRoute(
  state.map.biomes,
  state.start,
  state.end,
  biomeCosts,
  allowWater 
);

      const path: [number, number][] = Array.isArray(res?.path) ? res.path : [];

      if (path.length === 0) {
        if (!allowWater) {
          alert("No valid path without crossing water.\n\nTick 'Allow Water' if you want to allow water traversal.");
        } else {
          alert("No valid path found with current terrain costs.");
        }
        state.path = [];
        renderTerrain(state.map);
        return;
      }

    
      if (!allowWater) {
        const touchesWater = path.some(([x, y]) => state.map!.biomes[y][x] === 0);
        if (touchesWater) {
          alert("The shortest path requires crossing water.\n\nTick 'Allow Water' to enable water traversal.");
          state.path = [];
          renderTerrain(state.map);
          return;
        }
      }

      state.path = path;
      renderTerrain(state.map);
    } catch (e) {
      console.error("Path calculation failed:", e);
      alert("Path calculation failed. See console for details.");
    }
  });

  left.appendChild(title);
  left.appendChild(btnNew);
  left.appendChild(btnRover);
  left.appendChild(btnX);
  left.appendChild(btnClear);
  left.appendChild(btnPath);

  createBiomeControls(right);

  bar.appendChild(left);
  bar.appendChild(right);
  document.body.appendChild(bar);

  setActive(null);
  return bar;
}

function button(label: string, onClick: () => void | Promise<void>) {
  const b = document.createElement("button");
  b.textContent = label;
  b.style.padding = "8px 10px";
  b.style.borderRadius = "10px";
  b.style.border = "1px solid rgba(255,255,255,0.18)";
  b.style.background = "rgba(255,255,255,0.08)";
  b.style.color = "white";
  b.style.cursor = "pointer";
  b.style.whiteSpace = "nowrap";
  b.onmouseenter = () => (b.style.background = "rgba(255,255,255,0.14)");
  b.onmouseleave = () => (b.style.background = "rgba(255,255,255,0.08)");
  b.onclick = () => void onClick();
  return b;
}

function toggleButton(label: string, onActivate: () => void) {
  const b = button(label, onActivate);
  b.dataset.active = "0";
  styleToggle(b);
  return b;
}

function styleToggle(b: HTMLButtonElement) {
  const active = b.dataset.active === "1";
  b.style.background = active ? "rgba(46, 204, 113, 0.25)" : "rgba(255,255,255,0.08)";
  b.style.border = active
    ? "1px solid rgba(46, 204, 113, 0.6)"
    : "1px solid rgba(255,255,255,0.18)";
}
