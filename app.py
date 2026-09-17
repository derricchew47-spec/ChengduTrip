# -*- coding: utf-8 -*-
"""
Our Chengdu Story — V2
Single-file Streamlit family travel companion.

V2 focus:
- mobile-first UI that closely follows the frozen warm travel-journal preview
- realistic photographic landing (no stick-figure panda)
- Today page: iconic hero image -> cute route overview -> tasteful image timeline
- refined Home / Food / Explore / Trip / Memories
- no external API keys required for this visual V2

Run:
    streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="Our Chengdu Story",
    page_icon="🐼",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Keep Streamlit itself invisible; the app UI is rendered inside one controlled component.
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background:#eee9dd !important;
    }
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
    #MainMenu, footer {display:none !important;}
    .block-container{
        padding:0 !important;
        max-width:100% !important;
    }
    iframe{
        border:0 !important;
        display:block !important;
        margin:0 auto !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

now = datetime.now(ZoneInfo("Asia/Shanghai"))
today_iso = now.strftime("%Y-%m-%d")

# Images are deliberately chosen by day-theme rather than reused randomly.
# They are remote photographs so the single-file build stays easy to deploy.
IMG = {
    "landing_panda": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?auto=format&fit=crop&w=1000&q=90",
    "chengdu_city": "https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1200&q=88",
    "old_street": "https://images.unsplash.com/photo-1528127269322-539801943592?auto=format&fit=crop&w=1200&q=88",
    "temple": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?auto=format&fit=crop&w=1200&q=88",
    "panda": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?auto=format&fit=crop&w=1200&q=90",
    "jiuzhai": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=88",
    "mountain_lake": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=88",
    "museum": "https://images.unsplash.com/photo-1564399579883-451a5d44ec08?auto=format&fit=crop&w=1200&q=88",
    "tea": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=900&q=86",
    "food1": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=88",
    "food2": "https://images.unsplash.com/photo-1569058242253-92a9c755a0ec?auto=format&fit=crop&w=900&q=88",
    "food3": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&w=900&q=88",
    "coffee": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=900&q=86",
    "airport": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=900&q=86",
}

DAYS = [
    {
        "day": 1, "date": "15 Oct", "weekday": "Thu", "city": "Chengdu",
        "hero": IMG["old_street"], "title": "成都初印象", "hero_en": "Arrive softly. Let the story begin.",
        "route": [("春熙路","Chunxi Road"),("太古里","Taikoo Li"),("人民公园","People's Park"),("晚餐","Dinner")],
        "events": [
            ("00:05","Penang → Shanghai","槟城 → 上海","HO1366 · PVG T2",IMG["airport"],1),
            ("05:25","Shanghai Transit","上海转机","Transit only · PVG T2",IMG["coffee"],1),
            ("08:10","Shanghai → Chengdu","上海 → 成都","HO1119 · TFU T2",IMG["airport"],1),
            ("12:00","Airport → Hotel","机场前往酒店","Settle in · Leave bags",IMG["chengdu_city"],0),
            ("15:00","Chunxi Road · Taikoo Li","春熙路 · 太古里","Slow city walk",IMG["old_street"],0),
            ("17:00","People's Park · Kuanzhai Alley","人民公园 · 宽窄巷子","Tea, alleys and evening light",IMG["tea"],0),
            ("19:00","Dinner · Flexible","晚餐 · 自由安排","Search nearby when hungry",IMG["food1"],0),
        ],
    },
    {
        "day": 2, "date": "16 Oct", "weekday": "Fri", "city": "Chengdu",
        "hero": IMG["panda"], "title": "熊猫与千年成都", "hero_en": "A softer pace, a fuller day.",
        "route": [("酒店","Hotel"),("熊猫基地","Panda Base"),("都江堰","Dujiangyan"),("回程","Return")],
        "events": [
            ("08:00","Hotel Breakfast","酒店早餐","慢慢吃，养足精神",IMG["coffee"],0),
            ("09:00","Chengdu Research Base","成都大熊猫繁育研究基地","今天先去看最可爱的成都居民",IMG["panda"],0),
            ("12:30","Lunch · Flexible","午餐 · 灵活安排","Search nearby when hungry",IMG["food1"],0),
            ("14:00","Dujiangyan","都江堰","古老水利工程 · 慢慢走",IMG["temple"],0),
            ("18:30","Return to hotel","返回酒店","Rest well for tomorrow",IMG["old_street"],0),
        ],
    },
    {
        "day": 3, "date": "17 Oct", "weekday": "Sat", "city": "Jiuzhaigou",
        "hero": IMG["mountain_lake"], "title": "九寨沟", "hero_en": "Nature at its most beautiful.",
        "route": [("酒店","Hotel"),("九寨沟","Jiuzhaigou"),("午餐","Lunch"),("回酒店","Return")],
        "events": [
            ("07:00","Hotel Breakfast","酒店早餐","Warm up for a beautiful day",IMG["coffee"],0),
            ("08:00","Jiuzhaigou Scenic Area","九寨沟景区","自由游览 · Explore at your own pace",IMG["mountain_lake"],0),
            ("13:00","Lunch · Flexible","午餐 · 灵活安排","Find something nearby",IMG["food1"],0),
            ("14:00","Continue Exploration","继续游览","Keep the pace gentle",IMG["jiuzhai"],0),
            ("18:00","Return to hotel","返回酒店","A slow evening together",IMG["mountain_lake"],0),
        ],
    },
    {
        "day": 4, "date": "18 Oct", "weekday": "Sun", "city": "Dujiangyan",
        "hero": IMG["panda"], "title": "熊猫谷 · 都江堰", "hero_en": "A little cute, a little ancient.",
        "route": [("熊猫谷","Panda Valley"),("仰天窝","Yangtianwo"),("午餐","Lunch"),("古城","Ancient City")],
        "events": [
            ("08:00","Panda Valley","熊猫谷","Meet the sleepy locals",IMG["panda"],0),
            ("11:00","Yangtianwo Square","仰天窝广场","Giant panda photo stop",IMG["panda"],0),
            ("12:30","Lunch · Flexible","午餐 · 灵活安排","Search nearby when hungry",IMG["food2"],0),
            ("14:00","Dujiangyan Ancient City","都江堰 · 灌县古城","钟书阁 · 南桥 · 夜景",IMG["temple"],0),
            ("19:00","Dinner · Flexible","晚餐 · 灵活安排","Eat well, rest well",IMG["food1"],0),
        ],
    },
    {
        "day": 5, "date": "19 Oct", "weekday": "Mon", "city": "Chengdu",
        "hero": IMG["museum"], "title": "三星堆与成都夜色", "hero_en": "Old stories, new memories.",
        "route": [("三星堆","Sanxingdui"),("东郊记忆","Eastern Memory"),("玉林路","Yulin Road"),("九眼桥","Jiuyan Bridge")],
        "events": [
            ("09:00","Sanxingdui Museum","三星堆博物馆","Ancient Shu civilization",IMG["museum"],0),
            ("12:30","Lunch · Flexible","午餐 · 灵活安排","Nearby food when ready",IMG["food1"],0),
            ("14:00","Eastern Suburb Memory","东郊记忆","Industrial art district",IMG["old_street"],0),
            ("17:00","Yulin Road","玉林路","Neighborhood wandering",IMG["tea"],0),
            ("20:00","Anshun Bridge · Jiuyan Bridge","安顺廊桥 · 九眼桥","A gentle last Chengdu night",IMG["chengdu_city"],0),
        ],
    },
    {
        "day": 6, "date": "20 Oct", "weekday": "Tue", "city": "Chengdu / Shanghai",
        "hero": IMG["airport"], "title": "把成都带回家", "hero_en": "Take the memories home.",
        "route": [("酒店","Hotel"),("天府机场","TFU"),("上海","Shanghai"),("槟城","Penang")],
        "events": [
            ("08:00","Hotel → Tianfu Airport","酒店 → 天府机场","Leave with a comfortable buffer",IMG["airport"],1),
            ("09:00","Check-in · Rest","值机 · 休息","TFU T2",IMG["coffee"],1),
            ("12:30","Chengdu → Shanghai","成都 → 上海","HO1120 · TFU T2 → PVG T2",IMG["airport"],1),
            ("15:15","Shanghai Transit","上海转机","PVG T2 · Transit only",IMG["coffee"],1),
            ("17:30","Shanghai → Penang","上海 → 槟城","HO1365 · Home sweet home",IMG["airport"],1),
        ],
    },
]

# Serialize only simple data for JS.
import json
payload = json.dumps({"days": DAYS, "images": IMG, "today": today_iso}, ensure_ascii=False)

html = r"""
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Noto+Sans+SC:wght@300;400;500;600&family=Noto+Serif+SC:wght@500;600;700&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
<style>
:root{
  --paper:#f7f2e7;
  --paper2:#fbf8f0;
  --ink:#1d2a2d;
  --muted:#72776f;
  --green:#476853;
  --green2:#6f8c73;
  --sage:#dce3d2;
  --sage2:#edf1e6;
  --line:#d8d3c7;
  --red:#a75d4b;
  --gold:#b88445;
  --shadow:0 8px 28px rgba(47,50,43,.08);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;background:#eee9dd;color:var(--ink);font-family:"Noto Sans SC",sans-serif}
body{display:flex;justify-content:center}
#app{
  width:min(100vw,460px);
  min-height:100vh;
  background:
    radial-gradient(circle at 92% 0%,rgba(119,140,111,.12),transparent 22%),
    radial-gradient(circle at 4% 18%,rgba(190,162,112,.08),transparent 22%),
    var(--paper);
  position:relative;
  overflow-x:hidden;
}
.page{display:none;padding:14px 14px 92px;min-height:100vh}
.page.active{display:block}
.serif{font-family:"Cormorant Garamond","Noto Serif SC",serif}
.cnserif{font-family:"Noto Serif SC",serif}
.hand{font-family:"ZCOOL XiaoWei","Noto Serif SC",serif}
.topline{display:flex;align-items:flex-start;justify-content:space-between;margin:6px 3px 12px}
.greeting{font:700 31px/1 "Cormorant Garamond",serif;letter-spacing:.2px}
.poem{font-family:"Noto Serif SC";font-style:italic;font-size:14px;color:#786a59;margin-top:7px}
.weather-mini{text-align:right;padding-top:2px}
.weather-mini .deg{font:600 27px "Cormorant Garamond";white-space:nowrap}
.weather-mini small{color:var(--muted);font-size:10px}
.hero{
  position:relative;height:240px;border-radius:25px;overflow:hidden;background:#ddd;
  box-shadow:var(--shadow);isolation:isolate
}
.hero:after{
  content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,rgba(7,18,16,.64) 100%);
}
.hero img{width:100%;height:100%;object-fit:cover;display:block;transform:scale(1.01)}
.hero-copy{position:absolute;z-index:2;left:22px;bottom:20px;color:#fff;text-shadow:0 1px 7px rgba(0,0,0,.24)}
.hero-copy .cn{font:700 28px/1.12 "Noto Serif SC";letter-spacing:1px}
.hero-copy .en{font:italic 14px/1.4 "Cormorant Garamond";margin-top:7px}
.datebar{
  margin:14px 0 0;padding:12px 15px;border-radius:18px;background:rgba(255,255,255,.52);
  border:1px solid rgba(130,125,111,.14);display:flex;justify-content:space-between;align-items:center
}
.datebar b{font-family:"Noto Serif SC";font-size:14px}
.badge{padding:5px 10px;border-radius:999px;background:var(--green);color:#fff;font-size:10px}
.now-next{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
.mini-card{
  background:rgba(255,255,255,.72);border:1px solid rgba(130,125,111,.15);border-radius:20px;padding:14px;min-height:113px;
  box-shadow:0 4px 14px rgba(57,59,52,.04)
}
.mini-card .lab{font:700 10px "Noto Sans SC";letter-spacing:1px;color:#455b4a}
.mini-card h3{margin:8px 0 3px;font:700 18px/1.15 "Noto Serif SC"}
.mini-card .sub{font-size:11px;line-height:1.45;color:#666}
.quick{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:15px 0 19px}
.quick button{
  appearance:none;border:1px solid rgba(130,125,111,.14);background:rgba(255,255,255,.58);border-radius:18px;height:74px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;font-size:10px;color:#555
}
.quick .ico{font-size:22px}
.section-title{display:flex;align-items:end;justify-content:space-between;margin:8px 2px 10px}
.section-title h2{margin:0;font:700 26px "Cormorant Garamond","Noto Serif SC"}
.section-title span{font-size:10px;color:var(--muted)}
.daychips{display:flex;gap:7px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}
.daychip{min-width:54px;border:0;background:#fff9;border-radius:14px;padding:8px 5px;font-size:10px;color:#6c6c66}
.daychip.active{background:var(--green);color:#fff}
.quote{
  margin-top:18px;padding:18px 18px 20px;border-radius:20px;
  background:linear-gradient(135deg,rgba(255,255,255,.38),rgba(234,229,214,.58));
  font-family:"Noto Serif SC";font-size:13px;color:#665a4d
}
.quote .big{font:italic 18px "Cormorant Garamond";margin-bottom:6px}

/* Today */
.today-head{display:grid;grid-template-columns:36px 1fr 60px;align-items:center;margin:4px 0 10px}
.back{border:0;background:rgba(255,255,255,.6);width:34px;height:34px;border-radius:50%;font-size:20px}
.today-title{text-align:center}.today-title h1{margin:0;font:700 25px "Cormorant Garamond"}.today-title div{font-size:11px}
.today-temp{text-align:right;font-size:12px;color:#556}
.today-hero{height:210px;border-radius:0 0 24px 24px;margin:0 -14px 0;box-shadow:none}
.today-hero .hero-copy{left:24px;bottom:16px}
.today-hero .hero-copy .cn{font-size:26px}
.route-card{
  background:rgba(255,255,255,.72);border:1px solid rgba(130,125,111,.15);border-radius:22px;padding:14px 14px 12px;
  margin-top:11px;box-shadow:0 5px 16px rgba(51,53,47,.04)
}
.route-top{display:flex;justify-content:space-between;align-items:center}
.route-top h3{margin:0;font:700 17px "Noto Serif SC"}
.route-top small{font-size:9px;color:#777}
.route-art{position:relative;height:178px;margin-top:6px;overflow:hidden}
.route-art:before{
  content:"";position:absolute;left:8%;right:7%;top:41%;height:42%;
  border-top:4px dashed #82927d;border-radius:48% 52% 54% 46%;transform:rotate(4deg);opacity:.9
}
.route-art .hill{position:absolute;width:85px;height:38px;border-radius:50% 50% 12% 12%;background:linear-gradient(#cdd9c6,#eaf0e1);filter:blur(.1px)}
.route-art .hill.h1{left:-9px;bottom:8px}.route-art .hill.h2{right:4px;top:23px;width:92px}
.stop{position:absolute;display:flex;flex-direction:column;align-items:center;width:80px;text-align:center;z-index:2}
.stop .n{width:26px;height:26px;border-radius:50%;background:var(--green);border:3px solid #f8f5ec;color:#fff;font:bold 12px/20px sans-serif;box-shadow:0 3px 8px #0002}
.stop b{font:600 12px "Noto Serif SC";margin-top:3px}.stop small{font-size:8px;color:#777}
.stop.current .n{transform:scale(1.26);box-shadow:0 0 0 6px rgba(112,140,115,.18),0 5px 13px #0003}
.stop.s1{left:0;top:72px}.stop.s2{left:28%;top:110px}.stop.s3{left:56%;top:41px}.stop.s4{right:0;top:84px}
.route-mascot{position:absolute;right:15px;bottom:5px;font-size:36px;transform:rotate(-5deg)}
.route-note{text-align:center;font:italic 13px "Cormorant Garamond";color:#746558;margin-top:-4px}
.timeline{margin:18px 0 0 3px;border-left:2px solid #80927d;padding-left:14px}
.event{display:grid;grid-template-columns:54px 1fr 68px;gap:10px;align-items:center;min-height:96px;border-bottom:1px solid rgba(120,118,107,.16);position:relative}
.event:before{content:"";position:absolute;width:9px;height:9px;border-radius:50%;background:#526f5a;left:-19px;top:41px;border:2px solid var(--paper)}
.event.current:before{width:13px;height:13px;left:-21px;top:39px;box-shadow:0 0 0 5px rgba(83,111,90,.13)}
.event .time{font:600 13px "Cormorant Garamond";color:#4d514b}
.event h4{margin:0 0 3px;font:700 13px/1.35 "Noto Serif SC"}
.event .cn{font-size:10px;color:#686b64}
.event .desc{font-size:9px;color:#7b7b75;margin-top:2px;line-height:1.4}
.event img{width:66px;height:66px;object-fit:cover;border-radius:14px;box-shadow:0 4px 10px rgba(0,0,0,.08)}
.event .urgent{display:inline-block;margin-top:5px;background:#f4e4df;color:#a25546;border-radius:99px;font-size:7px;padding:3px 7px;letter-spacing:.3px}

/* Food */
.page-head{display:flex;align-items:center;justify-content:space-between;margin:4px 2px 11px}
.page-head h1{margin:0;font:700 25px "Cormorant Garamond","Noto Serif SC";text-align:center}
.search{background:rgba(255,255,255,.65);border:1px solid #ded8cb;border-radius:15px;padding:11px 13px;color:#888;font-size:11px}
.filters{display:flex;gap:7px;overflow-x:auto;margin:11px 0 13px;scrollbar-width:none}
.filter{white-space:nowrap;border:0;background:#f1ede3;padding:7px 11px;border-radius:99px;font-size:10px;color:#6d6b66}
.filter.active{background:var(--green);color:#fff}
.food-card{display:grid;grid-template-columns:88px 1fr;gap:12px;background:rgba(255,255,255,.64);border:1px solid rgba(120,118,107,.13);border-radius:18px;padding:8px;margin-bottom:9px}
.food-card img{width:88px;height:88px;border-radius:14px;object-fit:cover}
.food-card h3{font:700 13px "Noto Serif SC";margin:3px 0}
.food-card .meta{font-size:9px;color:#777;line-height:1.7}
.rating{color:#b87c25;font-weight:600;font-size:11px}
.platforms{display:flex;gap:5px;margin-top:7px}
.platforms i{font-style:normal;width:18px;height:18px;border-radius:6px;background:#e9eee8;color:#42634e;display:grid;place-items:center;font-size:9px;font-weight:700}
.platforms i.warn{background:#f3ece0;color:#b07c43}

/* Explore */
.mapbox{height:520px;margin:0 -14px;background:
 linear-gradient(rgba(241,242,235,.20),rgba(241,242,235,.20)),
 url('https://tile.openstreetmap.org/12/3241/1698.png') center/cover;
 position:relative;border-top:1px solid #ddd;border-bottom:1px solid #ddd;overflow:hidden}
.mapbox:before{
 content:"";position:absolute;inset:0;background:
 linear-gradient(90deg,transparent 49%,rgba(255,255,255,.38) 50%,transparent 51%),
 linear-gradient(transparent 49%,rgba(255,255,255,.32) 50%,transparent 51%);
 background-size:100px 100px;opacity:.55
}
.pin{position:absolute;transform:translate(-50%,-100%);font-size:24px;filter:drop-shadow(0 2px 3px #0003)}
.pin.you{font-size:34px}
.mapcats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:12px 0}
.cat{background:#fff8;border-radius:16px;padding:10px 2px;text-align:center;font-size:9px;border:1px solid #ddd8ca}
.cat b{display:block;font-size:18px;margin-bottom:4px}

/* Trip */
.trip-cover{height:280px;border-radius:24px;position:relative;overflow:hidden;margin-top:8px;box-shadow:var(--shadow)}
.trip-cover img{width:100%;height:100%;object-fit:cover}
.trip-cover:after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 45%,rgba(9,20,18,.76))}
.trip-cover .txt{position:absolute;left:20px;bottom:20px;color:#fff;z-index:2}
.trip-cover .txt h2{margin:0;font:700 30px "Cormorant Garamond"}.trip-cover .txt p{margin:5px 0 0;font-size:11px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin:12px 0}
.stat{background:#fff9;border-radius:16px;padding:13px;text-align:center;border:1px solid #e2ddd2}
.stat b{display:block;font:700 22px "Cormorant Garamond"}.stat span{font-size:9px;color:#777}
.highlight-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}
.highlight-grid img{width:100%;aspect-ratio:1;border-radius:12px;object-fit:cover}

/* Memories */
.memory-top{background:#fff8;border-radius:18px;padding:14px;margin-bottom:10px;border:1px solid #ded8cc}
.memory-top h3{font:700 18px "Noto Serif SC";margin:0 0 6px}
.memory-top .meta{font-size:10px;color:#777;display:flex;gap:12px}
.masonry{columns:2;column-gap:8px}
.masonry img{width:100%;margin:0 0 8px;border-radius:14px;break-inside:avoid;box-shadow:0 3px 10px #0001}

/* Bottom nav */
.nav{
  position:fixed;z-index:30;bottom:0;left:50%;transform:translateX(-50%);
  width:min(100vw,460px);height:72px;padding:8px 12px max(8px,env(safe-area-inset-bottom));
  background:rgba(250,248,241,.94);backdrop-filter:blur(16px);border-top:1px solid rgba(115,112,101,.14);
  display:grid;grid-template-columns:repeat(5,1fr)
}
.nav button{border:0;background:transparent;color:#7a8077;font-size:9px;display:flex;flex-direction:column;gap:4px;align-items:center;justify-content:center}
.nav button b{font-size:18px;font-weight:400}
.nav button.active{color:#355943;font-weight:600}

/* Landing */
#landing{
 position:fixed;z-index:100;inset:0;margin:auto;width:min(100vw,460px);height:100vh;overflow:hidden;background:#0d1914;color:white;
 transition:opacity .65s ease,visibility .65s
}
#landing.hide{opacity:0;visibility:hidden}
.land-photo{position:absolute;inset:0}
.land-photo img{
 width:100%;height:100%;object-fit:cover;object-position:center 48%;
 animation:cinematic 4.2s ease-out forwards;
}
.land-photo:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,14,11,.07),rgba(5,14,11,.10) 38%,rgba(5,14,11,.78) 100%)}
@keyframes cinematic{0%{transform:scale(1.10) translateX(-3%)}55%{transform:scale(1.03) translateX(0)}100%{transform:scale(1.00)}}
.land-top{position:absolute;z-index:2;top:22px;left:20px;right:20px;display:flex;justify-content:space-between;font-size:10px;letter-spacing:.3px}
.land-title{position:absolute;z-index:2;left:25px;bottom:142px}
.land-title h1{font:600 51px/.88 "Cormorant Garamond";margin:0;max-width:270px}
.land-title .cap{font-size:10px;letter-spacing:4px;margin-top:17px}
.bubble{
 position:absolute;z-index:3;right:18px;top:26%;max-width:215px;background:rgba(250,247,239,.94);color:#2b342d;
 padding:13px 15px;border-radius:20px 20px 5px 20px;font:500 13px/1.45 "Noto Serif SC";
 box-shadow:0 10px 28px rgba(0,0,0,.16);opacity:0;transform:translateY(10px);
 animation:bubbleIn .55s 2.35s ease forwards
}
.bubble small{display:block;color:#777;margin-top:4px;font:italic 11px "Cormorant Garamond"}
@keyframes bubbleIn{to{opacity:1;transform:none}}
.land-cta{position:absolute;z-index:2;left:25px;right:25px;bottom:35px;display:flex;align-items:center;justify-content:space-between}
.land-cta .line{height:2px;flex:1;background:rgba(255,255,255,.65);margin-right:18px}
.land-cta button{width:52px;height:52px;border-radius:50%;border:1px solid #ffffff55;background:#ffffff20;color:#fff;font-size:24px;backdrop-filter:blur(8px)}
.skip{border:0;background:transparent;color:#fff;font-size:10px}

/* Fine tune for short mobile */
@media (max-height:760px){
  .hero{height:220px}.today-hero{height:190px}.route-art{height:155px}
}
</style>
</head>
<body>
<div id="app">

<div id="landing">
  <div class="land-photo"><img src="__LANDING__" alt="realistic panda"/></div>
  <div class="land-top"><span>Sichuan, China</span><button class="skip" onclick="enterApp()">Skip</button></div>
  <div class="bubble" id="landBubble">我在成都等着你哦 ♡<small>I'll be waiting for you in Chengdu.</small></div>
  <div class="land-title">
    <h1>Our<br>Chengdu<br>Story</h1>
    <div class="cap">A FAMILY JOURNEY · 15–20 OCT 2026</div>
  </div>
  <div class="land-cta"><div class="line"></div><button onclick="enterApp()">→</button></div>
</div>

<section id="home" class="page active"></section>
<section id="today" class="page"></section>
<section id="food" class="page"></section>
<section id="explore" class="page"></section>
<section id="trip" class="page"></section>
<section id="memories" class="page"></section>

<nav class="nav">
  <button data-page="home" class="active"><b>⌂</b>Home</button>
  <button data-page="today"><b>▣</b>Today</button>
  <button data-page="explore"><b>◎</b>Explore</button>
  <button data-page="trip"><b>♧</b>Trip</button>
  <button data-page="memories"><b>▧</b>Memories</button>
</nav>
</div>

<script>
const DATA = __DATA__;
const days = DATA.days;
let selectedDay = 1;

function enterApp(){ document.getElementById('landing').classList.add('hide'); localStorage.setItem('chengduSeen','1');}
if(localStorage.getItem('chengduSeen')==='1'){setTimeout(()=>document.getElementById('landing').classList.add('hide'),160);}

function page(name){
  document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));
  document.getElementById(name).classList.add('active');
  document.querySelectorAll('.nav button').forEach(b=>b.classList.toggle('active', b.dataset.page===name));
  window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.nav button').forEach(b=>b.onclick=()=>page(b.dataset.page));

function currentDayByDate(){
  const t = new Date();
  const mo=t.getMonth()+1, d=t.getDate();
  if(mo===10 && d>=15 && d<=20) return d-14;
  if(mo<10 || (mo===10&&d<15)) return 1;
  return 6;
}
selectedDay=currentDayByDate();

function eventState(day,event){
  const now = new Date();
  const targetDate = new Date(`2026-10-${String(14+day.day).padStart(2,'0')}T${event[0]}:00+08:00`);
  const next = new Date(targetDate.getTime()+90*60000);
  if(now<targetDate) return 'future';
  if(now<=next) return 'current';
  return 'past';
}
function routeCurrentIndex(day){
  const now = new Date(), tripdate=new Date(`2026-10-${String(14+day.day).padStart(2,'0')}T00:00:00+08:00`);
  if(now.toDateString()!==tripdate.toDateString()) return Math.min(1,day.route.length-1);
  const hour=now.getHours()+now.getMinutes()/60;
  if(hour<10)return 0;if(hour<13)return 1;if(hour<17)return 2;return 3;
}
function tripPhaseText(){
  const now=new Date(), start=new Date('2026-10-15T00:00:00+08:00'), end=new Date('2026-10-21T00:00:00+08:00');
  if(now<start) return ['Trip begins soon','行李慢慢收，期待慢慢长。'];
  if(now>=end) return ['See you again, Chengdu','成都还在这里，等下一次回来。'];
  return ['Enjoy today','慢慢走，今天也会有好故事。'];
}
function nextEvent(){
  const d=days[selectedDay-1]; return d.events[0];
}
function home(){
 const d=days[Math.max(0,currentDayByDate()-1)];
 const phase=tripPhaseText();
 let chips=days.map(x=>`<button class="daychip ${x.day===d.day?'active':''}" onclick="selectedDay=${x.day};today();page('today')">Day ${x.day}<br><span>${x.date}</span></button>`).join('');
 document.getElementById('home').innerHTML=`
 <div class="topline">
   <div><div class="greeting">Good evening,</div><div class="poem">好好旅行，是让一家人更靠近。</div></div>
   <div class="weather-mini"><div class="deg">☁ 20°C</div><small>Chengdu · Cloudy</small></div>
 </div>
 <div class="hero"><img src="${d.hero}"><div class="hero-copy"><div class="cn">成都，刚刚好。</div><div class="en">Arrive softly. Let the story begin.</div></div></div>
 <div class="datebar"><b>15–20 Oct 2026<br><span style="font-size:10px;font-weight:400;color:#777">Chengdu Family Trip</span></b><span>›</span></div>
 <div class="now-next">
   <div class="mini-card"><div class="lab">NOW</div><h3>${phase[0]}</h3><div class="sub">${phase[1]}</div></div>
   <div class="mini-card"><div class="lab">NEXT</div><h3>00:05</h3><div class="sub">Penang → Shanghai<br>HO1366 · 00:05</div></div>
 </div>
 <div class="quick">
   <button onclick="page('today')"><div class="ico">▣</div>Today 今日行程</button>
   <button onclick="page('food')"><div class="ico">♨</div>Nearby Food</button>
   <button onclick="page('explore')"><div class="ico">◎</div>Explore 探索</button>
   <button onclick="page('memories')"><div class="ico">▧</div>Memories 相册</button>
 </div>
 <div class="section-title"><h2>Our Journey</h2><span>15–20 Oct 2026</span></div>
 <div class="daychips">${chips}</div>
 <div class="quote"><div class="big">“Not just places, but moments together.”</div>旅行的意义，是和重要的人一起。</div>`;
}
function today(){
 const d=days[selectedDay-1], ci=routeCurrentIndex(d);
 let stops=d.route.slice(0,4).map((s,i)=>`<div class="stop s${i+1} ${i===ci?'current':''}"><div class="n">${i+1}</div><b>${s[0]}</b><small>${s[1]}</small></div>`).join('');
 let ev=d.events.map(e=>{
   const st=eventState(d,e), urgent=e[5]?'<span class="urgent">TIME-SENSITIVE</span>':'';
   return `<div class="event ${st==='current'?'current':''}" style="${st==='past'?'opacity:.55':''}">
     <div class="time">${e[0]}</div><div><h4>${e[1]}</h4><div class="cn">${e[2]}</div><div class="desc">${e[3]}</div>${urgent}</div><img src="${e[4]}" loading="lazy"></div>`;
 }).join('');
 document.getElementById('today').innerHTML=`
 <div class="today-head"><button class="back" onclick="selectedDay=Math.max(1,selectedDay-1);today()">‹</button><div class="today-title"><h1>Today</h1><div>${d.date} · ${d.weekday}</div></div><div class="today-temp">☁ 16°C<br><small>12–20°C</small></div></div>
 <div class="hero today-hero"><img src="${d.hero}"><div class="hero-copy"><div class="cn">${d.title}</div><div class="en">${d.hero_en}</div></div></div>
 <div class="route-card">
   <div class="route-top"><h3>Today's Route　今日路线</h3><small>${d.route.length} stops · gentle pace</small></div>
   <div class="route-art"><div class="hill h1"></div><div class="hill h2"></div>${stops}<div class="route-mascot">🐼</div></div>
   <div class="route-note">Good food. Good company. That’s the day. ♡</div>
 </div>
 <div class="timeline">${ev}</div>
 <div class="quote"><div class="big">“今天不用赶，慢慢玩。”</div>Take your time. You’re exactly where you need to be.</div>`;
}
const foods=[
 [DATA.images.food1,'陈麻婆豆腐','川菜 · 450 m · 6 min','4.6','大众点评 / 高德 / 小红书'],
 [DATA.images.food3,'蜀大侠火锅','火锅 · 600 m · 8 min','4.5','大众点评 / 高德'],
 [DATA.images.coffee,'% Arabica 成都太古里','咖啡 · 750 m · 9 min','4.6','高德 / Google'],
 [DATA.images.food2,'建设路小吃街','小吃 · 1.1 km · 14 min','4.4','大众点评 / 高德 / 小红书']
];
function food(){
 let list=foods.map((f,i)=>`<div class="food-card"><img src="${f[0]}"><div><h3>${f[1]}</h3><div class="meta">${f[2]} · Open<br><span class="rating">★ ${f[3]}</span></div><div class="platforms"><i>DP</i><i>高</i><i class="${i===2?'warn':''}">RED</i><i>✓</i></div></div></div>`).join('');
 document.getElementById('food').innerHTML=`
 <div class="page-head"><button class="back" onclick="page('home')">‹</button><h1>附近美食<br><span style="font:400 11px Noto Sans SC">Nearby Food</span></h1><button class="back">⌕</button></div>
 <div class="search">⌕ Search nearby · 当前附近</div>
 <div class="filters"><button class="filter active">全部</button><button class="filter">川菜</button><button class="filter">火锅</button><button class="filter">小吃</button><button class="filter">咖啡</button><button class="filter">更多</button></div>
 ${list}
 <div class="quote">平台验证只做轻量提示；详细评分逻辑留在后台，不占你的视线。</div>`;
}
function explore(){
 document.getElementById('explore').innerHTML=`
 <div class="page-head"><button class="back" onclick="page('home')">‹</button><h1>探索周边<br><span style="font:400 11px Noto Sans SC">Explore</span></h1><button class="back">⌕</button></div>
 <div class="search">⌕ Search places, attractions…</div>
 <div class="mapcats"><div class="cat"><b>⛩</b>景点</div><div class="cat"><b>♨</b>美食</div><div class="cat"><b>☕</b>咖啡</div><div class="cat"><b>▣</b>便利店</div></div>
 <div class="mapbox"><div class="pin you" style="left:51%;top:45%">●</div><div class="pin" style="left:24%;top:32%">⌖</div><div class="pin" style="left:72%;top:26%">⌖</div><div class="pin" style="left:38%;top:66%">⌖</div><div class="pin" style="left:78%;top:72%">⌖</div></div>
 <div class="quote"><div class="big">“发现更多身边的美好。”</div>到了成都后，这一页再接实时 GPS 与高德附近搜索。</div>`;
}
function trip(){
 document.getElementById('trip').innerHTML=`
 <div class="page-head"><button class="back" onclick="page('home')">‹</button><h1>Trip Overview</h1><button class="back">⋯</button></div>
 <div class="trip-cover"><img src="${DATA.images.mountain_lake}"><div class="txt"><h2>Chengdu, China</h2><p>15–20 Oct 2026<br>Mountains, pandas, good food, and better company.</p></div></div>
 <div class="stats"><div class="stat"><b>6</b><span>Days</span></div><div class="stat"><b>4+</b><span>Key areas</span></div><div class="stat"><b>∞</b><span>Memories</span></div></div>
 <div class="section-title"><h2>Trip Highlights</h2><span>See all</span></div>
 <div class="highlight-grid"><img src="${DATA.images.panda}"><img src="${DATA.images.mountain_lake}"><img src="${DATA.images.temple}"><img src="${DATA.images.museum}"></div>
 <div class="quote"><div class="big">“More time together, less rush.”</div>这趟旅行，不只是抵达目的地，也是一起走过的时间。</div>`;
}
function memories(){
 const imgs=[DATA.images.panda,DATA.images.old_street,DATA.images.mountain_lake,DATA.images.food1,DATA.images.temple,DATA.images.tea,DATA.images.museum,DATA.images.chengdu_city];
 document.getElementById('memories').innerHTML=`
 <div class="page-head"><button class="back" onclick="page('home')">‹</button><h1>旅行相册<br><span style="font:400 11px Noto Sans SC">Memories</span></h1><button class="back">＋</button></div>
 <div class="filters"><button class="filter active">全部 All</button><button class="filter">Day 1</button><button class="filter">Day 2</button><button class="filter">Day 3</button><button class="filter">Day 4</button></div>
 <div class="memory-top"><h3>A Little Happiness</h3><div class="meta"><span>📷 24 Photos</span><span>⌖ 4 Places</span><span>☁ 16°C</span></div></div>
 <div class="masonry">${imgs.map((x,i)=>`<img src="${x}" style="height:${i%3===0?210:150}px;object-fit:cover">`).join('')}</div>
 <div class="quote" style="text-align:center"><div class="big">Collect moments, not things. ♡</div>这些瞬间，是我们的故事。</div>`;
}
home(); today(); food(); explore(); trip(); memories();
</script>
</body>
</html>
"""

html = html.replace("__DATA__", payload).replace("__LANDING__", IMG["landing_panda"])

components.html(html, height=980, scrolling=True)
