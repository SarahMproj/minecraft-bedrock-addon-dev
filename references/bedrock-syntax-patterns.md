# Bedrock stable syntax patterns

These are real Bedrock file shapes derived from Mojang/Microsoft documentation and the official `microsoft/minecraft-samples` repository. They are intentionally small enough to adapt safely.

The examples were reviewed on 2026-09-04 against the stable Creator documentation and official sample commit `5e04b6f719c316b0611f569af0cab7d6e9a2fb26`. They are JSON-parse tested by this skill. They have not, merely by appearing here, been imported into a user's game or approved for Marketplace.

## How to use these patterns

- Replace the `studio` namespace with one unique lowercase namespace and keep it stable.
- Generate new UUIDs. The UUIDs below are valid demo values, but copying them into multiple packs would create collisions.
- Treat shown `format_version`, `min_engine_version`, and Script API versions as a compatible example set, not a timeless "latest" value. Recheck the stable documentation for the target game version.
- Copy a complete pattern into the stated file path. Do not paste several root objects into one JSON file.
- Match case exactly across identifiers, texture keys, geometry identifiers, paths, and localization keys.
- Run the bundled validator, Mojang's `mct validate`, and an in-game Content Log test after adapting a pattern.

## Linked resource and behavior pack manifests

`resource_pack/manifest.json`:

```json
{
  "format_version": 2,
  "header": {
    "name": "Studio DLC Resources",
    "description": "Resource pack for Studio DLC",
    "uuid": "c4e5d0b2-93e3-4b91-a7a0-1c6d3fe5f101",
    "version": [1, 0, 0],
    "min_engine_version": [1, 26, 30]
  },
  "modules": [
    {
      "type": "resources",
      "uuid": "47f9c0d7-f344-4bb0-ae91-d85fa5f1d102",
      "version": [1, 0, 0]
    }
  ]
}
```

`behavior_pack/manifest.json` with a data module, script module, RP dependency, and stable Script API dependency:

```json
{
  "format_version": 2,
  "header": {
    "name": "Studio DLC Behavior",
    "description": "Behavior pack for Studio DLC",
    "uuid": "b842e2a5-42d8-4136-96a6-18deaf2df201",
    "version": [1, 0, 0],
    "min_engine_version": [1, 26, 30]
  },
  "modules": [
    {
      "type": "data",
      "uuid": "01afebcf-869f-40db-bdf2-e0155446f202",
      "version": [1, 0, 0]
    },
    {
      "type": "script",
      "language": "javascript",
      "entry": "scripts/main.js",
      "uuid": "62f301c5-47e6-4999-8806-d4e9cc27f203",
      "version": [1, 0, 0]
    }
  ],
  "dependencies": [
    {
      "uuid": "c4e5d0b2-93e3-4b91-a7a0-1c6d3fe5f101",
      "version": [1, 0, 0]
    },
    {
      "module_name": "@minecraft/server",
      "version": "2.6.0"
    }
  ]
}
```

If the add-on has no scripts, remove the script module and native module dependency. If it uses UI, add the verified stable `@minecraft/server-ui` dependency. Keep the installed NPM package versions aligned with manifest dependencies.

