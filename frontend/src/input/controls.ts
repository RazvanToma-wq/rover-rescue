import { state } from "./state";

export function createControls(onNewMap: () => void) {
  const bar = document.createElement("div");
  bar.style.position = "fixed";
  bar.style.top = "0";
  bar.style.left = "0";
  bar.style.right = "0";
  bar.style.height = "48px";
  bar.style.display = "flex";
  bar.style.gap = "8px";
  bar.style.padding = "8px";
  bar.style.background = "#111";
  bar.style.zIndex = "10";

  function btn(label: string, onClick: () => void) {
    const b = document.createElement("button");
    b.textContent = label;
    b.onclick = onClick;
    return b;
  }

  bar.append(
    btn("New Map", onNewMap),
    btn("Select Rover", () => state.mode = "start"),
    btn("Select Target", () => state.mode = "end"),
  );

  document.body.appendChild(bar);
}
