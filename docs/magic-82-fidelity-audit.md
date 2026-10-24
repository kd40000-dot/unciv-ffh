# EMM spell fidelity audit — 82 current implementations

Pinned EMM source: `bewlay/extramodmod` `60b0ec3740083162aaab7bf8491761a54a65a610`. Mod branch: `feature/expanded-magic-2026-10-24`. Frozen game-test branch unchanged. This is a **source-level, ruleset-validated** audit, not an Android gameplay certification. "Perfect" requires exact mechanics, target selection, duration, cast restrictions and verified behavior. "Very close" preserves the primary gameplay result and source costs/terrain but may differ in secondary rules. "Significant" indicates a different practical gameplay result or major missing mechanic.

## Audit totals

- **Perfect representation: 0 / 82 (0.0%)**
- **Very close: 13 / 82 (15.9%)**
- **Significant differences: 69 / 82 (84.1%)**

## Perfect representation

None yet. Static CI success alone is not proof of perfect equivalence.

## Very close

| Spell | School | Fidelity audit / remaining difference |
|---|---|---|
| `FIREBALL` | Fire II | A ranged expendable projectile approximates the summoned fireball but changes spell/projectile combat rules and EMM summoning lifetime. |
| `MAGIC_MISSILE` | Force II | An expendable ranged projectile approximates the magical missile but lacks exact damage and attack resolution. |
| `RAISE_SKELETON` | Death I | Permanent Skeleton creation preserves core effect, but caster/summon limits and spellcaster Python nuances are absent. |
| `SCORCH` | Sun I | The main Plains→Desert, Snow→Tundra and Marsh→Plains steps exist; EMM also scorches other terrains and may trigger war on foreign land. |
| `SPRING` | Water I | Owned unimproved Desert→Plains plus Smoke cleanup resembles EMM terraforming, but lacks all valid tile cases and exact source extinguish behavior. |
| `VITALIZE` | Nature III | Several EMM terrain improvements are reproduced, but other terrain/feature cases and existing improvements are restricted. |
| `UPGRADE_DOVIELLO_AXEMAN` | Faction / unit / existing | Gold-gated Sons of Asena transform follows source cost and tech; unit XP/class conversion still requires gameplay check. |
| `UPGRADE_DOVIELLO_BATTLEMASTER` | Faction / unit / existing | Gold-gated Battlemaster transform follows source tech/cost; skill inheritance unverified. |
| `UPGRADE_DOVIELLO_CHAMPION` | Faction / unit / existing | Gold-gated Axeman→Battlemaster transform follows EMM tech/cost; XP inheritance unverified. |
| `UPGRADE_DOVIELLO_WARRIOR` | Faction / unit / existing | Worker→Beastman Gold-gated transformation matches main EMM result; source AI conditions unmodeled. |
| `UPGRADE_DOVIELLO_WARRIOR_SLAVE` | Faction / unit / existing | Slave→Beastman Gold-gated transformation matches source result; source AI conditions unmodeled. |
| `ARENA_BATTLE` | Faction / unit / existing | Arena combat/victorious slave conversion exists and has user-reported basic gameplay verification, but not exact EMM match for every fight/outcome. |
| `PIRATE_COVE` | Faction / unit / existing | Lanun cove mechanic has user-reported gameplay verification within Unciv limits; source upgrade/territory behavior remains approximate. |

## Significant differences

