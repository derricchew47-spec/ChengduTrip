# -*- coding: utf-8 -*-
"""Our Chengdu Story — single-file Streamlit visual prototype.

Run with:
    streamlit run app.py

The visual app is intentionally self-contained in this file. It uses remote,
curated photographs so the file remains practical to copy into GitHub.
"""

from __future__ import annotations

import json
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st


st.set_page_config(
    page_title="Our Chengdu Story",
    page_icon="🐼",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Keep Streamlit's host chrome out of the visual composition.
st.markdown(
    """
    <style>
      html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        margin: 0 !important;
        background: #e9e4d8 !important;
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
    from urllib.parse import quote

    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(filename)}?width={width}"


IMG = {
    # Landing / panda
    "panda_portrait": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?auto=format&fit=crop&w=1600&q=92",
    "panda_bamboo": "https://images.unsplash.com/photo-1508264165352-258a6c1915d1?auto=format&fit=crop&w=1500&q=90",
    # Exact or strongly contextual Sichuan scenes
    "taikoo": commons("Sino-Ocean Taikoo Li Chengdu.jpg"),
    "teahouse": commons("Tea in People's Park - Chengdu, China - DSC05362.jpg"),
    "dujiangyan": commons("都江堰南桥 Dujiangyan Nanqiao Bridge.jpg"),
    "jiuzhai": commons("九寨溝-五花海 Jiuzhaigou Five Flower Lake.jpg"),
    "jiuzhai_alt": commons("5 Flowers Lake (127556467).jpeg"),
    "sanxingdui": commons("Ancient Bronze Mask from Sanxingdui with Protruding Eyes & Ears (9951414745).jpg"),
    "airport": commons("成都天府国际机场 Chengdu Tianfu International Airport 1.jpg"),
    "airport_hall": commons("2025 Chengdu Tianfu Airport 03.jpg"),
    # Food / supporting editorial photography
    "mapo": commons("Authentic Mapo Tofu.jpg", 1200),
    "hotpot": commons("Sichuan-style hotpot.jpg", 1200),
    "snack": commons("Chengdu Zhong Dumpling(Zhong Jiaozi).jpg", 1200),
    "coffee": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1100&q=88",
    "noodles": commons("担担面 Dandan noodles.jpg", 1200),
    "dessert": commons("Brown Sugar Bing Fen.jpg", 1200),
}


DAYS = [
    {
        "day": 1,
        "iso": "2026-10-15",
        "date": "15 Oct",
        "date_cn": "10月15日",
        "weekday": "Thu",
        "city": "Chengdu",
        "hero": IMG["taikoo"],
        "title": "成都初见",
        "hero_en": "Arrive softly. Let the story begin.",
        "weather": "18–24°C · 行程参考",
        "route": [
            ["酒店", "Hotel", "hotel"],
            ["春熙路", "Chunxi Road", "city"],
            ["人民公园", "People's Park", "tea"],
            ["宽窄巷子", "Kuanzhai Alley", "lantern"],
        ],
        "events": [
            ["00:05", "Penang → Shanghai", "槟城 → 上海", "HO1366 · PVG T2", IMG["airport_hall"], True],
            ["05:25", "Shanghai Transit", "上海转机", "Transit only · PVG T2", IMG["coffee"], True],
            ["08:10", "Shanghai → Chengdu", "上海 → 成都", "HO1119 · TFU T2", IMG["airport"], True],
            ["12:00", "Airport → Hotel", "机场前往酒店", "Leave bags · Settle in gently", IMG["airport_hall"], False],
            ["15:00", "Chunxi Road · Taikoo Li", "春熙路 · 太古里", "A first slow city walk", IMG["taikoo"], False],
            ["17:00", "People's Park · Kuanzhai", "人民公园 · 宽窄巷子", "Tea, alleys and evening light", IMG["teahouse"], False],
            ["19:00", "Dinner · Flexible", "晚餐 · 灵活安排", "Search nearby when hungry", IMG["mapo"], False],
        ],
        "ending": "第一天，不用急着认识整座城。",
        "ending_en": "Let Chengdu introduce itself slowly.",
    },
    {
        "day": 2,
        "iso": "2026-10-16",
        "date": "16 Oct",
        "date_cn": "10月16日",
        "weekday": "Fri",
        "city": "Chengdu",
        "hero": IMG["panda_portrait"],
        "title": "熊猫与千年成都",
        "hero_en": "A softer pace, a fuller day.",
        "weather": "16–22°C · 行程参考",
        "route": [
            ["酒店", "Hotel", "hotel"],
            ["熊猫基地", "Panda Base", "panda"],
            ["午餐", "Lunch", "meal"],
            ["都江堰", "Dujiangyan", "bridge"],
        ],
        "events": [
            ["08:00", "Hotel Breakfast", "酒店早餐", "A gentle start", IMG["coffee"], False],
            ["09:00", "Chengdu Panda Base", "成都大熊猫繁育研究基地", "Meet Chengdu's softest residents", IMG["panda_portrait"], False],
            ["12:30", "Lunch · Flexible", "午餐 · 灵活安排", "Search nearby when hungry", IMG["mapo"], False],
            ["14:00", "Dujiangyan", "都江堰", "Ancient water, living history", IMG["dujiangyan"], False],
            ["18:30", "Return to hotel", "返回酒店", "Rest well for tomorrow", IMG["dujiangyan"], False],
        ],
        "ending": "今天见到的可爱，要好好记住。",
        "ending_en": "Keep a little softness from today.",
    },
    {
        "day": 3,
        "iso": "2026-10-17",
        "date": "17 Oct",
        "date_cn": "10月17日",
        "weekday": "Sat",
        "city": "Jiuzhaigou",
        "hero": IMG["jiuzhai"],
        "title": "九寨沟",
        "hero_en": "Nature, held in blue and gold.",
        "weather": "8–17°C · 行程参考",
        "route": [
            ["酒店", "Hotel", "hotel"],
            ["五花海", "Five Flower Lake", "lake"],
            ["午餐", "Lunch", "meal"],
            ["长海", "Long Lake", "mountain"],
        ],
        "events": [
            ["07:00", "Hotel Breakfast", "酒店早餐", "Warm up for a beautiful day", IMG["coffee"], False],
            ["08:00", "Jiuzhaigou Scenic Area", "九寨沟景区", "Explore at your own pace", IMG["jiuzhai"], False],
            ["13:00", "Lunch · Flexible", "午餐 · 灵活安排", "Find something nearby", IMG["noodles"], False],
            ["14:00", "Continue Exploration", "继续游览", "Keep the pace gentle", IMG["jiuzhai_alt"], False],
            ["18:00", "Return to hotel", "返回酒店", "A slow evening together", IMG["jiuzhai"], False],
        ],
        "ending": "山水不说话，却会留在记忆里很久。",
        "ending_en": "Some views stay long after the day ends.",
    },
    {
        "day": 4,
        "iso": "2026-10-18",
        "date": "18 Oct",
        "date_cn": "10月18日",
        "weekday": "Sun",
        "city": "Dujiangyan",
        "hero": IMG["dujiangyan"],
        "title": "熊猫谷 · 都江堰",
        "hero_en": "A little cute, a little ancient.",
        "weather": "15–21°C · 行程参考",
        "route": [
            ["熊猫谷", "Panda Valley", "panda"],
            ["仰天窝", "Yangtianwo", "panda"],
            ["午餐", "Lunch", "meal"],
            ["灌县古城", "Ancient City", "bridge"],
        ],
        "events": [
            ["08:00", "Panda Valley", "熊猫谷", "Meet the sleepy locals", IMG["panda_bamboo"], False],
            ["11:00", "Yangtianwo Square", "仰天窝广场", "Giant panda photo stop", IMG["panda_portrait"], False],
            ["12:30", "Lunch · Flexible", "午餐 · 灵活安排", "Search nearby when hungry", IMG["hotpot"], False],
            ["14:00", "Dujiangyan Ancient City", "都江堰 · 灌县古城", "Bookshop, bridge and blue water", IMG["dujiangyan"], False],
            ["19:00", "Dinner · Flexible", "晚餐 · 灵活安排", "Eat well, rest well", IMG["mapo"], False],
        ],
        "ending": "把山水和小惊喜，一起收进今天。",
        "ending_en": "A day of old water and small wonders.",
    },
    {
        "day": 5,
        "iso": "2026-10-19",
        "date": "19 Oct",
        "date_cn": "10月19日",
        "weekday": "Mon",
        "city": "Chengdu",
        "hero": IMG["sanxingdui"],
        "title": "三星堆与成都夜色",
        "hero_en": "Old stories, new memories.",
        "weather": "17–23°C · 行程参考",
        "route": [
            ["三星堆", "Sanxingdui", "museum"],
            ["东郊记忆", "Eastern Memory", "city"],
            ["玉林路", "Yulin Road", "lantern"],
            ["九眼桥", "Jiuyan Bridge", "bridge"],
        ],
        "events": [
            ["09:00", "Sanxingdui Museum", "三星堆博物馆", "Ancient Shu civilization", IMG["sanxingdui"], False],
            ["12:30", "Lunch · Flexible", "午餐 · 灵活安排", "Nearby food when ready", IMG["noodles"], False],
            ["14:00", "Eastern Suburb Memory", "东郊记忆", "Industrial art district", IMG["taikoo"], False],
            ["17:00", "Yulin Road", "玉林路", "Neighborhood wandering", IMG["teahouse"], False],
            ["20:00", "Anshun · Jiuyan Bridge", "安顺廊桥 · 九眼桥", "A gentle last Chengdu night", IMG["dujiangyan"], False],
        ],
        "ending": "最后一个完整的成都日，也要好好玩。",
        "ending_en": "One more Chengdu night to keep.",
    },
    {
        "day": 6,
        "iso": "2026-10-20",
        "date": "20 Oct",
        "date_cn": "10月20日",
        "weekday": "Tue",
        "city": "Chengdu · Shanghai",
        "hero": IMG["airport"],
        "title": "把成都带回家",
        "hero_en": "Take the memories home.",
        "weather": "Travel day · 行程参考",
        "route": [
            ["酒店", "Hotel", "hotel"],
            ["天府机场", "TFU", "airport"],
            ["上海", "Shanghai", "city"],
            ["槟城", "Penang", "home"],
        ],
        "events": [
            ["08:00", "Hotel → Tianfu Airport", "酒店 → 天府机场", "Leave with a comfortable buffer", IMG["airport_hall"], True],
            ["09:00", "Check-in · Rest", "值机 · 休息", "TFU T2", IMG["airport"], True],
            ["12:30", "Chengdu → Shanghai", "成都 → 上海", "HO1120 · TFU T2 → PVG T2", IMG["airport"], True],
            ["15:15", "Shanghai Transit", "上海转机", "PVG T2 · Transit only", IMG["coffee"], True],
            ["17:30", "Shanghai → Penang", "上海 → 槟城", "HO1365 · Home sweet home", IMG["airport_hall"], True],
        ],
        "ending": "旅程会结束，但这些回忆会一直在。",
        "ending_en": "Trips end. The story stays.",
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


SERVER_NOW = datetime.now(ZoneInfo("Asia/Shanghai")).isoformat()
PAYLOAD = json.dumps(
    {"days": DAYS, "images": IMG, "foods": FOODS, "server_now": SERVER_NOW},
    ensure_ascii=False,
).replace("</", "<\\/")


HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
  <meta name="theme-color" content="#f3eee3">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Ma+Shan+Zheng&family=Noto+Sans+SC:wght@300;400;500;600&family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root{
      --paper:#f5f0e5; --paper-hi:#fbf8f1; --paper-deep:#ece5d6;
      --ink:#16251f; --ink-soft:#586157; --muted:#7e8179;
      --forest:#274f3b; --forest-2:#55745e; --sage:#d8e0d0;
      --sage-pale:#e9ede3; --line:rgba(44,61,51,.13);
      --brown:#80634c; --red:#a05242; --gold:#b78444;
      --serif:"Cormorant Garamond","Noto Serif SC",serif;
      --cn-serif:"Noto Serif SC",serif; --sans:"Noto Sans SC",sans-serif;
      --hand:"Ma Shan Zheng","Noto Serif SC",serif;
      --shadow:0 14px 34px rgba(49,55,45,.075);
      --pad:16px; --radius:24px; --nav-h:74px;
    }
    *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
    html,body{margin:0;min-height:100%;background:#e9e4d8;color:var(--ink);font-family:var(--sans);overscroll-behavior:none}
    body{display:flex;justify-content:center}
    button,input{font:inherit}
    button{color:inherit}
    img{display:block}
    .app-shell{
      width:min(100%,460px); min-height:100dvh; position:relative; overflow:hidden;
      background:
        radial-gradient(circle at 103% 8%,rgba(93,119,86,.11),transparent 23%),
        radial-gradient(circle at -5% 32%,rgba(176,142,91,.08),transparent 24%),
        var(--paper);
      box-shadow:0 0 70px rgba(37,44,36,.14);
    }
    .app-shell:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.18;z-index:99;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 160 160' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.08'/%3E%3C/svg%3E")}
    main{min-height:100dvh}
    .page{display:none;padding:15px var(--pad) calc(var(--nav-h) + 26px);animation:pageIn .38s ease both}
    .page.active{display:block}
    @keyframes pageIn{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
    .serif{font-family:var(--serif)} .cn-serif{font-family:var(--cn-serif)} .hand{font-family:var(--hand)}
    .icon{width:20px;height:20px;display:block;stroke:currentColor;fill:none;stroke-width:1.55;stroke-linecap:round;stroke-linejoin:round}
    .icon.sm{width:16px;height:16px}.icon.lg{width:25px;height:25px}
    .round-btn{width:38px;height:38px;border:1px solid var(--line);border-radius:50%;background:rgba(255,255,255,.58);display:grid;place-items:center;box-shadow:0 3px 12px rgba(43,51,43,.04)}
    .eyebrow{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--forest-2)}
    .section-head{display:flex;align-items:flex-end;justify-content:space-between;margin:22px 2px 10px}
    .section-head h2{font:600 29px/.9 var(--serif);margin:0}
    .section-head small{font:400 10px var(--serif);color:var(--muted);letter-spacing:.2px}
    .paper-card{background:rgba(255,255,255,.62);border:1px solid rgba(74,77,63,.11);box-shadow:0 8px 24px rgba(46,50,42,.045)}

    /* Landing — staged photographic movement, replayed every three hours. */
    #landing{position:fixed;z-index:200;inset:0;margin:auto;width:min(100vw,460px);height:100dvh;overflow:hidden;background:#d9ded2;transition:opacity .7s ease,visibility .7s ease}
    #landing.hidden{opacity:0;visibility:hidden;pointer-events:none}
    .land-scene{position:absolute;inset:0;overflow:hidden;background:#dce2d7}
    .land-scene img{width:100%;height:100%;object-fit:cover;object-position:56% 50%;filter:saturate(.82) contrast(.96) brightness(1.04);animation:landCamera 8.8s cubic-bezier(.2,.72,.2,1) forwards}
    .land-scene:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(248,246,238,.62) 0%,rgba(248,246,238,.05) 32%,rgba(12,27,20,.12) 60%,rgba(12,24,18,.62) 100%)}
    @keyframes landCamera{0%{transform:scale(1.16) translate3d(8%,1%,0)}28%{transform:scale(1.11) translate3d(3%,0,0)}58%{transform:scale(1.06) translate3d(-1%,0,0)}100%{transform:scale(1.02) translate3d(-2%,-1%,0)}}
    .land-bamboo{position:absolute;z-index:2;left:-45px;top:-18px;width:215px;height:330px;opacity:.75;transform-origin:top;animation:sway 4.8s ease-in-out infinite alternate;pointer-events:none}
    @keyframes sway{to{transform:rotate(2.4deg) translateX(3px)}}
    .land-bamboo svg{width:100%;height:100%}
    .land-brand{position:absolute;z-index:3;left:25px;right:25px;top:max(30px,env(safe-area-inset-top));text-align:center;color:#13231c;text-shadow:0 1px 12px rgba(255,255,255,.7);animation:titleReveal 1.2s ease both}
    .land-brand h1{font:600 44px/.88 var(--serif);margin:0;letter-spacing:-1.3px}
    .land-brand p{margin:11px 0 0;font:500 9px var(--sans);letter-spacing:4px}
    .land-brand:after{content:"";display:block;width:28px;height:1px;background:#526358;margin:16px auto}
    @keyframes titleReveal{from{opacity:0;transform:translateY(-9px)}to{opacity:1;transform:none}}
    .land-note{position:absolute;z-index:3;left:28px;right:28px;top:28%;text-align:right;color:#213228;opacity:0;animation:noteIn .9s 2.4s ease forwards}
    .land-note .cn{font:400 21px/1.55 var(--hand);letter-spacing:1px}.land-note .en{font:italic 13px var(--serif);color:#676c63}
    @keyframes noteIn{to{opacity:1;transform:translateY(-6px)}}
    .paw-orbit{position:absolute;z-index:4;right:12%;bottom:34%;width:78px;height:78px;border:1px solid rgba(255,255,255,.66);border-radius:50%;opacity:0;animation:pawWave 1.4s 4.1s ease-in-out forwards}
    .paw-orbit:before,.paw-orbit:after{content:"";position:absolute;border-radius:50%;background:rgba(255,255,255,.76);filter:blur(.2px)}
    .paw-orbit:before{width:20px;height:20px;left:29px;top:31px}.paw-orbit:after{width:10px;height:10px;left:17px;top:20px;box-shadow:15px -7px 0 rgba(255,255,255,.76),29px 0 0 rgba(255,255,255,.76)}
    @keyframes pawWave{0%{opacity:0;transform:rotate(-18deg) scale(.75)}35%{opacity:.9;transform:rotate(13deg) scale(1)}65%{transform:rotate(-9deg)}100%{opacity:0;transform:rotate(8deg)}}
    .land-bubble{position:absolute;z-index:5;right:18px;left:68px;top:43%;padding:15px 18px 14px;border-radius:25px 25px 7px 25px;background:rgba(252,249,241,.93);color:#1e3027;box-shadow:0 13px 36px rgba(23,37,29,.17);opacity:0;transform:translateY(12px) scale(.97);animation:bubbleIn .7s 5.05s cubic-bezier(.2,.8,.2,1) forwards}
    .land-bubble .cn{font:600 15px/1.5 var(--cn-serif)}.land-bubble .en{font:italic 12px/1.35 var(--serif);color:#74776e;margin-top:4px}
    @keyframes bubbleIn{to{opacity:1;transform:none}}
    .land-final{position:absolute;z-index:6;left:14px;right:14px;bottom:max(16px,env(safe-area-inset-bottom));border:1px solid rgba(255,255,255,.42);border-radius:28px;background:rgba(248,245,236,.94);box-shadow:0 20px 50px rgba(13,28,21,.25);padding:15px;opacity:0;transform:translateY(25px);animation:finalIn .8s 6.25s ease forwards}
    @keyframes finalIn{to{opacity:1;transform:none}}
    .land-final-top{display:flex;gap:12px;align-items:center}.land-avatar{width:48px;height:48px;border-radius:50%;object-fit:cover;border:3px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,.1)}
    .land-final h3{font:600 20px/1 var(--serif);margin:0 0 4px}.land-final p{font-size:10px;color:var(--muted);margin:0}
    .enter-btn{width:100%;margin-top:13px;border:0;border-radius:17px;padding:13px 15px;background:var(--forest);color:#fff;display:flex;align-items:center;justify-content:center;gap:9px;font-size:12px;letter-spacing:.3px}
    .land-skip{position:absolute;z-index:9;top:max(18px,env(safe-area-inset-top));right:16px;border:0;background:rgba(255,255,255,.5);backdrop-filter:blur(10px);padding:8px 11px;border-radius:99px;font-size:9px;color:#2d3e35}

    /* Home */
    .home-top{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;margin:5px 2px 14px}
    .greeting{font:600 clamp(29px,8vw,36px)/.95 var(--serif);letter-spacing:-.5px}
    .home-poem{font:400 13px/1.5 var(--hand);color:#765f4c;margin-top:8px}
    .weather-mini{text-align:right;color:var(--ink);min-width:96px}.weather-mini .temp{display:flex;justify-content:flex-end;align-items:center;gap:6px;font:600 24px/1 var(--serif)}.weather-mini small{display:block;margin-top:7px;font-size:9px;color:var(--muted)}
    .hero{height:244px;border-radius:27px;position:relative;overflow:hidden;background:#d8d8cf;box-shadow:var(--shadow);isolation:isolate}
    .hero img{width:100%;height:100%;object-fit:cover;transition:transform .7s ease}.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 38%,rgba(9,25,18,.65) 100%)}
    .hero-copy{position:absolute;z-index:2;left:22px;bottom:21px;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.22)}
    .hero-copy .cn{font:600 26px/1.15 var(--cn-serif);letter-spacing:1px}.hero-copy .en{font:italic 13px/1.4 var(--serif);margin-top:7px}
    .trip-strip{margin-top:14px;border-radius:19px;padding:12px 14px;display:flex;align-items:center;justify-content:space-between}.trip-strip strong{font:600 15px var(--serif)}.trip-strip span{display:block;font-size:9px;color:var(--muted);margin-top:4px}
    .now-next{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
    .moment-card{min-height:116px;border-radius:21px;padding:14px;position:relative;overflow:hidden}.moment-card .label{font:600 9px var(--sans);letter-spacing:1.3px;color:var(--forest-2)}.moment-card h3{font:600 21px/1.05 var(--serif);margin:8px 0 4px}.moment-card p{font-size:10px;line-height:1.5;color:var(--ink-soft);margin:0}
    .quick-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin:15px 0 2px}
    .quick-btn{border:1px solid var(--line);background:rgba(255,255,255,.54);height:76px;border-radius:19px;display:flex;flex-direction:column;gap:3px;align-items:center;justify-content:center;color:#4f5b53}.quick-btn .icon{color:var(--forest);margin-bottom:3px}.quick-btn span{font-size:8px;line-height:1}.quick-btn small{font-size:7px;line-height:1;color:#70766f}
    .day-row{display:flex;gap:7px;overflow:auto;scrollbar-width:none;padding:2px 0 4px}.day-row::-webkit-scrollbar{display:none}
    .day-bookmark{border:1px solid transparent;background:rgba(255,255,255,.57);border-radius:14px;min-width:56px;padding:8px 7px 7px;font:500 10px/1.15 var(--serif);color:#545c55}.day-bookmark span{font:400 8px var(--sans);color:#83867f}.day-bookmark.active{background:var(--forest);color:#fff;box-shadow:0 7px 16px rgba(39,79,59,.16)}.day-bookmark.active span{color:#e8eee9}
    .editorial-quote{margin-top:17px;border-radius:22px;padding:18px;background:linear-gradient(135deg,rgba(255,255,255,.38),rgba(229,222,207,.5));color:#695947;position:relative;overflow:hidden}.editorial-quote .en{font:italic 18px/1.25 var(--serif)}.editorial-quote .cn{font:400 12px var(--cn-serif);margin-top:7px}

    /* Shared page header */
    .page-head{height:50px;display:grid;grid-template-columns:42px 1fr 42px;align-items:center;margin:1px 0 8px}.page-head.today-header{grid-template-columns:72px 1fr 72px}.page-head.today-header>:first-child{justify-self:start}.page-head .center{text-align:center}.page-head h1{font:600 27px/.9 var(--serif);margin:0}.page-head .sub{font-size:9px;color:var(--muted);margin-top:5px}
    .page-hero{height:218px;border-radius:0 0 27px 27px;margin:0 calc(var(--pad) * -1);box-shadow:none}.page-hero .hero-copy{left:25px;bottom:18px}.page-hero .hero-copy .cn{font-size:25px}
    .day-jump{display:flex;justify-content:center;gap:8px;margin:11px 0 0}.day-jump button{width:25px;height:5px;border:0;border-radius:9px;background:#d6d3c8;padding:0}.day-jump button.active{width:45px;background:var(--forest-2)}

    /* Route illustration */
    .route-card{margin-top:13px;border-radius:24px;padding:15px 13px 12px;overflow:hidden}.route-title{display:flex;justify-content:space-between;align-items:flex-start}.route-title h2{font:600 18px/1 var(--cn-serif);margin:0}.route-title small{font:400 8px var(--sans);color:var(--muted)}
    .route-art{height:196px;position:relative;margin-top:5px}.route-art svg.route-line{position:absolute;inset:18px 0 0;width:100%;height:145px;overflow:visible}.route-art .wash{position:absolute;border-radius:50% 48% 15% 18%;background:linear-gradient(160deg,#cbd8c4,#e7ecdf);opacity:.8}.route-art .wash.w1{width:93px;height:48px;left:-26px;bottom:22px}.route-art .wash.w2{width:100px;height:45px;right:-12px;top:26px}.route-art .wash.w3{width:55px;height:30px;left:46%;top:66px;opacity:.43}
    .route-stop{position:absolute;width:86px;text-align:center;z-index:3}.route-stop.s1{left:-7px;top:83px}.route-stop.s2{left:25%;top:117px}.route-stop.s3{left:53%;top:39px}.route-stop.s4{right:-8px;top:88px}
    .route-stop .marker{width:27px;height:27px;border-radius:50%;margin:auto;background:var(--forest-2);border:3px solid var(--paper-hi);display:grid;place-items:center;color:white;font:600 11px var(--sans);box-shadow:0 4px 10px rgba(30,56,40,.18);transition:.3s}.route-stop.current .marker{transform:scale(1.23);background:var(--forest);box-shadow:0 0 0 7px rgba(77,107,84,.15),0 6px 13px rgba(30,56,40,.22)}.route-stop.past{opacity:.48}.route-stop b{display:block;font:600 11px/1.25 var(--cn-serif);margin-top:5px}.route-stop small{font:400 7px var(--sans);color:var(--muted)}
    .route-decoration{position:absolute;color:#647963;opacity:.8}.route-decoration.tree{left:12%;top:35px}.route-decoration.leaf{right:17%;bottom:7px}.route-decoration.panda{right:2%;bottom:27px;color:#2f4337}
    .route-note{text-align:center;font:italic 12px var(--serif);color:#7e6551;margin-top:-4px}

    /* Timeline */
    .timeline{margin:18px 0 0 7px;border-left:1.5px solid #78907b;padding-left:16px}.event{display:grid;grid-template-columns:45px minmax(0,1fr) 76px;gap:9px;align-items:center;min-height:104px;border-bottom:1px solid var(--line);position:relative;padding:9px 0}.event:last-child{border-bottom:0}.event:before{content:"";position:absolute;width:9px;height:9px;border-radius:50%;left:-21.5px;top:48px;background:var(--forest-2);border:2px solid var(--paper)}.event.current:before{width:13px;height:13px;left:-23.5px;top:46px;background:var(--forest);box-shadow:0 0 0 6px rgba(50,91,66,.13)}.event.past{opacity:.48}.event .time{font:600 12px var(--serif);color:#47554c}.event h3{font:600 13px/1.25 var(--cn-serif);margin:0 0 3px}.event .cn{font-size:9px;color:#5f685f}.event .desc{font-size:8px;line-height:1.45;color:var(--muted);margin-top:3px}.event img{width:72px;height:72px;border-radius:15px;object-fit:cover;box-shadow:0 5px 13px rgba(33,43,35,.12)}.time-sensitive{display:inline-flex;align-items:center;gap:4px;margin-top:6px;padding:3px 7px;border-radius:99px;background:#f2e4df;color:#9a5549;font-size:6.5px;letter-spacing:.5px;text-transform:uppercase}
    .ending{margin:20px 0 6px;text-align:center;padding:19px 12px;color:#6d5b49}.ending .cn{font:400 15px var(--cn-serif)}.ending .en{font:italic 12px var(--serif);margin-top:5px;color:#878078}

    /* Food */
    .search-box{border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.58);display:flex;align-items:center;gap:9px;padding:11px 13px;font-size:10px;color:var(--muted)}
    .filter-scroll{display:flex;gap:7px;overflow:auto;scrollbar-width:none;margin:11px 0 13px}.filter-scroll::-webkit-scrollbar{display:none}.filter-chip{border:0;border-radius:99px;background:#eae6dc;padding:7px 11px;white-space:nowrap;font-size:9px;color:#626960}.filter-chip.active{background:var(--forest);color:#fff}.radius-select{display:flex;justify-content:flex-end;gap:5px;margin:-3px 0 10px}.radius-select button{border:0;background:transparent;color:#85877f;font-size:8px;padding:3px}.radius-select button.active{color:var(--forest);font-weight:600;border-bottom:1px solid var(--forest)}
    .food-list{display:grid;gap:9px}.food-card{display:grid;grid-template-columns:104px 1fr;gap:12px;padding:8px;border-radius:19px}.food-card img{width:104px;height:101px;border-radius:15px;object-fit:cover}.food-card h3{font:600 13px/1.3 var(--cn-serif);margin:3px 0 5px}.food-meta{font-size:8px;line-height:1.65;color:var(--muted)}.food-rating{font:600 12px var(--serif);color:var(--gold)}.platforms{display:flex;align-items:center;gap:5px;margin-top:7px}.platform{width:20px;height:17px;border-radius:5px;background:#e4ece3;color:#3c674e;display:grid;place-items:center;font:600 6px var(--sans)}.platform:after{content:"✓";position:absolute;transform:translate(7px,-6px);font-size:6px;color:#4f7c5e}.open{color:#4c7256;font-weight:600}

    /* Explore map */
    .map-cats{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin:10px 0}.map-cat{border:1px solid var(--line);border-radius:15px;background:rgba(255,255,255,.55);padding:9px 2px;text-align:center;font-size:8px;color:#5f675f}.map-cat .icon{margin:0 auto 5px;color:var(--forest)}
    .map-wrap{height:486px;margin:0 calc(var(--pad) * -1);position:relative;overflow:hidden;background:#e5e9df}
    .map-wrap svg.map-art{width:100%;height:100%;display:block}.map-top-note{position:absolute;top:14px;left:50%;transform:translateX(-50%);border-radius:15px;background:rgba(255,255,255,.9);box-shadow:0 8px 22px rgba(37,54,43,.12);padding:10px 13px;font-size:9px;white-space:nowrap;color:#536159}.map-you{position:absolute;left:51%;top:48%;transform:translate(-50%,-50%);width:48px;height:48px;border-radius:50%;background:rgba(47,92,65,.13);display:grid;place-items:center}.map-you:before{content:"";width:16px;height:16px;border-radius:50%;background:var(--forest);border:4px solid white;box-shadow:0 4px 11px rgba(26,61,42,.26)}
    .poi{position:absolute;transform:translate(-50%,-100%);width:28px;height:34px;border-radius:16px 16px 16px 4px;rotate:-45deg;background:#a75a4d;box-shadow:0 5px 10px rgba(46,56,48,.18);display:grid;place-items:center}.poi .icon{rotate:45deg;color:#fff;width:14px}.poi.green{background:#4c7058}.poi.gold{background:#b78343}.poi.pink{background:#ad6c7d}.poi.blue{background:#4f7da3}
    .nearby-sheet{margin:-54px 0 0;position:relative;z-index:4;border-radius:25px 25px 0 0;padding:16px 0 0;background:var(--paper)}.sheet-handle{width:34px;height:3px;border-radius:9px;background:#cbc7bd;margin:0 auto 11px}.highlight-scroll{display:flex;gap:9px;overflow:auto;scrollbar-width:none}.highlight-scroll::-webkit-scrollbar{display:none}.place-card{min-width:164px;border-radius:18px;overflow:hidden;background:rgba(255,255,255,.62);border:1px solid var(--line)}.place-card img{width:100%;height:92px;object-fit:cover}.place-card div{padding:9px}.place-card b{display:block;font:600 12px var(--cn-serif)}.place-card small{font-size:8px;color:var(--muted)}

    /* Trip */
    .trip-cover{height:286px;border-radius:26px;overflow:hidden;position:relative;box-shadow:var(--shadow)}.trip-cover img{width:100%;height:100%;object-fit:cover}.trip-cover:after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 37%,rgba(10,24,17,.74))}.trip-cover .copy{position:absolute;z-index:2;left:20px;bottom:20px;color:#fff}.trip-cover h2{font:600 35px/.9 var(--serif);margin:0}.trip-cover p{font:400 10px/1.55 var(--sans);margin:8px 0 0}.tabs{display:grid;grid-template-columns:repeat(4,1fr);margin-top:9px;border-bottom:1px solid var(--line)}.tab{border:0;background:transparent;padding:10px 3px 9px;font:500 9px var(--sans);color:#81837c;position:relative}.tab.active{color:var(--forest);font-weight:600}.tab.active:after{content:"";position:absolute;height:2px;left:20%;right:20%;bottom:-1px;background:var(--forest);border-radius:9px}.trip-pane{display:none}.trip-pane.active{display:block;animation:pageIn .3s ease}.trip-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:13px 0}.trip-stat{border-radius:17px;padding:13px 6px;text-align:center}.trip-stat .icon{margin:0 auto 5px;color:var(--forest)}.trip-stat b{display:block;font:600 20px var(--serif)}.trip-stat span{font-size:8px;color:var(--muted)}
    .journal-copy{padding:4px 4px 8px}.journal-copy h3{font:600 21px var(--serif);margin:8px 0 7px}.journal-copy p{font:400 11px/1.75 var(--cn-serif);color:#676c65;margin:0}.detail-list{display:grid;gap:7px;margin-top:11px}.detail-row{border-radius:16px;padding:12px 13px;display:grid;grid-template-columns:28px 1fr 16px;align-items:center;gap:9px}.detail-row .icon{color:var(--forest)}.detail-row b{font:600 11px var(--cn-serif)}.detail-row small{display:block;font-size:8px;color:var(--muted);margin-top:3px}
    .hotel-editor{border-radius:20px;padding:15px;margin-top:13px}.hotel-editor label{display:block;font:600 12px var(--cn-serif);margin-bottom:4px}.hotel-editor p{font-size:8px;color:var(--muted);margin:0 0 10px}.hotel-input-row{display:flex;gap:7px}.hotel-input{min-width:0;flex:1;border:1px solid var(--line);background:var(--paper-hi);border-radius:13px;padding:10px 11px;font-size:10px;color:var(--ink);outline:none}.hotel-input:focus{border-color:#77917c;box-shadow:0 0 0 3px rgba(83,119,91,.09)}.save-hotel{border:0;border-radius:13px;background:var(--forest);color:white;padding:0 13px;font-size:9px}.saved-note{height:14px;font-size:8px;color:var(--forest-2);padding:5px 2px 0}
    .itinerary-list{margin-top:13px;display:grid;gap:8px}.itin-day{border-radius:18px;padding:12px 13px;display:grid;grid-template-columns:45px 1fr;gap:10px}.itin-day .num{width:40px;height:40px;border-radius:13px;background:var(--sage-pale);display:grid;place-items:center;font:600 16px var(--serif);color:var(--forest)}.itin-day b{font:600 12px var(--cn-serif)}.itin-day p{font-size:8px;color:var(--muted);margin:4px 0 0;line-height:1.5}.credit-note{margin:18px 3px 0;font-size:7px;line-height:1.6;color:#97968f}.credit-note a{color:inherit}

    /* Memories */
    .memory-feature{border-radius:22px;overflow:hidden;margin:4px 0 11px;position:relative;height:212px}.memory-feature img{width:100%;height:100%;object-fit:cover}.memory-feature:after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 42%,rgba(10,25,18,.66))}.memory-feature .copy{position:absolute;z-index:2;left:17px;right:17px;bottom:15px;color:#fff}.memory-feature h2{font:600 22px var(--serif);margin:0}.memory-feature p{font:400 10px var(--cn-serif);margin:3px 0 0}.memory-summary{display:flex;gap:8px;margin-top:8px;font-size:8px;color:#edf3ed}.memory-summary span{display:flex;gap:4px;align-items:center}.memory-summary .icon{width:12px;height:12px}
    .masonry{columns:2;column-gap:8px}.memory-img{width:100%;margin:0 0 8px;border-radius:15px;break-inside:avoid;object-fit:cover;box-shadow:0 4px 12px rgba(35,45,37,.09);transition:.25s}.memory-img:nth-child(3n+1){height:210px}.memory-img:nth-child(3n+2){height:143px}.memory-img:nth-child(3n){height:175px}
    .add-memory{border:1px dashed rgba(52,79,62,.28);background:rgba(255,255,255,.35);border-radius:18px;padding:17px;text-align:center;color:#6d796f;font-size:9px;margin-top:8px}.add-memory .icon{margin:0 auto 7px;color:var(--forest)}

    /* Navigation */
    .bottom-nav{position:fixed;z-index:80;left:50%;bottom:0;transform:translateX(-50%);width:min(100vw,460px);height:calc(var(--nav-h) + env(safe-area-inset-bottom));padding:7px 10px env(safe-area-inset-bottom);display:grid;grid-template-columns:repeat(5,1fr);background:rgba(249,247,240,.93);backdrop-filter:blur(18px);border-top:1px solid rgba(62,75,65,.12);box-shadow:0 -8px 24px rgba(44,51,44,.035)}.nav-btn{border:0;background:transparent;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;font-size:8px;color:#888d85}.nav-btn .icon{width:19px;height:19px}.nav-btn.active{color:var(--forest);font-weight:600}.nav-btn.active .icon{stroke-width:2}

    @media (min-width:461px){.app-shell{margin:18px 0;border-radius:32px;min-height:calc(100dvh - 36px)}#landing{height:calc(100dvh - 36px);top:18px;border-radius:32px}.bottom-nav{bottom:18px;border-radius:0 0 32px 32px}}
    @media (max-height:780px){.hero{height:218px}.page-hero{height:194px}.route-art{height:180px}.land-brand h1{font-size:39px}.land-final{padding:12px}.land-bubble{top:40%}}
    @media (prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.001ms!important;animation-delay:0ms!important;scroll-behavior:auto!important}}
  </style>
</head>
<body>
<div class="app-shell">
  <div id="landing" aria-label="Our Chengdu Story opening">
    <div class="land-scene"><img id="landingPhoto" alt="A real giant panda in green bamboo"></div>
    <div class="land-bamboo" aria-hidden="true">
      <svg viewBox="0 0 210 330" fill="none"><path d="M21-5c16 91 30 192 47 345M83-10c5 102 13 203 20 344" stroke="#60775f" stroke-width="4" opacity=".62"/><g fill="#748a70" opacity=".75"><path d="M33 48C7 22 3 11 1 2c25 3 43 14 51 33-5 8-11 12-19 13Z"/><path d="M46 85C16 70 7 59 3 50c26-3 46 4 58 20-2 8-7 13-15 15Z"/><path d="M62 141c-31-9-42-18-48-26 25-8 47-5 62 8 0 8-6 14-14 18Z"/><path d="M94 52c22-25 35-30 45-31-7 25-20 41-39 46-7-6-9-10-6-15Z"/><path d="M101 112c28-18 42-20 51-18-13 22-30 34-50 34-5-7-6-12-1-16Z"/><path d="M108 183c29-17 43-18 52-16-14 22-32 32-52 31-5-7-5-12 0-15Z"/></g></svg>
    </div>
    <button class="land-skip" onclick="enterApp()">SKIP</button>
    <div class="land-brand"><h1>Our<br>Chengdu Story</h1><p>A FAMILY JOURNEY</p></div>
    <div class="land-note"><div class="cn">慢一点，<br>和家人在一起。</div><div class="en">Slower steps. Richer memories.</div></div>
    <div class="paw-orbit" aria-hidden="true"></div>
    <div class="land-bubble" id="landingBubble"></div>
    <div class="land-final">
      <div class="land-final-top"><img class="land-avatar" id="landingAvatar" alt="Panda"><div><h3 id="landingPhase">Before Chengdu</h3><p>15–20 October 2026 · Family journey</p></div></div>
      <button class="enter-btn" onclick="enterApp()">开启我们的成都之旅 <span>→</span></button>
    </div>
  </div>

  <main>
    <section id="home" class="page active"></section>
    <section id="today" class="page"></section>
    <section id="food" class="page"></section>
    <section id="explore" class="page"></section>
    <section id="trip" class="page"></section>
    <section id="memories" class="page"></section>
  </main>
  <nav class="bottom-nav" aria-label="Main navigation"></nav>
</div>

<script>
const DATA=__DATA__;
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const days=DATA.days;
let selectedDay=1, foodCategory='全部', foodRadius=5, memoryDay='全部', tripTab='overview';

const ICONS={
 home:'<path d="M3 10.8 10 4l7 6.8v7.1a1.1 1.1 0 0 1-1.1 1.1H4.1A1.1 1.1 0 0 1 3 17.9Z"/><path d="M7.6 19v-5.4h4.8V19"/>',
 calendar:'<rect x="3" y="5" width="14" height="13" rx="2"/><path d="M6 3v4M14 3v4M3 9h14M7 12h.01M10 12h.01M13 12h.01M7 15h.01M10 15h.01"/>',
 compass:'<circle cx="10" cy="10" r="7.5"/><path d="m12.8 7.2-1.7 3.9-3.9 1.7 1.7-3.9Z"/>',
 suitcase:'<rect x="4" y="6" width="12" height="12" rx="2"/><path d="M7 6V4.5A1.5 1.5 0 0 1 8.5 3h3A1.5 1.5 0 0 1 13 4.5V6M8 10v4M12 10v4"/>',
 image:'<rect x="3" y="4" width="14" height="13" rx="2"/><circle cx="7" cy="8" r="1.2"/><path d="m4 15 4-4 2.5 2.4 2-2L16 15"/>',
 food:'<path d="M6 3v6M4 3v4a2 2 0 0 0 4 0V3M6 9v8M13 3v14M13 3c3 2 3 6 0 8"/>',
 cloud:'<path d="M5.2 15.5h9.2a3.6 3.6 0 0 0 .4-7.2A5.2 5.2 0 0 0 5 7.1a4.2 4.2 0 0 0 .2 8.4Z"/>',
 search:'<circle cx="8.7" cy="8.7" r="5.7"/><path d="m13 13 4.5 4.5"/>',
 chevron:'<path d="m8 4 6 6-6 6"/>',
 back:'<path d="m12.5 4-6 6 6 6"/>',
 pin:'<path d="M16 8.5c0 5-6 9-6 9s-6-4-6-9a6 6 0 1 1 12 0Z"/><circle cx="10" cy="8.5" r="2"/>',
 camera:'<path d="M3 7h3l1-2h6l1 2h3v10H3Z"/><circle cx="10" cy="12" r="3"/>',
 people:'<circle cx="7" cy="7" r="3"/><circle cx="14" cy="8" r="2.3"/><path d="M2.5 18c.4-4 2-6 4.5-6s4.1 2 4.5 6M12 13c3-.7 4.7 1 5.4 4"/>',
 heart:'<path d="M17 7.2C17 12 10 17 10 17S3 12 3 7.2C3 3.5 7.7 2.3 10 5c2.3-2.7 7-1.5 7 2.2Z"/>',
 plane:'<path d="m2 12 6-2 3-7 2 .8-1 6.5 4.8 1.9c1.7.7 1 2.5-.5 2.4l-5-.6-3 4-1.5-.6 1.3-4.6-5.6.9Z"/>',
 train:'<rect x="4" y="3" width="12" height="12" rx="3"/><path d="M7 7h6M7 11h.01M13 11h.01M7 15l-2 3M13 15l2 3M7 18h6"/>',
 hotel:'<path d="M3 18V5h9v13M12 9h5v9M6 8h2M6 11h2M6 14h2M15 12h.01M15 15h.01"/>',
 clock:'<circle cx="10" cy="10" r="7.5"/><path d="M10 5.5V10l3 2"/>',
 plus:'<path d="M10 3v14M3 10h14"/>',
 coffee:'<path d="M4 7h10v4a5 5 0 0 1-10 0ZM14 8h1.2a2.3 2.3 0 0 1 0 4.6H14M5 4c1-1 2 1 3 0s2 1 3 0"/>',
 shopping:'<path d="M4 7h12l-1 11H5Z"/><path d="M7 8V6a3 3 0 0 1 6 0v2"/>',
 toilet:'<circle cx="6" cy="4" r="1.5"/><circle cx="14" cy="4" r="1.5"/><path d="M4 8h4v4H7v6H5v-6H4ZM12 8h4l1 5h-2v5h-2v-5h-2Z"/>',
 pharmacy:'<path d="M3 7h14v10H3ZM7 3h6v4M10 9v6M7 12h6"/>',
 landmark:'<path d="M3 18h14M5 18V9h10v9M3 9h14L10 3 3 9ZM8 12h4M8 15h4"/>',
 leaf:'<path d="M17 3C8 3 4 7 4 13c0 2 1 3 3 3 6 0 9-5 10-13Z"/><path d="M4 18c2-5 5-8 10-11"/>'
};
function icon(name,cls=''){return `<svg class="icon ${cls}" viewBox="0 0 20 20" aria-hidden="true">${ICONS[name]||ICONS.leaf}</svg>`}
function esc(s){return String(s??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}

function chinaNow(){
  const parts=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date());
  const o=Object.fromEntries(parts.map(p=>[p.type,p.value]));
  return {iso:`${o.year}-${o.month}-${o.day}`,hour:Number(o.hour),minute:Number(o.minute)};
}
function phase(){
  const n=chinaNow(),start='2026-10-15',end='2026-10-20';
  if(n.iso<start)return 'before'; if(n.iso>end)return 'after'; return n.iso===end?'return':'during';
}
function currentDay(){const n=chinaNow();if(n.iso<'2026-10-15')return 1;if(n.iso>'2026-10-20')return 6;return Math.max(1,Math.min(6,Number(n.iso.slice(-2))-14))}
function greeting(){const h=chinaNow().hour;return h<5?'Still awake,':h<12?'Good morning,':h<18?'Good afternoon,':'Good evening,'}
function landingMessage(){
 const p=phase(),d=currentDay();
 const byDay={1:['终于来啦。今天先慢慢认识成都吧。','At last. Let Chengdu unfold slowly.'],2:['今天会看到很多可爱的家伙哦 ♡','Some very cute friends are waiting.'],3:['九寨沟是今天的主角，慢慢看，慢慢记住。','Today belongs to Jiuzhaigou.'],4:['把山水和小惊喜收进回忆里。','Keep every little wonder.'],5:['最后一个完整的成都日，也要好好玩呀。','One more full Chengdu day.'],6:['回家的路上，也别太想我哦 ♡','Take the memories home.']};
 if(p==='before')return ['我在成都等着你哦 ♡',"I'll be waiting for you in Chengdu.",'Before Chengdu'];
 if(p==='after')return ['我在成都很想你。下次再回来，好不好？','Come back when Chengdu calls again.','After the journey'];
 const m=byDay[d];return [m[0],m[1],`Day ${d} · ${days[d-1].date}`];
}
function tripMoment(){
 const p=phase(),d=days[currentDay()-1];
 if(p==='before')return {now:'Trip begins soon',nowcn:'行李慢慢收，期待慢慢长。',next:'15 Oct',nextcn:'Penang → Shanghai'};
 if(p==='after')return {now:'Story collected',nowcn:'成都还在照片和记忆里。',next:'Someday',nextcn:'See you again, Chengdu'};
 return {now:`Day ${d.day} · ${d.city}`,nowcn:d.title,next:d.events[0][0],nextcn:d.events[0][1]};
}

function prepareLanding(){
 $('#landingPhoto').src=DATA.images.panda_portrait;$('#landingAvatar').src=DATA.images.panda_portrait;
 const m=landingMessage();$('#landingBubble').innerHTML=`<div class="cn">${m[0]}</div><div class="en">${m[1]}</div>`;$('#landingPhase').textContent=m[2];
 const last=Number(localStorage.getItem('chengduLandingAt')||0),threeHours=3*60*60*1000;
 if(Date.now()-last<threeHours)$('#landing').classList.add('hidden');
}
function scrollHome(){
  try{document.scrollingElement.scrollTo({top:0,left:0,behavior:'instant'})}catch(e){}
  document.documentElement.scrollTop=0;document.body.scrollTop=0;
  try{window.parent.scrollTo({top:0,left:0,behavior:'instant'})}catch(e){}
}
function settleAtTop(){scrollHome();requestAnimationFrame(()=>{scrollHome();requestAnimationFrame(scrollHome)})}
function enterApp(){localStorage.setItem('chengduLandingAt',String(Date.now()));$('#landing').classList.add('hidden');settleAtTop()}

function nav(){
 const items=[['home','home','Home'],['today','calendar','Today'],['explore','compass','Explore'],['trip','suitcase','Trip'],['memories','image','Memories']];
 $('.bottom-nav').innerHTML=items.map(x=>`<button class="nav-btn ${x[0]==='home'?'active':''}" data-page="${x[0]}" onclick="showPage('${x[0]}')">${icon(x[1])}<span>${x[2]}</span></button>`).join('');
}
function showPage(name){
 $$('.page').forEach(p=>p.classList.toggle('active',p.id===name));
 $$('.nav-btn').forEach(b=>b.classList.toggle('active',b.dataset.page===name));
 if(name==='today')renderToday(); if(name==='food')renderFood(); if(name==='trip')renderTrip(); if(name==='memories')renderMemories();
  settleAtTop();
}
function selectDay(n,go=true){selectedDay=Math.max(1,Math.min(6,n));renderToday();renderHome();if(go)showPage('today')}

function renderHome(){
 const d=days[currentDay()-1],m=tripMoment();
 const chips=days.map(x=>`<button class="day-bookmark ${x.day===currentDay()?'active':''}" onclick="selectDay(${x.day})">Day ${x.day}<br><span>${x.date}</span></button>`).join('');
 $('#home').innerHTML=`
  <div class="home-top"><div><div class="greeting">${greeting()}</div><div class="home-poem">好好旅行，是让一家人更靠近。</div></div><div class="weather-mini"><div class="temp">${icon('cloud','sm')}<span>—°</span></div><small>实时天气 · 后续接入</small></div></div>
  <div class="hero"><img src="${d.hero}" alt="${esc(d.title)}"><div class="hero-copy"><div class="cn">成都，刚刚好。</div><div class="en">Arrive softly. Let the story begin.</div></div></div>
  <div class="trip-strip paper-card" onclick="showPage('trip')"><div><strong>15–20 Oct 2026</strong><span>Chengdu · A family journey</span></div>${icon('chevron','sm')}</div>
  <div class="now-next"><div class="moment-card paper-card"><div class="label">NOW</div><h3>${m.now}</h3><p>${m.nowcn}</p></div><div class="moment-card paper-card"><div class="label">NEXT</div><h3>${m.next}</h3><p>${m.nextcn}</p></div></div>
  <div class="quick-grid"><button class="quick-btn" onclick="showPage('today')">${icon('calendar','lg')}<span>Today</span><small>今日行程</small></button><button class="quick-btn" onclick="showPage('food')">${icon('food','lg')}<span>Nearby Food</span><small>附近美食</small></button><button class="quick-btn" onclick="showPage('explore')">${icon('compass','lg')}<span>Explore</span><small>探索周边</small></button><button class="quick-btn" onclick="showPage('memories')">${icon('image','lg')}<span>Memories</span><small>旅行相册</small></button></div>
  <div class="section-head"><h2>Our Journey</h2><small>15–20 Oct 2026</small></div><div class="day-row">${chips}</div>
  <div class="editorial-quote"><div class="en">“Not just places, but moments together.”</div><div class="cn">旅行的意义，是和重要的人一起。</div></div>`;
}

function eventState(day,event,index){
 const n=chinaNow();if(n.iso<day.iso)return 'future';if(n.iso>day.iso)return 'past';
 const [h,m]=event[0].split(':').map(Number),nowM=n.hour*60+n.minute,t=h*60+m,next=index<day.events.length-1?day.events[index+1][0].split(':').map(Number):[23,59],nextM=next[0]*60+next[1];
 return nowM<t?'future':nowM<nextM?'current':'past';
}
function routeIndex(day){
 const n=chinaNow();if(n.iso<day.iso)return 0;if(n.iso>day.iso)return 3;const h=n.hour+n.minute/60;return h<10?0:h<13?1:h<17?2:3;
}
function routeIcon(type){const map={hotel:'hotel',city:'shopping',tea:'coffee',meal:'food',airport:'plane',museum:'landmark',home:'home',bridge:'landmark',lake:'leaf',mountain:'leaf',lantern:'leaf',panda:'heart'};return icon(map[type]||'leaf','sm')}
function renderToday(){
 const d=days[selectedDay-1],ri=routeIndex(d);
 const stops=d.route.map((s,i)=>`<div class="route-stop s${i+1} ${i<ri?'past':''} ${i===ri?'current':''}"><div class="marker">${i+1}</div><b>${s[0]}</b><small>${s[1]}</small></div>`).join('');
 const events=d.events.map((e,i)=>{const state=eventState(d,e,i);return `<article class="event ${state}"><div class="time">${e[0]}</div><div><h3>${e[1]}</h3><div class="cn">${e[2]}</div><div class="desc">${e[3]}</div>${e[5]?`<span class="time-sensitive">${icon('clock','sm')}Time sensitive</span>`:''}</div><img src="${e[4]}" alt="${esc(e[1])}" loading="lazy"></article>`}).join('');
 const dots=days.map(x=>`<button aria-label="Day ${x.day}" class="${x.day===selectedDay?'active':''}" onclick="selectDay(${x.day},false)"></button>`).join('');
 $('#today').innerHTML=`
   <header class="page-head today-header"><button class="round-btn" onclick="selectDay(${selectedDay-1},false)">${icon('back')}</button><div class="center"><h1>Today</h1><div class="sub">${d.date_cn} · ${d.weekday}</div></div><div class="center"><div style="display:flex;justify-content:center">${icon('cloud','sm')}</div><div class="sub">${d.weather}</div></div></header>
   <div class="hero page-hero"><img src="${d.hero}" alt="${esc(d.title)}"><div class="hero-copy"><div class="cn">${d.title}</div><div class="en">${d.hero_en}</div></div></div><div class="day-jump">${dots}</div>
   <section class="route-card paper-card"><div class="route-title"><h2>Today's Route　今日路线</h2><small>4 stops · gentle pace</small></div><div class="route-art"><div class="wash w1"></div><div class="wash w2"></div><div class="wash w3"></div><svg class="route-line" viewBox="0 0 390 150" fill="none"><path d="M32 82C96 52 151 112 209 76S316 56 361 96" stroke="#82977f" stroke-width="3" stroke-linecap="round" stroke-dasharray="5 7"/><path d="M13 127c22-27 43-28 68 0M299 25c23-22 47-22 70 1" stroke="#bccab5" stroke-width="2" opacity=".75"/></svg>${stops}<div class="route-decoration tree">${icon('leaf','lg')}</div><div class="route-decoration leaf">${icon('leaf')}</div><div class="route-decoration panda">${icon('heart','lg')}</div></div><div class="route-note">Good food. Good company. That’s the day. ♡</div></section>
   <section class="timeline">${events}</section><div class="ending"><div class="cn">${d.ending}</div><div class="en">${d.ending_en}</div></div>`;
}

function renderFood(){
 const cats=['全部','川菜','火锅','小吃','面','咖啡','甜品','更多'];
 const filtered=DATA.foods.filter(f=>(foodCategory==='全部'||foodCategory==='更多'||f[2]===foodCategory)&&f[3]<=foodRadius);
 const list=filtered.map(f=>`<article class="food-card paper-card"><img src="${f[0]}" alt="${esc(f[1])}" loading="lazy"><div><h3>${f[1]}</h3><div class="food-meta">${f[2]} · ${f[3]<1?Math.round(f[3]*1000)+' m':f[3]+' km'} · ${f[4]} min walk<br><span class="open">${f[5]}</span>　<span class="food-rating">★ ${f[6]}</span></div><div class="platforms">${f[7].map(p=>`<i class="platform">${p}</i>`).join('')}</div></div></article>`).join('');
 $('#food').innerHTML=`<header class="page-head"><button class="round-btn" onclick="showPage('home')">${icon('back')}</button><div class="center"><h1>Nearby Food</h1><div class="sub">附近美食</div></div><button class="round-btn">${icon('search')}</button></header><div class="search-box">${icon('search','sm')}<span>Search nearby · 当前附近</span></div><div class="filter-scroll">${cats.map(c=>`<button class="filter-chip ${c===foodCategory?'active':''}" onclick="foodCategory='${c}';renderFood()">${c}</button>`).join('')}</div><div class="radius-select"><span style="font-size:8px;color:#96978f;padding:3px">范围</span>${[.5,1,2,5].map(r=>`<button class="${r===foodRadius?'active':''}" onclick="foodRadius=${r};renderFood()">${r<1?'500m':r+'km'}</button>`).join('')}</div><div class="food-list">${list||'<div class="ending"><div class="cn">这个范围暂时没有示例餐厅。</div></div>'}</div><div class="ending"><div class="cn">好吃的，不必找得太着急。</div><div class="en">Ratings stay visible; trust signals stay quiet.</div></div>`;
}

function renderExplore(){
 $('#explore').innerHTML=`<header class="page-head"><button class="round-btn" onclick="showPage('home')">${icon('back')}</button><div class="center"><h1>Explore</h1><div class="sub">我现在在这里，附近有什么？</div></div><button class="round-btn">${icon('search')}</button></header><div class="search-box">${icon('search','sm')}<span>Search places, attractions…</span></div><div class="map-cats"><div class="map-cat">${icon('landmark')}景点</div><div class="map-cat">${icon('food')}美食</div><div class="map-cat">${icon('coffee')}咖啡</div><div class="map-cat">${icon('shopping')}便利店</div><div class="map-cat">${icon('toilet')}洗手间</div><div class="map-cat">${icon('pharmacy')}药房</div><div class="map-cat">${icon('shopping')}购物</div><div class="map-cat">${icon('hotel')}酒店</div></div><div class="map-wrap"><svg class="map-art" viewBox="0 0 460 486" xmlns="http://www.w3.org/2000/svg"><rect width="460" height="486" fill="#e8ebe3"/><path d="M-15 80C86 106 112 54 203 77s130 68 282 33M-30 285C77 245 130 297 231 254s147-30 258 4M71-20c4 129 44 174 24 268S83 411 112 510M292-20c-3 104-31 151-8 247s43 154 25 284" stroke="#fff" stroke-width="13" opacity=".78"/><path d="M-10 211C89 189 126 158 215 184s168 16 260-35" stroke="#c5dbe1" stroke-width="26" opacity=".75"/><path d="M-10 211C89 189 126 158 215 184s168 16 260-35" stroke="#f7faf8" stroke-width="2" opacity=".9"/><g fill="#d3ddce" opacity=".8"><path d="m23 21 88 3 14 63-102 9Z"/><path d="m331 34 107-7 10 75-91 16Z"/><path d="m16 344 101-26 28 111-114 22Z"/><path d="m335 325 110 17-5 112-98-19Z"/></g><g stroke="#cbd0c8" stroke-width="2" opacity=".8"><path d="M0 145h460M0 389h460M178 0v486M385 0v486"/><path d="m0 460 460-310M0 20l460 338"/></g></svg><div class="map-top-note">${icon('pin','sm')} You are here · 春熙路附近</div><div class="map-you"></div><div class="poi green" style="left:24%;top:34%">${icon('landmark')}</div><div class="poi gold" style="left:73%;top:29%">${icon('coffee')}</div><div class="poi pink" style="left:34%;top:72%">${icon('shopping')}</div><div class="poi blue" style="left:78%;top:68%">${icon('toilet')}</div><div class="poi" style="left:60%;top:61%">${icon('food')}</div></div><section class="nearby-sheet"><div class="sheet-handle"></div><div class="section-head" style="margin-top:0"><h2>Nearby Highlights</h2><small>demo places</small></div><div class="highlight-scroll"><article class="place-card"><img src="${DATA.images.teahouse}"><div><b>人民公园</b><small>Tea & local life · 1.5 km</small></div></article><article class="place-card"><img src="${DATA.images.taikoo}"><div><b>太古里</b><small>Architecture · 600 m</small></div></article><article class="place-card"><img src="${DATA.images.dujiangyan}"><div><b>成都的夜</b><small>Saved for later</small></div></article></div></section>`;
}

function setTripTab(name){tripTab=name;renderTrip()}
function saveHotel(){const input=$('#hotelInput');localStorage.setItem('chengduHotel',input.value.trim());$('#hotelSaved').textContent=input.value.trim()?'已保存在这台设备 · Saved locally':'已清空酒店资料'}
function renderTrip(){
 const hotel=localStorage.getItem('chengduHotel')||'';
 const overview=`<div class="trip-stats"><div class="trip-stat paper-card">${icon('calendar')}<b>6</b><span>Days · 家庭旅行</span></div><div class="trip-stat paper-card">${icon('people')}<b>2+</b><span>People · 我们</span></div><div class="trip-stat paper-card">${icon('heart')}<b>Many</b><span>Memories · 回忆</span></div></div><div class="journal-copy"><h3>Our Journey · 这趟旅行</h3><p>多一点相处，少一点赶路。好吃的、好看的，还有一路上说过的话，都会慢慢变成我们的故事。</p></div><div class="detail-list"><div class="detail-row paper-card">${icon('plane')}<div><b>Flights · 航班</b><small>Penang → Shanghai → Chengdu</small></div>${icon('chevron','sm')}</div><div class="detail-row paper-card">${icon('train')}<div><b>Transport · 交通</b><small>Time-sensitive details are gently highlighted</small></div>${icon('chevron','sm')}</div></div><div class="hotel-editor paper-card"><label for="hotelInput">Accommodation · 酒店</label><p>酒店尚未确认，可以先在这里记录；内容只保存在当前设备。</p><div class="hotel-input-row"><input id="hotelInput" class="hotel-input" value="${esc(hotel)}" placeholder="输入酒店名称或地址…"><button class="save-hotel" onclick="saveHotel()">保存</button></div><div class="saved-note" id="hotelSaved"></div></div>`;
 const itinerary=`<div class="itinerary-list">${days.map(d=>`<article class="itin-day paper-card" onclick="selectDay(${d.day})"><div class="num">${d.day}</div><div><b>${d.date_cn} · ${d.title}</b><p>${d.route.map(r=>r[0]).join(' · ')}</p></div></article>`).join('')}</div>`;
 const photos=`<div class="masonry" style="margin-top:13px">${[DATA.images.panda_portrait,DATA.images.jiuzhai,DATA.images.dujiangyan,DATA.images.sanxingdui,DATA.images.teahouse,DATA.images.taikoo].map((x,i)=>`<img class="memory-img" src="${x}" alt="Trip highlight ${i+1}" loading="lazy">`).join('')}</div>`;
 const notes=`<div class="editorial-quote" style="margin-top:14px"><div class="en">“Slower steps, richer memories.”</div><div class="cn">想记住的，不只是去了哪里，还有一家人在一起时的样子。</div></div><div class="hotel-editor paper-card"><label>Travel notes · 旅行手记</label><p>文字记录功能会在下一阶段接入；这一版先确认阅读密度和视觉方向。</p></div><div class="credit-note">Photographs are loaded remotely from Wikimedia Commons and Unsplash. Wikimedia images retain their respective CC licences and attribution on the source file pages: JianEn Yu, Culantor Lin, Gary Todd, Daderot, FATIII Aviation and other listed contributors.</div>`;
 const panes={overview,itinerary,photos,notes};
 $('#trip').innerHTML=`<header class="page-head"><button class="round-btn" onclick="showPage('home')">${icon('back')}</button><div class="center"><h1>Trip Overview</h1><div class="sub">旅行概览</div></div><button class="round-btn">${icon('heart')}</button></header><div class="trip-cover"><img src="${DATA.images.dujiangyan}" alt="Chengdu journey"><div class="copy"><h2>Chengdu</h2><p>15–20 Oct 2026<br>Same family. A different view.</p></div></div><div class="tabs">${[['overview','Overview'],['itinerary','Itinerary'],['photos','Photos'],['notes','Notes']].map(t=>`<button class="tab ${tripTab===t[0]?'active':''}" onclick="setTripTab('${t[0]}')">${t[1]}</button>`).join('')}</div><div class="trip-pane active">${panes[tripTab]}</div>`;
}

function renderMemories(){
 const filters=['全部','Day 1','Day 2','Day 3','Day 4','Day 5','Day 6'];
 const all=[DATA.images.panda_portrait,DATA.images.taikoo,DATA.images.jiuzhai,DATA.images.mapo,DATA.images.dujiangyan,DATA.images.teahouse,DATA.images.sanxingdui,DATA.images.hotpot,DATA.images.airport];
 const offset=memoryDay==='全部'?0:Number(memoryDay.split(' ')[1])-1,imgs=memoryDay==='全部'?all:[all[offset%all.length],all[(offset+2)%all.length],all[(offset+4)%all.length],all[(offset+6)%all.length]];
 $('#memories').innerHTML=`<header class="page-head"><button class="round-btn" onclick="showPage('home')">${icon('back')}</button><div class="center"><h1>Memories</h1><div class="sub">旅行相册</div></div><button class="round-btn">${icon('plus')}</button></header><div class="filter-scroll">${filters.map(f=>`<button class="filter-chip ${f===memoryDay?'active':''}" onclick="memoryDay='${f}';renderMemories()">${f}</button>`).join('')}</div><article class="memory-feature"><img src="${DATA.images.panda_portrait}" alt="Panda memory"><div class="copy"><h2>A Little Happiness</h2><p>旅途中的小确幸</p><div class="memory-summary"><span>${icon('camera')}24 Photos</span><span>${icon('pin')}4 Places</span><span>${icon('cloud')}天气后续同步</span></div></div></article><div class="masonry">${imgs.map((x,i)=>`<img class="memory-img" src="${x}" alt="Travel memory ${i+1}" loading="lazy">`).join('')}</div><div class="add-memory">${icon('camera','lg')}Take Photo · Add from Gallery<br><span style="color:#999">相册功能将在下一阶段接入</span></div><div class="ending"><div class="cn">这些瞬间，是我们的故事。</div><div class="en">The moments we keep become the story we share.</div></div>`;
}

function fitFrame(){
 try{if(window.frameElement)window.frameElement.style.height=`${Math.max(720,window.parent.innerHeight||window.innerHeight)}px`}catch(e){}
}
selectedDay=currentDay();prepareLanding();nav();renderHome();renderToday();renderFood();renderExplore();renderTrip();renderMemories();fitFrame();settleAtTop();
window.addEventListener('resize',fitFrame);
</script>
</body>
</html>'''.replace("__DATA__", PAYLOAD)


st.iframe(HTML, width="stretch", height=852)
