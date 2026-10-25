#!/usr/bin/env python3
"""Deterministic themed temporary sprites for the scoped queue."""
import json,hashlib,random,argparse
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
Q=R/'art/SCOPED_UNIT_REDRAW_QUEUE.json'
A=R/'placeholder-generated.atlas'
N=R/'jsons/Nations.json'
THEMES={'Balseraphs':'jester','Clan of Embers':'orc','Calabim':'vampire','Bannor':'crusader','Ljosalfar':'forest','Svartalfar':'shadow','Khazad':'dwarf','Luchuirp':'dwarf','Lanun':'pirate','Illians':'frost','Doviello':'tribal','Malakim':'desert','Sheaim':'occult','Infernals':'demon','Hippus':'rider','Mercurians':'angel','Sidar':'shadow','Grigori':'adventurer'}
INK=(32,26,30,255); STEEL=(173,185,195,255); WOOD=(117,76,48,255); GOLD=(228,186,72,255)
def mix(a,b,t):return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))+(255,)
def unitrole(n):
 n=n.lower()
 if any(x in n for x in ('galley','caravel','galleon','frigate','trireme','privateer','workboat','queen of the line')):return 'ship'
 if any(x in n for x in ('horse','rider','chariot','knight','elephant')):return 'mounted'
 if any(x in n for x in ('adept','mage','wizard','shaman','archmage','priest','warlock')):return 'mage'
 if any(x in n for x in ('archer','bow','ranger','hunter','slinger','javelin','marksman')):return 'bow'
 if any(x in n for x in ('scout','assassin','harlequin','mimic')):return 'scout'
 if any(x in n for x in ('catapult','cannon')):return 'siege'
 if any(x in n for x in ('phalanx','spearman','pikeman')):return 'spear'
 return 'melee'
def draw(row,nations):
 name=row['unit'];civ=row['civilization'];theme=THEMES.get(civ,'adventurer');role=unitrole(name)
 raw=nations.get(civ,{}).get('outerColor',[170,85,110]);accent=nations.get(civ,{}).get('innerColor',[45,40,48])
 main=tuple(raw)+(255,);dark=tuple(accent)+(255,)
 if sum(main[:3])<190:main=mix(main,(235,219,180,255),.42)
 if sum(main[:3])>690:main=mix(main,(106,84,75,255),.33)
 trim=mix(main,(255,248,215,255),.40)
 seed=int(hashlib.sha256((civ+'|'+name).encode()).hexdigest()[:10],16);v=seed%5
 skin={'orc':(115,145,75,255),'vampire':(215,209,204,255),'dwarf':(194,144,108,255),'forest':(222,189,151,255),'shadow':(192,186,194,255),'demon':(169,74,65,255)}.get(theme,(208,166,132,255))
 im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im);s=4
 def poly(points,color,width=3):
  pts=[(round(x*s),round(y*s)) for x,y in points];d.polygon(pts,fill=color);d.line(pts+[pts[0]],fill=INK,width=width*s,joint='curve')
 def line(points,color,width=3):
  pts=[(round(x*s),round(y*s)) for x,y in points]
  d.line(pts,fill=INK,width=(width+3)*s,joint='curve');d.line(pts,fill=color,width=width*s,joint='curve')
 def circ(x,y,r,color):
  d.ellipse(((x-r)*s,(y-r)*s,(x+r)*s,(y+r)*s),fill=color,outline=INK,width=2*s)
 if role=='ship':
  poly([(15,79),(111,79),(96,103),(37,105)],dark)
  poly([(23,80),(105,80),(94,90),(36,91)],main)
  line([(64,80),(64,25)],WOOD,3)
  poly([(68,27),(103,58),(68,64)],trim)
  poly([(59,32),(29,66),(59,68)],main)
  for x in (40,63,87):circ(x,88,3,GOLD)
 elif role=='siege':
  poly([(25,79),(95,76),(106,93),(36,98)],WOOD)
  for x in (39,88):circ(x,97,12,dark);circ(x,97,4,GOLD)
  line([(51,85),(93,20)],WOOD,6)
  poly([(86,16),(102,18),(108,34),(85,38)],STEEL)
 else:
  mounted=role=='mounted';cx=61 if mounted else 64;y=22 if mounted else 31
  broad=19 if theme in ('orc','dwarf','tribal') else 14
  if mounted:
   poly([(10,78),(35,66),(89,68),(111,57),(120,70),(103,86),(31,92)],WOOD)
   for x in (29,51,82,100):poly([(x,83),(x+9,81),(x+7,116),(x,116)],dark)
  else:
   poly([(cx-16,78),(cx-1,80),(cx-5,116),(cx-22,118)],dark)
   poly([(cx+3,80),(cx+15,79),(cx+21,118),(cx+5,116)],dark)
  if role=='mage' or theme in ('vampire','shadow','occult'):
   poly([(cx-broad,y+13),(cx+broad,y+13),(cx+broad+12,103),(cx-broad-12,104)],dark)
  poly([(cx-broad,y+21),(cx-broad-12,y+32),(cx-broad-6,84),(cx-broad+2,75)],skin)
  poly([(cx+broad,y+21),(cx+broad+12,y+31),(cx+broad+7,84),(cx+broad-2,76)],skin)
  poly([(cx-broad,y+14),(cx,y+9),(cx+broad,y+14),(cx+broad+5,81),(cx,86),(cx-broad-5,80)],main)
  poly([(cx-5,y+16),(cx+4,y+15),(cx+2,81),(cx-7,81)],dark,2)
  circ(cx,y,11,skin)
  if theme=='jester':
   poly([(cx-11,y-7),(cx-20,y-24),(cx-7,y-17),(cx+2,y-7)],main)
   poly([(cx+2,y-8),(cx+15,y-23),(cx+24,y-12),(cx+10,y-5)],dark)
   circ(cx-20,y-24,3,GOLD);circ(cx+24,y-12,3,GOLD)
   for o in (-10,8):poly([(cx+o,y+34),(cx+o+6,y+26),(cx+o+12,y+34),(cx+o+6,y+42)],GOLD,2)
  elif theme=='crusader':
   poly([(cx-14,y-8),(cx,y-19),(cx+14,y-8),(cx+12,y+6),(cx-12,y+6)],STEEL)
   poly([(cx-3,y+22),(cx+3,y+22),(cx+3,y+48),(cx-3,y+48)],GOLD,1)
   poly([(cx-12,y+30),(cx+12,y+30),(cx+12,y+35),(cx-12,y+35)],GOLD,1)
  elif theme in ('forest','shadow','occult','frost','desert'):
   poly([(cx-17,y+3),(cx-14,y-20),(cx,y-26),(cx+14,y-20),(cx+17,y+3)],dark)
  elif theme=='vampire':
   poly([(cx-14,y-8),(cx,y-18),(cx+14,y-8),(cx+11,y+2),(cx-11,y+2)],dark)
   poly([(cx-12,y+14),(cx+12,y+14),(cx,y+42)],GOLD)
  elif theme=='pirate':
   poly([(cx-22,y-8),(cx,y-20),(cx+22,y-8),(cx+8,y-2)],dark)
  elif theme=='dwarf':
   poly([(cx-13,y-8),(cx,y-20),(cx+13,y-8),(cx+11,y+4),(cx-11,y+4)],STEEL)
   poly([(cx-9,y+7),(cx+9,y+7),(cx+5,y+22),(cx,y+25),(cx-6,y+19)],WOOD)
  elif theme=='orc':poly([(cx-11,y+7),(cx-17,y+15),(cx-6,y+11)],skin)
  else:poly([(cx-13,y-7),(cx,y-17),(cx+13,y-7),(cx+12,y)],dark)
  right=cx+broad+16;left=cx-broad-13
  if role=='bow':
   line([(right,y+3),(right+12,y+30),(right,104)],WOOD,3)
   line([(right,y+3),(right,104)],trim,1)
  elif role=='mage':
   line([(right,y-20),(right,115)],WOOD,3);circ(right,y-23,8,GOLD)
  elif role in ('spear','scout'):
   line([(right,y-29),(right,113)],WOOD,3)
   poly([(right-7,y-29),(right,y-44),(right+7,y-29)],STEEL)
  else:
   line([(right,y+5),(right+4,93)],WOOD,4)
   poly([(right-4,y-2),(right+13,y-14),(right+22,y+2),(right+7,y+18)],STEEL)
  if role in ('melee','spear') and v!=1:
   poly([(left-12,y+22),(left+9,y+17),(left+13,y+52),(left-13,y+58)],dark)
   poly([(left-8,y+27),(left+5,y+24),(left+8,y+48),(left-7,y+51)],main,2)
  if v==0:poly([(cx-broad,y+13),(cx-broad-14,y+18),(cx-broad-4,y+28)],GOLD)
  elif v==1:poly([(cx+broad,y+13),(cx+broad+15,y+15),(cx+broad+5,y+30)],STEEL)
  elif v==2:circ(cx-broad-6,y+21,6,GOLD)
  elif v==3:poly([(cx-broad,y+13),(cx-broad-12,y+6),(cx-broad-11,y+28)],dark)
  else:poly([(cx+broad,y+12),(cx+broad+14,y+21),(cx+broad+4,y+27)],trim)
 return im
