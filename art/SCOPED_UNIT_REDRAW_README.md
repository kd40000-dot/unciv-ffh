# Reduced EMM unit sprite scope

The active worklist is [SCOPED_UNIT_REDRAW_QUEUE.json](./SCOPED_UNIT_REDRAW_QUEUE.json), not the older full [REDRAW_QA.json](./REDRAW_QA.json).

## Scope from current jsons/Units.json
- 33 shared trainable base unit types. The active queue contains 32 generic entries (one is already covered by approved existing artwork) plus nation-specific representations.
- 67 civilization-unique unit types, including Doviello Lucian. A civ-unique that is unbuildable but a permanent named hero is kept; summoned/spell-created units are not.
- 688 *existing placeholder image paths* require new artwork in the reduced queue. A base unit such as Warrior has distinct artwork per applicable civilization. This is not a count of distinct unit definitions.
- All images in the active queue currently fail artistic acceptance and must be redrawn, not recolored.

## Exclusions
- Existing approved Amurite sprites, all Workers and Settlers
- Summons, temporary spell-created entities, Lich, and other unbuildable neutral entities
- Items, equipment, buildings, improvements, objects, spell effects and icons

## Acceptance
**Both** quality/style parity with approved Amurite artwork **and** civilization/race identity with appropriate colors must independently pass visual review. No image may be auto-approved by a Python script, by file format checks, or by GitHub Actions succeeding. Keep each rejected image labeled as a placeholder.

## Audit notes
These numbers derive from the currently implemented 125 unit definitions in `jsons/Units.json`, not the entire EMM source game's roster. The subset will need updating if units are added. Existing placeholders remain in the repository for backwards compatibility until replacements pass review. This commit changes the worklist only: it does not claim any artwork has passed.

To prevent confusion, all future redesigns must update `SCOPED_UNIT_REDRAW_QUEUE.json` in addition to the general placeholder manifest.
