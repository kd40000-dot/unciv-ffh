#!/usr/bin/env python3
"""Extract exact EMM disease/plague related promotion XML fields for an audit."""
import json,sys,xml.etree.ElementTree as ET
from pathlib import Path
root=ET.parse(Path(sys.argv[1])/'XML/Units/CIV4PromotionInfos.xml').getroot()
for e in root.iter():
 if '}' in e.tag:e.tag=e.tag.rsplit('}',1)[-1]
targets={'PROMOTION_DISEASED','PROMOTION_PLAGUED','PROMOTION_POISONED','PROMOTION_IMMUNE_TO_DISEASE','PROMOTION_IMMUNE_DISEASE'}
result={}
for e in root.iter('PromotionInfo'):
 name=e.findtext('Type')
 if name not in targets:continue
 result[name]={child.tag:child.text.strip() for child in e if child.text and child.text.strip()}
out=Path('docs/data/emm-disease-promotions.json')
out.write_text(json.dumps({'commit':'60b0ec3740083162aaab7bf8491761a54a65a610','source':'XML/Units/CIV4PromotionInfos.xml','promotions':result},indent=2)+'\n')
print('Extracted promotions:',list(result))
assert 'PROMOTION_DISEASED' in result and 'PROMOTION_PLAGUED' in result
