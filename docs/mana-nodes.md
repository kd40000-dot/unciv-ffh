# Mana nodes — first playable magic foundation

**Implementation date:** October 23, 2026. **Status:** Mod definitions committed, independent 21-sphere source verification passed and official Unciv `mod-ci` validation passed on October 23, 2026; user gameplay-verified for Fire Node construction and +1 Fire Mana on October 23, 2026; other 20 spheres and edge cases still unverified.

**Pinned EMM Continued source:** [commit `60b0ec3740083162aaab7bf8491761a54a65a610`](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610). `XML/Terrain/CIV4BonusInfos.xml` contains the Raw Mana and 21 sphere Mana bonus IDs; `XML/Terrain/CIV4ImprovementInfos.xml` contains 21 sphere improvements; `XML/Units/CIV4BuildInfos.xml` contains their tech gates and iTime=1200 build cost. [Machine-readable fidelity ledger](data/emm-mana-nodes.json).

## Playable Unciv conversion

- **Raw Mana** is a map-generated Bonus resource, visible from the start, that marks a convertible arcane source. It is intended to occur sparsely on land, and is not itself a source of Sphere Mana or an executable spell.
- **21 sphere Mana resources** (Air, Body, Chaos, Creation, Death, Dimensional, Earth, Enchantment, Entropy, Fire, Force, Ice, Law, Life, Metamagic, Mind, Nature, Spirit, Water, Shadow, Sun) are defined as Strategic resources. They never generate directly on the map.
- **21 sphere Mana Node improvements** exist. Their only valid locations are **owned Raw Mana tiles**. Each improvement provides **one unit of its own strategic Sphere Mana** to the empire with native `Provides [1] [Sphere Mana]` and `CityResources.getResourceFromUniqueImprovedTiles` mechanics. Unlike city-generated resources, the node does not need its tile to be worked to supply Mana.
- **Adepts** may construct all 21 nodes as normal tile improvements, using standard Unciv build actions and the appropriate technology. Each node takes **17 base turns**, scaled approximately from EMM's 1200 improvement construction points versus EMM's 500 for a Farm (currently Farm = 7 Unciv turns). These are *not* instant actions and do not consume the Adept.
- **One sphere per tile:** A tile has only one improvement at a time. Adepts may **retune** an existing node by building another sphere's node directly over it. The change takes the destination node's full 17-turn construction time and technology requirement. The old mana supply is replaced rather than duplicated; players do not need a remove-improvement action.

## Sphere-to-technology prerequisites

| School | Sphere Node choices |
| --- | --- |
| Elementalism | Air, Earth, Fire, Ice, Water |
| Alteration | Body, Enchantment, Force, Life, Nature |
| Necromancy | Chaos, Death, Dimensional, Entropy, Shadow |
| Divination | Creation, Law, Mind, Spirit, Sun |
| Sorcery | Metamagic |

These are EMM-sourced prerequisites, not arbitrary tiers.

## How to test on Android

1. Update the mod and **begin a new game**. Locate a **Raw Mana** resource on land (preferably on a Hill). Raw Mana is a new resource, so an older generated map may not have any.
2. Take ownership of the tile and research **Knowledge of the Ether**, then produce an **Adept**.
3. Research **Elementalism** and bring the Adept to an **Raw Mana tile**. It should offer **Fire Node**, **Water Node**, **Air Node**, **Earth Node**, or **Ice Node** as build actions.
4. Choose **Fire Node**; finish the build (17 base turns). Check the tile improvement changes to Fire Node and the empire now has **1 Fire Mana**. The mana is supplied even when the tile isn't worked, but pillaging the node should remove its contribution.
5. Check that the other four Elementalism spheres remain unbuilt, that Fire Node can't be placed on an ordinary tile, and that a **different** node can be constructed over the Fire Node after the required technology is researched, and the original Fire Mana disappears after replacement.
6. Research **Alteration, Necromancy, Divination, Sorcery** in turn. Confirm the other 16 node types unlock only after their respective prerequisites and have the same Raw Mana placement rules.
7. Build another node on a *different* Raw Mana tile and verify that both resource amounts are counted independently. Save/load and check persistence.

## Deliberate limitations

**Do not confuse the new resource layer with a complete magic system.** Sphere Mana resources do **not yet** unlock promotions, spells, summoning, or Amurite-specific magical effects. Next steps are to map EMM's sphere promotion requirements and implement a few real spell actions using Unciv's supported unit-action uniques.

EMM sometimes pre-places typed sphere mana directly through civilization-specific buildings/nodes and has additional Dispel Magic / node transformation rules. Those mechanics are **not implemented** here. Mana from the existing palaces remains incomplete. Raw Mana generation frequency/terrain distribution is an approximation, since Unciv map generation differs from EMM. The current pipeline also does not yet include custom Mana Node art; Unciv will use its fallback improvement visuals. Do not claim this milestone is fully working until an Adept creates a node and the strategic resource count changes in game.

## Body I → Haste prototype (October 23, 2026)

- Added **Body I**: Magic-unit promotion requiring Channeling I and an available **Body Mana** resource, using Unciv's native promotion availability condition.
- **Haste** action: `[This Unit] gains the [Hasted] status for [2] turn(s) <for all movement> <with [Body Mana]>`. The status temporarily grants `[+1] Movement`; casting costs all caster movement. Recasting refreshes the timer instead of stacking multiple extra movement bonuses.
- This is a **self-cast-only** conversion. EMM's Haste applies to friendly living units on the caster's tile and removes Slow. Neither group targeting nor Slow removal is implemented. Unciv's temporary status lasts two turns under its own turn-counting semantics, and does not require custom engine changes.
- Gameplay unverified: Build a **Body Node** after **Alteration**, ensure **Body Mana** count is 1, grant an Adept enough XP to choose **Body I**, cast the Hasted status action, verify the caster survives, movement is consumed and the temporary +1 Movement disappears after the effect expires. Test lost mana and repeated casts.

See `tools/verify_body_i.py` for source/resource/promotion static assertions.

## Retuning an existing mana node (October 23, 2026)

After user gameplay testing confirmed Fire Node and Body I Haste work, a missing conversion path was reported: there was no way to remove one's own existing Mana Node. We removed the `[unimproved]` tile restriction **only from the 21 sphere Mana Nodes**, preserving their owned Raw Mana tile constraint and technology gates. Move an Adept onto the old node and select a *different* node improvement, such as Body Node over Fire Node. Finish the standard 17-turn construction. Unciv replaces the old improvement with the new one and automatically recalculates its resource supply (Fire Mana −1, Body Mana +1). This avoids a separate demolition action and is not a free/instant conversion.

**Gameplay QA pending:** update the mod, visit your existing Fire Node with an Adept, research Alteration, construct Body Node on the same tile, and check that Fire Mana disappears and Body Mana appears. Verify the old node remains active during construction, that requirements still block locked spheres, and that no resource is duplicated. This changes no unrelated improvements or workers.
