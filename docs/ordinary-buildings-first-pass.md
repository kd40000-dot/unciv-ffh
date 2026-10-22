# Ordinary buildings — gameplay completion pass (2026-10-22)

Checkpoint: `checkpoint/pre-ordinary-buildings-2026-10-22`.

The original EMM source inventory (`docs/data/emm-unit-building-catalog.json`, pinned commit `60b0ec3740083162aaab7bf8491761a54a65a610`) often has **no standard yield changes** for buildings whose effects derive from Civ IV health, maintenance, specialists, unit production modifiers, and custom code. Consequently the following additions are **playability proxies**, *not verified EMM source-exact bonuses*. Review them before claiming source fidelity.

## Newly functional or improved
- Monument: +1 Culture (provisional early border-growth function).
- Theatre: +3 Culture (provisional cultural function).
- Inn, Harbor: +1 Gold each (provisional trade substitutes).
- Lighthouse, Aqueduct, Herbalist: +1 Food each; Infirmary: +2 Food. These are explicit health/coastal food playability approximations, NOT the same as Civ IV health.
- Courthouse: +2 Gold as a **fixed maintenance proxy**. EMM source has **-40% city maintenance**, which is *not* a fixed yield. This currently changes balance.
- Command Post: newly trained Military units receive 2 XP (provisional training proxy).
- Training Yard: Sword +2 XP; Hunting Lodge: Scout +2 XP; Stable: Mounted +2 XP; Siege Workshop: Siege +2 XP; Shipyard: Melee Water +2 XP. Unciv supports `New [baseUnitFilter] units start with [amount] XP [cityFilter]` but these source experience quantities are **not independently verified**.

These fixes should be treated as a test candidate, not a final economic balance conversion. Existing unit-unlock requirements remain in place.

## Known important omissions
- Source-exact Culture and specialist effects for Monument, Theatre and other buildings still require extraction from additional source tags and script.
- Warrens: unit duplication; faction buildings: Arena, Reliquary, Grigori Tavern, Forum, Lanun Harbor, Sculptors Studio; magical Obsidian Gate.
- Civ IV health model, trade-route calculations, unit/domain experience modifiers, global effects and city maintenance require fuller equivalents.
- Some buildings (e.g. Mage Guild) already function as unit prerequisites and are deferred to the magic milestone.

## Test
- Check Unciv Options → Locate mod errors after updating.
- Build Monument and Theatre in a city without Culture and verify positive per-turn Culture.
- Build Training Yard/Hunting Lodge/Stable and compare freshly trained unit XP.
- Verify Harbor coastal restriction and any gold bonuses.
- Compare food and population growth before and after health proxy buildings.

Static JSON parsing does not establish that new building uniques are recognized or that they reproduce EMM gameplay.
