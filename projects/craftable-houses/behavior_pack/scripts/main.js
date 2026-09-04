import { world } from "@minecraft/server";

const PLAINS_COTTAGE_KIT = "craftable:plains_cottage_kit";
const PLAINS_COTTAGE_STRUCTURE = "craftable:plains_starter_cottage";

world.afterEvents.itemUse.subscribe((event) => {
  if (event.itemStack.typeId !== PLAINS_COTTAGE_KIT) return;

  const player = event.source;

  try {
    const hit = player.getBlockFromViewDirection({ maxDistance: 8 });

    if (!hit) {
      player.sendMessage("§eLook at the ground within 8 blocks to place your cottage.");
      return;
    }

    const base = hit.block.location;
    const placement = {
      x: base.x,
      y: base.y + 1,
      z: base.z
    };

    // ALPHA: Before this can consume a Survival kit, add footprint clearance,
    // world-height, protected-build, orientation, and multiplayer checks.
    // We intentionally do NOT consume the item in this prototype path.
    world.structureManager.place(
      PLAINS_COTTAGE_STRUCTURE,
      player.dimension,
      placement
    );

    player.sendMessage("§aPlains Starter Cottage placed. §7(Alpha: kit not consumed yet.)");
  } catch (error) {
    player.sendMessage("§cThe cottage could not be placed here. Your kit was not consumed.");
    console.warn(`[Craftable Houses] Cottage placement failed: ${error}`);
  }
});
