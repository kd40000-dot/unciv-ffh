# Amurites Simple — optional Unciv unit set

This new selectable unit set is separate from the existing high-detail AbsoluteUnits artwork. The original images and 21 original atlas registrations are unchanged.

Select **Options → Display → Unitset → AmuritesSimple** to view the simple art; choose **AbsoluteUnits** for the high-detail set. No `unitset` is forced in ModOptions.json.

## Approved sprites — first ten

- Adept-Amurites
- Archer-Amurites
- Archmage-Amurites
- Beastmaster-Amurites
- Champion-Amurites
- Chanter
- Chariot-Amurites
- Crossbowman-Amurites
- Firebow
- Govannon

The first eight are extracted from the corrected user-approved artwork sheet with no clipping of the Chariot or bleed into Crossbowman; Chanter (red hood with metal claws) and Govannon (green clothes and green flame) are independently approved. Each is converted proportionally onto a transparent 95×81 sprite canvas with bold, minimal-color shading. A 5×2 atlas image page and `amurites-simple.atlas` register the ten sprite keys.

## Work in progress

- Horse Archer-Amurites
- Horseman-Amurites
- Hunter-Amurites
- Immortal-Amurites
- Marksman-Amurites
- Phalanx-Amurites
- Ranger-Amurites
- Scout-Amurites
- Swordsman
- Warrior-Amurites
- Wizard
- Goblin
- Warrior-Clan of Embers

These 13 entries still use the existing AbsoluteUnits artwork via cross-referenced atlas page paths while the rest of the simple roster is developed; they include the other 11 Amurite designs and Goblin/Clan Warrior. Other units may display built-in fallback markers until dedicated art exists. No gameplay units, promotions, or stats are added by this asset-only change; Govannon still requires a gameplay unit definition.

Static checks verified the atlas region keys and dimensions; live Unciv rendering still needs to be tested.

## Compatibility fix (October 22, 2026)

The first `AmuritesSimpleAtlas.png` was exported as an indexed-color PNG (color type 3), unlike the working high-detail Amurites PNGs. It has now been losslessly converted to a standard full-color RGBA PNG (color type 6), retaining every pixel, the 475×162 atlas layout, 95×81 subregions, alpha transparency, atlas keys, and nearest filtering. This is to address reports that the AmuritesSimple selection was present but the new sprite art did not appear. Verify in-game after updating; no gameplay or user unit-set preference was changed.
