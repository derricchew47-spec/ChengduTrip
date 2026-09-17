# -*- coding: utf-8 -*-
"""
Our Chengdu Story — single-file Streamlit family travel companion
===============================================================

Target: Streamlit >= 1.61 (uses inline Components v2 for a one-file app)

Optional keys (set in Streamlit Cloud Secrets OR environment variables):
    AMAP_WEB_KEY          = Web Service API key (live Nearby Food / Explore POIs)
    AMAP_JS_KEY           = Web JS API key (live interactive Explore map)
    AMAP_SECURITY_CODE    = JS API securityJsCode

The app still runs without keys: itinerary, landing animation, Today page,
route overview, Memories, and weather UI remain available; food / explore
show demo/fallback content until AMap is connected.
"""

from __future__ import annotations

import json
import math
import os
from datetime import datetime, date, time
from zoneinfo import ZoneInfo
from urllib.parse import quote

import requests
import streamlit as st


# -----------------------------------------------------------------------------
# App + configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Our Chengdu Story",
    page_icon="🐼",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
      #MainMenu, footer {display:none !important;}
      .block-container {padding:0 !important; max-width:100% !important;}
      [data-testid="stAppViewContainer"] {background:#f4f0e6;}
      iframe {border:0 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

if not hasattr(st.components, "v2"):
    st.error("This single-file build needs Streamlit 1.61 or newer. Please update Streamlit and rerun.")
    st.stop()

TZ = ZoneInfo("Asia/Shanghai")
TRIP_START = date(2026, 10, 15)
TRIP_END = date(2026, 10, 20)


def secret(name: str, default: str = "") -> str:
    """Read from Streamlit Secrets first, then environment, without requiring a secrets file."""
    try:
        val = st.secrets.get(name, None)
        if val:
            return str(val)
    except Exception:
        pass
    return os.getenv(name, default)


AMAP_WEB_KEY = secret("AMAP_WEB_KEY")
AMAP_JS_KEY = secret("AMAP_JS_KEY")
AMAP_SECURITY_CODE = secret("AMAP_SECURITY_CODE")


# -----------------------------------------------------------------------------
# Editable trip data — keep travel content separate from rendering logic
# -----------------------------------------------------------------------------
IMG = {
    "panda": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?auto=format&fit=crop&w=1100&q=82",
    "lake": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1100&q=82",
    "temple": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?auto=format&fit=crop&w=1100&q=82",
    "street": "https://images.unsplash.com/photo-1528127269322-539801943592?auto=format&fit=crop&w=1100&q=82",
    "coffee": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=900&q=82",
    "food": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=82",
    "museum": "https://images.unsplash.com/photo-1564399579883-451a5d44ec08?auto=format&fit=crop&w=900&q=82",
    "city": "https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1100&q=82",
}

# lat/lng are WGS84-ish anchor coordinates for weather / overview only.
# AMap live search uses browser GPS converted to GCJ-02 before query.
DAYS = [
    {
        "day": 1,
        "date": "2026-10-15",
        "weekday": "Thu",
        "city": "Chengdu",
        "lat": 30.5728,
        "lng": 104.0668,
        "hero": IMG["street"],
        "hero_cn": "成都，刚刚好。",
        "hero_en": "Arrive softly. Let the story begin.",
        "route_title": "Arrival · City Walk",
        "events": [
            {"start":"00:05","end":"05:25","title":"Penang → Shanghai","cn":"槟城 → 上海","subtitle":"HO1366 · PVG T2","type":"flight","image":IMG["city"],"time_sensitive":True},
            {"start":"05:25","end":"08:10","title":"Shanghai Transit","cn":"上海转机","subtitle":"Transit only · PVG T2","type":"transit","image":IMG["coffee"],"time_sensitive":True},
            {"start":"08:10","end":"11:25","title":"Shanghai → Chengdu","cn":"上海 → 成都","subtitle":"HO1119 · TFU T2","type":"flight","image":IMG["city"],"time_sensitive":True},
            {"start":"12:00","end":"14:00","title":"Airport → Hotel","cn":"机场前往酒店","subtitle":"Settle in · Leave bags","type":"transfer","image":IMG["street"]},
            {"start":"15:00","end":"17:00","title":"Chunxi Road · Taikoo Li","cn":"春熙路 · 太古里","subtitle":"Slow city walk","type":"place","image":IMG["street"]},
            {"start":"17:00","end":"19:00","title":"People's Park · Kuanzhai Alley","cn":"人民公园 · 宽窄巷子","subtitle":"Tea, alleys and evening light","type":"place","image":IMG["temple"]},
            {"start":"19:00","end":"20:00","title":"Dinner · Flexible","cn":"晚餐 · 自由安排","subtitle":"Search nearby when hungry","type":"meal","image":IMG["food"]},
            {"start":"20:00","end":"21:00","title":"Twin Towers · Optional","cn":"双子塔 · Optional","subtitle":"Only if everyone still has energy","type":"place","image":IMG["city"]},
        ],
    },
    {
        "day": 2,
        "date": "2026-10-16",
        "weekday": "Fri",
        "city": "Chengdu / Jiuzhaigou",
        "lat": 30.5728,
        "lng": 104.0668,
        "hero": IMG["temple"],
        "hero_cn": "慢下来，一起感受成都。",
        "hero_en": "Slower steps, richer memories.",
        "route_title": "Culture · Transfer North",
        "events": [
            {"start":"08:00","end":"09:00","title":"Hotel Breakfast","cn":"酒店早餐","subtitle":"Take it easy","type":"meal","image":IMG["coffee"]},
            {"start":"09:00","end":"10:00","title":"Wenshu Monastery","cn":"文殊院","subtitle":"Morning temple atmosphere","type":"place","image":IMG["temple"]},
            {"start":"10:00","end":"12:00","title":"Wuhou Shrine","cn":"武侯祠","subtitle":"Three Kingdoms history","type":"place","image":IMG["temple"]},
            {"start":"12:00","end":"13:00","title":"Lunch · Flexible","cn":"午餐 · 自由安排","subtitle":"Search nearby when hungry","type":"meal","image":IMG["food"]},
            {"start":"13:00","end":"16:00","title":"Du Fu Thatched Cottage","cn":"杜甫草堂","subtitle":"Gardens · poetry · slow walk","type":"place","image":IMG["street"]},
            {"start":"16:00","end":"19:00","title":"Transfer toward Jiuzhaigou","cn":"前往九寨沟方向","subtitle":"Private transfer · relax on the way","type":"transfer","image":IMG["lake"]},
            {"start":"19:00","end":"20:00","title":"Dinner · Flexible","cn":"晚餐 · 自由安排","subtitle":"Something warm after the ride","type":"meal","image":IMG["food"]},
        ],
    },
    {
        "day": 3,
        "date": "2026-10-17",
        "weekday": "Sat",
        "city": "Jiuzhaigou",
        "lat": 33.2600,
        "lng": 103.9186,
        "hero": IMG["lake"],
        "hero_cn": "九寨沟，是今天的主角。",
        "hero_en": "Slow down to see more.",
        "route_title": "Jiuzhaigou · Full Day",
        "events": [
            {"start":"07:00","end":"08:00","title":"Hotel Breakfast","cn":"酒店早餐","subtitle":"Warm up for a beautiful day","type":"meal","image":IMG["coffee"]},
            {"start":"08:00","end":"13:00","title":"Jiuzhaigou Scenic Area","cn":"九寨沟景区","subtitle":"自由游览 · Explore at your own pace","type":"place","image":IMG["lake"]},
            {"start":"13:00","end":"14:00","title":"Lunch · Flexible","cn":"午餐 · 自由安排","subtitle":"Find something nearby","type":"meal","image":IMG["food"]},
            {"start":"14:00","end":"18:00","title":"Scenic transfer / sightseeing","cn":"沿途游览 · 返回方向","subtitle":"Keep the pace gentle","type":"transfer","image":IMG["lake"]},
            {"start":"19:00","end":"20:00","title":"Dinner · Flexible","cn":"晚餐 · 自由安排","subtitle":"A warm meal together","type":"meal","image":IMG["food"]},
        ],
    },
    {
        "day": 4,
        "date": "2026-10-18",
        "weekday": "Sun",
        "city": "Dujiangyan",
        "lat": 30.9884,
        "lng": 103.6469,
        "hero": IMG["panda"],
        "hero_cn": "今天，看熊猫也看千年水利。",
        "hero_en": "A little cute, a little ancient.",
        "route_title": "Pandas · Dujiangyan",
        "events": [
            {"start":"07:00","end":"08:00","title":"Hotel Breakfast","cn":"酒店早餐","subtitle":"Easy morning","type":"meal","image":IMG["coffee"]},
            {"start":"08:00","end":"10:00","title":"Panda Valley","cn":"熊猫谷","subtitle":"Meet the sleepy locals 🐼","type":"place","image":IMG["panda"]},
            {"start":"11:00","end":"12:00","title":"Yangtianwo Square","cn":"仰天窝广场","subtitle":"Giant panda photo stop","type":"place","image":IMG["panda"]},
            {"start":"12:00","end":"13:00","title":"Lunch · Flexible","cn":"午餐 · 自由安排","subtitle":"Search nearby when hungry","type":"meal","image":IMG["food"]},
            {"start":"14:00","end":"18:00","title":"Dujiangyan Ancient City","cn":"都江堰 · 灌县古城","subtitle":"钟书阁 · 南桥 · 蓝眼泪夜景","type":"place","image":IMG["temple"]},
            {"start":"18:00","end":"19:00","title":"Dinner · Flexible","cn":"晚餐 · 自由安排","subtitle":"Dinner before heading back","type":"meal","image":IMG["food"]},
        ],
    },
    {
        "day": 5,
        "date": "2026-10-19",
        "weekday": "Mon",
        "city": "Chengdu",
        "lat": 30.5728,
        "lng": 104.0668,
        "hero": IMG["museum"],
        "hero_cn": "古蜀、街区与成都夜色。",
        "hero_en": "Old stories, new memories.",
        "route_title": "Sanxingdui · Chengdu Night",
        "events": [
            {"start":"08:00","end":"09:00","title":"Hotel Breakfast","cn":"酒店早餐","subtitle":"Start slowly","type":"meal","image":IMG["coffee"]},
            {"start":"09:00","end":"12:00","title":"Sanxingdui Museum","cn":"三星堆博物馆","subtitle":"Ancient Shu civilization","type":"place","image":IMG["museum"]},
            {"start":"12:00","end":"13:00","title":"Lunch · Flexible","cn":"午餐 · 自由安排","subtitle":"Nearby food when ready","type":"meal","image":IMG["food"]},
            {"start":"14:00","end":"17:00","title":"Eastern Suburb Memory","cn":"东郊记忆","subtitle":"Industrial art district","type":"place","image":IMG["street"]},
            {"start":"17:00","end":"19:00","title":"Yulin Road","cn":"玉林路","subtitle":"Neighborhood wandering","type":"place","image":IMG["street"]},
            {"start":"19:00","end":"20:00","title":"Dinner · Flexible","cn":"晚餐 · 自由安排","subtitle":"Pick what looks good nearby","type":"meal","image":IMG["food"]},
            {"start":"20:00","end":"21:00","title":"Anshun Bridge · Jiuyan Bridge","cn":"安顺廊桥 · 九眼桥","subtitle":"A gentle last Chengdu night","type":"place","image":IMG["city"]},
        ],
    },
    {
        "day": 6,
        "date": "2026-10-20",
        "weekday": "Tue",
        "city": "Chengdu / Shanghai",
        "lat": 30.3120,
        "lng": 104.4410,
        "hero": IMG["city"],
        "hero_cn": "回家的路，也是一段旅程。",
        "hero_en": "Take the memories home.",
        "route_title": "Homeward",
        "events": [
            {"start":"08:00","end":"09:00","title":"Hotel → Tianfu Airport","cn":"酒店 → 天府机场","subtitle":"Leave with a comfortable buffer","type":"transfer","image":IMG["city"],"time_sensitive":True},
            {"start":"09:00","end":"11:00","title":"Check-in · Rest","cn":"值机 · 休息","subtitle":"TFU T2","type":"transit","image":IMG["coffee"],"time_sensitive":True},
            {"start":"12:30","end":"15:15","title":"Chengdu → Shanghai","cn":"成都 → 上海","subtitle":"HO1120 · TFU T2 → PVG T2","type":"flight","image":IMG["city"],"time_sensitive":True},
            {"start":"15:15","end":"17:30","title":"Shanghai Transit","cn":"上海转机","subtitle":"PVG T2 · Transit only","type":"transit","image":IMG["coffee"],"time_sensitive":True},
            {"start":"17:30","end":"23:00","title":"Shanghai → Penang","cn":"上海 → 槟城","subtitle":"HO1365 · Home sweet home","type":"flight","image":IMG["city"],"time_sensitive":True},
        ],
    },
]

LANDING_MESSAGES = {
    "before": {"cn": "我在成都等着你哦 ♡", "en": "I'll be waiting for you in Chengdu."},
    1: {"cn": "今天轻轻落地成都呀，别急着赶路 ♡", "en": "Arrive softly. Let Chengdu say hello."},
    2: {"cn": "今天有古老成都，也有一路向北的小期待。", "en": "Old stories first, new scenery next."},
    3: {"cn": "九寨沟是今天的主角，记得多看几眼哦 ♡", "en": "Today belongs to Jiuzhaigou."},
    4: {"cn": "今天有熊猫、有山水，应该会很可爱。", "en": "Pandas, water and a very good day."},
    5: {"cn": "把三星堆和成都夜色，都装进回忆里吧。", "en": "One more day of stories to keep."},
    6: {"cn": "回家路上别太想我哦，成都记得你来过 ♡", "en": "Take the memories home with you."},
    "after": {"cn": "我在成都很想你。下次再回来，好不好？♡", "en": "Chengdu misses you. Come back someday."},
}


# -----------------------------------------------------------------------------
# Live helpers
# -----------------------------------------------------------------------------
WEATHER_CODES = {
    0:("☀️","Clear"), 1:("🌤️","Mostly clear"), 2:("⛅","Partly cloudy"), 3:("☁️","Cloudy"),
    45:("🌫️","Fog"), 48:("🌫️","Fog"), 51:("🌦️","Drizzle"), 53:("🌦️","Drizzle"), 55:("🌧️","Drizzle"),
    61:("🌦️","Light rain"), 63:("🌧️","Rain"), 65:("🌧️","Heavy rain"), 71:("🌨️","Light snow"),
    73:("🌨️","Snow"), 75:("❄️","Heavy snow"), 80:("🌦️","Showers"), 81:("🌧️","Showers"),
    82:("⛈️","Heavy showers"), 95:("⛈️","Thunderstorm"), 96:("⛈️","Thunderstorm"), 99:("⛈️","Thunderstorm"),
}


@st.cache_data(ttl=600, show_spinner=False)
def get_weather(lat: float, lng: float) -> dict:
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lng,
                "current": "temperature_2m,apparent_temperature,weather_code,precipitation",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
                "timezone": "Asia/Shanghai",
                "forecast_days": 7,
            },
            timeout=7,
        )
        r.raise_for_status()
        j = r.json()
        cur = j.get("current", {})
        daily = j.get("daily", {})
        code = int(cur.get("weather_code", 3) or 3)
        icon, desc = WEATHER_CODES.get(code, ("☁️", "Weather"))
        return {
            "ok": True,
            "temp": round(float(cur.get("temperature_2m", 0))),
            "feels": round(float(cur.get("apparent_temperature", 0))),
            "precip": float(cur.get("precipitation", 0) or 0),
            "icon": icon,
            "desc": desc,
            "high": round(float((daily.get("temperature_2m_max") or [0])[0])),
            "low": round(float((daily.get("temperature_2m_min") or [0])[0])),
            "rain_prob": int(float((daily.get("precipitation_probability_max") or [0])[0] or 0)),
        }
    except Exception:
        return {"ok": False, "temp": 16, "feels": 16, "precip": 0, "icon":"⛅", "desc":"Weather unavailable", "high":20, "low":12, "rain_prob":0}


