#!/usr/bin/env python3
"""Install Infernal default Demon race at new-unit creation.

Source: EMM CvUnit::init and CIV4CivilizationInfos.xml DefaultRace.
World-unit/animal identity parity still requires the full EMM roster.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
path=root/"core/src/com/unciv/logic/civilization/managers/UnitManager.kt"
s=path.read_text()
marker="        copiedFrom?.copyStatisticsTo(unit)"
block="""        copiedFrom?.copyStatisticsTo(unit)
        // EMM CIVILIZATION_INFERNAL DefaultRace: DEMON.
        // New ordinary land units lacking a race receive this as a free promotion.
        // Source exceptions for world units and animals need fuller roster metadata.
        if (civInfo.civName == "Infernal" &&
            !unit.baseUnit.isWaterUnit &&
            civInfo.gameInfo.ruleset.unitPromotions.containsKey("Demon") &&
            unit.promotions.promotions.none {
                it in setOf("Angel", "Avatar", "Demon", "Elemental", "Golem",
                    "Illusion", "Puppet", "Rift", "Undead", "Orc", "Dwarf",
                    "Elf", "Dark Elf")
            }) {
            unit.promotions.addPromotion("Demon", isFree = true)
        }"""
if "EMM CIVILIZATION_INFERNAL DefaultRace" in s:
    print("Infernal default race already installed")
    sys.exit(0)
assert s.count(marker)==1
path.write_text(s.replace(marker,block))
print("Installed Infernal new-unit Demon default-race assignment")
