# Magic milestone 0.3b — typed mana groundwork

## Implemented
- Defined 21 separate strategic resources: Air, Body, Chaos, Creation, Death, Dimensional, Earth, Enchantment, Entropy, Fire, Force, Ice, Law, Life, Metamagic, Mind, Nature, Shadow, Spirit, Sun, and Water Mana.
- All 21 can be improved with the existing **Node of Mana** improvement.
- Kept the existing generic **Mana** resource and its map-generation rule so existing games and the Arcane Circle prototype retain their behavior.
- No additional natural spawning was assigned to typed mana yet; the resources are defined but do not automatically appear on random maps.

## Not yet implemented
- Conversion of generic mana nodes to a selected sphere, including dispelling/reconversion.
- Palace-granted mana for each civilization.
- Ownership/availability gating for sphere promotions and spells.
- Genuine targeted casting, one spell per turn, summoned-unit durations, spell resistance, and FFH2 Python spell effects.
- Tier II and III spell effects. Existing promotion bonuses remain **prototypes**, not faithful FFH2 spells.

## Testing
- Update the mod and verify it loads without ruleset errors.
- Check the Civilopedia resource entries for the 21 named mana types.
- On a fresh random map, the original generic Mana should still spawn; typed mana will not spawn until a node conversion or explicit placement mechanism is implemented.

## Next milestone
Implement a real node-conversion interaction and civilization palace mana; then connect sphere promotion prerequisites to typed resource availability. Avoid replacing FFH2 spells with passive combat buffs as a permanent solution.
