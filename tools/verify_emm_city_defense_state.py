#!/usr/bin/env python3
"""Check source-faithful storage boundaries: city combat strength != building defense."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess,sys
with TemporaryDirectory() as tmp:
    root=Path(tmp)
    city=root/"core/src/com/unciv/logic/city/City.kt"
    typed=root/"core/src/com/unciv/logic/map/mapunit/EmmTypedDamage.kt"
    city.parent.mkdir(parents=True)
    typed.parent.mkdir(parents=True)
    city.write_text("""class City {
    var health = 200
    fun clone(): City {
        val toReturn = City()
        toReturn.health = health
        return toReturn
    }
}
""")
    typed.write_text("""object EmmTypedDamage {
        fun damaged() {
            // These two runtime inputs are exact Unciv state (built defenses,
            // resistance). Civ IV culture/ranged/owner modifiers and bombardment
            // state still require their own EMM source integrations.
            buildingDefense = city.getStrength().toInt(),
            naturalDefense = 0,
            ownerDefense = 0,
            rangedDefense = 0,
            defenseDamage = 0,
            maximumCityDefenseDamage = 100,
        }
}
""")
    for i in range(2):
        subprocess.run([sys.executable,"tools/patch_emm_city_defense_state.py",tmp],check=True)
    c=city.read_text()
    t=typed.read_text()
    assert c.count("var emmBuildingDefense: Int = 0")==1
    assert "toReturn.emmDefenseDamage = emmDefenseDamage" in c
    assert "buildingDefense = city.emmBuildingDefense" in t
    assert "naturalDefense = city.emmNaturalDefense" in t
    assert "ownerDefense = city.emmOwnerDefense" in t
    assert "rangedDefense = city.emmRangedDefense" in t
    assert "defenseDamage = city.emmDefenseDamage" in t
    assert "city.getStrength()" not in t
print("PASS: defense and bombardment state persists independently of Unciv combat strength")
