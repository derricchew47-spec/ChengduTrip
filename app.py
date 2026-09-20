# -*- coding: utf-8 -*-
"""Our Chengdu Story — single-file Streamlit app (Home-first rebuild).

Run with:
    streamlit run app.py

Everything (HTML, CSS, JS, SVG artwork) lives in this one file.

Optional: paste your bespoke landing artwork into LANDING_IMAGE_DATA as a
"data:image/webp;base64,..." string. If it is left empty, a remote panda photo
is used on the landing page instead.

Testing tip: append ?now=2026-10-16T13:20 (China time) to the app URL to
preview how the panda traveler moves along a day's route.
"""

from __future__ import annotations

import json
from urllib.parse import quote

import streamlit as st

# Paste your existing base64 landing image here (optional).
LANDING_IMAGE_DATA = ""


st.set_page_config(
    page_title="Our Chengdu Story",
    page_icon="🐼",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Keep Streamlit's own chrome out of the composition.
st.markdown(
    """
    <style>
      html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        margin: 0 !important;
        background: #e6e2d6 !important;
      }
      [data-testid="stHeader"], [data-testid="stToolbar"],
      [data-testid="stDecoration"], #MainMenu, footer { display:none !important; }
      .block-container { padding:0 !important; max-width:none !important; }
      [data-testid="stElementContainer"] { margin:0 !important; }
      iframe { display:block !important; width:100% !important; border:0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def commons(filename: str, width: int = 1400) -> str:
    """Stable Wikimedia redirect URL with an output width hint."""
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(filename)}?width={width}"


IMG = {
    "panda_portrait": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?auto=format&fit=crop&w=1600&q=92",
    "panda_bamboo": "https://images.unsplash.com/photo-1508264165352-258a6c1915d1?auto=format&fit=crop&w=1500&q=90",
    "taikoo": commons("Sino-Ocean Taikoo Li Chengdu.jpg"),
    "teahouse": commons("Tea in People's Park - Chengdu, China - DSC05362.jpg"),
    "dujiangyan": commons("都江堰南桥 Dujiangyan Nanqiao Bridge.jpg"),
    "jiuzhai": commons("九寨溝-五花海 Jiuzhaigou Five Flower Lake.jpg"),
    "jiuzhai_alt": commons("5 Flowers Lake (127556467).jpeg"),
    "sanxingdui": commons("Ancient Bronze Mask from Sanxingdui with Protruding Eyes & Ears (9951414745).jpg"),
    "airport": commons("成都天府国际机场 Chengdu Tianfu International Airport 1.jpg"),
    "airport_hall": commons("2025 Chengdu Tianfu Airport 03.jpg"),
    "mapo": commons("Authentic Mapo Tofu.jpg", 1200),
    "hotpot": commons("Sichuan-style hotpot.jpg", 1200),
    "snack": commons("Chengdu Zhong Dumpling(Zhong Jiaozi).jpg", 1200),
    "coffee": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1100&q=88",
    "noodles": commons("担担面 Dandan noodles.jpg", 1200),
    "dessert": commons("Brown Sugar Bing Fen.jpg", 1200),
}

# Each node: [time, short Chinese title (<=5 chars), image key, fallback icon]
DAYS = [
    {
        "day": 1, "iso": "2026-10-15", "date": "15 Oct", "dow": "Thu", "city": "Chengdu",
        "vt": "初见成都", "note": "先别急着认识整座城。",
        "nodes": [
            ["00:05", "飞往上海", "airport_hall", "plane"],
            ["08:10", "飞往成都", "airport", "plane"],
            ["12:00", "抵达酒店", "coffee", "hotel"],
            ["15:00", "春熙路", "taikoo", "landmark"],
            ["17:00", "人民公园", "teahouse", "leaf"],
        ],
    },
    {
        "day": 2, "iso": "2026-10-16", "date": "16 Oct", "dow": "Fri", "city": "Chengdu",
        "vt": "熊猫都江", "note": "把今天的可爱好好记住。",
        "nodes": [
            ["08:00", "酒店出发", "coffee", "hotel"],
            ["09:00", "熊猫基地", "panda_portrait", "leaf"],
            ["12:30", "午餐自由", "mapo", "food"],
            ["14:00", "都江堰", "dujiangyan", "landmark"],
            ["18:30", "返回酒店", "teahouse", "hotel"],
        ],
    },
    {
        "day": 3, "iso": "2026-10-17", "date": "17 Oct", "dow": "Sat", "city": "Jiuzhaigou",
        "vt": "九寨仙境", "note": "山水不语，记忆很久。",
        "nodes": [
            ["07:00", "早餐出发", "coffee", "hotel"],
            ["08:00", "九寨沟", "jiuzhai", "landmark"],
            ["13:00", "午餐自由", "noodles", "food"],
            ["14:00", "继续游览", "jiuzhai_alt", "leaf"],
            ["18:00", "返回酒店", "jiuzhai", "hotel"],
        ],
    },
    {
        "day": 4, "iso": "2026-10-18", "date": "18 Oct", "dow": "Sun", "city": "Dujiangyan",
        "vt": "山水慢游", "note": "山水与小惊喜，都收好。",
        "nodes": [
            ["08:00", "熊猫谷", "panda_bamboo", "leaf"],
            ["11:00", "仰天窝", "panda_portrait", "leaf"],
            ["12:30", "午餐自由", "hotpot", "food"],
            ["14:00", "灌县古城", "dujiangyan", "landmark"],
            ["19:00", "晚餐自由", "mapo", "food"],
        ],
    },
    {
        "day": 5, "iso": "2026-10-19", "date": "19 Oct", "dow": "Mon", "city": "Chengdu",
        "vt": "古蜀一日", "note": "古蜀的谜，留给夜色。",
        "nodes": [
            ["09:00", "三星堆", "sanxingdui", "landmark"],
            ["12:30", "午餐自由", "noodles", "food"],
            ["14:00", "东郊记忆", "taikoo", "landmark"],
            ["17:00", "玉林路", "teahouse", "leaf"],
            ["20:00", "九眼桥", "dujiangyan", "landmark"],
        ],
    },
    {
        "day": 6, "iso": "2026-10-20", "date": "20 Oct", "dow": "Tue", "city": "Chengdu → Penang",
        "vt": "带回成都", "note": "旅程会结束，故事还在。",
        "nodes": [
            ["08:00", "前往机场", "airport_hall", "plane"],
            ["09:00", "值机·休息", "airport", "plane"],
            ["12:30", "飞往上海", "airport", "plane"],
            ["15:15", "上海转机", "coffee", "plane"],
            ["17:30", "飞回槟城", "airport_hall", "plane"],
        ],
    },
]

FOODS = [
    [IMG["mapo"], "陈麻婆豆腐（总店）", "川菜", 1.2, 16, "Open", 4.6, ["DP", "AM", "RED"]],
    [IMG["hotpot"], "蜀大侠火锅", "火锅", 0.45, 6, "Open", 4.5, ["DP", "AM", "RED"]],
    [IMG["snack"], "建设路小吃街", "小吃", 1.8, 23, "Open", 4.4, ["DP", "AM", "RED"]],
    [IMG["noodles"], "明婷饭店", "川菜", 1.1, 14, "Open", 4.4, ["DP", "AM"]],
    [IMG["coffee"], "% Arabica · 太古里", "咖啡", 0.75, 9, "Open", 4.6, ["AM", "GG"]],
    [IMG["dessert"], "成都小甜水", "甜品", 0.9, 12, "Open", 4.3, ["DP", "RED"]],
]

PAYLOAD = json.dumps(
    {"days": DAYS, "images": IMG, "foods": FOODS, "landing_image": LANDING_IMAGE_DATA},
    ensure_ascii=False,
).replace("</", "<\\/")


HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<meta name="theme-color" content="#faf8f1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Caveat:wght@500;600&family=Ma+Shan+Zheng&family=Noto+Sans+SC:wght@300;400;500;600&family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --paper:#faf8f1; --paper-2:#f3f1e7; --sheet:#fcfbf6;
  --ink:#1f2b25; --ink-soft:#56655c; --muted:#7d8a82;
  --forest:#2c6a4c; --forest-2:#4f8467; --slate:#6f86a0; --slate-ink:#57738f;
  --line:rgba(45,80,62,.14); --gold:#e3aa3f; --coral:#d96d5f;
  --serif:"Cormorant Garamond","Noto Serif SC",serif;
  --cn-serif:"Noto Serif SC",serif; --sans:"Noto Sans SC",sans-serif;
  --hand:"Ma Shan Zheng","Noto Serif SC",serif; --script:"Caveat","Cormorant Garamond",cursive;
  --nav-h:68px; --acc-h:clamp(300px,calc(100dvh - 440px),400px);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;min-height:100%;background:#e6e2d6;color:var(--ink);font-family:var(--sans);overscroll-behavior:none}
body{display:flex;justify-content:center}
button,input{font:inherit;color:inherit}
img{display:block}
.app-shell{width:min(100%,460px);min-height:100dvh;position:relative;overflow:hidden;background:linear-gradient(180deg,#fdfcf7 0%,#f8f6ee 100%);box-shadow:0 0 60px rgba(50,60,45,.14)}
.app-shell:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.16;z-index:99;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 160 160' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.08'/%3E%3C/svg%3E")}
main{min-height:100dvh}
.page{display:none;padding:14px 8px calc(var(--nav-h) + 22px);animation:pageIn .35s ease both}
.page.active{display:block}
@keyframes pageIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
.icon{width:20px;height:20px;display:block;stroke:currentColor;fill:none;stroke-width:1.55;stroke-linecap:round;stroke-linejoin:round}
.icon.sm{width:14px;height:14px}.icon.lg{width:24px;height:24px}

/* ───── HOME ───── */
.home-top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;padding:2px 12px 12px}
.greeting{font:700 clamp(27px,7.6vw,32px)/1 var(--serif);letter-spacing:-.3px;color:#1c2a23}
.home-poem{font:500 clamp(13px,3.7vw,15px)/1.22 var(--serif);color:var(--slate-ink);margin-top:5px;max-width:200px}
.wx{text-align:right;flex:none}
.wx-row{display:flex;align-items:center;justify-content:flex-end;gap:7px}
.wx-row svg{width:30px;height:30px}
.wx-temp{font:600 clamp(22px,6.4vw,27px)/1 var(--serif);color:#1c2a23}
.wx small{display:block;margin-top:5px;font:400 11px var(--sans);color:var(--slate-ink);letter-spacing:.2px}
.hero{position:relative;height:clamp(172px,50vw,232px);border-radius:22px;overflow:hidden;background:#3d4a3a;isolation:isolate;box-shadow:0 10px 26px rgba(40,60,45,.14)}
.hero img{width:100%;height:100%;object-fit:cover;object-position:72% 38%}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(9,28,18,.56) 0%,rgba(9,28,18,.12) 58%,transparent 100%),linear-gradient(180deg,transparent 52%,rgba(9,24,16,.34) 100%)}
.hero-copy{position:absolute;z-index:2;left:20px;top:22%;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.35)}
.hero-copy .cn1,.hero-copy .cn2{font:400 clamp(27px,8.2vw,36px)/1.14 var(--hand);letter-spacing:2px}
.hero-copy .cn2{padding-left:26px}
.hero-copy .en{font:500 clamp(17px,5vw,21px)/1.05 var(--script);margin-top:9px;font-style:italic}
.sheet{position:relative;z-index:3;margin-top:-30px;background:var(--sheet);border-radius:26px 26px 0 0;padding:10px 8px 16px;box-shadow:0 -10px 24px rgba(50,60,45,.06)}
.date-row{display:flex;align-items:center;gap:11px;padding:9px 13px 9px 9px;margin-bottom:10px;border-radius:19px;background:#f1f2e9;border:1px solid rgba(60,90,70,.08);cursor:pointer;width:100%;text-align:left}
.date-row .cal{width:38px;height:38px;border-radius:50%;background:#e4e8da;display:grid;place-items:center;color:#22392d;flex:none}
.date-row b{display:block;font:500 clamp(15px,4.4vw,17px)/1.15 var(--serif);color:#25332b;letter-spacing:.1px}
.date-row span{display:block;font:400 clamp(11px,3.3vw,13px)/1.2 var(--serif);color:#6b7770;margin-top:2px}
.date-row .chev{margin-left:auto;color:#22392d}

/* Horizontal accordion */
.acc{--gap:4px;display:flex;gap:var(--gap);height:var(--acc-h)}
.strip{position:relative;flex:1 1 0;min-width:0;border-radius:18px;overflow:hidden;cursor:pointer;
  background:linear-gradient(180deg,#fefefb 0%,#f5f6ef 52%,#eef1e7 100%);
  box-shadow:0 8px 18px rgba(50,70,55,.08),inset 0 1px 0 #fff;
  transition:flex-grow .62s cubic-bezier(.32,.72,.2,1),box-shadow .45s,background .45s;outline:none;-webkit-user-select:none;user-select:none}
.strip:after{content:"";position:absolute;inset:0;border-radius:inherit;border:1px solid rgba(70,100,80,.14);pointer-events:none;z-index:8;transition:border-color .4s}
.strip:focus-visible{outline:2px solid var(--forest);outline-offset:2px}
.strip.open{flex-grow:9;cursor:default;background:linear-gradient(180deg,#fffef9 0%,#faf9f0 60%,#f3f4e9 100%);box-shadow:0 12px 26px rgba(50,70,55,.13),inset 0 1px 0 #fff}
.strip.open:after{border-color:rgba(60,110,80,.26)}
.cover{position:absolute;left:0;right:0;bottom:0;height:52%;pointer-events:none;transition:opacity .6s,filter .6s;-webkit-mask-image:linear-gradient(180deg,rgba(0,0,0,0) 0%,#000 36%);mask-image:linear-gradient(180deg,rgba(0,0,0,0) 0%,#000 36%)}
.cover svg{width:100%;height:100%;display:block}
.strip.open .cover{opacity:.2;filter:blur(.8px)}
.head{position:absolute;top:10px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:11px;transition:opacity .22s}
.strip.open .head{opacity:0;pointer-events:none}
.marker{width:calc(100% - 12px);max-width:46px;aspect-ratio:1}
.marker svg,.pmarker svg{width:100%;height:100%;display:block;overflow:visible}
.vt{writing-mode:vertical-rl;text-orientation:upright;font:600 var(--vt,15px)/1.3 var(--cn-serif);letter-spacing:.2em;color:#25352c;white-space:nowrap;transition:font-size .5s,letter-spacing .5s}
.acc.has-open .strip:not(.open) .marker{width:calc(100% - 5px)}
.acc.has-open .strip:not(.open) .head{gap:9px;top:9px}
.acc.has-open .strip:not(.open) .vt{font-size:11px;letter-spacing:.12em}
.panel{position:absolute;left:0;top:0;bottom:0;width:calc(var(--ew,210px));padding:9px 9px 8px;display:flex;flex-direction:column;opacity:0;pointer-events:none;transition:opacity .2s}
.strip.open .panel{opacity:1;pointer-events:auto;transition:opacity .42s .3s}
.p-head{text-align:center;cursor:pointer;padding:0 20px}
.p-heads{display:flex;justify-content:center;gap:3px;height:21px}
.p-heads svg{width:21px;height:21px;display:block;overflow:visible}
.p-title b{display:block;font:700 17px/1.15 var(--cn-serif);color:var(--ink);margin-top:5px;white-space:nowrap;letter-spacing:.06em}
.p-title span{display:block;font:500 9.5px var(--sans);color:var(--muted);letter-spacing:.3px;margin-top:3px;white-space:nowrap}
.close{position:absolute;top:8px;right:8px;width:24px;height:24px;border-radius:50%;border:1px solid var(--line);background:rgba(255,255,255,.85);display:grid;place-items:center;color:#4a5b52;cursor:pointer;padding:0;z-index:9}
.p-note{text-align:center;font:400 12.5px/1.35 var(--hand);color:#5a7a67;margin:5px 2px 0;white-space:nowrap}

/* Illustrated route */
.route{position:relative;flex:1;min-height:0;margin-top:2px}
.rz{position:absolute;left:0;right:0;top:34px;bottom:2px}
.rz svg.line{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.rz path{fill:none;vector-effect:non-scaling-stroke;stroke-linecap:round;stroke-linejoin:round}
.rz .base{stroke:#a3b8a8;stroke-width:1.6;stroke-dasharray:1.5 5}
.rz .done{stroke:#3f7b5c;stroke-width:2.3}
.node{position:absolute;left:0;right:0;height:0}
.strip.open .panel:not(.quiet) .node{animation:nodeIn .5s cubic-bezier(.2,.8,.2,1) both;animation-delay:calc(.34s + var(--d,0s))}
@keyframes nodeIn{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:none}}
.dot{position:absolute;top:0;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;background:#fbfaf3;border:2px solid #8ba796;z-index:3}
.node.done .dot{background:#3f7b5c;border-color:#fbfaf3;box-shadow:0 0 0 1px #3f7b5c}
.node.cur .dot{background:var(--gold);border-color:#fffdf5;box-shadow:0 0 0 5px rgba(227,170,63,.24)}
.card{position:absolute;top:-20px;height:40px;display:flex;align-items:center;gap:4px;z-index:2}
.card.r{left:57%;right:0}
.card.l{left:0;right:57%;flex-direction:row-reverse;text-align:right}
.thumb{position:relative;width:38px;height:38px;flex:none;overflow:hidden;border-radius:46% 54% 50% 50%/54% 46% 54% 46%;background:linear-gradient(145deg,#dfe9d9,#f0eedc);display:grid;place-items:center;color:#5b7f69;-webkit-mask-image:radial-gradient(ellipse at 50% 50%,#000 60%,rgba(0,0,0,0) 100%);mask-image:radial-gradient(ellipse at 50% 50%,#000 60%,rgba(0,0,0,0) 100%)}
.thumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(.9) contrast(.96) brightness(1.04)}
.t{min-width:0;flex:1;text-shadow:0 0 4px #fbfaf3,0 0 7px #fbfaf3}
.t small{display:block;font:700 9.5px/1 var(--serif);color:var(--forest-2);letter-spacing:.2px}
.t b{display:block;font:600 9.5px/1.15 var(--cn-serif);color:var(--ink);margin-top:3px;white-space:nowrap}
.node.done .t{opacity:.8}
.panda{position:absolute;width:30px;height:40px;margin:-38px 0 0 -15px;z-index:5;transition:left 1.7s cubic-bezier(.4,.1,.2,1),top 1.7s cubic-bezier(.4,.1,.2,1);filter:drop-shadow(0 3px 2px rgba(30,50,40,.26))}
.panda svg{width:100%;height:100%;display:block}
.panda.walk svg{animation:bob .75s ease-in-out infinite alternate}
@keyframes bob{to{transform:translateY(-2px)}}
.panel.quiet .panda{transition:none}

/* ───── BOTTOM NAV ───── */
.bottom-nav{position:fixed;z-index:80;left:50%;bottom:0;transform:translateX(-50%);width:min(100vw,460px);height:calc(var(--nav-h) + env(safe-area-inset-bottom));padding:6px 10px env(safe-area-inset-bottom);display:grid;grid-template-columns:repeat(4,1fr);background:rgba(253,252,247,.95);backdrop-filter:blur(16px);border-top:1px solid rgba(60,75,65,.1)}
.nav-btn{border:0;background:transparent;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;font:400 10.5px var(--sans);color:var(--slate);cursor:pointer}
.nav-btn .icon{width:22px;height:22px}
.nav-btn.active{color:var(--forest);font-weight:600}
.nav-btn.active .icon{stroke-width:2}

/* ───── shared page bits (Food / Explore / Expenses) ───── */
.page-head{height:50px;display:grid;grid-template-columns:42px 1fr 42px;align-items:center;margin:1px 0 8px}
.page-head .center{text-align:center}.page-head h1{font:600 27px/.9 var(--serif);margin:0}.page-head .sub{font-size:9px;color:var(--muted);margin-top:5px}
.round-btn{width:38px;height:38px;border:1px solid var(--line);border-radius:50%;background:rgba(255,255,255,.82);display:grid;place-items:center;cursor:pointer}
.paper-card{background:rgba(255,255,255,.9);border:1px solid rgba(44,116,84,.1);box-shadow:0 8px 22px rgba(45,70,55,.06)}
.search-box{border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.6);display:flex;align-items:center;gap:9px;padding:11px 13px;font-size:10px;color:var(--muted)}
.filter-scroll{display:flex;gap:7px;overflow:auto;scrollbar-width:none;margin:11px 0 13px}.filter-scroll::-webkit-scrollbar{display:none}
.filter-chip{border:0;border-radius:99px;background:#eae7db;padding:7px 12px;white-space:nowrap;font-size:10px;color:#626960;cursor:pointer}.filter-chip.active{background:var(--forest);color:#fff}
.radius-select{display:flex;justify-content:flex-end;gap:5px;margin:-3px 0 10px}.radius-select button{border:0;background:transparent;color:#85877f;font-size:9px;padding:3px;cursor:pointer}.radius-select button.active{color:var(--forest);font-weight:600;border-bottom:1px solid var(--forest)}
.food-list{display:grid;gap:9px}.food-card{display:grid;grid-template-columns:104px 1fr;gap:12px;padding:8px;border-radius:19px}.food-card img{width:104px;height:101px;border-radius:15px;object-fit:cover}.food-card h3{font:600 13px/1.3 var(--cn-serif);margin:3px 0 5px}.food-meta{font-size:9px;line-height:1.65;color:var(--muted)}.food-rating{font:600 12px var(--serif);color:var(--gold)}.platforms{display:flex;gap:5px;margin-top:7px}.platform{width:22px;height:17px;border-radius:5px;background:#e4ece3;color:#3c674e;display:grid;place-items:center;font:600 6.5px var(--sans);font-style:normal}.open-t{color:#4c7256;font-weight:600}
.ending{margin:20px 0 6px;text-align:center;padding:16px 12px;color:#6d5b49}.ending .cn{font:400 15px var(--cn-serif)}.ending .en{font:italic 12px var(--serif);margin-top:5px;color:#878078}
.map-cats{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin:10px 0}.map-cat{border:1px solid var(--line);border-radius:15px;background:rgba(255,255,255,.55);padding:9px 2px;text-align:center;font-size:9px;color:#5f675f}.map-cat .icon{margin:0 auto 5px;color:var(--forest)}
.map-wrap{height:420px;margin:0 -8px;position:relative;overflow:hidden;background:#e5e9df}.map-wrap svg{width:100%;height:100%;display:block}
.map-top-note{position:absolute;top:14px;left:50%;transform:translateX(-50%);border-radius:15px;background:rgba(255,255,255,.92);box-shadow:0 8px 22px rgba(37,54,43,.12);padding:10px 13px;font-size:10px;white-space:nowrap;color:#536159;display:flex;gap:6px;align-items:center}
.map-you{position:absolute;left:51%;top:48%;transform:translate(-50%,-50%);width:48px;height:48px;border-radius:50%;background:rgba(47,92,65,.13);display:grid;place-items:center}.map-you:before{content:"";width:16px;height:16px;border-radius:50%;background:var(--forest);border:4px solid #fff;box-shadow:0 4px 11px rgba(26,61,42,.26)}
.poi{position:absolute;transform:translate(-50%,-100%);width:28px;height:34px;border-radius:16px 16px 16px 4px;rotate:-45deg;background:#a75a4d;box-shadow:0 5px 10px rgba(46,56,48,.18);display:grid;place-items:center}.poi .icon{rotate:45deg;color:#fff;width:14px;height:14px}.poi.green{background:#4c7058}.poi.gold{background:#b78343}.poi.pink{background:#ad6c7d}.poi.blue{background:#4f7da3}
.exp-total{border-radius:22px;padding:18px;text-align:center;background:linear-gradient(140deg,#eef3e6,#fbf7e8)}.exp-total small{font:500 10px var(--sans);color:var(--muted)}.exp-total b{display:block;font:600 38px/1.1 var(--serif);color:#25382e;margin-top:6px}
.exp-form{border-radius:20px;padding:13px;margin-top:11px}.exp-row{display:flex;gap:7px;margin-top:9px}.exp-input{min-width:0;flex:1;border:1px solid var(--line);background:#fffefa;border-radius:13px;padding:10px 11px;font-size:12px;outline:none}.exp-input:focus{border-color:#77917c;box-shadow:0 0 0 3px rgba(83,119,91,.1)}.exp-input.amt{flex:0 0 96px}
.exp-add{border:0;border-radius:13px;background:var(--forest);color:#fff;padding:0 15px;font-size:12px;cursor:pointer}
.exp-list{margin-top:11px;display:grid;gap:7px}.exp-item{display:grid;grid-template-columns:1fr auto auto;align-items:center;gap:10px;border-radius:15px;padding:10px 12px}.exp-item b{font:600 12px var(--cn-serif)}.exp-item small{display:block;font-size:9px;color:var(--muted);margin-top:3px}.exp-item .amt{font:600 16px var(--serif)}.exp-item button{border:0;background:transparent;color:#9a9a92;cursor:pointer;padding:4px}

/* ───── LANDING ───── */
#landing{position:fixed;z-index:200;inset:0;margin:auto;width:min(100vw,460px);height:100dvh;overflow:hidden;background:#d8ebe3;transition:opacity .7s ease,visibility .7s ease}
#landing.hidden{opacity:0;visibility:hidden;pointer-events:none}
.land-scene{position:absolute;inset:0;overflow:hidden;background:#d8ebe3}
.land-scene img{width:100%;height:100%;object-fit:cover;object-position:50% 50%;animation:landCamera 8.8s cubic-bezier(.2,.72,.2,1) forwards}
.land-scene:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(250,253,247,.48) 0%,rgba(250,253,247,.02) 34%,rgba(19,71,52,.02) 61%,rgba(13,51,38,.52) 100%)}
@keyframes landCamera{0%{transform:scale(1.045) translate3d(0,1%,0)}100%{transform:scale(1) translate3d(0,-.4%,0)}}
.land-bamboo{position:absolute;z-index:2;left:-45px;top:-18px;width:215px;height:330px;opacity:.75;transform-origin:top;animation:sway 4.8s ease-in-out infinite alternate;pointer-events:none}
@keyframes sway{to{transform:rotate(2.4deg) translateX(3px)}}
.land-bamboo svg{width:100%;height:100%}
.land-brand{position:absolute;z-index:3;left:25px;right:25px;top:max(30px,env(safe-area-inset-top));text-align:center;color:#13231c;text-shadow:0 1px 12px rgba(255,255,255,.7);animation:titleReveal 1.2s ease both}
.land-brand h1{font:600 44px/.88 var(--serif);margin:0;letter-spacing:-1.3px}
.land-brand p{margin:11px 0 0;font:500 9px var(--sans);letter-spacing:4px}
.land-brand:after{content:"";display:block;width:28px;height:1px;background:#526358;margin:16px auto}
@keyframes titleReveal{from{opacity:0;transform:translateY(-9px)}to{opacity:1;transform:none}}
.land-note{position:absolute;z-index:3;left:28px;right:28px;top:24%;text-align:right;color:#213f34;opacity:0;animation:noteIn .9s 2.4s ease forwards}
.land-note .cn{font:400 21px/1.55 var(--hand);letter-spacing:1px}.land-note .en{font:italic 13px var(--serif);color:#676c63}
@keyframes noteIn{to{opacity:1;transform:translateY(-6px)}}
.land-bubble{position:absolute;z-index:5;right:18px;left:68px;top:38%;padding:15px 18px 14px;border-radius:25px 25px 7px 25px;background:rgba(255,254,248,.93);color:#1e3a2f;box-shadow:0 13px 36px rgba(23,74,54,.16);opacity:0;transform:translateY(12px) scale(.97);animation:bubbleIn .7s 5.05s cubic-bezier(.2,.8,.2,1) forwards}
.land-bubble .cn{font:600 15px/1.5 var(--cn-serif)}.land-bubble .en{font:italic 12px/1.35 var(--serif);color:#74776e;margin-top:4px}
@keyframes bubbleIn{to{opacity:1;transform:none}}
.land-final{position:absolute;z-index:6;left:14px;right:14px;bottom:max(16px,env(safe-area-inset-bottom));border:1px solid rgba(255,255,255,.7);border-radius:28px;background:rgba(251,255,249,.94);box-shadow:0 20px 50px rgba(13,65,45,.24);padding:15px;opacity:0;transform:translateY(25px);animation:finalIn .8s 6.25s ease forwards}
@keyframes finalIn{to{opacity:1;transform:none}}
.land-final-top{display:flex;gap:12px;align-items:center}.land-avatar{width:48px;height:48px;border-radius:50%;object-fit:cover;border:3px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,.1)}
.land-final h3{font:600 20px/1 var(--serif);margin:0 0 4px}.land-final p{font-size:10px;color:var(--muted);margin:0}
.enter-btn{width:100%;margin-top:13px;border:0;border-radius:17px;padding:13px 15px;background:var(--forest);color:#fff;display:flex;align-items:center;justify-content:center;gap:9px;font-size:12px;cursor:pointer}
.land-skip{position:absolute;z-index:9;top:max(18px,env(safe-area-inset-top));right:16px;border:0;background:rgba(255,255,255,.5);backdrop-filter:blur(10px);padding:8px 11px;border-radius:99px;font-size:9px;color:#2d3e35;cursor:pointer}

@media (min-width:461px){.app-shell{margin:18px 0;border-radius:32px;min-height:calc(100dvh - 36px)}#landing{height:calc(100dvh - 36px);top:18px;border-radius:32px}.bottom-nav{bottom:18px;border-radius:0 0 32px 32px}}
@media (prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.001ms!important;animation-delay:0ms!important;transition-duration:.001ms!important;transition-delay:0ms!important}}
</style>
</head>
<body>
<div class="app-shell">
  <div id="landing" aria-label="Our Chengdu Story opening">
    <div class="land-scene"><img id="landingPhoto" alt="A giant panda walking beside a Chengdu garden lake"></div>
    <div class="land-bamboo" aria-hidden="true"><svg viewBox="0 0 210 330" fill="none"><path d="M21-5c16 91 30 192 47 345M83-10c5 102 13 203 20 344" stroke="#60775f" stroke-width="4" opacity=".62"/><g fill="#748a70" opacity=".75"><path d="M33 48C7 22 3 11 1 2c25 3 43 14 51 33-5 8-11 12-19 13Z"/><path d="M46 85C16 70 7 59 3 50c26-3 46 4 58 20-2 8-7 13-15 15Z"/><path d="M62 141c-31-9-42-18-48-26 25-8 47-5 62 8 0 8-6 14-14 18Z"/><path d="M94 52c22-25 35-30 45-31-7 25-20 41-39 46-7-6-9-10-6-15Z"/><path d="M101 112c28-18 42-20 51-18-13 22-30 34-50 34-5-7-6-12-1-16Z"/><path d="M108 183c29-17 43-18 52-16-14 22-32 32-52 31-5-7-5-12 0-15Z"/></g></svg></div>
    <button class="land-skip" onclick="enterApp()">SKIP</button>
    <div class="land-brand"><h1>Our<br>Chengdu Story</h1><p>A FAMILY JOURNEY</p></div>
    <div class="land-note"><div class="cn">慢一点，<br>和家人在一起。</div><div class="en">Slower steps. Richer memories.</div></div>
    <div class="land-bubble" id="landingBubble"></div>
    <div class="land-final">
      <div class="land-final-top"><img class="land-avatar" id="landingAvatar" alt="Panda"><div><h3 id="landingPhase">Before Chengdu</h3><p>15–20 October 2026 · Family journey</p></div></div>
      <button class="enter-btn" onclick="enterApp()">开启我们的成都之旅 <span>→</span></button>
    </div>
  </div>

  <main>
    <section id="home" class="page active"></section>
    <section id="food" class="page"></section>
    <section id="explore" class="page"></section>
    <section id="expenses" class="page"></section>
  </main>
  <nav class="bottom-nav" aria-label="Main navigation"></nav>
</div>

<script>
const DATA=__DATA__;
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const days=DATA.days;
let foodCategory='全部', foodRadius=5, expCat='餐饮', openIdx=-1, wx=null;

/* Safe storage (falls back to memory if the frame blocks localStorage) */
const mem={};
const store={get(k){try{return localStorage.getItem(k)}catch(e){return mem[k]??null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){mem[k]=v}}};

/* ───── icons ───── */
const ICONS={
 home:'<path d="M3 10.8 10 4l7 6.8v7.1a1.1 1.1 0 0 1-1.1 1.1H4.1A1.1 1.1 0 0 1 3 17.9Z"/><path d="M7.6 19v-5.4h4.8V19"/>',
 homeSolid:'<path d="M10 2.6 2.3 9.5a.6.6 0 0 0 .4 1H4v7.1a1 1 0 0 0 1 1h3.3v-5h3.4v5H15a1 1 0 0 0 1-1v-7.1h1.3a.6.6 0 0 0 .4-1Z" fill="currentColor" stroke="none"/>',
 food:'<path d="M6 3v6M4 3v4a2 2 0 0 0 4 0V3M6 9v8M13 3v14M13 3c3 2 3 6 0 8"/>',
 compass:'<circle cx="10" cy="10" r="7.5"/><path d="m12.8 7.2-1.7 3.9-3.9 1.7 1.7-3.9Z"/>',
 wallet:'<rect x="2" y="6" width="16" height="11.5" rx="2.2"/><path d="M4 6l9-3a1 1 0 0 1 1.3 1v2M13 11.7h5v3h-5a1.5 1.5 0 0 1 0-3Z"/>',
 calendar:'<rect x="3" y="5" width="14" height="13" rx="2"/><path d="M6 3v4M14 3v4M3 9h14M7 12h.01M10 12h.01M13 12h.01M7 15h.01M10 15h.01"/>',
 chevron:'<path d="m8 4 6 6-6 6"/>', back:'<path d="m12.5 4-6 6 6 6"/>', close:'<path d="M5.5 5.5l9 9M14.5 5.5l-9 9"/>',
 search:'<circle cx="8.7" cy="8.7" r="5.7"/><path d="m13 13 4.5 4.5"/>',
 pin:'<path d="M16 8.5c0 5-6 9-6 9s-6-4-6-9a6 6 0 1 1 12 0Z"/><circle cx="10" cy="8.5" r="2"/>',
 plane:'<path d="m2 12 6-2 3-7 2 .8-1 6.5 4.8 1.9c1.7.7 1 2.5-.5 2.4l-5-.6-3 4-1.5-.6 1.3-4.6-5.6.9Z"/>',
 hotel:'<path d="M3 18V5h9v13M12 9h5v9M6 8h2M6 11h2M6 14h2M15 12h.01M15 15h.01"/>',
 landmark:'<path d="M3 18h14M5 18V9h10v9M3 9h14L10 3 3 9ZM8 12h4M8 15h4"/>',
 leaf:'<path d="M17 3C8 3 4 7 4 13c0 2 1 3 3 3 6 0 9-5 10-13Z"/><path d="M4 18c2-5 5-8 10-11"/>',
 coffee:'<path d="M4 7h10v4a5 5 0 0 1-10 0ZM14 8h1.2a2.3 2.3 0 0 1 0 4.6H14M5 4c1-1 2 1 3 0s2 1 3 0"/>',
 shopping:'<path d="M4 7h12l-1 11H5Z"/><path d="M7 8V6a3 3 0 0 1 6 0v2"/>',
 toilet:'<circle cx="6" cy="4" r="1.5"/><circle cx="14" cy="4" r="1.5"/><path d="M4 8h4v4H7v6H5v-6H4ZM12 8h4l1 5h-2v5h-2v-5h-2Z"/>',
 pharmacy:'<path d="M3 7h14v10H3ZM7 3h6v4M10 9v6M7 12h6"/>',
 trash:'<path d="M4 6h12M8 6V4h4v2M6 6l.7 11h6.6L14 6"/>'
};
const icon=(n,c='')=>`<svg class="icon ${c}" viewBox="0 0 20 20" aria-hidden="true">${ICONS[n]||ICONS.leaf}</svg>`;
const esc=s=>String(s??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));

/* ───── time (China Standard Time; ?now=YYYY-MM-DDTHH:MM overrides for testing) ───── */
function chinaNow(){
  let ov=null;try{ov=new URLSearchParams(window.parent.location.search).get('now')}catch(e){}
  if(ov&&/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(ov))return{iso:ov.slice(0,10),h:+ov.slice(11,13),m:+ov.slice(14,16)};
  const p=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(new Date());
  const o=Object.fromEntries(p.map(x=>[x.type,x.value]));
  return{iso:`${o.year}-${o.month}-${o.day}`,h:+o.hour,m:+o.minute};
}
const hm=t=>{const [h,m]=t.split(':').map(Number);return h*60+m};
function phase(){const n=chinaNow();if(n.iso<'2026-10-15')return'before';if(n.iso>'2026-10-20')return'after';return n.iso==='2026-10-20'?'return':'during'}
function currentDay(){const n=chinaNow();if(n.iso<'2026-10-15')return 1;if(n.iso>'2026-10-20')return 6;return Math.max(1,Math.min(6,Number(n.iso.slice(-2))-14))}
function greeting(){const h=chinaNow().h;return h<12?'Good morning,':h<18?'Good afternoon,':'Good evening,'}

/* ───── panda-head day markers (Mahjong circle-dot layouts) ───── */
const LAY={1:[[30,30]],2:[[30,16],[30,44]],3:[[15,15],[30,30],[45,45]],4:[[18,18],[42,18],[18,42],[42,42]],5:[[16,16],[44,16],[30,30],[16,44],[44,44]],6:[[18,11],[42,11],[18,30],[42,30],[18,49],[42,49]]};
const RAD={1:20,2:14,3:11,4:11.5,5:10,6:9.2};
function pandaHead(cx,cy,R){
  const k=v=>(v*R).toFixed(2), e='#242c28';
  return `<g transform="translate(${cx} ${cy})"><circle cx="${k(-.62)}" cy="${k(-.6)}" r="${k(.31)}" fill="${e}"/><circle cx="${k(.62)}" cy="${k(-.6)}" r="${k(.31)}" fill="${e}"/><ellipse cx="0" cy="${k(.08)}" rx="${k(.8)}" ry="${k(.72)}" fill="#fffef8" stroke="#2a322d" stroke-width="${k(.05)}"/><ellipse cx="${k(-.32)}" cy="${k(.02)}" rx="${k(.17)}" ry="${k(.25)}" transform="rotate(22 ${k(-.32)} ${k(.02)})" fill="${e}"/><ellipse cx="${k(.32)}" cy="${k(.02)}" rx="${k(.17)}" ry="${k(.25)}" transform="rotate(-22 ${k(.32)} ${k(.02)})" fill="${e}"/><circle cx="${k(-.3)}" cy="${k(-.03)}" r="${k(.05)}" fill="#fff"/><circle cx="${k(.3)}" cy="${k(-.03)}" r="${k(.05)}" fill="#fff"/><ellipse cx="0" cy="${k(.3)}" rx="${k(.1)}" ry="${k(.075)}" fill="${e}"/><path d="M${k(-.09)} ${k(.42)}Q0 ${k(.52)} ${k(.09)} ${k(.42)}" fill="none" stroke="${e}" stroke-width="${k(.045)}" stroke-linecap="round"/></g>`;
}
const marker=n=>`<svg viewBox="0 0 60 60" role="img" aria-label="${n}">${LAY[n].map(p=>pandaHead(p[0],p[1],RAD[n])).join('')}</svg>`;

/* ───── watercolor cover art (one landmark scene per day) ───── */
const pine=(x,y,s,c)=>`<g transform="translate(${x} ${y}) scale(${s})"><path d="M0 -17L-5.5 -6.5H-2.6L-7.5 1.5H-3.4L-8.6 10H8.6L3.4 1.5H7.5L2.6 -6.5H5.5Z" fill="${c}"/><rect x="-1" y="10" width="2" height="4" fill="#75624d"/></g>`;
const tree=(x,y,s,c)=>`<g transform="translate(${x} ${y}) scale(${s})"><rect x="-.9" y="-3" width="1.8" height="8" fill="#7a664f"/><circle cx="0" cy="-10" r="6.6" fill="${c}"/><circle cx="-5" cy="-5" r="5" fill="${c}"/><circle cx="5" cy="-5" r="5" fill="${c}"/></g>`;
const leaf=(x,y,a,l,c)=>`<path transform="translate(${x} ${y}) rotate(${a})" d="M0 0Q${l*.5} ${-l*.2} ${l} 0Q${l*.5} ${l*.2} 0 0Z" fill="${c}" opacity=".93"/>`;
function bamboo(x,top,bot,w){
  let s=`<path d="M${x} ${bot}L${x+.5} ${top}" stroke="#7aa47c" stroke-width="${w}" stroke-linecap="round"/>`;
  for(let y=bot-20;y>top+6;y-=21)s+=`<path d="M${x-w*.7} ${y}h${w*1.4}" stroke="#4c7550" stroke-width=".8"/>`;
  for(let k=0;k<5;k++){const y=top+6+k*11,r=k%2;s+=leaf(x,y,r?-25-k*5:-155+k*5,13-k*.8,r?'#88b083':'#6f9d72')+leaf(x,y+4,r?15+k*5:165-k*5,11-k*.6,'#96ba8b')}
  return s;
}
const lantern=(x,y,r,l)=>`<g><path d="M${x} ${y}V${y+l}" stroke="#5a3b2a" stroke-width=".7"/><circle cx="${x}" cy="${y+l+r}" r="${(r*2.2).toFixed(1)}" fill="#f6ae52" opacity=".3"/><rect x="${x-r*.5}" y="${y+l-.8}" width="${r}" height="1.6" fill="#4a3325"/><ellipse cx="${x}" cy="${y+l+r}" rx="${r}" ry="${(r*1.12).toFixed(1)}" fill="#c9433a"/><path d="M${x-r*.55} ${y+l+r*.7}Q${x} ${y+l+r*1.5} ${x+r*.55} ${y+l+r*.7}" stroke="#f2a08a" stroke-width=".5" fill="none"/><path d="M${x} ${y+l+r*2.1}v${r*1.5}" stroke="#e0a54a" stroke-width=".9"/></g>`;

const PB=`<ellipse cx="17" cy="59" rx="6" ry="4.5" fill="#242c28"/><ellipse cx="31" cy="57" rx="6" ry="4.5" fill="#242c28"/><ellipse cx="24" cy="42" rx="16" ry="17" fill="#fffef8" stroke="#2a322d" stroke-width=".8"/><path d="M8.5 37c2-9 10-13 15.5-13s13.5 4 15.5 13c-3-3-8-4.5-15.5-4.5S11.5 34 8.5 37z" fill="#242c28"/><ellipse cx="9" cy="43" rx="5.2" ry="11" transform="rotate(8 9 43)" fill="#242c28"/><ellipse cx="39" cy="43" rx="5.2" ry="11" transform="rotate(-8 39 43)" fill="#242c28"/><rect x="13.5" y="33" width="21" height="22" rx="5.5" fill="#7f9c5c" stroke="#5a7340" stroke-width=".8"/><rect x="13.5" y="33" width="21" height="9" rx="4.5" fill="#93ae6f"/><rect x="18" y="44" width="12" height="7" rx="2.5" fill="#6f8a4f" stroke="#5a7340" stroke-width=".6"/><path d="M16 34v20M32 34v20" stroke="#5a7340" stroke-width=".9" opacity=".6"/><rect x="11.5" y="29.5" width="25" height="5.5" rx="2.7" fill="#d9b56a" stroke="#a78440" stroke-width=".6"/><circle cx="10.5" cy="9" r="5.3" fill="#242c28"/><circle cx="37.5" cy="9" r="5.3" fill="#242c28"/><ellipse cx="24" cy="17" rx="15" ry="13" fill="#fffef8" stroke="#2a322d" stroke-width=".8"/>`;
const PANDA=`<svg viewBox="0 0 48 64" aria-hidden="true">${PB}</svg>`;

function art(d){
  const lg=(id,stops)=>`<linearGradient id="${id}${d}" x1="0" y1="0" x2="0" y2="1">${stops.map(s=>`<stop offset="${s[0]}" stop-color="${s[1]}"${s[2]!=null?` stop-opacity="${s[2]}"`:''}/>`).join('')}</linearGradient>`;
  const defs=`<defs>
   <filter id="wc${d}" x="-4%" y="-4%" width="108%" height="108%" color-interpolation-filters="sRGB">
     <feTurbulence type="fractalNoise" baseFrequency=".03 .045" numOctaves="3" seed="${d+2}" result="n"/>
     <feDisplacementMap in="SourceGraphic" in2="n" scale="4.5" xChannelSelector="R" yChannelSelector="G" result="w"/>
     <feTurbulence type="fractalNoise" baseFrequency=".5" numOctaves="2" seed="${d+9}" result="g"/>
     <feColorMatrix in="g" type="matrix" values=".4 .4 .4 0 .45  .4 .4 .4 0 .45  .4 .4 .4 0 .45  0 0 0 0 1" result="gg"/>
     <feBlend in="w" in2="gg" mode="multiply" result="m"/>
     <feComposite in="m" in2="w" operator="in"/>
   </filter>
   <filter id="bl${d}" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.6"/></filter>
   ${lg('fd',[[0,'#f4f5ed',1],[.34,'#f4f5ed',0]])}
   ${lg('lk',[[0,'#86d8d2'],[1,'#3f9db8']])}
   ${lg('rv',[[0,'#a9d8d6'],[1,'#6ab0bf']])}
   ${lg('gl',[[0,'#f8e2a6'],[1,'#e9b866']])}
   ${lg('bz',[[0,'#98c4ae'],[1,'#5f8f7c']])}
   ${lg('sk',[[0,'#d8ebf2'],[1,'#f4f5ed']])}
   ${lg('gs',[[0,'#cfe4ea'],[1,'#a6c5d0']])}
   <radialGradient id="glow${d}" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#f6b45c" stop-opacity=".55"/><stop offset="1" stop-color="#f6b45c" stop-opacity="0"/></radialGradient>
  </defs>`;
  const A={
  /* Day 1 — lantern-lit Sichuan street (Chunxi · People's Park · Kuanzhai) */
  1:`<g filter="url(#bl${d})"><path d="M0 112C16 92 30 100 48 84S80 80 100 98V250H0Z" fill="#cfdccf" opacity=".85"/></g>
  <g filter="url(#wc${d})">
   <path d="M0 136C10 114 24 120 34 110S60 106 74 114 94 110 100 122V160H0Z" fill="#8fb08f" opacity=".8"/>
   <rect x="12" y="178" width="76" height="44" fill="#dccca6"/><rect x="14" y="144" width="72" height="34" fill="#e6d6b0"/>
   <path d="M3 146Q7 124 50 117Q93 124 97 146L91 148Q87 135 50 130Q13 135 9 148Z" fill="#59606a"/>
   <path d="M3 146Q1 151 8 150M97 146Q99 151 92 150" stroke="#59606a" stroke-width="1.6" fill="none"/>
   <path d="M13 138Q50 126 87 138M19 143Q50 133 81 143" stroke="#828a94" stroke-width=".8" fill="none" opacity=".75"/>
   <path d="M7 180Q10 171 50 167Q90 171 93 180L89 182H11Z" fill="#6a717b"/>
   <rect x="20" y="149" width="14" height="19" fill="#f4dc9f"/><rect x="43" y="149" width="14" height="19" fill="#f4dc9f"/><rect x="66" y="149" width="14" height="19" fill="#f4dc9f"/>
   <path d="M27 149v19M20 158h14M50 149v19M43 158h14M73 149v19M66 158h14" stroke="#8a5a3c" stroke-width=".9"/>
   <path d="M15 144V222M38 144V222M62 144V222M85 144V222" stroke="#7a4b34" stroke-width="2.3"/>
   <rect x="19" y="187" width="16" height="35" fill="url(#gl${d})"/><rect x="42" y="187" width="16" height="35" fill="url(#gl${d})"/><rect x="65" y="187" width="16" height="35" fill="url(#gl${d})"/>
   <rect x="39" y="181" width="22" height="7" rx="1" fill="#8a3f34"/><path d="M42 184.5h16" stroke="#e6c26a" stroke-width="1.2"/>
   ${lantern(24,152,4.2,5)}${lantern(37,152,3.8,10)}${lantern(63,152,3.8,10)}${lantern(77,152,4.2,5)}${lantern(28,181,3.2,6)}${lantern(50,190,3,4)}${lantern(72,181,3.2,6)}
   <ellipse cx="50" cy="222" rx="36" ry="6" fill="url(#glow${d})"/>
   <path d="M0 222H100V250H0Z" fill="#c8c2b1"/><rect x="8" y="219" width="84" height="4" fill="#d8d2c3"/>
   <path d="M0 233H100M0 244H100M22 222L12 250M50 222V250M78 222L88 250" stroke="#a8a291" stroke-width=".7" fill="none"/>
   <path d="M6 231h11l-1.6 9H7.6z" fill="#b8734f"/><circle cx="11.5" cy="226" r="6" fill="#5f8c60"/><circle cx="7" cy="229" r="4.4" fill="#79a06a"/><circle cx="16" cy="229" r="4.4" fill="#4f7d56"/>
   <path d="M83 231h11l-1.6 9h-7.8z" fill="#b8734f"/><circle cx="88.5" cy="226" r="6" fill="#5f8c60"/><circle cx="84" cy="229" r="4.4" fill="#79a06a"/><circle cx="93" cy="229" r="4.4" fill="#4f7d56"/>
  </g>`,
  /* Day 2 — panda base (panda & bamboo) with a hint of Dujiangyan's bridge */
  2:`<g filter="url(#bl${d})"><path d="M0 116L22 76 34 96 54 62 72 94 86 78 100 108V250H0Z" fill="#cfdcd2" opacity=".85"/></g>
  <g filter="url(#wc${d})">
   <g opacity=".45"><path d="M56 151H96V155H56Z" fill="#8a7d6a"/><path d="M60 151L64 143H72L76 151M80 151L84 142H92L96 151" fill="#8a7d6a"/></g>
   ${bamboo(10,66,250,3)}${bamboo(23,90,250,2.2)}${bamboo(90,72,250,2.8)}${bamboo(78,100,250,2)}
   <path d="M0 226C20 214 40 224 62 218S90 216 100 224V250H0Z" fill="#a0bf8f"/>
   <ellipse cx="36" cy="236" rx="10" ry="8" fill="#252b28"/><ellipse cx="64" cy="236" rx="10" ry="8" fill="#252b28"/>
   <ellipse cx="50" cy="206" rx="26" ry="28" fill="#fbfaf2"/><ellipse cx="60" cy="212" rx="14" ry="20" fill="#d8d6c8" opacity=".35"/>
   <path d="M24 197C28 183 40 179 50 179S72 183 76 197C68 191 60 189 50 189S32 191 24 197Z" fill="#252b28"/>
   <path d="M26 236L56 182" stroke="#7fae76" stroke-width="3.2" stroke-linecap="round"/><path d="M33 224h4M41 211h4M49 197h4" stroke="#4c7550" stroke-width=".9"/>
   <ellipse cx="27" cy="207" rx="7.5" ry="17" transform="rotate(14 27 207)" fill="#252b28"/><ellipse cx="73" cy="207" rx="7.5" ry="17" transform="rotate(-14 73 207)" fill="#252b28"/>
   <ellipse cx="42" cy="207" rx="4.8" ry="4" fill="#252b28"/><ellipse cx="54" cy="188" rx="4.4" ry="3.6" fill="#252b28"/>
   <ellipse cx="50" cy="164" rx="19" ry="16.5" fill="#fbfaf2"/>
   <circle cx="35" cy="150" r="7" fill="#252b28"/><circle cx="65" cy="150" r="7" fill="#252b28"/>
   <ellipse cx="42" cy="164" rx="4.6" ry="6.2" transform="rotate(20 42 164)" fill="#252b28"/><ellipse cx="58" cy="164" rx="4.6" ry="6.2" transform="rotate(-20 58 164)" fill="#252b28"/>
   <circle cx="42.6" cy="162.4" r="1.3" fill="#fff"/><circle cx="57.4" cy="162.4" r="1.3" fill="#fff"/>
   <ellipse cx="50" cy="171" rx="3.2" ry="2.2" fill="#252b28"/><path d="M46 175Q50 179 54 175" stroke="#252b28" stroke-width="1" fill="none"/>
   <ellipse cx="36" cy="172" rx="3.4" ry="2" fill="#f0a89a" opacity=".3"/><ellipse cx="64" cy="172" rx="3.4" ry="2" fill="#f0a89a" opacity=".3"/>
   ${leaf(55,181,-50,13,'#88b083')}${leaf(55,181,-15,11,'#6f9d72')}${leaf(55,181,-85,10,'#96ba8b')}
  </g>`,
  /* Day 3 — Jiuzhaigou: snow peaks, Five Flower Lake, prayer flags */
  3:`<g filter="url(#bl${d})"><path d="M0 122L16 94 24 102 40 68 54 90 66 72 84 98 100 86V250H0Z" fill="#bcd2e6" opacity=".9"/></g>
  <g filter="url(#wc${d})">
   <path d="M0 152L20 106 34 124 52 76 70 120 84 102 100 134V250H0Z" fill="#90b2d0"/>
   <path d="M52 76L70 120 58 122Z" fill="#6f97b9" opacity=".55"/>
   <path d="M52 76L43 99 48 93 52 103 57 94 62 99Z" fill="#fbfdff"/><path d="M20 106L15 118 19 113 22 120 26 113 29 118Z" fill="#fbfdff"/>
   <path d="M0 178C16 156 34 164 50 152S84 152 100 170V250H0Z" fill="#5f8f72"/>
   ${pine(8,176,.8,'#3f7f70')}${pine(18,172,.9,'#46866f')}${pine(30,168,.8,'#3f7f70')}${pine(70,166,.85,'#46866f')}${pine(82,170,.9,'#3f7f70')}${pine(93,176,.8,'#46866f')}
   ${tree(40,178,.8,'#e3b04a')}${tree(58,176,.75,'#d9873c')}${tree(50,182,.6,'#ebc25c')}
   <path d="M0 198C20 186 44 194 68 188S94 190 100 196V250H0Z" fill="url(#lk${d})"/>
   <ellipse cx="34" cy="216" rx="24" ry="8" fill="#5ec8c4" opacity=".75"/><ellipse cx="72" cy="228" rx="22" ry="7" fill="#3f9db8" opacity=".75"/><ellipse cx="55" cy="206" rx="16" ry="4.5" fill="#b9e08a" opacity=".6"/>
   <path d="M22 202L38 214 50 208 64 220 80 206" stroke="#eaf8f6" stroke-width="1.4" fill="none" opacity=".55"/>
   <path d="M0 198C20 186 44 194 68 188" stroke="#f3f7f1" stroke-width="1.8" fill="none" opacity=".8"/>
   <path d="M10 178Q50 192 90 176" stroke="#7a6a58" stroke-width=".7" fill="none"/>
   ${[.08,.2,.32,.44,.56,.68,.8,.92].map((t,i)=>{const x=(1-t)**2*10+2*(1-t)*t*50+t*t*90,y=(1-t)**2*178+2*(1-t)*t*192+t*t*176;return `<path d="M${(x-2.3).toFixed(1)} ${y.toFixed(1)}L${(x+2.3).toFixed(1)} ${y.toFixed(1)}L${x.toFixed(1)} ${(y+5).toFixed(1)}Z" fill="${['#3a6fb0','#f4f0e6','#c8493c','#4c9a5f','#e6b73c'][i%5]}"/>`}).join('')}
   <path d="M0 240C24 232 58 246 100 236V250H0Z" fill="#6d9a7a"/>${pine(12,236,1.3,'#3b7a66')}${pine(90,238,1.2,'#3b7a66')}
  </g>`,
  /* Day 4 — Dujiangyan Nanqiao covered bridge over the Min River */
  4:`<g filter="url(#bl${d})"><path d="M0 120C18 96 34 104 50 90S84 88 100 108V250H0Z" fill="#c8d8cc" opacity=".9"/></g>
  <g filter="url(#wc${d})">
   <path d="M0 156C20 136 40 146 60 136S88 134 100 148V250H0Z" fill="#a9c4ad"/>
   <path d="M0 178C22 164 46 174 72 166S94 168 100 172V250H0Z" fill="#88ad8f"/>
   ${pine(10,182,.9,'#5f866a')}${pine(20,186,.7,'#6f9474')}${pine(90,180,.9,'#5f866a')}${tree(80,186,.7,'#78a17d')}
   <path d="M0 198C24 192 50 200 76 194S96 196 100 198V250H0Z" fill="url(#rv${d})"/>
   <path d="M10 214q14-3 28 0M52 222q16-3 32 0M20 232q12-3 24 0" stroke="#f1fbfa" stroke-width="1.2" fill="none" opacity=".75"/>
   <rect x="16" y="192" width="6" height="16" fill="#a9a394"/><rect x="36" y="192" width="6" height="16" fill="#a9a394"/><rect x="58" y="192" width="6" height="16" fill="#a9a394"/><rect x="78" y="192" width="6" height="16" fill="#a9a394"/>
   <path d="M12 206v14M30 208v16M52 208v16M70 208v16M88 206v14" stroke="#6f7f7a" stroke-width="1.6" opacity=".22"/>
   <rect x="8" y="189" width="84" height="5" fill="#8a5d43"/>
   <rect x="10" y="176" width="80" height="13" fill="#cfae7e"/>
   <path d="M10 176V189M22 176V189M36 176V189M50 176V189M64 176V189M78 176V189M90 176V189" stroke="#7a4b34" stroke-width="1.6"/>
   <path d="M16 180h6M40 180h6M66 180h6M80 180h6" stroke="#f0d39a" stroke-width="3"/>
   <path d="M5 178Q50 167 95 178L91 181H9Z" fill="#59606a"/>
   ${[22,50,78].map(x=>`<path d="M${x-10} 172Q${x} 158 ${x+10} 172L${x+8} 175H${x-8}Z" fill="#4f565f"/><rect x="${x-6}" y="172" width="12" height="6" fill="#b6875a"/><path d="M${x} 158v-4" stroke="#4f565f" stroke-width="1.2"/>`).join('')}
   <path d="M6 150C4 160 8 170 6 182M12 148C10 160 14 170 12 184M18 150C16 160 20 168 18 180" stroke="#8fb07a" stroke-width="1.2" fill="none"/>
   <path d="M0 240C24 232 58 246 100 236V250H0Z" fill="#7fa585"/>
  </g>`,
  /* Day 5 — Sanxingdui bronze mask */
  5:`<g filter="url(#bl${d})"><path d="M0 126C16 104 30 112 46 98S80 96 100 116V250H0Z" fill="#d7d3c1" opacity=".85"/></g>
  <g filter="url(#wc${d})">
   <path d="M0 176C22 160 46 168 68 158S94 160 100 166V250H0Z" fill="#c8cdb6" opacity=".9"/><path d="M0 214C28 204 60 216 100 208V250H0Z" fill="#cfd0b8"/>
   <circle cx="50" cy="176" r="38" fill="none" stroke="#c9a44f" stroke-width="1.6" opacity=".45"/><circle cx="50" cy="176" r="31" fill="none" stroke="#c9a44f" stroke-width=".8" opacity=".35"/>
   <path d="M39 220L35 232H65L61 220Z" fill="#79a18c"/>
   <path d="M27 181L9 164Q5 162 5 168L6 190Q7 196 12 198L27 200Z" fill="#78a591" stroke="#3e5d4e" stroke-width=".9" stroke-linejoin="round"/><path d="M73 181L91 164Q95 162 95 168L94 190Q93 196 88 198L73 200Z" fill="#78a591" stroke="#3e5d4e" stroke-width=".9" stroke-linejoin="round"/>
   <path d="M10 172L23 186M10 180L23 191M90 172L77 186M90 180L77 191" stroke="#3e5d4e" stroke-width=".7" opacity=".8"/><path d="M9 168Q7 178 9 190M91 168Q93 178 91 190" stroke="#c9a44f" stroke-width=".9" fill="none"/>
   <path d="M47 170V140Q50 130 53 140V170Z" fill="#c9a44f" stroke="#8a6f2f" stroke-width=".8"/><path d="M50 141q-7-5-2-12" stroke="#c9a44f" stroke-width="1.6" fill="none" stroke-linecap="round"/>
   <path d="M26 170H74L72 208Q66 222 50 224Q34 222 28 208Z" fill="url(#bz${d})" stroke="#3e5d4e" stroke-width="1" stroke-linejoin="round"/>
   <path d="M30 181H47M53 181H70" stroke="#2f4a3f" stroke-width="2.2"/>
   <rect x="29" y="184" width="19" height="10" rx="2.2" fill="#a9d0bc" stroke="#3e5d4e" stroke-width=".9"/><rect x="52" y="184" width="19" height="10" rx="2.2" fill="#a9d0bc" stroke="#3e5d4e" stroke-width=".9"/>
   <circle cx="38.5" cy="189" r="4.2" fill="#eef4de" stroke="#3e5d4e" stroke-width=".9"/><circle cx="61.5" cy="189" r="4.2" fill="#eef4de" stroke="#3e5d4e" stroke-width=".9"/><circle cx="38.5" cy="189" r="1.7" fill="#2f4a3f"/><circle cx="61.5" cy="189" r="1.7" fill="#2f4a3f"/>
   <path d="M47 194H53V213L50 217L47 213Z" fill="#7aa892" stroke="#3e5d4e" stroke-width=".8"/>
   <path d="M31 210Q50 219 69 210" stroke="#2f4a3f" stroke-width="1.7" fill="none"/><path d="M33 213Q50 223 67 213" stroke="#c9a44f" stroke-width="1" fill="none"/>
   <path d="M31 201q4 3 8 0M61 201q4 3 8 0" stroke="#3e5d4e" stroke-width=".9" fill="none"/>
   <ellipse cx="36" cy="175" rx="3" ry="1.4" fill="#5f8f7c" opacity=".6"/><ellipse cx="66" cy="204" rx="3.4" ry="1.6" fill="#b8dcc8" opacity=".55"/>
   <rect x="20" y="232" width="60" height="14" rx="2" fill="#cfc9b8"/><path d="M20 239H80" stroke="#b4ae9c" stroke-width=".7"/>
  </g>`,
  /* Day 6 — Tianfu Airport, a plane overhead, the panda heading home */
  6:`<rect x="0" y="60" width="100" height="120" fill="url(#sk${d})"/>
  <g filter="url(#bl${d})"><ellipse cx="26" cy="112" rx="18" ry="5" fill="#fff" opacity=".85"/><ellipse cx="74" cy="132" rx="20" ry="5" fill="#fff" opacity=".8"/></g>
  <g filter="url(#wc${d})">
   <path d="M52 114Q30 128 6 138" stroke="#fff" stroke-width="2.2" opacity=".85" stroke-linecap="round" fill="none"/>
   <g transform="translate(68 104) rotate(-16)"><path d="M-15 0Q-15-3.4-8-3.4H10Q17-3.4 19 0Q17 3.4 10 3.4H-8Q-15 3.4-15 0Z" fill="#fbfbf6" stroke="#8ea6b6" stroke-width=".7"/><path d="M-2 0L-9-11 -4-11 5 0Z" fill="#e8eef0" stroke="#8ea6b6" stroke-width=".6"/><path d="M-13-1L-16-7-12-7-8-1Z" fill="#e0503f"/></g>
   <rect x="84" y="128" width="5" height="44" fill="#d9dfe0" stroke="#9fb0ba" stroke-width=".6"/><path d="M79 128h15l-2 8H81Z" fill="#8fb3c4" stroke="#7d98a6" stroke-width=".6"/>
   <path d="M4 172Q22 150 44 164Q64 176 80 158Q90 152 98 160V188H4Z" fill="#eef1f1" stroke="#9fb0ba" stroke-width=".9"/>
   <path d="M4 172Q22 154 44 166Q64 178 80 162" fill="none" stroke="#c7d3d8" stroke-width="2"/>
   <rect x="8" y="174" width="88" height="14" fill="url(#gs${d})"/><path d="M14 174v14M24 174v14M34 174v14M44 174v14M54 174v14M64 174v14M74 174v14M84 174v14" stroke="#fff" stroke-width=".7" opacity=".85"/>
   <rect x="18" y="180" width="6" height="4" fill="#f6dc9a"/><rect x="40" y="180" width="6" height="4" fill="#f6dc9a"/><rect x="66" y="180" width="6" height="4" fill="#f6dc9a"/>
   <path d="M0 188H100V250H0Z" fill="#dcdccb"/><path d="M30 250L44 190H58L76 250Z" fill="#cfc8b6"/><path d="M34 236H70M38 222H66M42 208H62M52 190V250" stroke="#b7b09e" stroke-width=".7" fill="none"/>
   ${bamboo(8,118,250,2.6)}${bamboo(19,144,250,2.1)}${bamboo(92,122,250,2.6)}
   <g transform="translate(35 202) scale(.62)">${PB}</g>
  </g>`
  };
  return `<svg viewBox="0 0 100 250" preserveAspectRatio="xMidYMax slice" aria-hidden="true">${defs}${A[d]}</svg>`;
}

/* ───── route geometry ───── */
const lerp=(a,b,t)=>({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t});
const seg=(a,b)=>{const ym=(a.y+b.y)/2;return[a,{x:a.x,y:ym},{x:b.x,y:ym},b]};
function bez(s,t){const u=1-t,f=(c)=>u*u*u*s[0][c]+3*u*u*t*s[1][c]+3*u*t*t*s[2][c]+t*t*t*s[3][c];return{x:f('x'),y:f('y')}}
function leftPart(s,t){const a=lerp(s[0],s[1],t),b=lerp(s[1],s[2],t),c=lerp(s[2],s[3],t),d=lerp(a,b,t),e=lerp(b,c,t);return[s[0],a,d,lerp(d,e,t)]}
const P=p=>`${p.x.toFixed(2)} ${p.y.toFixed(2)}`, cub=s=>`C${P(s[1])} ${P(s[2])} ${P(s[3])}`;
function progress(d){
  const n=d.nodes.length,now=chinaNow();
  if(now.iso<d.iso)return{idx:0,st:'future'};
  if(now.iso>d.iso)return{idx:n-1,st:'past'};
  const m=now.h*60+now.m,T=d.nodes.map(x=>hm(x[0]));
  if(m<=T[0])return{idx:0,st:'today'};
  for(let i=0;i<n-1;i++)if(m<T[i+1])return{idx:i+(m-T[i])/(T[i+1]-T[i]),st:'today'};
  return{idx:n-1,st:'today'};
}
const thumbUrl=u=>u.replace(/width=\d+/,'width=160').replace(/w=\d+/,'w=160');
function routeGeom(d){
  const n=d.nodes.length,pr=progress(d);
  const pts=d.nodes.map((_,i)=>({x:i%2?55:45,y:93-i*(86/(n-1))}));
  const segs=pts.slice(0,-1).map((p,i)=>seg(p,pts[i+1]));
  const base='M'+P(pts[0])+segs.map(cub).join('');
  let done='';
  if(pr.st==='past')done=base;
  else if(pr.st==='today'&&pr.idx>0){
    const k=Math.min(Math.floor(pr.idx),n-2),u=pr.idx>=n-1?1:pr.idx-k;
    done='M'+P(pts[0])+segs.slice(0,k).map(cub).join('')+cub(leftPart(segs[k],u));
  }
  const k=Math.min(Math.floor(pr.idx),n-2),u=pr.idx>=n-1?1:pr.idx-k;
  return{n,pr,pts,base,done,target:bez(segs[k],u)};
}
function routeHTML(d,quiet){
  const g=routeGeom(d),{pr,pts,n}=g;
  const nodes=d.nodes.map((nd,i)=>{
    const st=pr.st==='past'?'done':pr.st==='future'?'':(pr.idx>=n-1?'done':i<Math.floor(pr.idx)?'done':i===Math.floor(pr.idx)?'cur':'');
    return `<div class="node ${st}" style="top:${pts[i].y}%;--d:${(i*.07).toFixed(2)}s"><i class="dot" style="left:${pts[i].x}%"></i><div class="card ${i%2?'l':'r'}"><div class="thumb">${icon(nd[3],'sm')}<img src="${thumbUrl(DATA.images[nd[2]])}" alt="" loading="lazy" onerror="this.remove()"></div><div class="t"><small>${nd[0]}</small><b>${nd[1]}</b></div></div></div>`;
  }).join('');
  const start=quiet?g.target:pts[0];
  return `<svg class="line" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path class="base" d="${g.base}"/>${g.done?`<path class="done" d="${g.done}"/>`:''}</svg>${nodes}<div class="panda ${pr.st==='today'?'walk':''}" style="left:${start.x}%;top:${start.y}%">${PANDA}</div>`;
}

/* ───── Home ───── */
function wxIcon(c){
  if(c===null)return `<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="8" fill="#f2a33a"/><g stroke="#f2a33a" stroke-width="2" stroke-linecap="round"><path d="M20 4v5M20 31v5M4 20h5M31 20h5M8.7 8.7l3.5 3.5M27.8 27.8l3.5 3.5M31.3 8.7l-3.5 3.5M12.2 27.8l-3.5 3.5"/></g></svg>`;
  if(c<=1)return wxIcon(null);
  const cloud='<path d="M11 30h17a6 6 0 0 0 .8-11.9A8.5 8.5 0 0 0 12.3 16.6 6.7 6.7 0 0 0 11 30Z" fill="#dfe8ee" stroke="#8ea3b5" stroke-width="1.6"/>';
  if(c>=51)return `<svg viewBox="0 0 40 40">${cloud}<path d="M14 33l-1.5 4M20 33l-1.5 4M26 33l-1.5 4" stroke="#5b9bc4" stroke-width="2" stroke-linecap="round"/></svg>`;
  return `<svg viewBox="0 0 40 40"><circle cx="14" cy="13" r="6" fill="#f2a33a"/>${cloud}</svg>`;
}
function stripHTML(d,i){
  return `<div class="strip" data-i="${i}" role="button" tabindex="0" aria-expanded="false" aria-label="第${d.day}天 ${d.vt} ${d.date}"><div class="cover">${art(d.day)}</div><div class="head"><div class="marker">${marker(d.day)}</div><div class="vt">${d.vt}</div></div><div class="panel"></div></div>`;
}
function renderHome(){
  const hero=DATA.images.panda_portrait.replace(/w=\d+/,'w=1000');
  $('#home').innerHTML=`
   <div class="home-top"><div><div class="greeting" id="greet">${greeting()}</div><div class="home-poem">Good company turns places into beautiful stories.</div></div>
     <div class="wx"><div class="wx-row" id="wxIcon">${wxIcon(wx?wx.code:null)}<span class="wx-temp" id="wxTemp">${wx?Math.round(wx.t)+'°C':'—°C'}</span></div><small>Chengdu · 成都</small></div></div>
   <div class="hero"><img src="${hero}" alt="A giant panda resting on a wooden log" onerror="this.style.display='none'"><div class="hero-copy"><div class="cn1">成都，</div><div class="cn2">刚刚好。</div><div class="en">Chengdu.<br>Just right.</div></div></div>
   <div class="sheet">
     <button class="date-row" onclick="setOpen(currentDay()-1)" aria-label="Open today's route"><span class="cal">${icon('calendar')}</span><span><b>15 - 20 Oct 2026</b><span>Chengdu Family Trip</span></span><span class="chev">${icon('chevron','sm')}</span></button>
     <div class="acc" id="acc">${days.map(stripHTML).join('')}</div>
   </div>`;
  sizeAcc();
}
function sizeAcc(){
  const acc=$('#acc');if(!acc||!acc.clientWidth)return;
  const gap=4,E=9,w=acc.clientWidth,unit=(w-gap*5)/(5+E);
  acc.style.setProperty('--ew',(unit*E).toFixed(1)+'px');
  acc.style.setProperty('--vt',Math.max(13,Math.min(17,Math.round((w-gap*5)/6*.27)))+'px');
}
function fillPanel(i,quiet){
  const d=days[i],p=$$('#acc .panel')[i];
  p.classList.toggle('quiet',!!quiet);
  const heads=Array.from({length:d.day},()=>`<svg viewBox="-10 -10 20 20" aria-hidden="true">${pandaHead(0,0,9.3)}</svg>`).join('');
  p.innerHTML=`<button class="close" aria-label="收起">${icon('close','sm')}</button><div class="p-head"><div class="p-heads" role="img" aria-label="第${d.day}天">${heads}</div><div class="p-title"><b>${d.vt}</b><span>${d.date} · ${d.dow} · ${d.city}</span></div></div><div class="p-note">${d.note}</div><div class="route"><div class="rz">${routeHTML(d,quiet)}</div></div>`;
  if(!quiet){
    const g=routeGeom(d),pd=p.querySelector('.panda');
    setTimeout(()=>{if(openIdx===i&&pd){pd.style.left=g.target.x+'%';pd.style.top=g.target.y+'%'}},520);
  }
}
function setOpen(i){
  const strips=$$('#acc .strip'),acc=$('#acc');if(!acc)return;
  if(i>=0&&i!==openIdx)fillPanel(i,false);
  strips.forEach((s,k)=>{const o=k===i;s.classList.toggle('open',o);s.setAttribute('aria-expanded',String(o))});
  acc.classList.toggle('has-open',i>=0);
  openIdx=i;
}
document.addEventListener('click',e=>{
  const s=e.target.closest('#acc .strip');if(!s)return;
  const i=+s.dataset.i;
  if(i!==openIdx)setOpen(i);
  else if(e.target.closest('.p-head,.close'))setOpen(-1);
});
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'&&openIdx>=0){setOpen(-1);return}
  const s=e.target.closest&&e.target.closest('#acc .strip');
  if(s&&(e.key==='Enter'||e.key===' ')&&+s.dataset.i!==openIdx){e.preventDefault();setOpen(+s.dataset.i)}
});
async function loadWeather(){
  try{
    const r=await fetch('https://api.open-meteo.com/v1/forecast?latitude=30.66&longitude=104.06&current=temperature_2m,weather_code&timezone=Asia%2FShanghai');
    const j=await r.json();wx={t:j.current.temperature_2m,code:j.current.weather_code};
    const t=$('#wxTemp'),ic=$('#wxIcon svg');
    if(t){t.textContent=Math.round(wx.t)+'°C';ic.outerHTML=wxIcon(wx.code)}
  }catch(e){}
}

/* ───── Food ───── */
function renderFood(){
  const cats=['全部','川菜','火锅','小吃','咖啡','甜品'];
  const list=DATA.foods.filter(f=>(foodCategory==='全部'||f[2]===foodCategory)&&f[3]<=foodRadius).map(f=>`<article class="food-card paper-card"><img src="${f[0]}" alt="${esc(f[1])}" loading="lazy" onerror="this.style.visibility='hidden'"><div><h3>${f[1]}</h3><div class="food-meta">${f[2]} · ${f[3]<1?Math.round(f[3]*1000)+' m':f[3]+' km'} · ${f[4]} min walk<br><span class="open-t">${f[5]}</span>　<span class="food-rating">★ ${f[6]}</span></div><div class="platforms">${f[7].map(p=>`<i class="platform">${p}</i>`).join('')}</div></div></article>`).join('');
  $('#food').innerHTML=`<header class="page-head"><button class="round-btn" onclick="showPage('home')" aria-label="Back">${icon('back')}</button><div class="center"><h1>Nearby Food</h1><div class="sub">附近美食</div></div><span></span></header><div class="search-box">${icon('search','sm')}<span>Search nearby · 当前附近</span></div><div class="filter-scroll">${cats.map(c=>`<button class="filter-chip ${c===foodCategory?'active':''}" onclick="foodCategory='${c}';renderFood()">${c}</button>`).join('')}</div><div class="radius-select"><span style="font-size:9px;color:#96978f;padding:3px">范围</span>${[.5,1,2,5].map(r=>`<button class="${r===foodRadius?'active':''}" onclick="foodRadius=${r};renderFood()">${r<1?'500m':r+'km'}</button>`).join('')}</div><div class="food-list">${list||'<div class="ending"><div class="cn">这个范围暂时没有示例餐厅。</div></div>'}</div><div class="ending"><div class="cn">好吃的，不必找得太着急。</div></div>`;
}

/* ───── Explore ───── */
function renderExplore(){
  $('#explore').innerHTML=`<header class="page-head"><button class="round-btn" onclick="showPage('home')" aria-label="Back">${icon('back')}</button><div class="center"><h1>Explore</h1><div class="sub">我现在在这里，附近有什么？</div></div><span></span></header><div class="search-box">${icon('search','sm')}<span>Search places, attractions…</span></div><div class="map-cats"><div class="map-cat">${icon('landmark')}景点</div><div class="map-cat">${icon('food')}美食</div><div class="map-cat">${icon('coffee')}咖啡</div><div class="map-cat">${icon('shopping')}便利店</div><div class="map-cat">${icon('toilet')}洗手间</div><div class="map-cat">${icon('pharmacy')}药房</div><div class="map-cat">${icon('shopping')}购物</div><div class="map-cat">${icon('hotel')}酒店</div></div>
  <div class="map-wrap"><svg viewBox="0 0 460 420" preserveAspectRatio="xMidYMid slice"><rect width="460" height="420" fill="#e8ebe3"/><path d="M-15 80C86 106 112 54 203 77s130 68 282 33M-30 285C77 245 130 297 231 254s147-30 258 4M71-20c4 129 44 174 24 268S83 411 112 470M292-20c-3 104-31 151-8 247s43 154 25 244" stroke="#fff" stroke-width="13" opacity=".78" fill="none"/><path d="M-10 211C89 189 126 158 215 184s168 16 260-35" stroke="#c5dbe1" stroke-width="26" opacity=".75" fill="none"/><g fill="#d3ddce" opacity=".8"><path d="m23 21 88 3 14 63-102 9Z"/><path d="m331 34 107-7 10 75-91 16Z"/><path d="m16 314 101-26 28 111-114 22Z"/><path d="m335 305 110 17-5 92-98-19Z"/></g></svg>
  <div class="map-top-note">${icon('pin','sm')} You are here · 春熙路附近</div><div class="map-you"></div><div class="poi green" style="left:24%;top:34%">${icon('landmark')}</div><div class="poi gold" style="left:73%;top:29%">${icon('coffee')}</div><div class="poi pink" style="left:34%;top:72%">${icon('shopping')}</div><div class="poi blue" style="left:78%;top:68%">${icon('toilet')}</div><div class="poi" style="left:60%;top:61%">${icon('food')}</div></div>`;
}

/* ───── Expenses (kept on this device) ───── */
const expLoad=()=>{try{return JSON.parse(store.get('chengduExpenses')||'[]')}catch(e){return[]}};
const expSave=a=>store.set('chengduExpenses',JSON.stringify(a));
function addExpense(){
  const amt=parseFloat($('#expAmt').value),note=$('#expNote').value.trim();
  if(!(amt>0)){$('#expAmt').focus();return}
  const a=expLoad();a.unshift({id:Date.now(),amt,note:note||expCat,cat:expCat,d:chinaNow().iso.slice(5)});expSave(a);renderExpenses();
}
function delExpense(id){expSave(expLoad().filter(x=>x.id!==id));renderExpenses()}
function renderExpenses(){
  const a=expLoad(),tot=a.reduce((s,x)=>s+x.amt,0),cats=['餐饮','交通','门票','购物','其他'];
  $('#expenses').innerHTML=`<header class="page-head"><button class="round-btn" onclick="showPage('home')" aria-label="Back">${icon('back')}</button><div class="center"><h1>Expenses</h1><div class="sub">旅行开销 · 保存在这台设备</div></div><span></span></header>
   <div class="exp-total paper-card"><small>Total spent · 总支出</small><b>¥ ${tot.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})}</b></div>
   <div class="exp-form paper-card"><div class="filter-scroll" style="margin:0">${cats.map(c=>`<button class="filter-chip ${c===expCat?'active':''}" onclick="expCat='${c}';renderExpenses()">${c}</button>`).join('')}</div><div class="exp-row"><input id="expAmt" class="exp-input amt" inputmode="decimal" placeholder="¥ 0.00"><input id="expNote" class="exp-input" placeholder="备注（可选）"><button class="exp-add" onclick="addExpense()">添加</button></div></div>
   <div class="exp-list">${a.map(x=>`<div class="exp-item paper-card"><div><b>${esc(x.note)}</b><small>${esc(x.cat)} · ${esc(x.d)}</small></div><span class="amt">¥ ${x.amt.toFixed(2)}</span><button onclick="delExpense(${x.id})" aria-label="Delete">${icon('trash','sm')}</button></div>`).join('')||'<div class="ending"><div class="cn">还没有记录，花了就记一笔吧。</div></div>'}</div>`;
}

/* ───── Navigation ───── */
function nav(){
  const items=[['home','Home'],['food','Food'],['explore','Explore'],['expenses','Expenses']],ic={home:'home',food:'food',explore:'compass',expenses:'wallet'};
  $('.bottom-nav').innerHTML=items.map(x=>`<button class="nav-btn" data-page="${x[0]}" onclick="showPage('${x[0]}')"><span data-ic="${x[0]}"></span><span>${x[1]}</span></button>`).join('');
  $$('.nav-btn').forEach(b=>{b.dataset.icon=ic[b.dataset.page]});
}
function showPage(name){
  $$('.page').forEach(p=>p.classList.toggle('active',p.id===name));
  $$('.nav-btn').forEach(b=>{
    const on=b.dataset.page===name;b.classList.toggle('active',on);
    b.firstElementChild.innerHTML=icon(b.dataset.page==='home'&&on?'homeSolid':b.dataset.icon);
  });
  if(name==='home')sizeAcc(); if(name==='food')renderFood(); if(name==='expenses')renderExpenses();
  settleAtTop();
}
function scrollHome(){try{document.scrollingElement.scrollTo({top:0,left:0,behavior:'instant'})}catch(e){}document.documentElement.scrollTop=0;document.body.scrollTop=0;try{window.parent.scrollTo({top:0,left:0,behavior:'instant'})}catch(e){}}
function settleAtTop(){scrollHome();requestAnimationFrame(()=>{scrollHome();requestAnimationFrame(scrollHome)})}

/* ───── Landing ───── */
function landingMessage(){
  const p=phase(),d=currentDay();
  const byDay={1:['终于来啦。今天先慢慢认识成都吧。','At last. Let Chengdu unfold slowly.'],2:['今天会看到很多可爱的家伙哦 ♡','Some very cute friends are waiting.'],3:['九寨沟是今天的主角，慢慢看，慢慢记住。','Today belongs to Jiuzhaigou.'],4:['把山水和小惊喜收进回忆里。','Keep every little wonder.'],5:['最后一个完整的成都日，也要好好玩呀。','One more full Chengdu day.'],6:['回家的路上，也别太想我哦 ♡','Take the memories home.']};
  if(p==='before')return['我在成都等着你哦 ♡',"I'll be waiting for you in Chengdu.",'Before Chengdu'];
  if(p==='after')return['我在成都很想你。下次再回来，好不好？','Come back when Chengdu calls again.','After the journey'];
  const m=byDay[d];return[m[0],m[1],`Day ${d} · ${days[d-1].date}`];
}
function prepareLanding(){
  $('#landingPhoto').src=DATA.landing_image||DATA.images.panda_portrait;$('#landingAvatar').src=DATA.images.panda_portrait.replace(/w=\d+/,'w=200');
  const m=landingMessage();$('#landingBubble').innerHTML=`<div class="cn">${m[0]}</div><div class="en">${m[1]}</div>`;$('#landingPhase').textContent=m[2];
  const last=Number(store.get('chengduLandingAt')||0);
  if(Date.now()-last<3*60*60*1000)$('#landing').classList.add('hidden');
}
function enterApp(){store.set('chengduLandingAt',String(Date.now()));$('#landing').classList.add('hidden');sizeAcc();settleAtTop()}

function fitFrame(){try{if(window.frameElement)window.frameElement.style.height=`${Math.max(640,window.parent.innerHeight||window.innerHeight)}px`}catch(e){}}

/* ───── boot ───── */
prepareLanding();nav();renderHome();renderFood();renderExplore();renderExpenses();showPage('home');fitFrame();loadWeather();
window.addEventListener('resize',()=>{fitFrame();sizeAcc()});
setInterval(()=>{if(openIdx>=0&&$('#home').classList.contains('active'))fillPanel(openIdx,true);const g=$('#greet');if(g)g.textContent=greeting()},60000);
</script>
</body>
</html>'''.replace("__DATA__", PAYLOAD)


FRAME_HEIGHT = 860
if hasattr(st, "iframe"):
    st.iframe(HTML, width="stretch", height=FRAME_HEIGHT)
else:  # older Streamlit versions
    import streamlit.components.v1 as components

    components.html(HTML, height=FRAME_HEIGHT, scrolling=False)
