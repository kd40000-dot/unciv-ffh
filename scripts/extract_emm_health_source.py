#!/usr/bin/env python3
"""Inventory source-defined EMM health stats from the pinned EMM XML.
This deliberately produces source evidence, not Unciv gameplay code.
"""
import sys,json,xml.etree.ElementTree as ET
from pathlib import Path
src=Path(sys.argv[1])
out=Path(sys.argv[2])
groups=[
("buildings","XML/Buildings/CIV4BuildingInfos.xml","BuildingInfo"),
("traits","XML/Civilizations/CIV4TraitInfos.xml","TraitInfo"),
("resources","XML/Terrain/CIV4BonusInfos.xml","BonusInfo"),
("features","XML/Terrain/CIV4FeatureInfos.xml","FeatureInfo"),
("handicaps","XML/Gameinfo/CIV4HandicapInfo.xml","HandicapInfo"),
]
doc={"upstream":"bewlay/extramodmod","commit":"60b0ec3740083162aaab7bf8491761a54a65a610","groups":{}}
for group,rel,tag in groups:
 p=src/rel
 if not p.exists():
  print("Missing optional XML:",p)
  continue
 root=ET.parse(p).getroot()
 # Civ4 XML uses x-schema default namespaces; normalize tag names for XPath.
 for e in root.iter():
  if '}' in e.tag:e.tag=e.tag.rsplit('}',1)[-1]
 rows=[]
 for node in root.iter(tag):
  typ=node.findtext("Type")
  if not typ:continue
  evidence={}
  for child in node:
   if ("health" in child.tag.lower() or "unhealth" in child.tag.lower()) and child.text and child.text.strip():
    evidence[child.tag]=child.text.strip()
  if evidence:rows.append({"id":typ,"fields":evidence})
 doc["groups"][group]={"source":rel,"entries":rows}
 print(group,len(rows))
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(doc,indent=2)+"\n")
