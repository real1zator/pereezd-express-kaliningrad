#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final build: ТК Переезд Экспресс - FIT SERVICE style"""
import sys, json, re, pathlib
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = pathlib.Path(r"D:\PROJCT\САЙТ\Сайты-По-Темам\Переезд-1")
DATA = json.loads((OUT_DIR / "_avito_data.json").read_text(encoding='utf-8'))

COMPANY = "ТК Переезд Экспресс"
TAGLINE = "Переезд без стресса"
PHONE = "+7 (900) 000-00-00"   # UPDATE after getting from Avito listing
PHONE_CLEAN = PHONE.replace("+", "").replace(" ","").replace("(","").replace(")","").replace("-","")
AVITO_URL = DATA.get("url", "https://www.avito.ru/kaliningrad/predlozheniya_uslug/pereezdy_gruzoperevozki_dostavki_do_3_tonn_7275388730")
CITY = "Калининград"

HERO_IMG = "avito_1.jpg"   # First real Avito photo
PHOTOS = [f"photo_{i}.webp" for i in range(1, 8)]

# ─── Logo SVG (green truck) ────────────────────────────────────────────────
LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 70" width="240" height="70">
  <defs>
    <linearGradient id="gb" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1a5c2e"/>
      <stop offset="100%" stop-color="#2d7a47"/>
    </linearGradient>
  </defs>
  <rect width="240" height="70" rx="8" fill="url(#gb)"/>
  <!-- Truck body -->
  <g transform="translate(10,12)">
    <rect x="26" y="8" width="36" height="26" rx="3" fill="none" stroke="white" stroke-width="2.2"/>
    <rect x="2" y="16" width="26" height="18" rx="2" fill="none" stroke="white" stroke-width="2.2"/>
    <rect x="5" y="19" width="15" height="10" rx="1.5" fill="rgba(255,255,255,0.25)" stroke="white" stroke-width="1.2"/>
    <circle cx="12" cy="40" r="6" fill="none" stroke="white" stroke-width="2.2"/>
    <circle cx="12" cy="40" r="2.5" fill="white"/>
    <circle cx="52" cy="40" r="6" fill="none" stroke="white" stroke-width="2.2"/>
    <circle cx="52" cy="40" r="2.5" fill="white"/>
    <!-- Speed lines -->
    <line x1="-2" y1="22" x2="-12" y2="22" stroke="white" stroke-width="2" stroke-linecap="round"/>
    <line x1="-2" y1="28" x2="-15" y2="28" stroke="white" stroke-width="2" stroke-linecap="round"/>
    <line x1="-2" y1="34" x2="-10" y2="34" stroke="white" stroke-width="2" stroke-linecap="round"/>
  </g>
  <!-- Text block -->
  <text x="90" y="24" font-family="'Arial Black',Arial,sans-serif" font-weight="900" font-size="15" fill="white" letter-spacing="0.5">ПЕРЕЕЗД</text>
  <text x="90" y="42" font-family="'Arial Black',Arial,sans-serif" font-weight="900" font-size="15" fill="white" letter-spacing="0.5">ЭКСПРЕСС</text>
  <text x="90" y="58" font-family="Arial,sans-serif" font-size="8.5" fill="rgba(200,240,215,0.9)" letter-spacing="0.3">ТРАНСПОРТНАЯ КОМПАНИЯ</text>
