import type { BiomeMap } from "./types";

const API = import.meta.env.DEV
  ? "http://127.0.0.1:8000"
  : "https://rover-rescue-backend.onrender.com";

async function readError(res: Response) {
  const text = await res.text().catch(() => "");
  return `${res.status} ${res.statusText}${text ? ` — ${text}` : ""}`;
}

export async function fetchMap(): Promise<BiomeMap> {
  const res = await fetch(`${API}/map/generate`);
  if (!res.ok) throw new Error(await readError(res));
  return res.json();
}

export async function fetchRoute(
  grid: number[][],
  start: [number, number],
  goal: [number, number],
  costs: Record<number, number>,
  allowWater: boolean
) {
  const res = await fetch(`${API}/mission/route`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      grid,
      start,
      goal,
      costs,
      allow_water: allowWater,
    }),
  });

  if (!res.ok) throw new Error(await readError(res));
  return res.json();
}
