#!/usr/bin/env python3
"""Generate the Craftable Houses Plains Starter Cottage .mcstructure."""
from __future__ import annotations
import argparse, hashlib, struct
from collections import Counter
from pathlib import Path
TAG_END=0; TAG_BYTE=1; TAG_INT=3; TAG_STRING=8; TAG_LIST=9; TAG_COMPOUND=10
BLOCK_VERSION=18168865
SIZE_X,SIZE_Y,SIZE_Z=11,8,9
VOID=None; AIR="minecraft:air"
def sp(s):
    b=s.encode("utf-8"); return struct.pack("<H",len(b))+b
def nt(t,n,p): return bytes([t])+sp(n)+p
def ip(v): return struct.pack("<i",v)
def bp(v): return struct.pack("<b",v)
def lp(t,ps): return bytes([t])+struct.pack("<i",len(ps))+b"".join(ps)
def cp(es): return b"".join(es)+bytes([TAG_END])
def plan():
    b={(x,y,z):VOID for x in range(SIZE_X) for y in range(SIZE_Y) for z in range(SIZE_Z)}
    def s(x,y,z,v): b[(x,y,z)]=v
    for x in range(1,10):
        for z in range(1,8): s(x,0,z,"minecraft:cobblestone" if x in (1,9) or z in (1,7) else "minecraft:oak_planks")
    for x in range(4,7): s(x,0,0,"minecraft:cobblestone")
    for x in range(2,9):
        for y in range(1,5):
            for z in range(2,7): s(x,y,z,AIR)
    for y in range(1,5):
        for x in range(1,10):
            for z in range(1,8):
                if x in (1,9) or z in (1,7): s(x,y,z,"minecraft:oak_planks")
    for y in range(1,5):
        for x,z in ((1,1),(9,1),(1,7),(9,7),(4,1),(6,1),(3,7),(7,7)): s(x,y,z,"minecraft:oak_log")
    for y in (1,2): s(5,y,1,AIR)
    for x in (2,3,7,8):
        for y in (2,3): s(x,y,1,"minecraft:glass")
    for x in (1,9):
        for z in (3,4):
            for y in (2,3): s(x,y,z,"minecraft:glass")
    for x in (4,5,6):
        for y in (2,3): s(x,y,7,"minecraft:glass")
    s(2,1,6,"minecraft:crafting_table"); s(8,1,6,"minecraft:bookshelf"); s(8,2,6,"minecraft:bookshelf")
    for x in range(2,9): s(x,5,1,"minecraft:oak_planks"); s(x,5,7,"minecraft:oak_planks")
    for x in range(4,7): s(x,6,1,"minecraft:oak_planks"); s(x,6,7,"minecraft:oak_planks")
    for z in range(0,9):
        for x in (0,1,9,10): s(x,5,z,"minecraft:oak_planks")
        for x in (2,3,7,8): s(x,6,z,"minecraft:oak_planks")
        for x in (4,5,6): s(x,7,z,"minecraft:oak_planks")
    for y in range(4,8): s(8,y,5,"minecraft:cobblestone")
    return b
def binary(b):
    palette=[("minecraft:air",{}),("minecraft:oak_planks",{}),("minecraft:cobblestone",{}),("minecraft:oak_log",{"pillar_axis":"y"}),("minecraft:glass",{}),("minecraft:crafting_table",{}),("minecraft:bookshelf",{})]
    pi={(n,tuple(sorted(s.items()))):i for i,(n,s) in enumerate(palette)}
    primary=[]
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            for z in range(SIZE_Z):
                v=b[(x,y,z)]
                if v is VOID: primary.append(-1)
                elif v=="minecraft:oak_log": primary.append(pi[(v,(("pillar_axis","y"),))])
                else: primary.append(pi[(v,())])
    secondary=[-1]*(SIZE_X*SIZE_Y*SIZE_Z)
    pcs=[]
    for name,states in palette:
        ses=[]
        for k,v in states.items(): ses.append(nt(TAG_STRING,k,sp(v)))
        pcs.append(cp([nt(TAG_STRING,"name",sp(name)),nt(TAG_COMPOUND,"states",cp(ses)),nt(TAG_INT,"version",ip(BLOCK_VERSION))]))
    default=cp([nt(TAG_LIST,"block_palette",lp(TAG_COMPOUND,pcs)),nt(TAG_COMPOUND,"block_position_data",cp([]))])
    structure=cp([nt(TAG_LIST,"block_indices",lp(TAG_LIST,[lp(TAG_INT,[ip(v) for v in primary]),lp(TAG_INT,[ip(v) for v in secondary])])),nt(TAG_LIST,"entities",lp(TAG_COMPOUND,[])),nt(TAG_COMPOUND,"palette",cp([nt(TAG_COMPOUND,"default",default)]))])
    root=cp([nt(TAG_INT,"format_version",ip(1)),nt(TAG_LIST,"size",lp(TAG_INT,[ip(SIZE_X),ip(SIZE_Y),ip(SIZE_Z)])),nt(TAG_COMPOUND,"structure",structure),nt(TAG_LIST,"structure_world_origin",lp(TAG_INT,[ip(0),ip(0),ip(0)]))])
    return bytes([TAG_COMPOUND])+sp("")+root
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="projects/craftable-houses/behavior_pack/structures/craftable/plains_starter_cottage.mcstructure"); a=ap.parse_args()
    b=plan(); raw=binary(b); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(raw)
    counts=Counter(v for v in b.values() if v not in (VOID,AIR))
    print(f"Wrote {out}\nSize: {SIZE_X}x{SIZE_Y}x{SIZE_Z}\nBytes: {len(raw)}\nSHA-256: {hashlib.sha256(raw).hexdigest()}")
    for k,v in sorted(counts.items()): print(f"{k}: {v}")
if __name__=="__main__": main()