Sources: [manifest reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/addonsreference/packmanifest?view=minecraft-bedrock-stable), [official scripted manifest sample](https://github.com/microsoft/minecraft-samples/blob/5e04b6f719c316b0611f569af0cab7d6e9a2fb26/toss_lab/behavior_packs/toss_lab/manifest.json).

## Custom item, texture atlas, and localization

`behavior_pack/items/house_kit.item.json`:

```json
{
  "format_version": "1.21.80",
  "minecraft:item": {
    "description": {
      "identifier": "studio:house_kit",
      "menu_category": {
        "category": "items"
      }
    },
    "components": {
      "minecraft:icon": "studio:house_kit",
      "minecraft:display_name": {
        "value": "item.studio.house_kit.name"
      },
      "minecraft:max_stack_size": 16
    }
  }
}
```

`resource_pack/textures/item_texture.json`:

```json
{
  "resource_pack_name": "Studio DLC Resources",
  "texture_name": "atlas.items",
  "texture_data": {
    "studio:house_kit": {
      "textures": "textures/items/house_kit"
    }
  }
}
```

Place the texture at `resource_pack/textures/items/house_kit.png`. Add this line to `resource_pack/texts/en_US.lang`:

```text
item.studio.house_kit.name=Starter House Kit
```

Source: [official custom item sample](https://github.com/microsoft/minecraft-samples/blob/5e04b6f719c316b0611f569af0cab7d6e9a2fb26/toss_lab/behavior_packs/toss_lab/items/ice_disc.json), [official item texture atlas sample](https://github.com/microsoft/minecraft-samples/blob/5e04b6f719c316b0611f569af0cab7d6e9a2fb26/toss_lab/resource_packs/toss_lab/textures/item_texture.json).

## Shaped crafting recipe

`behavior_pack/recipes/house_kit.recipe.json`:

```json
{
  "format_version": "1.21.20",
  "minecraft:recipe_shaped": {
    "description": {
      "identifier": "studio:house_kit_recipe"
    },
    "tags": ["crafting_table"],
    "pattern": [
      "PPP",
      "PBP",
      "PPP"
    ],
    "key": {
      "P": {
        "item": "minecraft:oak_planks"
      },
      "B": {
        "item": "minecraft:brick_block"
      }
    },
    "unlock": [
      {
        "item": "minecraft:brick"
      }
    ],
    "result": {
      "item": "studio:house_kit",
      "count": 1
    }
  }
}
```

Each pattern row must have the same width. Every non-space symbol must appear in `key`; keys not used in the pattern should be removed.

Source: [official shaped recipe sample](https://github.com/microsoft/minecraft-samples/blob/5e04b6f719c316b0611f569af0cab7d6e9a2fb26/casual_creator/chill_dreams/complete/behavior_packs/mamm_cds/recipes/dream_journal_pencil.json).

## Custom full-cube block, terrain atlas, and drop

`behavior_pack/blocks/builder_table.block.json`:

```json
{
  "format_version": "1.21.80",
  "minecraft:block": {
    "description": {
      "identifier": "studio:builder_table",
      "menu_category": {
        "category": "construction"
      }
    },
    "components": {
      "minecraft:geometry": "minecraft:geometry.full_block",
      "minecraft:material_instances": {
        "*": {
          "texture": "studio_builder_table",
          "render_method": "opaque"
        }
      },
      "minecraft:destructible_by_mining": {
        "seconds_to_destroy": 2.0
      },
      "minecraft:destructible_by_explosion": {
        "explosion_resistance": 6.0
      },
      "minecraft:loot": "loot_tables/blocks/builder_table.json",
      "minecraft:map_color": "#8B5A2B"
    }
  }
}
```

`resource_pack/textures/terrain_texture.json`:

```json
{
  "resource_pack_name": "Studio DLC Resources",
  "texture_name": "atlas.terrain",
  "padding": 8,
  "num_mip_levels": 4,
  "texture_data": {
    "studio_builder_table": {
      "textures": "textures/blocks/builder_table"
    }
  }
}
```

`behavior_pack/loot_tables/blocks/builder_table.json`:

```json
{
  "pools": [
    {
      "rolls": 1,
      "entries": [
        {
          "type": "item",
          "name": "studio:builder_table",
          "weight": 1
        }
      ]
    }
  ]
}
```

Place the texture at `resource_pack/textures/blocks/builder_table.png`. Current block guidance requires `minecraft:geometry` and `minecraft:material_instances` together when either is used in content format 1.21.80 or newer.

Sources: [official custom block sample](https://github.com/microsoft/minecraft-samples/blob/5e04b6f719c316b0611f569af0cab7d6e9a2fb26/casual_creator/gray_wave/behavior_packs/mikeamm_gwve/blocks/gray_ore.block.json), [geometry reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_geometry?view=minecraft-bedrock-stable), [official loot-table sample](https://github.com/microsoft/minecraft-samples/blob/5e04b6f719c316b0611f569af0cab7d6e9a2fb26/custom_features/basic_orange_ore/behavior_packs/basic_orange_ore/loot_tables/blocks/orange_ore.json).

## Summonable trading entity

`behavior_pack/entities/builder.entity.json`:

```json
{
  "format_version": "1.21.80",
  "minecraft:entity": {
    "description": {
      "identifier": "studio:builder",
      "is_spawnable": true,
      "is_summonable": true,
      "is_experimental": false
    },
    "components": {
      "minecraft:type_family": {
        "family": ["studio_builder", "mob"]
      },
      "minecraft:collision_box": {
        "width": 0.6,
        "height": 1.8
      },
      "minecraft:health": {
        "value": 20,
        "max": 20
      },
      "minecraft:physics": {},
      "minecraft:pushable": {
        "is_pushable": true,
        "is_pushable_by_piston": true
      },
      "minecraft:nameable": {},
      "minecraft:trade_table": {
        "display_name": "entity.studio.builder.name",
        "table": "trading/builder_trades.json",
        "convert_trades_economy": true
      }
    }
  }
}
```

`behavior_pack/trading/builder_trades.json`:

```json
{
  "tiers": [
    {
      "total_exp_required": 0,
      "groups": [
        {
          "num_to_select": 1,
          "trades": [
            {
              "wants": [
                {
                  "item": "minecraft:emerald",
                  "quantity": 3
                }
              ],
              "gives": [
                {
                  "item": "studio:house_kit",
                  "quantity": 1
                }
              ],
              "trader_exp": 1,
              "max_uses": 12,
              "reward_exp": true
            }
          ]
        }
      ]
    }
  ]
}
```

The server entity still needs a matching client entity, geometry, texture, and render controller in the RP before it is visually complete. Add `entity.studio.builder.name=Builder` to `resource_pack/texts/en_US.lang`.

Sources: [trade-table tutorial](https://learn.microsoft.com/en-us/minecraft/creator/documents/createtradetable?view=minecraft-bedrock-stable), [`minecraft:trade_table` component](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trade_table?view=minecraft-bedrock-stable), [official client-entity shape](https://github.com/microsoft/minecraft-samples/blob/5e04b6f719c316b0611f569af0cab7d6e9a2fb26/custom_projectiles/resource_pack/entity/custom_snowball.json).

## Script API event handler

`behavior_pack/scripts/main.js`:

```javascript
import { world } from "@minecraft/server";

world.afterEvents.itemUse.subscribe((event) => {
  if (event.itemStack.typeId !== "studio:house_kit") return;

  const player = event.source;
  player.sendMessage("Choose a clear area before placing this house.");
});
```

Use after-events for observation and ordinary follow-up work. Before-events run in restricted execution and may require deferring mutations with `system.run`. Subscribe once at module scope, filter immediately, and do not start one subscription per player.

Source: [stable `@minecraft/server` reference](https://learn.microsoft.com/en-us/minecraft/creator/scriptapi/minecraft/server/minecraft-server?view=minecraft-bedrock-stable), [official event-subscription samples](https://github.com/microsoft/minecraft-samples/blob/5e04b6f719c316b0611f569af0cab7d6e9a2fb26/toss_lab/scripts/main.ts).

## Packaged structure placement

Place a Structure Block export at `behavior_pack/structures/starter_house.mcstructure`. It is addressed as `studio:starter_house` when the first path segment is the namespace folder; if the file is directly inside `structures/`, confirm the identifier produced by the target toolchain.

With a stable 2.x Script API that exposes `world.structureManager`:

```javascript
import { world } from "@minecraft/server";

function placeStarterHouse(player, location) {
  world.structureManager.place(
    "studio:starter_house",
    player.dimension,
    location
  );
}
```

Before calling this in gameplay, validate footprint clearance, world height, chunk loading, orientation, collision with protected builds, item consumption, rollback behavior, and simultaneous multiplayer placement. Do not consume a kit until placement succeeds.

Source: [official structure-placement sample](https://github.com/microsoft/minecraft-samples/blob/5e04b6f719c316b0611f569af0cab7d6e9a2fb26/custom_dimensions/scripts/main.ts), [stable Script API reference](https://learn.microsoft.com/en-us/minecraft/creator/scriptapi/?view=minecraft-bedrock-stable).

## Function-file syntax

`behavior_pack/functions/debug_setup.mcfunction`:

```mcfunction
give @s studio:house_kit 1
summon studio:builder ~2 ~ ~
```

Commands in `.mcfunction` files do not begin with `/`. Keep debugging functions out of the release artifact unless they are intentional support tools.

Source: [commands introduction](https://learn.microsoft.com/en-us/minecraft/creator/documents/commandsintroduction?view=minecraft-bedrock-stable).

## Molang placement-direction condition

Molang appears as a string inside relevant JSON properties. For example, a permutation condition can test a block trait state:

```json
{
  "condition": "query.block_state('minecraft:cardinal_direction') == 'north'",
  "components": {
    "minecraft:transformation": {
      "rotation": [0, 0, 0]
    }
  }
}
```

The exact available queries and context vary by file type. Verify that the chosen query is supported in that block, entity, animation, or render context; syntactically valid Molang can still evaluate incorrectly in the wrong context.

Source: [Molang documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/molangreference/?view=minecraft-bedrock-stable), [block states and traits](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockstateandtraitlistings?view=minecraft-bedrock-stable).

## Verification labels for generated work

Use these exact meanings in handoffs:

- `source-backed`: adapted from a current official schema, documentation page, or official sample.
- `parse-tested`: JSON/JavaScript parsing or TypeScript compilation passed.
- `mct-validated`: Mojang's current `mct validate` passed; include tool version and warnings.
- `import-tested`: the packaged artifact imported and activated in a clean Bedrock installation.
- `gameplay-tested`: named acceptance tests passed in-game, with game/device versions recorded.
- `Marketplace approved`: only after the publisher/Mojang process actually grants approval.

Never use `verified`, `working`, or `production-ready` alone when a more precise label is available.
