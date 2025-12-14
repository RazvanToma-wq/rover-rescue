import type { BiomeMap } from "../api/types";

export type PlacementMode = "start" | "end" | null;

export const state: {
  map: BiomeMap | null;
  mode: PlacementMode;
  start: [number, number] | null;
  end: [number, number] | null;
  path: [number, number][];
} = {
  map: null,
  mode: null,
  start: null,
  end: null,
  path: [],
};
