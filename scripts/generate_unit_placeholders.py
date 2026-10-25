#!/usr/bin/env python3
"""Deterministic, conservative, role/faction-aware procedural Unciv placeholders."""
import json, re, math, io, hashlib
from pathlib import Path
from PIL import Image
import cairosvg

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'Images/TileSets/AmuritesSimple/Units/Generated'
ATLAS=ROOT/'amurites-simple-complete.atlas'
MANIFEST=ROOT/'scripts/placeholder-manifest.json'
SKIP={'Worker','Settler'}
ROLE_VARIANTS={
 'archer':'bow','bow':'bow','crossbow':'bow','hunter':'bow','ranger':'bow',
 'assassin':'dagger','scout':'spear','spearman':'spear','phalanx':'spear','pikeman':'spear',
 'mage':'staff','adept':'staff','wizard':'staff','druid':'staff','priest':'staff','lich':'staff',
 'horse':'spear','chariot':'spear','knight':'sword','paladin':'sword','champion':'sword',
 'axeman':'axe','berserker':'axe','beastmaster':'axe','warrior':'axe','swordsman':'sword'
}
def role(name):
 n=name.lower()
 return next((v for k,v in ROLE_VARIANTS.items() if k in n),'sword')
def rgb(c, fallback):
 if not isinstance(c,list) or len(c)<3:return fallback
 return '#%02x%02x%02x'%tuple(max(0,min(255,int(x))) for x in c[:3])
def shade(c,f):
 v=[int(c[i:i+2],16) for i in (1,3,5)]
 return '#%02x%02x%02x'%tuple(max(0,min(255,int(x*f))) for x in v)
