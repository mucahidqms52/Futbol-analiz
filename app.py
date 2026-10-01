import streamlit as st
import math
import copy
import re
import random
import json
import os
import html as _html
import time
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

try:
    SCRAPINGBEE_API_KEY = st.secrets["SCRAPINGBEE_API_KEY"]
except Exception:
    SCRAPINGBEE_API_KEY = ""

st.markdown("""
<style>
    .block-container { padding-top: 2rem !important; padding-bottom: 0.5rem !important; padding-left: 0.7rem !important; padding-right: 0.7rem !important; max-width: 100% !important; }
    h1 { font-size: 1.2rem !important; margin: 0.2rem 0 !important; text-align: center; }
    h2 { font-size: 1rem !important; margin: 0.3rem 0 !important; }
    h3 { font-size: 0.9rem !important; margin: 0.15rem 0 !important; }
    p { font-size: 0.85rem !important; margin: 0.2rem 0 !important; }
    hr { margin: 0.3rem 0 !important; }
    div[data-testid="stNumberInput"] label p { font-size: 0.75rem !important; margin: 0 !important; }
    div[data-testid="stNumberInput"] input { font-size: 0.85rem !important; padding: 0.15rem 0.3rem !important; height: 1.8rem !important; }
    div[data-testid="stNumberInput"] button { height: 1.8rem !important; padding: 0 !important; width: 1.5rem !important; }
    div[data-testid="stNumberInput"] > div { margin-bottom: 0.2rem !important; }
    div[data-testid="stMetric"] { padding: 0.2rem !important; }
    div[data-testid="stMetricValue"] { font-size: 1rem !important; }
    div[data-testid="stMetricLabel"] { font-size: 0.7rem !important; }
    div[data-testid="stMetricDelta"] { font-size: 0.65rem !important; }
    .stButton button { padding: 0.4rem 0.6rem !important; font-size: 0.9rem !important; height: 2.2rem !important; }
    div[data-testid="stAlert"] { padding: 0.3rem 0.5rem !important; font-size: 0.85rem !important; }
    details summary { font-size: 0.8rem !important; padding: 0.2rem 0.4rem !important; }
    textarea { font-size: 0.75rem !important; }
    div[data-testid="stExpander"] summary { font-size: 0.9rem !important; padding: 0.4rem !important; }
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
    div[data-testid="stMetric"] { background: #131c2e; border: 1px solid #23304a; border-radius: 12px; }
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
    .stApp .fa-ci { position: relative; height: 8px; background: #1d2940; border-radius: 99px; margin-top: 8px; }
    .stApp .fa-ci-fill { position: absolute; top: 0; bottom: 0; background: rgba(148,163,184,0.45); border-radius: 99px; }
    .stApp .fa-ci-dot { position: absolute; top: -3px; width: 14px; height: 14px; border-radius: 50%; border: 2px solid #0b1220; margin-left: -7px; }
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
    .login-logo { font-size: 4.5rem; line-height: 1; margin-bottom: 12px; display: inline-block; filter: drop-shadow(0 0 20px rgba(34,197,94,0.5)); }
    .login-title { font-size: 2rem !important; font-weight: 900 !important; background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0 !important; padding: 0 !important; letter-spacing: 1.2px; border: none !important; text-align: center !important; }
    .login-subtitle { font-size: 0.88rem; color: #8fa0bd !important; margin-top: 8px; letter-spacing: 0.5px; font-weight: 500; }
    div[data-testid="stForm"] { background: linear-gradient(145deg, rgba(19,28,46,0.85), rgba(11,18,32,0.95)) !important; border: 1px solid rgba(34,197,94,0.18) !important; border-radius: 22px !important; padding: 24px 20px !important; box-shadow: 0 12px 48px rgba(0,0,0,0.45) !important; }
    div[data-testid="stForm"] label p { font-size: 0.8rem !important; font-weight: 700 !important; color: #cbd5e1 !important; margin-bottom: 4px !important; }
    div[data-testid="stForm"] input { height: 46px !important; font-size: 0.95rem !important; padding: 0 14px !important; background: rgba(11,18,32,0.85) !important; border: 1.5px solid #23304a !important; border-radius: 12px !important; }
    div[data-testid="stForm"] input:focus { border-color: #22c55e !important; box-shadow: 0 0 0 3px rgba(34,197,94,0.18) !important; outline: none !important; }
    div[data-testid="stForm"] button { height: 46px !important; font-size: 0.95rem !important; font-weight: 700 !important; border-radius: 12px !important; }
    div[data-testid="stForm"] button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; border: none !important; }
    div[data-testid="stForm"] button[kind="secondary"] { background: rgba(30,41,59,0.55) !important; border: 1.5px solid #23304a !important; }
    .login-divider { display: flex; align-items: center; gap: 12px; margin: 10px 0 6px 0; color: #64748b !important; font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; justify-content: center; }
    .login-divider::before, .login-divider::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, transparent, #23304a 50%, transparent); }
    .login-features { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 22px; padding: 0 10px; }
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
    .mh-info b { color: #22c55e !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DOSYALAR
# ==========================================
GECMIS_DOSYA = "gecmis.json"
GELECEK_DOSYA = "gelecek.json"
AYARLAR_DOSYA = "ayarlar.json"
ADMIN_SIFRE = "Mg153759"


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
    varsayilan = {
        "ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0,
        "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0,
    }
    try:
        if os.path.exists(AYARLAR_DOSYA):
            with open(AYARLAR_DOSYA, "r", encoding="utf-8") as f:
                yuklenen = json.load(f)
                varsayilan.update(yuklenen)
    except Exception:
        pass
    return varsayilan


def ayarlar_kaydet(esikler):
    try:
        with open(AYARLAR_DOSYA, "w", encoding="utf-8") as f:
            json.dump(esikler, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ==========================================
# SABİTLER
# ==========================================
ESIK_YUKSEK = 65.0
ESIK_ORTA = 55.0
ESIK_BELIRSIZ = 50.0
MONTE_CARLO_N = 10000
MAX_GOL = 8
BELIRSIZLIK = 0.20


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
    "saat": "", "tarih": "", "ulke": "", "format": "bilinmiyor",
}


# ==========================================
# SESSION STATE
# ==========================================
if "sayfa" not in st.session_state: st.session_state.sayfa = "giris"
if "form_verileri" not in st.session_state: st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
if "gecmis_analizler" not in st.session_state: st.session_state.gecmis_analizler = gecmis_yukle()
if "gelecek_analizler" not in st.session_state: st.session_state.gelecek_analizler = gelecek_yukle()
if "kayit_yapildi" not in st.session_state: st.session_state.kayit_yapildi = False
if "gecmisten_gelindi" not in st.session_state: st.session_state.gecmisten_gelindi = False
if "gelecekten_gelindi" not in st.session_state: st.session_state.gelecekten_gelindi = False
if "silme_onay" not in st.session_state: st.session_state.silme_onay = False
if "aktif_kayit_idx" not in st.session_state: st.session_state.aktif_kayit_idx = None
if "aktif_gelecek_idx" not in st.session_state: st.session_state.aktif_gelecek_idx = None
if "okunamayan_alanlar" not in st.session_state: st.session_state.okunamayan_alanlar = []
if "manuel_bekleyen" not in st.session_state: st.session_state.manuel_bekleyen = []
if "tek_silme_onay" not in st.session_state: st.session_state.tek_silme_onay = None
if "tek_silme_gelecek" not in st.session_state: st.session_state.tek_silme_gelecek = None
if "giris_yapildi" not in st.session_state: st.session_state.giris_yapildi = False
if "rol" not in st.session_state: st.session_state.rol = None
if "toplu_cek_sonuc" not in st.session_state: st.session_state.toplu_cek_sonuc = None
if "esikler" not in st.session_state: st.session_state.esikler = ayarlar_yukle()
if "bt_market" not in st.session_state:
    st.session_state.bt_market = {"1x2": False, "kg_var": False, "kg_yok": False, "ust": False, "alt": False}
if "bt_market_esik" not in st.session_state:
    st.session_state.bt_market_esik = {"esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "kg_var": 70.0, "kg_yok": 70.0, "ust": 70.0, "alt": 70.0}
if "bt_sonuc" not in st.session_state: st.session_state.bt_sonuc = None
if "bt_detaylar" not in st.session_state: st.session_state.bt_detaylar = []


def admin_mi(): return st.session_state.get("rol") == "admin"
def esik_al(key): return st.session_state.esikler.get(key, 50.0)
def esik_1x2_al(secim):
    key_map = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}
    return st.session_state.esikler.get(key_map.get(secim, ""), 55.0)


# ==========================================
# ÜLKE BAYRAK
# ==========================================
ULKE_BAYRAK = {
    "switzerland": "🇨🇭", "isviçre": "🇨🇭", "i̇sviçre": "🇨🇭",
    "england": "🏴", "ingiltere": "🏴", "i̇ngiltere": "🏴",
    "spain": "🇪🇸", "ispanya": "🇪🇸", "i̇spanya": "🇪🇸",
    "italy": "🇮🇹", "italya": "🇮🇹", "i̇talya": "🇮🇹",
    "germany": "🇩🇪", "almanya": "🇩🇪", "france": "🇫🇷", "fransa": "🇫🇷",
    "netherlands": "🇳🇱", "hollanda": "🇳🇱", "portugal": "🇵🇹", "portekiz": "🇵🇹",
    "belgium": "🇧🇪", "belçika": "🇧🇪", "turkey": "🇹🇷", "türkiye": "🇹🇷", "turkiye": "🇹🇷",
    "argentina": "🇦🇷", "arjantin": "🇦🇷", "brazil": "🇧🇷", "brezilya": "🇧🇷",
    "mexico": "🇲🇽", "meksika": "🇲🇽", "usa": "🇺🇸", "united states": "🇺🇸", "abd": "🇺🇸",
    "japan": "🇯🇵", "japonya": "🇯🇵", "south korea": "🇰🇷", "korea": "🇰🇷", "güney kore": "🇰🇷",
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
    "saudi": "🇸🇦", "suudi arabistan": "🇸🇦", "uae": "🇦🇪", "qatar": "🇶🇦", "katar": "🇶🇦",
    "egypt": "🇪🇬", "mısır": "🇪🇬", "morocco": "🇲🇦", "fas": "🇲🇦",
    "algeria": "🇩🇿", "cezayir": "🇩🇿", "tunisia": "🇹🇳", "tunus": "🇹🇳",
    "nigeria": "🇳🇬", "nijerya": "🇳🇬", "south africa": "🇿🇦", "güney afrika": "🇿🇦",
    "australia": "🇦🇺", "avustralya": "🇦🇺", "new zealand": "🇳🇿", "yeni zelanda": "🇳🇿",
    "india": "🇮🇳", "hindistan": "🇮🇳", "iran": "🇮🇷", "iraq": "🇮🇶", "irak": "🇮🇶",
    "israel": "🇮🇱", "i̇srail": "🇮🇱", "colombia": "🇨🇴", "kolombiya": "🇨🇴",
    "chile": "🇨🇱", "şili": "🇨🇱", "peru": "🇵🇪", "uruguay": "🇺🇾",
    "ecuador": "🇪🇨", "ekvador": "🇪🇨", "paraguay": "🇵🇾", "bolivia": "🇧🇴", "bolivya": "🇧🇴",
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
    "bosnia": "🇧🇦", "bosna": "🇧🇦",
}


def ulke_bayrak_bul(ulke_adi):
    if not ulke_adi: return "🌍"
    u = ulke_adi.lower().strip()
    for anahtar in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if anahtar in u: return ULKE_BAYRAK[anahtar]
    return "🌍"


def _ulke_bul(metin):
    m = re.search(r'Standings\s+([^\n]+)', metin)
    if not m: return ""
    satir = m.group(1).strip()
    if not satir: return ""
    alt = satir.lower()
    for anahtar in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if anahtar in alt: return anahtar
    parcalar = satir.split()
    return " ".join(parcalar[:2]) if len(parcalar) >= 2 else (parcalar[0] if parcalar else "")


# ==========================================
# YARDIMCI
# ==========================================
def clamp(x, lo, hi): return max(lo, min(hi, x))


def ort_iki(a, b):
    vals = [x for x in [a, b] if x is not None and x > 0]
    if not vals: return 0
    return sum(vals) / len(vals)


def guven_seviyesi_bul(olasilik):
    if olasilik >= ESIK_YUKSEK: return ("yuksek", "🟢", "success", "Yüksek")
    if olasilik >= ESIK_ORTA: return ("orta", "🟡", "warning", "Orta")
    if olasilik >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "error", "Belirsiz")
    return ("cok_dusuk", "⚫", "error", "Düşük")


# ==========================================
# SCRAPINGBEE İLE ÇEKME
# ==========================================
def _scrapingbee_get(url, render_js=True, timeout=60):
    if not SCRAPINGBEE_API_KEY or SCRAPINGBEE_API_KEY.strip() == "":
        return None, "ScrapingBee API anahtarı ayarlanmamış."
    try:
        params = {
            "api_key": SCRAPINGBEE_API_KEY,
            "url": url,
            "render_js": "true" if render_js else "false",
        }
        r = requests.get("https://app.scrapingbee.com/api/v1/", params=params, timeout=timeout)
        if r.status_code == 200:
            return r.text, None
        elif r.status_code == 401:
            return None, "API anahtarı geçersiz."
        elif r.status_code == 402:
            return None, "Ücretsiz kota doldu."
        else:
            return None, f"ScrapingBee hata: {r.status_code}"
    except Exception as e:
        return None, f"Bağlantı hatası: {str(e)}"


def _html_metne_cevir(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
        tag.decompose()
    for td in soup.find_all(["td", "th"]):
        td.insert_after("\t")
    for tr in soup.find_all("tr"):
        tr.insert_after("\n")
    for etiket in soup.find_all(["div", "p", "li", "h1", "h2", "h3", "h4", "br"]):
        etiket.insert_after("\n")
    metin = soup.get_text(separator="", strip=False)
    metin = re.sub(r'[ \t]+\n', '\n', metin)
    metin = re.sub(r'\n{3,}', '\n\n', metin)
    return metin


def mutating_ana_sayfa_linklerini_al(max_mac=5):
    html, hata = _scrapingbee_get("https://www.mutating.com/football-stats/", render_js=True)
    if hata: return [], [hata]
    if not html: return [], ["Ana sayfa indirilemedi."]
    soup = BeautifulSoup(html, "html.parser")
    maclar = []
    gorulen = set()
    for link in soup.find_all("a", href=True):
        if len(maclar) >= max_mac: break
        href = link.get("href", "")
        if not any(x in href for x in ["match-preview", "match/", "/stats/"]):
            continue
        if href.startswith("/"):
            href = "https://www.mutating.com" + href
        elif not href.startswith("http"):
            continue
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
    html, hata = _scrapingbee_get(url, render_js=True)
    if hata: return None, [hata]
    if not html: return None, ["Sayfa indirilemedi."]
    soup = BeautifulSoup(html, "html.parser")
    veri = {}
    okunamayanlar = []
    h1 = soup.find("h1")
    if h1:
        baslik = h1.get_text(strip=True)
        if " - " in baslik:
            parcalar = baslik.replace(" Stats", "").replace(" stats", "").split(" - ")
            veri["takim_ev"] = parcalar[0].strip()
            if len(parcalar) > 1:
                veri["takim_dep"] = parcalar[1].strip()
    metin = _html_metne_cevir(html)
    m = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', metin)
    if m: veri["tarih"] = m.group(1)
    m = re.search(r'(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1)
    veri["ulke"] = _ulke_bul(metin)

    def _cift(label):
        for pat in [
            r'([\d.,]+)\s*%?\s*\t\s*' + re.escape(label) + r'\s*\t\s*([\d.,]+)',
            r'([\d.,]+)\s*%?\s*\|\s*' + re.escape(label) + r'\s*\|\s*([\d.,]+)',
            r'([\d.,]+)\s*%?\s+' + re.escape(label) + r'\s+([\d.,]+)\s*%?',
            r'([\d.,]+)\s*%?\s*\n\s*' + re.escape(label) + r'\s*\n\s*([\d.,]+)',
        ]:
            mm = re.search(pat, metin, re.IGNORECASE)
            if mm:
                try:
                    return float(mm.group(1).replace(",", ".")), float(mm.group(2).replace(",", "."))
                except ValueError:
                    continue
        return None, None

    eslesmeler = [
        ("Goals scored per game", "atilan_ev", "atilan_dep"),
        ("Goals conceded per game", "yenen_ev", "yenen_dep"),
        ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"),
        ("Team scored", "team_scored_ev", "team_scored_dep"),
        ("Both Teams to Score", "kg_siklik_ev", "kg_siklik_dep"),
        ("Over 2.5 goals", "ust25_ev", "ust25_dep"),
        ("Over 1.5 goals", "ust15_ev", "ust15_dep"),
        ("Over 3.5 goals", "ust35_ev", "ust35_dep"),
    ]
    for label, k_ev, k_dep in eslesmeler:
        a, b = _cift(label)
        if a is not None and veri.get(k_ev, 0) == 0:
            veri[k_ev] = a; veri[k_dep] = b

    for label, k_ev, k_dep in [("Win", "galibiyet_ev", "galibiyet_dep"), ("Draw", "beraberlik_ev", "beraberlik_dep"), ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
        mm = re.search(r'([\d.,]+)\s*%\s*\t\s*' + label + r'\s*\t\s*([\d.,]+)\s*%', metin, re.MULTILINE)
        if mm:
            try:
                veri[k_ev] = float(mm.group(1).replace(",", "."))
                veri[k_dep] = float(mm.group(2).replace(",", "."))
            except ValueError:
                pass

    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) + veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2

    veri["format"] = "mutating"
    veri["skor_belli"] = False
    if not veri.get("takim_ev"): okunamayanlar.append("Takım isimleri (Ev)")
    if not veri.get("takim_dep"): okunamayanlar.append("Takım isimleri (Dep)")
    if veri.get("atilan_ev", 0) == 0: okunamayanlar.append("Atılan Gol (Ev)")
    if veri.get("yenen_ev", 0) == 0: okunamayanlar.append("Yenen Gol (Ev)")
    return veri, okunamayanlar


def mutating_toplu_cek(max_mac=5, progress_callback=None):
    basarili = []; hatali = []
    if not SCRAPINGBEE_API_KEY or SCRAPINGBEE_API_KEY.strip() == "":
        return [], ["ScrapingBee API anahtarı ayarlanmamış. Streamlit Secrets'e ekle."]
    maclar, hatalar = mutating_ana_sayfa_linklerini_al(max_mac=max_mac)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Ana sayfada maç linki bulunamadı."]
    for i, mac in enumerate(maclar):
        if progress_callback:
            try: progress_callback(i, len(maclar), mac.get("takim_ev", "") + " vs " + mac.get("takim_dep", ""))
            except Exception: pass
        try:
            veri, okunamayanlar = mutating_mac_detay_cek(mac["url"])
            if veri:
                if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
                if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
                if not veri.get("saat"): veri["saat"] = mac.get("saat", "")
                veri["kaynak_url"] = mac["url"]
                basarili.append(veri)
            else:
                hatali.append(f"Maç {i+1}: Veri çekilemedi")
        except Exception as e:
            hatali.append(f"Maç {i+1}: {str(e)}")
        time.sleep(1)
    return basarili, hatali


# ==========================================
# SPORTYTRADER PARSER
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
        veri["takim_ev"] = m.group(1).strip()
        veri["takim_dep"] = m.group(2).strip()
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
        v1, v2 = _cift_tab("Goals scored per game", blok)
        if v1 is not None: veri["atilan_ev"] = v1; veri["atilan_dep"] = v2
        v1, v2 = _cift_tab("Goals conceded per game", blok)
        if v1 is not None: veri["yenen_ev"] = v1; veri["yenen_dep"] = v2
        v1, v2 = _cift_tab("Clean sheets", blok)
        if v1 is not None: veri["clean_sheets_ev"] = v1; veri["clean_sheets_dep"] = v2
        v1, v2 = _cift_tab("Team scored", blok)
        if v1 is not None: veri["team_scored_ev"] = v1; veri["team_scored_dep"] = v2
    idx = metin.find("Win Draw Lose")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for etiket, ke, kd in [("Win", "galibiyet_ev", "galibiyet_dep"), ("Draw", "beraberlik_ev", "beraberlik_dep"), ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
            mm = re.search(r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*' + etiket + r'\s*\t\s*([\d.,]+)%', blok, re.MULTILINE)
            if mm:
                try:
                    veri[ke] = float(mm.group(1).replace(",", "."))
                    veri[kd] = float(mm.group(2).replace(",", "."))
                except ValueError: pass
    idx = metin.find("Both Teams to Score")
    if idx != -1:
        blok = metin[idx:idx+1500]
        v1, v2 = _cift_tab("BTTS in first-half", blok)
        if v1 is not None: veri["btts_1h_ev"] = v1; veri["btts_1h_dep"] = v2
        v1, v2 = _cift_tab("BBTS in second-half", blok)
        if v1 is not None: veri["btts_2h_ev"] = v1; veri["btts_2h_dep"] = v2
        mm = re.search(r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*Both Teams to Score\s*\t\s*([\d.,]+)%', blok, re.MULTILINE)
        if mm:
            try:
                veri["kg_siklik_ev"] = float(mm.group(1).replace(",", "."))
                veri["kg_siklik_dep"] = float(mm.group(2).replace(",", "."))
            except ValueError: pass
    idx = metin.find("Over Under Goals")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for etiket, ke, kd in [("Over 0.5 goals", "ust05_ev", "ust05_dep"), ("Over 1.5 goals", "ust15_ev", "ust15_dep"), ("Over 2.5 goals", "ust25_ev", "ust25_dep"), ("Over 3.5 goals", "ust35_ev", "ust35_dep")]:
            v1, v2 = _cift_tab(etiket, blok)
            if v1 is not None: veri[ke] = v1; veri[kd] = v2
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
    veri = {"format": "genel"}; return veri, []


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
    atilan_e = v.get("atilan_ev", 0.0); yenen_e = v.get("yenen_ev", 0.0)
    atilan_d = v.get("atilan_dep", 0.0); yenen_d = v.get("yenen_dep", 0.0)
    xg_e = v.get("xg_ev", 0.0); xg_d = v.get("xg_dep", 0.0)
    hucum_ev_baz = (xg_e * 0.60 + atilan_e * 0.40) if xg_e > 0 else (atilan_e if atilan_e > 0 else 1.2)
    hucum_dep_baz = (xg_d * 0.60 + atilan_d * 0.40) if xg_d > 0 else (atilan_d if atilan_d > 0 else 1.0)
    ts_ev = v.get("team_scored_ev", 0); ts_dep = v.get("team_scored_dep", 0)
    if ts_ev > 0: hucum_ev_baz *= clamp(ts_ev / 60, 0.7, 1.3)
    if ts_dep > 0: hucum_dep_baz *= clamp(ts_dep / 60, 0.7, 1.3)
    savunma_dep_zaaf = yenen_d if yenen_d > 0 else 1.2
    savunma_ev_zaaf = yenen_e if yenen_e > 0 else 1.0
    cs_ev = v.get("clean_sheets_ev", 0.0); cs_dep = v.get("clean_sheets_dep", 0.0)
    def cf(cs):
        if cs <= 0: return 1.0
        if cs < 40.0: return 1.0 - (cs / 250.0)
        return max(0.40, 0.84 - (cs - 40.0) * (0.44 / 60.0))
    dep_freni = cf(cs_ev); ev_freni = cf(cs_dep)
    lam_ev_ham = hucum_ev_baz * 0.60 + savunma_dep_zaaf * 0.40
    lam_dep_ham = hucum_dep_baz * 0.60 + savunma_ev_zaaf * 0.40
    ust25_e = v.get("ust25_ev", 0); ust25_d = v.get("ust25_dep", 0)
    if ust25_e > 0: lam_ev_ham *= clamp(ust25_e / 50, 0.85, 1.15)
    if ust25_d > 0: lam_dep_ham *= clamp(ust25_d / 50, 0.85, 1.15)
    kg_e = v.get("kg_siklik_ev", 0); kg_d = v.get("kg_siklik_dep", 0)
    if kg_e > 0 and kg_d > 0:
        kg_ort = (kg_e + kg_d) / 2
        if kg_ort >= 60: lam_ev_ham *= 1.05; lam_dep_ham *= 1.05
        elif kg_ort <= 35: lam_ev_ham *= 0.95; lam_dep_ham *= 0.95
    form_ev = clamp(1 + (v.get("ppg_ev", 1.5) - 1.5) / 15, 0.85, 1.15)
    form_dep = clamp(1 + (v.get("mpg_dep", 1.5) - 1.5) / 15, 0.85, 1.15)
    sira_e = v.get("siralama_ev", 10); sira_d = v.get("siralama_dep", 10)
    dom = 1.0
    if 1 <= sira_e <= 5 and sira_d >= 10: dom = 1.20
    gal_ev = v.get("galibiyet_ev", 0); gal_dep = v.get("galibiyet_dep", 0)
    if gal_ev > 0 and gal_dep > 0:
        if gal_ev - gal_dep >= 25: lam_ev_ham *= 1.08; lam_dep_ham *= 0.95
        elif gal_dep - gal_ev >= 25: lam_ev_ham *= 0.95; lam_dep_ham *= 1.08
    lam_ev = lam_ev_ham * 1.05 * form_ev * ev_freni * dom
    lam_dep = lam_dep_ham * 0.95 * form_dep * dep_freni
    if lam_ev > 2.50: lam_ev = 2.50 + (lam_ev - 2.50) * 0.5
    if lam_dep > 2.50: lam_dep = 2.50 + (lam_dep - 2.50) * 0.5
    return clamp(lam_ev, 0.05, 4.5), clamp(lam_dep, 0.05, 4.5), 0.80


def matristen_olasilik(matris, mg=MAX_GOL):
    p1 = px = p2 = 0.0
    ust05 = ust15 = ust25 = ust35 = 0.0
    kg_var = 0.0; skorlar = {}; toplam = 0.0
    for i in range(mg):
        for j in range(mg):
            p = matris[i][j]; toplam += p
            if i > j: p1 += p
            elif i == j: px += p
            else: p2 += p
            tg = i + j
            if tg > 0.5: ust05 += p
            if tg > 1.5: ust15 += p
            if tg > 2.5: ust25 += p
            if tg > 3.5: ust35 += p
            if i > 0 and j > 0: kg_var += p
            skorlar[f"{i}-{j}"] = p
    return {"1": p1, "X": px, "2": p2, "ust_05": ust05, "ust_15": ust15, "ust_25": ust25, "ust_35": ust35, "kg_var": kg_var, "skorlar": skorlar, "toplam": toplam}


def veri_yeterli_mi(v):
    onemli = [v["atilan_ev"], v["atilan_dep"], v["yenen_ev"], v["yenen_dep"]]
    return sum(1 for x in onemli if x > 0) >= 2


def mac_ici_sok(lam_ev, lam_dep, rng=None):
    r = rng if rng is not None else random
    if r.random() < 0.03:
        if r.random() < 0.5: lam_ev *= 0.70
        else: lam_dep *= 0.70
    return lam_ev, lam_dep


def monte_carlo_simulasyon(lam_ev_base, lam_dep_base, n=MONTE_CARLO_N):
    seed = int(round(lam_ev_base * 1_000_000)) * 1_000_003 + int(round(lam_dep_base * 1_000_000))
    rng = random.Random(seed)
    sayac = {"1": 0, "X": 0, "2": 0, "ust25": 0, "kg_var": 0}
    for _ in range(n):
        lam_ev = lam_ev_base * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        lam_dep = lam_dep_base * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        lam_ev, lam_dep = mac_ici_sok(lam_ev, lam_dep, rng)
        ev_gol = min(MAX_GOL - 1, poisson_random(lam_ev, rng))
        dep_gol = min(MAX_GOL - 1, poisson_random(lam_dep, rng))
        if ev_gol > dep_gol: sayac["1"] += 1
        elif ev_gol == dep_gol: sayac["X"] += 1
        else: sayac["2"] += 1
        if ev_gol + dep_gol > 2.5: sayac["ust25"] += 1
        if ev_gol > 0 and dep_gol > 0: sayac["kg_var"] += 1
    def yz(s): return s / n * 100 if n > 0 else 0
    return {"p1": yz(sayac["1"]), "px": yz(sayac["X"]), "p2": yz(sayac["2"]), "ust25": yz(sayac["ust25"]), "alt25": 100 - yz(sayac["ust25"]), "kg_var": yz(sayac["kg_var"]), "kg_yok": 100 - yz(sayac["kg_var"]), "n": n}


def analiz_hesapla(v):
    lam_ev, lam_dep, guven = hesapla_lambda(v)
    matris = poisson_matris(lam_ev, lam_dep, MAX_GOL)
    olas = matristen_olasilik(matris, MAX_GOL)
    toplam = olas["toplam"] or 1
    p1_po = olas["1"] / toplam * 100
    px_po = olas["X"] / toplam * 100
    p2_po = olas["2"] / toplam * 100
    ust25_po = olas["ust_25"] / toplam * 100
    kg_var_po = olas["kg_var"] / toplam * 100
    mc = monte_carlo_simulasyon(lam_ev, lam_dep, MONTE_CARLO_N)
    lig_ust25 = v.get("lig_ust25", 0.0); lig_kg = v.get("lig_kg", 0.0)
    p1 = p1_po * 0.60 + mc["p1"] * 0.40
    px = px_po * 0.60 + mc["px"] * 0.40
    p2 = p2_po * 0.60 + mc["p2"] * 0.40
    gal_e = v.get("galibiyet_ev", 0); gal_d = v.get("galibiyet_dep", 0)
    if gal_e > 0 and gal_d > 0:
        p1 = p1 * 0.85 + gal_e * 0.15
        p2 = p2 * 0.85 + gal_d * 0.15
    ber_e = v.get("beraberlik_ev", 0); ber_d = v.get("beraberlik_dep", 0)
    if ber_e > 0 and ber_d > 0:
        px = px * 0.85 + ((ber_e + ber_d) / 2) * 0.15
    t = p1 + px + p2
    if t > 0: p1, px, p2 = (p1 / t) * 100, (px / t) * 100, (p2 / t) * 100
    ust_25 = ust25_po * 0.60 + lig_ust25 * 0.10 + mc["ust25"] * 0.30 if lig_ust25 > 0 else ust25_po * 0.65 + mc["ust25"] * 0.35
    kg_var_model = kg_var_po * 0.40 + lig_kg * 0.30 + mc["kg_var"] * 0.30 if lig_kg > 0 else kg_var_po * 0.60 + mc["kg_var"] * 0.40
    kg_sik_e = v.get("kg_siklik_ev", 0); kg_sik_d = v.get("kg_siklik_dep", 0)
    if kg_sik_e > 0 and kg_sik_d > 0:
        kg_var_model = kg_var_model * 0.85 + ((kg_sik_e + kg_sik_d) / 2) * 0.15
    toplam_beklenen = lam_ev + lam_dep
    if toplam_beklenen < 1.80:
        bf = (1.80 - toplam_beklenen) / 1.80
        ust_25 = max(10.0, ust_25 * (1.0 - bf * 0.8))
        kg_var_model = max(15.0, kg_var_model * (1.0 - bf * 0.9))
    kg_yok_model = 100.0 - kg_var_model
    alt_25 = 100.0 - ust_25
    en_olasi = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    en_guvenli = max([("1X", p1 + px), ("X2", p2 + px), ("12", p1 + p2)], key=lambda x: x[1])
    return {
        "lam_ev": lam_ev, "lam_dep": lam_dep, "guven": guven, "matris": matris, "olas": olas,
        "p1": p1, "px": px, "p2": p2,
        "cifte_1x": p1 + px, "cifte_x2": p2 + px, "cifte_12": p1 + p2,
        "tahmini_gol": lam_ev + lam_dep, "ust_25": ust_25, "alt_25": alt_25,
        "kg_var_model": kg_var_model, "kg_yok_model": kg_yok_model,
        "en_olasi": en_olasi, "en_guvenli": en_guvenli,
        "en_olasi_gol": "Üst" if ust_25 > alt_25 else "Alt",
        "en_olasi_kg": "Var" if kg_var_model > kg_yok_model else "Yok",
        "p1_po": p1_po, "px_po": px_po, "p2_po": p2_po, "ust25_po": ust25_po, "kg_var_po": kg_var_po,
        "p1_mc": mc["p1"], "px_mc": mc["px"], "p2_mc": mc["p2"], "ust25_mc": mc["ust25"], "kg_var_mc": mc["kg_var"],
        "mc_n": mc["n"]
    }


def kayit_olustur(v, a):
    return {"veri": copy.deepcopy(v), "analiz": {
        "p1": a["p1"], "px": a["px"], "p2": a["p2"],
        "tahmini_gol": a["tahmini_gol"], "kg_var_model": a["kg_var_model"], "ust_25": a["ust_25"],
        "en_olasi_1x2": a["en_olasi"][0], "en_guvenli_cifte": a["en_guvenli"][0],
        "en_olasi_gol": a["en_olasi_gol"], "en_olasi_kg": a["en_olasi_kg"]}}


def sonuc_hesapla(kayit):
    v = kayit["veri"]; analiz = kayit.get("analiz", {})
    if not v.get("skor_belli", False): return None
    skor_ev = v.get("skor_ev", 0); skor_dep = v.get("skor_dep", 0)
    toplam_gol = skor_ev + skor_dep
    gercek_ust = toplam_gol > 2.5
    gercek_kg_var = (skor_ev > 0 and skor_dep > 0)
    gercek_1x2 = "1" if skor_ev > skor_dep else ("X" if skor_ev == skor_dep else "2")
    ust_25 = analiz.get("ust_25", 50); alt_25 = 100 - ust_25
    kg_var = analiz.get("kg_var_model", 50); kg_yok = 100 - kg_var
    p1_a = analiz.get("p1", 33.33); px_a = analiz.get("px", 33.33); p2_a = analiz.get("p2", 33.34)
    secim_1x2, yuzde_1x2 = max([("1", p1_a), ("X", px_a), ("2", p2_a)], key=lambda x: x[1])
    oneri_1x2 = secim_1x2 if yuzde_1x2 >= esik_1x2_al(secim_1x2) else None
    oneri_gol = None
    if ust_25 >= esik_al("ust") and ust_25 >= alt_25: oneri_gol = "Üst"
    elif alt_25 >= esik_al("alt") and alt_25 >= ust_25: oneri_gol = "Alt"
    oneri_kg = None
    if kg_var >= esik_al("kg_var") and kg_var >= kg_yok: oneri_kg = "Var"
    elif kg_yok >= esik_al("kg_yok") and kg_yok >= kg_var: oneri_kg = "Yok"
    d_o1 = None if oneri_1x2 is None else ("tam" if oneri_1x2 == gercek_1x2 else "yanlis")
    d_og = None if oneri_gol is None else ("tam" if oneri_gol == ("Üst" if gercek_ust else "Alt") else "yanlis")
    d_ok = None if oneri_kg is None else ("tam" if oneri_kg == ("Var" if gercek_kg_var else "Yok") else "yanlis")
    def _t(d): return None if d is None else (d == "tam")
    return {
        "oneri_1x2": {"tahmin": oneri_1x2, "tuttu": _t(d_o1), "durum": d_o1},
        "oneri_gol": {"tahmin": oneri_gol, "tuttu": _t(d_og), "durum": d_og},
        "oneri_kg": {"tahmin": oneri_kg, "tuttu": _t(d_ok), "durum": d_ok},
        "gercek_1x2": gercek_1x2,
        "gercek_gol": "Üst" if gercek_ust else "Alt",
        "gercek_kg": "Var" if gercek_kg_var else "Yok",
    }


# ==========================================
# UI YARDIMCILARI
# ==========================================
def _e(x): return _html.escape(str(x))


def rozet(metin, tip="gray"):
    return f'<span class="fa-badge fa-b-{tip}">{_e(metin)}</span>'


def mac_karti(ev, dep, skor_belli, skor_ev, skor_dep, lam_ev, lam_dep, saat="", ulke="", tarih=""):
    orta = f'<div class="fa-score">{int(skor_ev)} - {int(skor_dep)}</div>' if skor_belli else '<div class="fa-vs">VS</div>'
    bayrak = ulke_bayrak_bul(ulke)
    ust_bilgi = ""
    if saat or ulke or tarih:
        parcalar = []
        if bayrak != "🌍" or ulke: parcalar.append(f"{bayrak} {_e((ulke or '').title())}")
        if tarih: parcalar.append(f"📅 {_e(tarih)}")
        if saat: parcalar.append(f"🕐 {_e(saat)}")
        if parcalar: ust_bilgi = f'<div class="fa-sub" style="margin-bottom:8px;">{" • ".join(parcalar)}</div>'
    alt = f'<div class="fa-sub">Model beklenen gol: {lam_ev:.2f} - {lam_dep:.2f}</div>'
    return f'<div class="fa-hero">{ust_bilgi}<div class="fa-teams"><div class="fa-team">{_e(ev)}</div>{orta}<div class="fa-team">{_e(dep)}</div></div>{alt}</div>'


def olasilik_bar(etiket, yuzde, esik=None, renk="#3b82f6"):
    y = max(0.0, min(100.0, yuzde))
    isaret = ""
    if esik is not None:
        renk = "#22c55e" if yuzde >= esik else "#475569"
        isaret = f'<div class="fa-tick" style="left:{esik:.0f}%"></div>'
    return f'<div class="fa-row"><div class="fa-row-top"><span class="fa-lbl">{_e(etiket)}</span><span class="fa-val">%{yuzde:.1f}</span></div><div class="fa-bar"><div class="fa-fill" style="width:{y:.1f}%;background:{renk}"></div>{isaret}</div></div>'


def olasilik_paneli(a):
    satirlar = ('<div class="fa-ttl">Maç Sonucu</div>'
        + olasilik_bar("Ev Sahibi (1)", a["p1"], esik_1x2_al("1"), "#3b82f6")
        + olasilik_bar("Beraberlik (X)", a["px"], esik_1x2_al("X"), "#94a3b8")
        + olasilik_bar("Deplasman (2)", a["p2"], esik_1x2_al("2"), "#f59e0b")
        + '<div class="fa-ttl" style="margin-top:12px">Piyasalar</div>'
        + olasilik_bar("Üst 2.5", a["ust_25"], esik_al("ust"))
        + olasilik_bar("Alt 2.5", a["alt_25"], esik_al("alt"))
        + olasilik_bar("KG Var", a["kg_var_model"], esik_al("kg_var"))
        + olasilik_bar("KG Yok", a["kg_yok_model"], esik_al("kg_yok")))
    return f'<div class="fa-card">{satirlar}</div>'


def oneri_karti(baslik, secim, yuzde, esik, poz, alt_satir):
    if poz:
        seviye, _, _, etiket = guven_seviyesi_bul(yuzde)
        tip = "green" if seviye == "yuksek" else "yellow" if seviye == "orta" else "gray"
        durum = rozet(f"{etiket} güven", tip)
        sinif = "fa-card fa-pos"; pct_sinif = "fa-pct"
        not_satiri = f'<div class="fa-mut">{_e(alt_satir)}</div>'
    else:
        durum = rozet("Eşik altı", "gray"); sinif = "fa-card fa-neg"; pct_sinif = "fa-pct fa-off"
        not_satiri = f'<div class="fa-mut">{_e(alt_satir)} • Gerekli: %{esik:.0f}</div>'
    bar = olasilik_bar("", yuzde, esik)
    return f'<div class="{sinif}"><div class="fa-ttl">{_e(baslik)}</div><div class="fa-pickrow"><div><div class="fa-pick">{_e(secim)}</div>{durum}</div><div class="{pct_sinif}">%{yuzde:.1f}</div></div>{bar}{not_satiri}</div>'


def istat_karti(baslik, ist, esik_metni):
    t = ist["tam"]; y = ist["yakin"]; yl = ist["yanlis"]; top = t + y + yl
    if top == 0:
        govde = '<div class="fa-big fa-off">—</div><div class="fa-mut">Henüz bahis yok</div>'
    else:
        isabet = (t + y) / top * 100
        sinif = "fa-g" if isabet >= 85 else "fa-y" if isabet >= 70 else "fa-r"
        govde = f'<div class="fa-big {sinif}">%{isabet:.0f}</div><div class="fa-mut">✅ {t + y} doğru • ❌ {yl} yanlış</div>'
    return f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>{govde}<div class="fa-mut">{_e(esik_metni)}</div></div>'


def mac_tahmin_karti(v_g, g=None):
    try:
        ya = (g or {}).get("analiz", {})
        a = analiz_hesapla(v_g)
        p1 = a["p1"]; px = a["px"]; p2 = a["p2"]
        ust_25 = a["ust_25"]; alt_25 = a["alt_25"]
        kg_var = a["kg_var_model"]; kg_yok = a["kg_yok_model"]
        sec1x2, y1x2 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        e1x2 = esik_1x2_al(sec1x2)
        p1x2_poz = y1x2 >= e1x2
        isim1x2 = {"1": "1 — Ev Kazanır", "X": "X — Beraberlik", "2": "2 — Dep Kazanır"}[sec1x2]
        if ust_25 >= alt_25: gol_s = "Üst 2.5"; gol_y = ust_25; gol_e = esik_al("ust")
        else: gol_s = "Alt 2.5"; gol_y = alt_25; gol_e = esik_al("alt")
        gol_poz = gol_y >= gol_e
        if kg_var >= kg_yok: kg_s = "KG Var"; kg_y = kg_var; kg_e = esik_al("kg_var")
        else: kg_s = "KG Yok"; kg_y = kg_yok; kg_e = esik_al("kg_yok")
        kg_poz = kg_y >= kg_e
        def r(p): return "pass" if p else "off"
        def b(p): return "ok" if p else "no"
        def bt(p): return "✅" if p else "⚪"
        return f'''<div class="fa-mk">
        <div class="fa-mk-row"><span class="fa-mk-lbl">🎯 1X2</span><span class="fa-mk-pick {r(p1x2_poz)}">{_e(isim1x2)}</span><span class="fa-mk-pct">%{y1x2:.0f} <span class="fa-mk-badge {b(p1x2_poz)}">{bt(p1x2_poz)} eşik %{e1x2:.0f}</span></span></div>
        <div class="fa-mk-row"><span class="fa-mk-lbl">⚽ Gol</span><span class="fa-mk-pick {r(gol_poz)}">{_e(gol_s)}</span><span class="fa-mk-pct">%{gol_y:.0f} <span class="fa-mk-badge {b(gol_poz)}">{bt(gol_poz)} eşik %{gol_e:.0f}</span></span></div>
        <div class="fa-mk-row"><span class="fa-mk-lbl">🤝 KG</span><span class="fa-mk-pick {r(kg_poz)}">{_e(kg_s)}</span><span class="fa-mk-pct">%{kg_y:.0f} <span class="fa-mk-badge {b(kg_poz)}">{bt(kg_poz)} eşik %{kg_e:.0f}</span></span></div>
        </div>'''
    except Exception:
        return ""


def oneri_istatistik_guncel(gecmis):
    ist = {"1x2": {"tam": 0, "yakin": 0, "yanlis": 0}, "gol": {"tam": 0, "yakin": 0, "yanlis": 0}, "kg": {"tam": 0, "yakin": 0, "yanlis": 0}}
    for g in gecmis:
        try:
            v = g["veri"]
            if not v.get("skor_belli", False): continue
            ya = g.get("analiz", {})
            d = sonuc_hesapla({"veri": v, "analiz": ya})
            if not d: continue
            for key in ["oneri_1x2", "oneri_gol", "oneri_kg"]:
                kisa = key.replace("oneri_", "")
                durum = d[key].get("durum")
                if durum == "tam": ist[kisa]["tam"] += 1
                elif durum == "yanlis": ist[kisa]["yanlis"] += 1
        except Exception:
            continue
    return ist


def mac_sonuc_ikon(g):
    try:
        v = g["veri"]
        if not v.get("skor_belli", False): return "⚫"
        ya = g.get("analiz", {})
        d = sonuc_hesapla({"veri": v, "analiz": ya})
        if not d: return "⚫"
        verilen = [x for x in [d["oneri_1x2"]["tuttu"], d["oneri_gol"]["tuttu"], d["oneri_kg"]["tuttu"]] if x is not None]
        if not verilen: return "⚫"
        if all(verilen): return "✅"
        if not any(verilen): return "❌"
        return "🟡"
    except Exception:
        return "⚫"


def okunan_veriler_paneli(v):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{v.get('takim_ev', 'Ev')}**")
        st.markdown(f"- Atılan: **{v.get('atilan_ev', 0):.2f}**")
        st.markdown(f"- Yenen: **{v.get('yenen_ev', 0):.2f}**")
        st.markdown(f"- Clean sheets: **{v.get('clean_sheets_ev', 0):.1f}%**")
        st.markdown(f"- KG Var: **{v.get('kg_siklik_ev', 0):.1f}%**")
        st.markdown(f"- Üst 2.5: **{v.get('ust25_ev', 0):.1f}%**")
    with c2:
        st.markdown(f"**{v.get('takim_dep', 'Dep')}**")
        st.markdown(f"- Atılan: **{v.get('atilan_dep', 0):.2f}**")
        st.markdown(f"- Yenen: **{v.get('yenen_dep', 0):.2f}**")
        st.markdown(f"- Clean sheets: **{v.get('clean_sheets_dep', 0):.1f}%**")
        st.markdown(f"- KG Var: **{v.get('kg_siklik_dep', 0):.1f}%**")
        st.markdown(f"- Üst 2.5: **{v.get('ust25_dep', 0):.1f}%**")


def nav_bar():
    if st.session_state.sayfa == "giris": return
    try: kutu = st.container(key="fa_nav")
    except TypeError: kutu = st.container()
    with kutu:
        if admin_mi():
            secenekler = [("🏠", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek"), ("⚙️ Ayar", "ayarlar")]
        else:
            secenekler = [("🏠 Ana", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek")]
        kolonlar = st.columns(len(secenekler))
        for kol, (etiket, hedef) in zip(kolonlar, secenekler):
            with kol:
                aktif = st.session_state.sayfa == hedef
                if st.button(etiket, key=f"nav_{hedef}", use_container_width=True, type="primary" if aktif else "secondary"):
                    if not aktif:
                        st.session_state.sayfa = hedef
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
            st.session_state.toplu_cek_sonuc = None
            st.rerun()


# ==========================================
# GİRİŞ EKRANI
# ==========================================
def giris_ekrani():
    st.markdown("""
        <div class="login-hero">
            <div class="login-logo">⚽</div>
            <h1 class="login-title">Futbol Analiz Pro</h1>
            <p class="login-subtitle">Akıllı maç analizi ve tahmin motoru</p>
        </div>
    """, unsafe_allow_html=True)
    with st.form("giris_form"):
        sifre = st.text_input("🔐 Admin Şifresi", type="password", key="sifre_input", placeholder="Şifreni gir...")
        admin_btn = st.form_submit_button("👑  Admin Girişi", use_container_width=True, type="primary")
        st.markdown('<div class="login-divider">VEYA</div>', unsafe_allow_html=True)
        misafir_btn = st.form_submit_button("👤  Misafir Olarak Devam Et", use_container_width=True)
        if admin_btn:
            if sifre == ADMIN_SIFRE:
                st.session_state.giris_yapildi = True
                st.session_state.rol = "admin"
                st.session_state.sayfa = "giris"
                st.rerun()
            else:
                st.error("❌ Yanlış şifre.")
        if misafir_btn:
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


# ==========================================
# UYGULAMA BAŞLANGIÇ
# ==========================================
if not st.session_state.giris_yapildi:
    giris_ekrani()
    st.stop()

ust_bar()
nav_bar()


# ==========================================
# TOPLU ÇEKİM SONUÇLARI
# ==========================================
if st.session_state.toplu_cek_sonuc:
    st.markdown("<h1>🔄 Çekilen Maçlar</h1>", unsafe_allow_html=True)
    st.caption(f"{len(st.session_state.toplu_cek_sonuc)} maç çekildi.")
    for i, veri in enumerate(st.session_state.toplu_cek_sonuc):
        takim_ev = veri.get("takim_ev", "Ev"); takim_dep = veri.get("takim_dep", "Dep")
        saat = veri.get("saat", ""); tarih = veri.get("tarih", "")
        st.markdown(f"### {i+1}. {takim_ev} vs {takim_dep}")
        c_info, c_btn = st.columns([3, 1])
        with c_info:
            st.caption(f"🕐 {tarih} {saat} • Atılan: {veri.get('atilan_ev', 0):.1f}/{veri.get('atilan_dep', 0):.1f}")
        with c_btn:
            if st.button("🔍 Analiz Et", key=f"toplu_analiz_{i}", use_container_width=True, type="primary"):
                yeni_veri = copy.deepcopy(VARSAYILAN_VERI)
                yeni_veri.update(veri)
                st.session_state.form_verileri = yeni_veri
                st.session_state.kayit_yapildi = False
                st.session_state.okunamayan_alanlar = []
                st.session_state.manuel_bekleyen = []
                st.session_state.toplu_cek_sonuc = None
                st.session_state.sayfa = "sonuc"
                st.rerun()
        st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True):
        st.session_state.toplu_cek_sonuc = None
        st.rerun()
    st.stop()


# ==========================================
# ANA SAYFA
# ==========================================
if st.session_state.sayfa == "giris":
    if admin_mi():
        st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>Mutating.com'dan otomatik çek veya manuel yapıştır.</p>", unsafe_allow_html=True)

        sekme1, sekme2 = st.tabs(["🔄 Mutating'den Otomatik", "📋 Metin Yapıştır"])

        with sekme1:
            st.caption("Mutating.com ana sayfasındaki maçları tek tek açar ve verileri çeker.")
            max_mac = st.slider("Kaç maç çekilsin?", 1, 10, 5, 1, key="mutating_max")
            if st.button("🚀 Maçları Çek", use_container_width=True, type="primary", key="mutating_toplu_btn"):
                with st.spinner(f"İlk {max_mac} maç çekiliyor... (30-60 saniye)"):
                    basarili, hatali = mutating_toplu_cek(max_mac=max_mac)
                if hatali:
                    for h in hatali: st.warning(f"⚠️ {h}")
                if not basarili:
                    st.error("❌ Hiçbir maç çekilemedi.")
                else:
                    st.success(f"✅ {len(basarili)} maç çekildi!")
                    st.session_state.toplu_cek_sonuc = basarili
                    time.sleep(1)
                    st.rerun()

        with sekme2:
            st.caption("SportyTrader / Mutating metnini elle yapıştır.")
            yapistir_metni = st.text_area("Yapıştırma alanı", height=280, key="yapistir_input", label_visibility="collapsed", placeholder="İstatistik metnini buraya yapıştır.")
            if st.button("📋 Metinden Analiz Et", use_container_width=True, type="primary", key="metin_analiz_btn"):
                if not yapistir_metni.strip():
                    st.warning("⚠️ Önce metni yapıştır.")
                else:
                    cikan, okunamayanlar = metinden_veri_cikar(yapistir_metni)
                    if not cikan:
                        st.error("❌ Metinden hiçbir veri çıkarılamadı.")
                    else:
                        yeni_veri = copy.deepcopy(VARSAYILAN_VERI)
                        yeni_veri.update(cikan)
                        st.session_state.form_verileri = yeni_veri
                        st.session_state.kayit_yapildi = False
                        st.session_state.okunamayan_alanlar = okunamayanlar
                        st.session_state.manuel_bekleyen = okunamayanlar.copy()
                        if not veri_yeterli_mi(yeni_veri):
                            st.error("⚠️ Analiz için yeterli veri yok.")
                        else:
                            st.session_state.sayfa = "sonuc"
                            st.rerun()

        st.divider()
        col_bt1, col_bt2, col_bt3 = st.columns(3)
        with col_bt1:
            if st.button("📊 Geçmiş", use_container_width=True):
                st.session_state.sayfa = "gecmis"; st.rerun()
        with col_bt2:
            if st.button("🔮 Gelecek", use_container_width=True):
                st.session_state.sayfa = "gelecek"; st.rerun()
        with col_bt3:
            if st.button("⚙️ Ayarlar", use_container_width=True):
                st.session_state.sayfa = "ayarlar"; st.rerun()
    else:
        gecmis_sayi = len(st.session_state.gecmis_analizler)
        gelecek_sayi = len(st.session_state.gelecek_analizler)
        st.markdown(f"""
            <div class="mh-hero">
                <div class="mh-hero-icon">⚽</div>
                <div class="mh-hero-title">Futbol Analiz Pro</div>
                <div class="mh-hero-sub">Akıllı maç analizi ve tahmin motoru</div>
                <div class="mh-hero-badge">● CANLI VERİ</div>
            </div>
            <div class="mh-stat-grid">
                <div class="mh-stat"><div class="mh-stat-icon">📊</div><div class="mh-stat-num">{gecmis_sayi}</div><div class="mh-stat-lbl">Geçmiş Maç</div></div>
                <div class="mh-stat"><div class="mh-stat-icon">🔮</div><div class="mh-stat-num">{gelecek_sayi}</div><div class="mh-stat-lbl">Gelecek Maç</div></div>
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
        st.markdown("""
            <div class="mh-info">
                💡 <b>İpucu:</b> Geçmiş maçlarda isabet oranlarını incele, gelecek maçlarda yüksek güvenli tahminleri filtrele.
            </div>
        """, unsafe_allow_html=True)


# ==========================================
# GEÇMİŞ
# ==========================================
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gecmis = st.session_state.gecmis_analizler
    toplam = len(gecmis)
    oneri_ist = oneri_istatistik_guncel(gecmis)
    if toplam == 0:
        st.info("ℹ️ Henüz kayıtlı maç yok.")
    else:
        st.markdown("### 🎯 ÖNERİ İSTATİSTİKLERİ")
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.markdown(istat_karti("🎯 1X2", oneri_ist["1x2"], f"1 %{esik_1x2_al('1'):.0f} • X %{esik_1x2_al('X'):.0f} • 2 %{esik_1x2_al('2'):.0f}"), unsafe_allow_html=True)
        with col_2:
            st.markdown(istat_karti("⚽ Üst/Alt 2.5", oneri_ist["gol"], f"Üst %{esik_al('ust'):.0f} • Alt %{esik_al('alt'):.0f}"), unsafe_allow_html=True)
        with col_3:
            st.markdown(istat_karti("🤝 KG Var/Yok", oneri_ist["kg"], f"Var %{esik_al('kg_var'):.0f} • Yok %{esik_al('kg_yok'):.0f}"), unsafe_allow_html=True)
    st.divider()
    st.markdown(f"### ⚽ Maçlar ({toplam})")
    for i, g in enumerate(reversed(gecmis)):
        idx_gercek = len(gecmis) - 1 - i
        v_g = g["veri"]
        takim_ev = v_g.get("takim_ev", "Ev") or "Ev"
        takim_dep = v_g.get("takim_dep", "Dep") or "Dep"
        skor_ev = v_g.get("skor_ev", 0); skor_dep = v_g.get("skor_dep", 0)
        ikon = mac_sonuc_ikon(g)
        st.markdown(f"### {ikon}")
        st.markdown(mac_karti(takim_ev, takim_dep, True, skor_ev, skor_dep, 0, 0, saat=v_g.get("saat", ""), ulke=v_g.get("ulke", ""), tarih=v_g.get("tarih", "")), unsafe_allow_html=True)
        tahmin_html = mac_tahmin_karti(v_g, g)
        if tahmin_html: st.markdown(tahmin_html, unsafe_allow_html=True)
        if admin_mi():
            c_detay, c_sil = st.columns([5, 1])
            with c_detay:
                if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"mac_{idx_gercek}"):
                    st.session_state.form_verileri = copy.deepcopy(v_g)
                    st.session_state.kayit_yapildi = True
                    st.session_state.sayfa = "sonuc"
                    st.rerun()
            with c_sil:
                if st.button("🗑️", key=f"sil_{idx_gercek}"):
                    st.session_state.tek_silme_onay = idx_gercek if st.session_state.tek_silme_onay != idx_gercek else None
                    st.rerun()
            if st.session_state.tek_silme_onay == idx_gercek:
                st.warning(f"⚠️ **{takim_ev} vs {takim_dep}** silinsin mi?")
                ce, ch = st.columns(2)
                with ce:
                    if st.button("✅ Sil", key=f"evet_{idx_gercek}", use_container_width=True, type="primary"):
                        if 0 <= idx_gercek < len(st.session_state.gecmis_analizler):
                            st.session_state.gecmis_analizler.pop(idx_gercek)
                            gecmis_kaydet(st.session_state.gecmis_analizler)
                        st.session_state.tek_silme_onay = None
                        st.rerun()
                with ch:
                    if st.button("❌ İptal", key=f"hayir_{idx_gercek}", use_container_width=True):
                        st.session_state.tek_silme_onay = None
                        st.rerun()
        else:
            if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"mac_{idx_gercek}"):
                st.session_state.form_verileri = copy.deepcopy(v_g)
                st.session_state.kayit_yapildi = True
                st.session_state.sayfa = "sonuc"
                st.rerun()
        st.divider()
    if admin_mi():
        c_temizle, c_geri = st.columns(2)
        with c_temizle:
            if st.button("🗑️ Tüm Geçmişi Temizle", use_container_width=True, key="temizle_btn"):
                st.session_state.silme_onay = True; st.rerun()
        with c_geri:
            if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gecmis_geri"):
                st.session_state.sayfa = "giris"; st.rerun()
        if st.session_state.silme_onay:
            st.warning("⚠️ Tüm geçmiş silinecek. Emin misin?")
            ce, ch = st.columns(2)
            with ce:
                if st.button("✅ Evet, Sil", use_container_width=True, type="primary", key="sil_hepsi_evet"):
                    st.session_state.gecmis_analizler = []
                    try:
                        if os.path.exists(GECMIS_DOSYA): os.remove(GECMIS_DOSYA)
                    except Exception: pass
                    st.session_state.silme_onay = False
                    st.rerun()
            with ch:
                if st.button("❌ İptal", use_container_width=True, key="sil_hepsi_iptal"):
                    st.session_state.silme_onay = False; st.rerun()
    else:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gecmis_geri_misafir"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# GELECEK