def register(atlas,rel):
 key=str(rel).replace('\\','/')
 name=rel.stem
 block=key+'\nsize: 512, 512\nformat: RGBA8888\nfilter: Linear, Linear\nrepeat: none\n'
 for tileset in ('AmuritesSimple','AbsoluteUnits'):
  block+='TileSets/'+tileset+'/Units/'+name+'\n  rotate: false\n  xy: 0, 0\n  size: 512, 512\n  orig: 512, 512\n  offset: 0, 0\n  index: -1\n'
 start=atlas.find(key+'\n')
 if start>=0:
  end=atlas.find('\n\n',start)
  if end<0:end=len(atlas)
  return atlas[:start]+block.rstrip()+atlas[end:]
 return atlas.rstrip()+'\n\n'+block
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--all',action='store_true');args=ap.parse_args()
 queue=json.loads(Q.read_text());nations={x['name']:x for x in json.loads(N.read_text())}
 atlas=A.read_text();n=0
 pilot={'Balseraphs','Clan of Embers','Calabim','Bannor'}
 for row in queue['entries']:
  civ=row['civilization'];name=row['unit'];path=row['path']
  if not args.all and civ not in pilot:continue
  if civ=='Amurites' or name in ('Worker','Settler'):continue
  if row.get('accepted') or row.get('reviewed') or row.get('replacement'):continue
  if '/Generated/' not in path or not path.endswith('.png'):continue
  dest=R/path
  # Approved sheet crops and reviewed artwork must never be replaced.
  if row.get('previous')=='approved-sprite-sheet-crop':continue
  dest.parent.mkdir(parents=True,exist_ok=True)
  im=draw(row,nations);im.save(dest,optimize=True)
  atlas=register(atlas,dest.relative_to(R))
  row.update(previous='procedural-themed-v2',status='temporary-procedural',themeColors='Nations.json',styleQuality='placeholder-only')
  n+=1
 A.write_text(atlas)
 Q.write_text(json.dumps(queue,indent=2,ensure_ascii=False)+'\n')
 print('Generated',n,'themed 512x512 temporary sprites')
if __name__=='__main__':main()
