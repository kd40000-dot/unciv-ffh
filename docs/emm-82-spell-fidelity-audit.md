# Audit of 82 spell definitions — EMM source fidelity

**Date:** October 24, 2026. **Development branch:** `feature/expanded-magic-2026-10-24` (unchanged frozen playtest branch `magic-test-2026-10-24`). **Authoritative source:** ExtraModMod Continued `CIV4SpellInfos.xml`, pinned commit `60b0ec3740083162aaab7bf8491761a54a65a610`, with related promotion and Python definitions.

## Classification method

- **Perfect:** Source-equivalent targets, stats, cast permissions, costs, timing/expiry, side effects and unit interactions; confirmed in gameplay. **No spell meets this bar yet.**
- **Very close:** Central gameplay effect, primary conditions and numerical values reproduced natively, with relatively narrow differences such as XP inheritance, source subtypes, limited target/terrain scope or cap bookkeeping; still requires Android verification.
- **Significant differences:** Outcome, target, duration, secondary effects or game-state behavior materially differs; may be only a proxy, or no distinct executable cast exists. Do not interpret presence of a promotion or code definition as complete implementation.

**Totals:** 0 perfect, 7 very close, 75 significant = 82 audited EMM records. The phrase “82 implemented” historically includes EMM spell definitions covered by the mod's sphere system even when source variants are merged or no distinct action exists (especially **RIFT_OPEN** and **RESSURECTION_GRAVEYARD**). Thus the completion percentage is *coverage*, not 82 mechanically complete spells. These ratings describe code/source fidelity, not Android-verified results.

## Perfect representation (0)

None established. Passing Unciv `mod-ci` is parser/ruleset validation, not proof of identical game mechanics.

## Very close representation (7)