# ==========================================
elif st.session_state.sayfa == "gelecek":
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    gelecek = st.session_state.gelecek_analizler
    if not gelecek:
        st.info("ℹ️ Gelecek maç yok.")
    else:
        for i, g in enumerate(reversed(gelecek)):
            idx_gercek = len(gelecek) - 1 - i
            v_g = g["veri"]
            takim_ev = v_g.get("takim_ev", "Ev") or "Ev"
            takim_dep = v_g.get("takim_dep", "Dep") or "Dep"
            try:
                a = analiz_hesapla(v_g)
                lam_ev = a["lam_ev"]; lam_dep = a["lam_dep"]
            except Exception:
                lam_ev = lam_dep = 0
            st.markdown(mac_karti(takim_ev, takim_dep, False, 0, 0, lam_ev, lam_dep, saat=v_g.get("saat", ""), ulke=v_g.get("ulke", ""), tarih=v_g.get("tarih", "")), unsafe_allow_html=True)
            th = mac_tahmin_karti(v_g, g)
            if th: st.markdown(th, unsafe_allow_html=True)
            if admin_mi():
                c_detay, c_sil = st.columns([5, 1])
                with c_detay:
                    if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"gmac_{idx_gercek}"):
                        st.session_state.form_verileri = copy.deepcopy(v_g)
                        st.session_state.kayit_yapildi = True
                        st.session_state.gelecekten_gelindi = True
                        st.session_state.aktif_gelecek_idx = idx_gercek
                        st.session_state.sayfa = "sonuc"
                        st.rerun()
                with c_sil:
                    if st.button("🗑️", key=f"gsil_{idx_gercek}"):
                        st.session_state.tek_silme_gelecek = idx_gercek if st.session_state.tek_silme_gelecek != idx_gercek else None
                        st.rerun()
                if st.session_state.tek_silme_gelecek == idx_gercek:
                    st.warning(f"⚠️ **{takim_ev} vs {takim_dep}** silinsin mi?")
                    ce, ch = st.columns(2)
                    with ce:
                        if st.button("✅ Sil", key=f"evet_g_{idx_gercek}", use_container_width=True, type="primary"):
                            if 0 <= idx_gercek < len(st.session_state.gelecek_analizler):
                                st.session_state.gelecek_analizler.pop(idx_gercek)
                                gelecek_kaydet(st.session_state.gelecek_analizler)
                            st.session_state.tek_silme_gelecek = None
                            st.rerun()
                    with ch:
                        if st.button("❌ İptal", key=f"hayir_g_{idx_gercek}", use_container_width=True):
                            st.session_state.tek_silme_gelecek = None; st.rerun()
            else:
                if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"gmac_{idx_gercek}"):
                    st.session_state.form_verileri = copy.deepcopy(v_g)
                    st.session_state.kayit_yapildi = True
                    st.session_state.sayfa = "sonuc"
                    st.rerun()
            st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="g_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# AYARLAR
