# EMM Continued selected leader traits and civilization palaces

Pinned source: [ExtraModMod Continued 60b0ec3740083162aaab7bf8491761a54a65a610](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610). Original `XML/Civilizations/CIV4TraitInfos.xml` and `XML/Buildings/CIV4BuildingInfos.xml` were used; numeric source values and resolved selected leaders are stored in [the machine-readable source ledger](data/emm-leader-palace-fidelity.json).

## Trait conversion (selected leader only)

| Trait | EMM source | Unciv implementation | Fidelity limit |
| --- | --- | --- | --- |
| Financial | +25% Gold commerce | +25% Gold in all cities | Lacks Civ IV commerce slider |
| Creative | +2 Culture and +10% Culture | Both flat and percentage Culture in all cities | Income stacking may differ |
| Ingenuity | +50 starting Gold and -50% gold cost to upgrade | Both; Gold awarded once on new-game initialization | Unciv game-speed scaling may differ |
| Aggressive | Free Combat I for Adept, Archer, Disciple, Melee, Mounted and Recon | Grants on newly trained Magic, Archery, Disciple, Sword, Mounted and Scout units | Starting units are not newly trained; combat-class correspondence is approximate |
| Arcane | Free Mobility I and Potency for Adepts | Free Mobility I for newly trained Magic units | Potency and spellcraft mechanics deferred |
| Spiritual | Free Mobility I and Favored for Disciples | Free Mobility I for newly trained Disciple units | Favored effect and religion progression deferred |
| Raiders | +100% pillage Gold, free Commando | Double normal pillage yields (currently all Gold; `100%` Unciv bonus) | Enemy-road movement and first strike not ported |
| Barbarian | -10% Research, barbarian alliance | -10% Science in all cities | Barbarian alliance and Civ IV commerce slider not ported |

Earlier traits retained as implemented: Charismatic, Industrious, Philosophical. **Organized** in EMM gives -50% *civic upkeep*, not a general Unciv unit, road, or building upkeep bonus, so it is intentionally deferred. **Expansive** grants +3 Civ IV health, which Unciv lacks. **Raiders** now doubles pillage Gold through native Unciv's `100% Yield from pillaging tiles`, but its free Commando promotion (enemy roads and first strike) remains deferred. **Barbarian** now gives its source -10% Research modifier as -10% Unciv Science, while its alliance with barbarian units remains deferred. **Adaptive**, **Insane** and **Summoner** still require specialized systems.

## Palaces: source data and approximation

Every one of the **19 normal playable civilizations** has an EMM-specific `BUILDING_PALACE_<FACTION>` which is a capital building. The pinned source inventories show identical ordinary base stats for all 19: cost **160**, +**1 Happiness**, yields **0 Food / 1 Production / 8 Commerce** and no base defense modifier.

The new buildings are named `<Faction> Palace`, have `uniqueTo`, `replaces: Palace`, `isNationalWonder: true`, and retain `Indicates the capital city`. Unciv's `capitalCityIndicator` chooses a civilization-specific building with the capital indicator unique. Existing generic Palace is preserved for fallback/non-playable contexts.

**Explicit gameplay proxy:** Civ IV's +8 Commerce can be divided between research and treasury using its commerce slider; stock Unciv has no equivalent. We currently represent **+4 Science and +4 Gold** from each faction palace, totaling 8 points of fixed income. This is **not** source-exact player-controlled commerce. The +1 Production, +1 Happiness and cost 160 remain exact from the EMM inventory. Mana resources, free spell promotions, scripted effects and special palace mechanics are not included here.

## Validation and in-game test plan

`tools/verify_leaders_palaces.py` checks all selected-leader source traits, specific trait bonuses, 19 faction palace definitions, EMM source costs/yields, and the explicit 4/4 commerce proxy. Earlier source verifiers remain enabled in CI; the official Unciv `mod-ci` is still a separate gating step.

Android playtests should confirm: (1) founding a first city gives the correct named faction palace automatically; (2) it grants +1 Production, +4 Science, +4 Gold and +1 Happiness; (3) a capital move handles the variant palace correctly; (4) each leader receives the correct added bonuses; (5) starting +50 Gold for Valledia is granted once only; and (6) newly trained Arcane/Spiritual/Aggressive eligible units receive their proper promotions.

The static source check is **not** proof of those in-game outcomes. These remain untested until a gameplay session verifies them.

## Economic and raiding update — October 21, 2026

The pinned Raider trait gives `iPillagingGold=100`, meaning **100% extra Gold** rather than a total yield of 100%. Unciv's pillage loot calculator multiplies by `1 + percent/100`, meaning `100% Yield from pillaging tiles` produces a 2× payout. A previous `200%` value would have caused 3× loot and was corrected after engine-code verification. All currently configured pillageable improvements yield Gold only, making this source-faithful for existing improvements. The multiplier affects the unit's improvement pillage loot, not barbarian camp prizes. This bonus now applies to selected Hippus and Svartalfar leaders. The source Commando promotion includes `bEnemyRoute=1` and an extra first strike; we have **not** added a misleading replacement.

Charadon's Doviello also receive the source Barbarian trait's `commerceModifiers=[0,-10,0]` as `[-10]% Science [in all cities]`, approximating the research-commerce penalty while retaining a separate ledger entry for missing barbarian alliance. Other factions receive neither effect.

The user has verified that the prior source-derived palaces and leader effects behave as expected in gameplay. The user tested these economic effects after the Raider multiplier correction and reported that both appear to work as expected (October 21, 2026). They are considered gameplay-verified for now; any subsequent issues will be reported and addressed.
