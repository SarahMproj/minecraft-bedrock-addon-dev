---
name: minecraft-bedrock-addon-dev
description: Build, edit, debug, validate, and package Minecraft Bedrock Edition add-ons or world-template DLC using behavior packs, resource packs, JSON/Molang, and the Script API. Use for Bedrock custom blocks, items, entities, recipes, loot, trades, structures, UI, gameplay systems, .mcpack, .mcaddon, or .mcworld work; do not use for Java Edition mods, Bukkit/Spigot plugins, or server administration.
---

# Minecraft Bedrock Add-on Developer

Produce a playable, maintainable Bedrock add-on and an evidence-based release assessment. Treat "DLC" as a product/distribution goal: ordinary Bedrock files can be built locally, but Marketplace publication still requires an approved partner or publisher and Mojang review.

## Establish the target

Inspect the existing project and its instructions before editing. When starting from a concept, state reasonable assumptions and ask only about choices that would materially change the architecture, such as:

- stable Bedrock versus Preview/Beta;
- an attachable add-on versus a bundled world template;
- data-driven JSON/Molang versus Script API gameplay;
- required devices, multiplayer behavior, and persistence;
- whether an approved Marketplace publisher is already involved.

Default to the stable channel, an attachable behavior-pack/resource-pack pair, multiplayer-safe mechanics, and no experimental capabilities. Never silently opt into Preview/Beta APIs.

Before choosing format versions, components, manifest dependencies, or Script API versions, verify them against the stable view of the official Creator documentation. Bedrock schemas evolve. Read [references/official-sources.md](references/official-sources.md) when a claim depends on the current platform.

Before authoring a common block, item, recipe, loot table, trader, structure-placement mechanic, or Script API entry point, read the applicable section of [references/bedrock-syntax-patterns.md](references/bedrock-syntax-patterns.md). Its examples are source-backed executable shapes, not substitutes for checking the target version.

## Design before expansion

Convert the concept into a small vertical slice with:

- player fantasy and target audience;
- core loop, inputs, rewards, fail states, and progression;
- content inventory split into must-have, launch, and later items;
- acceptance criteria observable in-game;
- compatibility, multiplayer, performance, localization, and accessibility needs;
- BP/RP/Script API ownership for each feature.

Prefer data-driven components and Molang when they fully express the mechanic. Add scripts only for behavior that genuinely needs event orchestration, dynamic state, UI, or persistence. Read [references/content-architecture.md](references/content-architecture.md) when mapping a feature to pack files.

## Build a working slice

Prefer Mojang's current Minecraft Creator Tools (`mct create`) for a new production project when available. If a dependency-free manual skeleton is useful, run:

```bash
python3 scripts/scaffold_addon.py "Add-on Name" --output <directory> --namespace <namespace> --min-engine-version <major.minor.patch>
```

Use `--script --server-version <stable-module-version>` only after confirming the current stable `@minecraft/server` version. The scaffolder refuses to overwrite an existing project.

Maintain these invariants:

- every pack header and module UUID is unique;
- the behavior pack dependency points to the resource-pack header UUID and exact version when both packs are required;
- identifiers use one lowercase project namespace and remain stable after release;
- filenames, identifiers, texture keys, geometry names, animation names, and localization keys match exactly, including case;
- `min_engine_version` and content `format_version` are selected from the feature requirements, not copied blindly;
- stable content uses manifest format 2 unless official stable documentation says otherwise;
- source TypeScript, secrets, debug artifacts, and build tools do not enter shipped packs;
- third-party code, textures, audio, models, fonts, and brands have documented commercial rights.

Implement the smallest end-to-end interaction first. Add placeholder art only when it lets the mechanic be tested, label it clearly, and keep asset requirements explicit for the production artist.

## Verify behavior

Run fast checks after each coherent change. At minimum:

```bash
python3 scripts/validate_addon.py <project-directory>
npx mct validate <project-directory>
```

The bundled validator catches structural and cross-pack errors; it is not a substitute for Mojang's validator or an in-game run. If the official tool is unavailable, report that verification gap.

Test in a fresh creative world with content logging enabled. Exercise creation, acquisition/crafting, use, destruction/removal, save/reload, death/respawn, multiplayer host/client behavior, and conflicts with a second unrelated add-on. Do not call a mechanic complete from static validation alone. Read [references/quality-and-release.md](references/quality-and-release.md) for the test and release gates.

## Package and hand off

After validation and in-game testing, package attachable packs with:

```bash
python3 scripts/package_addon.py <project-directory> --output <name>.mcaddon
```

Import the produced artifact into a clean Bedrock installation and repeat the smoke test. For a world template, preserve the world's required metadata and export it with the current official Editor/Creator Tools workflow instead of treating a world folder as an ordinary add-on pair.

Hand off:

- source project and importable artifact;
- version/target matrix and required capabilities;
- implemented-versus-planned content inventory;
- exact validation commands and results;
- in-game test evidence and unresolved defects;
- upgrade/save-compatibility notes;
- asset-rights ledger and Marketplace/publisher status.

Never claim "Marketplace approved," "console compatible," or "certified" without the corresponding external review or device evidence.