def generate(name,faction,colors):
 seed=int(hashlib.sha256(name.encode()).hexdigest()[:8],16)
 accent=rgb(colors.get('outerColor'),'#8d293a')
 dark=shade(accent,.45); light=shade(accent,1.28)
 skin='#a89181' if faction=='Calabim' else '#7b9461' if faction=='Clan of Embers' else '#c8a58a'
 if faction in ('Ljosalfar','Svartalfar'):skin='#bfae9b'
 if faction=='Khazad':skin='#c5957c'
 if faction=='Illians':skin='#b4c5cf'
 if faction=='Balseraphs':skin='#e3d2c4'
 n=name.lower(); orc=faction=='Clan of Embers' or 'orc' in n or 'goblin' in n
 clown=faction=='Balseraphs'
 undead=any(x in n for x in ('skeleton','lich','spectre','wraith','vampire','bloodpet'))
 if undead:skin='#b7aa9f'
 short='goblin' in n or faction=='Khazad' or 'dwarf' in n
 tall='giant' in n or 'troll' in n or 'ogre' in n
 animal=any(x in n for x in ('wolf','bear','lion','spider','griffon','dragon','elephant'))
 # Do not generate misleading humanoid art for creatures, ships or siege engines.
 if animal or any(x in n for x in ('ship','galley','frigate','boat','catapult','cannon','trebuchet')): return None
 scale=.78 if short else 1.13 if tall else 1.
 # Original silhouettes share the Amurite 512-canvas foot baseline.
 parts=[]
 def p(coords,color,edge='#241c25',width=3):
  points=' '.join(f'{x:.1f},{y:.1f}' for x,y in coords)
  parts.append(f'<polygon points="{points}" fill="{color}" stroke="{edge}" stroke-width="{width}" stroke-linejoin="round"/>')
 def seg(a,b,color='#241c25',w=5):
  parts.append(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')
 def oval(x,y,rx,ry,color):
  parts.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{color}" stroke="#241c25" stroke-width="3"/>')
 # local character coordinates: center 287, baseline 468, top near 193
 def q(points):
  return [(287+(x-287)*scale,468+(y-468)*scale) for x,y in points]
 def poly(coords,c,e='#241c25',w=3):p(q(coords),c,e,w)
 # unique widths and stances by name
 width=23+(seed%12); lean=(seed%13)-6
 # cape, rear limbs and footgear
 poly([(259,260),(310,258),(329,295),(339,392),(315,382),(297,404),(277,385),(252,395),(248,313)],dark)
 poly([(263,286),(270,280),(264,383),(254,388)],accent,'none',0)
 poly([(278,374),(295,374),(285,427),(276,464),(256,463),(261,422)],'#373039')
 poly([(301,376),(319,370),(325,435),(325,465),(302,466),(295,426)],'#282733')
 poly([(257,451),(278,452),(279,473),(249,473),(243,468)],'#282028')
 poly([(303,451),(326,451),(336,471),(298,473),(294,466)],'#282028')
 # armor vs cloth by role
 r=role(name); armor=r in ('axe','sword','spear')
 poly([(264+lean,267),(286,261),(311+lean,268),(327,308),(317,376),(285,388),(254,376),(250,309)],'#444047' if armor else dark)
 poly([(260,295),(279,281),(277,344),(256,350)],accent,'none',0)
 poly([(290,281),(310,292),(314,348),(292,343)],light if not armor else '#64545a','none',0)
 poly([(275,330),(317,334),(320,348),(272,346)],'#27222c')
 poly([(287,332),(300,334),(301,348),(286,347)],'#aa8860')
 for i in range(4):
  x=271+i*11
  poly([(x,352),(x+5,354),(x+3,378),(x-3,381)],shade(accent,.74),'none',0)
 # anatomy/sleeves, individual arm posture
 poly([(261,274),(246,284),(235,323),(244,337),(257,320),(271,292)],shade(accent,.69))
 poly([(310,273),(329,285),(339,320),(327,333),(316,314),(301,293)],shade(accent,.71))
 poly([(237,328),(249,331),(239,376),(229,373)],skin)
 poly([(329,327),(339,328),(350,368),(341,377)],skin)
 # asymmetric pads with angular lighting
 poly([(250,282),(263,267),(274,283),(261,300),(240,297)],'#4d4649')
 poly([(246,284),(261,274),(266,282),(249,294)],light,'none',0)
 poly([(312,268),(329,280),(337,300),(315,302),(302,285)],'#514249')
 poly([(314,275),(326,286),(329,294),(313,290)],light,'none',0)
 # neck face and headgear, not all generic rectangles
 poly([(277,250),(303,248),(308,280),(290,292),(273,281)],skin)
 oval(289+lean,229,19 if not orc else 23,27,skin)
 poly([(274+lean,236),(284,233),(286,241),(276,243)],shade(skin,.5),'none',0)
 poly([(293,232),(306+lean,235),(301,242),(293,238)],shade(skin,.5),'none',0)
 if orc:
  poly([(269,235),(260,241),(273,251)],skin)
  poly([(306,238),(320,245),(307,251)],skin)
  poly([(280,247),(285,256),(276,257)],'#efe0b6')
  poly([(298,247),(304,255),(296,258)],'#efe0b6')
 elif undead:
  poly([(277,229),(283,228),(282,233),(278,234)],'#a72938','none',0)
  poly([(296,229),(302,229),(300,235),(296,234)],'#a72938','none',0)
 if clown:
  poly([(278,233),(287,230),(289,236),(282,241)],'#c42735','none',0)
  poly([(287,246),(295,245),(300,251),(286,254)],'#b83438','none',0)
 # class-specific headgear
 if r=='staff':
  poly([(266,216),(293,175),(316,216),(305,224),(275,224)],shade(accent,.6))
  poly([(270,216),(291,186),(281,219)],accent,'none',0)
 elif r=='bow':
  poly([(267,222),(277,195),(306,191),(318,218),(303,211),(279,211)],dark)
 else:
  poly([(267,218),(277,199),(296,195),(310,213),(303,218),(286,208),(277,226)],'#2b242c')
  poly([(279,203),(297,200),(303,209),(281,212)],accent,'none',0)
 if faction=='Khazad':
  poly([(278,250),(290,264),(303,248),(306,279),(290,287),(274,276)],'#67483b')
 # distinctive accessory and weapon depending on role
 if r=='bow':
  seg((229,302),(221,413),'#926d41',5)
  parts.append('<path d="M229 302 Q180 343 221 413" stroke="#7b4a32" stroke-width="5" fill="none"/>')
  seg((229,302),(221,413),'#ddd8b9',1.4)
  seg((230,362),(294,324),'#c9b69b',3)
  poly([(228,361),(241,350),(243,366)],'#aab0ad')
 elif r=='staff':
  seg((228,249),(228,463),'#5b3c2c',7)
  poly([(228,227),(242,246),(229,265),(215,248)],light)
  poly([(226,228),(237,245),(229,254),(219,244)],'#b6c9dd','none',0)
 elif r=='spear':
  seg((222,462),(231,238),'#79543d',6)
  poly([(232,209),(244,239),(229,264),(220,238)],'#919aa0')
  poly([(232,212),(235,244),(226,247)],'#d2d1bf','none',0)
 elif r=='axe':
  seg((229,336),(215,460),'#6d4b39',7)
  poly([(217,350),(201,350),(192,378),(211,399),(226,379),(236,357)],'#868e94')
  poly([(201,355),(195,379),(211,391),(213,367)],'#c4c6bb','none',0)
 elif r=='dagger':
  seg((235,347),(215,417),'#4e3430',7)
  poly([(212,412),(203,448),(224,422)],'#b1babd')
 else:
  seg((232,348),(214,451),'#664c37',7)
  poly([(230,324),(241,341),(221,420),(211,406)],'#aeb8b9')
  poly([(230,334),(236,341),(219,407)],'#d6d5c7','none',0)
 # final small visual variation: rivets, stitched seams
 for i in range(4):
  x=263+((seed+i*19)%46); y=301+i*15
  parts.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#c4a98b"/>')
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">'+''.join(parts)+'</svg>'
 png=cairosvg.svg2png(bytestring=svg.encode(),output_width=1024,output_height=1024)
 im=Image.open(io.BytesIO(png)).convert('RGBA').resize((512,512),Image.Resampling.LANCZOS)
 box=im.getchannel('A').getbbox()
 if not box or box[3]>492 or box[1]<65:raise ValueError((name,box))
 return im,box,len(parts)
def run():
 nations={x['name']:x for x in json.loads((ROOT/'jsons/Nations.json').read_text())}
 units=json.loads((ROOT/'jsons/Units.json').read_text())
 entries=ATLAS.read_text()
 existing=set(re.findall(r'^TileSets/AmuritesSimple/Units/(.+)$',entries,re.M))
 report={'created':[],'preserved':[],'excluded':[]}
 for unit in units:
  name=unit['name']
  if name in SKIP:continue
  # Explicit per-nation units use -Civilization suffix if available.
  faction=unit.get('replaces') and next((n for n in nations if n.lower() in name.lower()),None)
  faction=faction or next((n for n in nations if name.endswith('-'+n)),None)
  if faction is None: faction=next((n for n in nations if n in name),None)
  if name in existing or (DEST/(name+'.png')).exists():
   report['preserved'].append(name);continue
  # preserve existing approved unmapped art even without atlas entries
  if (DEST.parent/(name+'.png')).exists():
   report['preserved'].append(name);continue
  art=generate(name,faction,nations.get(faction,{}))
  if art is None:
   report['excluded'].append(name);continue
  image,box,count=art
  target=DEST/(name+'.png');target.parent.mkdir(parents=True,exist_ok=True)
  image.save(target,optimize=True)
  block=['',str(target.relative_to(ROOT)),'size: 512, 512','format: RGBA8888',
   'filter: Linear, Linear','repeat: none']
  for atlasname in ['TileSets/AmuritesSimple/Units/'+name,'TileSets/AbsoluteUnits/Units/'+name]:
   block += [atlasname,'  rotate: false','  xy: 0, 0','  size: 512, 512',
             '  orig: 512, 512','  offset: 0, 0','  index: -1']
  entries+='\n'.join(block)+'\n'
  report['created'].append({'unit':name,'faction':faction,'role':role(name),'bounds':list(box),'polygons':count})
 ATLAS.write_text(entries)
 MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
 print('Generated:',len(report['created']),'preserved:',len(report['preserved']),'excluded:',len(report['excluded']))
if __name__=='__main__':run()
