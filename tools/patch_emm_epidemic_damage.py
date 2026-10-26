#!/usr/bin/env python3
"""Postprocess a generated Unciv checkout to enable EMM epidemic unit damage.

Run after tools/patch_unciv_health.py, before Kotlin compilation.
Source: pinned EMM CvRandomEventInterface.py (60b0ec374...).
This is explicitly a raw-damage compatibility adapter, not Death resistance parity.
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

    // Both EMM callbacks damage each living unit, including units owned by
    // the Infernal civilization. Exact DLL isAlive() and typed Death resistance
    // remain unsupported by this temporary adapter.
    private fun damageLivingUnits(game: GameInfo) {
        val nonliving = setOf("Undead", "Demon", "Angel", "Elemental", "Golem", "Not Alive")
        for (civ in game.civilizations)
            for (unit in civ.units.getCivUnits().toList()) {
                if (unit.promotions.promotions.any { it in nonliving }) continue
                unit.takeDamage(25)
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
