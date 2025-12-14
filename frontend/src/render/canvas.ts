export const canvas = document.createElement("canvas");
export const ctx = canvas.getContext("2d")!;

let topOffsetPx = 0;

export function setTopOffset(px: number) {
  topOffsetPx = px;
  canvas.style.position = "absolute";
  canvas.style.left = "50%";
  canvas.style.top = `${topOffsetPx}px`;
  canvas.style.transform = "translateX(-50%)";
}

/**
 * Canvas fits the FULL map inside the viewport.
 * No zoom-in. Aspect ratio preserved.
 */
export function resizeCanvasToMap(mapWidth: number, mapHeight: number) {
  const dpr = window.devicePixelRatio || 1;

  const availW = window.innerWidth;
  const availH = window.innerHeight - topOffsetPx;

  const scale = Math.min(availW / mapWidth, availH / mapHeight);

  const cssW = Math.floor(mapWidth * scale);
  const cssH = Math.floor(mapHeight * scale);

  canvas.width = cssW * dpr;
  canvas.height = cssH * dpr;

  canvas.style.width = `${cssW}px`;
  canvas.style.height = `${cssH}px`;

  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}
