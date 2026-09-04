# Minecraft Bedrock Add-on Developer Skill

An installable Codex skill for building, debugging, validating, and packaging Minecraft Bedrock Edition add-ons and world-template DLC.

The guidance and examples use real Bedrock JSON, Molang, JavaScript, pack, and Script API patterns. Syntax references are grounded in Microsoft Learn and Mojang's public `minecraft-samples` repository; they are not invented pseudo-syntax. Because Bedrock schemas change, the skill requires checking current stable Creator documentation before selecting format or API versions.

## What it covers

- Behavior-pack and resource-pack architecture
- Manifests, UUID linkage, identifiers, and versioning
- Custom blocks, items, entities, recipes, loot, trades, and structures
- Molang and Script API decisions
- Add-on scaffolding, structural validation, and `.mcaddon` packaging
- Multiplayer, compatibility, release, asset-rights, and Marketplace handoff checks

It intentionally does not cover Java Edition mods, Bukkit/Spigot plugins, or server administration.

## Install

Clone the repository into your Codex skills directory:

```bash
git clone https://github.com/SarahMproj/minecraft-bedrock-addon-dev.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/minecraft-bedrock-addon-dev"
```

Restart or reload Codex so it discovers the skill. It can then activate automatically for Bedrock add-on work, or you can invoke it explicitly as `$minecraft-bedrock-addon-dev`.

## Example requests

```text
Use $minecraft-bedrock-addon-dev to scaffold a stable Bedrock add-on with linked behavior and resource packs.

Use $minecraft-bedrock-addon-dev to diagnose why this custom item does not appear in-game.

Use $minecraft-bedrock-addon-dev to validate and package this project as an .mcaddon.
```

## Included tools

```bash
# Create a dependency-free BP/RP skeleton.
python3 scripts/scaffold_addon.py "Add-on Name" \
  --output ./addon \
  --namespace example \
  --min-engine-version 1.21.0

# Run local structural and cross-pack checks.
python3 scripts/validate_addon.py ./addon

# Package a validated project.
python3 scripts/package_addon.py ./addon --output addon.mcaddon
```

The bundled validator complements—but does not replace—Mojang's current validator and an in-game test on the target Bedrock release.

## Source policy

Platform claims and examples are based on primary sources:

- [Minecraft Creator documentation](https://learn.microsoft.com/en-us/minecraft/creator/)
- [Minecraft Bedrock samples](https://github.com/microsoft/minecraft-samples)
- [Minecraft Partner Program](https://www.minecraft.net/en-us/partner)

See `references/official-sources.md` and `references/bedrock-syntax-patterns.md` for the detailed source map and verification status.

## Project status

This is an independent, early-stage developer skill. It can help create ordinary Bedrock add-on files, but it does not grant Marketplace access or imply that content is approved, certified, or compatible with every Bedrock device. Marketplace publication still requires the applicable publisher/partner and Mojang review process.

## License

Released under the [MIT License](LICENSE). Minecraft is a trademark of Microsoft. This project is not affiliated with or endorsed by Microsoft or Mojang.
