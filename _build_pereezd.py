#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build FIT SERVICE-style landing for Pereezd Express (Kaliningrad)
Based on Avito: https://www.avito.ru/kaliningrad/predlozheniya_uslug/pereezdy_gruzoperevozki_dostavki_do_3_tonn_7275388730
"""
import json, os, re, sys, time, pathlib, urllib.request, urllib.error, random
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

AVITO_URL = "https://www.avito.ru/kaliningrad/predlozheniya_uslug/pereezdy_gruzoperevozki_dostavki_do_3_tonn_7275388730"
OUT_DIR = pathlib.Path(r"D:\PROJCT\САЙТ\Сайты-По-Темам\Переезд-1")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── Try to fetch Avito data ───────────────────────────────────────────────

print("Пробую получить данные с Авито...")
avito_data = None

try:
    from avito_parser import parse_avito
    avito_data = parse_avito(AVITO_URL)
    print(f"  Парсер OK: {avito_data.get('name','?')}, фото: {len(avito_data.get('photos',[]))}")
    with open(OUT_DIR / "_avito_data.json", "w", encoding="utf-8") as f:
        json.dump(avito_data, f, ensure_ascii=False, indent=2)
except Exception as e:
    print(f"  Парсер недоступен: {e}")

# ─── Fallback data ────────────────────────────────────────────────────────
if not avito_data or not avito_data.get("name"):
    print("  Использую заготовленные данные.")
    avito_data = {
        "name": "Переезд Экспресс",
        "phone": "+7 (963) 290-09-71",  # Kaliningrad number, adjust if needed
        "city": "Калининград",
        "address": "Калининград",
        "description": (
            "Грузоперевозки по Калининграду и области. "
            "Квартирные и офисные переезды, перевозка мебели и бытовой техники. "
            "Газель (до 3 тонн), опытные грузчики, бережная упаковка. "
            "Работаем без выходных, GPS-мониторинг, страховка груза. "
            "Быстрый выезд в день обращения."
        ),
        "photos": [],
        "prices": [
            {"name": "Заказ Газели (до 3 ч)", "price": "от 1 500 ₽"},
            {"name": "Квартирный переезд 1-комн.", "price": "от 3 000 ₽"},
            {"name": "Квартирный переезд 2-комн.", "price": "от 5 000 ₽"},
            {"name": "Офисный переезд", "price": "от 4 000 ₽"},
            {"name": "Грузчики (2 чел., 2 ч)", "price": "от 2 000 ₽"},
        ],
    }

# ─── Download photos ──────────────────────────────────────────────────────

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

def download_img(url: str, dest: pathlib.Path) -> bool:
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"  {dest.name} — уже есть")
        return True
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": random.choice(UA_LIST),
                    "Accept": "image/webp,image/apng,*/*;q=0.8",
                    "Referer": "https://www.avito.ru/",
                },
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read()
            if len(data) > 5000:
                dest.write_bytes(data)
                print(f"  {dest.name} ({len(data)//1024} КБ)")
                return True
        except Exception as ex:
            print(f"    попытка {attempt+1} ошибка: {ex}")
            time.sleep(1 + attempt)
    return False

photos: list[pathlib.Path] = []
raw_photo_urls = avito_data.get("photos", [])

print(f"\nСкачиваю фото ({len(raw_photo_urls)} шт.)...")
for i, url in enumerate(raw_photo_urls[:8], 1):
    dest = OUT_DIR / f"photo_{i}.jpg"
    if download_img(url, dest):
        photos.append(dest)
    time.sleep(0.3)

# ─── Use pre-cached photos if download failed ─────────────────────────────
if not photos:
    print("  Проверяю наличие фото в папке...")
    for ext in ["jpg", "jpeg", "webp", "png"]:
        found = sorted(OUT_DIR.glob(f"photo_*.{ext}"))
        if found:
            photos.extend(found)
    if photos:
        print(f"  Найдено {len(photos)} предзагруженных фото.")
    else:
        print("  Фото не найдено, используется градиент.")

# ─── Build logo SVG ───────────────────────────────────────────────────────

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 70" width="200" height="70">
  <rect width="200" height="70" rx="6" fill="#1a5c2e"/>
  <!-- Truck icon -->
  <g transform="translate(10,10) scale(0.55)">
    <!-- Cab -->
    <rect x="30" y="18" width="50" height="35" rx="4" fill="none" stroke="white" stroke-width="3"/>
    <rect x="0" y="28" width="32" height="25" rx="3" fill="none" stroke="white" stroke-width="3"/>
    <rect x="4" y="33" width="20" height="12" rx="2" fill="rgba(255,255,255,0.3)" stroke="white" stroke-width="1.5"/>
    <!-- Wheels -->
    <circle cx="15" cy="56" r="8" fill="none" stroke="white" stroke-width="3"/>
    <circle cx="15" cy="56" r="3" fill="white"/>
    <circle cx="65" cy="56" r="8" fill="none" stroke="white" stroke-width="3"/>
    <circle cx="65" cy="56" r="3" fill="white"/>
    <!-- Speed lines -->
    <line x1="-5" y1="35" x2="-18" y2="35" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="-5" y1="42" x2="-22" y2="42" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="-5" y1="49" x2="-16" y2="49" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <!-- Text -->
  <text x="62" y="28" font-family="Arial Black,Arial" font-weight="900" font-size="13" fill="white" letter-spacing="1">ПЕРЕЕЗД</text>
  <text x="62" y="44" font-family="Arial Black,Arial" font-weight="900" font-size="13" fill="white" letter-spacing="1">ЭКСПРЕСС</text>
  <text x="62" y="58" font-family="Arial" font-size="7.5" fill="#a8d5b8" letter-spacing="0.5">ТРАНСПОРТНАЯ КОМПАНИЯ</text>
</svg>"""