def _transform_lat(x: float, y: float) -> float:
    ret = -100.0 + 2.0*x + 3.0*y + 0.2*y*y + 0.1*x*y + 0.2*math.sqrt(abs(x))
    ret += (20.0*math.sin(6.0*x*math.pi) + 20.0*math.sin(2.0*x*math.pi))*2.0/3.0
    ret += (20.0*math.sin(y*math.pi) + 40.0*math.sin(y/3.0*math.pi))*2.0/3.0
    ret += (160.0*math.sin(y/12.0*math.pi) + 320*math.sin(y*math.pi/30.0))*2.0/3.0
    return ret


def _transform_lng(x: float, y: float) -> float:
    ret = 300.0 + x + 2.0*y + 0.1*x*x + 0.1*x*y + 0.1*math.sqrt(abs(x))
    ret += (20.0*math.sin(6.0*x*math.pi) + 20.0*math.sin(2.0*x*math.pi))*2.0/3.0
    ret += (20.0*math.sin(x*math.pi) + 40.0*math.sin(x/3.0*math.pi))*2.0/3.0
    ret += (150.0*math.sin(x/12.0*math.pi) + 300.0*math.sin(x/30.0*math.pi))*2.0/3.0
    return ret


def wgs84_to_gcj02(lat: float, lng: float) -> tuple[float, float]:
    # China offset conversion used only so browser GPS aligns with domestic AMap POIs.
    if not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271):
        return lat, lng
    a = 6378245.0
    ee = 0.00669342162296594323
    dlat = _transform_lat(lng - 105.0, lat - 35.0)
    dlng = _transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * math.pi)
    return lat + dlat, lng + dlng


