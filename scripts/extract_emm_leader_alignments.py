#!/usr/bin/env python3
"""Extract selected EMM leader alignments from pinned EMM source XML."""
import json,sys,xml.etree.ElementTree as ET
from pathlib import Path
src=Path(sys.argv[1]); root=ET.parse(src/'XML/Civilizations/CIV4LeaderHeadInfos.xml').getroot()
for el in root.iter():
 if '}' in el.tag:el.tag=el.tag.rsplit('}',1)[-1]
leaders={}
for info in root.iter('LeaderHeadInfo'):
 ident=info.findtext('Type')
 if ident: leaders[ident]=info.findtext('Alignment') or info.findtext('DefaultAlignment')
j=json.loads(Path('docs/data/emm-civilizations.json').read_text())
mapping={}
for civ in j['civilizations']:
 if not civ['playable']:continue
 leader=civ['chosenLeader']
 value=leaders.get(leader)
 assert value in ('ALIGNMENT_GOOD','ALIGNMENT_NEUTRAL','ALIGNMENT_EVIL'),(civ['name'],leader,value)
 mapping[civ['name']]={'leader':leader,'alignment':value}
assert len(mapping)==19
out={'commit':'60b0ec3740083162aaab7bf8491761a54a65a610','source':'XML/Civilizations/CIV4LeaderHeadInfos.xml','selectedCivilizations':mapping}
Path('docs/data/emm-leader-alignments.json').write_text(json.dumps(out,indent=2)+'\n')
print('Extracted 19 selected EMM leader alignments')
