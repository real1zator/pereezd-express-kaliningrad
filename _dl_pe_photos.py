#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download all 15 Avito photos for Pereezd Express and rebuild site."""
import sys, json, re, time, random, pathlib, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = pathlib.Path(r"D:\PROJCT\САЙТ\Сайты-По-Темам\Переезд-1\_avito_data.json")
OUT_DIR = pathlib.Path(r"D:\PROJCT\САЙТ\Сайты-По-Темам\Переезд-1")

data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
photo_urls = data.get("photos", [])
print(f"Фото для скачивания: {len(photo_urls)}")

UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

def dl(url, dest):
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"  {dest.name} — уже есть ({dest.stat().st_size//1024} КБ)")
        return True
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": random.choice(UA),
                    "Accept": "image/webp,image/apng,image/jpeg,*/*;q=0.8",
                    "Referer": "https://www.avito.ru/",
                    "Accept-Language": "ru-RU,ru;q=0.9",
                },
            )
            ctx = __import__('ssl').create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = __import__('ssl').CERT_NONE
            with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                raw = r.read()
            if len(raw) > 3000:
                dest.write_bytes(raw)
                print(f"  {dest.name} ({len(raw)//1024} КБ)")
                return True
        except Exception as e:
            print(f"  попытка {attempt+1} ошибка: {e}")
            time.sleep(1.5 * (attempt + 1))
    print(f"  FAIL: {dest.name}")
    return False

downloaded = []
for i, url in enumerate(photo_urls[:10], 1):
    dest = OUT_DIR / f"avito_{i}.jpg"
    if dl(url, dest):
        downloaded.append(dest)
    time.sleep(0.5)

print(f"\nСкачано: {len(downloaded)}/{len(photo_urls[:10])}")

# Also list existing webp photos
webp_photos = sorted(OUT_DIR.glob("photo_*.webp"))
print(f"Кэш-фото: {len(webp_photos)}")

# Combined photo list: avito first, then webp cache
all_photos = downloaded + [p for p in webp_photos if p not in downloaded]
print(f"Всего: {len(all_photos)} фото для сайта")
