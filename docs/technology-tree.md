# EMM Continued complete technology tree — first conversion

**Upstream commit:** [60b0ec3740083162aaab7bf8491761a54a65a610](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610)  
**Source file:** `XML/Technologies/CIV4TechInfos.xml`  
**Machine-readable original semantics:** [`docs/data/emm-technologies.json`](data/emm-technologies.json)

## Coverage

- **84** EMM technology definitions accounted for.
- **82** positive-cost, researchable technologies converted into Unciv's `Techs.json`.
- **2** negative-cost/special entries retained in the reference dataset but not made normally researchable: **Never** (disabled) and **Seafaring** (cost -1). Fishing's normal Exploration research path is available.
- Exact EMM `iCost`, `iGridX` and `iGridY` preserved for all 82 regular technologies.
- All **AND** prerequisites and every single-choice prerequisite are preserved.
- **Future Tech** is marked repeatable using Unciv's `Can be continually researched` unique.

## Technology prerequisite compatibility

Civilization IV supports the formula **ALL `AndPreReqs` PLUS ANY ONE `OrPreReqs`**. Unciv's ordinary `prerequisites` property supports ALL requirements but not OR. For the **11** technologies that have multiple OR alternatives, this version chooses the **first EMM-listed alternative**, preserving all AND requirements. This is a temporary gameplay limitation; no original alternatives were discarded from the source reference JSON.

| Technology | EMM alternatives (ANY ONE) | Temporary Unciv requirement |
| --- | --- | --- |
| Archery | Hunting / Mining | Hunting |
| Commune with Nature | Hidden Paths / Arete / Fanaticism | Hidden Paths |
| Divine Essence | Commune with Nature / Theology / Righteousness / Malevolent Designs / Rage | Commune with Nature |
| Fishing | Exploration / Seafaring | Exploration |
| Malevolent Designs | Infernal Pact / Mind Stapling | Infernal Pact |
| Omniscience | Strength of Will / Pass Through the Ether / Divine Essence | Strength of Will |
| Righteousness | Orders from Heaven / Honor | Orders from Heaven |
| Sanitation | Construction / Bronze Working | Construction |
| Sorcery | Alteration / Divination / Elementalism / Necromancy | Alteration |
| Stirrups | Archery / Animal Handling | Archery |
| Trade | Horseback Riding / Sailing | Horseback Riding |

This means, for example, that **Archery** requires Hunting in this version even though EMM also accepts Mining. Special Seafaring is not a researchable route to Fishing.

## Era compatibility

EMM's original eras are `ERA_ANCIENT`, `ERA_CLASSICAL`, `ERA_MEDIEVAL`. Unciv assigns one era per *column*, so the port uses:

- Columns 1–2: **Ancient era**
- Columns 3–5: **Classical era**
- Columns 6–9: **Medieval era**

The 2 source-era discrepancies are:

- **Festivals**: source era ERA_ANCIENT, but Unciv's column 3 is Classical era.
- **Infernal Pact**: source era ERA_MEDIEVAL, but Unciv's column 5 is Classical era.

All 82 technology descriptions keep their source names, research costs and tree positions. Special research rules like non-tradeability, first-discovery rewards and Civ IV-specific tech effects are **not implemented yet**.

## Validation

Run `python3 tools/verify_tech_tree.py` to check:

1. Full upstream source coverage and correct non-researchable entries.
2. Counts, names, costs, grid positions, repeatability, eras, and prerequisites.
3. Uniqueness, all technology references, and acyclic progression.

The existing GitHub Actions workflow runs this verifier and Unciv's official `mod-ci` ruleset validator after changes.

## Gameplay scope

Technologies are **researchable**, but this milestone does not yet port their complete gameplay unlocks. The units/buildings/resources from the original slice remain provisional. Full tech-specific effects and research rewards will be added with units, buildings, magic, religions and later milestones.
