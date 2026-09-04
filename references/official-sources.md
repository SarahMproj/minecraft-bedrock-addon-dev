# Official Bedrock sources

Read the stable view first. Use Preview documentation only when the user explicitly chooses Preview/Beta, and label all Preview-dependent output.

## Platform and schemas

- [Minecraft Bedrock Creator Documentation](https://learn.microsoft.com/en-us/minecraft/creator/?view=minecraft-bedrock-stable): primary entry point for current tutorials and JSON, Molang, command, and Script API references.
- [Add-on development workflow](https://learn.microsoft.com/en-us/minecraft/creator/documents/addondevelopmentworkflow?view=minecraft-bedrock-stable): current project layout, local deployment, hot reload, testing, and release workflow.
- [Comprehensive pack contents](https://learn.microsoft.com/en-us/minecraft/creator/documents/comprehensivepackcontents?view=minecraft-bedrock-stable): authoritative folder and file routing for BP/RP content.
- [Manifest reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/addonsreference/packmanifest?view=minecraft-bedrock-stable): header, module, dependency, capability, and metadata fields.
- [Version disambiguation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/versiondisambiguation?view=minecraft-bedrock-stable): differences among manifest format, content format, pack version, minimum engine version, and base game version.
- [Latest platform version guidance](https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/latestplatformversion?view=minecraft-bedrock-stable): current stable versioning guidance and support window.
- [Script API reference](https://learn.microsoft.com/en-us/minecraft/creator/scriptapi/?view=minecraft-bedrock-stable): stable module versions, events, classes, permissions, and examples.

## Tools, validation, and release

- [Minecraft Creator Tools overview](https://learn.microsoft.com/en-us/minecraft/creator/documents/mctoolsoverview?view=minecraft-bedrock-stable): Mojang's `mct create`, `mct add`, and `mct validate` workflows.
- [MCTools validation rules](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/mctoolsvalreference/validationrulesindex?view=minecraft-bedrock-stable): rule meanings and remediations.
- [Troubleshooting add-ons](https://learn.microsoft.com/en-us/minecraft/creator/documents/troubleshootingaddons?view=minecraft-bedrock-stable): Content Log, file-location, identifier, reload, and cache checks.
- [Minecraft file extensions](https://learn.microsoft.com/en-us/minecraft/creator/documents/minecraftfileextensions?view=minecraft-bedrock-stable): `.mcpack`, `.mcaddon`, `.mcworld`, `.mctemplate`, and `.mcproject` meanings.
- [Cooperative add-on guidance](https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/guidelinesforbuildingcooperativeaddons?view=minecraft-bedrock-stable): namespaces, interoperability, file-count, size, and permutation guidance.
- [Minecraft Partner Program](https://www.minecraft.net/en-us/partner): public criteria and process boundary for selling through Marketplace.

## Official samples

- [Mojang Bedrock samples](https://github.com/microsoft/minecraft-samples): official sample packs and scripting projects. Select the branch/tag matching the target stable release; do not assume `main` matches the user's installed game.

## Version decision rule

When creating or revising content:

1. Confirm the user's installed Bedrock release and stable/Preview channel when possible.
2. Open the stable reference for every component or Script API used.
3. Choose the highest `min_engine_version` compatible with the intended audience and all used features.
4. Pin Script API module versions in `manifest.json` and `package.json` consistently.
5. Record the verified date and links in the project handoff.

Do not preserve an obsolete version merely because an old tutorial uses it. Do not raise a version without testing save compatibility and every target device class.
