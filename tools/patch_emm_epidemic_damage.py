#!/usr/bin/env python3
"""Postprocess a generated Unciv checkout to enable EMM epidemic unit damage.

Run after tools/patch_unciv_health.py, before Kotlin compilation.
Source: pinned EMM CvRandomEventInterface.py (60b0ec374...).
Living status follows pinned EMM bMechanized and bNotAlive promotion counters;\nEpidemic damage uses source-derived typed resistance and two-roll damage;\nexact strength, experience-level and city-defense parity is still under review.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-unciv")
path = root / "core/src/com/unciv/logic/city/EmmArmageddonEvents.kt"
code = path.read_text()
if "private fun damageLivingUnits(game: GameInfo)" in code:
    print("EMM epidemic unit damage already present")
    sys.exit(0)
blight = """            city.cityStats.update()
        }
    }

    fun firePestilence(game: GameInfo) {"""
patched = """            city.cityStats.update()
        }
        damageLivingUnits(game)
    }

    // Pinned EMM CvUnit::isAlive: m_iAlive == 0.
    // CvUnit::init adds +1 for bMechanized; setHasPromotion changes it
    // by +/-1 for every promotion whose bNotAlive is set.
    // Derived on demand so adding/removing a racial promotion immediately
    // changes epidemic eligibility, including multiple stacked sources.
    private val emmNotAlivePromotions = setOf(
        "Angel", "Avatar", "Demon", "Elemental", "Golem",
        "Illusion", "Puppet", "Rift", "Undead"
    )
    // CIV4UnitInfos.xml bMechanized=1, excluding equipment records.
    private val emmMechanizedUnits = setOf(
        "Arcane Barge", "Battering Ram", "Black Wind", "Cannon",
        "Dwarven Cannon", "Caravel", "Catapult", "Trebuchet", "Frigate",
        "Galleon", "Galley", "Man O War", "Pirate", "Privateer",
        "Airship", "Queen Of The Line", "Sailors Dirge", "Trireme",
        "War Machine", "Workboat"
    )
    private fun isEmmLiving(unit: com.unciv.logic.map.mapunit.MapUnit): Boolean {
        val counter = (if (unit.baseUnit.name in emmMechanizedUnits) 1 else 0) +
            unit.promotions.promotions.count { it in emmNotAlivePromotions }
        return counter == 0
    }
    // Source callbacks specify 25 DAMAGE_DEATH, damage cap 100.
    // Typed Death resistance is still outstanding.
    private fun damageLivingUnits(game: GameInfo) {
        for (civ in game.civilizations)
            for (unit in civ.units.getCivUnits().toList()) {
                if (!isEmmLiving(unit)) continue
                com.unciv.logic.map.mapunit.EmmTypedDamage.applyToUnit(
                    unit = unit,
                    type = "DAMAGE_DEATH",
                    initialDamage = 25,
                    damageLimit = 100,
                    random = civ.state.stateBasedRandom("EMM.Epidemic.Death." + game.turns + "." + unit.id)
                )
            }
    }

    fun firePestilence(game: GameInfo) {"""
assert code.count(blight) == 1, "blight anchor mismatch"
code = code.replace(blight, patched)
pestilence = """            EmmCityEpidemics.pestilence(city, random, goodBuildingHealth)
            city.cityStats.update()
        }
    }
}"""
revised = """            EmmCityEpidemics.pestilence(city, random, goodBuildingHealth)
            city.cityStats.update()
        }
        damageLivingUnits(game)
    }
}"""
assert code.count(pestilence) == 1, "pestilence anchor mismatch"
code = code.replace(pestilence, revised)
path.write_text(code)
assert code.count("damageLivingUnits(game)") == 2
print("Patched both epidemic callbacks with shared unit damage")
