#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebuild Pereezd-1 site with cached webp photos.
"""
import sys, re, shutil, pathlib
sys.stdout.reconfigure(encoding='utf-8')

SRC = pathlib.Path(r"D:\PROJCT\САЙТ\сайты\сделаны")
DST = pathlib.Path(r"D:\PROJCT\САЙТ\Сайты-По-Темам\Переезд-1")

# Photos with close timestamps (likely from one cargo/moving listing)
WANT = [
    "d3821d54da4b50fcd6498cf955d5a68a651568de-1760334837.webp",
    "d27edf08dc2e70a2eff2288c25a191f8e0f87c38-1760334863.webp",
    "bd6d65f7131312c539cfb35bfb12872d74601856-1760334889.webp",
    "8bd705952275cdbf3bb842abd0330ef1958b5931-1760334916.webp",
    "1d9991266b7c2c4b1ec944252e28b3cb311eb3d3-1760334941.webp",
]

photos = []
for i, name in enumerate(WANT, 1):
    src = SRC / name
    if src.exists():
        dest_name = f"photo_{i}.webp"
        dest = DST / dest_name
        shutil.copy2(src, dest)
        photos.append(dest_name)
        print(f"  photo_{i}.webp ← {name} ({src.stat().st_size//1024} КБ)")
    else:
        print(f"  SKIP: {name} — не найдено")

print(f"\nФото скопировано: {len(photos)}")

# Also add 2 more with 1758 series timestamps
WANT2 = [
    "b556d50d75d3fdf8728d574ec107aa9948ae5329-1758089709.webp",
    "1167767b36520184d744809ac5501afa2ec77e5a-1758090021.webp",
]
for i, name in enumerate(WANT2, len(photos)+1):
    src = SRC / name
    if src.exists():
        dest_name = f"photo_{i}.webp"
        dest = DST / dest_name
        shutil.copy2(src, dest)
        photos.append(dest_name)
        print(f"  photo_{i}.webp ← {name} ({src.stat().st_size//1024} КБ)")

print(f"\nВсего: {len(photos)} фото")
for p in photos:
    print(f"  {p}")