| EMM spell | Source effect | Native Unciv implementation | Remaining gap |
|---|---|---|---|
| RAISE SKELETON | summons SKELETON; EMM Python action/condition | Free [Skeleton (Summoned)] appears <for all movement> | EMM permanent Strength 2, Movement 1 Skeleton; native mod creates those stats and caps them at three per civilization rather than the EMM caster limit. |
| VITALIZE | EMM Python action/condition | Turn this tile into a [Grassland] tile <for all movement> <in [Plains] tiles> <in [your] tiles> <in [unimproved] tiles> ; Turn this tile into a [Plains] tile <for all movement> <in [Desert] tiles> <in [your] tiles> <in [ | Reproduces principal owned-tile Desert→Plains→Grassland, Snow→Tundra→Plains and Marsh→Grassland steps; EMM feature/scrub and hell terrain conversions missing. |
| UPGRADE DOVIELLO AXEMAN | special native/source action | Existing or new unit/civilization specific action; see source differences and Android QA | Native Bronze Working Warrior→Sons of Asena and 30 Gold cost; minor native-transform retention/animation differences possible. |
| UPGRADE DOVIELLO BATTLEMASTER | special native/source action | Existing or new unit/civilization specific action; see source differences and Android QA | Native Iron Working Warrior→Battlemaster for 100 Gold; minor source unit promotion transfer/AI differences possible. |
| UPGRADE DOVIELLO CHAMPION | special native/source action | Existing or new unit/civilization specific action; see source differences and Android QA | Native Iron Working Axeman/Sons→Battlemaster for 70 Gold; minor unit state transfer/AI differences possible. |
| UPGRADE DOVIELLO WARRIOR | EMM Python action/condition | Existing or new unit/civilization specific action; see source differences and Android QA | Worker→Beastman for 20 Gold (Doviello), source human behavior reproduced; AI special requirement unavailable. |
| UPGRADE DOVIELLO WARRIOR SLAVE | EMM Python action/condition | Existing or new unit/civilization specific action; see source differences and Android QA | Slave→Beastman for 20 Gold (Doviello), but slave acquisition remains a separate incomplete feature. |

## Significant differences (75)

| EMM spell | Source effect | Mod action/proxy | Key differences |
|---|---|---|---|
| BLAZE | EMM Python action/condition | Can instantly construct a [Smoke] improvement <for all movement> | Smoke is placed rather than EMM's fire spreading/expiration and broader wildfire behavior. |
| BLESSING | city spell BLESSING | Gain a free [Blessing (Spell)] [in this city] <for all movement> <in [City center] tiles> | Source +20% living-unit production and specialist; mod approximates Land-unit production but lacks specialist and caster-dependent removal. |
| BLINDING LIGHT | grants BLINDED | [This Unit] gains the [Blinding Light (Spell)] status for [2] turn(s) <for all movement> | EMM gives resisted Blinded to hostile units in radius 1; mod merely debuffs nearby enemy combat strength. |
| BLUR | grants BLUR | [This Unit] gains the [Blur (Spell)] status for [2] turn(s) <for all movement> | EMM removes first-strike vulnerability from eligible allies; mod gives only temporary self-defense strength. |
| CHARM PERSON | grants CHARMED | [This Unit] gains the [Charm Person (Spell)] status for [2] turn(s) <for all movement> | EMM resists and applies Charm to enemies in radius 1; mod substitutes a nearby combat debuff. |
| COURAGE | grants COURAGE | [This Unit] gains the [Courage (Spell)] status for [2] turn(s) <for all movement> | Correct +10 healing area direction, but adjacent instead of same-tile recipients; missing fear immunity, exploration bonus and random expiry. |
| DANCE OF BLADES | grants DANCE OF BLADES | [This Unit] gains the [Dance of Blades (Spell)] status for [2] turn(s) <for all movement> | EMM grants one first strike to allies; mod substitutes +15% attacking Strength to caster. |
| DESTROY UNDEAD | EMM Python action/condition | [This Unit] gains the [Destroy Undead (Spell)] status for [2] turn(s) <for all movement> | Now distinguishes Undead from other Magic units; still a +50% combat bonus, not immediate radial anti-undead spell damage. |
| DISPEL MAGIC | EMM Python action/condition | Remove [All] improvements from this tile <for all movement> <in [Raw Mana] tiles> <in [your] tiles> | Source dispels unit buffs/improvements in radius 2; mod removes only a node improvement on caster tile. |
| DOMINATION | EMM Python action/condition | [This Unit] gains the [Domination (Spell)] status for [2] turn(s) <for all movement> | Source can take control of living hostile units after resistance roll; mod is a local combat debuff, no capture. |
| ENCHANT SPELLSTAFF | grants SPELLSTAFF | [This Unit] gains [1] movement <for [0] movement> <once> | Replaced movement-speed buff with a one-time no-cost movement refresh to approximate another spell cast; no separate stored staff/consume step. |
| ENCHANTED BLADE | grants ENCHANTED BLADE | [This Unit] gains the [Enchanted Blade Aura] status for [2] turn(s) <for all movement> ; [This Unit] gains the [Repair (Spell)] status for [2] turn(s) <for all movement> <for units with [Dwarf]> | Source permanently enchants eligible melee allies and removes Rust; mod gives brief caster-centered Sword Strength aura. |
| ESCAPE | EMM Python action/condition | [This Unit] gains the [Escape (Spell)] status for [2] turn(s) <for all movement> | EMM teleports caster to capital; mod offers only movement/terrain-cost effects. |
| FAIR WINDS | grants FAIR WINDS | [This Unit] gains the [Fair Winds (Spell)] status for [2] turn(s) <for all movement> | Source buff to naval allies gives +1 movement and +25% withdrawal; mod instead grants caster +1 movement, including on land. |
| FERTILITY | EMM Python action/condition | Add [Sheep] to this tile <for all movement> <in [Cattle] tiles> <in [your] tiles> | EMM resource-type cycling (several crops/animals); mod provides only owned Cattle → Sheep, dependent on resource replacement behavior. |
| FIREBALL | summons FIREBALL | Free [Fireball (Summoned)] appears <for all movement> | Mod creates ranged sacrificial projectile, but combat math, ranged execution and turn-duration differ from EMM missile. |
| FLAMING ARROWS | grants FLAMING ARROWS | [This Unit] gains the [Flaming Arrows (Spell)] status for [2] turn(s) <for all movement> | EMM individually enchants ranged allies with Fire damage, lasting beyond caster; mod gives two-turn Archery Strength aura. |
| FLOATING EYE | summons EYE | Free [Floating Eye (Summoned)] appears <for all movement> | Source flying scouting eye has 0 combat, true scouting and limited duration; mod has strength 1, 3 movement, sight, no attack, manual dismissal. |
| GRAFT FLESH | summons FLESH GOLEM | Free [Flesh Golem (Summoned)] appears <for all movement> | Mod spawns permanent Flesh Golem, but cannot combine/graft constituent units as in EMM. |
| GROWTH | city spell GROWTH | Gain a free [Growth (Spell)] [in this city] <for all movement> <in [City center] tiles> | EMM +2 Food, +1 Culture, 10% food retention and +1 Health; mod now reproduces +2 Food, +1 Culture and retention, but lacks Health and caster-dependent removal. |
| HASTE | grants HASTED | [This Unit] gains the [Hasted] status for [2] turn(s) <for all movement> | Correct +1 Movement, but only to caster, fixed 2 turns, with no same-tile allies or Slow removal. |
| HOPE | city spell HOPE | Gain a free [Hope (Spell)] [in this city] <for all movement> <in [City center] tiles> | Source caster-maintained city +1 Happiness and +4 Culture; mod now matches those yields, but lacks revolution-index change, promotion granted on movement and caster-dependent removal. |
| INSPIRATION | city spell INSPIRATION | [This Unit] gains the [Inspiration (Spell)] status for [2] turn(s) <for all movement> <in [City center] tiles> | Source creates caster-dependent +2 Science and +1 Sage GP/turn building; mod +2 Science/turn temporary self status in city. |
| ILLUMINATION | city spell ILLUMINATION | Gain a free [Illumination (Spell)] [in this city] <for all movement> <in [City center] tiles> ; Gain [5] [Culture] <for all movement> | Source +50% Great Person rate plus EMM Power and caster-maintained building; mod reproduces GP rate but loses Power/lifetime. |
| LABYRINTH | special native/source action | Can instantly construct a [Labyrinth (Spell)] improvement <for all movement> | Source creates special labyrinth map feature; mod builds a permanent +Gold improvement lacking terrain and movement/portal properties. |
| LICHDOM | grants UNDEAD; EMM Python action/condition | Free [Wraith (Summoned)] appears <for all movement> ; Can transform to [Lich] <for all movement> <after discovering [Divine Essence]> | Source converts caster into Lich retaining unit state with Undead and special limits; mod transforms but resets type attributes and inheritance may differ. |
| LOYALTY | grants LOYALTY | [This Unit] gains the [Loyalty (Spell)] status for [2] turn(s) <for all movement> | Source buffs allied units with immunity to capture and removes Burning Blood; mod boosts Sword combat strength near caster. |
| MAELSTROM | 15 damage / range 2 | [This Unit] gains the [Maelstrom (Spell)] status for [2] turn(s) <for all movement> | EMM lightning AoE damage 15 (cap 30) in radius 2; mod only applies two-turn adjacent combat debuff. |
| MAGIC MISSILE | summons MAGIC MISSILE | Free [Magic Missile (Summoned)] appears <for all movement> | Native expendable ranged projectile approximates summon; range, battle mechanics, duration and AI differ. |
| MUTATION | grants MUTATED | [This Unit] gains the [Mutation (Spell)] status for [2] turn(s) <for all movement> | EMM randomly mutates eligible living units; mod deterministic +20% attack/-20% defense on caster. |
| POISONED BLADE | grants POISONED BLADE | [This Unit] gains the [Poisoned Blade (Spell)] status for [2] turn(s) <for all movement> | EMM grants poisoned weapons to target units; mod proximity Sword Strength bonus without poison or lasting enchant. |
| REGENERATION | grants REGENERATION | [This Unit] gains the [Regeneration (Spell)] status for [2] turn(s) <for all movement> | Restored +10 HP healing and the ability to heal even after acting, both present in EMM. Still affects only caster for two turns instead of allied targets until fully healed. |
| REPAIR | EMM Python action/condition | [This Unit] gains the [Enchanted Blade Aura] status for [2] turn(s) <for all movement> ; [This Unit] gains the [Repair (Spell)] status for [2] turn(s) <for all movement> <for units with [Dwarf]> | Source instant +20 healing to damaged constructs on caster tile by Dwarf caster; mod adjacent +20 to normal healing and not limited to constructs. |
| RESSURECTION | EMM Python action/condition | Free [Returned Soul (Summoned)] appears <for all movement> | EMM raises a specific dead heroic unit after timed casting; mod spawns generic Returned Soul and does not restore history. |
| RESSURECTION GRAVEYARD | EMM Python action/condition | Free [Returned Soul (Summoned)] appears <for all movement> | EMM graveyard-only Resurrection variant; mod has no separate graveyard-conditional casting action. |
| RIFT CREATE | EMM Python action/condition | Can instantly construct a [Rift (Spell)] improvement <for all movement> | EMM spawns temporary dimensional Rift unit tied to caster; mod leaves permanent Rift improvement. |
| RIFT OPEN | EMM Python action/condition | Can instantly construct a [Rift (Spell)] improvement <for all movement> | EMM Rift unit opens link/transport to caster; mod has no separate functioning Rift Open action. |
| RUST | grants RUSTED | [This Unit] gains the [Rusted (Spell)] status for [2] turn(s) <for all movement> | EMM destroys Bronze/Iron/Mithril weapon promotions on nearby hostile units; mod only briefly weakens enemy Sword Strength. |
| SANCTIFY | EMM Python action/condition | Remove [Smoke] improvements from this tile <for all movement> <in [your] tiles> <in [Smoke] tiles> | EMM cleanses ruins, graveyards, hell terrain and Armageddon counter; mod removes only friendly Smoke. |
| SCORCH | EMM Python action/condition | Turn this tile into a [Desert] tile <for all movement> <in [Plains] tiles> <in [your] tiles> <in [unimproved] tiles> ; Turn this tile into a [Tundra] tile <for all movement> <in [Snow] tiles> <in [your] tiles> <in [unimp | EMM transforms multiple terrain classes and can initiate war on foreign owned land; mod transforms three common types only on owned unimproved land, no war trigger. |
| SHADOWWALK | grants SHADOWWALK | [This Unit] gains the [Shadowwalk (Spell)] status for [2] turn(s) <for all movement> | Source ignores city defensive building bonus and defensive strikes; mod applies only +20% city attack, not precision bypass. |
| SLOW | grants SLOW | [This Unit] gains the [Chilling Presence (Spell)] status for [2] turn(s) <for all movement> | EMM removes Haste and reduces enemy movement in area after resist; mod adjacent enemy combat penalty via Ice I aura. |
| SNOWFALL | 40 damage / range 1; EMM Python action/condition | [This Unit] gains the [Snowfall (Spell)] status for [2] turn(s) <for all movement> | EMM cold damage 40 capped 70 in radius 1; mod enemy adjacent combat debuff without direct damage. |
| SPRING | EMM Python action/condition | Turn this tile into a [Plains] tile <for all movement> <in [Desert] tiles> <in [your] tiles> <in [unimproved] tiles> <in tiles without [Flood plains]> ; Remove [Smoke] improvements from this tile <for all movement> <in [ | EMM extinguishes fires and converts scorched/desert land according to Python; mod owned unimproved Desert → Plains and Smoke removal only. |
| STONESKIN | grants STONESKIN | [This Unit] gains the [Stoneskin (Spell)] status for [2] turn(s) <for all movement> | Corrected to +2 flat defending Strength, but missing three first strikes and 50% resistance. |
| SUMMON AIR ELEMENTAL | summons AIR ELEMENTAL | Free [Air Elemental (Summoned)] appears <for all movement> | Strength 5, movement 2 match source nominal stats; EMM summon duration and special elemental effects missing; mod manual-dismiss capped unit. |
| SUMMON AUREALIS | summons AUREALIS | Free [Aurealis (Summoned)] appears <for all movement> | Strength 6 and movement 1 match source nominal stats; automatic summon expiry and special effects absent. |
| SUMMON DJINN | summons DJINN | Free [Djinn (Summoned)] appears <for all movement> | Strength 5 and movement 2 nominal; source summon lifetime, elemental affinity and abilities missing. |
| SUMMON EARTH ELEMENTAL | summons EARTH ELEMENTAL | Free [Earth Elemental (Summoned)] appears <for all movement> | Strength 11 and movement 1 nominal; source elemental effects and expiry missing. |
| SUMMON EINHERJAR | summons EINHERJAR | Free [Einherjar (Summoned)] appears <for all movement> | Strength 3 and movement 1 nominal; source summon effects and expiry missing. |
| SUMMON FIRE ELEMENTAL | summons FIRE ELEMENTAL | Free [Fire Elemental (Summoned)] appears <for all movement> | Strength 6 and movement 2 nominal; source Fire affinity and summon expiry missing. |
| SUMMON ICE ELEMENTAL | summons ICE ELEMENTAL | Free [Ice Elemental (Summoned)] appears <for all movement> | Strength 2 and movement 1 nominal; source cold immunity/affinity and expiry missing. |
| SUMMON MISTFORM | summons MISTFORM | Free [Mistform (Summoned)] appears <for all movement> | Strength 6 and movement 2 nominal; EMM invisible/temporary mist form differs in target/visibility/duration. |
| SUMMON PIT BEAST | summons PIT BEAST | Free [Pit Beast (Summoned)] appears <for all movement> | Strength 4 and movement 1 nominal; source temporary summoned creature effects/expiry missing. |
| SUMMON RUNEWYN | summons RUNEWYN | Free [Runewyn (Summoned)] appears <for all movement> | Strength 6 and movement 1 nominal; source special abilities and expiry missing. |
| SUMMON SPECTRE | summons SPECTRE | Free [Spectre (Summoned)] appears <for all movement> | Strength 3, movement 2 nominal; invisible/Undead tagging added, but source summon lifetime and precise targeting absent. |
| SUMMON WATER ELEMENTAL | summons WATER ELEMENTAL | Free [Water Elemental (Summoned)] appears <for all movement> | Strength 8 and movement 1 nominal; water-specific source promotions and expiry absent. |
| SUMMON WRAITH | summons WRAITH | Free [Wraith (Summoned)] appears <for all movement> ; Can transform to [Lich] <for all movement> <after discovering [Divine Essence]> | Strength 6 and movement 2 nominal; Undead/visibility tagged, but source duration/special attacks differ. |
| TEMPERANCE | grants TEMPERANCE | [This Unit] gains the [Temperance (Spell)] status for [2] turn(s) <for all movement> | EMM grants resistance to Fire/Cold and other magical elements; mod caster defense Strength instead. |
| TREETOP TACTICS | grants TREETOP TACTICS | [This Unit] gains the [Treetop Tactics] status for [2] turn(s) <for all movement> <in [Forest] tiles> | EMM grants friendly units forest attack/withdrawal bonuses; mod caster-only +10% Forest Strength for two turns. |
| TRUST | EMM Python action/condition | Gain a free [Illumination (Spell)] [in this city] <for all movement> <in [City center] tiles> ; Gain [5] [Culture] <for all movement> | EMM has a permanent diplomatic feat affecting AI; mod grants one-off 5 Culture, no diplomatic behavior. |
| VALOR | grants VALOR | [This Unit] gains the [Valor (Spell)] status for [2] turn(s) <for all movement> | Corrected combat XP from invented +50% to EMM flat +1 XP; missing resistance, exploration and ally targeting. |
| WALL OF STONE | city spell WALL OF STONE | Gain a free [Wall of Stone (Spell)] [in this city] <for all movement> <in [City center] tiles> | EMM grants 25% city defense/bombard defense while caster is present; mod gives permanent +8 city Strength, not bombard defense. |
| WITHER | grants WITHERED; 10 damage / range 1 | [This Unit] gains the [Wither (Spell)] status for [2] turn(s) <for all movement> | EMM direct damage and persistent healing/XP suppression on enemy targets; mod temporary adjacent enemy Strength penalty. |
| WONDER | EMM Python action/condition | Gain [1]-[12] [Gold] <for all movement> | EMM casts 3–5 random spells from 72 outcomes; mod grants random Gold, not random spellcasting. |
| ARENA BATTLE | EMM Python action/condition | Existing or new unit/civilization specific action; see source differences and Android QA | Existing Balseraph Arena proxy uses Arena Battle/Victory statuses; EMM performs source-specific slave fight/upgrade/XP logic that differs. |
| PIRATE COVE | EMM Python action/condition | Existing or new unit/civilization specific action; see source differences and Android QA | Lanun cove creation/port mechanics implemented and gameplay verified within native limitations; full cove improvement upgrades and source build rules differ. |
| BURNING BLOOD | grants BURNING BLOOD | Existing or new unit/civilization specific action; see source differences and Android QA | Moroi +20% Strength and +1 move reproduced, but missing Blitz, fear protection, betrayal chance, automatic expiry and Loyalty removal. |
| SPRINT | grants HASTED; EMM Python action/condition | Existing or new unit/civilization specific action; see source differences and Android QA | Centaurs gain +1 move and -10% Strength; EMM grants Hasted and Fatigued as separate effects with independent expiration. |
| WHITEOUT | grants HIDDEN; EMM Python action/condition | Existing or new unit/civilization specific action; see source differences and Android QA | Illians Assassin on Snow gains actual invisibility, but EMM ends Hidden on casting/combat rather than fixed two turns. |
| SPORES | special native/source action | Existing or new unit/civilization specific action; see source differences and Android QA | EMM immobilizes hostile living units for 3 turns with resistance checks; mod only reduces enemy Strength. |
| SUMMON SAND LION | summons SAND LION; EMM Python action/condition | Existing or new unit/civilization specific action; see source differences and Android QA | Source nominal Strength 5, movement 3 and Desert/Malakim gate reproduced; temporary summoned creature remains until manually dismissed. |
| UPGRADE DOVIELLO AXEMAN LUCIAN | EMM Python action/condition | Existing or new unit/civilization specific action; see source differences and Android QA | Lucian gets +1 Strength for 80 Gold without transforming his source unit class into Sons of Asena and preserving all source promotions. |
| SEVER | EMM Python action/condition | Existing or new unit/civilization specific action; see source differences and Android QA | Sidar recon units spawn Strength 1, Move 2 invisible soul; EMM soul lasts 3 turns, copies promotions and is summoner-linked, not permanent/once-only. |
| HIDE | grants HIDDEN; EMM Python action/condition | Existing or new unit/civilization specific action; see source differences and Android QA | Stealth grants Hidden invisibility, but source ends on attack/cast; Unciv uses two turns and cannot enforce source state resets. |

## Source-corrected work completed in this audit

1. **Life II Destroy Undead:** applied Undead tags to Skeleton, Spectre, Wraith, Pyre Zombie and Lich, rather than counting all Magic units as undead; source direct AoE remains unimplemented.
2. **Law III Valor:** replaced incorrect +50% XP/+10% attack with native +1 XP per combat; source resistance and buff targeting remain unavailable.
3. **Body II Regeneration:** restored the original `bAlwaysHeal=1` so the unit heals even when it acts, together with +10 HP when healing; source applies to allied living units until fully healed.
4. **Earth II Stoneskin:** replaced +40% defending Strength with +2 flat defending Strength; EMM three first strikes and 50% resistances still missing.
5. **Shadow II Shadowwalk:** removed unintended terrain-cost ignoring; retains a city-combat proxy for bypassing building defenses.
6. **Enchantment III Spellstaff:** replaced temporary +1 maximum movement with one-time +1 movement restoration at zero movement cost, attempting an extra cast. **Android validation is essential** to check execution order and zero-movement availability.
7. **All summoned proxies:** one-at-a-time empire-wide cap for temporary creatures, maximum 3 Skeletons, maximum 2 Flesh Golems; manual dismiss remains, source caster-linked lifetime does not.
8. **Growth city building:** restored EMM's +2 Food and +1 Culture city yields (alongside 10% food retained on growth); +1 Health and caster-linked building removal still missing.
9. **Source-specific state:** existing higher-fidelity changes preserved, including Scorch three terrain conversions, Vitalize five terrain conversions, Full Hidden invisibility for Sidar/Whiteout and reduced Sprint recast exploits.

## Testing priority

**Critical:** Spellstaff's movement restoration; Resurrection and Rift Open lack a distinct faithful cast; creation/replacement of Cattle→Sheep resource; Source-accurate targeting of Undead vs other Magic units; summoned unit caps versus unlimited casting; Lich transformation and inherited XP/promotions; and reliable cast button availability with zero movement.

**Next:** Every buff's duration, combat preview and save/reload; controlled/uncontrolled tiles, owned/foreign city effects, spellcaster death, ally vs enemy target filters; mana loss after learning; all Doviello transform Gold deductions and XP retention.

**Release gate:** Official Unciv `mod-ci` green, all local check scripts green, Unciv **Locate mod errors**, Android test cases checked, no broken actions. Do not merge into `main` until approved.