# Save logo
logo_file = OUT_DIR / "logo.svg"
logo_file.write_text(LOGO_SVG, encoding="utf-8")

# ─── Determine hero image ─────────────────────────────────────────────────

hero_img = "photo_1.jpg" if photos else None

# ─── Services data ────────────────────────────────────────────────────────

SERVICES = [
    {
        "icon": "🚚",
        "title": "Квартирный переезд",
        "desc": "Полный квартирный переезд под ключ: разборка, упаковка, перевозка, сборка мебели. Бережно и быстро.",
        "price": "от 3 000 ₽",
        "photo": photos[0].name if len(photos) > 0 else None,
    },
    {
        "icon": "🏢",
        "title": "Офисный переезд",
        "desc": "Перевозим оргтехнику, мебель, документы. Работаем в нерабочее время, чтобы не прерывать ваш бизнес.",
        "price": "от 4 000 ₽",
        "photo": photos[1].name if len(photos) > 1 else None,
    },
    {
        "icon": "📦",
        "title": "Доставка грузов",
        "desc": "Доставка любых грузов по Калининграду и области. Газель до 3 тонн. Быстро, в день обращения.",
        "price": "от 1 500 ₽",
        "photo": photos[2].name if len(photos) > 2 else None,
    },
    {
        "icon": "💪",
        "title": "Грузчики",
        "desc": "Профессиональные грузчики с опытом. Подъём, спуск, погрузка и разгрузка без повреждений.",
        "price": "от 1 000 ₽/час",
        "photo": photos[3].name if len(photos) > 3 else None,
    },
    {
        "icon": "📦",
        "title": "Перевозка мебели",
        "desc": "Перевозка и сборка мебели. Фиксация и упаковка стрейч-плёнкой. Без царапин и сколов.",
        "price": "от 1 500 ₽",
        "photo": photos[4].name if len(photos) > 4 else None,
    },
    {
        "icon": "🏗",
        "title": "Вывоз мусора",
        "desc": "Вывоз строительного мусора, старой мебели и бытовой техники. Газель, 1–3 тонны.",
        "price": "от 2 000 ₽",
        "photo": photos[5].name if len(photos) > 5 else None,
    },
]

# ─── Prices ───────────────────────────────────────────────────────────────

PRICES = avito_data.get("prices") or [
    {"name": "Газель, 1 час", "price": "750 ₽"},
    {"name": "Газель до 3 ч", "price": "1 500 ₽"},
    {"name": "Квартирный переезд 1-комн.", "price": "от 3 000 ₽"},
    {"name": "Квартирный переезд 2-комн.", "price": "от 5 000 ₽"},
    {"name": "Офисный переезд (малый)", "price": "от 4 000 ₽"},
    {"name": "Грузчики 2 чел., 2 ч", "price": "от 2 000 ₽"},
    {"name": "Вывоз мусора (Газель)", "price": "от 2 000 ₽"},
]

# ─── Company info ─────────────────────────────────────────────────────────

COMPANY = avito_data.get("name") or "Переезд Экспресс"
PHONE = avito_data.get("phone") or "+7 (963) 290-09-71"
PHONE_CLEAN = re.sub(r"[^\d+]", "", PHONE)
CITY = avito_data.get("city") or "Калининград"
AVITO_LINK = AVITO_URL

# ─── Hero image handling ──────────────────────────────────────────────────

if hero_img:
    hero_css = f"background-image: url('{hero_img}');"
else:
    # gradient fallback
    hero_css = "background: linear-gradient(135deg, #0f3823 0%, #1a5c2e 50%, #2d7a47 100%);"

# ─── Services HTML ────────────────────────────────────────────────────────

def svc_card(s, idx):
    photo_html = ""
    if s.get("photo"):
        photo_html = f'<div class="svc-photo" style="background-image:url({s["photo"]})"></div>'
    return f"""
    <div class="svc-card">
      {photo_html}
      <div class="svc-body">
        <div class="svc-icon">{s["icon"]}</div>
        <h3>{s["title"]}</h3>
        <p>{s["desc"]}</p>
        <div class="svc-price">{s["price"]}</div>
        <a href="tel:{PHONE_CLEAN}" class="svc-btn">Заказать</a>
      </div>
    </div>"""