</svg>"""

(OUT_DIR / "logo.svg").write_text(LOGO_SVG, encoding='utf-8')

# ─── Services ─────────────────────────────────────────────────────────────
SERVICES = [
    {
        "icon": "🏠",
        "title": "Квартирный переезд",
        "desc": "Перевезём квартиру любой площади. Разборка, упаковка, перевозка, сборка. Бережно и быстро.",
        "price": "от 4 800 ₽",
        "photo": PHOTOS[0] if len(PHOTOS) > 0 else None,
    },
    {
        "icon": "🏢",
        "title": "Офисный переезд",
        "desc": "Переезд офиса без остановки бизнеса. Работаем вечером и в выходные.",
        "price": "от 4 800 ₽",
        "photo": PHOTOS[1] if len(PHOTOS) > 1 else None,
    },
    {
        "icon": "🚚",
        "title": "Газель + 2 грузчика",
        "desc": "Фиксированная ставка: газель + 2 грузчика. Включает подъём/спуск и упаковку.",
        "price": "2 400 ₽/час",
        "photo": PHOTOS[2] if len(PHOTOS) > 2 else None,
    },
    {
        "icon": "📦",
        "title": "Перевозка мебели",
        "desc": "Разберём, упакуем стрейч-плёнкой, перевезём и соберём. Без царапин и сколов.",
        "price": "от 2 000 ₽",
        "photo": PHOTOS[3] if len(PHOTOS) > 3 else None,
    },
    {
        "icon": "💪",
        "title": "Услуги грузчиков",
        "desc": "Профессиональные грузчики на час. Подъём, спуск, перестановка, разгрузка.",
        "price": "от 1 200 ₽/час",
        "photo": PHOTOS[4] if len(PHOTOS) > 4 else None,
    },
    {
        "icon": "🗑",
        "title": "Вывоз мусора",
        "desc": "Вывоз строительного мусора, старой мебели, бытовой техники. Газель до 3 т.",
        "price": "от 2 400 ₽",
        "photo": PHOTOS[5] if len(PHOTOS) > 5 else None,
    },
]

PRICES_DATA = [
    ("Газель + 2 грузчика (минум 2 ч)", "2 400 ₽/час"),
    ("Газель + 3 грузчика", "3 000 ₽/час"),
    ("Только газель (без грузчиков)", "1 400 ₽/час"),
    ("Квартирный переезд 1-комн.", "от 4 800 ₽"),
    ("Квартирный переезд 2-комн.", "от 7 200 ₽"),
    ("Квартирный переезд 3-комн.", "от 9 600 ₽"),
    ("Офисный переезд (до 5 рабочих мест)", "от 4 800 ₽"),
    ("Вывоз мусора (газель)", "от 2 400 ₽"),
    ("Доп. грузчик", "+ 600 ₽/час"),
]

# ─── HTML Build ────────────────────────────────────────────────────────────

# Service cards
def svc_card(s):
    photo_html = ""
    if s.get("photo"):
        photo_html = f'<div class="svc-photo" style="background-image:url({s["photo"]})"></div>'
    else:
        photo_html = f'<div class="svc-photo svc-photo-empty"></div>'
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

SERVICES_HTML = "".join(svc_card(s) for s in SERVICES)

# Price table rows
PRICES_HTML = "".join(f"""<tr>
  <td>{name}</td>
  <td class="price-val">{price}</td>
  <td><a href="tel:{PHONE_CLEAN}" class="price-btn">Заказать</a></td>
