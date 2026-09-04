# Craftable Houses

A Minecraft Bedrock add-on built around a simple fantasy: **craft a house the way you craft a tool, then place it into the world.**

## Core loop

1. Explore and gather biome-relevant materials.
2. Craft a House Kit at a crafting table.
3. Carry the kit to a suitable build site.
4. Use the kit to place a complete Minecraft-native structure.
5. Decorate, expand, inhabit, trade, or connect houses into a settlement.

The pack is designed so each structure feels earned in Survival rather than functioning like a free Creative-mode prefab library.

## Pack 01 — Village Collection

The launch collection is anchored to the five vanilla biomes with naturally generating village styles.

| House | Biome | Gameplay identity | Signature materials |
|---|---|---|---|
| Plains Starter Cottage | Plains | Cheap first home / vertical slice | Oak, cobblestone, glass |
| Desert Courtyard House | Desert | Heat-safe compact home with enclosed court | Sandstone, smooth sandstone, acacia accent |
| Savanna Lookout House | Savanna | Raised profile / broad visibility | Acacia, cobblestone, fences |
| Taiga Hearth Lodge | Taiga | Heavy timber survival lodge | Spruce, cobblestone, campfire |
| Snowy Gabled Cabin | Snowy Plains | Insulated-looking alpine cabin | Spruce, stone brick, snow/ice accent |

These are **collection anchors**, not strict copies of vanilla village buildings. The visual rule is “recognizably native to that biome, but desirable enough that a player wants to craft it intentionally.”

## Content primitive

Every new house must ship as a complete `House Kit` unit:

- unique namespaced item identifier
- Survival recipe
- item icon
- localization
- packaged `.mcstructure`
- footprint and clearance definition
- placement/orientation behavior
- consume-on-success behavior
- failure feedback
- multiplayer test case
- screenshots / gameplay capture target

No house is counted as complete because its structure alone exists.

## Drop model

After Pack 01 validates the primitive, future collections can be added as themed drops rather than reinventing the system:

- Jungle Expedition
- Swamp Witchcraft
- Coastal / Fishing Village
- Mushroom Fantasy
- Nether Frontier
- End Settlers
- Medieval Keep
- Steampunk Town
- Cottagecore / Garden
- Adventure Guild
- Seasonal / holiday drops

## Design principles

**Minecraft-native.** Houses should look like something a great Minecraft builder might build, not an imported low-detail model.

**Survival-legible.** Recipes should communicate the material identity of the finished building.

**Useful immediately.** Starter structures should include sensible doors, light, basic storage/furnishing slots, and a safe interior footprint without trivializing progression.

**Collectible.** Icons, names, recipe cards and screenshots should make players want to complete sets.

**Expandable.** A placed house should remain ordinary editable blocks so the player's story continues after placement.

**Multiplayer-safe.** Placement cannot assume a single-player world or unlimited empty terrain.

## Alpha namespace

`craftable`

## Alpha target

The first vertical slice is `craftable:plains_cottage_kit` placing the packaged structure `craftable:plains_starter_cottage`.