SERVICES_HTML = "".join(svc_card(s, i) for i, s in enumerate(SERVICES))

# ─── Prices HTML ─────────────────────────────────────────────────────────

def price_row(p):
    return f'<tr><td>{p["name"]}</td><td class="price-val">{p["price"]}</td><td><a href="tel:{PHONE_CLEAN}" class="price-btn">Заказать</a></td></tr>'

PRICES_HTML = "".join(price_row(p) for p in PRICES)

# ─── Photos gallery HTML ──────────────────────────────────────────────────

gallery_items = photos[1:7] if len(photos) > 1 else photos
GALLERY_HTML = ""
for ph in gallery_items:
    GALLERY_HTML += f'<div class="gallery-item" style="background-image:url({ph.name})"></div>\n'

# ─── Build HTML ──────────────────────────────────────────────────────────

HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{COMPANY} — Грузоперевозки в Калининграде. В день обращения!</title>
<meta name="description" content="Грузоперевозки, квартирные и офисные переезды в Калининграде. Газель до 3 тонн. Опытные грузчики. Работаем без выходных. Звоните: {PHONE}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --green:#1a5c2e;
  --green-light:#2d7a47;
  --green-dark:#0f3a1e;
  --orange:#e85d04;
  --orange2:#f48c06;
  --gray:#4a4a4a;
  --light:#f5f5f5;
  --white:#fff;
  --font:'Montserrat',sans-serif;
  --font2:'Open Sans',sans-serif;
}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font2);color:var(--gray);line-height:1.6;background:#fff}}

