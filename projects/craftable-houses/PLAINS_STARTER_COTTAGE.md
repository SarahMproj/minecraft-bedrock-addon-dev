# Plains Starter Cottage — House Specification

**DLC:** Craftable Houses  
**House ID:** `craftable:plains_starter_cottage`  
**Kit ID:** `craftable:plains_cottage_kit`  
**Biome family:** Plains / village starter  
**Structure bounds:** `11 × 8 × 9` blocks (`X × Y × Z`)  
**Enclosed core:** `9 × 7` blocks  
**Front:** local `Z=0/1`; centered entry at `X=5`  
**Alpha status:** structure design frozen; generated binary still requires in-game validation

## Design intent

The Plains Starter Cottage is the reference implementation for every Craftable Houses structure. It should read immediately as a cozy Minecraft-native home, fit on a modest Survival plot, and be deterministic enough that placement, rotation, collision testing and material accounting can be reused by every later house.

The alpha deliberately favors robust full-block geometry over decorative stairs, trapdoors, beds, chests and other state/block-entity-heavy details. Those become the art-polish pass after the structure pipeline is proven.

## Player fantasy

Craft a house kit from gathered materials, walk to a clear patch of land, aim at the intended front-center location, use the kit, and get a useful starter cottage without damaging nearby builds.

The cottage includes:

- cobblestone perimeter foundation and porch threshold;
- oak plank floor and walls;
- oak-log timber framing;
- front, side and rear glazing;
- centered two-block doorway ready for a player-supplied door;
- stepped gable roof;
- cobblestone chimney;
- crafting table;
- two-block bookshelf feature;
- open furnishing space for bed, chest and furnace.

## Coordinate system

Local origin is the north-west-lower corner of the structure bounds.

- `X`: left → right when facing the front.
- `Y`: bottom → top.
- `Z`: front → back.
- Front entry center is `X=5, Z=1`.
- Porch threshold occupies `X=4..6, Y=0, Z=0`.
- Main footprint occupies `X=1..9, Y=0..4, Z=1..7`.
- Roof reaches `Y=7`.
- Chimney is near rear-right at `X=8, Z=5`.

Exterior empty cells are stored as structure void (`-1` in the structure palette indices), not air. Only the interior volume and doorway contain explicit `minecraft:air`. This prevents the structure asset itself from unnecessarily clearing blocks outside its intended body.

## Floor plan

Front is at the bottom.

```text
BACK  Z=7
        1 2 3 4 5 6 7 8 9
Z7      L W L G G G L W L
Z6      W C . . . . . B W
Z5      W . . . . . . . W
Z4      G . . . . . . . G
Z3      G . . . . . . . G
Z2      W . . . . . . . W
Z1      L G G L D L G G L
Z0            # # #
FRONT
```

Legend: `L` oak log, `W` oak plank wall, `G` glass, `D` two-block doorway, `#` cobblestone porch, `C` crafting table, `B` bookshelf, `.` interior air.

## Front elevation concept

```text
Y7          █ █ █
Y6        █ █   █ █
Y5      █ █       █ █
Y4       L L L W L L L
Y3       L G G L W L G G L
Y2       L G G L   L G G L
Y1       L W W L   L W W L
Y0       ═════════════════
             ▓ ▓ ▓
```

The roof is a stepped full-block gable with an overhang. This is intentionally chunky for the first alpha; stairs/slabs can replace it once block-state rotation is proven.

## Palette

- `minecraft:air`
- `minecraft:oak_planks`
- `minecraft:cobblestone`
- `minecraft:oak_log` with `pillar_axis=y`
- `minecraft:glass`
- `minecraft:crafting_table`
- `minecraft:bookshelf`

No entities are embedded. No chest, furnace, bed or other block-entity-dependent furnishing is embedded in alpha.

## Bill of materials

| Material | Count |
|---|---:|
| Oak planks | 209 |
| Oak logs | 32 |
| Cobblestone | 35 |
| Glass | 22 |
| Bookshelves | 2 |
| Crafting table | 1 |
| **Total solid blocks** | **301** |

The BOM is now the source of truth for Survival recipe balancing. The kit recipe should use compressed Building Bundles so the material cost remains meaningful without asking a 3×3 grid to represent hundreds of blocks directly.

## Placement contract

For the vertical slice:

1. Player targets a ground block within interaction range.
2. Target becomes the intended front-center reference point.
3. Placement code derives structure origin from the selected rotation.
4. The rotated footprint is checked before placement.
5. Structure-void cells are ignored.
6. Explicit interior-air cells may clear only cells that passed the safe-replaceability test.
7. Invalid height or destructive overlap fails with useful feedback.
8. Kit remains in inventory on failure.
9. Kit is consumed only after placement succeeds.
10. Multiplayer attempts must not double-consume or overlap.

Foundation leveling is intentionally not automatic in the first vertical slice. The player should select reasonably flat ground. Terrain adaptation can be added after the basic loop is reliable.

## Art direction

**Read:** village-native, warm, practical, collectible.

Silhouette anchors: centered entrance, symmetrical front glazing, pronounced gable, visible chimney, timber-frame verticals, one-storey body with taller roof.

Avoid modern furniture, non-vanilla-looking geometry, noisy detailing at icon scale, and rare materials that undermine the starter-home fantasy.

## Alpha acceptance test

- Pack loads with no structure parsing error.
- `world.structureManager.getPackStructureIds()` includes `craftable:plains_starter_cottage`.
- Rotation 0 produces the intended 11×8×9 cottage.
- Front, sides, rear, roof, chimney, windows and interior match this spec.
- All four rotations are tested.
- Structure void leaves exterior cells untouched.
- No embedded entities appear.
- Two-player placement race is tested.
- Generated BOM matches this document.
- Status log is updated after test.

## Source references

- Minecraft Creator docs: https://learn.microsoft.com/minecraft/creator/
- Stable StructureManager: https://learn.microsoft.com/minecraft/creator/scriptapi/minecraft/server/structuremanager
- Official samples: https://github.com/microsoft/minecraft-samples
- `.mcstructure` technical reference: https://github.com/Bedrock-OSS/bedrock-wiki/blob/wiki/docs/nbt/mcstructure.md
