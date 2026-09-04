# Craftable Houses — Status Log

**Product:** Craftable Houses
**Phase:** Alpha production / first playable vertical slice
**Current milestone:** Craft → use → place one complete Plains Starter Cottage safely in Survival
**Status updated:** 2026-09-04

## Status dashboard

| Category | Status | Current state | Next gate |
|---|---|---|---|
| Bedrock engineering capability | 🟢 Strong | Shared Bedrock skill, source-backed syntax references, scaffold/validator/packager exist | Validate this pack against current target Bedrock build |
| DLC portfolio / product strategy | 🟢 Defined | Craftable Houses is Pack 01 of the opening DLC trilogy; intended as an expandable biome/theme drop system | Freeze launch SKU and update cadence |
| Content design | 🟡 In production | Launch architecture = biome-based house kits; first vertical slice is Plains Starter Cottage | Lock Pack 01 house roster and recipe matrix |
| Brand / visual universe | 🟡 Emerging | Cozy, collectible, immediately legible house-kit fantasy; structures should feel Minecraft-native rather than imported prefab art | Formalize palette, icon language, naming rules, screenshot style |
| Competitive research | 🟡 Pending consolidation | Category and competitor research identified as required before commercial positioning is frozen | Build current Marketplace competitor/pricing/review matrix |
| Behavior Pack / Resource Pack implementation | 🟡 Started | Alpha pack manifests, first custom house-kit item, recipe, localization, item atlas and placement script are being created | Add real `.mcstructure`, clearance logic and validated consumption flow |
| Models / textures / icons | 🟡 Spec stage | First kit icon slot and structure art direction defined; production asset not yet final | Produce final 16/32px kit icon and house structure |
| Playable package | 🔴 Not yet | Packaging tooling exists; product is not yet a complete `.mcaddon` | Produce first alpha package after real structure asset exists |
| Device / multiplayer testing | 🔴 Not yet | No in-game test session recorded | Windows Bedrock content log → multiplayer → console/mobile matrix |
| Publisher / Marketplace track | 🔴 Not selected | Commercial publishing partner still required | Identify and approach qualified partner after vertical slice |
| Creator GTM / gameplay capture | 🟡 Strategy defined | Creator reviews, gameplay reels and drop-based fandom strategy are planned | Capture first satisfying craft/place transformation clip |
| Current milestone | 🟡 Active | Plains Starter Cottage vertical slice | Achieve reliable Survival craft-and-place loop |
| Blockers / risks | 🟡 Known | Real structure binary, placement UX/clearance, final art assets, in-game validation, Marketplace partner | Resolve in vertical-slice order |

## Session log

### 2026-09-04 — Production kickoff

**Start**
- Converted Craftable Houses from concept/pre-production into an explicit product project.
- Established the rule that every DLC maintains this same status dashboard and gets updated every work session.

**Threshold**
- Chose one-house vertical-slice development instead of attempting the entire catalog at once.
- First alpha target: `Plains Starter Cottage`.

**Odyssey**
- Began BP/RP project structure.
- Defined first house-kit item and shaped Survival recipe.
- Began Script API placement path for a packaged `.mcstructure`.

**Realization**
- The reusable product primitive is not “a house”; it is **House Kit = recipe + item + icon + structure + placement rules + safety checks + localization + test case**. Once one primitive is proven, the catalog can scale systematically.

**Internal change**
- Project status changes from late pre-production to **alpha production**.

**External change**
- Product files now begin living under a dedicated Craftable Houses project path rather than only as generic skill examples.

**Stop / handoff**
- Next work session begins with creation/import of the actual Plains Starter Cottage `.mcstructure`, final placement/consumption behavior, validation, and first package build.

## Definition of vertical-slice done

The first house is only considered **validated** when all are true:

- Player can obtain ingredients in Survival.
- Crafting-table recipe produces exactly one Plains Cottage Kit.
- Kit has a final icon and localized display name.
- Using the kit places the intended structure in the correct dimension/location.
- Placement checks prevent obvious destructive overlap and invalid world-height placement.
- Kit is consumed only after successful placement.
- Failure leaves the kit in inventory and gives useful feedback.
- Structure behaves correctly when two players attempt placement.
- Content Log has no release-blocking errors.
- Pack passes local validator and Mojang validation available for the target release.
- `.mcaddon` installs cleanly in a fresh test world.

## Next session priorities

1. Build/import `craftable:plains_starter_cottage` structure.
2. Implement clearance + placement-success + item-consumption logic.
3. Produce final kit icon and localization pass.
4. Validate BP/RP identifiers and pack linkage.
5. Package Alpha 0.1 and run the first in-game test.
6. Record bugs here before expanding to House 02.