@st.cache_data(ttl=300, show_spinner=False)
def amap_around(lat_gcj: float, lng_gcj: float, radius: int, keyword: str, page_size: int = 12) -> list[dict]:
    if not AMAP_WEB_KEY:
        return []
    try:
        r = requests.get(
            "https://restapi.amap.com/v5/place/around",
            params={
                "key": AMAP_WEB_KEY,
                "location": f"{lng_gcj:.6f},{lat_gcj:.6f}",
                "radius": int(radius),
                "keywords": keyword,
                "show_fields": "business,photos,navi",
                "page_size": min(max(page_size, 1), 25),
                "page_num": 1,
            },
            timeout=8,
        )
        j = r.json()
        if str(j.get("status")) != "1":
            return []
        out = []
        for p in j.get("pois", []) or []:
            biz = p.get("business") or {}
            photos = p.get("photos") or []
            loc = (p.get("location") or "").split(",")
            out.append({
                "id": p.get("id", ""),
                "name": p.get("name", ""),
                "type": p.get("type", ""),
                "address": p.get("address", ""),
                "distance": int(float(p.get("distance", 0) or 0)),
                "lng": float(loc[0]) if len(loc) == 2 else None,
                "lat": float(loc[1]) if len(loc) == 2 else None,
                "rating": biz.get("rating") or "",
                "cost": biz.get("cost") or "",
                "tag": biz.get("tag") or "",
                "open_today": biz.get("opentime_today") or "",
                "photo": (photos[0].get("url") if photos and isinstance(photos[0], dict) else "") or "",
            })
        return out
    except Exception:
        return []


DEMO_FOOD = [
    {"name":"陈麻婆豆腐","type":"川菜","distance":450,"rating":"4.6","cost":"68","open_today":"11:00-22:00","photo":IMG["food"],"lat":30.572,"lng":104.066,"demo":True},
    {"name":"蜀大侠火锅","type":"火锅","distance":600,"rating":"4.5","cost":"110","open_today":"10:00-23:00","photo":IMG["food"],"lat":30.575,"lng":104.068,"demo":True},
    {"name":"明婷饭店","type":"川菜","distance":1100,"rating":"4.4","cost":"75","open_today":"10:30-21:30","photo":IMG["food"],"lat":30.570,"lng":104.071,"demo":True},
    {"name":"建设路小吃街","type":"小吃","distance":1800,"rating":"4.6","cost":"35","open_today":"10:00-23:30","photo":IMG["street"],"lat":30.590,"lng":104.098,"demo":True},
]


# -----------------------------------------------------------------------------
# Determine current / selected day and live backend payload
# -----------------------------------------------------------------------------
now = datetime.now(TZ)
if TRIP_START <= now.date() <= TRIP_END:
    default_day = (now.date() - TRIP_START).days + 1
elif now.date() < TRIP_START:
    default_day = 1
else:
    default_day = 6

state = st.session_state.get("chengdu_story_ui")
getstate = lambda name, default: getattr(state, name, default) if state is not None else default
page = getstate("page", "home") or "home"
selected_day = int(getstate("selected_day", default_day) or default_day)
selected_day = max(1, min(6, selected_day))
radius = int(getstate("radius", 1000) or 1000)
food_category = str(getstate("food_category", "全部") or "全部")
explore_category = str(getstate("explore_category", "景点") or "景点")
location = getstate("location", None)

loc_wgs = None
if isinstance(location, dict) and location.get("lat") is not None and location.get("lng") is not None:
    try:
        loc_wgs = (float(location["lat"]), float(location["lng"]))
    except Exception:
        loc_wgs = None

selected = DAYS[selected_day - 1]
weather = get_weather(selected["lat"], selected["lng"])

food_keyword_map = {"全部":"餐饮", "川菜":"川菜", "火锅":"火锅", "小吃":"小吃", "面":"面馆", "咖啡":"咖啡", "甜品":"甜品"}
explore_keyword_map = {"景点":"景点", "便利店":"便利店", "厕所":"公共厕所", "咖啡":"咖啡", "药房":"药房", "商场":"商场", "酒店":"酒店"}

food_results = []
explore_results = []
loc_gcj = None
if loc_wgs:
    glat, glng = wgs84_to_gcj02(*loc_wgs)
    loc_gcj = {"lat": glat, "lng": glng}
    food_results = amap_around(glat, glng, radius, food_keyword_map.get(food_category, food_category), 12)
    explore_results = amap_around(glat, glng, 2500, explore_keyword_map.get(explore_category, explore_category), 20)

if not food_results:
    food_results = DEMO_FOOD

# compact source status: never fake sources we do not actually query
for p in food_results:
    p["sources"] = {
        "amap": bool(AMAP_WEB_KEY and not p.get("demo")),
        "dianping": None,
        "xiaohongshu": None,
    }
    # Internal trust matrix hook: rating + fresh structured POI fields + source breadth.
    # Multi-platform adapters can be added later without changing the UI.
    score = 0
    try:
        score += 45 if float(p.get("rating") or 0) >= 4.3 else 30 if float(p.get("rating") or 0) >= 4.0 else 15
    except Exception:
        score += 10
    score += 25 if p.get("open_today") else 10
    score += 15 if p.get("photo") else 5
    score += 15 if p["sources"]["amap"] else 0
    p["trust_score"] = score

payload = {
    "now_iso": now.isoformat(),
    "trip_start": TRIP_START.isoformat(),
    "trip_end": TRIP_END.isoformat(),
    "days": DAYS,
    "selected_day": selected_day,
    "page": page,
    "weather": weather,
    "landing_messages": LANDING_MESSAGES,
    "food": food_results,
    "food_live": bool(AMAP_WEB_KEY and loc_wgs),
    "explore": explore_results,
    "location_wgs": {"lat":loc_wgs[0], "lng":loc_wgs[1]} if loc_wgs else None,
    "location_gcj": loc_gcj,
    "amap_js_key": AMAP_JS_KEY,
    "amap_security_code": AMAP_SECURITY_CODE,
    "amap_web_connected": bool(AMAP_WEB_KEY),
    "images": IMG,
}


# -----------------------------------------------------------------------------
# Single inline UI component
# -----------------------------------------------------------------------------
APP_HTML = r"""
<div id="app-root" class="app-shell"></div>
"""

APP_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap');

:root{
  --paper:#f8f5ec; --paper2:#f2eee2; --ink:#24302a; --muted:#7d8278; --green:#596d52;
  --green2:#77866c; --sage:#dce3d3; --gold:#ba8a50; --red:#9a493b; --line:#dad4c6;
  --shadow:0 8px 26px rgba(54,58,47,.10); --radius:24px;
}
*{box-sizing:border-box}
body{margin:0}
.app-shell{width:100%;min-height:100vh;background:var(--paper);color:var(--ink);font-family:'Noto Sans SC',system-ui,-apple-system,sans-serif;overflow-x:hidden}
.screen{max-width:480px;margin:0 auto;min-height:100vh;padding:16px 16px 92px;position:relative;background:
 radial-gradient(circle at 100% 0%,rgba(129,143,109,.08),transparent 27%),var(--paper)}
