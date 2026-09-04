# Quality and release gates

## Static gate

- Parse every shipped JSON file without comments or trailing commas.
- Run TypeScript type checking, linting, formatting checks, and production bundling when scripts are used.
- Run the bundled structural validator and Mojang's current `mct validate` suite.
- Resolve all errors. Triage warnings explicitly; do not hide them by disabling rules.
- Confirm UUID uniqueness, exact BP/RP dependency versions, script entry paths, namespaces, and localization coverage.
- Scan the package for source maps, `.env` files, credentials, temporary files, editor caches, tests, raw source art, and unlicensed assets.

## In-game functional gate

Use a fresh test world and keep Content Log enabled. Test at least:

1. Both packs import, activate, and load without Content Log errors.
2. Every launch item/block/entity/structure can be acquired or triggered through intended survival progression.
3. Creative acquisition commands work for diagnostics.
4. Placement, interaction, crafting, damage, death/destruction, pickup/drop, and cleanup behave correctly.
5. State survives save/quit/reload and, when applicable, world upgrades.
6. Two players test host/client ownership, simultaneous actions, disconnect/reconnect, permissions, and late join.
7. The feature behaves at chunk boundaries and after chunks unload/reload.
8. A second unrelated add-on can load alongside it without identifier or global-behavior collisions.
9. Mobile/low-end settings remain usable; multiplayer and dedicated-server targets receive their own evidence.
10. Localization fallback, controller input, touch input, and accessibility-facing text are checked where relevant.

Textures, models, and sounds generally require a full world exit/re-entry to verify; do not rely on `/reload` for them.

## Performance gate

- Avoid unbounded tick loops, entity scans, command spam, particle floods, and explosive permutation counts.
- Track uncompressed bytes and file count. Treat 25 MB and 3,500 files as conservative cooperative-add-on warning thresholds; investigate before exceeding them.
- Test dense worst-case placement/spawn scenarios, not only a clean demo world.
- Measure scripts under simultaneous multiplayer actions and after long sessions.

## Packaging gate

An `.mcpack` is a ZIP containing one pack at its archive root. An `.mcaddon` is a ZIP containing `.mcpack` and/or `.mcworld` files. After packaging:

- inspect the archive layout;
- import into a clean Bedrock installation;
- verify displayed names, icons, versions, and dependencies;
- activate it in a new world and repeat the smoke test;
- retain an immutable copy of the shipped source commit and artifact checksum.

Use semantic release versions. Bump every linked dependency version consistently. Document whether an update is save-compatible and how existing worlds migrate.

## Marketplace-readiness gate

Marketplace readiness is broader than a valid `.mcaddon`. Maintain evidence for:

- original, polished, commercially licensed content;
- clear onboarding and age-appropriate text;
- complete launch content and no debug/placeholder assets;
- key art, screenshots, trailer/gameplay capture, title, short/long descriptions, and feature bullets;
- tested device/platform matrix and multiplayer claims;
- localization plan and text inventory;
- changelog, support contact, known issues, and update policy;
- publisher/partner ownership, submission status, and reviewer feedback.

The public Partner Program describes eligibility and submission expectations but does not expose every review rule. Report a project as `technically validated`, `import-tested`, `publisher review pending`, or `Marketplace approved` according to actual evidence. Never collapse those states into one claim.