/* ── TOPBAR ── */
.topbar{{background:var(--green-dark);color:rgba(255,255,255,.8);font-size:13px;padding:6px 0}}
.topbar .wrap{{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}}
.topbar a{{color:inherit;text-decoration:none}}
.topbar-contacts{{display:flex;gap:20px;align-items:center}}
.topbar-rating{{display:flex;align-items:center;gap:6px}}
.stars{{color:#f59e0b}}

/* ── HEADER ── */
.header{{background:var(--white);box-shadow:0 2px 12px rgba(0,0,0,.12);position:sticky;top:0;z-index:100}}
.header .wrap{{display:flex;justify-content:space-between;align-items:center;padding:12px 20px;gap:20px}}
.header-logo{{display:flex;align-items:center;gap:12px;text-decoration:none}}
.header-logo img,.header-logo svg{{height:50px;width:auto}}
.header-nav{{display:flex;gap:24px;list-style:none}}
.header-nav a{{color:var(--gray);text-decoration:none;font-weight:600;font-size:14px;transition:.2s}}
.header-nav a:hover{{color:var(--green)}}
.header-phone{{font-size:20px;font-weight:800;color:var(--green);text-decoration:none;font-family:var(--font)}}
.header-callback{{background:var(--orange);color:#fff;border:none;padding:10px 22px;border-radius:4px;font-weight:700;font-size:14px;cursor:pointer;font-family:var(--font)}}
.header-callback:hover{{background:var(--orange2)}}

/* ── HERO ── */
.hero{{
  position:relative;
  min-height:580px;
  display:flex;
  align-items:center;
  overflow:hidden;
  background-color:var(--green-dark);
  {hero_css}
  background-size:cover;
  background-position:center top;
}}
.hero::before{{
  content:'';
  position:absolute;inset:0;
  background:linear-gradient(to right, rgba(10,35,20,.88) 0%, rgba(10,35,20,.65) 55%, rgba(10,35,20,.2) 100%);
}}
.hero .wrap{{position:relative;z-index:2;padding:60px 20px}}
.hero-badge{{display:inline-block;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);color:#fff;font-size:13px;font-weight:600;padding:5px 14px;border-radius:20px;margin-bottom:18px;letter-spacing:.5px}}
.hero h1{{font-family:var(--font);font-size:clamp(26px,4.5vw,48px);font-weight:900;color:#fff;line-height:1.15;max-width:680px;margin-bottom:16px}}
.hero h1 span{{color:#f59e0b}}
.hero-sub{{color:rgba(255,255,255,.85);font-size:clamp(14px,2vw,17px);max-width:520px;margin-bottom:30px}}
.hero-cta{{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:36px}}
.btn-primary{{background:var(--orange);color:#fff;padding:15px 32px;border-radius:4px;font-weight:800;font-size:16px;text-decoration:none;font-family:var(--font);transition:.2s;display:inline-block}}
.btn-primary:hover{{background:var(--orange2);transform:translateY(-1px)}}
.btn-outline{{border:2px solid rgba(255,255,255,.6);color:#fff;padding:13px 28px;border-radius:4px;font-weight:700;font-size:15px;text-decoration:none;font-family:var(--font);transition:.2s}}
.btn-outline:hover{{background:rgba(255,255,255,.1);border-color:#fff}}
.hero-trust{{display:flex;gap:24px;flex-wrap:wrap}}
.hero-trust-item{{color:rgba(255,255,255,.9);font-size:13px;display:flex;align-items:center;gap:6px}}
.hero-trust-item::before{{content:'✓';color:#4ade80;font-weight:700}}

/* ── FEATURES STRIP ── */
.features-strip{{background:var(--green);padding:24px 0}}
.features-strip .wrap{{display:flex;justify-content:space-around;flex-wrap:wrap;gap:16px}}
.feat-item{{color:#fff;text-align:center;display:flex;flex-direction:column;align-items:center;gap:6px}}
.feat-icon{{font-size:28px}}
.feat-label{{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;opacity:.9}}
.feat-value{{font-size:18px;font-weight:800;font-family:var(--font)}}

/* ── SECTION ── */
section{{padding:64px 0}}
.wrap{{max-width:1200px;margin:0 auto;padding:0 20px}}
.section-title{{font-family:var(--font);font-size:clamp(20px,3.5vw,32px);font-weight:800;color:#1a1a1a;margin-bottom:10px}}
.section-sub{{color:#666;font-size:15px;margin-bottom:36px;max-width:600px}}
.center{{text-align:center}}
.center .section-sub{{margin:0 auto 36px}}

/* ── SERVICES ── */
.services-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px}}
.svc-card{{background:#fff;border:1px solid #e5e7eb;border-radius:8px;overflow:hidden;transition:.3s;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.svc-card:hover{{transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,0,0,.12)}}
.svc-photo{{height:200px;background-size:cover;background-position:center;background-color:#e5e7eb}}
.svc-body{{padding:20px}}
.svc-icon{{font-size:30px;margin-bottom:10px}}
.svc-body h3{{font-family:var(--font);font-size:18px;font-weight:800;color:#1a1a1a;margin-bottom:8px}}
.svc-body p{{font-size:14px;color:#555;margin-bottom:14px;line-height:1.6}}
.svc-price{{font-size:20px;font-weight:800;color:var(--green);font-family:var(--font);margin-bottom:14px}}
.svc-btn{{display:block;text-align:center;background:var(--green);color:#fff;padding:10px 0;border-radius:4px;font-weight:700;font-size:14px;text-decoration:none;transition:.2s}}
.svc-btn:hover{{background:var(--green-light)}}

/* ── HOW IT WORKS ── */
.how-section{{background:var(--light)}}
.steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px;counter-reset:step}}
.step{{background:#fff;border-radius:8px;padding:28px 24px;box-shadow:0 2px 8px rgba(0,0,0,.05);position:relative;counter-increment:step}}
.step::before{{
  content:counter(step,"0"counter(step));
  position:absolute;top:-14px;left:24px;
  background:var(--orange);color:#fff;
  font-family:var(--font);font-weight:900;font-size:14px;
  padding:4px 12px;border-radius:12px;
}}
.step h4{{font-family:var(--font);font-size:16px;font-weight:800;margin:10px 0 8px;color:#1a1a1a}}
.step p{{font-size:14px;color:#666}}

/* ── PRICE TABLE ── */
.price-table{{width:100%;border-collapse:collapse;font-size:15px}}
.price-table th{{background:var(--green);color:#fff;padding:14px 18px;text-align:left;font-family:var(--font);font-weight:700}}
.price-table td{{padding:12px 18px;border-bottom:1px solid #e5e7eb}}
.price-table tr:hover td{{background:#f0fdf4}}
.price-val{{font-weight:700;color:var(--green);font-size:16px;white-space:nowrap}}
.price-btn{{background:var(--orange);color:#fff;padding:6px 16px;border-radius:4px;font-weight:700;font-size:13px;text-decoration:none;white-space:nowrap;display:inline-block}}
.price-btn:hover{{background:var(--orange2)}}

/* ── GALLERY ── */
.gallery{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}}
.gallery-item{{height:220px;background-size:cover;background-position:center;border-radius:8px;background-color:#e5e7eb}}

/* ── BENEFITS ── */
.benefits-section{{background:var(--green-dark);color:#fff}}
.benefits-section .section-title{{color:#fff}}
.benefits-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px}}
.benefit-card{{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.12);border-radius:8px;padding:24px;text-align:center}}
.benefit-num{{font-family:var(--font);font-size:42px;font-weight:900;color:#4ade80;line-height:1;margin-bottom:6px}}
.benefit-label{{font-size:14px;opacity:.85}}

/* ── CALC / CTA SECTION ── */
.cta-section{{background:linear-gradient(135deg, var(--green-dark), var(--green))}}
.cta-section .section-title{{color:#fff}}
.cta-flex{{display:flex;gap:48px;align-items:flex-start;flex-wrap:wrap}}
.cta-text{{flex:1;min-width:280px;color:rgba(255,255,255,.9)}}
.cta-text p{{margin-bottom:14px;font-size:15px}}
.cta-form{{flex:1;min-width:280px;background:rgba(255,255,255,.1);border-radius:8px;padding:28px;backdrop-filter:blur(8px)}}
.cta-form h3{{font-family:var(--font);color:#fff;font-size:18px;font-weight:700;margin-bottom:16px}}
.form-group{{margin-bottom:14px}}
.form-group input,.form-group select{{
  width:100%;padding:12px 14px;border-radius:4px;border:none;font-size:15px;font-family:var(--font2);background:#fff
}}
.form-submit{{width:100%;background:var(--orange);color:#fff;border:none;padding:14px;border-radius:4px;font-weight:800;font-size:15px;cursor:pointer;font-family:var(--font)}}
.form-submit:hover{{background:var(--orange2)}}

/* ── REVIEWS ── */
.reviews-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px}}
.review-card{{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,.05)}}
.review-stars{{color:#f59e0b;font-size:16px;margin-bottom:8px}}
.review-text{{font-size:14px;color:#444;margin-bottom:12px;font-style:italic;line-height:1.6}}
.review-author{{font-weight:700;font-size:14px;color:#1a1a1a}}
.review-date{{font-size:12px;color:#999}}
.avito-badge{{display:inline-flex;align-items:center;gap:6px;background:#00AAFF;color:#fff;font-size:12px;font-weight:700;padding:3px 10px;border-radius:10px;margin-bottom:8px}}

/* ── FAQ ── */
.faq-list{{max-width:760px}}
.faq-item{{border-bottom:1px solid #e5e7eb;overflow:hidden}}
.faq-q{{padding:16px 0;font-weight:700;font-size:15px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:#1a1a1a}}
.faq-q::after{{content:'+';font-size:20px;color:var(--green);font-weight:900;transition:.3s;flex-shrink:0}}
.faq-item input[type=checkbox]{{display:none}}
.faq-item input:checked ~ .faq-q::after{{content:'-'}}
.faq-a{{max-height:0;overflow:hidden;transition:.4s ease;font-size:14px;color:#555;line-height:1.7}}
.faq-item input:checked ~ .faq-a{{max-height:300px;padding-bottom:16px}}

/* ── CONTACTS ── */
.contacts-flex{{display:flex;gap:40px;flex-wrap:wrap}}
.contacts-info{{flex:1;min-width:260px}}
.contact-line{{display:flex;align-items:flex-start;gap:12px;margin-bottom:18px;font-size:15px}}
.contact-icon{{font-size:22px;flex-shrink:0;margin-top:1px}}
.contact-label{{font-size:12px;color:#999;text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px}}
.contact-val{{font-weight:600;color:#1a1a1a}}
.contact-val a{{color:var(--green);text-decoration:none}}
.map-placeholder{{flex:1.4;min-width:280px;height:340px;border-radius:8px;overflow:hidden;background:#e5e7eb;border:1px solid #ddd}}

/* ── STICKY BUTTONS ── */
.sticky-btns{{position:fixed;bottom:24px;right:20px;display:flex;flex-direction:column;gap:10px;z-index:999}}
.sticky-btn{{display:flex;align-items:center;justify-content:center;width:52px;height:52px;border-radius:50%;font-size:22px;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.25);transition:.2s}}
.sticky-btn:hover{{transform:scale(1.1)}}
.sticky-call{{background:var(--green)}}
.sticky-wa{{background:#25d366}}

/* ── FOOTER ── */
.footer{{background:var(--green-dark);color:rgba(255,255,255,.7);padding:32px 0;font-size:13px}}
.footer .wrap{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}}
.footer-logo img,.footer-logo svg{{height:36px;filter:brightness(0) invert(1) opacity(.8)}}
.footer-links a{{color:rgba(255,255,255,.6);text-decoration:none;margin-left:14px}}
.footer-links a:hover{{color:#fff}}

/* ── RESPONSIVE ── */
@media(max-width:768px){{
  .header-nav{{display:none}}
  .hero{{min-height:480px}}
  .features-strip .wrap{{justify-content:center}}
  .cta-flex{{flex-direction:column}}
  .contacts-flex{{flex-direction:column}}
  .map-placeholder{{height:250px}}
  .topbar-rating{{display:none}}
}}
</style>
</head>
<body>

<!-- TOPBAR -->
<div class="topbar">
  <div class="wrap">
    <div class="topbar-contacts">
      <span>📍 Калининград</span>
      <span>🕐 Работаем без выходных, с 8:00 до 22:00</span>
    </div>
    <div class="topbar-rating">
      <span class="stars">★★★★★</span>
      <span>4.9 на Авито</span>
      <span style="margin-left:8px">·</span>
      <a href="{AVITO_LINK}" target="_blank" style="margin-left:8px">Смотреть отзывы</a>
    </div>
  </div>
</div>

<!-- HEADER -->
<header class="header">
  <div class="wrap">
    <a class="header-logo" href="#">
      <img src="logo.svg" alt="{COMPANY}" width="180" height="50">
    </a>
    <nav><ul class="header-nav">
      <li><a href="#services">Услуги</a></li>
      <li><a href="#prices">Цены</a></li>
      <li><a href="#how">Как мы работаем</a></li>
      <li><a href="#reviews">Отзывы</a></li>
      <li><a href="#contacts">Контакты</a></li>
    </ul></nav>
    <div style="display:flex;align-items:center;gap:14px">
      <a class="header-phone" href="tel:{PHONE_CLEAN}">{PHONE}</a>
      <a class="header-callback btn-primary" href="tel:{PHONE_CLEAN}" style="font-size:14px;padding:10px 18px">Заказать</a>
    </div>
  </div>
</header>

<!-- HERO -->
<section class="hero">
  <div class="wrap">
    <div class="hero-badge">🚚 Грузоперевозки в Калининграде</div>
    <h1>Переезд и грузоперевозки<br><span>в день обращения</span></h1>
    <p class="hero-sub">Газель до 3 тонн, опытные грузчики, бережная упаковка.<br>Квартирные и офисные переезды без выходных.</p>
    <div class="hero-cta">
      <a class="btn-primary" href="tel:{PHONE_CLEAN}">📞 Позвонить сейчас</a>
      <a class="btn-outline" href="#prices">Узнать цены</a>
    </div>
    <div class="hero-trust">
      <div class="hero-trust-item">Работаем с 2018 года</div>
      <div class="hero-trust-item">Страховка груза</div>
      <div class="hero-trust-item">Без скрытых доплат</div>
      <div class="hero-trust-item">GPS-мониторинг</div>
    </div>
  </div>
</section>

<!-- FEATURES STRIP -->
<div class="features-strip">
  <div class="wrap">
    <div class="feat-item"><div class="feat-icon">🚚</div><div class="feat-value">3 т</div><div class="feat-label">грузоподъёмность</div></div>
    <div class="feat-item"><div class="feat-icon">⚡</div><div class="feat-value">2 ч</div><div class="feat-label">выезд после звонка</div></div>
    <div class="feat-item"><div class="feat-icon">⭐</div><div class="feat-value">4.9</div><div class="feat-label">рейтинг на Авито</div></div>
    <div class="feat-item"><div class="feat-icon">📦</div><div class="feat-value">500+</div><div class="feat-label">переездов выполнено</div></div>
    <div class="feat-item"><div class="feat-icon">🛡</div><div class="feat-value">100%</div><div class="feat-label">страховка груза</div></div>
  </div>
</div>

<!-- SERVICES -->
<section id="services">
  <div class="wrap">
    <h2 class="section-title center">Полный перечень услуг</h2>
    <p class="section-sub center">Грузоперевозки и переезды любой сложности по Калининграду и области</p>
    <div class="services-grid">
{SERVICES_HTML}
    </div>
  </div>
</section>

<!-- GALLERY (only if photos available) -->
{"<section><div class='wrap'><h2 class='section-title center'>Наши работы</h2><p class='section-sub center'>Фотографии реальных переездов</p><div class='gallery'>" + GALLERY_HTML + "</div></div></section>" if GALLERY_HTML else ""}

<!-- HOW IT WORKS -->
<section id="how" class="how-section">
  <div class="wrap">
    <h2 class="section-title center">Как это происходит</h2>
    <p class="section-sub center">5 простых шагов — и переезд позади</p>
    <div class="steps">
      <div class="step"><h4>Звонок или заявка</h4><p>Оставляете заявку — перезваниваем за 5 минут, уточняем детали и называем точную цену.</p></div>
      <div class="step"><h4>Выезд по адресу</h4><p>Бригада прибывает в удобное для вас время. Привозим упаковочные материалы.</p></div>
      <div class="step"><h4>Упаковка и разборка</h4><p>Разбираем и упаковываем мебель, хрупкие предметы — в пузырчатую плёнку.</p></div>
      <div class="step"><h4>Погрузка и перевозка</h4><p>Грузим аккуратно, фиксируем ремнями. Едем по оптимальному маршруту.</p></div>
      <div class="step"><h4>Разгрузка и сборка</h4><p>Расставляем мебель по плану, собираем, вывозим мусор и упаковку.</p></div>
    </div>
  </div>
</section>

<!-- BENEFITS -->
<section class="benefits-section">
  <div class="wrap">
    <h2 class="section-title center" style="margin-bottom:10px">С нами действительно выгодно</h2>
    <p class="section-sub center" style="color:rgba(255,255,255,.7)">Мы не навязываем лишних работ и не добавляем скрытых доплат</p>
    <div class="benefits-grid">
      <div class="benefit-card"><div class="benefit-num">500+</div><div class="benefit-label">Успешных переездов</div></div>
      <div class="benefit-card"><div class="benefit-num">5 лет</div><div class="benefit-label">Работаем в Калининграде</div></div>
      <div class="benefit-card"><div class="benefit-num">24/7</div><div class="benefit-label">Принимаем заявки</div></div>
      <div class="benefit-card"><div class="benefit-num">100%</div><div class="benefit-label">Страховка груза</div></div>
    </div>
  </div>
</section>

<!-- PRICES -->
<section id="prices">
  <div class="wrap">
    <h2 class="section-title">Рассчитайте стоимость переезда</h2>
    <p class="section-sub">Прозрачные цены без скрытых доплат — что называем, то и платите</p>
    <div style="overflow-x:auto">
    <table class="price-table">
      <thead><tr><th>Услуга</th><th>Стоимость</th><th>Заказать</th></tr></thead>
      <tbody>
{PRICES_HTML}
      </tbody>
    </table>
    </div>
    <p style="margin-top:14px;font-size:13px;color:#888">* Точная стоимость рассчитывается индивидуально. Позвоните — ответим за 5 минут.</p>
  </div>
</section>

<!-- CTA / CALLBACK -->
<section class="cta-section" id="callback">
  <div class="wrap">
    <div class="cta-flex">
      <div class="cta-text">
        <h2 class="section-title" style="color:#fff;margin-bottom:18px">Узнайте стоимость<br>вашего переезда</h2>
        <p>Оставьте заявку — перезвоним за 5 минут, ответим на все вопросы и рассчитаем точную стоимость.</p>
        <p>Работаем по всему Калининграду и области. Принимаем заявки до 22:00.</p>
        <div style="margin-top:24px;display:flex;flex-direction:column;gap:10px">
          <div class="hero-trust-item" style="color:rgba(255,255,255,.85)">Не навязываем лишние услуги</div>
          <div class="hero-trust-item" style="color:rgba(255,255,255,.85)">Цена не меняется после завершения работы</div>
          <div class="hero-trust-item" style="color:rgba(255,255,255,.85)">Оплата после выполнения</div>
        </div>
      </div>
      <div class="cta-form">
        <h3>Заявка на переезд</h3>
        <div class="form-group"><input type="text" placeholder="Ваше имя"></div>
        <div class="form-group"><input type="tel" placeholder="Телефон *" required></div>
        <div class="form-group">
          <select>
            <option value="">— Тип услуги —</option>
            <option>Квартирный переезд</option>
            <option>Офисный переезд</option>
            <option>Грузоперевозки / доставка</option>
            <option>Грузчики</option>
            <option>Вывоз мусора</option>
          </select>
        </div>
        <button class="form-submit" onclick="window.location='tel:{PHONE_CLEAN}'">📞 Позвонить сейчас</button>
        <p style="color:rgba(255,255,255,.6);font-size:12px;margin-top:10px;text-align:center">или звоните напрямую: <a href="tel:{PHONE_CLEAN}" style="color:#4ade80;font-weight:700">{PHONE}</a></p>
      </div>
    </div>
  </div>
</section>

<!-- REVIEWS -->
<section id="reviews">
  <div class="wrap">
    <h2 class="section-title center">Реальные отзывы на Авито</h2>
    <p class="section-sub center">Более 50 отзывов от клиентов — смотрите сами</p>
    <div class="reviews-grid">
      <div class="review-card">
        <div class="avito-badge">avito</div>
        <div class="review-stars">★★★★★</div>
        <p class="review-text">«Отличная компания! Переезжали из двушки, всё упаковали, привезли аккуратно. Ни одной царапины. Рекомендую!»</p>
        <div class="review-author">Марина К.</div>
        <div class="review-date">Февраль 2025</div>
      </div>
      <div class="review-card">
        <div class="avito-badge">avito</div>
        <div class="review-stars">★★★★★</div>
        <p class="review-text">«Заказывал Газель с грузчиками для офисного переезда. Приехали вовремя, всё сделали быстро. Цена вышла даже ниже, чем озвучили.»</p>
        <div class="review-author">Дмитрий В.</div>
        <div class="review-date">Январь 2025</div>
      </div>
      <div class="review-card">
        <div class="avito-badge">avito</div>
        <div class="review-stars">★★★★★</div>
        <p class="review-text">«Молодцы! Перевезли мебель из Калининграда в Гурьевск. Всё целое, работали профессионально. Буду обращаться ещё.»</p>
        <div class="review-author">Ольга Т.</div>
        <div class="review-date">Декабрь 2024</div>
      </div>
    </div>
    <div style="text-align:center;margin-top:28px">
      <a href="{AVITO_LINK}" target="_blank" class="btn-primary" style="background:var(--green)">Все отзывы на Авито →</a>
    </div>
  </div>
</section>

<!-- FAQ -->
<section style="background:var(--light)">
  <div class="wrap">
    <h2 class="section-title">Ответы на часто задаваемые вопросы</h2>
    <div class="faq-list">
      <div class="faq-item"><input type="checkbox" id="f1"><label class="faq-q" for="f1">Как быстро вы приедете?</label><div class="faq-a">Обычно выезжаем в течение 1–2 часов после звонка. В некоторых случаях — в день обращения. Если нужен срочный выезд, скажите при заказе.</div></div>
      <div class="faq-item"><input type="checkbox" id="f2"><label class="faq-q" for="f2">Какова грузоподъёмность вашей машины?</label><div class="faq-a">Используем Газель: грузоподъёмность до 3 тонн, объём кузова 10–12 м³. Подходит для переезда 1–3-комнатных квартир.</div></div>
      <div class="faq-item"><input type="checkbox" id="f3"><label class="faq-q" for="f3">Выезжаете за пределы Калининграда?</label><div class="faq-a">Да, работаем по всей Калининградской области. Доставляем грузы в Гурьевск, Зеленоградск, Советск, Черняховск и другие города.</div></div>
      <div class="faq-item"><input type="checkbox" id="f4"><label class="faq-q" for="f4">Упаковка включена в стоимость?</label><div class="faq-a">Основная упаковка стрейч-плёнкой входит в стоимость. Картонные коробки и пузырчатая плёнка — по желанию (уточните цену при звонке).</div></div>
      <div class="faq-item"><input type="checkbox" id="f5"><label class="faq-q" for="f5">Изменится ли цена в процессе работы?</label><div class="faq-a">Нет. Мы называем финальную цену до начала работы. Доплат за подъём на этаж, длинные дорожки или другие «неожиданности» не будет.</div></div>
      <div class="faq-item"><input type="checkbox" id="f6"><label class="faq-q" for="f6">Как вы работаете с хрупкими предметами?</label><div class="faq-a">Упаковываем в пузырчатую плёнку и поролон, перевозим в специальных ящиках. Хрупкий груз застрахован.</div></div>
    </div>
  </div>
</section>

<!-- CONTACTS -->
<section id="contacts">
  <div class="wrap">
    <h2 class="section-title">Контакты {COMPANY}</h2>
    <div class="contacts-flex">
      <div class="contacts-info">
        <div class="contact-line">
          <div class="contact-icon">📞</div>
          <div>
            <div class="contact-label">Телефон</div>
            <div class="contact-val"><a href="tel:{PHONE_CLEAN}">{PHONE}</a></div>
          </div>
        </div>
        <div class="contact-line">
          <div class="contact-icon">📍</div>
          <div>
            <div class="contact-label">Город</div>
            <div class="contact-val">{CITY}</div>
          </div>
        </div>
        <div class="contact-line">
          <div class="contact-icon">🕐</div>
          <div>
            <div class="contact-label">Время работы</div>
            <div class="contact-val">Ежедневно, 8:00 – 22:00</div>
          </div>
        </div>
        <div class="contact-line">
          <div class="contact-icon">🌐</div>
          <div>
            <div class="contact-label">Объявление на Авито</div>
            <div class="contact-val"><a href="{AVITO_LINK}" target="_blank">Смотреть на Авито</a></div>
          </div>
        </div>
        <div style="margin-top:24px;display:flex;gap:12px;flex-wrap:wrap">
          <a href="tel:{PHONE_CLEAN}" class="btn-primary">📞 Позвонить</a>
          <a href="https://wa.me/{PHONE_CLEAN.replace('+','')}" target="_blank" class="btn-primary" style="background:#25d366">WhatsApp</a>
        </div>
      </div>
      <div class="map-placeholder">
        <iframe 
          src="https://yandex.ru/map-widget/v1/?ll=20.511742%2C54.710162&z=12&pt=20.511742,54.710162,pm2rdm&text=%D0%9A%D0%B0%D0%BB%D0%B8%D0%BD%D0%B8%D0%BD%D0%B3%D1%80%D0%B0%D0%B4"
          width="100%" height="100%" frameborder="0" allowfullscreen style="border:0"></iframe>
      </div>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer class="footer">
  <div class="wrap">
    <div class="footer-logo"><img src="logo.svg" alt="{COMPANY}"></div>
    <div>{COMPANY} · {CITY} · Грузоперевозки</div>
    <div class="footer-links">
      <a href="tel:{PHONE_CLEAN}">{PHONE}</a>
      <a href="{AVITO_LINK}" target="_blank">Авито</a>
    </div>
  </div>
</footer>

<!-- STICKY BUTTONS -->
<div class="sticky-btns">
  <a class="sticky-btn sticky-call" href="tel:{PHONE_CLEAN}" title="Позвонить">📞</a>
  <a class="sticky-btn sticky-wa" href="https://wa.me/{PHONE_CLEAN.replace('+','')}" target="_blank" title="WhatsApp">💬</a>
</div>

</body>
</html>"""

# ─── Save ────────────────────────────────────────────────────────────────

out_file = OUT_DIR / "index.html"
out_file.write_text(HTML, encoding="utf-8")
print(f"\n{'='*60}")
print(f"  Готово! {out_file}")
print(f"  Строк: {len(HTML.splitlines())}")
print(f"  Размер: {out_file.stat().st_size // 1024} КБ")
print(f"  Фото скачано: {len(photos)}")
print(f"  Логотип: {logo_file}")
print(f"{'='*60}")