</tr>""" for name, price in PRICES_DATA)

# Gallery
GALLERY_HTML = "".join(
    f'<div class="gallery-item" style="background-image:url({p})"></div>\n'
    for p in PHOTOS[:6]
)

HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{COMPANY} — Переезды и грузоперевозки в Калининграде. В день обращения!</title>
<meta name="description" content="Квартирные и офисные переезды, грузоперевозки в Калининграде. Газель до 3 тонн. Грузчики. 2400₽/час без скрытых доплат. Работаем 24/7.">
<meta property="og:title" content="{COMPANY} — Переезды в Калининграде">
<meta property="og:description" content="Квартирные переезды от 4800₽. Газель + 2 грузчика от 2400₽/час.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --green:#1a5c2e;
  --green2:#2d7a47;
  --green3:#0f3a1e;
  --orange:#e85d04;
  --orange2:#f48c06;
  --gray:#4a4a4a;
  --light:#f4f6f0;
  --white:#fff;
  --fn:'Montserrat',sans-serif;
  --fn2:'Open Sans',sans-serif;
}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--fn2);color:var(--gray);line-height:1.6;background:#fff;overflow-x:hidden}}

/* ── TOPBAR ── */
.topbar{{background:var(--green3);color:rgba(255,255,255,.78);font-size:13px;padding:7px 0}}
.topbar .w{{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}}
.topbar a{{color:inherit;text-decoration:none;transition:.15s}}
.topbar a:hover{{color:#fff}}
.topbar-right{{display:flex;align-items:center;gap:18px}}
.stars{{color:#f59e0b;letter-spacing:-1px}}

/* ── HEADER ── */
.hdr{{background:#fff;box-shadow:0 2px 14px rgba(0,0,0,.11);position:sticky;top:0;z-index:100}}
.hdr .w{{display:flex;justify-content:space-between;align-items:center;padding:10px 20px;gap:16px}}
.hdr-logo{{text-decoration:none}}
.hdr-logo img,.hdr-logo svg{{height:54px;width:auto;display:block}}
.hdr-nav{{display:flex;gap:22px;list-style:none}}
.hdr-nav a{{color:var(--gray);text-decoration:none;font-weight:600;font-size:14px;transition:.2s;font-family:var(--fn)}}
.hdr-nav a:hover{{color:var(--green)}}
.hdr-right{{display:flex;align-items:center;gap:14px}}
.hdr-phone{{font-size:19px;font-weight:800;color:var(--green);text-decoration:none;font-family:var(--fn);white-space:nowrap}}
.btn-call{{background:var(--orange);color:#fff;padding:10px 22px;border-radius:5px;font-weight:700;font-size:14px;text-decoration:none;font-family:var(--fn);transition:.18s;white-space:nowrap}}
.btn-call:hover{{background:var(--orange2);transform:translateY(-1px)}}

/* ── HERO ── */
.hero{{
  position:relative;
  min-height:600px;
  display:flex;
  align-items:center;
  background-color:var(--green3);
  background-image:url('{HERO_IMG}');
  background-size:cover;
  background-position:center 30%;
  overflow:hidden;
}}
.hero::before{{
  content:'';
  position:absolute;inset:0;
  background:linear-gradient(105deg,rgba(8,28,15,.90) 0%,rgba(8,28,15,.68) 45%,rgba(8,28,15,.18) 100%);
}}
.hero .w{{position:relative;z-index:2;padding:70px 20px}}
.hero-badge{{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.28);color:#fff;font-size:13px;font-weight:600;padding:5px 14px;border-radius:20px;margin-bottom:20px}}
.hero h1{{font-family:var(--fn);font-size:clamp(28px,5vw,52px);font-weight:900;color:#fff;line-height:1.12;max-width:700px;margin-bottom:14px}}
.hero h1 em{{color:#f59e0b;font-style:normal}}
.hero-sub{{color:rgba(255,255,255,.88);font-size:clamp(14px,2vw,18px);max-width:540px;margin-bottom:28px;line-height:1.55}}
.hero-cta{{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:34px}}
.btn-hero-primary{{background:var(--orange);color:#fff;padding:16px 34px;border-radius:5px;font-weight:800;font-size:16px;text-decoration:none;font-family:var(--fn);transition:.2s;display:inline-flex;align-items:center;gap:8px}}
.btn-hero-primary:hover{{background:var(--orange2);transform:translateY(-2px);box-shadow:0 6px 20px rgba(232,93,4,.4)}}
.btn-hero-outline{{border:2px solid rgba(255,255,255,.55);color:#fff;padding:14px 28px;border-radius:5px;font-weight:700;font-size:15px;text-decoration:none;font-family:var(--fn);transition:.18s}}
.btn-hero-outline:hover{{background:rgba(255,255,255,.1);border-color:#fff}}
.hero-trust{{display:flex;gap:20px;flex-wrap:wrap}}
.trust-item{{color:rgba(255,255,255,.9);font-size:13px;display:flex;align-items:center;gap:6px;font-weight:600}}
.trust-item::before{{content:'✓';color:#4ade80;font-weight:800;font-size:14px}}

/* ── PRICE HERO BADGE ── */
.hero-price-badge{{
  position:absolute;right:48px;top:50%;transform:translateY(-50%);
  background:rgba(255,255,255,.95);border-radius:12px;padding:22px 24px;
  text-align:center;box-shadow:0 8px 28px rgba(0,0,0,.25);
  backdrop-filter:blur(6px);min-width:180px;
}}
.hero-price-badge .price-big{{font-family:var(--fn);font-size:32px;font-weight:900;color:var(--green);line-height:1}}
.hero-price-badge .price-desc{{font-size:12px;color:#666;margin-top:4px;margin-bottom:10px}}
.hero-price-badge a{{display:block;background:var(--orange);color:#fff;padding:9px 16px;border-radius:6px;font-weight:700;font-size:13px;text-decoration:none;font-family:var(--fn)}}

/* ── STRIP ── */
.strip{{background:var(--green);padding:22px 0}}
.strip .w{{display:flex;justify-content:space-around;flex-wrap:wrap;gap:12px}}
.strip-item{{color:#fff;display:flex;flex-direction:column;align-items:center;gap:4px;min-width:130px}}
.strip-icon{{font-size:26px}}
.strip-val{{font-size:20px;font-weight:900;font-family:var(--fn);line-height:1}}
.strip-lbl{{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.6px;opacity:.85}}

/* ── SECTIONS ── */
section{{padding:64px 0}}
.w{{max-width:1200px;margin:0 auto;padding:0 20px}}
.sec-title{{font-family:var(--fn);font-size:clamp(22px,3.5vw,34px);font-weight:800;color:#1a1a1a;margin-bottom:10px}}
.sec-sub{{color:#666;font-size:15px;margin-bottom:36px;max-width:620px}}
.center{{text-align:center}}
.center .sec-sub{{margin-left:auto;margin-right:auto}}

/* ── SERVICE CARDS ── */
.services-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:24px}}
.svc-card{{background:#fff;border:1px solid #e8eee9;border-radius:10px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.06);transition:.3s}}
.svc-card:hover{{transform:translateY(-5px);box-shadow:0 10px 28px rgba(0,0,0,.12)}}
.svc-photo{{height:210px;background-size:cover;background-position:center}}
.svc-photo-empty{{background:linear-gradient(135deg,var(--green3),var(--green))}}
.svc-body{{padding:22px}}
.svc-icon{{font-size:28px;margin-bottom:8px}}
.svc-body h3{{font-family:var(--fn);font-size:18px;font-weight:800;color:#1a1a1a;margin-bottom:8px}}
.svc-body p{{font-size:14px;color:#555;margin-bottom:14px;line-height:1.65}}
.svc-price{{font-size:22px;font-weight:900;color:var(--green);font-family:var(--fn);margin-bottom:14px}}
.svc-btn{{display:block;text-align:center;background:var(--green);color:#fff;padding:11px;border-radius:5px;font-weight:700;font-size:14px;text-decoration:none;font-family:var(--fn);transition:.15s}}
.svc-btn:hover{{background:var(--green2)}}

/* ── HOW ── */
.how-section{{background:var(--light)}}
.steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px;counter-reset:step}}
.step{{background:#fff;border-radius:10px;padding:28px 22px;box-shadow:0 2px 10px rgba(0,0,0,.05);position:relative;counter-increment:step}}
.step::before{{
  content:counter(step);
  position:absolute;top:-14px;left:22px;
  background:var(--orange);color:#fff;
  font-family:var(--fn);font-weight:900;font-size:14px;
  padding:4px 14px;border-radius:12px;min-width:30px;text-align:center;
}}
.step h4{{font-family:var(--fn);font-size:16px;font-weight:800;margin:12px 0 8px;color:#1a1a1a}}
.step p{{font-size:14px;color:#666;line-height:1.6}}

/* ── GALLERY ── */
.gallery{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}}
.gallery-item{{height:230px;background-size:cover;background-position:center;border-radius:10px;background-color:#c8d8cc}}

/* ── BENEFITS DARK ── */
.benefits-sec{{background:var(--green3)}}
.benefits-sec .sec-title{{color:#fff}}
.benefits-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:20px}}
.benefit-card{{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.14);border-radius:10px;padding:26px 22px;text-align:center}}
.benefit-num{{font-family:var(--fn);font-size:44px;font-weight:900;color:#4ade80;line-height:1;margin-bottom:6px}}
.benefit-lbl{{font-size:14px;color:rgba(255,255,255,.85)}}

/* ── PRICE TABLE ── */
.price-table{{width:100%;border-collapse:collapse;font-size:15px;margin-top:24px}}
.price-table th{{background:var(--green);color:#fff;padding:14px 18px;text-align:left;font-family:var(--fn);font-weight:700;font-size:14px}}
.price-table td{{padding:13px 18px;border-bottom:1px solid #e5ece8}}
.price-table tr:hover td{{background:#f0fdf4}}
.price-val{{font-weight:800;color:var(--green);font-size:16px;white-space:nowrap}}
.price-btn{{background:var(--orange);color:#fff;padding:7px 16px;border-radius:5px;font-weight:700;font-size:13px;text-decoration:none;white-space:nowrap;display:inline-block}}
.price-btn:hover{{background:var(--orange2)}}

/* ── CTA SECTION ── */
.cta-sec{{background:linear-gradient(130deg,var(--green3),var(--green))}}
.cta-sec .sec-title{{color:#fff}}
.cta-flex{{display:flex;gap:50px;align-items:flex-start;flex-wrap:wrap}}
.cta-left{{flex:1;min-width:280px;color:rgba(255,255,255,.9)}}
.cta-left p{{margin-bottom:14px;font-size:15px;line-height:1.6}}
.trust-list{{list-style:none;margin-top:20px}}
.trust-list li{{padding:6px 0;font-size:14px;color:rgba(255,255,255,.87);display:flex;align-items:center;gap:8px}}
.trust-list li::before{{content:'✓';color:#4ade80;font-weight:800;font-size:15px}}
.cta-form{{flex:0 0 340px;background:rgba(255,255,255,.1);border-radius:10px;padding:28px;backdrop-filter:blur(8px)}}
.cta-form h3{{font-family:var(--fn);color:#fff;font-size:18px;font-weight:700;margin-bottom:16px}}
.fg{{margin-bottom:14px}}
.fg input,.fg select{{width:100%;padding:12px 14px;border-radius:5px;border:none;font-size:15px;font-family:var(--fn2)}}
.fg select{{color:#555}}
.cta-submit{{width:100%;background:var(--orange);color:#fff;border:none;padding:15px;border-radius:5px;font-weight:800;font-size:15px;cursor:pointer;font-family:var(--fn)}}
.cta-submit:hover{{background:var(--orange2)}}

/* ── REVIEWS ── */
.reviews-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px}}
.rev-card{{background:#fff;border:1px solid #e5ece8;border-radius:10px;padding:22px;box-shadow:0 2px 10px rgba(0,0,0,.05)}}
.rev-badge{{display:inline-flex;align-items:center;gap:5px;background:#0d76bd;color:#fff;font-size:12px;font-weight:700;padding:3px 10px;border-radius:10px;margin-bottom:8px}}
.rev-stars{{color:#f59e0b;font-size:15px;margin-bottom:10px}}
.rev-text{{font-size:14px;color:#444;font-style:italic;margin-bottom:12px;line-height:1.65}}
.rev-author{{font-weight:700;font-size:14px;color:#1a1a1a}}
.rev-date{{font-size:12px;color:#999}}

/* ── FAQ ── */
.faq-list{{max-width:780px}}
.faq-item{{border-bottom:1px solid #e5ece8}}
.faq-item input[type=checkbox]{{display:none}}
.faq-q{{padding:16px 0;font-weight:700;font-size:15px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:#1a1a1a;user-select:none}}
.faq-q::after{{content:'+';font-size:20px;color:var(--green);font-weight:900;flex-shrink:0;transition:.3s}}
.faq-item input:checked ~ .faq-q::after{{content:'−'}}
.faq-a{{max-height:0;overflow:hidden;transition:.35s ease;font-size:14px;color:#555;line-height:1.7}}
.faq-item input:checked ~ .faq-a{{max-height:300px;padding-bottom:16px}}

/* ── CONTACTS ── */
.contacts-flex{{display:flex;gap:40px;flex-wrap:wrap}}
.contacts-info{{flex:1;min-width:260px}}
.cline{{display:flex;gap:14px;margin-bottom:20px;align-items:flex-start}}
.cline-icon{{font-size:22px;flex-shrink:0;margin-top:2px}}
.cline-lbl{{font-size:11px;color:#999;text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px}}
.cline-val{{font-weight:600;color:#1a1a1a}}
.cline-val a{{color:var(--green);text-decoration:none;font-size:18px;font-weight:800}}
.map-frame{{flex:1.4;min-width:280px;height:360px;border-radius:10px;overflow:hidden;border:1px solid #ddd}}

/* ── STICKY ── */
.sticky{{position:fixed;bottom:24px;right:20px;display:flex;flex-direction:column;gap:10px;z-index:999}}
.sticky-btn{{display:flex;align-items:center;justify-content:center;width:54px;height:54px;border-radius:50%;font-size:22px;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.25);transition:.2s}}
.sticky-btn:hover{{transform:scale(1.12)}}
.sticky-call{{background:var(--green);color:white}}
.sticky-wa{{background:#25d366;color:white}}

/* ── FOOTER ── */
footer{{background:var(--green3);color:rgba(255,255,255,.68);padding:30px 0;font-size:13px}}
footer .w{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px}}
footer .f-logo{{display:flex;align-items:center;gap:14px}}
footer .f-logo img{{height:36px;filter:brightness(0) invert(1);opacity:.75}}
footer a{{color:rgba(255,255,255,.6);text-decoration:none;margin-left:16px}}
footer a:hover{{color:#fff}}

/* ── RESPONSIVE ── */
@media(max-width:900px){{
  .hdr-nav,.hero-price-badge{{display:none}}
  .hero{{min-height:500px}}
  .cta-flex{{flex-direction:column}}
  .cta-form{{flex:1;min-width:unset;width:100%}}
  .contacts-flex{{flex-direction:column}}
  .map-frame{{height:260px}}
}}
@media(max-width:600px){{
  .strip .w{{gap:8px}}
  .strip-item{{min-width:90px}}
}}
</style>
</head>
<body>

<!-- TOPBAR -->
<div class="topbar">
  <div class="w">
    <div style="display:flex;gap:20px;align-items:center;flex-wrap:wrap">
      <span>📍 {CITY}</span>
      <span>⏰ Работаем 24/7 — подача авто за 30 мин</span>
    </div>
    <div class="topbar-right">
      <span class="stars">★★★★★</span>
      <span>4.9 на Авито</span>
      <a href="{AVITO_URL}" target="_blank" style="margin-left:10px">Отзывы</a>
    </div>
  </div>
</div>

<!-- HEADER -->
<header class="hdr">
  <div class="w">
    <a class="hdr-logo" href="#">
      <img src="logo.svg" alt="{COMPANY}" width="200" height="54">
    </a>
    <nav><ul class="hdr-nav">
      <li><a href="#services">Услуги</a></li>
      <li><a href="#prices">Цены</a></li>
      <li><a href="#how">Как работаем</a></li>
      <li><a href="#reviews">Отзывы</a></li>
      <li><a href="#contacts">Контакты</a></li>
    </ul></nav>
    <div class="hdr-right">
      <a class="hdr-phone" href="tel:{PHONE_CLEAN}">{PHONE}</a>
      <a class="btn-call" href="tel:{PHONE_CLEAN}">Заказать</a>
    </div>
  </div>
</header>

<!-- HERO -->
<section class="hero">
  <div class="w">
    <div class="hero-badge">🚚 {COMPANY}</div>
    <h1>Переезд без стресса —<br><em>газель с грузчиками</em><br>от 2400 ₽/час</h1>
    <p class="hero-sub">Квартирные, офисные переезды и грузоперевозки по Калининграду и области.<br>Фиксированная цена без скрытых платежей.</p>
    <div class="hero-cta">
      <a class="btn-hero-primary" href="tel:{PHONE_CLEAN}">📞 Позвонить сейчас</a>
      <a class="btn-hero-outline" href="#prices">Посмотреть цены</a>
    </div>
    <div class="hero-trust">
      <div class="trust-item">Работаем 24/7</div>
      <div class="trust-item">Страховка груза</div>
      <div class="trust-item">Без скрытых доплат</div>
      <div class="trust-item">Подача за 30 минут</div>
    </div>
  </div>
  <div class="hero-price-badge">
    <div class="price-big">2 400 ₽</div>
    <div class="price-desc">газель + 2 грузчика / час</div>
    <a href="tel:{PHONE_CLEAN}">Рассчитать стоимость</a>
  </div>
</section>

<!-- STRIP -->
<div class="strip">
  <div class="w">
    <div class="strip-item"><div class="strip-icon">🚚</div><div class="strip-val">3 т</div><div class="strip-lbl">грузоподъёмность</div></div>
    <div class="strip-item"><div class="strip-icon">⚡</div><div class="strip-val">30 мин</div><div class="strip-lbl">подача авто</div></div>
    <div class="strip-item"><div class="strip-icon">⭐</div><div class="strip-val">4.9</div><div class="strip-lbl">рейтинг Авито</div></div>
    <div class="strip-item"><div class="strip-icon">📦</div><div class="strip-val">500+</div><div class="strip-lbl">переездов</div></div>
    <div class="strip-item"><div class="strip-icon">🛡</div><div class="strip-val">100%</div><div class="strip-lbl">страховка груза</div></div>
    <div class="strip-item"><div class="strip-icon">📋</div><div class="strip-val">Договор</div><div class="strip-lbl">для юридических лиц</div></div>
  </div>
</div>

<!-- SERVICES -->
<section id="services">
  <div class="w">
    <h2 class="sec-title center">Полный перечень услуг</h2>
    <p class="sec-sub center">Переезды любой сложности по городу и области. Фиксированная цена без сюрпризов.</p>
    <div class="services-grid">
      {SERVICES_HTML}
    </div>
  </div>
</section>

<!-- GALLERY -->
<section style="padding:48px 0;background:var(--light)">
  <div class="w">
    <h2 class="sec-title center">Фотографии наших работ</h2>
    <p class="sec-sub center">Реальные переезды наших клиентов</p>
    <div class="gallery">
      {GALLERY_HTML}
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section id="how">
  <div class="w">
    <h2 class="sec-title center">Как это происходит</h2>
    <p class="sec-sub center">5 шагов — и переезд позади</p>
    <div class="steps">
      <div class="step"><h4>Звоните или пишите</h4><p>Перезваниваем за 2 минуты, уточняем список вещей и адреса, называем точную цену.</p></div>
      <div class="step"><h4>Приезжаем по адресу</h4><p>Бригада прибывает в удобное время. Привозим упаковочные материалы.</p></div>
      <div class="step"><h4>Разборка и упаковка</h4><p>Разбираем мебель, упаковываем хрупкое в пузырчатую плёнку, фиксируем ремнями.</p></div>
      <div class="step"><h4>Перевозка</h4><p>Аккуратно грузим, едем по оптимальному маршруту с GPS-контролем.</p></div>
      <div class="step"><h4>Разгрузка и сборка</h4><p>Расставляем мебель по плану, собираем, вывозим упаковку. Оплата после!</p></div>
    </div>
  </div>
</section>

<!-- BENEFITS -->
<section class="benefits-sec">
  <div class="w">
    <h2 class="sec-title center" style="margin-bottom:10px">Мы не навязываем лишних работ</h2>
    <p class="sec-sub center" style="color:rgba(255,255,255,.7);margin-bottom:36px">Цена называется сразу и не меняется по ходу работы</p>
    <div class="benefits-grid">
      <div class="benefit-card"><div class="benefit-num">500+</div><div class="benefit-lbl">Успешных переездов</div></div>
      <div class="benefit-card"><div class="benefit-num">5 лет</div><div class="benefit-lbl">Работаем в Калининграде</div></div>
      <div class="benefit-card"><div class="benefit-num">30 мин</div><div class="benefit-lbl">Подача авто после звонка</div></div>
      <div class="benefit-card"><div class="benefit-num">24/7</div><div class="benefit-lbl">Принимаем заявки</div></div>
    </div>
  </div>
</section>

<!-- PRICES -->
<section id="prices">
  <div class="w">
    <h2 class="sec-title">Рассчитайте стоимость переезда</h2>
    <p class="sec-sub">Фиксированные тарифы без скрытых доплат. Минимальный заказ — 2 часа.</p>
    <div style="overflow-x:auto">
    <table class="price-table">
      <thead><tr><th style="width:55%">Услуга</th><th>Стоимость</th><th>Заказать</th></tr></thead>
      <tbody>{PRICES_HTML}</tbody>
    </table>
    </div>
    <p style="margin-top:14px;font-size:13px;color:#888">* В стоимость газели + 2 грузчика включены: подъём/спуск, разборка/сборка мебели, упаковка. Никаких доплат сверху.</p>
  </div>
</section>

<!-- CTA / CALLBACK -->
<section class="cta-sec" id="callback">
  <div class="w">
    <div class="cta-flex">
      <div class="cta-left">
        <h2 class="sec-title" style="color:#fff;margin-bottom:18px">Узнайте стоимость<br>вашего переезда</h2>
        <p>Оставьте заявку — перезвоним за 2 минуты, ответим на все вопросы и организуем переезд под ключ.</p>
        <p>Работаем круглосуточно по Калининграду и всей Калининградской области.</p>
        <ul class="trust-list">
          <li>Фиксированная цена, которая не меняется</li>
          <li>Оплата после выполнения работы</li>
          <li>Чистые машины с креплениями и стрейч-плёнкой</li>
          <li>Договор и чеки для юридических лиц</li>
          <li>GPL-мониторинг на всём маршруте</li>
        </ul>
      </div>
      <div class="cta-form">
        <h3>Заявка на переезд</h3>
        <div class="fg"><input type="text" placeholder="Ваше имя"></div>
        <div class="fg"><input type="tel" placeholder="Телефон *" required></div>
        <div class="fg">
          <select>
            <option>— Тип услуги —</option>
            <option>Квартирный переезд</option>
            <option>Офисный переезд</option>
            <option>Газель + грузчики (почасово)</option>
            <option>Перевозка мебели</option>
            <option>Вывоз мусора</option>
          </select>
        </div>
        <button class="cta-submit" onclick="window.location='tel:{PHONE_CLEAN}'">📞 Позвонить сейчас</button>
        <p style="color:rgba(255,255,255,.55);font-size:12px;margin-top:10px;text-align:center">
          Или звоните напрямую: <a href="tel:{PHONE_CLEAN}" style="color:#4ade80;font-weight:700">{PHONE}</a>
        </p>
      </div>
    </div>
  </div>
</section>

<!-- REVIEWS -->
<section id="reviews">
  <div class="w">
    <h2 class="sec-title center">Реальные отзывы на Авито</h2>
    <p class="sec-sub center">Более 50 отзывов клиентов — смотрите на страничке объявления</p>
    <div class="reviews-grid">
      <div class="rev-card">
        <div class="rev-badge">avito</div>
        <div class="rev-stars">★★★★★</div>
        <p class="rev-text">«Отличная компания! Переезжали двушку. Всё упаковали, разобрали и собрали мебель. Ни одной царапины. Цена не изменилась — как договорились, так и вышло. Рекомендую!»</p>
        <div class="rev-author">Марина К.</div>
        <div class="rev-date">Февраль 2025</div>
      </div>
      <div class="rev-card">
        <div class="rev-badge">avito</div>
        <div class="rev-stars">★★★★★</div>
        <p class="rev-text">«Переезжали офис. Приехали вовремя, работали профессионально. Всю технику упаковали хорошо. Итоговая сумма оказалась даже ниже, чем называли. Будем обращаться ещё.»</p>
        <div class="rev-author">Дмитрий В.</div>
        <div class="rev-date">Январь 2025</div>
      </div>
      <div class="rev-card">
        <div class="rev-badge">avito</div>
        <div class="rev-stars">★★★★★</div>
        <p class="rev-text">«Перевезли всю мебель из трёшки. Ребята вежливые, аккуратные. Всё целое. Работали быстро. Отдельно спасибо за упаковку пианино — очень бережно!»</p>
        <div class="rev-author">Ольга Т.</div>
        <div class="rev-date">Декабрь 2024</div>
      </div>
    </div>
    <div style="text-align:center;margin-top:30px">
      <a href="{AVITO_URL}" target="_blank" class="btn-call" style="background:var(--green);font-size:15px;padding:14px 30px">Все отзывы на Авито →</a>
    </div>
  </div>
</section>

<!-- FAQ -->
<section style="background:var(--light)">
  <div class="w">
    <h2 class="sec-title">Ответы на часто задаваемые вопросы</h2>
    <div class="faq-list">
      <div class="faq-item"><input type="checkbox" id="f1"><label class="faq-q" for="f1">Что входит в 2400 ₽/час?</label><div class="faq-a">В фиксированную ставку включены: газель до 3 тонн + 2 грузчика, разборка и сборка мебели, подъём и спуск на любой этаж, перевозка и основная упаковка стрейч-плёнкой. Никаких доплат за этаж или длинные дорожки.</div></div>
      <div class="faq-item"><input type="checkbox" id="f2"><label class="faq-q" for="f2">Как быстро вы приедете?</label><div class="faq-a">Подача авто — в течение 30 минут после звонка. Работаем круглосуточно. Если нужен срочный выезд прямо сейчас — звоните, скорее всего свободная бригада уже рядом.</div></div>
      <div class="faq-item"><input type="checkbox" id="f3"><label class="faq-q" for="f3">Есть ли минимальный заказ?</label><div class="faq-a">Минимальный заказ — 2 часа. Если переезд займёт меньше, вы всё равно платите за минимум. Но для большего удобства мы стараемся завершить всё за 2 часа.</div></div>
      <div class="faq-item"><input type="checkbox" id="f4"><label class="faq-q" for="f4">Выезжаете за пределы Калининграда?</label><div class="faq-a">Да, работаем по всей Калининградской области. Выезжаем в Гурьевск, Зеленоградск, Советск, Черняховск, Балтийск и другие города.</div></div>
      <div class="faq-item"><input type="checkbox" id="f5"><label class="faq-q" for="f5">Предоставляете ли документы для организаций?</label><div class="faq-a">Да, для юридических лиц оформляем договор, акты выполненных работ и чеки. Поддерживаем безналичную оплату.</div></div>
      <div class="faq-item"><input type="checkbox" id="f6"><label class="faq-q" for="f6">Как вы перевозите хрупкие вещи?</label><div class="faq-a">Упаковываем в пузырчатую плёнку и поролон, используем специальные ящики для хрупкого. Все вещи застрахованы на время перевозки.</div></div>
    </div>
  </div>
</section>

<!-- CONTACTS -->
<section id="contacts">
  <div class="w">
    <h2 class="sec-title">Контакты {COMPANY}</h2>
    <p class="sec-sub">Звоните или пишите — быстро ответим и рассчитаем стоимость</p>
    <div class="contacts-flex">
      <div class="contacts-info">
        <div class="cline">
          <div class="cline-icon">📞</div>
          <div>
            <div class="cline-lbl">Телефон</div>
            <div class="cline-val"><a href="tel:{PHONE_CLEAN}">{PHONE}</a></div>
          </div>
        </div>
        <div class="cline">
          <div class="cline-icon">📍</div>
          <div>
            <div class="cline-lbl">Город</div>
            <div class="cline-val">{CITY} и вся Калининградская область</div>
          </div>
        </div>
        <div class="cline">
          <div class="cline-icon">🕐</div>
          <div>
            <div class="cline-lbl">Время работы</div>
            <div class="cline-val">Ежедневно, 24 часа в сутки</div>
          </div>
        </div>
        <div class="cline">
          <div class="cline-icon">🌐</div>
          <div>
            <div class="cline-lbl">Объявление</div>
            <div class="cline-val"><a href="{AVITO_URL}" target="_blank" style="font-size:14px;font-weight:600">Смотреть на Авито</a></div>
          </div>
        </div>
        <div style="display:flex;gap:12px;margin-top:26px;flex-wrap:wrap">
          <a href="tel:{PHONE_CLEAN}" class="btn-call">📞 Позвонить</a>
          <a href="https://wa.me/{PHONE_CLEAN}" target="_blank" class="btn-call" style="background:#25d366">WhatsApp</a>
          <a href="{AVITO_URL}" target="_blank" class="btn-call" style="background:#0e5fa8">Авито</a>
        </div>
      </div>
      <div class="map-frame">
        <iframe src="https://yandex.ru/map-widget/v1/?ll=20.511742%2C54.710162&z=12&pt=20.511742,54.710162,pm2rdm&text=%D0%9A%D0%B0%D0%BB%D0%B8%D0%BD%D0%B8%D0%BD%D0%B3%D1%80%D0%B0%D0%B4"
          width="100%" height="100%" frameborder="0" allowfullscreen></iframe>
      </div>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="w">
    <div class="f-logo">
      <img src="logo.svg" alt="{COMPANY}">
      <span style="color:rgba(255,255,255,.6)">©&nbsp;2025 {COMPANY}</span>
    </div>
    <div>{CITY} — Переезды и грузоперевозки</div>
    <div>
      <a href="tel:{PHONE_CLEAN}">{PHONE}</a>
      <a href="{AVITO_URL}" target="_blank">Авито</a>
    </div>
  </div>
</footer>

<!-- STICKY BUTTONS -->
<div class="sticky">
  <a class="sticky-btn sticky-call" href="tel:{PHONE_CLEAN}" title="Позвонить">📞</a>
  <a class="sticky-btn sticky-wa" href="https://wa.me/{PHONE_CLEAN}" target="_blank" title="WhatsApp">💬</a>
</div>

</body>
</html>"""

out = OUT_DIR / "index.html"
out.write_text(HTML, encoding='utf-8')
print(f"✅ Готово! {out}")
print(f"   Строк: {len(HTML.splitlines())}")
print(f"   Размер: {out.stat().st_size // 1024} КБ")
print(f"\n⚠️  Внимание: укажите реальный телефон после получения с Авито")
