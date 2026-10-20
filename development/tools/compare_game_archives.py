#!/usr/bin/env python3
"""Inventory full FFH2/ExtraModMod archives without extracting untrusted paths.

Usage:
 python development/tools/compare_game_archives.py --emm ExtraModMod.zip --ffh "Fall from Heaven 2.zip" --out development/reference/local-archive-audit.json

Output contains metadata and content hashes, not copyrighted game data.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

def normalized(path):
    bits = PurePosixPath(path.replace("\\","/")).parts
    if not bits or ".." in bits:
        return None
    # Drop packaging folder if file trees include an archive wrapper.
    for anchor in ("Assets", "XML", "Python", "Art", "CvGameCoreDLL"):
        if anchor in bits:
            return "/".join(bits[bits.index(anchor):])
    return "/".join(bits)

def category(name):
    p = name.lower()
    if p.endswith(".xml"): return "XML"
    if p.endswith(".py"): return "Python"
    if p.endswith((".dll", ".pyd", ".exe")): return "DLL/binary"
    if p.endswith((".dds",".nif",".kf",".kfm",".tga",".png",".jpg",".jpeg",".bmp",".fpk",".webp")): return "Artwork/asset"
    return "Other"

def inspect(path):
    results={}
    duplicates=[]
    with zipfile.ZipFile(path, "r") as archive:
        for item in archive.infolist():
            if item.is_dir(): continue
            key=normalized(item.filename)
            if not key: continue
            with archive.open(item) as stream:
                hasher=hashlib.sha256()
                while part:=stream.read(1024*1024): hasher.update(part)
            entry={"archivePath":item.filename,"size":item.file_size,"sha256":hasher.hexdigest(),"category":category(key)}
            if key in results: duplicates.append(key)
            results[key]=entry
    return results,duplicates

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--emm",type=Path,required=True)
    ap.add_argument("--ffh",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    emm,ed=inspect(a.emm); ffh,fd=inspect(a.ffh)
    ek,fk=set(emm),set(ffh)
    shared=ek&fk
    changed=sorted(p for p in shared if emm[p]["sha256"]!=ffh[p]["sha256"])
    ident=sorted(p for p in shared if emm[p]["sha256"]==ffh[p]["sha256"])
    unique_emm=sorted(ek-fk)
    unique_ffh=sorted(fk-ek)
    output={
        "emm":str(a.emm),"ffh":str(a.ffh),
        "counts":{"emm":len(emm),"ffh":len(ffh),"identical":len(ident),"modified":len(changed),
                  "extraModModOnly":len(unique_emm),"ffhOnly":len(unique_ffh)},
        "byCategory":{
          k:dict(Counter(category(p) for p in v))
          for k,v in {"identical":ident,"modified":changed,"extraModModOnly":unique_emm,"ffhOnly":unique_ffh}.items()
        },
        "fileLists":{"modified":changed,"extraModModOnly":unique_emm,"ffhOnly":unique_ffh},
        "duplicates":{"emm":ed,"ffh":fd},
        "assetsInEmm":[{"path":p,"size":emm[p]["size"]} for p in sorted(ek) if category(p)=="Artwork/asset"],
        "assetsInFfh":[{"path":p,"size":ffh[p]["size"]} for p in sorted(fk) if category(p)=="Artwork/asset"]
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(output["counts"],indent=2))
    print(json.dumps(output["byCategory"],indent=2))
    print("Saved",a.out)
if __name__=="__main__":main()
