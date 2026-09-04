# Content architecture

Use this guide to decide which Bedrock system owns a feature. Verify each exact schema in the official stable reference before implementation.

| Need | Primary implementation | Typical supporting files |
| --- | --- | --- |
| Custom block | Behavior pack block definition | RP textures, terrain texture atlas, geometry/material instances, localization, loot and recipe files |
| Custom item/tool/food | Behavior pack item definition | RP item texture atlas and texture, localization, recipes |
| Mob/NPC | BP entity, components, component groups, events | RP client entity, geometry, textures, animations, animation/render controllers, sounds |
| Crafting/cooking | BP recipe definitions | Items/blocks being produced, localization, unlock/test plan |
| Drops and rewards | BP loot tables and entity/block references | Items, functions, progression logic |
| Villager-like trade system | BP trade tables plus entity trade component | Items, dialogue/UI or scripts only if standard trading is insufficient |
| Spawn behavior | BP spawn rules | Biome filters, entity definition, performance caps |
| Structure/building | `.mcstructure` assets loaded by features, commands, or scripts | Preview placement, collision/clearance rules, rotation, loot and NPC setup |
| World generation | BP features and feature rules | Structures, custom blocks, biome/dimension configuration when required |
| Visual animation | RP animations and controllers with Molang | Entity/block/item state exposed by BP |
| Particles and sound | RP particle/sound definitions and assets | BP events, animation events, commands, or scripts that trigger them |
| Branching NPC dialogue | BP dialogue scenes and NPC commands | Localization and optional scripts for stateful consequences |
| Dynamic UI | Stable `@minecraft/server-ui` Script API | BP script module, state model, cancellation/error handling |
| Event-driven game system | Stable `@minecraft/server` Script API | BP script module, objective/dynamic-property persistence, multiplayer ownership |
| Fixed adventure/map | World or world template with embedded packs | Spawn, gamerules, localization, onboarding, reset/upgrade strategy |

## Architecture rules

- Keep the behavior pack authoritative for gameplay and the resource pack authoritative for client presentation.
- Treat the server/world as authoritative in multiplayer. Never assume the initiating player is the only participant.
- Subscribe to events once, filter early, and avoid scanning all entities/blocks every tick.
- Prefer scheduled batches and bounded searches to unbounded per-tick work.
- Use stable identifiers as save-file contracts. Renaming an identifier after release can strand placed blocks, items, entities, or persisted data.
- Version dynamic-property schemas. Include a migration or an explicit save-breaking notice when stored state changes.
- Design custom blocks/items to coexist with other add-ons: unique namespace, narrow tags, no global replacement unless the product requires it, and conservative vanilla modification.
- Separate authored content data from orchestration code so large catalogs (houses, crops, recipes, villagers) can be generated and validated consistently.

## Catalog-driven DLC

For repeatable content such as craftable houses or recipes, maintain one source-of-truth catalog per content family. Each entry should include:

- stable identifier and localization key;
- acquisition/crafting inputs and output;
- tier, progression gate, tags, and rarity;
- BP/RP asset references;
- balance values and platform budget;
- test fixture/command and expected result;
- source/license/artist attribution.

Generate repetitive JSON from the catalog when practical, but keep generated output reviewable and deterministic. Validation should detect missing assets, duplicate identifiers, broken recipes, unreachable progression, and mismatched localization.
