# EMM Continued promotions, upgrades and resources — initial implementation

> **Historical progression snapshot:** The counts below describe the earlier 50-unit milestone. The current roster contains **100 units and 31 promotions**, including new Dwarf and Dark Elf racial promotions. The earlier 27 mapped upgrade routes remain the baseline, and newly added faction replacements still need a full upgrade-path audit. See [civilization expansion](civilizations.md).

**Pinned reference:** [bewlay/extramodmod at 60b0ec3740083162aaab7bf8491761a54a65a610](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610).
[Full machine-readable source and porting ledger](data/emm-promotions-upgrades-resources.json).

## Coverage

| Area | Source records | Current implementation |
| --- | ---: | --- |
| Promotions | 305 | 26 EMM-derived + 3 legacy system promotions |
| Unit upgrade definitions | 356 source units | 27 of our 50 units have at least one mapped path |
| Resource types | 68 | 16 in Unciv, including Copper, Mithril and Reagents |
| Unit roster | 356 | 50, including upgrade units Mage, Archmage and Wizard |

### Promotions

Promotions now use EMM's actual **Combat I–V** (+20% each), **City Raider I–III** (+30% attacking cities), **City Garrison I–III** (+30% defending cities), **Mobility I–II**, **Sentry**, **Woodsman**, **Shock**, **Cover**, and **Formation** values. Appropriate EMM technology requirements and promotion prerequisites are preserved where supported. `Channeling I–III` are marker promotions, **not functioning spellcasting**. Orc and Elf promotions approximate their source terrain effects; the Clan of Embers and Ljosalfar receive automatic land-military racial promotion on training via their source default races.

Previously included normal Civ V promotion lines with different effects have been removed, rather than representing them as FfH2.

### Upgrade paths

Where the source class upgrade points to an implemented unit, it is represented with `upgradesTo` and supplemental `Can upgrade to [unit]` uniques for additional paths. Unciv automatically resolves an upgraded unit's civilization-specific replacement, so Amurite upgrades will point to Swordsmen/Wizards and Clan upgrades to their Orc counterparts.

**Limitations:** EMM has more upgrade targets than our current roster, and city/level/trait/religion requirements are not complete. Mage (source minimum level 4) and Archmage (source minimum level 6) are currently trainable after their technology instead of enforcing EMM's civilization-level minimum. That is a temporary simplification.

### Resources

Added **Copper** (Mining), **Mithril** (Mithril Working), and **Reagents** from the resource definitions. Adjusted the visibility of **Horses** and **Iron** to their EMM reveal techs. Their tiles, placement rates and quantities are approximations pending the full terrain conversion.

Source unit dependencies use Unciv's `Can only be built <with [resource]>` to **require access without consuming stockpiled strategic resources**. EMM's resource `ANY of` alternatives are not fully expressible by Unciv, so the current port uses the first available mapped alternative and keeps the full list in source data. For example Horsemen require Horses, while original EMM also allows Nightmares. Mithril and Reagents gates work independently where supported.

This milestone does **not** include magical mana nodes, mana-related promotion requirements, spell effects, heroic actions, resource transformation, or exact civics.

## Validation

The CI pipeline checks source counts and translation traceability, checks technology and unit/building fidelity, and runs Unciv's native `mod-ci`. Android turn-by-turn testing has not yet occurred.

## Known fidelity issues

- Unciv's promotion prerequisites are OR choices; EMM uses a mixture of compulsory + alternative relationships, so complex combinations require approximations.
- FfH2 chance-based first strikes, many promotion side effects, race-specific casting behavior, and healing values are deferred.
- EMM resource requirements do not consume strategic resources in the same way as Unciv; our current `Can only be built` gates approximate resource ownership. The full source alternatives are catalogued.
- Source XP/level requirements for Mage/Archmage are not yet gated.
- Some source upgrades point to units not yet implemented and are intentionally omitted rather than redirecting to unrelated units.

### Validation details

The source-fidelity test also compares Combat I–V, City Raider I–III, Mobility I and Sentry bonuses against the original XML and checks the two faction default-race grants. These are static/engine checks, not proof that every effect behaves identically to Civ IV in a played game.