# ==========================================
elif st.session_state.sayfa == "ayarlar":
    if not admin_mi():
        st.error("❌ Sadece admin.")
        st.stop()
    st.markdown("<h1>⚙️ Eşik Ayarları</h1>", unsafe_allow_html=True)
    mevcut = st.session_state.esikler.copy()
    st.markdown("### 🎯 Maç Sonucu Eşikleri")
    c1, c2, c3 = st.columns(3)
    with c1: yeni_1 = st.slider("1 (Ev) %", 0, 100, int(mevcut.get("esik_1", 55.0)), 1, key="ay_1")
    with c2: yeni_x = st.slider("X %", 0, 100, int(mevcut.get("esik_x", 55.0)), 1, key="ay_x")
    with c3: yeni_2 = st.slider("2 (Dep) %", 0, 100, int(mevcut.get("esik_2", 55.0)), 1, key="ay_2")
    st.markdown("### ⚽ Gol Eşikleri")
    c4, c5 = st.columns(2)
    with c4: yeni_ust = st.slider("Üst 2.5 %", 0, 100, int(mevcut["ust"]), 1, key="ay_ust")
    with c5: yeni_alt = st.slider("Alt 2.5 %", 0, 100, int(mevcut["alt"]), 1, key="ay_alt")
    st.markdown("### 🤝 KG Eşikleri")
    c6, c7 = st.columns(2)
    with c6: yeni_kg_var = st.slider("KG Var %", 0, 100, int(mevcut["kg_var"]), 1, key="ay_kgv")
    with c7: yeni_kg_yok = st.slider("KG Yok %", 0, 100, int(mevcut["kg_yok"]), 1, key="ay_kgy")
    st.divider()
    ck, cs, cg = st.columns(3)
    with ck:
        if st.button("💾 Kaydet", use_container_width=True, type="primary"):
            yeni = {"esik_1": float(yeni_1), "esik_x": float(yeni_x), "esik_2": float(yeni_2), "ust": float(yeni_ust), "alt": float(yeni_alt), "kg_var": float(yeni_kg_var), "kg_yok": float(yeni_kg_yok)}
            st.session_state.esikler = yeni
            ayarlar_kaydet(yeni)
            st.success("✅ Kaydedildi!")
    with cs:
        if st.button("🔄 Sıfırla", use_container_width=True):
            v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0}
            st.session_state.esikler = v
            ayarlar_kaydet(v)
            st.rerun()
    with cg:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="ay_geri"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SONUÇ
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)
    ust_25 = a["ust_25"]; alt_25 = a["alt_25"]
    kg_var_model = a["kg_var_model"]; kg_yok_model = a["kg_yok_model"]
    takim_ev = v.get("takim_ev", "") or "Ev Sahibi"
    takim_dep = v.get("takim_dep", "") or "Deplasman"
    skor_belli = v.get("skor_belli", False)
    skor_ev = v.get("skor_ev", 0); skor_dep = v.get("skor_dep", 0)

    st.markdown(mac_karti(takim_ev, takim_dep, skor_belli, skor_ev, skor_dep, a["lam_ev"], a["lam_dep"], saat=v.get("saat", ""), ulke=v.get("ulke", ""), tarih=v.get("tarih", "")), unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)

    with st.expander("📋 Okunan Veriler", expanded=False):
        okunan_veriler_paneli(v)

    st.divider()
    st.markdown("## 🏆 FİNAL ÖNERİ")

    secim_1x2, yuzde_1x2 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    esik_1x2_secim = esik_1x2_al(secim_1x2)
    poz_1x2 = yuzde_1x2 >= esik_1x2_secim
    isim_map = {"1": "1 (Ev Sahibi)", "X": "X (Beraberlik)", "2": "2 (Deplasman)"}
    st.markdown(oneri_karti("🎯 Maç Sonucu (1X2)", isim_map[secim_1x2], yuzde_1x2, esik_1x2_secim, poz_1x2, f"1: %{a['p1']:.1f} • X: %{a['px']:.1f} • 2: %{a['p2']:.1f}"), unsafe_allow_html=True)

    if ust_25 >= alt_25: gol_secim, gol_yuzde, gol_esik = "Üst 2.5", ust_25, esik_al("ust")
    else: gol_secim, gol_yuzde, gol_esik = "Alt 2.5", alt_25, esik_al("alt")
    gol_poz = gol_yuzde >= gol_esik
    st.markdown(oneri_karti("⚽ Gol", gol_secim, gol_yuzde, gol_esik, gol_poz, f"Üst %{ust_25:.1f} • Alt %{alt_25:.1f}"), unsafe_allow_html=True)

    if kg_var_model >= kg_yok_model: kg_secim, kg_yuzde, kg_esik = "KG Var", kg_var_model, esik_al("kg_var")
    else: kg_secim, kg_yuzde, kg_esik = "KG Yok", kg_yok_model, esik_al("kg_yok")
    kg_poz = kg_yuzde >= kg_esik
    st.markdown(oneri_karti("🤝 Karşılıklı Gol", kg_secim, kg_yuzde, kg_esik, kg_poz, f"Var %{kg_var_model:.1f} • Yok %{kg_yok_model:.1f}"), unsafe_allow_html=True)

    if st.session_state.gelecekten_gelindi and admin_mi():
        idx_g = st.session_state.aktif_gelecek_idx
        if idx_g is not None and 0 <= idx_g < len(st.session_state.gelecek_analizler):
            st.divider()
            st.markdown("### 📥 Sonucu Gir ve Geçmişe Taşı")
            sc1, sc2, sc3 = st.columns([1, 1, 1])
            with sc1: yse = st.number_input("Ev Gol", 0, 20, int(v.get("skor_ev", 0)), 1, key=f"gse_{idx_g}")
            with sc2: ysd = st.number_input("Dep Gol", 0, 20, int(v.get("skor_dep", 0)), 1, key=f"gsd_{idx_g}")
            with sc3:
                st.markdown(""); st.markdown("")
                if st.button("📥 Taşı", key=f"tasi_{idx_g}", use_container_width=True, type="primary"):
                    kayit = st.session_state.gelecek_analizler[idx_g]
                    kayit["veri"]["skor_ev"] = int(yse)
                    kayit["veri"]["skor_dep"] = int(ysd)
                    kayit["veri"]["skor_belli"] = True
                    yd = sonuc_hesapla(kayit)
                    if yd: kayit["dogruluk"] = yd
                    st.session_state.gecmis_analizler.append(kayit)
                    st.session_state.gelecek_analizler.pop(idx_g)
                    gecmis_kaydet(st.session_state.gecmis_analizler)
                    gelecek_kaydet(st.session_state.gelecek_analizler)
                    st.session_state.gelecekten_gelindi = False
                    st.session_state.aktif_gelecek_idx = None
                    st.session_state.sayfa = "gelecek"
                    st.rerun()

    kaydet_mi = gol_poz or kg_poz or poz_1x2
    if not st.session_state.kayit_yapildi and admin_mi():
        yeni_kayit = kayit_olustur(v, a)
        if skor_belli:
            st.session_state.gecmis_analizler.append(yeni_kayit)
            gecmis_kaydet(st.session_state.gecmis_analizler)
            if kaydet_mi: st.success("📊 Geçmişe kaydedildi.")
            else: st.info("📊 Geçmişe kaydedildi (öneri yoktu).")
        else:
            if kaydet_mi:
                st.session_state.gelecek_analizler.append(yeni_kayit)
                gelecek_kaydet(st.session_state.gelecek_analizler)
                st.info("🔮 Geleceğe kaydedildi.")
            else:
                st.warning("⚠️ Hiçbir market pozitif değil. Kaydedilmedi.")
        st.session_state.kayit_yapildi = True

    st.divider()
    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.sayfa = "giris"
        st.rerun()
