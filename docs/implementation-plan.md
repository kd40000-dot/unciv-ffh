# Implementation plan

## Authoritative game data

ExtraModMod Continued upstream: https://github.com/bewlay/extramodmod

Use XML for unit/building/technology/civilization definitions, Python and C++ for implemented mechanics, and the changelog for version-dependent behavior. Record the upstream commit before importing data. Confirm whether assets may be redistributed before adding any upstream art/audio to this repository.

## Architecture

- Deliverable: an Unciv `isBaseRuleset` mod with files in `jsons/` and, later, game assets in appropriate Unciv folders.
- Prefer stock Unciv mechanisms and valid Unciv uniqueness strings. Do not assume arbitrary FfH2-specific code can be defined by JSON.
- Keep gameplay values traceable to ExtraModMod Continued source entries.
- Define automated JSON/schema/reference checks and validate using the game's ruleset validator before labeling a build playable.

## Milestones

1. **Data inventory:** pin upstream revision; extract factions, techs, religions, civics, units, promotions, buildings, resources, improvements, terrains, spells, and victory mechanics. Establish mapping to Unciv format and count each category.
2. **Playable foundation:** implement the smallest internally consistent Unciv base ruleset, a starting scenario with a few representative factions, tech progression, units, and cities. Test loading and turn advancement.
3. **Full ordinary ruleset:** add all feasible definitions and unique civilization differences, preserving prerequisite chains and balance values.
4. **Magic and religion:** implement mana sources, sphere promotions, caster ranks, available spell actions and religious progression. Document every proxy or omission.
5. **Advanced systems:** heroes, world spells, global Armageddon Counter, exploration events, terrain conversion, and AI compatibility; isolate engine changes when essential.
6. **Art, UX, and regression:** improve presentation, validate mod installation on Android and desktop, test AI turns and repeatable games.

## Definition of done (for each milestone)

- Every added JSON file parses.
- All references to objects and uniques are valid for the targeted Unciv version.
- No significant FfH2 mechanic is claimed supported without an actual game test.
- All deviations from ExtraModMod Continued appear in `docs/compatibility.md`.
