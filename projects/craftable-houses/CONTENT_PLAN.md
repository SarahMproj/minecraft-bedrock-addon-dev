# Craftable Houses — Content & Economy Plan

## Product promise

Craftable Houses should feel like a legitimate Survival progression system, not a cheat command disguised as an item. The player should experience a satisfying compression of gathering/building effort while still paying a meaningful material cost.

## Recipe architecture

A 3×3 crafting grid cannot directly express the true material cost of an entire building. Production recipes therefore use **Building Bundles** as compressed ingredients.

### Shared component items

- `craftable:lumber_bundle` — represents a large stack of processed wood
- `craftable:masonry_bundle` — represents stone/cobble/brick construction material
- `craftable:glass_bundle` — represents prepared glazing
- `craftable:roofing_bundle` — represents stairs/slabs/roof material
- `craftable:builder_blueprint` — progression/control ingredient used to unlock full house kits

The exact input counts will be tuned against the actual block bill-of-materials for each finished `.mcstructure`. A bundle should represent an intuitive batch (for example 16 or 32 related blocks), not arbitrary currency.

## Recommended production rule

For each house:

1. Export/build the final structure.
2. Count its major Survival-obtainable block families.
3. Convert those counts into bundle requirements with a modest convenience discount.
4. Preserve biome identity by requiring one or more signature materials directly or through a biome-specific bundle.
5. Keep rare decorative blocks out of starter recipes unless they are supplied as part of the finished structure intentionally.

The convenience discount is the player's reward for buying/using the DLC; it should not collapse early-game progression.

## Pack 01 — Village Collection

### 01. Plains Starter Cottage

**Role:** cheapest universal starter home and alpha vertical slice.

**Visual target:** oak frame, cobblestone foundation/chimney, simple glass windows, warm interior, compact pitched roof.

**Production recipe target:**

```text
L G L
M B M
L R L
```

- `L` Lumber Bundle (oak-compatible)
- `G` Glass Bundle
- `M` Masonry Bundle
- `R` Roofing Bundle
- `B` Builder Blueprint

The current raw oak/glass/cobblestone recipe in the alpha branch is mechanics-only and should be replaced after bundle items exist.

### 02. Desert Courtyard House

**Role:** enclosed, low-profile desert home.

**Signature:** sandstone family + courtyard + shaded entry.

**Recipe emphasis:** Masonry-heavy; sandstone signature input; lighter lumber requirement.

### 03. Savanna Lookout House

**Role:** high-visibility home with vertical character.

**Signature:** acacia + stone + balcony/lookout.

**Recipe emphasis:** Lumber-heavy with fencing/railing identity.

### 04. Taiga Hearth Lodge

**Role:** durable midgame lodge with cozy utility fantasy.

**Signature:** spruce, cobblestone, central hearth/chimney.

**Recipe emphasis:** Lumber + Masonry + explicit hearth component.

### 05. Snowy Gabled Cabin

**Role:** alpine/snow-biome collectible home.

**Signature:** steep spruce roof, stone base, snow-compatible exterior.

**Recipe emphasis:** Roofing-heavy; spruce + masonry; snow/ice accent requirement should be tuned so it is biome-relevant without being annoying.

## Placement UX

House kits should behave consistently:

- Player holds kit and targets the ground.
- A valid placement requires enough horizontal/vertical clearance for the known footprint.
- Final orientation should be predictable from the player's facing direction.
- Invalid placement explains the reason and preserves the kit.
- Successful placement consumes exactly one kit in Survival.
- Creative behavior can be unlimited.
- The placed result is normal editable Minecraft blocks.

### Future polish target

Before use, show a lightweight footprint/ghost preview or boundary indicator. This is not required for first alpha if it would slow proof of the core loop.

## Structure quality bar

Each launch house should include:

- safe enclosed interior
- correctly oriented door(s)
- basic lighting
- windows
- roof with no obvious spawnable dark cavities
- at least one intended bed location
- small storage/crafting area
- editable furnishing space
- no unobtainable/command-only blocks in ordinary Survival SKU structures unless intentionally justified
- no loot that breaks progression

## Expansion model

New drops should mostly add **content**, not new engine systems. A drop can be produced by creating new House Kit units using the existing placement/economy framework. System changes should be reserved for meaningful expansions such as upgradeable houses, settlement bonuses, NPC builders, or multiplayer town mechanics.
