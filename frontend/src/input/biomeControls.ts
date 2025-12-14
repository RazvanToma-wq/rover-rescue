// biomeControls.ts

export let allowWater = false;

export const biomeCosts: Record<number, number> = {
  1: 2,  // SAND
  2: 1,  // GRASS
  3: 3,  // HILL
  4: 5,  // MOUNTAIN
  5: 8,  // SNOW
};

export function createBiomeControls(container: HTMLElement) {
  // --- Water toggle ---
  const waterWrapper = document.createElement("div");
  waterWrapper.style.display = "flex";
  waterWrapper.style.alignItems = "center";
  waterWrapper.style.gap = "8px";
  waterWrapper.style.whiteSpace = "nowrap";

  const waterCheckbox = document.createElement("input");
  waterCheckbox.type = "checkbox";
  waterCheckbox.checked = allowWater;

  const waterLabel = document.createElement("label");
  waterLabel.textContent = "Allow Water";

  waterCheckbox.onchange = () => {
    allowWater = waterCheckbox.checked;
  };

  waterWrapper.appendChild(waterCheckbox);
  waterWrapper.appendChild(waterLabel);
  container.appendChild(waterWrapper);

  // --- Sliders ---
  const entries: [string, number, number, number][] = [
    ["Sand", 1, 1, 10],
    ["Grass", 2, 1, 10],
    ["Hill", 3, 1, 15],
    ["Mountain", 4, 1, 20],
    ["Snow", 5, 1, 25],
  ];

  for (const [label, biome, min, max] of entries) {
    const wrapper = document.createElement("div");
    wrapper.style.display = "grid";
    wrapper.style.gap = "6px";
    wrapper.style.minWidth = "140px";

    const row = document.createElement("div");
    row.style.display = "flex";
    row.style.justifyContent = "space-between";

    const text = document.createElement("span");
    text.textContent = label;

    const val = document.createElement("span");
    val.textContent = String(biomeCosts[biome]);

    const slider = document.createElement("input");
    slider.type = "range";
    slider.min = String(min);
    slider.max = String(max);
    slider.value = String(biomeCosts[biome]);

    slider.oninput = () => {
      biomeCosts[biome] = Number(slider.value);
      val.textContent = slider.value;
    };

    row.appendChild(text);
    row.appendChild(val);
    wrapper.appendChild(row);
    wrapper.appendChild(slider);
    container.appendChild(wrapper);
  }
}
