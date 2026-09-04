# Craftable Houses — Status Log

**Product:** Craftable Houses
**Phase:** Alpha production / first playable vertical slice
**Current milestone:** Validate and safely place the generated Plains Starter Cottage in Bedrock
**Status updated:** 2026-09-04

## Status dashboard

| Category | Status | Current state | Next gate |
|---|---|---|---|
| Bedrock engineering capability | 🟢 Strong | Shared Bedrock skill, source-backed syntax references, scaffold/validator/packager exist | Validate this pack and generated structure against target Bedrock build |
| DLC portfolio / product strategy | 🟢 Defined | Craftable Houses is Pack 01 of the opening DLC trilogy; expandable biome/theme drop system | Freeze launch SKU/update cadence after first playtest |
| Content design | 🟢 Vertical slice frozen | Plains Starter Cottage spec is frozen at 11×8×9; launch Village Collection roster is defined | Apply house primitive to Desert Courtyard House after alpha validates |
| Brand / visual universe | 🟡 Emerging | Cozy, collectible, Minecraft-native house-kit fantasy; Plains silhouette language established | Produce final kit icon and screenshot style |
| Competitive research | 🟡 Pending consolidation | Competitor/pricing/review matrix remains a commercial-positioning task | Complete before Marketplace packaging/partner pitch |
| Behavior Pack / Resource Pack implementation | 🟡 Advanced alpha | Linked manifests, kit item, recipe, placement script, deterministic structure generator and packaged `.mcstructure` now exist | Add clearance, orientation, success confirmation and Survival consumption |
| Models / textures / icons | 🟡 Structure built / icon pending | First actual house structure asset exists; item icon/resource atlas still pending | Finalize cottage art polish and kit icon |
| Playable package | 🟡 Structure-ready | Core product files now include the real cottage structure; full `.mcaddon` not yet built/tested | Complete placement safety + RP assets, then package Alpha 0.1 |
| Device / multiplayer testing | 🔴 Not yet | No in-game structure load or placement test recorded yet | Windows Bedrock Content Log + four rotations + 2-player race |
| Publisher / Marketplace track | 🔴 Not selected | Commercial publishing partner still required | Approach after vertical slice demonstrates clean gameplay |
| Creator GTM / gameplay capture | 🟡 Strategy defined | Creator reviews, gameplay reels and transformation clips planned | Capture first successful craft → place moment |
| Current milestone | 🟡 Active | Generated `craftable:plains_starter_cottage` is committed | Confirm Bedrock parses/loads it, then harden placement loop |
| Blockers / risks | 🟡 Narrowed | In-game structure validation, placement UX/clearance, final icon/RP assets, recipe economy | Resolve in vertical-slice order |

## Session log

### 2026-09-04 — Production kickoff

**Start**
- Converted Craftable Houses from concept/pre-production into an explicit product project.
- Established the rule that every DLC maintains this same status dashboard and gets updated every work session.

**Threshold**
- Chose one-house vertical-slice development instead of attempting the entire catalog at once.
- First alpha target: `Plains Starter Cottage`.

**Odyssey**
- Created linked BP/RP manifests.
- Added `craftable:plains_cottage_kit` and shaped mechanics-test recipe.
- Added Script API structure placement path.
- Defined the Pack 01 Village Collection and Building Bundle economy architecture.

**Realization**
- The reusable product primitive is **House Kit = recipe + item + icon + structure + placement rules + safety checks + localization + test case**.

**Internal change**
- Project moved from late pre-production to alpha production.

**External change**
- Product files now live under a dedicated Craftable Houses project path.

### 2026-09-04 — Plains Starter Cottage structure build

**Start**
- Took the first house from a visual target to a deterministic build specification.

**Threshold**
- Froze the alpha structure at `11×8×9` with a `9×7` enclosed core and a centered front entry.

**Odyssey**
- Designed cobblestone foundation, oak plank shell, oak-log frame, symmetrical glass windows, stepped gable roof, chimney, crafting table and bookshelf utility.
- Generated an exact structural BOM: 209 oak planks, 32 oak logs, 35 cobblestone, 22 glass, 2 bookshelves, 1 crafting table.
- Added `PLAINS_STARTER_COTTAGE.md` as the source design spec.
- Added dependency-free `tools/generate_plains_starter_cottage.py`.
- Generated and committed `behavior_pack/structures/craftable/plains_starter_cottage.mcstructure`.
- Exterior empty cells use structure void while interior clear-space cells use explicit air to reduce accidental terrain erasure.

**Realization**
- Structures should be generated from reproducible source definitions wherever practical. This gives us exact dimensions, BOMs, repeatability and easier iteration rather than treating `.mcstructure` binaries as opaque assets.

**Internal change**
- The first cottage is no longer a concept or missing binary; it is an actual generated Bedrock structure candidate.

**External change**
- `craftable:plains_starter_cottage` now exists in the branch at the path expected by the placement script.

**Stop / handoff**
- Next work session begins with in-game structure parsing/placement validation, then orientation + clearance + consume-on-success behavior.

## Definition of vertical-slice done

The first house is only considered **validated** when all are true:

- Player can obtain ingredients in Survival.
- Crafting-table recipe produces exactly one Plains Cottage Kit.
- Kit has a final icon and localized display name.
- Bedrock recognizes `craftable:plains_starter_cottage` from the behavior pack.
- Using the kit places the intended structure in the correct dimension/location.
- Placement checks prevent obvious destructive overlap and invalid world-height placement.
- Player-facing orientation is predictable in all four directions.
- Kit is consumed only after successful placement.
- Failure leaves the kit in inventory and gives useful feedback.
- Structure behaves correctly when two players attempt placement.
- Content Log has no release-blocking errors.
- Pack passes local validation plus available Mojang validation for target release.
- `.mcaddon` installs cleanly in a fresh test world.

## Next session priorities

1. Load generated `.mcstructure` in target Bedrock build and confirm `getPackStructureIds()` sees it.
2. Test raw placement and visually inspect cottage against `PLAINS_STARTER_COTTAGE.md`.
3. Implement four-direction orientation and anchor offsets.
4. Implement conservative footprint/world-height clearance checks.
5. Implement consume-on-success in Survival with no-consume failure path.
6. Add final item atlas/localization/icon assets.
7. Package Alpha 0.1 and record the first in-game test results here.
