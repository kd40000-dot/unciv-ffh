# Lanun Pirate Cove → Pirate Harbor → Pirate Port

**Status (October 23, 2026):** All three improvements and the technology-locked, manual Workboat upgrades are implemented as a mod-only alternative to EMM's automatic per-tile maturation. **New upgrades are not yet confirmed in gameplay**, although basic Cove construction was previously user-verified.

**EMM Continued source:** [pinned commit 60b0ec3740083162aaab7bf8491761a54a65a610](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610). Original spell in `XML/Units/CIV4SpellInfos.xml`, stages in `XML/Terrain/CIV4ImprovementInfos.xml`, placement in `python/entrypoints/CvSpellInterface.py`. [Machine-readable source ledger](data/emm-lanun-pirate-coves.json).

## Three distinct tile improvements

| Stage | Required technology | Action cost | Workboat consumed | Food | Production | Gold | Science | Defense |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| Pirate Cove | Fishing (for the Workboat) | 0 Gold | 1 | 0 | 0 | +1 | +1 | +10% |
| Pirate Harbor | Sailing | 100 Gold | 1 | +1 | +1 | +2 | +1 | +20% |
| Pirate Port | Optics | 200 Gold | 1 | +2 | +2 | +2 | +2 | +30% |

All rows are **improvement yields in addition to base Coast yields**. EMM Commerce progression 2→3→4 becomes Gold+Science 1+1→2+1→2+2. These yield values match the original Food and Production. The upgrade costs and technology gates are intentional balance adjustments and **not** in the original EMM maturation system.

**Total investment for a Pirate Port starting from bare Coast: 300 Gold plus three Workboats (30 Production each, total 90 base Production), and research of Fishing, Sailing and Optics.**

## How the mod-only upgrade works

All three stages are distinct, Lanun-exclusive `TileImprovements.json` entries. A Workboat has three native `Can instantly construct a [stage] improvement` actions.

1. Build the original Cove on eligible owned Coast adjacent to Land and lacking a visible resource/improvement. This immediately consumes the first Workboat.
2. After **Sailing**, bring a new Workboat **onto the existing Cove tile**. The special `Create Pirate Harbor` action requires `Can only be built on [Pirate Cove] tiles`. It deducts **100 Gold**, consumes the Workboat, and replaces the Cove with a Harbor.
3. After **Optics**, bring another Workboat onto the **Pirate Harbor**. The `Create Pirate Port` action requires `Can only be built on [Pirate Harbor] tiles`, deducts **200 Gold**, consumes the Workboat, and replaces the Harbor with the final Port.

No direct Cove→Port skip: `Pirate Port` explicitly requires the Harbor stage on that tile. No Harbor/Port can be placed on empty Coast. All three stages use `turnsToBuild: -1` so regular build commands cannot manufacture them; the Workboat's instant-build action is what places them. All actions are Lanun-only.

Unciv's implementation of `ConstructImprovementInstantly` checks the improvement's required technology and its tile placement rules, then `UnitActionModifiers` checks/deducts the `<costs [N Gold] stats>` action fee. The `<by consuming this unit>` modifier destroys the Workboat. `TileImprovementFunctions.setImprovement()` installs the new improvement, replacing the prior stage.

## Known differences from EMM and open QA

- EMM automatically matured an individual Cove after 10 turns and an individual Harbor after another 20 turns. This port **requires paid, manual upgrades**.
- No native mod-only 5-by-5 exclusion radius for nearby Coves/Harbors/Ports. Their spacing restriction is unimplemented.
- Sea tile placement, pillaging and upgrades should be checked in-game, particularly whether the new special actions appear correctly on occupied Coast and whether the Gold cost is displayed and enforced.
- The appearance of Harbor and Port uses Unciv's normal improvement fallback art until dedicated per-stage assets are supplied; we have not claimed original EMM graphics.
- The existing `Pirate Cove` placement rules and consumption are unchanged.

## Test the new mechanic in Unciv

1. Update the mod and start a fresh **Lanun** game; research Fishing, build a Workboat, and make a Cove on eligible coast. Check +1 Gold/+1 Science.
2. Research **Sailing**, keep **at least 100 Gold**, build a second Workboat, move it onto the existing Cove, and choose `Create Pirate Harbor`. Check the unit disappears, treasury drops 100, and the tile is **Pirate Harbor** with +1 Food/+1 Production/+2 Gold/+1 Science, +20% Defense.
3. Verify Harbor cannot be created with **under 100 Gold**, before researching Sailing, or on an empty coastal tile.
4. Research **Optics**, keep **at least 200 Gold**, bring a third Workboat to the Harbor, and choose `Create Pirate Port`. Confirm an additional 200 Gold deducted, unit consumed, and the resulting +2 Food/+2 Production/+2 Gold/+2 Science, +30% Defense.
5. Test the Port action on a Cove tile, before Optics, below 200 Gold, and on empty Coast: it must not be usable.
6. Check non-Lanun workboats, save/load, and repairing pillaged Coves/Harbors.

**CI check:** `python3 tools/verify_lanun_cove.py` statically validates all three improvement definitions, proper predecessor filters, tech requirements, Gold costs, Workboat consumption and source yields. Static verification does not replace in-game testing.
