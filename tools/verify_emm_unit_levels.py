#!/usr/bin/env python3
"""Regression checks for EMM level serialization, free promotions, and damage call site."""
from pathlib import Path
import tempfile,subprocess,sys
with tempfile.TemporaryDirectory() as d:
    root=Path(d)
    mp=root/"core/src/com/unciv/logic/map/mapunit"
    mp.mkdir(parents=True)
    (mp/"MapUnit.kt").write_text('''class MapUnit {
    var health: Int = 100
    fun copyStatisticsTo(newUnit: MapUnit) {
        newUnit.health = health
    }
}
''')
    (mp/"UnitPromotions.kt").write_text('''class UnitPromotions {
    fun promotion() {
                XP -= xpForNextPromotion()
                numberOfPromotions++
    }
}
''')
    (mp/"EmmTypedDamage.kt").write_text('''object EmmTypedDamage {
    fun apply() {
            level = unit.promotions.numberOfPromotions + 1,
    }
}
''')
    for _ in range(2):
        subprocess.run([sys.executable,"tools/patch_emm_unit_levels.py",d],check=True)
    u=(mp/"MapUnit.kt").read_text()
    p=(mp/"UnitPromotions.kt").read_text()
    t=(mp/"EmmTypedDamage.kt").read_text()
    assert u.count("var emmLevel: Int = 1")==1
    assert u.count("newUnit.emmLevel = emmLevel")==1
    assert p.count("unit.emmLevel++")==1
    assert "level = unit.emmLevel," in t
    assert p.index("unit.emmLevel++")>p.index("numberOfPromotions++")
print("PASS: persisted level, no free-promotion inflation, copy/upgrade and typed damage usage")
