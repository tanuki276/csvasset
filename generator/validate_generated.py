#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,math
from collections import Counter,defaultdict
from pathlib import Path

def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument("root",type=Path,nargs="?",default=Path("generated"));a=ap.parse_args()
 root=a.root;errs=[];summary=json.loads((root/"summary.json").read_text());ids=set();stats=defaultdict(lambda:[0,Counter(),Counter(),Counter(),set()])
 with (root/"manifest.csv").open(encoding="utf-8",newline="") as f:manifest=list(csv.DictReader(f))
 if sum(int(x["rows"]) for x in manifest)!=summary["total_rows"]:errs.append("manifest total mismatch")
 for m in manifest:
  p=root/m["file"]
  if not p.exists():errs.append(f"missing {p}");continue
  if sha(p)!=m["sha256"]:errs.append(f"sha mismatch {p}")
  with p.open(encoding="utf-8",newline="") as f:
   r=csv.DictReader(f);count=0
   for row in r:
    count+=1;rid=row["id"];tier=int(row["tier"]);grade=int(row["grade"])
    if rid in ids:errs.append(f"duplicate {rid}")
    ids.add(rid)
    if not rid.startswith(m["pack"]+"_"):errs.append(f"namespace {rid}")
    if not 1<=tier<=20 or not 0<=grade<=4:errs.append(f"range {rid}")
    for k,v in row.items():
     if k in ("id","seed_key","archetype"):continue
     try:
      x=float(v)
      if not math.isfinite(x):raise ValueError
     except:errs.append(f"numeric {rid}:{k}")
    s=stats[(m["pack"],m["dataset"])];s[0]+=1;s[1][tier]+=1;s[2][grade]+=1;s[3][row["archetype"]]+=1
    s[4].add(tuple(v for k,v in row.items() if k not in ("id","seed_key")))
   if count!=int(m["rows"]):errs.append(f"rows {p}")
 report=[]
 for (pack,ds),s in sorted(stats.items()):
  rows,tiers,grades,arches,sigs=s;ratio=len(sigs)/rows
  if rows!=summary["rows_per_dataset"]:errs.append(f"dataset rows {pack}/{ds}")
  if len(tiers)!=20 or len(grades)!=5 or len(arches)<3:errs.append(f"coverage {pack}/{ds}")
  if ratio<.95:errs.append(f"diversity {pack}/{ds} {ratio:.4f}")
  report.append((pack,ds,rows,len(tiers),len(grades),len(arches),f"{ratio:.6f}","ok"))
 with (root/"quality_report.csv").open("w",encoding="utf-8",newline="") as f:
  w=csv.writer(f);w.writerow(["pack","dataset","rows","tiers","grades","archetypes","unique_signature_ratio","status"]);w.writerows(report)
 if errs:
  print("\n".join("ERROR "+x for x in errs[:100]));raise SystemExit(f"{len(errs)} validation errors")
 print(f"CSVASSET generated validation OK: {summary['total_rows']} rows, {len(stats)} datasets, {len(manifest)} shards")
if __name__=="__main__":main()
