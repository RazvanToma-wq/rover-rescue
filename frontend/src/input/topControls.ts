export function createTopControls() {
  const top = document.getElementById("top-ui")!;

  const newMap = document.createElement("button");
  newMap.textContent = "New map";
  newMap.onclick = () => location.reload();

  const rover = document.createElement("button");
  rover.textContent = "Place rover";
  rover.id = "place-rover";

  const target = document.createElement("button");
  target.textContent = "Place target";
  target.id = "place-target";

  top.append(newMap, rover, target);
}
