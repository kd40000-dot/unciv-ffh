# Prototype 0.1a — development snapshot

**Status: not yet tested in Unciv. Do not call this a playable release until tested.**

- Four EMM civilizations with canonical cities from pinned EMM source.
- 31 EMM technologies, reduced costs and simplified OR dependencies.
- 16 prototype units, including Adept, Mage, Wizard, Goblin and Firebow.
- Stock Unciv terrain definitions for functioning climate/map rules.
- Civ-specific bonuses are approximations, not faithful recreation of EMM traits.
- Mana resource exists, but it does not yet power spells; no castable spells or temporary summons implemented.
- EMM religions, Armageddon Counter and many late-game features are deferred.
- Original EMM Civ IV combat/stacks are adapted to Unciv 1UPT.

See `reference/manifest.json` for source and adaptation decisions.

**Android testing:** in Unciv, use the mod download-by-URL option for
`https://github.com/kd40000-dot/unciv-ffh` and select its standalone ruleset.
If the mod does not appear, or game creation fails, record the error. This repo's static checks do not assert a successful game load.