.serif{font-family:'Cormorant Garamond','Noto Serif SC',serif}.muted{color:var(--muted)}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:2px 0 14px}.topbar h1{font-size:25px;margin:0;font-weight:600}.sub{font-size:12px;color:var(--muted)}
.card{background:rgba(255,255,255,.58);border:1px solid rgba(93,105,84,.14);border-radius:20px;box-shadow:0 5px 16px rgba(43,48,39,.055)}
.hero{height:238px;border-radius:24px;overflow:hidden;position:relative;background:#d9ddce;box-shadow:var(--shadow)}
.hero img{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(.86) contrast(.96)}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,28,24,.02) 30%,rgba(19,24,20,.55) 100%)}
.hero-copy{position:absolute;z-index:2;left:20px;right:20px;bottom:18px;color:#fff}.hero-copy .cn{font-family:'Cormorant Garamond','Noto Sans SC';font-size:28px;line-height:1.15;font-weight:600}.hero-copy .en{font-family:'Cormorant Garamond';font-style:italic;font-size:16px;margin-top:6px;opacity:.94}
.quote{font-family:'Cormorant Garamond','Noto Sans SC';font-size:17px;font-style:italic;color:#5d6659;line-height:1.4}
.greeting{display:flex;justify-content:space-between;align-items:flex-start;margin:6px 4px 14px}.greeting h2{font:600 32px/1 'Cormorant Garamond';margin:0 0 6px}.greeting .weather{font-size:26px;text-align:right}.greeting .weather small{display:block;font-size:11px;color:var(--muted);font-family:'Noto Sans SC'}
.now-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}.mini-card{padding:14px 14px 12px;min-height:116px}.label{font-size:11px;letter-spacing:.08em;color:var(--red);font-weight:600}.mini-card h3{font-size:15px;margin:7px 0 4px;line-height:1.28}.mini-card p{font-size:11px;color:var(--muted);margin:0;line-height:1.45}.timebig{font:600 20px 'Cormorant Garamond';color:var(--green)}
.quick{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin:14px 0}.quick button{border:0;background:transparent;padding:0;cursor:pointer}.quick .qbox{height:66px;border-radius:18px;background:rgba(255,255,255,.58);border:1px solid rgba(93,105,84,.13);display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:22px}.quick span{font-size:10px;color:#565f55;margin-top:5px;display:block}.quick .qbox:hover{transform:translateY(-2px);box-shadow:var(--shadow)}
.section-title{display:flex;justify-content:space-between;align-items:end;margin:20px 2px 9px}.section-title h3{font:600 22px 'Cormorant Garamond','Noto Sans SC';margin:0}.section-title small{font-size:11px;color:var(--muted)}
.day-strip{display:flex;gap:8px;overflow:auto;padding:2px 1px 7px;scrollbar-width:none}.day-chip{flex:0 0 auto;border:1px solid var(--line);border-radius:16px;padding:9px 12px;background:#faf8f0;font-size:11px;color:#5e655b;cursor:pointer}.day-chip.active{background:var(--green);color:#fff;border-color:var(--green);transform:translateY(-1px)}
.route-card{padding:13px;margin:10px 0 12px;background:linear-gradient(145deg,#fcfaf4,#f1eee3);position:relative;overflow:hidden}.route-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}.route-head strong{font:600 18px 'Cormorant Garamond','Noto Sans SC'}.route-head small{color:var(--muted);font-size:10px}.route-svg{width:100%;height:166px;display:block}.route-note{text-align:center;font:italic 14px 'Cormorant Garamond','Noto Sans SC';color:#667060;margin-top:-5px}
.route-node circle{fill:#6f8067;stroke:#f8f5ec;stroke-width:4}.route-node text.num{fill:#fff;font:600 10px sans-serif;text-anchor:middle;dominant-baseline:middle}.route-node text.name{fill:#4b5549;font:500 8.5px 'Noto Sans SC';text-anchor:middle}.route-node.past{opacity:.42}.route-node.next circle{fill:#b08b55}.route-node.current circle{fill:#9d4d3f;filter:drop-shadow(0 3px 5px rgba(118,58,48,.3));animation:pulse 1.8s ease-in-out infinite;transform-origin:center}.route-node.current text.name{font-weight:700;fill:#803f36}.route-path{fill:none;stroke:#87957d;stroke-width:3;stroke-dasharray:6 7;stroke-linecap:round}.route-decor{font-size:17px;opacity:.72}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.14)}}
.timeline{position:relative;padding-left:22px}.timeline:before{content:"";position:absolute;left:8px;top:11px;bottom:14px;width:1.5px;background:#8b987f}.event{position:relative;display:grid;grid-template-columns:58px 1fr 74px;gap:8px;align-items:center;padding:10px 0;border-bottom:1px solid rgba(92,99,84,.10)}.event:before{content:"";position:absolute;left:-18px;width:9px;height:9px;border-radius:50%;background:var(--green);border:2px solid var(--paper)}.event.past{opacity:.48}.event.current{background:linear-gradient(90deg,rgba(220,227,211,.52),transparent);border-radius:12px;padding-left:7px;margin-left:-7px}.event.current:before{background:var(--red);box-shadow:0 0 0 4px rgba(154,73,59,.13)}.event.next:before{background:var(--gold)}.event .tm{font:600 14px 'Cormorant Garamond';color:#5a6157}.event h4{margin:0 0 2px;font-size:13px}.event p{font-size:10px;line-height:1.38;color:var(--muted);margin:0}.event img{width:68px;height:58px;border-radius:12px;object-fit:cover;filter:saturate(.88)}.event .urgent{display:inline-block;font-size:9px;color:#8b4439;background:#f3e3dd;border-radius:999px;padding:2px 6px;margin-top:4px}
.soft-note{margin:14px 0;padding:15px 17px;border-radius:18px;background:linear-gradient(135deg,#f8efe0,#f5f2e7);font:italic 16px/1.5 'Cormorant Garamond','Noto Sans SC';color:#6c6356}
.nav{position:fixed;z-index:50;left:50%;transform:translateX(-50%);bottom:0;width:min(480px,100vw);height:72px;background:rgba(248,245,236,.94);backdrop-filter:blur(14px);border-top:1px solid rgba(84,95,76,.12);display:grid;grid-template-columns:repeat(5,1fr);padding:8px 7px 10px}.nav button{border:0;background:none;color:#7d837b;font-size:10px;cursor:pointer;display:flex;flex-direction:column;gap:3px;align-items:center;justify-content:center}.nav button b{font-size:20px;font-weight:400}.nav button.active{color:#3f6048;font-weight:600}
.filters{display:flex;gap:7px;overflow:auto;scrollbar-width:none;padding:4px 0 9px}.pill{border:1px solid var(--line);background:#f9f7ef;border-radius:999px;padding:8px 12px;font-size:11px;white-space:nowrap;cursor:pointer}.pill.active{background:var(--green);color:white;border-color:var(--green)}
.location-bar{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:11px 13px;margin-bottom:10px}.loc-left{display:flex;align-items:center;gap:8px}.loc-dot{width:9px;height:9px;border-radius:50%;background:#2d7cdc;box-shadow:0 0 0 4px rgba(45,124,220,.12)}.loc-text{font-size:11px}.loc-btn{border:0;border-radius:999px;background:#e7ecdf;color:#465a42;padding:7px 10px;font-size:10px;cursor:pointer}
.poi-list{display:flex;flex-direction:column;gap:9px}.poi{display:grid;grid-template-columns:82px 1fr;gap:11px;padding:9px}.poi img{width:82px;height:78px;border-radius:14px;object-fit:cover}.poi h4{font-size:14px;margin:1px 0 3px}.meta{font-size:10px;color:var(--muted);line-height:1.55}.rating{color:#b16d34;font-weight:600;font-size:12px}.sources{display:flex;gap:5px;margin-top:5px}.src{width:21px;height:21px;border-radius:7px;display:inline-flex;align-items:center;justify-content:center;font-size:9px;font-weight:700}.src.amap{background:#e7f0e6;color:#3e7042}.src.dp{background:#fbe6df;color:#c44d2d}.src.xhs{background:#f5e2e4;color:#b9414a}.src.unknown{opacity:.35;filter:grayscale(1)}.trust{margin-left:auto;font-size:9px;color:#64725f}.poi-top{display:flex;align-items:center;gap:6px}.open{color:#44845a;font-size:10px}.demo-flag{font-size:9px;color:#9b7c51;background:#f4ead9;border-radius:999px;padding:2px 6px}
.map-card{height:390px;border-radius:24px;overflow:hidden;position:relative;background:linear-gradient(145deg,#e7ede0,#dce8e9);border:1px solid #d7dacd}.map-canvas{position:absolute;inset:0;background:
 linear-gradient(22deg,transparent 0 45%,rgba(255,255,255,.68) 46% 49%,transparent 50%),
 linear-gradient(-26deg,transparent 0 40%,rgba(255,255,255,.74) 41% 44%,transparent 45%),
 repeating-linear-gradient(90deg,rgba(119,151,171,.12) 0 2px,transparent 2px 90px),
 repeating-linear-gradient(0deg,rgba(119,151,171,.10) 0 2px,transparent 2px 88px)}.river{position:absolute;width:140%;height:70px;background:rgba(112,180,196,.24);transform:rotate(-21deg);left:-25%;top:42%;border-radius:55%}.you{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:20px;height:20px;border:5px solid white;border-radius:50%;background:#2c7fd1;box-shadow:0 0 0 14px rgba(44,127,209,.14),0 3px 12px rgba(44,80,110,.25)}.map-pin{position:absolute;width:26px;height:26px;border-radius:50% 50% 50% 0;background:#5a7651;transform:rotate(-45deg);box-shadow:0 4px 9px rgba(52,66,47,.18)}.map-pin span{display:block;transform:rotate(45deg);font-size:11px;text-align:center;line-height:26px;color:white}.map-overlay{position:absolute;left:12px;right:12px;bottom:12px;background:rgba(250,248,240,.92);backdrop-filter:blur(10px);border-radius:18px;padding:11px 12px;font-size:11px}.map-overlay strong{display:block;font-size:13px}.map-live{width:100%;height:100%;}
.explore-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:10px 0 12px}.explore-btn{border:1px solid rgba(90,105,82,.13);background:#faf8f0;border-radius:16px;padding:10px 3px;text-align:center;font-size:10px;cursor:pointer}.explore-btn b{display:block;font-size:20px;margin-bottom:3px}.explore-btn.active{background:#e7ecdf;color:#3f6149}
.trip-hero{height:245px}.tabs{display:flex;gap:18px;border-bottom:1px solid var(--line);margin:10px 0 14px;padding:0 3px}.tabs span{font:600 15px 'Cormorant Garamond';padding:6px 0}.tabs .active{border-bottom:2px solid var(--green);color:var(--green)}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.stat{text-align:center;padding:13px 6px}.stat b{display:block;font:600 20px 'Cormorant Garamond';color:#4d6549}.trip-day{display:grid;grid-template-columns:48px 1fr auto;gap:9px;align-items:center;padding:11px 12px;border-bottom:1px solid rgba(80,91,76,.09);cursor:pointer}.trip-day .badge{background:#e7ecdf;border-radius:12px;text-align:center;padding:6px 4px;font-size:10px;color:#4e654b}.trip-day strong{font-size:12px}.trip-day small{display:block;color:var(--muted);font-size:9px;margin-top:2px}
.memory-head{padding:14px}.memory-actions{display:flex;gap:8px;margin-top:9px}.action-btn{flex:1;border:1px solid var(--line);background:#faf8ef;border-radius:14px;padding:9px;font-size:11px;cursor:pointer}.memory-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:10px}.memory-item{aspect-ratio:1;border-radius:12px;overflow:hidden;position:relative;background:#e6e0d4}.memory-item img{width:100%;height:100%;object-fit:cover}.memory-item.selected:after{content:'✓';position:absolute;right:6px;top:6px;background:#4f704f;color:#fff;width:20px;height:20px;border-radius:50%;display:grid;place-items:center;font-size:11px}.memory-item input{display:none}.memory-empty{text-align:center;color:var(--muted);padding:35px 10px;font:italic 16px 'Cormorant Garamond'}.day-summary{display:grid;grid-template-columns:1fr auto;gap:8px;padding:12px 14px;margin:10px 0}.day-summary h3{margin:0;font:600 20px 'Cormorant Garamond','Noto Sans SC'}.day-summary p{font-size:10px;color:var(--muted);margin:3px 0 0}
.landing{position:fixed;z-index:999;inset:0;background:linear-gradient(180deg,#faf7ef,#f1eee4);display:flex;align-items:center;justify-content:center;overflow:hidden}.landing.hidden{animation:fadeOut .55s ease forwards}.land-inner{width:min(430px,94vw);height:min(760px,94vh);position:relative;border-radius:32px;overflow:hidden;background:
 radial-gradient(circle at 75% 15%,rgba(133,151,115,.16),transparent 28%),linear-gradient(180deg,#fbf8f0,#eee8da)}.bamboo{position:absolute;font-size:110px;opacity:.15;top:-15px;left:-28px;transform:rotate(-12deg)}.mountains{position:absolute;bottom:0;left:0;right:0;height:35%;opacity:.22;background:linear-gradient(155deg,transparent 0 24%,#7b8d79 25% 42%,transparent 43%),linear-gradient(25deg,transparent 0 31%,#8d9d87 32% 49%,transparent 50%)}.land-title{position:absolute;top:70px;left:20px;right:20px;text-align:center}.land-title h1{font:600 42px/1 'Cormorant Garamond';margin:0;color:#26342b}.land-title small{font:500 10px/2 'Noto Sans SC';letter-spacing:.28em;color:#7b8177}.panda{position:absolute;width:112px;height:150px;left:-120px;bottom:120px;animation:walkIn 2.45s cubic-bezier(.25,.75,.25,1) .25s forwards}.panda-body{position:absolute;width:88px;height:100px;background:#fff;border-radius:50% 50% 45% 45%;left:12px;top:42px;box-shadow:inset 0 -5px 0 #e8e5dd}.panda-head{position:absolute;width:92px;height:84px;background:#fff;border-radius:48% 48% 45% 45%;left:10px;top:0;z-index:3}.ear{position:absolute;width:30px;height:30px;background:#202522;border-radius:50%;top:-7px}.ear.l{left:4px}.ear.r{right:4px}.eye{position:absolute;width:23px;height:31px;background:#202522;border-radius:55% 45% 55% 45%;top:27px}.eye.l{left:15px;transform:rotate(25deg)}.eye.r{right:15px;transform:rotate(-25deg)}.eye:after{content:'';position:absolute;width:6px;height:8px;background:#fff;border-radius:50%;left:9px;top:8px}.nose{position:absolute;width:15px;height:10px;background:#202522;border-radius:50%;left:39px;top:54px}.arm{position:absolute;width:28px;height:72px;background:#202522;border-radius:20px;top:56px;z-index:2}.arm.l{left:5px;transform:rotate(16deg)}.arm.r{right:2px;transform-origin:top center;transform:rotate(-8deg)}.leg{position:absolute;width:28px;height:50px;background:#202522;border-radius:18px;top:115px}.leg.l{left:19px}.leg.r{right:19px}.panda.wave .arm.r{animation:wave .55s ease-in-out 4}.bubble{position:absolute;left:50%;transform:translateX(-50%) scale(.88);bottom:300px;width:82%;background:rgba(255,255,255,.88);border:1px solid #ded8ca;border-radius:24px;padding:18px 20px;text-align:center;box-shadow:var(--shadow);opacity:0;animation:bubbleIn .45s ease 2.9s forwards}.bubble .cn{font-size:17px;font-weight:500}.bubble .en{font:italic 15px 'Cormorant Garamond';color:#70766d;margin-top:5px}.enter-btn{position:absolute;left:50%;bottom:36px;transform:translateX(-50%);border:0;background:#4f654c;color:#fff;border-radius:999px;padding:12px 28px;font-size:12px;opacity:0;animation:bubbleIn .45s ease 3.35s forwards;cursor:pointer}.skip{position:absolute;right:20px;top:20px;border:0;background:transparent;color:#8c9188;font-size:11px;cursor:pointer}
@keyframes walkIn{0%{left:-120px;transform:scale(.58)}70%{left:50%;transform:translateX(-50%) scale(.78)}100%{left:50%;transform:translateX(-50%) scale(1)}}
@keyframes wave{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(-58deg)}}@keyframes bubbleIn{to{opacity:1;transform:translateX(-50%) scale(1)}}@keyframes fadeOut{to{opacity:0;visibility:hidden}}
@media(max-width:390px){.screen{padding-left:12px;padding-right:12px}.event{grid-template-columns:52px 1fr 66px}.event img{width:62px;height:54px}.hero{height:222px}.route-svg{height:158px}}
"""

APP_JS = r"""
export default function(component) {
  const { data, parentElement, setStateValue } = component;
  const root = parentElement.querySelector('#app-root');
  const D = data;
  const state = {
    page: D.page || 'home',
    day: Number(D.selected_day || 1),
    radius: Number(D.radius || 1000),
    foodCategory: D.food_category || '全部',
    exploreCategory: D.explore_category || '景点',
    location: D.location_wgs || null,
  };
  const esc = (s='') => String(s).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
  const dayData = () => D.days[state.day - 1];
  const eventToMinutes = t => { const [h,m]=t.split(':').map(Number); return h*60+m; };
  const localNow = new Date();
  const ymd = d => `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  const todayStr = ymd(localNow);

  function currentEventIndex(day) {
    if (day.date !== todayStr) return -1;
    const min = localNow.getHours()*60 + localNow.getMinutes();
    for (let i=0;i<day.events.length;i++) {
      const e = day.events[i];
      if (min >= eventToMinutes(e.start) && min < eventToMinutes(e.end)) return i;
    }
    return -1;
  }
  function nextEventIndex(day) {
    const min = localNow.getHours()*60 + localNow.getMinutes();
    if (day.date !== todayStr) return 0;
    for (let i=0;i<day.events.length;i++) if (eventToMinutes(day.events[i].start) > min) return i;
    return -1;
  }
  function phaseForEvent(day, i) {
    if (day.date !== todayStr) return '';
    const ci = currentEventIndex(day), ni = nextEventIndex(day);
    if (ci === i) return 'current';
    if (ni === i) return 'next';
    const min = localNow.getHours()*60 + localNow.getMinutes();
    if (eventToMinutes(day.events[i].end) <= min) return 'past';
    return '';
  }
  function hhmmDiff(t) {
    const [h,m]=t.split(':').map(Number); const target=new Date(localNow); target.setHours(h,m,0,0);
    const diff=Math.max(0,target-localNow); const mins=Math.round(diff/60000); const hh=Math.floor(mins/60), mm=mins%60;
    return hh ? `${hh}h ${mm}m` : `${mm} min`;
  }
  function iconFor(e){ return e.type==='flight'?'✈️':e.type==='meal'?'🍜':e.type==='place'?'◉':e.type==='transfer'?'🚗':'☕'; }
  function shortName(e){
    let s=e.cn || e.title; s=s.replace(' · 自由安排','').replace(' · Optional','');
    if(s.length>8) s=s.slice(0,8); return s;
  }
  function greeting(){ const h=localNow.getHours(); return h<12?'Good morning':h<18?'Good afternoon':'Good evening'; }
  function atmosphere(){ const lines=['慢慢走，今天也会有好故事。','Good days are better when shared.','好好旅行，是让一家人更靠近。','Collect moments, not things.']; return lines[(localNow.getDate()+state.day)%lines.length]; }

  function landingMessage(){
    const now=todayStr, start=D.trip_start, end=D.trip_end;
    if(now < start) return D.landing_messages.before;
    if(now > end) return D.landing_messages.after;
    const diff=Math.round((new Date(now+'T00:00:00')-new Date(start+'T00:00:00'))/86400000)+1;
    return D.landing_messages[String(diff)] || D.landing_messages[diff] || D.landing_messages.before;
  }
  function renderLanding(){
    if(sessionStorage.getItem('chengduLandingSeen')==='1') return '';
    const m=landingMessage();
    return `<div class="landing" id="landing"><div class="land-inner">
      <button class="skip" data-action="close-landing">Skip</button><div class="bamboo">🎋</div><div class="mountains"></div>
      <div class="land-title"><h1>Our Chengdu Story</h1><small>A FAMILY JOURNEY · 15–20 OCT 2026</small></div>
      <div class="bubble"><div class="cn">${esc(m.cn)}</div><div class="en">${esc(m.en)}</div></div>
      <div class="panda wave"><div class="panda-body"></div><div class="panda-head"><i class="ear l"></i><i class="ear r"></i><i class="eye l"></i><i class="eye r"></i><i class="nose"></i></div><i class="arm l"></i><i class="arm r"></i><i class="leg l"></i><i class="leg r"></i></div>
      <button class="enter-btn" data-action="close-landing">开启今天的旅程　→</button>
    </div></div>`;
  }

  function nav(){
    const items=[['home','⌂','Home'],['today','▣','Today'],['explore','⌾','Explore'],['trip','♧','Trip'],['memories','▧','Memories']];
    return `<nav class="nav">${items.map(([p,i,t])=>`<button data-page="${p}" class="${state.page===p?'active':''}"><b>${i}</b>${t}</button>`).join('')}</nav>`;
  }
  function dayChips(){ return `<div class="day-strip">${D.days.map(d=>`<button class="day-chip ${d.day===state.day?'active':''}" data-day="${d.day}">Day ${d.day}<br><small>${d.weekday} ${d.date.slice(8)}</small></button>`).join('')}</div>`; }

  function routeSvg(day){
    let ev=day.events.filter(e=>['place','meal'].includes(e.type));
    if(ev.length>5) ev=ev.slice(0,5);
    const n=ev.length;
    const pos = n<=4 ? [[16,64],[39,78],[62,43],[85,64]] : [[12,64],[31,78],[50,43],[69,75],[88,53]];
    const path = n<=4 ? 'M16 64 Q27 88 39 78 Q50 69 62 43 Q73 38 85 64' : 'M12 64 Q21 88 31 78 Q41 67 50 43 Q59 44 69 75 Q78 86 88 53';
    const dayCurrent=currentEventIndex(day);
    return `<svg class="route-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
      <text x="8" y="24" class="route-decor">🏯</text><text x="78" y="24" class="route-decor">🌿</text><text x="83" y="91" class="route-decor">🐼</text>
      <path class="route-path" d="${path}"/>
      ${ev.map((e,j)=>{
        const orig=day.events.indexOf(e); let cls='';
        if(day.date===todayStr){ if(orig<dayCurrent && dayCurrent>=0) cls='past'; else if(orig===dayCurrent) cls='current'; else if(orig===nextEventIndex(day)) cls='next'; }
        const [x,y]=pos[j];
        return `<g class="route-node ${cls}"><circle cx="${x}" cy="${y}" r="6.3"></circle><text class="num" x="${x}" y="${y}">${j+1}</text><text class="name" x="${x}" y="${y+13}">${esc(shortName(e))}</text></g>`
      }).join('')}
    </svg>`;
  }

  function timeline(day){
    return `<div class="timeline">${day.events.map((e,i)=>`<div class="event ${phaseForEvent(day,i)}">
      <div class="tm">${e.start}</div><div><h4>${esc(e.title)}</h4><p>${esc(e.cn)}<br>${esc(e.subtitle||'')}</p>${e.time_sensitive?'<span class="urgent">TIME-SENSITIVE</span>':''}</div><img src="${esc(e.image||D.images.street)}" alt=""></div>`).join('')}</div>`;
  }

  function home(){
    const actualDay = todayStr>=D.trip_start && todayStr<=D.trip_end ? Math.min(6, Math.max(1, Math.floor((new Date(todayStr)-new Date(D.trip_start))/86400000)+1)) : state.day;
    const day=D.days[actualDay-1]; const ci=currentEventIndex(day), ni=nextEventIndex(day);
    let nowCard, nextCard;
    if(todayStr < D.trip_start){
      const daysLeft=Math.ceil((new Date(D.trip_start)-new Date(todayStr))/86400000);
      nowCard={title:`Trip begins in ${daysLeft} days`,sub:'行李慢慢收，期待慢慢长。',time:'15 Oct'};
      nextCard={title:'Penang → Shanghai',sub:'HO1366 · 00:05',time:'00:05'};
    }else if(todayStr > D.trip_end){
      nowCard={title:'Back home',sub:'回忆已经悄悄留下来了。',time:'♡'}; nextCard={title:'Chengdu misses you',sub:'下次再回来，好不好？',time:'Next time'};
    }else{
      const ce=ci>=0?day.events[ci]:null, ne=ni>=0?day.events[ni]:null;
      nowCard=ce?{title:ce.title,sub:ce.cn,time:ce.start}:{title:'Between little moments',sub:'慢慢来，不需要赶。',time:'Now'};
      nextCard=ne?{title:ne.title,sub:`${ne.cn} · ${hhmmDiff(ne.start)} to go`,time:ne.start}:{title:'Today is complete',sub:'回酒店，好好休息。',time:'Done'};
    }
    const w=D.weather;
    return `<main class="screen">
      <div class="greeting"><div><h2>${greeting()},</h2><div class="quote">${esc(atmosphere())}</div></div><div class="weather">${w.icon} ${w.temp}°C<small>${esc(day.city)} · ${esc(w.desc)}</small></div></div>
      <div class="hero"><img src="${esc(day.hero)}"><div class="hero-copy"><div class="cn">${esc(day.hero_cn)}</div><div class="en">${esc(day.hero_en)}</div></div></div>
      <div class="now-grid"><div class="card mini-card"><div class="label">NOW</div><div class="timebig">${esc(nowCard.time)}</div><h3>${esc(nowCard.title)}</h3><p>${esc(nowCard.sub)}</p></div>
      <div class="card mini-card"><div class="label">NEXT</div><div class="timebig">${esc(nextCard.time)}</div><h3>${esc(nextCard.title)}</h3><p>${esc(nextCard.sub)}</p></div></div>
      <div class="quick">
       <button data-page="today"><div class="qbox">▣</div><span>Today 今日行程</span></button>
       <button data-page="food"><div class="qbox">♨</div><span>Nearby Food</span></button>
       <button data-page="weather"><div class="qbox">☁</div><span>Weather 天气</span></button>
       <button data-page="memories"><div class="qbox">▧</div><span>Memories 相册</span></button></div>
      <div class="section-title"><h3>Our Journey</h3><small>15–20 Oct 2026</small></div>${dayChips()}
      <div class="soft-note">“Not just places, but moments together.”<br><span class="sub">旅行的意义，是和重要的人一起。</span></div>
      ${nav()}
    </main>`;
  }

  function today(){ const day=dayData(); return `<main class="screen"><div class="topbar"><button class="pill" data-day="${Math.max(1,state.day-1)}">‹</button><div style="text-align:center"><h1 class="serif">Today</h1><div class="sub">${day.date.slice(5).replace('-','/')} · ${day.weekday}</div></div><button class="pill" data-day="${Math.min(6,state.day+1)}">›</button></div>
    <div class="hero" style="height:205px"><img src="${esc(day.hero)}"><div class="hero-copy"><div class="cn">${esc(day.hero_cn)}</div><div class="en">${esc(day.hero_en)}</div></div></div>
    <div class="card route-card"><div class="route-head"><strong>Today's Route　今日路线</strong><small>${day.events.filter(e=>['place','meal'].includes(e.type)).length} stops · gentle pace</small></div>${routeSvg(day)}<div class="route-note">Good food. Good company. That's the day. ♡</div></div>
    ${timeline(day)}<div class="soft-note">今天不用赶，慢慢玩。<br><span class="sub">Take your time. You're exactly where you need to be. ♡</span></div>${nav()}</main>`; }

  function sourceIcons(p){ const a=p.sources?.amap; return `<div class="sources"><span class="src amap ${a?'':'unknown'}">高${a?'✓':'·'}</span><span class="src dp unknown">评·</span><span class="src xhs unknown">书·</span><span class="trust">${p.trust_score>=75?'✓':p.trust_score>=55?'~':'!'} trust</span></div>`; }
  function food(){
    const cats=['全部','川菜','火锅','小吃','面','咖啡','甜品']; const radii=[500,1000,2000,5000];
    return `<main class="screen"><div class="topbar"><div><h1 class="serif">附近美食</h1><div class="sub">Nearby Food · around you, when hungry</div></div><button class="pill" data-action="locate">◎ 定位</button></div>
      <div class="card location-bar"><div class="loc-left"><i class="loc-dot"></i><div class="loc-text">${D.location_wgs?'Using your current location':'Tap 定位 to search around you'}<br><span class="muted">${D.food_live?'Live AMap POIs':'Preview / fallback until AMap key is connected'}</span></div></div></div>
      <div class="filters">${cats.map(c=>`<button class="pill ${state.foodCategory===c?'active':''}" data-food-cat="${c}">${c}</button>`).join('')}</div>
      <div class="filters">${radii.map(r=>`<button class="pill ${state.radius===r?'active':''}" data-radius="${r}">${r<1000?r+' m':r/1000+' km'}</button>`).join('')}</div>
      <div class="poi-list">${D.food.map(p=>`<div class="card poi" data-poi="${esc(p.name)}"><img src="${esc(p.photo||D.images.food)}"><div><div class="poi-top"><h4>${esc(p.name)}</h4>${p.demo?'<span class="demo-flag">PREVIEW</span>':''}</div><div class="meta">${esc(p.tag||p.type||'Local food')} · ${Number(p.distance||0)<1000?Math.round(p.distance)+' m':(Number(p.distance||0)/1000).toFixed(1)+' km'}</div><div><span class="rating">★ ${esc(p.rating||'—')}</span>　<span class="open">${p.open_today?'Open · '+esc(p.open_today):'Hours unavailable'}</span></div>${sourceIcons(p)}</div></div>`).join('')}</div>
      <div class="soft-note">评分看得到，复杂判断留在后台。<br><span class="sub">We compare signals quietly — the screen stays simple.</span></div>${nav()}</main>`;
  }

  function stylizedMap(){
    const pins=(D.explore||[]).slice(0,7).map((p,i)=>{const pos=[[18,25],[72,22],[30,42],[78,48],[20,68],[62,70],[42,18]][i]||[50,30]; return `<div class="map-pin" style="left:${pos[0]}%;top:${pos[1]}%"><span>${i+1}</span></div>`}).join('');
    return `<div class="map-card"><div class="map-canvas"><div class="river"></div>${pins}<div class="you"></div></div><div class="map-overlay"><strong>📍 ${D.location_wgs?'You are here':'Tap 定位 to place yourself on the map'}</strong>${D.amap_js_key?'Live AMap loads when configured':'Cute overview fallback · live AMap key not added yet'}</div></div>`;
  }
  function explore(){ const cats=[['景点','🏯'],['便利店','🏪'],['厕所','🚻'],['咖啡','☕'],['药房','✚'],['商场','🛍'],['酒店','▥']];
    return `<main class="screen"><div class="topbar"><div><h1 class="serif">探索周边</h1><div class="sub">Explore · what is around me?</div></div><button class="pill" data-action="locate">◎ 定位</button></div>
      <div class="explore-grid">${cats.map(([c,i])=>`<button class="explore-btn ${state.exploreCategory===c?'active':''}" data-explore-cat="${c}"><b>${i}</b>${c}</button>`).join('')}</div>
      <div id="live-map-holder">${stylizedMap()}</div>
      <div class="section-title"><h3>Nearby</h3><small>${D.explore?.length||0} places</small></div>
      <div class="poi-list">${(D.explore||[]).slice(0,6).map((p,i)=>`<div class="card" style="padding:11px 13px;display:flex;justify-content:space-between;gap:10px"><div><strong style="font-size:12px">${i+1}. ${esc(p.name)}</strong><div class="meta">${esc(p.address||p.type||'')} · ${p.distance?Math.round(p.distance)+' m':''}</div></div><button class="loc-btn" data-amap="${p.lng||''},${p.lat||''},${esc(p.name)}">导航</button></div>`).join('') || '<div class="memory-empty">定位后，这里会出现你身边的小惊喜。</div>'}</div>
      ${nav()}</main>`;
  }

  function weatherPage(){ const w=D.weather, day=dayData(); return `<main class="screen"><div class="topbar"><div><h1 class="serif">天气 · Weather</h1><div class="sub">${esc(day.city)} · live conditions</div></div><button class="pill" data-page="home">‹ Home</button></div>
    <div class="hero" style="height:230px"><img src="${esc(day.hero)}"><div class="hero-copy"><div class="cn">${w.icon} ${w.temp}°C</div><div class="en">${esc(w.desc)} · feels like ${w.feels}°C</div></div></div>
    <div class="stats" style="margin-top:12px"><div class="card stat"><b>${w.high}°</b><small>High</small></div><div class="card stat"><b>${w.low}°</b><small>Low</small></div><div class="card stat"><b>${w.rain_prob}%</b><small>Rain</small></div></div>
    <div class="soft-note">普通天气只提醒，不打乱行程。<br><span class="sub">Only meaningful disruptions deserve a real alert.</span></div>${nav()}</main>`; }

  function trip(){ return `<main class="screen"><div class="topbar"><div><h1 class="serif">我们的旅程</h1><div class="sub">Trip Overview</div></div><span class="sub">15–20 Oct 2026</span></div>
    <div class="hero trip-hero"><img src="${D.images.temple}"><div class="hero-copy"><div class="cn">Chengdu</div><div class="en">Same people. A different view.</div></div></div>
    <div class="tabs"><span class="active">Overview</span><span>Itinerary</span><span>Photos</span><span>Notes</span></div>
    <div class="stats"><div class="card stat"><b>6</b><small>Days</small></div><div class="card stat"><b>1</b><small>Family trip</small></div><div class="card stat"><b>♡</b><small>Many memories</small></div></div>
    <div class="section-title"><h3>Our Journey</h3><small>Shanghai · transit only</small></div>
    <div class="card">${D.days.map(d=>{const brief=d.events.filter(e=>e.type==='place').slice(0,3).map(e=>e.cn.split(' · ')[0]).join(' · ') || d.events[0].cn; return `<div class="trip-day" data-day="${d.day}" data-page="today"><div class="badge">Day ${d.day}</div><div><strong>${esc(d.city)}</strong><small>${esc(brief)}</small></div><span>›</span></div>`}).join('')}</div>
    <div class="soft-note">一起走过的，都是更好的风景。♡<br><span class="sub">A trip well taken brings us closer.</span></div>${nav()}</main>`; }

  async function openDB(){ return new Promise((resolve,reject)=>{ const req=indexedDB.open('chengduStoryMemories',1); req.onupgradeneeded=()=>{const db=req.result;if(!db.objectStoreNames.contains('photos')) db.createObjectStore('photos',{keyPath:'id'});};req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error);}); }
  async function getPhotos(){ const db=await openDB(); return new Promise((resolve,reject)=>{const tx=db.transaction('photos','readonly');const rq=tx.objectStore('photos').getAll();rq.onsuccess=()=>resolve(rq.result||[]);rq.onerror=()=>reject(rq.error);}); }
  async function saveFiles(files){ const db=await openDB(); const tx=db.transaction('photos','readwrite'); for(const f of files){ const url=await new Promise(res=>{const r=new FileReader();r.onload=()=>res(r.result);r.readAsDataURL(f)}); tx.objectStore('photos').put({id:`${Date.now()}-${Math.random()}`,name:f.name||'photo.jpg',type:f.type||'image/jpeg',dataUrl:url,date:todayStr}); } return new Promise(res=>tx.oncomplete=res); }
  async function renderMemories(){ const box=root.querySelector('#memory-grid'); if(!box) return; const photos=await getPhotos(); if(!photos.length){box.innerHTML='<div class="memory-empty" style="grid-column:1/-1">还没有照片。第一张回忆，等你来拍 ♡</div>';return;} box.innerHTML=photos.slice().reverse().map(p=>`<div class="memory-item" data-photo-id="${p.id}"><img src="${p.dataUrl}"></div>`).join(''); }
  function memories(){ const day=dayData(); return `<main class="screen"><div class="topbar"><div><h1 class="serif">旅行相册</h1><div class="sub">Memories · stored on this device</div></div><span>♡</span></div>
    ${dayChips()}<div class="card day-summary"><div><h3>${day.date.slice(8)} Oct · ${esc(day.city)}</h3><p>${D.weather.icon} ${D.weather.temp}°C · ${day.events.filter(e=>e.type==='place').length} planned places</p></div><div style="font-size:28px">🍃</div></div>
    <div class="card memory-head"><strong>A Little Happiness</strong><div class="sub">旅途中的小确幸</div><div class="memory-actions"><label class="action-btn">📷 Take Photo<input id="camera-input" type="file" accept="image/*" capture="environment"></label><label class="action-btn">＋ Add from Gallery<input id="gallery-input" type="file" accept="image/*" multiple></label></div></div>
    <div id="memory-grid" class="memory-grid"></div><button id="save-selected" class="action-btn" style="width:100%;margin-top:10px">Save selected to phone / Share</button>
    <div class="soft-note">这些瞬间，是我们最珍贵的故事。<br><span class="sub">Their memories are our most precious souvenirs.</span></div>${nav()}</main>`; }

  function render(){
    let body = state.page==='today'?today():state.page==='food'?food():state.page==='explore'?explore():state.page==='trip'?trip():state.page==='memories'?memories():state.page==='weather'?weatherPage():home();
    root.innerHTML = renderLanding() + body;
    bind();
    if(state.page==='memories') renderMemories();
    if(state.page==='explore' && D.amap_js_key && D.amap_security_code && D.location_gcj) initAmap();
  }

  function requestLocation(){
    if(!navigator.geolocation){ alert('This browser does not support location.'); return; }
    navigator.geolocation.getCurrentPosition(pos=>{
      setStateValue('location',{lat:pos.coords.latitude,lng:pos.coords.longitude,accuracy:pos.coords.accuracy,ts:Date.now()});
    }, err=> alert('Location permission is needed for nearby search. '+err.message), {enableHighAccuracy:true,timeout:12000,maximumAge:60000});
  }

  function bind(){
    root.querySelectorAll('[data-page]').forEach(el=>el.addEventListener('click',()=>setStateValue('page',el.dataset.page)));
    root.querySelectorAll('[data-day]').forEach(el=>el.addEventListener('click',()=>setStateValue('selected_day',Number(el.dataset.day))));
    root.querySelectorAll('[data-radius]').forEach(el=>el.addEventListener('click',()=>setStateValue('radius',Number(el.dataset.radius))));
    root.querySelectorAll('[data-food-cat]').forEach(el=>el.addEventListener('click',()=>setStateValue('food_category',el.dataset.foodCat)));
    root.querySelectorAll('[data-explore-cat]').forEach(el=>el.addEventListener('click',()=>setStateValue('explore_category',el.dataset.exploreCat)));
    root.querySelectorAll('[data-action="locate"]').forEach(el=>el.addEventListener('click',requestLocation));
    root.querySelectorAll('[data-action="close-landing"]').forEach(el=>el.addEventListener('click',()=>{sessionStorage.setItem('chengduLandingSeen','1');const l=root.querySelector('#landing');if(l)l.classList.add('hidden')}));
    root.querySelectorAll('[data-amap]').forEach(el=>el.addEventListener('click',()=>{const [lng,lat,name]=el.dataset.amap.split(','); window.open(`https://uri.amap.com/marker?position=${lng},${lat}&name=${encodeURIComponent(name)}&callnative=1`,'_blank')}));
    const cam=root.querySelector('#camera-input'), gal=root.querySelector('#gallery-input');
    [cam,gal].filter(Boolean).forEach(inp=>inp.addEventListener('change',async()=>{if(inp.files?.length){await saveFiles([...inp.files]);await renderMemories();}}));
    const save=root.querySelector('#save-selected'); if(save) save.addEventListener('click',()=>saveSelected());
    if((state.page==='food'||state.page==='explore') && !D.location_wgs && !sessionStorage.getItem('geoAsked')){sessionStorage.setItem('geoAsked','1'); setTimeout(requestLocation,350);}
  }

  async function saveSelected(){
    const selected=[...root.querySelectorAll('.memory-item.selected')];
    if(!selected.length){alert('先点选想保存的照片 ♡');return;}
    const all=await getPhotos(); const ids=new Set(selected.map(x=>x.dataset.photoId)); const photos=all.filter(p=>ids.has(p.id)); const files=[];
    for(const p of photos){const blob=await (await fetch(p.dataUrl)).blob(); files.push(new File([blob],p.name||'chengdu-memory.jpg',{type:p.type||blob.type||'image/jpeg'}));}
    if(navigator.canShare && navigator.canShare({files}) && navigator.share){try{await navigator.share({files,title:'Our Chengdu Story'});return;}catch(e){}}
    photos.forEach(p=>{const a=document.createElement('a');a.href=p.dataUrl;a.download=p.name||'chengdu-memory.jpg';a.click();});
  }
  root.addEventListener('click',e=>{const it=e.target.closest('.memory-item'); if(it) it.classList.toggle('selected');});

  function initAmap(){
    const holder=root.querySelector('#live-map-holder'); if(!holder) return;
    holder.innerHTML='<div class="map-card"><div id="amap-live" class="map-live"></div></div>';
    window._AMapSecurityConfig={securityJsCode:D.amap_security_code};
    const make=()=>{
      try{
        const c=[D.location_gcj.lng,D.location_gcj.lat]; const map=new AMap.Map('amap-live',{zoom:15,center:c,viewMode:'2D'});
        new AMap.Marker({position:c,map,content:'<div style="width:18px;height:18px;border:5px solid #fff;border-radius:50%;background:#2d7dcc;box-shadow:0 0 0 10px rgba(45,125,204,.15)"></div>'});
        (D.explore||[]).slice(0,20).forEach((p,i)=>{if(p.lng&&p.lat)new AMap.Marker({position:[p.lng,p.lat],map,title:p.name,label:{content:String(i+1),direction:'top'}})});
      }catch(e){ holder.innerHTML=stylizedMap(); }
    };
    if(window.AMap) make(); else { const s=document.createElement('script');s.src=`https://webapi.amap.com/maps?v=2.0&key=${encodeURIComponent(D.amap_js_key)}`;s.onload=make;s.onerror=()=>holder.innerHTML=stylizedMap();document.head.appendChild(s); }
  }

  render();
}
"""

journey_component = st.components.v2.component(
    name="chengdu_family_story_single_file",
    html=APP_HTML,
    css=APP_CSS,
    js=APP_JS,
)

# Mount with state callbacks so frontend values persist and are returned to Python.
result = journey_component(
    data={
        **payload,
        "radius": radius,
        "food_category": food_category,
        "explore_category": explore_category,
    },
    default={
        "page": page,
        "selected_day": selected_day,
        "radius": radius,
        "food_category": food_category,
        "explore_category": explore_category,
        "location": location,
    },
    on_page_change=lambda: None,
    on_selected_day_change=lambda: None,
    on_radius_change=lambda: None,
    on_food_category_change=lambda: None,
    on_explore_category_change=lambda: None,
    on_location_change=lambda: None,
    key="chengdu_story_ui",
)
