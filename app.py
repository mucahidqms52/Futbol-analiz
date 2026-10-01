import streamlit as st
import math
import copy
import re
import random
import json
import os
import html as _html
import time
import threading
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

import subprocess, sys


@st.cache_resource(show_spinner="Tarayıcı kuruluyor (ilk açılışta 1-2 dk sürer)...")
def _tarayici_kur():
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False, timeout=600)
    except Exception:
        pass
    return True


_tarayici_kur()

st.markdown("""
<style>
    .block-container { padding-top: 2rem !important; padding-bottom: 0.5rem !important; padding-left: 0.7rem !important; padding-right: 0.7rem !important; max-width: 100% !important; }
    h1 { font-size: 1.2rem !important; margin: 0.2rem 0 !important; text-align: center; }
    h2 { font-size: 1rem !important; margin: 0.3rem 0 !important; }
    h3 { font-size: 0.9rem !important; margin: 0.15rem 0 !important; }
    p { font-size: 0.85rem !important; margin: 0.2rem 0 !important; }
    hr { margin: 0.3rem 0 !important; }
    .stButton button { padding: 0.4rem 0.6rem !important; font-size: 0.9rem !important; height: 2.2rem !important; }
    div[data-testid="stAlert"] { padding: 0.3rem 0.5rem !important; font-size: 0.85rem !important; }
    textarea { font-size: 0.75rem !important; }
    .stApp { background: #0b1220 !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp div[data-testid="stMarkdownContainer"] { color: #e6edf7 !important; }
    .stApp div[data-testid="stCaptionContainer"], .stApp div[data-testid="stCaptionContainer"] *, .stApp small { color: #8fa0bd !important; }
    hr { border-color: #23304a !important; }
    h2, h3 { border-left: 3px solid #22c55e; padding-left: 0.45rem; }
    .stTextArea textarea, .stTextInput input, div[data-testid="stNumberInput"] input { background: #131c2e !important; color: #e6edf7 !important; border: 1px solid #23304a !important; border-radius: 10px !important; }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="base-input"] { background: #131c2e !important; border-radius: 10px !important; }
    .stButton button, div[data-testid="stDownloadButton"] button, div[data-testid="stFormSubmitButton"] button { background: #18233a !important; border: 1px solid #23304a !important; border-radius: 12px !important; font-weight: 600 !important; }
    .stButton button p, div[data-testid="stDownloadButton"] button p, div[data-testid="stFormSubmitButton"] button p { color: #e6edf7 !important; }
    .stButton button:hover, div[data-testid="stDownloadButton"] button:hover { border-color: #22c55e !important; }
    .stButton button[kind="primary"], button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; border: none !important; }
    .stButton button[kind="primary"] p, button[data-testid="stBaseButton-primary"] p, button[data-testid="stBaseButton-primaryFormSubmit"] p { color: #04130a !important; }
    div[data-testid="stExpander"] { background: #131c2e !important; border: 1px solid #23304a !important; border-radius: 14px !important; }
    div[data-testid="stExpander"] details { border: none !important; }
    div[data-testid="stAlert"] { border-radius: 12px !important; }
    .st-key-fa_nav div[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.3rem !important; }
    .st-key-fa_nav div[data-testid="stColumn"], .st-key-fa_nav div[data-testid="column"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
    .st-key-fa_nav .stButton button { padding: 0.2rem 0.2rem !important; height: 2rem !important; }
    .st-key-fa_nav .stButton button p { font-size: 0.72rem !important; white-space: nowrap; }
    .stApp .fa-hero { background: linear-gradient(135deg, #16233d, #0f1a2e); border: 1px solid #23304a; border-radius: 18px; padding: 14px 10px; margin: 6px 0 10px 0; text-align: center; }
    .stApp .fa-teams { display: flex; align-items: center; justify-content: space-between; gap: 6px; }
    .stApp .fa-team { flex: 1; font-weight: 700; font-size: 0.95rem; line-height: 1.2; word-break: break-word; }
    .stApp .fa-score { font-size: 1.7rem; font-weight: 800; color: #22c55e !important; min-width: 70px; }
    .stApp .fa-vs { font-size: 0.95rem; font-weight: 700; color: #8fa0bd !important; min-width: 50px; }
    .stApp .fa-sub { font-size: 0.72rem; color: #8fa0bd !important; margin-top: 6px; }
    .stApp .fa-card { background: #131c2e; border: 1px solid #23304a; border-radius: 16px; padding: 12px; margin-bottom: 10px; }
    .stApp .fa-card.fa-pos { border-color: rgba(34,197,94,0.55); box-shadow: 0 0 0 1px rgba(34,197,94,0.15) inset; }
    .stApp .fa-card.fa-neg { opacity: 0.92; }
    .stApp .fa-ttl { font-size: 0.78rem; font-weight: 700; color: #8fa0bd !important; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px; }
    .stApp .fa-pickrow { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .stApp .fa-pick { font-size: 1.15rem; font-weight: 800; }
    .stApp .fa-pct { font-size: 1.5rem; font-weight: 800; color: #22c55e !important; }
    .stApp .fa-pct.fa-off { color: #8fa0bd !important; }
    .stApp .fa-mut { font-size: 0.74rem; color: #8fa0bd !important; margin-top: 6px; }
    .stApp .fa-row { margin: 7px 0; }
    .stApp .fa-row-top { display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 3px; }
    .stApp .fa-lbl { color: #cbd5e1 !important; }
    .stApp .fa-val { font-weight: 700; }
    .stApp .fa-bar { position: relative; height: 8px; background: #1d2940; border-radius: 99px; overflow: hidden; }
    .stApp .fa-fill { height: 100%; border-radius: 99px; }
    .stApp .fa-tick { position: absolute; top: 0; bottom: 0; width: 2px; background: #e6edf7; opacity: 0.7; }
    .stApp .fa-badge { display: inline-block; padding: 3px 10px; border-radius: 99px; font-size: 0.72rem; font-weight: 700; white-space: nowrap; }
    .stApp .fa-b-green { background: rgba(34,197,94,0.15); color: #22c55e !important; border: 1px solid rgba(34,197,94,0.45); }
    .stApp .fa-b-yellow { background: rgba(245,158,11,0.15); color: #f59e0b !important; border: 1px solid rgba(245,158,11,0.45); }
    .stApp .fa-b-red { background: rgba(239,68,68,0.15); color: #ef4444 !important; border: 1px solid rgba(239,68,68,0.45); }
    .stApp .fa-b-gray { background: rgba(148,163,184,0.12); color: #94a3b8 !important; border: 1px solid rgba(148,163,184,0.35); }
    .stApp .fa-big { font-size: 1.9rem; font-weight: 800; line-height: 1.1; }
    .stApp .fa-g { color: #22c55e !important; }
    .stApp .fa-y { color: #f59e0b !important; }
    .stApp .fa-r { color: #ef4444 !important; }
    .stApp .fa-mk { background: #131c2e; border: 1px solid #23304a; border-radius: 16px; padding: 10px 12px; margin: -4px 0 8px 0; }
    .stApp .fa-mk-row { display: flex; align-items: center; justify-content: space-between; padding: 5px 0; border-bottom: 1px dashed #1d2940; }
    .stApp .fa-mk-row:last-child { border-bottom: none; }
    .stApp .fa-mk-lbl { font-size: 0.82rem; font-weight: 700; color: #cbd5e1 !important; min-width: 60px; }
    .stApp .fa-mk-pick { font-size: 0.92rem; font-weight: 800; }
    .stApp .fa-mk-pick.pass { color: #22c55e !important; }
    .stApp .fa-mk-pick.off { color: #94a3b8 !important; }
    .stApp .fa-mk-pct { font-size: 0.85rem; font-weight: 700; color: #e6edf7 !important; }
    .stApp .fa-mk-badge { font-size: 0.68rem; font-weight: 700; padding: 2px 8px; border-radius: 99px; margin-left: 6px; }
    .stApp .fa-mk-badge.ok { background: rgba(34,197,94,0.15); color: #22c55e !important; border: 1px solid rgba(34,197,94,0.45); }
    .stApp .fa-mk-badge.no { background: rgba(148,163,184,0.12); color: #94a3b8 !important; border: 1px solid rgba(148,163,184,0.35); }
    .login-hero { text-align: center; padding: 40px 10px 24px 10px; }
    .login-logo { font-size: 4.5rem; line-height: 1; margin-bottom: 12px; display: inline-block; }
    .login-title { font-size: 2rem !important; font-weight: 900 !important; background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0 !important; padding: 0 !important; letter-spacing: 1.2px; border: none !important; text-align: center !important; }
    .login-subtitle { font-size: 0.88rem; color: #8fa0bd !important; margin-top: 8px; }
    div[data-testid="stForm"] { background: linear-gradient(145deg, rgba(19,28,46,0.85), rgba(11,18,32,0.95)) !important; border: 1px solid rgba(34,197,94,0.18) !important; border-radius: 22px !important; padding: 24px 20px !important; }
    div[data-testid="stForm"] label p { font-size: 0.8rem !important; font-weight: 700 !important; color: #cbd5e1 !important; }
    div[data-testid="stForm"] input { height: 46px !important; font-size: 0.95rem !important; padding: 0 14px !important; background: rgba(11,18,32,0.85) !important; border: 1.5px solid #23304a !important; border-radius: 12px !important; }
    div[data-testid="stForm"] input:focus { border-color: #22c55e !important; outline: none !important; }
    div[data-testid="stForm"] button { height: 46px !important; font-size: 0.95rem !important; font-weight: 700 !important; border-radius: 12px !important; }
    div[data-testid="stForm"] button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; border: none !important; }
    div[data-testid="stForm"] button[kind="secondary"] { background: rgba(30,41,59,0.55) !important; border: 1.5px solid #23304a !important; }
    .login-divider { display: flex; align-items: center; gap: 12px; margin: 10px 0 6px 0; color: #64748b !important; font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; justify-content: center; }
    .login-divider::before, .login-divider::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, transparent, #23304a 50%, transparent); }
    .login-features { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 22px; }
    .lf-chip { display: inline-block; padding: 6px 14px; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.25); border-radius: 99px; font-size: 0.75rem; font-weight: 600; color: #cbd5e1 !important; }
    .login-footer { text-align: center; margin-top: 26px; font-size: 0.72rem; color: #64748b !important; }
    .login-footer b { color: #22c55e !important; font-weight: 700; }
    .mh-hero { position: relative; overflow: hidden; text-align: center; padding: 30px 14px 22px 14px; background: linear-gradient(135deg, rgba(22,35,61,0.85), rgba(15,26,46,0.9)); border: 1px solid rgba(34,197,94,0.22); border-radius: 22px; margin: 6px 0 16px 0; }
    .mh-hero-icon { font-size: 3.2rem; line-height: 1; margin-bottom: 10px; display: inline-block; }
    .mh-hero-title { font-size: 1.7rem; font-weight: 900; background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: 1px; margin: 0; }
    .mh-hero-sub { font-size: 0.84rem; color: #8fa0bd; margin-top: 8px; }
    .mh-hero-badge { display: inline-block; margin-top: 12px; padding: 4px 14px; background: rgba(34,197,94,0.12); border: 1px solid rgba(34,197,94,0.4); border-radius: 99px; font-size: 0.72rem; font-weight: 700; color: #22c55e !important; }
    .mh-stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 0 0 16px 0; }
    .mh-stat { position: relative; background: linear-gradient(145deg, #16233d, #0f1a2e); border: 1px solid #23304a; border-radius: 16px; padding: 14px 8px 12px 8px; text-align: center; }
    .mh-stat::after { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #22c55e, #3b82f6); }
    .mh-stat-icon { font-size: 1.3rem; margin-bottom: 2px; }
    .mh-stat-num { font-size: 1.85rem; font-weight: 900; color: #22c55e !important; line-height: 1; }
    .mh-stat-lbl { font-size: 0.68rem; color: #8fa0bd !important; margin-top: 5px; text-transform: uppercase; font-weight: 700; }
    .mh-section-title { font-size: 0.78rem; color: #8fa0bd !important; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; margin: 4px 0 8px 4px; text-align: left; border-left: 3px solid #22c55e; padding-left: 8px; }
    .st-key-fa_misafir_nav .stButton button { height: 72px !important; font-size: 1rem !important; font-weight: 800 !important; border-radius: 16px !important; }
    .st-key-fa_misafir_nav .stButton button p { font-size: 1rem !important; font-weight: 800 !important; }
    .mh-info { background: linear-gradient(145deg, rgba(19,28,46,0.6), rgba(11,18,32,0.8)); border: 1px solid #23304a; border-radius: 14px; padding: 12px 14px; margin-top: 14px; font-size: 0.76rem; color: #8fa0bd !important; line-height: 1.6; }
    .stApp .ga-wrap { display: flex; flex-direction: column; gap: 12px; margin: 6px 0 12px 0; }
    .stApp .ga-card { position: relative; overflow: hidden; background: linear-gradient(150deg, #18253f 0%, #101b30 100%); border: 1px solid #26334d; border-radius: 20px; padding: 16px 16px 14px 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.25); }
    .stApp .ga-card::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 5px; background: var(--c); box-shadow: 0 0 18px var(--c); }
    .stApp .ga-glow { position: absolute; right: -40px; top: -40px; width: 140px; height: 140px; border-radius: 50%; background: radial-gradient(circle, var(--c) 0%, transparent 70%); opacity: 0.13; pointer-events: none; }
    .stApp .ga-head { display: flex; align-items: center; justify-content: space-between; gap: 10px; position: relative; z-index: 1; }
    .stApp .ga-title { font-size: 0.8rem; font-weight: 800; color: #cbd5e1 !important; text-transform: uppercase; letter-spacing: 1px; display: flex; align-items: center; gap: 6px; }
    .stApp .ga-sub { font-size: 0.72rem; color: #8fa0bd !important; margin-top: 4px; }
    .stApp .ga-big { font-size: 2.6rem; font-weight: 900; line-height: 1; color: var(--c) !important; text-shadow: 0 0 22px var(--c); }
    .stApp .ga-pctsign { font-size: 1.1rem; font-weight: 800; color: var(--c) !important; opacity: 0.65; margin-left: 2px; }
    .stApp .ga-bar { position: relative; height: 9px; background: #1a2439; border-radius: 99px; overflow: hidden; margin: 13px 0; box-shadow: inset 0 1px 3px rgba(0,0,0,0.4); }
    .stApp .ga-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, var(--c), color-mix(in srgb, var(--c) 55%, #ffffff)); box-shadow: 0 0 14px var(--c); }
    .stApp .ga-items { display: grid; gap: 9px; grid-template-columns: repeat(auto-fit, minmax(88px, 1fr)); }
    .stApp .ga-item { position: relative; background: rgba(255,255,255,0.035); border: 1px solid #232f47; border-radius: 14px; padding: 10px 6px 9px 6px; text-align: center; transition: transform 0.15s ease, border-color 0.15s ease; }
    .stApp .ga-item:hover { transform: translateY(-2px); border-color: var(--c); }
    .stApp .ga-il { font-size: 0.7rem; font-weight: 700; color: #93a4c1 !important; letter-spacing: 0.3px; }
    .stApp .ga-iv { font-size: 1.35rem; font-weight: 900; color: var(--c) !important; line-height: 1.3; }
    .stApp .ga-in { font-size: 0.66rem; color: #64748b !important; margin-top: 2px; }
    .stApp .ga-chip { display: inline-block; margin-top: 9px; padding: 3px 11px; border-radius: 99px; font-size: 0.68rem; font-weight: 800; border: 1px solid var(--c); color: var(--c) !important; background: rgba(255,255,255,0.03); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DOSYALAR
# ==========================================
GECMIS_DOSYA = "gecmis.json"
GELECEK_DOSYA = "gelecek.json"
AYARLAR_DOSYA = "ayarlar.json"
ADMIN_SIFRE = os.environ.get("ADMIN_SIFRE", "Mg153759")


def _yukle(dosya):
    try:
        if os.path.exists(dosya):
            with open(dosya, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _kaydet(dosya, veri):
    try:
        with open(dosya, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def gecmis_yukle(): return _yukle(GECMIS_DOSYA)
def gecmis_kaydet(v): _kaydet(GECMIS_DOSYA, v)
def gelecek_yukle(): return _yukle(GELECEK_DOSYA)
def gelecek_kaydet(v): _kaydet(GELECEK_DOSYA, v)


def ayarlar_yukle():
    v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0}
    try:
        if os.path.exists(AYARLAR_DOSYA):
            with open(AYARLAR_DOSYA, "r", encoding="utf-8") as f:
                v.update(json.load(f))
    except Exception:
        pass
    return v


def ayarlar_kaydet(esikler):
    try:
        with open(AYARLAR_DOSYA, "w", encoding="utf-8") as f:
            json.dump(esikler, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    _ESIK_CACHE.clear()
    _ESIK_CACHE.update(esikler)


# ==========================================
# SABİTLER
# ==========================================
ESIK_YUKSEK = 65.0
ESIK_ORTA = 55.0
ESIK_BELIRSIZ = 50.0
MONTE_CARLO_N = 10000
MAX_GOL = 8
BELIRSIZLIK = 0.20
MAX_MAC_SINIRI = 200
_kilit = threading.Lock()
_ESIK_CACHE = {}

# Aynı anda en fazla kaç Chromium açılabilir (RAM koruması)
TARAYICI_ESZAMANLI = int(os.environ.get("TARAYICI_ESZAMANLI", "3"))
_TARAYICI_SEM = threading.Semaphore(TARAYICI_ESZAMANLI)


VARSAYILAN_VERI = {
    "ppg_ev": 0.0, "mpg_dep": 0.0, "form_str_ev": "", "form_str_dep": "",
    "siralama_ev": 0, "siralama_dep": 0, "puan_ev": 0, "puan_dep": 0,
    "xg_ev": 0.0, "xg_dep": 0.0, "atilan_ev": 0.0, "atilan_dep": 0.0,
    "yenen_ev": 0.0, "yenen_dep": 0.0, "clean_sheets_ev": 0.0, "clean_sheets_dep": 0.0,
    "team_scored_ev": 0.0, "team_scored_dep": 0.0, "team_scored_2_ev": 0.0, "team_scored_2_dep": 0.0,
    "scored_both_halves_ev": 0.0, "scored_both_halves_dep": 0.0,
    "goal_both_halves_ev": 0.0, "goal_both_halves_dep": 0.0,
    "ust05_ev": 80.0, "ust05_dep": 80.0, "ust15_ev": 50.0, "ust15_dep": 50.0,
    "ust25_ev": 30.0, "ust25_dep": 30.0, "ust35_ev": 20.0, "ust35_dep": 20.0,
    "kg_siklik_ev": 50.0, "kg_siklik_dep": 50.0, "btts_1h_ev": 0.0, "btts_1h_dep": 0.0,
    "btts_2h_ev": 0.0, "btts_2h_dep": 0.0, "btts_over15_ev": 0.0, "btts_over15_dep": 0.0,
    "btts_over25_ev": 0.0, "btts_over25_dep": 0.0,
    "tg_0_ev": 0.0, "tg_0_dep": 0.0, "tg_1_ev": 0.0, "tg_1_dep": 0.0,
    "tg_2_ev": 0.0, "tg_2_dep": 0.0, "tg_3_ev": 0.0, "tg_3_dep": 0.0,
    "tg_4_ev": 0.0, "tg_4_dep": 0.0, "tg_01_ev": 0.0, "tg_01_dep": 0.0,
    "tg_23_ev": 0.0, "tg_23_dep": 0.0, "tg_4p_ev": 0.0, "tg_4p_dep": 0.0,
    "ht_ust05_ev": 0.0, "ht_ust05_dep": 0.0, "ht_ust15_ev": 0.0, "ht_ust15_dep": 0.0,
    "ht_ust25_ev": 0.0, "ht_ust25_dep": 0.0,
    "wht_wft_ev": 0.0, "wht_wft_dep": 0.0, "wht_dft_ev": 0.0, "wht_dft_dep": 0.0,
    "wht_lft_ev": 0.0, "wht_lft_dep": 0.0, "dht_wft_ev": 0.0, "dht_wft_dep": 0.0,
    "dht_dft_ev": 0.0, "dht_dft_dep": 0.0, "dht_lft_ev": 0.0, "dht_lft_dep": 0.0,
    "lht_wft_ev": 0.0, "lht_wft_dep": 0.0, "lht_dft_ev": 0.0, "lht_dft_dep": 0.0,
    "lht_lft_ev": 0.0, "lht_lft_dep": 0.0,
    "galibiyet_ev": 30.0, "galibiyet_dep": 30.0, "beraberlik_ev": 30.0, "beraberlik_dep": 30.0,
    "maglubiyet_ev": 30.0, "maglubiyet_dep": 30.0,
    "win_1h_ev": 0.0, "win_1h_dep": 0.0, "draw_ht_ev": 0.0, "draw_ht_dep": 0.0,
    "lose_1h_ev": 0.0, "lose_1h_dep": 0.0, "win_btts_ev": 0.0, "win_btts_dep": 0.0,
    "draw_btts_ev": 0.0, "draw_btts_dep": 0.0, "lose_btts_ev": 0.0, "lose_btts_dep": 0.0,
    "win_over15_ev": 0.0, "win_over15_dep": 0.0, "lose_over15_ev": 0.0, "lose_over15_dep": 0.0,
    "takim_ev": "", "takim_dep": "", "skor_ev": 0, "skor_dep": 0, "skor_belli": False,
    "lig_ort_toplam": 0.0, "lig_ust25": 0.0, "lig_kg": 0.0,
    "saat": "", "tarih": "", "ulke": "", "format": "bilinmiyor", "kaynak_url": "",
}


# ==========================================
# SESSION STATE
# ==========================================
if "sayfa" not in st.session_state: st.session_state.sayfa = "giris"
if "form_verileri" not in st.session_state: st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
if "gecmis_analizler" not in st.session_state: st.session_state.gecmis_analizler = gecmis_yukle()
if "gelecek_analizler" not in st.session_state: st.session_state.gelecek_analizler = gelecek_yukle()
if "kayit_yapildi" not in st.session_state: st.session_state.kayit_yapildi = False
if "gelecekten_gelindi" not in st.session_state: st.session_state.gelecekten_gelindi = False
if "aktif_gelecek_idx" not in st.session_state: st.session_state.aktif_gelecek_idx = None
if "tek_silme_onay" not in st.session_state: st.session_state.tek_silme_onay = None
if "tek_silme_gelecek" not in st.session_state: st.session_state.tek_silme_gelecek = None
if "silme_onay" not in st.session_state: st.session_state.silme_onay = False
if "silme_onay_gelecek" not in st.session_state: st.session_state.silme_onay_gelecek = False
if "giris_yapildi" not in st.session_state: st.session_state.giris_yapildi = False
if "rol" not in st.session_state: st.session_state.rol = None
if "esikler" not in st.session_state: st.session_state.esikler = ayarlar_yukle()

# Global cache'e kopyala (thread'ler için)
_ESIK_CACHE.clear()
_ESIK_CACHE.update(st.session_state.esikler)


def admin_mi(): return st.session_state.get("rol") == "admin"

def esik_al(key):
    if _ESIK_CACHE:
        return _ESIK_CACHE.get(key, 50.0)
    try:
        return st.session_state.esikler.get(key, 50.0)
    except Exception:
        return 50.0

def esik_1x2_al(secim):
    km = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}
    if _ESIK_CACHE:
        return _ESIK_CACHE.get(km.get(secim, ""), 55.0)
    try:
        return st.session_state.esikler.get(km.get(secim, ""), 55.0)
    except Exception:
        return 55.0


# ==========================================
# ÜLKE BAYRAK
# ==========================================
ULKE_BAYRAK = {
    "switzerland": "🇨🇭", "isviçre": "🇨🇭", "i̇sviçre": "🇨🇭",
    "england": "🏴󠁧󠁢󠁥󠁮󠁧", "ingiltere": "🏴", "i̇ngiltere": "🏴",
    "spain": "🇪🇸", "ispanya": "🇪🇸", "italy": "🇮🇹", "italya": "🇮🇹",
    "germany": "🇩🇪", "almanya": "🇩🇪", "france": "🇫🇷", "fransa": "🇫🇷",
    "netherlands": "🇳🇱", "hollanda": "🇳🇱", "portugal": "🇵🇹", "portekiz": "🇵🇹",
    "belgium": "🇧🇪", "belçika": "🇧🇪", "turkey": "🇹🇷", "türkiye": "🇹🇷",
    "argentina": "🇦🇷", "arjantin": "🇦🇷", "brazil": "🇧🇷", "brezilya": "🇧🇷",
    "mexico": "🇲🇽", "meksika": "🇲🇽", "usa": "🇺🇸", "abd": "🇺🇸",
    "japan": "🇯🇵", "japonya": "🇯🇵", "south korea": "🇰🇷", "güney kore": "🇰🇷",
    "china": "🇨🇳", "çin": "🇨🇳", "russia": "🇷🇺", "rusya": "🇷🇺",
    "ukraine": "🇺🇦", "ukrayna": "🇺🇦", "poland": "🇵🇱", "polonya": "🇵🇱",
    "greece": "🇬🇷", "yunanistan": "🇬🇷", "scotland": "🏴", "i̇skoçya": "🏴",
    "wales": "🏴", "galler": "🏴", "ireland": "🇮🇪", "i̇rlanda": "🇮🇪",
    "austria": "🇦🇹", "avusturya": "🇦🇹", "croatia": "🇭🇷", "hırvatistan": "🇭🇷",
    "serbia": "🇷🇸", "sırbistan": "🇷🇸", "romania": "🇷🇴", "romanya": "🇷🇴",
    "bulgaria": "🇧🇬", "bulgaristan": "🇧🇬", "denmark": "🇩🇰", "danimarka": "🇩🇰",
    "sweden": "🇸🇪", "i̇sveç": "🇸🇪", "norway": "🇳🇴", "norveç": "🇳🇴",
    "finland": "🇫🇮", "finlandiya": "🇫🇮", "iceland": "🇮🇸", "i̇zlanda": "🇮🇸",
    "hungary": "🇭🇺", "macaristan": "🇭🇺", "czech": "🇨🇿", "çekya": "🇨🇿",
    "slovakia": "🇸🇰", "slovakya": "🇸🇰", "slovenia": "🇸🇮", "slovenya": "🇸🇮",
    "saudi": "🇸🇦", "suudi arabistan": "🇸🇦", "qatar": "🇶🇦", "katar": "🇶🇦",
    "egypt": "🇪🇬", "mısır": "🇪🇬", "morocco": "🇲🇦", "fas": "🇲🇦",
    "algeria": "🇩🇿", "cezayir": "🇩🇿", "tunisia": "🇹🇳", "tunus": "🇹🇳",
    "nigeria": "🇳🇬", "nijerya": "🇳🇬", "south africa": "🇿🇦", "güney afrika": "🇿🇦",
    "australia": "🇦🇺", "avustralya": "🇦🇺", "new zealand": "🇳🇿", "yeni zelanda": "🇳🇿",
    "india": "🇮🇳", "hindistan": "🇮🇳", "iran": "🇮🇷", "iraq": "🇮🇶", "irak": "🇮🇶",
    "israel": "🇮🇱", "i̇srail": "🇮🇱", "colombia": "🇨🇴", "kolombiya": "🇨🇴",
    "chile": "🇨🇱", "şili": "🇨🇱", "peru": "🇵🇪", "uruguay": "🇺🇾",
    "ecuador": "🇪🇨", "ekvador": "🇪🇨", "paraguay": "🇵🇾", "bolivia": "🇧🇴",
    "venezuela": "🇻🇪", "costa rica": "🇨🇷", "panama": "🇵🇦", "jamaica": "🇯🇲",
    "canada": "🇨🇦", "kanada": "🇨🇦", "kosovo": "🇽🇰", "kosova": "🇽🇰",
    "albania": "🇦🇱", "arnavutluk": "🇦🇱", "moldova": "🇲🇩",
    "georgia": "🇬🇪", "gürcistan": "🇬🇪", "armenia": "🇦🇲", "ermenistan": "🇦🇲",
    "azerbaijan": "🇦🇿", "azerbaycan": "🇦🇿", "kazakhstan": "🇰🇿", "kazakistan": "🇰🇿",
    "uzbekistan": "🇺🇿", "özbekistan": "🇺🇿", "belarus": "🇧🇾",
    "latvia": "🇱🇻", "letonya": "🇱🇻", "lithuania": "🇱🇹", "litvanya": "🇱🇹",
    "estonia": "🇪🇪", "estonya": "🇪🇪", "luxembourg": "🇱🇺", "lüksemburg": "🇱🇺",
    "malta": "🇲🇹", "cyprus": "🇨🇾", "kıbrıs": "🇨🇾",
    "montenegro": "🇲🇪", "karadağ": "🇲🇪", "north macedonia": "🇲🇰", "kuzey makedonya": "🇲🇰",
    "bosnia": "🇧🇦", "bosna": "🇧🇦", "liechtenstein": "🇱🇮",
}


def ulke_bayrak_bul(ulke_adi):
    if not ulke_adi: return "🌍"
    u = ulke_adi.lower().strip()
    for a in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if a in u: return ULKE_BAYRAK[a]
    return "🌍"


def _ulke_bul(metin):
    m = re.search(r'Standings\s+([^\n]+)', metin)
    if not m: return ""
    satir = m.group(1).strip()
    if not satir: return ""
    alt = satir.lower()
    for a in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if a in alt: return a
    parcalar = satir.split()
    return " ".join(parcalar[:2]) if len(parcalar) >= 2 else (parcalar[0] if parcalar else "")


def clamp(x, lo, hi): return max(lo, min(hi, x))
def ort_iki(a, b):
    v = [x for x in [a, b] if x is not None and x > 0]
    return sum(v) / len(v) if v else 0


def guven_seviyesi_bul(o):
    if o >= ESIK_YUKSEK: return ("yuksek", "🟢", "success", "Yüksek")
    if o >= ESIK_ORTA: return ("orta", "🟡", "warning", "Orta")
    if o >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "error", "Belirsiz")
    return ("cok_dusuk", "⚫", "error", "Düşük")


# ==========================================
# SAYFA ÇEKİCİ (API YOK) — Playwright + requests yedek
# ==========================================
# Not: Fonksiyon adı eski kodla uyumlu kalsın diye _scrapingbee_get olarak bırakıldı.
# Artık ScrapingBee veya herhangi bir API kullanılmıyor.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def _js_tikla_kodu(mac_sec):
    # Filtre: Last games = mac_sec (5/10/15). Ev sahibi takım = Home, deplasman takımı = Away.
    # Sayfada her takım için Home/Away/Overall var; sırayla ilk "Home" ve son "Away" seçilir.
    # Tablo içindeki hücreler (puan durumu vb.) atlanır.
    return """
    (function() {
        var macSayi = "%s";
        function ok(el) { return el.children.length <= 1 && !el.closest('table'); }
        function tikla(el) {
            try { el.click(); } catch(e) {}
            var inp = el.querySelector('input[type=radio], input[type=checkbox]');
            if (inp && !inp.checked) { try { inp.click(); } catch(e) {} }
        }
        var tum = document.querySelectorAll('label, span, div, button, a, li');
        var homes = [], aways = [];
        for (var i = 0; i < tum.length; i++) {
            var t = (tum[i].textContent || '').trim();
            if (!ok(tum[i])) continue;
            if (t === macSayi) tikla(tum[i]);
            else if (t === 'Home') homes.push(tum[i]);
            else if (t === 'Away') aways.push(tum[i]);
        }
        if (homes.length) tikla(homes[0]);
        if (aways.length) tikla(aways[aways.length - 1]);
        return true;
    })()
    """ % mac_sec


def _son_n_oku(metin):
    m = re.search(r'Last\s+(\d+)\s+games', metin or "")
    return int(m.group(1)) if m else None


def _playwright_html(url, mac_sec, timeout, dogrula=False):
    from playwright.sync_api import sync_playwright
    js_kod = _js_tikla_kodu(mac_sec)
    hedef = int(mac_sec) if str(mac_sec).isdigit() else None
    with _TARAYICI_SEM:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
            try:
                ctx = b.new_context(user_agent=UA, locale="en-US")
                pg = ctx.new_page()
                # Hız/RAM için resim, medya, font yükleme
                pg.route("**/*", lambda route: route.abort()
                         if route.request.resource_type in ("image", "media", "font")
                         else route.continue_())
                pg.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
                try:
                    pg.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    pass
                pg.wait_for_timeout(3000)
                pg.evaluate(js_kod)
                pg.wait_for_timeout(3500)

                if dogrula and hedef:
                    n = _son_n_oku(pg.inner_text("body"))
                    # Sayfa "Last 10 games" diyorsa filtre uygulanmamış demektir: gerçek tıklamayla tekrar dene
                    if n is not None and n != hedef:
                        try:
                            for el in pg.get_by_text(str(hedef), exact=True).all()[:20]:
                                try:
                                    if el.evaluate("e => !!e.closest('table')"):
                                        continue
                                    el.click(timeout=1500)
                                except Exception:
                                    pass
                            pg.wait_for_timeout(1500)
                            pg.evaluate(js_kod)
                            pg.wait_for_timeout(3000)
                        except Exception:
                            pass
                        n = _son_n_oku(pg.inner_text("body"))
                    if n is not None and n != hedef:
                        raise RuntimeError(f"{hedef} maç filtresi uygulanamadı (sayfa: Last {n} games)")
                return pg.content()
            finally:
                try: b.close()
                except Exception: pass


def _scrapingbee_get(url, render_js=True, timeout=90, mac_sec="5", max_retry=3, dogrula=False):
    son_hata = None

    # --- Aşama 1: gerçek tarayıcı (veriler eskisiyle birebir aynı) ---
    try:
        import playwright  # noqa: F401
        playwright_var = True
    except ImportError:
        playwright_var = False
        son_hata = "playwright kurulu değil"

    if playwright_var:
        for deneme in range(max_retry):
            try:
                html = _playwright_html(url, mac_sec, timeout, dogrula)
                if html and len(html) > 500:
                    return html, None
                son_hata = "Boş sayfa"
            except Exception as e:
                son_hata = f"Tarayıcı hatası: {str(e)[:150]}"
            if deneme < max_retry - 1:
                time.sleep(2 + deneme * 2)

    # --- Aşama 2: yedek, düz requests (JS tıklamaları olmaz => varsayılan 10 maç gelir) ---
    # Maç filtresi doğrulanması istenen sayfalarda bu yedek KULLANILMAZ, yanlış veri yerine hata döner.
    if dogrula:
        return None, son_hata or "Filtre uygulanamadı"
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=30)
        if r.status_code == 200 and r.text:
            return r.text, None
        son_hata = f"HTTP {r.status_code}" + (f" | {son_hata}" if son_hata else "")
    except Exception as e:
        son_hata = f"Bağlantı hatası: {str(e)[:100]}" + (f" | {son_hata}" if son_hata else "")

    return None, son_hata or "Sayfa alınamadı."


def _html_metne_cevir(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe"]): tag.decompose()
    for td in soup.find_all(["td", "th"]): td.insert_after("\t")
    for tr in soup.find_all("tr"): tr.insert_after("\n")
    for e in soup.find_all(["div", "p", "li", "h1", "h2", "h3", "h4", "br"]): e.insert_after("\n")
    metin = soup.get_text(separator="", strip=False)
    metin = re.sub(r'[ \t]+\n', '\n', metin)
    metin = re.sub(r'\n{3,}', '\n\n', metin)
    return metin


def mutating_ana_sayfa_linklerini_al(max_mac=MAX_MAC_SINIRI):
    html, hata = _scrapingbee_get("https://www.mutating.com/football-stats/", render_js=True)
    if hata: return [], [hata]
    if not html: return [], ["Ana sayfa indirilemedi."]
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gorulen = set()
    for link in soup.find_all("a", href=True):
        if len(maclar) >= max_mac: break
        href = link.get("href", "")
        if not any(x in href for x in ["match-preview", "match/", "/stats/"]): continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gorulen: continue
        gorulen.add(href)
        h2_list = link.find_all("h2")
        takim_ev = h2_list[0].get_text(strip=True) if len(h2_list) > 0 else ""
        takim_dep = h2_list[1].get_text(strip=True) if len(h2_list) > 1 else ""
        saat_el = link.find(class_=re.compile(r"nostart|time|match-time"))
        saat = saat_el.get_text(strip=True) if saat_el else ""
        maclar.append({"url": href, "takim_ev": takim_ev, "takim_dep": takim_dep, "saat": saat})
    return maclar, []


def mutating_mac_detay_cek(url):
    html, hata = _scrapingbee_get(url, render_js=True, mac_sec="5", dogrula=True)
    if hata: return None, [hata]
    if not html: return None, ["Sayfa indirilemedi."]
    return _mac_html_parse(html, url)


def _mac_html_parse(html, url=""):
    soup = BeautifulSoup(html, "html.parser")
    veri = {}; okunamayanlar = []
    h1 = soup.find("h1")
    if h1:
        baslik = h1.get_text(strip=True)
        if " - " in baslik:
            p = baslik.replace(" Stats", "").replace(" stats", "").split(" - ")
            veri["takim_ev"] = p[0].strip()
            if len(p) > 1: veri["takim_dep"] = p[1].strip()
    metin = _html_metne_cevir(html)
    veri["son_n"] = _son_n_oku(metin)
    m = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', metin)
    if m: veri["tarih"] = m.group(1)
    m = re.search(r'(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1)
    veri["ulke"] = _ulke_bul(metin)

    skor_ev = skor_dep = None
    m = re.search(r'FT\s*\n+\s*(\d{1,2})\s*[-:]\s*(\d{1,2})', metin)
    if m:
        skor_ev = int(m.group(1)); skor_dep = int(m.group(2))
    if skor_ev is not None:
        veri["skor_ev"] = skor_ev; veri["skor_dep"] = skor_dep; veri["skor_belli"] = True
    else:
        veri["skor_belli"] = False

    def _cift(label):
        for pat in [
            r'([\d.,]+)\s*%?\s*\t\s*' + re.escape(label) + r'\s*\t\s*([\d.,]+)',
            r'([\d.,]+)\s*%?\s*\|\s*' + re.escape(label) + r'\s*\|\s*([\d.,]+)',
            r'([\d.,]+)\s*%?\s+' + re.escape(label) + r'\s+([\d.,]+)\s*%?',
            r'([\d.,]+)\s*%?\s*\n\s*' + re.escape(label) + r'\s*\n\s*([\d.,]+)',
        ]:
            mm = re.search(pat, metin, re.IGNORECASE)
            if mm:
                try: return float(mm.group(1).replace(",", ".")), float(mm.group(2).replace(",", "."))
                except ValueError: continue
        return None, None

    for label, k_ev, k_dep in [
        ("Goals scored per game", "atilan_ev", "atilan_dep"),
        ("Goals conceded per game", "yenen_ev", "yenen_dep"),
        ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"),
        ("Team scored", "team_scored_ev", "team_scored_dep"),
        ("Both Teams to Score", "kg_siklik_ev", "kg_siklik_dep"),
        ("Over 2.5 goals", "ust25_ev", "ust25_dep"),
        ("Over 1.5 goals", "ust15_ev", "ust15_dep"),
        ("Over 3.5 goals", "ust35_ev", "ust35_dep"),
    ]:
        a, b = _cift(label)
        if a is not None and veri.get(k_ev, 0) == 0:
            veri[k_ev] = a; veri[k_dep] = b

    for label, k_ev, k_dep in [("Win", "galibiyet_ev", "galibiyet_dep"), ("Draw", "beraberlik_ev", "beraberlik_dep"), ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
        mm = re.search(r'([\d.,]+)\s*%\s*\t\s*' + label + r'\s*\t\s*([\d.,]+)\s*%', metin, re.MULTILINE)
        if mm:
            try:
                veri[k_ev] = float(mm.group(1).replace(",", "."))
                veri[k_dep] = float(mm.group(2).replace(",", "."))
            except ValueError: pass

    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) + veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2

    veri["format"] = "mutating"
    if url: veri["kaynak_url"] = url
    if not veri.get("takim_ev"): okunamayanlar.append("Takım isimleri (Ev)")
    if not veri.get("takim_dep"): okunamayanlar.append("Takım isimleri (Dep)")
    if veri.get("atilan_ev", 0) == 0: okunamayanlar.append("Atılan Gol (Ev)")
    if veri.get("yenen_ev", 0) == 0: okunamayanlar.append("Yenen Gol (Ev)")
    return veri, okunamayanlar


def _mac_tahmin_var_mi(v):
    try:
        a = analiz_hesapla(v)
        s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
        if y1 >= esik_1x2_al(s1): return True
        if a["ust_25"] >= esik_al("ust") and a["ust_25"] >= a["alt_25"]: return True
        if a["alt_25"] >= esik_al("alt") and a["alt_25"] >= a["ust_25"]: return True
        if a["kg_var_model"] >= esik_al("kg_var") and a["kg_var_model"] >= a["kg_yok_model"]: return True
        if a["kg_yok_model"] >= esik_al("kg_yok") and a["kg_yok_model"] >= a["kg_var_model"]: return True
        return False
    except Exception:
        return False


# ==========================================
# GELECEK MAÇ (Paralel + Retry)
# ==========================================
def _gelecek_mac_isle(mac, mevcut_urls):
    try:
        veri, _ = mutating_mac_detay_cek(mac["url"])
        if not veri:
            return ("hata", mac, "Veri çekilemedi")
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        if not veri.get("saat"): veri["saat"] = mac.get("saat", "")
        veri["kaynak_url"] = mac["url"]
        if mac["url"] in mevcut_urls:
            return ("atlandi", veri, "Zaten var")
        if _mac_tahmin_var_mi(veri):
            kayit = kayit_olustur(veri, analiz_hesapla(veri))
            with _kilit:
                st.session_state.gelecek_analizler.append(kayit)
                gelecek_kaydet(st.session_state.gelecek_analizler)
            return ("eklendi", veri, "Gelecek'e eklendi")
        return ("atlandi", veri, "Tahmin yok")
    except Exception as e:
        return ("hata", mac, str(e))


def mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=None, max_workers=2):
    maclar, hatalar = mutating_ana_sayfa_linklerini_al(max_mac=max_mac)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Ana sayfada maç linki bulunamadı."]

    mevcut_urls = set()
    for g in st.session_state.gelecek_analizler:
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut_urls.add(u)

    basarili = []; hatali = []
    eklenen = 0; atlanan = 0; tamamlanan = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_gelecek_mac_isle, m, mevcut_urls): m for m in maclar}
        for fut in as_completed(futures):
            tamamlanan += 1
            mac = futures[fut]
            try:
                sonuc, veri, mesaj = fut.result()
                if sonuc == "eklendi":
                    eklenen += 1; basarili.append(veri)
                elif sonuc == "atlandi":
                    atlanan += 1; basarili.append(veri)
                else:
                    hatali.append(f"{mac.get('takim_ev','?')}: {mesaj}")
            except Exception as e:
                hatali.append(f"{mac.get('takim_ev','?')}: {e}")
            if progress_callback:
                try: progress_callback(tamamlanan - 1, len(maclar), mac.get("takim_ev", ""))
                except Exception: pass

    st.session_state.toplu_cek_ozet = {"eklenen": eklenen, "atlanan": atlanan, "toplam": len(basarili)}
    return basarili, hatali


# ==========================================
# LİG SAYFASI → SON N MAÇ → GEÇMİŞ
# ==========================================
def _lig_son_mac_linklerini_al(lig_url, adet=10):
    html, hata = _scrapingbee_get(lig_url, render_js=True, mac_sec="10")
    if hata: return [], [hata]
    if not html: return [], ["Lig sayfası indirilemedi."]
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gorulen = set()
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        if "match-preview" not in href: continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gorulen: continue
        gorulen.add(href)
        takim_ev = ""; takim_dep = ""
        img = link.find_all("img", alt=True)
        if len(img) >= 2:
            takim_ev = img[0].get("alt", "").strip()
            takim_dep = img[1].get("alt", "").strip()
        if not takim_ev:
            txt = link.get_text(" ", strip=True)
            if " - " in txt:
                p = txt.split(" - ")
                takim_ev = p[0].strip(); takim_dep = p[1].strip() if len(p) > 1 else ""
        maclar.append({"url": href, "takim_ev": takim_ev, "takim_dep": takim_dep})
        if len(maclar) >= adet: break
    return maclar, []


def _gecmis_mac_isle(mac, mevcut_urls):
    try:
        if mac["url"] in mevcut_urls:
            return ("atlandi", None, "Zaten var")
        html, hata = _scrapingbee_get(mac["url"], render_js=True, mac_sec="5", dogrula=True)
        if hata or not html:
            return ("hata", mac, hata or "HTML yok")
        veri, _ = _mac_html_parse(html, mac["url"])
        if not veri.get("skor_belli", False):
            return ("atlandi", None, "Skor yok (bitmemiş maç)")
        if veri.get("atilan_ev", 0) == 0 or veri.get("yenen_ev", 0) == 0:
            return ("atlandi", None, "İstatistik eksik")
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")

        yv = copy.deepcopy(VARSAYILAN_VERI); yv.update(veri)
        kayit = kayit_olustur(yv, analiz_hesapla(yv))
        kayit["dogruluk"] = sonuc_hesapla(kayit)
        with _kilit:
            st.session_state.gecmis_analizler.append(kayit)
            gecmis_kaydet(st.session_state.gecmis_analizler)
        return ("eklendi", veri, f"{veri['skor_ev']}-{veri['skor_dep']}")
    except Exception as e:
        return ("hata", mac, str(e))


def lig_gecmis_cek(lig_url, adet=10, max_workers=2, progress_callback=None):
    maclar, hatalar = _lig_son_mac_linklerini_al(lig_url, adet=adet)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Lig sayfasında maç linki bulunamadı."]

    mevcut_urls = set()
    for g in st.session_state.gecmis_analizler:
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut_urls.add(u)

    basarili = []; hatali = []
    eklenen = 0; atlanan = 0; tamamlanan = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_gecmis_mac_isle, m, mevcut_urls): m for m in maclar}
        for fut in as_completed(futures):
            tamamlanan += 1
            mac = futures[fut]
            try:
                sonuc, veri, mesaj = fut.result()
                if sonuc == "eklendi":
                    eklenen += 1; basarili.append(veri)
                elif sonuc == "atlandi":
                    atlanan += 1
                else:
                    hatali.append(f"{mac.get('takim_ev','?')}: {mesaj}")
            except Exception as e:
                hatali.append(f"{mac.get('takim_ev','?')}: {e}")
            if progress_callback:
                try: progress_callback(tamamlanan - 1, len(maclar), mac.get("takim_ev", ""))
                except Exception: pass

    st.session_state.gecmis_cek_ozet = {"eklenen": eklenen, "atlanan": atlanan}
    return basarili, hatali


# ==========================================
# BİTEN MAÇLARIN SKORUNU ÇEK → GEÇMİŞE AKTAR
# ==========================================
def _skor_parse(html):
    metin = _html_metne_cevir(html)
    m = re.search(r'(?<![A-Za-z])FT\s*\n+\s*(\d{1,2})\s*[-:]\s*(\d{1,2})', metin)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def _skor_cek(url, tarayici_yedek=False):
    """(skor veya None, hata veya None). Önce hızlı requests, istenirse tarayıcı yedeği."""
    html = None; hata = None
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=30)
        if r.status_code == 200 and r.text:
            html = r.text
        else:
            hata = f"HTTP {r.status_code}"
    except Exception as e:
        hata = f"Bağlantı: {str(e)[:80]}"
    skor = _skor_parse(html) if html else None
    if skor is None and tarayici_yedek:
        h2, hata2 = _scrapingbee_get(url, render_js=True, mac_sec="5")
        if h2:
            skor = _skor_parse(h2); hata = None
        elif hata2:
            hata = hata2
    if skor is None and html:
        hata = None  # sayfa alındı ama skor yok = maç bitmemiş
    return skor, hata


def sonuclari_isle(tarayici_yedek=False, max_workers=3, progress_callback=None):
    gel = st.session_state.gelecek_analizler
    isler = [(i, g) for i, g in enumerate(gel) if g.get("veri", {}).get("kaynak_url")]
    sonuc = {}
    tamam = 0
    if isler:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            fut = {ex.submit(_skor_cek, g["veri"]["kaynak_url"], tarayici_yedek): (i, g) for i, g in isler}
            for f in as_completed(fut):
                i, g = fut[f]; tamam += 1
                try: sonuc[i] = f.result()
                except Exception as e: sonuc[i] = (None, str(e)[:80])
                if progress_callback:
                    try: progress_callback(tamam - 1, len(isler), g["veri"].get("takim_ev", ""))
                    except Exception: pass

    mevcut = {x.get("veri", {}).get("kaynak_url") for x in st.session_state.gecmis_analizler}
    tasinan = 0; bitmemis = 0; hatalar = []; kalan = []
    for i, g in enumerate(gel):
        r = sonuc.get(i)
        if r is None:
            kalan.append(g); continue
        skor, hata = r
        v = g["veri"]; isim = f"{v.get('takim_ev', '?')} - {v.get('takim_dep', '?')}"
        if hata:
            hatalar.append(f"{isim}: {hata}"); kalan.append(g); continue
        if skor is None:
            bitmemis += 1; kalan.append(g); continue
        v["skor_ev"], v["skor_dep"], v["skor_belli"] = skor[0], skor[1], True
        d = sonuc_hesapla(g)
        if d: g["dogruluk"] = d
        if v.get("kaynak_url") not in mevcut:
            st.session_state.gecmis_analizler.append(g)
            mevcut.add(v.get("kaynak_url"))
        tasinan += 1

    st.session_state.gelecek_analizler = kalan
    st.session_state.aktif_gelecek_idx = None
    st.session_state.gelecekten_gelindi = False
    gecmis_kaydet(st.session_state.gecmis_analizler)
    gelecek_kaydet(st.session_state.gelecek_analizler)
    return {"tasinan": tasinan, "bitmemis": bitmemis, "hatalar": hatalar, "toplam": len(isler)}


# ==========================================
# SPORTYTRADER PARSER (metin yapıştırma)
# ==========================================
def _cift_tab(etiket, blok):
    for pat in [
        r'([\d.,]+)%?\s*\t\s*' + re.escape(etiket) + r'\s*\t\s*([\d.,]+)%?',
        r'([\d.,]+)%?\s{1,4}' + re.escape(etiket) + r'\s{1,4}([\d.,]+)%?',
    ]:
        m = re.search(pat, blok, re.IGNORECASE)
        if m:
            try: return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
            except ValueError: pass
    return None, None


def sportytrader_veri_cikar(metin):
    veri = {}; okunamayanlar = []
    m = re.search(r'^([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s*-\s*([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s+Stats', metin, re.MULTILINE)
    if m:
        veri["takim_ev"] = m.group(1).strip(); veri["takim_dep"] = m.group(2).strip()
    m = re.search(r'Time\s*\t\s*(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1).strip()
    m = re.search(r'Date\s*\t\s*(\d{1,2}\.\d{1,2}\.\d{2,4})', metin)
    if m: veri["tarih"] = m.group(1).strip()
    veri["ulke"] = _ulke_bul(metin)
    m = re.search(r'FT\s*\r?\n\s*(\d+)\s*-\s*(\d+)', metin)
    if m:
        veri["skor_ev"] = int(m.group(1)); veri["skor_dep"] = int(m.group(2)); veri["skor_belli"] = True
    else:
        veri["skor_belli"] = False
    idx = metin.find("Main Stats")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for label, k_ev, k_dep in [("Goals scored per game", "atilan_ev", "atilan_dep"), ("Goals conceded per game", "yenen_ev", "yenen_dep"), ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"), ("Team scored", "team_scored_ev", "team_scored_dep")]:
            a, b = _cift_tab(label, blok)
            if a is not None: veri[k_ev] = a; veri[k_dep] = b
    idx = metin.find("Over Under Goals")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for label, k_ev, k_dep in [("Over 0.5 goals", "ust05_ev", "ust05_dep"), ("Over 1.5 goals", "ust15_ev", "ust15_dep"), ("Over 2.5 goals", "ust25_ev", "ust25_dep"), ("Over 3.5 goals", "ust35_ev", "ust35_dep")]:
            a, b = _cift_tab(label, blok)
            if a is not None: veri[k_ev] = a; veri[k_dep] = b
    idx = metin.find("Both Teams to Score")
    if idx != -1:
        blok = metin[idx:idx+1500]
        mm = re.search(r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*Both Teams to Score\s*\t\s*([\d.,]+)%', blok, re.MULTILINE)
        if mm:
            try:
                veri["kg_siklik_ev"] = float(mm.group(1).replace(",", "."))
                veri["kg_siklik_dep"] = float(mm.group(2).replace(",", "."))
            except ValueError: pass
    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) + veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2
    veri["format"] = "sportytrader"
    if not veri.get("takim_ev"): okunamayanlar.append("Takım isimleri (Ev)")
    if not veri.get("takim_dep"): okunamayanlar.append("Takım isimleri (Dep)")
    return veri, okunamayanlar


def metinden_veri_cikar(metin):
    metin = metin.replace(",", ".")
    if "Main Stats" in metin and "Goals scored per game" in metin:
        return sportytrader_veri_cikar(metin)
    return {"format": "genel"}, []


# ==========================================
# POISSON & MODEL
# ==========================================
def poisson_pmf(k, lam):
    if lam <= 0: return 1.0 if k == 0 else 0.0
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)


def poisson_random(lam, rng=None):
    r = rng if rng is not None else random
    if lam <= 0: return 0
    L = math.exp(-lam); k = 0; p = 1.0
    while True:
        k += 1; p *= r.random()
        if p <= L: return k - 1


def poisson_matris(lam_ev, lam_dep, mg=MAX_GOL):
    return [[poisson_pmf(i, lam_ev) * poisson_pmf(j, lam_dep) for j in range(mg)] for i in range(mg)]


def hesapla_lambda(v):
    at_e = v.get("atilan_ev", 0.0); ye = v.get("yenen_ev", 0.0)
    at_d = v.get("atilan_dep", 0.0); yd = v.get("yenen_dep", 0.0)
    xg_e = v.get("xg_ev", 0.0); xg_d = v.get("xg_dep", 0.0)
    h_ev = (xg_e * 0.60 + at_e * 0.40) if xg_e > 0 else (at_e if at_e > 0 else 1.2)
    h_dep = (xg_d * 0.60 + at_d * 0.40) if xg_d > 0 else (at_d if at_d > 0 else 1.0)
    ts_e = v.get("team_scored_ev", 0); ts_d = v.get("team_scored_dep", 0)
    if ts_e > 0: h_ev *= clamp(ts_e / 60, 0.7, 1.3)
    if ts_d > 0: h_dep *= clamp(ts_d / 60, 0.7, 1.3)
    sd = yd if yd > 0 else 1.2
    se = ye if ye > 0 else 1.0
    cs_e = v.get("clean_sheets_ev", 0.0); cs_d = v.get("clean_sheets_dep", 0.0)
    def cf(cs):
        if cs <= 0: return 1.0
        if cs < 40.0: return 1.0 - (cs / 250.0)
        return max(0.40, 0.84 - (cs - 40.0) * (0.44 / 60.0))
    df = cf(cs_e); ef = cf(cs_d)
    le_h = h_ev * 0.60 + sd * 0.40
    ld_h = h_dep * 0.60 + se * 0.40
    u25e = v.get("ust25_ev", 0); u25d = v.get("ust25_dep", 0)
    if u25e > 0: le_h *= clamp(u25e / 50, 0.85, 1.15)
    if u25d > 0: ld_h *= clamp(u25d / 50, 0.85, 1.15)
    kg_e = v.get("kg_siklik_ev", 0); kg_d = v.get("kg_siklik_dep", 0)
    if kg_e > 0 and kg_d > 0:
        kg_ort = (kg_e + kg_d) / 2
        if kg_ort >= 60: le_h *= 1.05; ld_h *= 1.05
        elif kg_ort <= 35: le_h *= 0.95; ld_h *= 0.95
    fe = clamp(1 + (v.get("ppg_ev", 1.5) - 1.5) / 15, 0.85, 1.15)
    fd = clamp(1 + (v.get("mpg_dep", 1.5) - 1.5) / 15, 0.85, 1.15)
    se_s = v.get("siralama_ev", 10); sd_s = v.get("siralama_dep", 10)
    dom = 1.0
    if 1 <= se_s <= 5 and sd_s >= 10: dom = 1.20
    ge = v.get("galibiyet_ev", 0); gd = v.get("galibiyet_dep", 0)
    if ge > 0 and gd > 0:
        if ge - gd >= 25: le_h *= 1.08; ld_h *= 0.95
        elif gd - ge >= 25: le_h *= 0.95; ld_h *= 1.08
    le = le_h * 1.05 * fe * ef * dom
    ld = ld_h * 0.95 * fd * df
    if le > 2.50: le = 2.50 + (le - 2.50) * 0.5
    if ld > 2.50: ld = 2.50 + (ld - 2.50) * 0.5
    return clamp(le, 0.05, 4.5), clamp(ld, 0.05, 4.5), 0.80


def matristen_olasilik(matris, mg=MAX_GOL):
    p1 = px = p2 = 0.0
    u05 = u15 = u25 = u35 = 0.0
    kg = 0.0; sk = {}; tot = 0.0
    for i in range(mg):
        for j in range(mg):
            p = matris[i][j]; tot += p
            if i > j: p1 += p
            elif i == j: px += p
            else: p2 += p
            tg = i + j
            if tg > 0.5: u05 += p
            if tg > 1.5: u15 += p
            if tg > 2.5: u25 += p
            if tg > 3.5: u35 += p
            if i > 0 and j > 0: kg += p
            sk[f"{i}-{j}"] = p
    return {"1": p1, "X": px, "2": p2, "ust_05": u05, "ust_15": u15, "ust_25": u25, "ust_35": u35, "kg_var": kg, "skorlar": sk, "toplam": tot}


def mac_ici_sok(le, ld, rng=None):
    r = rng if rng is not None else random
    if r.random() < 0.03:
        if r.random() < 0.5: le *= 0.70
        else: ld *= 0.70
    return le, ld


def monte_carlo(le_b, ld_b, n=MONTE_CARLO_N):
    seed = int(round(le_b * 1_000_000)) * 1_000_003 + int(round(ld_b * 1_000_000))
    rng = random.Random(seed)
    s = {"1": 0, "X": 0, "2": 0, "u25": 0, "kg": 0}
    for _ in range(n):
        le = le_b * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        ld = ld_b * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        le, ld = mac_ici_sok(le, ld, rng)
        eg = min(MAX_GOL - 1, poisson_random(le, rng))
        dg = min(MAX_GOL - 1, poisson_random(ld, rng))
        if eg > dg: s["1"] += 1
        elif eg == dg: s["X"] += 1
        else: s["2"] += 1
        if eg + dg > 2.5: s["u25"] += 1
        if eg > 0 and dg > 0: s["kg"] += 1
    def yz(x): return x / n * 100 if n > 0 else 0
    return {"p1": yz(s["1"]), "px": yz(s["X"]), "p2": yz(s["2"]), "ust25": yz(s["u25"]), "alt25": 100 - yz(s["u25"]), "kg_var": yz(s["kg"]), "kg_yok": 100 - yz(s["kg"]), "n": n}


def analiz_hesapla(v):
    le, ld, gv = hesapla_lambda(v)
    matris = poisson_matris(le, ld, MAX_GOL)
    o = matristen_olasilik(matris, MAX_GOL)
    tot = o["toplam"] or 1
    p1p = o["1"] / tot * 100; pxp = o["X"] / tot * 100; p2p = o["2"] / tot * 100
    u25p = o["ust_25"] / tot * 100; kgp = o["kg_var"] / tot * 100
    mc = monte_carlo(le, ld, MONTE_CARLO_N)
    lu = v.get("lig_ust25", 0.0); lk = v.get("lig_kg", 0.0)
    p1 = p1p * 0.60 + mc["p1"] * 0.40
    px = pxp * 0.60 + mc["px"] * 0.40
    p2 = p2p * 0.60 + mc["p2"] * 0.40
    ge = v.get("galibiyet_ev", 0); gd = v.get("galibiyet_dep", 0)
    if ge > 0 and gd > 0:
        p1 = p1 * 0.85 + ge * 0.15; p2 = p2 * 0.85 + gd * 0.15
    be = v.get("beraberlik_ev", 0); bd = v.get("beraberlik_dep", 0)
    if be > 0 and bd > 0:
        px = px * 0.85 + ((be + bd) / 2) * 0.15
    t = p1 + px + p2
    if t > 0: p1, px, p2 = (p1 / t) * 100, (px / t) * 100, (p2 / t) * 100
    u25 = u25p * 0.60 + lu * 0.10 + mc["ust25"] * 0.30 if lu > 0 else u25p * 0.65 + mc["ust25"] * 0.35
    kgm = kgp * 0.40 + lk * 0.30 + mc["kg_var"] * 0.30 if lk > 0 else kgp * 0.60 + mc["kg_var"] * 0.40
    kge = v.get("kg_siklik_ev", 0); kgd = v.get("kg_siklik_dep", 0)
    if kge > 0 and kgd > 0:
        kgm = kgm * 0.85 + ((kge + kgd) / 2) * 0.15
    tbg = le + ld
    if tbg < 1.80:
        bf = (1.80 - tbg) / 1.80
        u25 = max(10.0, u25 * (1.0 - bf * 0.8))
        kgm = max(15.0, kgm * (1.0 - bf * 0.9))
    kgy = 100.0 - kgm; alt = 100.0 - u25
    eo = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    eg = max([("1X", p1 + px), ("X2", p2 + px), ("12", p1 + p2)], key=lambda x: x[1])
    return {
        "lam_ev": le, "lam_dep": ld, "guven": gv,
        "p1": p1, "px": px, "p2": p2,
        "ust_25": u25, "alt_25": alt, "kg_var_model": kgm, "kg_yok_model": kgy,
        "en_olasi": eo, "en_guvenli": eg,
        "en_olasi_gol": "Üst" if u25 > alt else "Alt",
        "en_olasi_kg": "Var" if kgm > kgy else "Yok",
    }


def kayit_olustur(v, a):
    return {"veri": copy.deepcopy(v), "analiz": {
        "p1": a["p1"], "px": a["px"], "p2": a["p2"],
        "tahmini_gol": a["lam_ev"] + a["lam_dep"],
        "kg_var_model": a["kg_var_model"], "ust_25": a["ust_25"],
        "en_olasi_1x2": a["en_olasi"][0], "en_guvenli_cifte": a["en_guvenli"][0],
        "en_olasi_gol": a["en_olasi_gol"], "en_olasi_kg": a["en_olasi_kg"]}}


def sonuc_hesapla(kayit):
    v = kayit["veri"]; a = kayit.get("analiz", {})
    if not v.get("skor_belli", False): return None
    se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    tg = se + sd
    gu = tg > 2.5
    gk = (se > 0 and sd > 0)
    g1 = "1" if se > sd else ("X" if se == sd else "2")
    u25 = a.get("ust_25", 50); alt = 100 - u25
    kgv = a.get("kg_var_model", 50); kgy = 100 - kgv
    p1a = a.get("p1", 33.33); pxa = a.get("px", 33.33); p2a = a.get("p2", 33.34)
    s1x2, y1x2 = max([("1", p1a), ("X", pxa), ("2", p2a)], key=lambda x: x[1])
    o1 = s1x2 if y1x2 >= esik_1x2_al(s1x2) else None
    og = None
    if u25 >= esik_al("ust") and u25 >= alt: og = "Üst"
    elif alt >= esik_al("alt") and alt >= u25: og = "Alt"
    okg = None
    if kgv >= esik_al("kg_var") and kgv >= kgy: okg = "Var"
    elif kgy >= esik_al("kg_yok") and kgy >= kgv: okg = "Yok"
    def _t(o, g):
        if o is None: return None, None
        d = "tam" if o == g else "yanlis"
        return d == "tam", d
    t1, d1 = _t(o1, g1)
    tg_, dg_ = _t(og, "Üst" if gu else "Alt")
    tk, dk = _t(okg, "Var" if gk else "Yok")
    return {
        "oneri_1x2": {"tahmin": o1, "tuttu": t1, "durum": d1},
        "oneri_gol": {"tahmin": og, "tuttu": tg_, "durum": dg_},
        "oneri_kg": {"tahmin": okg, "tuttu": tk, "durum": dk},
        "gercek_1x2": g1, "gercek_gol": "Üst" if gu else "Alt", "gercek_kg": "Var" if gk else "Yok",
    }


def test_hesapla(kayitlar, e):
    """Geçmiş maçları verilen eşiklerle değerlendirir (kayıtlı analiz değerlerini kullanır)."""
    isimler = ["1", "X", "2", "Üst", "Alt", "KG Var", "KG Yok"]
    st_ = {k: [0, 0] for k in isimler}  # [tahmin sayısı, tutan]
    satirlar = []
    for g in kayitlar:
        v = g.get("veri", {}); a = g.get("analiz", {})
        se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
        g1 = "1" if se > sd else ("X" if se == sd else "2")
        gg = "Üst" if se + sd > 2.5 else "Alt"
        gk = "KG Var" if (se > 0 and sd > 0) else "KG Yok"

        p1 = a.get("p1", 33.33); px = a.get("px", 33.33); p2 = a.get("p2", 33.34)
        s1, y1 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        t1 = {"1": e["esik_1"], "X": e["esik_x"], "2": e["esik_2"]}[s1]
        o1 = s1 if y1 >= t1 else None

        u25 = a.get("ust_25", 50.0); alt = 100 - u25
        og = None
        if u25 >= e["ust"] and u25 >= alt: og = "Üst"
        elif alt >= e["alt"] and alt >= u25: og = "Alt"

        kgv = a.get("kg_var_model", 50.0); kgy = 100 - kgv
        ok = None
        if kgv >= e["kg_var"] and kgv >= kgy: ok = "KG Var"
        elif kgy >= e["kg_yok"] and kgy >= kgv: ok = "KG Yok"

        d1 = dg = dk = None
        if o1:
            d1 = (o1 == g1); st_[o1][0] += 1; st_[o1][1] += int(d1)
        if og:
            dg = (og == gg); st_[og][0] += 1; st_[og][1] += int(dg)
        if ok:
            dk = (ok == gk); st_[ok][0] += 1; st_[ok][1] += int(dk)
        satirlar.append({"ev": v.get("takim_ev", "Ev"), "dep": v.get("takim_dep", "Dep"),
                         "skor": f"{se}-{sd}", "o1": o1, "d1": d1, "og": og, "dg": dg, "ok": ok, "dk": dk})
    return st_, satirlar


def _ga_renk(pc):
    if pc is None: return "#64748b"
    if pc >= 70: return "#22c55e"
    if pc >= 55: return "#f59e0b"
    return "#ef4444"


def ozet_html(ist):
    """test_hesapla çıktısını modern kartlara çevirir (1X2 / Gol / KG)."""
    def _pc(n, h): return (h / n * 100) if n else None

    def _yorum(pc):
        if pc is None: return "veri yok"
        if pc >= 80: return "Mükemmel"
        if pc >= 70: return "Çok iyi"
        if pc >= 60: return "İyi"
        if pc >= 50: return "Orta"
        return "Zayıf"

    def _item(lbl, n, h):
        pc = _pc(n, h)
        pt = f"%{pc:.0f}" if pc is not None else "—"
        return (f'<div class="ga-item" style="--c:{_ga_renk(pc)}"><div class="ga-il">{_e(lbl)}</div>'
                f'<div class="ga-iv">{pt}</div><div class="ga-in">{h}/{n}</div></div>')

    def _card(ikon, baslik, keys, etiketler):
        n = sum(ist[k][0] for k in keys); h = sum(ist[k][1] for k in keys)
        pc = _pc(n, h); renk = _ga_renk(pc)
        pt = f"{pc:.0f}" if pc is not None else "0"
        items = "".join(_item(et, *ist[k]) for k, et in zip(keys, etiketler))
        return (f'<div class="ga-card" style="--c:{renk}"><div class="ga-glow"></div>'
                f'<div class="ga-head"><div><div class="ga-title">{ikon} {_e(baslik)}</div>'
                f'<div class="ga-sub">{h} tuttu • {n - h} tutmadı • {n} tahmin</div></div>'
                f'<div><span class="ga-big">{pt}</span><span class="ga-pctsign">%</span></div></div>'
                f'<div class="ga-bar"><div class="ga-fill" style="width:{pt}%"></div></div>'
                f'<div class="ga-items">{items}</div>'
                f'<div class="ga-chip">● {_e(_yorum(pc))}</div></div>')

    return ('<div class="ga-wrap">'
            + _card("🎯", "1X2 Toplam", ["1", "X", "2"], ["1 (Ev)", "X (Ber)", "2 (Dep)"])
            + _card("⚽", "Gol 2.5 Toplam", ["Üst", "Alt"], ["Üst 2.5", "Alt 2.5"])
            + _card("🤝", "Karşılıklı Gol Toplam", ["KG Var", "KG Yok"], ["KG Var", "KG Yok"])
            + '</div>')


def kayitli_esikler():
    return {"esik_1": esik_1x2_al("1"), "esik_x": esik_1x2_al("X"), "esik_2": esik_1x2_al("2"),
            "ust": esik_al("ust"), "alt": esik_al("alt"), "kg_var": esik_al("kg_var"), "kg_yok": esik_al("kg_yok")}


# ==========================================
# UI YARDIMCILARI
# ==========================================
def _e(x): return _html.escape(str(x))


def rozet(m, t="gray"): return f'<span class="fa-badge fa-b-{t}">{_e(m)}</span>'


def mac_karti(ev, dep, sb, se, sd, le, ld, saat="", ulke="", tarih=""):
    orta = f'<div class="fa-score">{int(se)} - {int(sd)}</div>' if sb else '<div class="fa-vs">VS</div>'
    b = ulke_bayrak_bul(ulke)
    ust = ""
    if saat or ulke or tarih:
        p = []
        if b != "🌍" or ulke: p.append(f"{b} {_e((ulke or '').title())}")
        if tarih: p.append(f"📅 {_e(tarih)}")
        if saat: p.append(f"🕐 {_e(saat)}")
        if p: ust = f'<div class="fa-sub" style="margin-bottom:8px;">{" • ".join(p)}</div>'
    alt = f'<div class="fa-sub">Model beklenen gol: {le:.2f} - {ld:.2f}</div>'
    return f'<div class="fa-hero">{ust}<div class="fa-teams"><div class="fa-team">{_e(ev)}</div>{orta}<div class="fa-team">{_e(dep)}</div></div>{alt}</div>'


def olasilik_bar(e, y, esik=None, renk="#3b82f6"):
    y = max(0.0, min(100.0, y)); isr = ""
    if esik is not None:
        renk = "#22c55e" if y >= esik else "#475569"
        isr = f'<div class="fa-tick" style="left:{esik:.0f}%"></div>'
    return f'<div class="fa-row"><div class="fa-row-top"><span class="fa-lbl">{_e(e)}</span><span class="fa-val">%{y:.1f}</span></div><div class="fa-bar"><div class="fa-fill" style="width:{y:.1f}%;background:{renk}"></div>{isr}</div></div>'


def olasilik_paneli(a):
    s = ('<div class="fa-ttl">Maç Sonucu</div>'
        + olasilik_bar("Ev (1)", a["p1"], esik_1x2_al("1"), "#3b82f6")
        + olasilik_bar("Beraberlik (X)", a["px"], esik_1x2_al("X"), "#94a3b8")
        + olasilik_bar("Dep (2)", a["p2"], esik_1x2_al("2"), "#f59e0b")
        + '<div class="fa-ttl" style="margin-top:12px">Piyasalar</div>'
        + olasilik_bar("Üst 2.5", a["ust_25"], esik_al("ust"))
        + olasilik_bar("Alt 2.5", a["alt_25"], esik_al("alt"))
        + olasilik_bar("KG Var", a["kg_var_model"], esik_al("kg_var"))
        + olasilik_bar("KG Yok", a["kg_yok_model"], esik_al("kg_yok")))
    return f'<div class="fa-card">{s}</div>'


def oneri_karti(b, s, y, e, poz, alt):
    if poz:
        sv, _, _, et = guven_seviyesi_bul(y)
        t = "green" if sv == "yuksek" else "yellow" if sv == "orta" else "gray"
        d = rozet(f"{et} güven", t); sn = "fa-card fa-pos"; ps = "fa-pct"
        ns = f'<div class="fa-mut">{_e(alt)}</div>'
    else:
        d = rozet("Eşik altı", "gray"); sn = "fa-card fa-neg"; ps = "fa-pct fa-off"
        ns = f'<div class="fa-mut">{_e(alt)} • Gerekli: %{e:.0f}</div>'
    bar = olasilik_bar("", y, e)
    return f'<div class="{sn}"><div class="fa-ttl">{_e(b)}</div><div class="fa-pickrow"><div><div class="fa-pick">{_e(s)}</div>{d}</div><div class="{ps}">%{y:.1f}</div></div>{bar}{ns}</div>'


def mac_tahmin_karti(v_g, g=None):
    try:
        a = analiz_hesapla(v_g)
        p1 = a["p1"]; px = a["px"]; p2 = a["p2"]
        u25 = a["ust_25"]; alt = a["alt_25"]
        kgv = a["kg_var_model"]; kgy = a["kg_yok_model"]
        s1, y1 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        e1 = esik_1x2_al(s1); poz1 = y1 >= e1
        i1 = {"1": "1 — Ev Kazanır", "X": "X — Beraberlik", "2": "2 — Dep Kazanır"}[s1]
        if u25 >= alt: gs = "Üst 2.5"; gy = u25; ge_ = esik_al("ust")
        else: gs = "Alt 2.5"; gy = alt; ge_ = esik_al("alt")
        gp = gy >= ge_
        if kgv >= kgy: ks = "KG Var"; ky = kgv; ke = esik_al("kg_var")
        else: ks = "KG Yok"; ky = kgy; ke = esik_al("kg_yok")
        kp = ky >= ke
        def r(p): return "pass" if p else "off"
        def b(p): return "ok" if p else "no"
        def bt(p): return "✅" if p else "⚪"
        return f'''<div class="fa-mk">
        <div class="fa-mk-row"><span class="fa-mk-lbl">🎯 1X2</span><span class="fa-mk-pick {r(poz1)}">{_e(i1)}</span><span class="fa-mk-pct">%{y1:.0f} <span class="fa-mk-badge {b(poz1)}">{bt(poz1)} eşik %{e1:.0f}</span></span></div>
        <div class="fa-mk-row"><span class="fa-mk-lbl">⚽ Gol</span><span class="fa-mk-pick {r(gp)}">{_e(gs)}</span><span class="fa-mk-pct">%{gy:.0f} <span class="fa-mk-badge {b(gp)}">{bt(gp)} eşik %{ge_:.0f}</span></span></div>
        <div class="fa-mk-row"><span class="fa-mk-lbl">🤝 KG</span><span class="fa-mk-pick {r(kp)}">{_e(ks)}</span><span class="fa-mk-pct">%{ky:.0f} <span class="fa-mk-badge {b(kp)}">{bt(kp)} eşik %{ke:.0f}</span></span></div>
        </div>'''
    except Exception:
        return ""


def okunan_veriler_paneli(v):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{v.get('takim_ev', 'Ev')}**")
        st.markdown(f"- Atılan: **{v.get('atilan_ev', 0):.2f}**")
        st.markdown(f"- Yenen: **{v.get('yenen_ev', 0):.2f}**")
        st.markdown(f"- CS: **{v.get('clean_sheets_ev', 0):.1f}%**")
        st.markdown(f"- KG Var: **{v.get('kg_siklik_ev', 0):.1f}%**")
        st.markdown(f"- Üst 2.5: **{v.get('ust25_ev', 0):.1f}%**")
    with c2:
        st.markdown(f"**{v.get('takim_dep', 'Dep')}**")
        st.markdown(f"- Atılan: **{v.get('atilan_dep', 0):.2f}**")
        st.markdown(f"- Yenen: **{v.get('yenen_dep', 0):.2f}**")
        st.markdown(f"- CS: **{v.get('clean_sheets_dep', 0):.1f}%**")
        st.markdown(f"- KG Var: **{v.get('kg_siklik_dep', 0):.1f}%**")
        st.markdown(f"- Üst 2.5: **{v.get('ust25_dep', 0):.1f}%**")


def nav_bar():
    if st.session_state.sayfa == "giris": return
    try: k = st.container(key="fa_nav")
    except TypeError: k = st.container()
    with k:
        if admin_mi():
            sc = [("🏠", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek"), ("🧪 Test", "test"), ("⚙️", "ayarlar")]
        else:
            sc = [("🏠 Ana", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek")]
        kl = st.columns(len(sc))
        for ko, (e, h) in zip(kl, sc):
            with ko:
                a = st.session_state.sayfa == h
                if st.button(e, key=f"nav_{h}", use_container_width=True, type="primary" if a else "secondary"):
                    if not a:
                        st.session_state.sayfa = h
                        st.session_state.kayit_yapildi = False
                        st.session_state.tek_silme_onay = None
                        st.session_state.tek_silme_gelecek = None
                        st.rerun()


def ust_bar():
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("👑 **Admin Modu**" if admin_mi() else "👤 **Misafir Modu**")
    with c2:
        if st.button("🚪 Çıkış", use_container_width=True, key="cikis_btn"):
            st.session_state.giris_yapildi = False
            st.session_state.rol = None
            st.session_state.sayfa = "giris"
            st.rerun()


def giris_ekrani():
    st.markdown("""
        <div class="login-hero">
            <div class="login-logo">⚽</div>
            <h1 class="login-title">Futbol Analiz Pro</h1>
            <p class="login-subtitle">Akıllı maç analizi ve tahmin motoru</p>
        </div>
    """, unsafe_allow_html=True)
    with st.form("giris_form"):
        s = st.text_input("🔐 Admin Şifresi", type="password", key="sifre_input", placeholder="Şifreni gir...")
        ab = st.form_submit_button("👑  Admin Girişi", use_container_width=True, type="primary")
        st.markdown('<div class="login-divider">VEYA</div>', unsafe_allow_html=True)
        mb = st.form_submit_button("👤  Misafir Olarak Devam Et", use_container_width=True)
        if ab:
            if s == ADMIN_SIFRE:
                st.session_state.giris_yapildi = True
                st.session_state.rol = "admin"
                st.session_state.sayfa = "giris"
                st.rerun()
            else:
                st.error("❌ Yanlış şifre.")
        if mb:
            st.session_state.giris_yapildi = True
            st.session_state.rol = "misafir"
            st.session_state.sayfa = "giris"
            st.rerun()
    st.markdown("""
        <div class="login-features">
            <span class="lf-chip">🎯 1X2</span>
            <span class="lf-chip">⚽ Üst / Alt 2.5</span>
            <span class="lf-chip">🤝 KG Var / Yok</span>
            <span class="lf-chip">📊 İstatistik</span>
        </div>
        <div class="login-footer">© <b>Futbol Analiz Pro</b> • Bilgi amaçlıdır</div>
    """, unsafe_allow_html=True)


if not st.session_state.giris_yapildi:
    giris_ekrani()
    st.stop()

ust_bar()
nav_bar()


# ==========================================
# ANA SAYFA
# ==========================================
if st.session_state.sayfa == "giris":
    if admin_mi():
        st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>Mutating.com'dan otomatik çek. Paralel + Retry aktif.</p>", unsafe_allow_html=True)

        # ==== HIZLI SONUÇ İŞLEME (biten maçları otomatik geçmişe taşı) ====
        st.markdown("### 🏁 Biten Maçları Otomatik Aktar")
        st.caption("Gelecek'teki maçların skorlarını siteden okur, bitenleri skorlarıyla birlikte **Geçmiş'e** taşır. Bitmemişler Gelecek'te kalır.")
        if st.session_state.get("skor_ozet"):
            oz4 = st.session_state.skor_ozet
            st.success(f"✅ Son işlem: {oz4['tasinan']} maç taşındı • {oz4['bitmemis']} maç henüz bitmemiş")
            if oz4["hatalar"]:
                with st.expander(f"⚠️ {len(oz4['hatalar'])} hata"):
                    for h in oz4["hatalar"]: st.caption(h)
        hc1, hc2, hc3 = st.columns([2, 1, 1])
        with hc1:
            st.markdown(f"🔮 Bekleyen maç: **{len(st.session_state.gelecek_analizler)}**")
        with hc2:
            _hw = st.number_input("Paralel", 1, 6, 3, 1, key="hizli_skor_w", label_visibility="collapsed")
        with hc3:
            if st.button("🏁 Şimdi İşle", use_container_width=True, type="primary", key="hizli_skor_btn"):
                if not st.session_state.gelecek_analizler:
                    st.warning("⚠️ Gelecek'te maç yok.")
                else:
                    _hp = st.empty()
                    def _hp_cb(i, total, isim):
                        try: _hp.progress(min((i + 1) / total, 1.0), text=f"{i+1}/{total}: {isim}")
                        except Exception: pass
                    with st.spinner("Skorlar kontrol ediliyor..."):
                        st.session_state.skor_ozet = sonuclari_isle(tarayici_yedek=False, max_workers=int(_hw), progress_callback=_hp_cb)
                    _hp.empty()
                    st.rerun()
        st.divider()

        sekme1, sekme2, sekme3, sekme4 = st.tabs(["🔄 Gelecek Maçlar", "📜 Lig Geçmişi", "📋 Metin Yapıştır", "🏁 Sonuçları İşle"])

        with sekme1:
            st.caption("✅ Bugünün maçları çekilir, **tahmin olanlar Gelecek'e** eklenir.")
            if "toplu_cek_ozet" in st.session_state and st.session_state.toplu_cek_ozet:
                oz = st.session_state.toplu_cek_ozet
                if oz.get("eklenen", 0) > 0:
                    st.success(f"✅ Önceki çekim: **{oz['eklenen']}** maç eklendi.")
            c_w, c_b = st.columns(2)
            with c_w:
                workers = st.number_input("Paralel işlem", 1, 6, 2, 1, key="fw")
            with c_b:
                st.markdown("")
                if st.button("🚀 Bugünün Maçlarını Çek", use_container_width=True, type="primary", key="mbtn"):
                    prog_ph = st.empty()
                    def _prog(i, total, isim):
                        try: prog_ph.progress(min((i + 1) / total, 1.0), text=f"{i+1}/{total}: {isim}")
                        except Exception: pass
                    with st.spinner("Çekiliyor..."):
                        bas, hat = mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=_prog, max_workers=int(workers))
                    prog_ph.empty()
                    if hat:
                        with st.expander(f"⚠️ {len(hat)} hata"):
                            for h in hat: st.caption(h)
                    if not bas:
                        st.error("❌ Hiçbir maç çekilemedi.")
                    else:
                        st.success(f"✅ {len(bas)} maç işlendi.")
                        time.sleep(2)
                        st.rerun()

        with sekme2:
            st.caption("Lig URL'i yapıştır → son N maç çekilir, skorla **Geçmiş'e** eklenir.")
            lig_url = st.text_input(
                "Lig URL",
                placeholder="https://www.mutating.com/football-stats/league-uefa-champions-league-country-world-tables-stats-h2h-2/",
                key="lig_url_input",
            )
            c_a, c_b = st.columns(2)
            with c_a:
                lig_adet = st.number_input("Kaç maç?", 5, 30, 10, 1, key="lig_adet")
            with c_b:
                lig_workers = st.number_input("Paralel işlem", 1, 6, 2, 1, key="lig_workers")
            if st.button("📜 Ligi Çek", use_container_width=True, type="primary", key="lig_cek_btn"):
                if not lig_url.strip():
                    st.warning("⚠️ Lig URL gir.")
                else:
                    prog_ph = st.empty()
                    def _prog2(i, total, isim):
                        try: prog_ph.progress(min((i + 1) / total, 1.0), text=f"{i+1}/{total}: {isim}")
                        except Exception: pass
                    with st.spinner(f"Son {lig_adet} maç çekiliyor..."):
                        bas, hat = lig_gecmis_cek(lig_url.strip(), adet=int(lig_adet), max_workers=int(lig_workers), progress_callback=_prog2)
                    prog_ph.empty()
                    if hat:
                        with st.expander(f"⚠️ {len(hat)} hata"):
                            for h in hat: st.caption(h)
                    if not bas:
                        st.error("❌ Hiçbir maç eklenemedi.")
                    else:
                        st.success(f"✅ {len(bas)} maç Geçmiş'e eklendi!")
                        time.sleep(2)
                        st.rerun()

        with sekme3:
            st.caption("SportyTrader / Mutating metnini elle yapıştır.")
            ym = st.text_area("Yapıştırma", height=200, key="yapistir_input", label_visibility="collapsed", placeholder="İstatistik metnini buraya yapıştır.")
            if st.button("📋 Analiz Et", use_container_width=True, type="primary", key="metin_btn"):
                if not ym.strip():
                    st.warning("⚠️ Metin yapıştır.")
                else:
                    ck, okl = metinden_veri_cikar(ym)
                    if not ck:
                        st.error("❌ Veri çıkarılamadı.")
                    else:
                        yv = copy.deepcopy(VARSAYILAN_VERI); yv.update(ck)
                        st.session_state.form_verileri = yv
                        st.session_state.kayit_yapildi = False
                        st.session_state.sayfa = "sonuc"; st.rerun()

        with sekme4:
            st.caption("Maçlar bitince: Gelecek'teki maçların skorları siteden okunur, **biten maçlar skoruyla Geçmiş'e taşınır**. Bitmeyenler Gelecek'te kalır.")
            if st.session_state.get("skor_ozet"):
                oz4 = st.session_state.skor_ozet
                st.success(f"✅ {oz4['tasinan']} maç Geçmiş'e taşındı • {oz4['bitmemis']} maç henüz bitmemiş/skor yok")
                if oz4["hatalar"]:
                    with st.expander(f"⚠️ {len(oz4['hatalar'])} hata"):
                        for h in oz4["hatalar"]: st.caption(h)
            st.markdown(f"Bekleyen maç: **{len(st.session_state.gelecek_analizler)}**")
            skor_yedek = st.checkbox("Skor bulunamazsa tarayıcıyla da dene (yavaş, belleği zorlar)", value=False, key="skor_yedek")
            skor_w = st.number_input("Paralel işlem", 1, 6, 3, 1, key="skor_w")
            if st.button("🏁 Biten Maçları Geçmişe Aktar", use_container_width=True, type="primary", key="skor_btn"):
                if not st.session_state.gelecek_analizler:
                    st.warning("⚠️ Gelecek'te maç yok.")
                else:
                    prog4 = st.empty()
                    def _prog4(i, total, isim):
                        try: prog4.progress(min((i + 1) / total, 1.0), text=f"{i+1}/{total}: {isim}")
                        except Exception: pass
                    with st.spinner("Skorlar kontrol ediliyor..."):
                        st.session_state.skor_ozet = sonuclari_isle(tarayici_yedek=bool(skor_yedek), max_workers=int(skor_w), progress_callback=_prog4)
                    prog4.empty()
                    st.rerun()

        st.divider()
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("📊 Geçmiş", use_container_width=True):
                st.session_state.sayfa = "gecmis"; st.rerun()
        with c2:
            if st.button("🔮 Gelecek", use_container_width=True):
                st.session_state.sayfa = "gelecek"; st.rerun()
        with c3:
            if st.button("🧪 Test", use_container_width=True):
                st.session_state.sayfa = "test"; st.rerun()
        with c4:
            if st.button("⚙️ Ayarlar", use_container_width=True):
                st.session_state.sayfa = "ayarlar"; st.rerun()
    else:
        gs = len(st.session_state.gecmis_analizler)
        gl = len(st.session_state.gelecek_analizler)
        st.markdown(f"""
            <div class="mh-hero">
                <div class="mh-hero-icon">⚽</div>
                <div class="mh-hero-title">Futbol Analiz Pro</div>
                <div class="mh-hero-sub">Akıllı maç analizi ve tahmin motoru</div>
                <div class="mh-hero-badge">● CANLI VERİ</div>
            </div>
            <div class="mh-stat-grid">
                <div class="mh-stat"><div class="mh-stat-icon">📊</div><div class="mh-stat-num">{gs}</div><div class="mh-stat-lbl">Geçmiş Maç</div></div>
                <div class="mh-stat"><div class="mh-stat-icon">🔮</div><div class="mh-stat-num">{gl}</div><div class="mh-stat-lbl">Gelecek Maç</div></div>
            </div>
            <div class="mh-section-title">HIZLI ERİŞİM</div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📊  Geçmiş Maçlar", use_container_width=True, type="primary", key="m_gecmis"):
                st.session_state.sayfa = "gecmis"; st.rerun()
        with c2:
            if st.button("🔮  Gelecek Maçlar", use_container_width=True, type="primary", key="m_gelecek"):
                st.session_state.sayfa = "gelecek"; st.rerun()


# ==========================================
# GEÇMİŞ
# ==========================================
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gec = st.session_state.gecmis_analizler
    toplam = len(gec)
    if not gec:
        st.info("ℹ️ Kayıt yok.")
    gec_s = [g for g in gec if g.get("veri", {}).get("skor_belli")]
    if gec_s:
        ist_g, _ = test_hesapla(gec_s, kayitli_esikler())
        st.markdown("### 📈 Genel Analiz")
        st.markdown(ozet_html(ist_g), unsafe_allow_html=True)
        st.caption(f"{len(gec_s)} skorlu maç • kayıtlı eşiklere göre isabet % ve tutan/tahmin sayısı")
        st.divider()
    for i, g in enumerate(reversed(gec)):
        ig = len(gec) - 1 - i
        v = g["veri"]
        te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
        se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
        st.markdown(mac_karti(te, td, True, se, sd, 0, 0, saat=v.get("saat", ""), ulke=v.get("ulke", ""), tarih=v.get("tarih", "")), unsafe_allow_html=True)
        th = mac_tahmin_karti(v, g)
        if th: st.markdown(th, unsafe_allow_html=True)
        if admin_mi():
            cd, csil = st.columns([5, 1])
            with cd:
                if st.button("🔍 Detaylı", use_container_width=True, key=f"gmac_{ig}"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True
                    st.session_state.sayfa = "sonuc"; st.rerun()
            with csil:
                if st.button("🗑️", key=f"gsil_{ig}"):
                    st.session_state.tek_silme_onay = ig if st.session_state.tek_silme_onay != ig else None
                    st.rerun()
            if st.session_state.tek_silme_onay == ig:
                ce, ch = st.columns(2)
                with ce:
                    if st.button("✅ Sil", key=f"gevet_{ig}", use_container_width=True, type="primary"):
                        if 0 <= ig < len(st.session_state.gecmis_analizler):
                            st.session_state.gecmis_analizler.pop(ig)
                            gecmis_kaydet(st.session_state.gecmis_analizler)
                        st.session_state.tek_silme_onay = None; st.rerun()
                with ch:
                    if st.button("❌ İptal", key=f"ghayir_{ig}", use_container_width=True):
                        st.session_state.tek_silme_onay = None; st.rerun()
        st.divider()

    # Yedekleme
    if admin_mi():
        st.markdown("### 💾 Yedekleme (Geçmiş)")
        cind, cyuk = st.columns(2)
        with cind:
            st.download_button(
                label=f"📥 Geçmişi İndir ({toplam} maç)",
                data=json.dumps(st.session_state.gecmis_analizler, ensure_ascii=False, indent=2),
                file_name=f"gecmis_{toplam}mac.json",
                mime="application/json",
                use_container_width=True,
                key="ind_gecmis"
            )
        with cyuk:
            yuk = st.file_uploader("📤 Geçmişi Yükle (JSON)", type=["json"], key="yuk_gecmis")
            if yuk is not None:
                try:
                    veri = json.loads(yuk.read().decode("utf-8"))
                    if isinstance(veri, list):
                        st.session_state.gecmis_analizler = veri
                        gecmis_kaydet(veri)
                        st.success(f"✅ {len(veri)} maç yüklendi!")
                        st.rerun()
                    else:
                        st.error("❌ Format hatalı (liste bekleniyor).")
                except Exception as ex:
                    st.error(f"❌ Hata: {ex}")

        st.divider()
        ct, cg = st.columns(2)
        with ct:
            if st.button("🗑️ Tüm Geçmişi Temizle", use_container_width=True, key="g_temizle"):
                st.session_state.silme_onay = True; st.rerun()
        with cg:
            if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="g_geri"):
                st.session_state.sayfa = "giris"; st.rerun()
        if st.session_state.silme_onay:
            st.warning("⚠️ Tüm geçmiş silinecek. Emin misin?")
            ce, ch = st.columns(2)
            with ce:
                if st.button("✅ Evet, Sil", key="g_sil_evet", use_container_width=True, type="primary"):
                    st.session_state.gecmis_analizler = []
                    try:
                        if os.path.exists(GECMIS_DOSYA): os.remove(GECMIS_DOSYA)
                    except Exception: pass
                    st.session_state.silme_onay = False
                    st.rerun()
            with ch:
                if st.button("❌ İptal", key="g_sil_hayir", use_container_width=True):
                    st.session_state.silme_onay = False; st.rerun()
    else:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="g_geri_m"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# GELECEK
# ==========================================
elif st.session_state.sayfa == "gelecek":
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    gel = st.session_state.gelecek_analizler
    toplam_g = len(gel)
    if not gel:
        st.info("ℹ️ Gelecek maç yok. Ana sayfada **Bugünün Maçlarını Çek** basınca tahmin olanlar otomatik eklenir.")
    for i, g in enumerate(reversed(gel)):
        ig = len(gel) - 1 - i
        v = g["veri"]
        te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
        try:
            a = analiz_hesapla(v); le = a["lam_ev"]; ld = a["lam_dep"]
        except Exception: le = ld = 0
        st.markdown(mac_karti(te, td, False, 0, 0, le, ld, saat=v.get("saat", ""), ulke=v.get("ulke", ""), tarih=v.get("tarih", "")), unsafe_allow_html=True)
        th = mac_tahmin_karti(v, g)
        if th: st.markdown(th, unsafe_allow_html=True)
        if admin_mi():
            cd, csil = st.columns([5, 1])
            with cd:
                if st.button("🔍 Detaylı", use_container_width=True, key=f"ggmac_{ig}"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True
                    st.session_state.gelecekten_gelindi = True
                    st.session_state.aktif_gelecek_idx = ig
                    st.session_state.sayfa = "sonuc"; st.rerun()
            with csil:
                if st.button("🗑️", key=f"ggsil_{ig}"):
                    st.session_state.tek_silme_gelecek = ig if st.session_state.tek_silme_gelecek != ig else None
                    st.rerun()
            if st.session_state.tek_silme_gelecek == ig:
                ce, ch = st.columns(2)
                with ce:
                    if st.button("✅ Sil", key=f"ggevet_{ig}", use_container_width=True, type="primary"):
                        if 0 <= ig < len(st.session_state.gelecek_analizler):
                            st.session_state.gelecek_analizler.pop(ig)
                            gelecek_kaydet(st.session_state.gelecek_analizler)
                        st.session_state.tek_silme_gelecek = None; st.rerun()
                with ch:
                    if st.button("❌ İptal", key=f"gghayir_{ig}", use_container_width=True):
                        st.session_state.tek_silme_gelecek = None; st.rerun()
        else:
            if st.button("🔍 Detaylı", use_container_width=True, key=f"ggmac_{ig}"):
                st.session_state.form_verileri = copy.deepcopy(v)
                st.session_state.kayit_yapildi = True
                st.session_state.gelecekten_gelindi = True
                st.session_state.aktif_gelecek_idx = ig
                st.session_state.sayfa = "sonuc"; st.rerun()
        st.divider()

    # Yedekleme
    if admin_mi():
        st.markdown("### 💾 Yedekleme (Gelecek)")
        cind, cyuk = st.columns(2)
        with cind:
            st.download_button(
                label=f"📥 Geleceği İndir ({toplam_g} maç)",
                data=json.dumps(st.session_state.gelecek_analizler, ensure_ascii=False, indent=2),
                file_name=f"gelecek_{toplam_g}mac.json",
                mime="application/json",
                use_container_width=True,
                key="ind_gelecek"
            )
        with cyuk:
            yuk = st.file_uploader("📤 Geleceği Yükle (JSON)", type=["json"], key="yuk_gelecek")
            if yuk is not None:
                try:
                    veri = json.loads(yuk.read().decode("utf-8"))
                    if isinstance(veri, list):
                        st.session_state.gelecek_analizler = veri
                        gelecek_kaydet(veri)
                        st.success(f"✅ {len(veri)} maç yüklendi!")
                        st.rerun()
                    else:
                        st.error("❌ Format hatalı.")
                except Exception as ex:
                    st.error(f"❌ Hata: {ex}")

        st.divider()
        ct, cg = st.columns(2)
        with ct:
            if st.button("🗑️ Tüm Geleceği Temizle", use_container_width=True, key="gel_temizle"):
                st.session_state.silme_onay_gelecek = True; st.rerun()
        with cg:
            if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gel_geri"):
                st.session_state.sayfa = "giris"; st.rerun()
        if st.session_state.silme_onay_gelecek:
            st.warning("⚠️ Tüm gelecek silinecek. Emin misin?")
            ce, ch = st.columns(2)
            with ce:
                if st.button("✅ Evet, Sil", key="gel_sil_evet", use_container_width=True, type="primary"):
                    st.session_state.gelecek_analizler = []
                    try:
                        if os.path.exists(GELECEK_DOSYA): os.remove(GELECEK_DOSYA)
                    except Exception: pass
                    st.session_state.silme_onay_gelecek = False
                    st.rerun()
            with ch:
                if st.button("❌ İptal", key="gel_sil_hayir", use_container_width=True):
                    st.session_state.silme_onay_gelecek = False; st.rerun()
    else:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gel_geri_m"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# AYARLAR
# ==========================================
elif st.session_state.sayfa == "ayarlar":
    if not admin_mi():
        st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>⚙️ Eşik Ayarları</h1>", unsafe_allow_html=True)
    mv = st.session_state.esikler.copy()
    st.markdown("### 🎯 Maç Sonucu")
    c1, c2, c3 = st.columns(3)
    with c1: y1 = st.slider("1 (Ev) %", 0, 100, int(mv.get("esik_1", 55.0)), 1, key="ay_1")
    with c2: yx = st.slider("X %", 0, 100, int(mv.get("esik_x", 55.0)), 1, key="ay_x")
    with c3: y2 = st.slider("2 (Dep) %", 0, 100, int(mv.get("esik_2", 55.0)), 1, key="ay_2")
    st.markdown("### ⚽ Gol")
    c4, c5 = st.columns(2)
    with c4: yu = st.slider("Üst 2.5 %", 0, 100, int(mv["ust"]), 1, key="ay_ust")
    with c5: ya = st.slider("Alt 2.5 %", 0, 100, int(mv["alt"]), 1, key="ay_alt")
    st.markdown("### 🤝 KG")
    c6, c7 = st.columns(2)
    with c6: ykv = st.slider("KG Var %", 0, 100, int(mv["kg_var"]), 1, key="ay_kgv")
    with c7: yky = st.slider("KG Yok %", 0, 100, int(mv["kg_yok"]), 1, key="ay_kgy")
    st.divider()
    ck, cs, cg = st.columns(3)
    with ck:
        if st.button("💾 Kaydet", use_container_width=True, type="primary"):
            y = {"esik_1": float(y1), "esik_x": float(yx), "esik_2": float(y2), "ust": float(yu), "alt": float(ya), "kg_var": float(ykv), "kg_yok": float(yky)}
            st.session_state.esikler = y; ayarlar_kaydet(y); st.success("✅ Kaydedildi!")
    with cs:
        if st.button("🔄 Sıfırla", use_container_width=True):
            v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0}
            st.session_state.esikler = v; ayarlar_kaydet(v); st.rerun()
    with cg:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="aygeri"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# TEST (Geçmiş maçlar üzerinde eşik testi)
# ==========================================
elif st.session_state.sayfa == "test":
    if not admin_mi():
        st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>🧪 Test (Geçmiş Maçlar)</h1>", unsafe_allow_html=True)

    gec_t = [g for g in st.session_state.gecmis_analizler if g.get("veri", {}).get("skor_belli")]
    if not gec_t:
        st.info("ℹ️ Skorlu geçmiş maç yok. Önce Ana Sayfa → Lig Geçmişi ile maç ekle.")
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="t_geri0"):
            st.session_state.sayfa = "giris"; st.rerun()
        st.stop()

    mv_t = st.session_state.esikler
    ANAHTARLAR = [("t_1", "esik_1", 55.0), ("t_x", "esik_x", 55.0), ("t_2", "esik_2", 55.0),
                  ("t_ust", "ust", 65.0), ("t_alt", "alt", 55.0), ("t_kgv", "kg_var", 57.0), ("t_kgy", "kg_yok", 72.0)]

    def _t_sifirla():
        for wk, ek, vr in ANAHTARLAR:
            st.session_state[wk] = int(st.session_state.esikler.get(ek, vr))

    for wk, ek, vr in ANAHTARLAR:
        if wk not in st.session_state:
            st.session_state[wk] = int(mv_t.get(ek, vr))

    st.caption(f"{len(gec_t)} skorlu maç. Eşikleri değiştir, sonuç anında güncellenir. Burada yaptığın değişiklik **Ayarlar'ı etkilemez**, istersen aşağıdan kaydedebilirsin.")

    st.markdown("### 🎯 Maç Sonucu")
    tc1, tc2, tc3 = st.columns(3)
    with tc1: st.slider("1 (Ev) %", 0, 100, key="t_1")
    with tc2: st.slider("X %", 0, 100, key="t_x")
    with tc3: st.slider("2 (Dep) %", 0, 100, key="t_2")
    st.markdown("### ⚽ Gol")
    tc4, tc5 = st.columns(2)
    with tc4: st.slider("Üst 2.5 %", 0, 100, key="t_ust")
    with tc5: st.slider("Alt 2.5 %", 0, 100, key="t_alt")
    st.markdown("### 🤝 KG")
    tc6, tc7 = st.columns(2)
    with tc6: st.slider("KG Var %", 0, 100, key="t_kgv")
    with tc7: st.slider("KG Yok %", 0, 100, key="t_kgy")

    e_t = {"esik_1": float(st.session_state.t_1), "esik_x": float(st.session_state.t_x), "esik_2": float(st.session_state.t_2),
           "ust": float(st.session_state.t_ust), "alt": float(st.session_state.t_alt),
           "kg_var": float(st.session_state.t_kgv), "kg_yok": float(st.session_state.t_kgy)}

    ist, satirlar = test_hesapla(gec_t, e_t)

    html_t = ozet_html(ist)
    st.markdown("### 📊 Sonuç")
    st.markdown(html_t, unsafe_allow_html=True)
    st.caption("Format: isabet % ve tutan/tahmin sayısı. Tahmin sayısı, eşiği geçen maç sayısıdır.")

    with st.expander("📈 Eşik taraması (her piyasa ayrı ayrı)"):
        import pandas as pd
        lst = [50, 55, 60, 65, 70, 75, 80]
        harita = [("esik_1", "1"), ("esik_x", "X"), ("esik_2", "2"), ("ust", "Üst"), ("alt", "Alt"), ("kg_var", "KG Var"), ("kg_yok", "KG Yok")]
        rows = []
        for t in lst:
            row = {"Eşik": f"%{t}"}
            for ak, isim in harita:
                e2 = dict(e_t); e2[ak] = float(t)
                s2, _ = test_hesapla(gec_t, e2)
                n_, h_ = s2[isim]
                row[isim] = f"%{h_ / n_ * 100:.0f} ({n_})" if n_ else "—"
            rows.append(row)
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        st.caption("Hücre: isabet % (tahmin sayısı). Diğer piyasaların eşikleri yukarıdaki kaydırıcılardaki gibi kalır.")

    with st.expander("🔎 Maç maç detay"):
        def _ik(d): return "—" if d is None else ("✅" if d else "❌")
        for r in reversed(satirlar):
            st.markdown(
                f"**{_e(r['ev'])} {_e(r['skor'])} {_e(r['dep'])}**  \n"
                f"1X2: {r['o1'] or '—'} {_ik(r['d1'])} • Gol: {r['og'] or '—'} {_ik(r['dg'])} • KG: {r['ok'] or '—'} {_ik(r['dk'])}"
            )

    st.divider()
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("💾 Ayarlara Kaydet", use_container_width=True, type="primary", key="t_kaydet"):
            st.session_state.esikler = dict(e_t); ayarlar_kaydet(dict(e_t)); st.success("✅ Eşikler Ayarlar'a kaydedildi!")
    with b2:
        st.button("🔄 Kayıtlıya Dön", use_container_width=True, key="t_sifirla", on_click=_t_sifirla)
    with b3:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="t_geri"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SONUÇ
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)
    u25 = a["ust_25"]; alt = a["alt_25"]; kgv = a["kg_var_model"]; kgy = a["kg_yok_model"]
    te = v.get("takim_ev", "") or "Ev Sahibi"; td = v.get("takim_dep", "") or "Deplasman"
    sb = v.get("skor_belli", False); se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    st.markdown(mac_karti(te, td, sb, se, sd, a["lam_ev"], a["lam_dep"], saat=v.get("saat", ""), ulke=v.get("ulke", ""), tarih=v.get("tarih", "")), unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)
    with st.expander("📋 Okunan Veriler", expanded=False):
        okunan_veriler_paneli(v)
    st.divider()
    st.markdown("## 🏆 FİNAL ÖNERİ")
    s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    e1 = esik_1x2_al(s1); p1 = y1 >= e1
    im = {"1": "1 (Ev Sahibi)", "X": "X (Beraberlik)", "2": "2 (Deplasman)"}
    st.markdown(oneri_karti("🎯 1X2", im[s1], y1, e1, p1, f"1: %{a['p1']:.1f} • X: %{a['px']:.1f} • 2: %{a['p2']:.1f}"), unsafe_allow_html=True)
    if u25 >= alt: gs, gy, ge_ = "Üst 2.5", u25, esik_al("ust")
    else: gs, gy, ge_ = "Alt 2.5", alt, esik_al("alt")
    gp = gy >= ge_
    st.markdown(oneri_karti("⚽ Gol", gs, gy, ge_, gp, f"Üst %{u25:.1f} • Alt %{alt:.1f}"), unsafe_allow_html=True)
    if kgv >= kgy: ks, ky, ke = "KG Var", kgv, esik_al("kg_var")
    else: ks, ky, ke = "KG Yok", kgy, esik_al("kg_yok")
    kp = ky >= ke
    st.markdown(oneri_karti("🤝 Karşılıklı Gol", ks, ky, ke, kp, f"Var %{kgv:.1f} • Yok %{kgy:.1f}"), unsafe_allow_html=True)

    if st.session_state.gelecekten_gelindi and admin_mi():
        ig = st.session_state.aktif_gelecek_idx
        if ig is not None and 0 <= ig < len(st.session_state.gelecek_analizler):
            st.divider()
            st.markdown("### 📥 Sonucu Gir ve Geçmişe Taşı")
            sc1, sc2, sc3 = st.columns([1, 1, 1])
            with sc1: yse = st.number_input("Ev Gol", 0, 20, int(v.get("skor_ev", 0)), 1, key=f"gse_{ig}")
            with sc2: ysd = st.number_input("Dep Gol", 0, 20, int(v.get("skor_dep", 0)), 1, key=f"gsd_{ig}")
            with sc3:
                st.markdown(""); st.markdown("")
                if st.button("📥 Taşı", key=f"tasi_{ig}", use_container_width=True, type="primary"):
                    k = st.session_state.gelecek_analizler[ig]
                    k["veri"]["skor_ev"] = int(yse); k["veri"]["skor_dep"] = int(ysd); k["veri"]["skor_belli"] = True
                    yd = sonuc_hesapla(k)
                    if yd: k["dogruluk"] = yd
                    st.session_state.gecmis_analizler.append(k)
                    st.session_state.gelecek_analizler.pop(ig)
                    gecmis_kaydet(st.session_state.gecmis_analizler)
                    gelecek_kaydet(st.session_state.gelecek_analizler)
                    st.session_state.gelecekten_gelindi = False
                    st.session_state.aktif_gelecek_idx = None
                    st.session_state.sayfa = "gelecek"
                    st.rerun()

    st.divider()
    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.sayfa = "giris"
        st.rerun()
