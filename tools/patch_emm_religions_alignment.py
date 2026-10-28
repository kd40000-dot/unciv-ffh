#!/usr/bin/env python3
"""Generate source-pinned EMM religions/alignment and persistent civilization state.

Phase 1: canonical definitions, original tech requirements, alignment targets,
and saved civilization alignment and state religion, with deterministic
transition functions. Founding, spread, priest units and UI are later phases.
"""
from pathlib import Path
import subprocess,sys,xml.etree.ElementTree as ET,json,re
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
emm=Path(sys.argv[2] if len(sys.argv)>2 else "upstream-emm")
rev=subprocess.check_output(["git","-C",str(emm),"rev-parse","HEAD"],text=True).strip()
assert rev=="60b0ec3740083162aaab7bf8491761a54a65a610",rev
def tag(x):return x.tag.rsplit("}",1)[-1]
def field(x,k):return next((a.text for a in x if tag(a)==k),None)
align=ET.parse(emm/"XML/Basicinfos/CIV4AlignmentInfos.xml").getroot()
alignment=[field(x,"Type") for x in align.iter() if tag(x)=="AlignmentInfo"]
assert alignment==["ALIGNMENT_GOOD","ALIGNMENT_NEUTRAL","ALIGNMENT_EVIL"],alignment
rels=ET.parse(emm/"XML/Gameinfo/CIV4ReligionInfo.xml").getroot()
records=[]
for item in rels.iter():
    if tag(item)!="ReligionInfo":continue
    key=field(item,"Type")
    records.append(dict(key=key,tech=field(item,"TechPrereq"),
        alignment=field(item,"Alignment"),best=field(item,"AlignmentBest"),
        worst=field(item,"AlignmentWorst"),spread=int(field(item,"iSpreadFactor") or 0),
        counterFound=int(field(item,"iGlobalCounterFound") or 0),
        counterSpread=int(field(item,"iGlobalCounterSpread") or 0),
        hidden=(field(item,"bHidden")=="1")))
assert len(records)==7 and len({x["key"] for x in records})==7
assert all(x["alignment"] in alignment for x in records)
destination=Path("docs/data/emm-religions-alignment.json")
data={"sourceRevision":rev,"alignments":alignment,"religions":records}
out=json.dumps(data,indent=2)+"\n"
if not destination.exists() or destination.read_text()!=out:destination.write_text(out)
def lit(s):return json.dumps(s) if s else "null"
entries=",\n".join('        Religion(%s, %s, %s, %s, %s, %d, %d, %d, %s)'%(
    lit(x["key"]),lit(x["tech"]),lit(x["alignment"]),lit(x["best"]),lit(x["worst"]),
    x["spread"],x["counterFound"],x["counterSpread"],str(x["hidden"]).lower()) for x in records)
generated=root/"core/src/com/unciv/logic/civilization/EmmReligions.kt"
generated.write_text('''package com.unciv.logic.civilization

/** Source-pinned EMM religion definitions and alignment transition baseline.
 * Game events and leader-specific exceptions will use this canonical state.
 */
object EmmReligions {
    data class Religion(
        val key: String, val tech: String?, val alignment: String,
        val best: String?, val worst: String?, val spreadFactor: Int,
        val counterOnFound: Int, val counterOnSpread: Int, val hidden: Boolean
    )
    val source = listOf(
%s
    )
    private val byKey = source.associateBy { it.key }
    val alignmentTypes = setOf("ALIGNMENT_GOOD", "ALIGNMENT_NEUTRAL", "ALIGNMENT_EVIL")

    fun adopt(civ: Civilization, religionKey: String): Boolean {
        val religion = byKey[religionKey] ?: return false
        if (civ.emmStateReligion == religion.key) return false
        civ.emmStateReligion = religion.key
        civ.emmAlignment = religion.alignment
        return true
    }

    fun changeAlignment(civ: Civilization, alignment: String): Boolean {
        if (alignment !in alignmentTypes || civ.emmAlignment == alignment) return false
        civ.emmAlignment = alignment
        return true
    }
}
''' % entries)
civ=root/"core/src/com/unciv/logic/civilization/Civilization.kt"
s=civ.read_text()
if "var emmAlignment: String" not in s:
    anchor="    var religionManager = ReligionManager()"
    assert s.count(anchor)==1
    s=s.replace(anchor,anchor+'''
    /** EMM alignment; null until leader/civilization initialization is installed. */
    var emmAlignment: String? = null
    /** EMM state religion; distinct from Unciv's ReligionManager. */
    var emmStateReligion: String? = null''')
    anchor="        toReturn.religionManager = religionManager.clone()"
    assert s.count(anchor)==1
    s=s.replace(anchor,anchor+'''
        toReturn.emmAlignment = emmAlignment
        toReturn.emmStateReligion = emmStateReligion''')
    civ.write_text(s)
print("Installed 7 source EMM religions, 3 alignments and serialized civ state")