| Spell | School | Fidelity audit / remaining difference |
|---|---|---|
| `BLAZE` | Fire I | Smoke is persistent and has a fixed adjacent damage effect; EMM spreads fires, alters burning terrain and extinguishes naturally. |
| `BLESSING` | Creation III | Approximates living unit production bonus; EMM also grants specialist effects, requires caster, and excludes constructs. |
| `BLINDING_LIGHT` | Sun II | Strength suppression does not reproduce EMM disabling Blinded status and resist chance. |
| `BLUR` | Shadow I | Self-defense bonus instead of first-strike immunity granted to allied units. |
| `CHARM_PERSON` | Mind II | Debuff aura does not actually Charm target units, check resistance or disable movement. |
| `COURAGE` | Spirit I | Adjacent healing proxy lacks same-tile individual buffs, fear immunity, exploration bonus and source expiry. |
| `DANCE_OF_BLADES` | Chaos I | Temporary attacking Strength instead of an actual EMM first strike. |
| `DESTROY_UNDEAD` | Life II | Targets Undead-tagged opponents after audit instead of all Magic units, but is a combat buff, not undead-only ranged AoE damage. |
| `DISPEL_MAGIC` | Metamagic II | Raw Mana improvement removal is only a small part of EMM range-two dispel, promotion/effect stripping. |
| `DOMINATION` | Mind III | Weakness aura does not permanently capture an enemy living unit. |
| `ENCHANT_SPELLSTAFF` | Enchantment III | An extra movement action is not an additional spell cast. |
| `ENCHANTED_BLADE` | Enchantment I | Temporary aura doesn't enchant eligible melee targets permanently or remove Rust. |
| `ESCAPE` | Dimensional I | Movement buff cannot teleport caster to its capital. |
| `FAIR_WINDS` | Air I | Reworked to support naval units, but converts EMM movement/withdrawal effects into ship Strength; very different in play. |
| `FERTILITY` | Creation II | Only Cattle→Sheep conversion is available; EMM cycles many resource families and checks owned tiles. |
| `FLAMING_ARROWS` | Enchantment II | Nearby Archer Strength bonus is not persistent Fire-damage promotion. |
| `FLOATING_EYE` | Metamagic I | Summoned scout cannot expire automatically and source movement/sight behavior isn't exact. |
| `GRAFT_FLESH` | Body III | Spawns a Flesh Golem but lacks EMM's actual combination of existing living unit bodies. |
| `GROWTH` | Creation I | Food retention modeled, but +1 Health and the EMM caster-linked building lifetime are absent. |
| `HASTE` | Body I | Movement self-buff doesn't grant Haste to eligible co-located allies or remove Slow. |
| `HOPE` | Spirit II | City Happiness/Culture approximation, but source city building also affects rebellion and requires caster presence. |
| `INSPIRATION` | Mind I | A two-turn caster science status is not EMM's caster-linked city building with Great Sage points. |
| `ILLUMINATION` | Spirit III | +50% Great Person growth is reproduced but source power and caster lifetime are missing. |
| `LABYRINTH` | Dimensional II | Native proxy has substantive differences in targeting, duration, spell effects or EMM's Python logic. |
| `LICHDOM` | Death III | Transforms into a Lich, but EMM's limited Liches, undead conversion, preserved unit attributes and death rules differ. |
| `LOYALTY` | Law I | Nearby Sword Strength bonus is not capture immunity or Burning Blood removal. |
| `MAELSTROM` | Air II | Strength debuff does not inflict EMM capped lightning damage within its specified range. |
| `MUTATION` | Chaos II | Fixed attacker/defender bonuses cannot reproduce random permanent mutation outcomes. |
| `POISONED_BLADE` | Nature II | Aura strength does not grant weapon poison status to eligible allies. |
| `REGENERATION` | Body II | Reworked to heal nearby units, yet source grants promotions to living co-located units, not an aura. |
| `REPAIR` | Enchantment I | Applies a healing aura rather than healing injured constructs directly, and targets different units. |
| `RESSURECTION` | Life III | Creates a generic Returned Soul rather than resurrecting a specific dead hero. |
| `RESSURECTION_GRAVEYARD` | Life III | Graveyard-specific restoration mechanics and targeting aren't implemented; generic Life III summon is not equivalent. |
| `RIFT_CREATE` | Dimensional III | Creates a static tile improvement rather than a temporary summoned, moving Rift unit. |
| `RIFT_OPEN` | Dimensional III | A connected portal cannot be opened from the static improvement, unlike EMM. |
| `RUST` | Entropy I | Combat penalty does not strip equipped Copper, Iron or Mithril weapons. |
| `SANCTIFY` | Life I | Smoke cleanup is not hell terrain purification, Graveyard/City Ruins cleansing or Armageddon reduction. |
| `SHADOWWALK` | Shadow II | Ignoring terrain cost differs from EMM city defense bypass. |
| `SLOW` | Ice I | Adjacent combat penalty does not subtract Movement or remove Haste. |
| `SNOWFALL` | Ice III | Strength debuff does not inflict capped cold damage and its source terrain effects. |
| `STONESKIN` | Earth II | Defense bonus lacks first strikes and spell resistance. |
| `SUMMON_AIR_ELEMENTAL` | Air III | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `SUMMON_AUREALIS` | Sun III | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `SUMMON_DJINN` | Metamagic III | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `SUMMON_EARTH_ELEMENTAL` | Earth III | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `SUMMON_EINHERJAR` | Law II | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `SUMMON_FIRE_ELEMENTAL` | Fire III | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `SUMMON_ICE_ELEMENTAL` | Ice II | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `SUMMON_MISTFORM` | Shadow III | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `SUMMON_PIT_BEAST` | Entropy II | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `SUMMON_RUNEWYN` | Force III | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `SUMMON_SPECTRE` | Death II | Source creature is summoned but persists indefinitely without native turn expiration. |
| `SUMMON_WATER_ELEMENTAL` | Water III | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `SUMMON_WRAITH` | Death III | Source summon exists as a persistent unit; no automatic EMM summon duration or caster-linked limit; manual dismissal only. |
| `TEMPERANCE` | Force I | Combat defense bonus is not the original elemental/magic resistances. |
| `TREETOP_TACTICS` | Nature I | Combat bonus approximated but withdrawal bonus, same-tile ally targeting and Ancient Forest support differ. |
| `TRUST` | Spirit III | A small Culture reward cannot reproduce EMM permanent diplomatic Trust feat. |
| `VALOR` | Law III | Temporary caster XP and Strength differs from lasting Valor promotion for co-located living allies. |
| `WALL_OF_STONE` | Earth I | Adds native city defense, but differs from EMM +25% city defense and bombard defense, with caster-dependent expiry. |
| `WITHER` | Entropy III | Debuff aura lacks instant Death damage, resistance and target's lasting Withered promotion. |
| `WONDER` | Chaos III | A random Gold payout does not execute EMM's 3–5 randomly selected spells. |
| `BURNING_BLOOD` | Faction / unit / existing | Temporary +20% combat/+1 movement, but missing Blitz, fear immunity, betrayal and source random expiry. |
| `SPRINT` | Faction / unit / existing | Movement/fatigue modeled but combined status has different expiry and action timing. |
| `WHITEOUT` | Faction / unit / existing | Snow-restricted partial invisibility differs from true Hidden removed on combat/cast. |
| `SPORES` | Faction / unit / existing | Combat Strength aura rather than targeted 3-turn immobility with resistance. |
| `SUMMON_SAND_LION` | Faction / unit / existing | Desert-only Malakim summon approximated; lacks automatic EMM lifetime and Burning Sands case. |
| `UPGRADE_DOVIELLO_AXEMAN_LUCIAN` | Faction / unit / existing | Keeps Lucian and adds +1 Strength for Gold instead of actual EMM conversion/renaming mechanics. |
| `SEVER` | Faction / unit / existing | Sidar Severed Soul's mobility/invisibility approximated; no true invisibility, 3-turn expiry or summoned-unit promotions. |
| `HIDE` | Faction / unit / existing | Temporary nonadjacent invisibility cannot replicate full EMM Hidden or its combat/casting removal. |

## Validation and priority fixes

1. Restore EMM target unit selection and individually applied promotions where Unciv supports it. Current temporary caster auras are only substitutes for same-tile friend buffs.
2. Reproduce automatic summon expiration and caster-linked limitations. This likely requires engine support, currently outside the no-engine-edit constraint.
3. Replace enemy weakness auras with original AoE damage, unit conversion, magic resistance and status effects where native rules permit; do not target all Magic units as "undead".
4. Add proper religion/faction/world/equipment infrastructure separately; these 82 are not the complete 355 spell catalog.
5. Verify every action on Android with the parallel per-spell checkbox ledger before promoting it to "Perfect".
