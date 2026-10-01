import streamlit as st
import math
import copy
import re
import random
import json
import os
import html as _html

# ===== VERİ ÇEKME =====
try:
    import requests
    import cloudscraper
    from bs4 import BeautifulSoup
    HTTP_OK = True
except ImportError:
    HTTP_OK = False

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

st.markdown("""
<style>
    .block-container { padding-top: 2rem !important; padding-bottom: 0.5rem !important;
        padding-left: 0.7rem !important; padding-right: 0.7rem !important; max-width: 100% !important; }
    h1 { font-size: 1.2rem !important; margin: 0.2rem 0 !important; text-align: center; }
    h2 { font-size: 1rem !important; margin: 0.3rem 0 !important; }
    h3 { font-size: 0.9rem !important; margin: 0.15rem 0 !important; }
    p { font-size: 0.85rem !important; margin: 0.2rem 0 !important; }
    hr { margin: 0.3rem 0 !important; border-color: #23304a !important; }
    div[data-testid="stNumberInput"] label p { font-size: 0.75rem !important; margin: 0 !important; }
    div[data-testid="stNumberInput"] input { font-size: 0.85rem !important; padding: 0.15rem 0.3rem !important; height: 1.8rem !important; }
    div[data-testid="stNumberInput"] button { height: 1.8rem !important; padding: 0 !important; width: 1.5rem !important; }
    .stButton button { padding: 0.4rem 0.6rem !important; font-size: 0.9rem !important; height: 2.2rem !important; }
    div[data-testid="stAlert"] { padding: 0.3rem 0.5rem !important; font-size: 0.85rem !important; border-radius: 12px !important; }
    textarea { font-size: 0.75rem !important; }
    div[data-testid="stExpander"] summary { font-size: 0.9rem !important; padding: 0.4rem !important; }
    .stApp { background: #0b1220 !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp div[data-testid="stMarkdownContainer"] { color: #e6edf7 !important; }
    .stApp div[data-testid="stCaptionContainer"], .stApp div[data-testid="stCaptionContainer"] *, .stApp small { color: #8fa0bd !important; }
    h1 { letter-spacing: 0.2px; }
    h2, h3 { border-left: 3px solid #22c55e; padding-left: 0.45rem; }
    .stTextArea textarea, .stTextInput input, div[data-testid="stNumberInput"] input {
        background: #131c2e !important; color: #e6edf7 !important; border: 1px solid #23304a !important; border-radius: 10px !important; }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="base-input"] { background: #131c2e !important; border-radius: 10px !important; }
    .stButton button, div[data-testid="stDownloadButton"] button, div[data-testid="stFormSubmitButton"] button {
        background: #18233a !important; border: 1px solid #23304a !important; border-radius: 12px !important; font-weight: 600 !important; }
    .stButton button p, div[data-testid="stDownloadButton"] button p, div[data-testid="stFormSubmitButton"] button p { color: #e6edf7 !important; }
    .stButton button:hover { border-color: #22c55e !important; }
    .stButton button[kind="primary"], button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] {
        background: linear-gradient(135deg, #16a34a, #22c55e) !important; border: none !important; }
    .stButton button[kind="primary"] p, button[data-testid="stBaseButton-primary"] p, button[data-testid="stBaseButton-primaryFormSubmit"] p { color: #04130a !important; }
    div[data-testid="stExpander"] { background: #131c2e !important; border: 1px solid #23304a !important; border-radius: 14px !important; }
    div[data-testid="stExpander"] details { border: none !important; }
    div[data-testid="stFileUploader"] section { background: #131c2e !important; border: 1px dashed #23304a !important; border-radius: 12px !important; }
    .st-key-fa_nav div[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.3rem !important; }
    .st-key-fa_nav div[data-testid="stColumn"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
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
    .login-logo { font-size: 4.5rem; line-height: 1; margin-bottom: 12px; display: inline-block;
        filter: drop-shadow(0 0 20px rgba(34,197,94,0.5)); animation: logoPulse 3s ease-in-out infinite; }
    @keyframes logoPulse { 0%, 100% { transform: scale(1); filter: drop-shadow(0 0 15px rgba(34,197,94,0.4)); }
        50% { transform: scale(1.06); filter: drop-shadow(0 0 32px rgba(34,197,94,0.85)); } }
    .login-title { font-size: 2rem !important; font-weight: 900 !important;
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; margin: 0 !important; padding: 0 !important;
        letter-spacing: 1.2px; border: none !important; text-align: center !important; }
    .login-subtitle { font-size: 0.88rem; color: #8fa0bd !important; margin-top: 8px; letter-spacing: 0.5px; font-weight: 500; }
    div[data-testid="stForm"] { background: linear-gradient(145deg, rgba(19,28,46,0.85), rgba(11,18,32,0.95)) !important;
        border: 1px solid rgba(34,197,94,0.18) !important; border-radius: 22px !important; padding: 24px 20px !important;
        box-shadow: 0 12px 48px rgba(0,0,0,0.45) !important; }
    div[data-testid="stForm"] label p { font-size: 0.8rem !important; font-weight: 700 !important; color: #cbd5e1 !important; }
    div[data-testid="stForm"] input { height: 46px !important; font-size: 0.95rem !important; padding: 0 14px !important;
        background: rgba(11,18,32,0.85) !important; border: 1.5px solid #23304a !important; border-radius: 12px !important; }
    div[data-testid="stForm"] input:focus { border-color: #22c55e !important; box-shadow: 0 0 0 3px rgba(34,197,94,0.18) !important; }
    div[data-testid="stForm"] button { height: 46px !important; font-size: 0.95rem !important; font-weight: 700 !important; border-radius: 12px !important; }
    div[data-testid="stForm"] button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; border: none !important; }
    div[data-testid="stForm"] button[kind="secondary"] { background: rgba(30,41,59,0.55) !important; border: 1.5px solid #23304a !important; }
    .login-divider { display: flex; align-items: center; gap: 12px; margin: 10px 0 6px 0; color: #64748b !important; font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; justify-content: center; }
    .login-divider::before, .login-divider::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, transparent, #23304a 50%, transparent); }
    .login-features { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 22px; padding: 0 10px; }
    .lf-chip { display: inline-block; padding: 6px 14px; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.25); border-radius: 99px; font-size: 0.75rem; font-weight: 600; color: #cbd5e1 !important; }
    .login-footer { text-align: center; margin-top: 26px; font-size: 0.72rem; color: #64748b !important; }
    .login-footer b { color: #22c55e !important; font-weight: 700; }
    .mh-hero { position: relative; overflow: hidden; text-align: center; padding: 30px 14px 22px 14px;
        background: linear-gradient(135deg, rgba(22,35,61,0.85), rgba(15,26,46,0.9));
        border: 1px solid rgba(34,197,94,0.22); border-radius: 22px; margin: 6px 0 16px 0; }
    .mh-hero::before { content: ""; position: absolute; top: -60%; left: -60%; width: 220%; height: 220%;
        background: radial-gradient(circle at 50% 50%, rgba(34,197,94,0.15), transparent 55%);
        animation: mhGlow 5s ease-in-out infinite; pointer-events: none; }
    @keyframes mhGlow { 0%, 100% { opacity: 0.5; transform: scale(1) rotate(0deg); }
        50% { opacity: 1; transform: scale(1.15) rotate(20deg); } }
    .mh-hero-icon { font-size: 3.2rem; margin-bottom: 10px; display: inline-block;
        filter: drop-shadow(0 0 20px rgba(34,197,94,0.55)); animation: logoPulse 3s ease-in-out infinite; position: relative; z-index: 1; }
    .mh-hero-title { font-size: 1.7rem; font-weight: 900;
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        letter-spacing: 1px; position: relative; z-index: 1; margin: 0; }
    .mh-hero-sub { font-size: 0.84rem; color: #8fa0bd; margin-top: 8px; position: relative; z-index: 1; }
    .mh-hero-badge { display: inline-block; margin-top: 12px; padding: 4px 14px;
        background: rgba(34,197,94,0.12); border: 1px solid rgba(34,197,94,0.4); border-radius: 99px;
        font-size: 0.72rem; font-weight: 700; color: #22c55e !important; position: relative; z-index: 1; }
    .mh-stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 0 0 16px 0; }
    .mh-stat { position: relative; background: linear-gradient(145deg, #16233d, #0f1a2e);
        border: 1px solid #23304a; border-radius: 16px; padding: 14px 8px 12px 8px; text-align: center; overflow: hidden; }
    .mh-stat::after { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #22c55e, #3b82f6); }
    .mh-stat-icon { font-size: 1.3rem; margin-bottom: 2px; }
    .mh-stat-num { font-size: 1.85rem; font-weight: 900; color: #22c55e !important; line-height: 1; }
    .mh-stat-lbl { font-size: 0.68rem; color: #8fa0bd !important; margin-top: 5px; text-transform: uppercase; font-weight: 700; }
    .mh-section-title { font-size: 0.78rem; color: #8fa0bd !important; text-transform: uppercase; font-weight: 700;
        margin: 4px 0 8px 4px; border-left: 3px solid #22c55e; padding-left: 8px; }
    .st-key-fa_misafir_nav .stButton button { height: 72px !important; font-size: 1rem !important; font-weight: 800 !important;
        border-radius: 16px !important; box-shadow: 0 8px 24px rgba(34,197,94,0.25) !important; }
    .st-key-fa_misafir_nav .stButton button p { font-size: 1rem !important; font-weight: 800 !important; }
    .mh-info { background: linear-gradient(145deg, rgba(19,28,46,0.6), rgba(11,18,32,0.8));
        border: 1px solid #23304a; border-radius: 14px; padding: 12px 14px; margin-top: 14px;
        font-size: 0.76rem; color: #8fa0bd !important; line-height: 1.6; }
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
    varsayilan = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0,
                  "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0}
    try:
        if os.path.exists(AYARLAR_DOSYA):
            with open(AYARLAR_DOSYA, "r", encoding="utf-8") as f:
                y = json.load(f)
                if "1x2" in y and "esik_1" not in y:
                    e = float(y["1x2"])
                    y["esik_1"] = e; y["esik_x"] = e; y["esik_2"] = e
                varsayilan.update(y)
    except Exception:
        pass
    return varsayilan


def ayarlar_kaydet(esikler):
    try:
        with open(AYARLAR_DOSYA, "w", encoding="utf-8") as f:
            json.dump(esikler, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


ESIK_YUKSEK = 65.0
ESIK_ORTA = 55.0
ESIK_BELIRSIZ = 50.0
MONTE_CARLO_N = 10000

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
    "kg_siklik_ev": 50.0, "kg_siklik_dep": 50.0,
    "btts_1h_ev": 0.0, "btts_1h_dep": 0.0, "btts_2h_ev": 0.0, "btts_2h_dep": 0.0,
    "btts_over15_ev": 0.0, "btts_over15_dep": 0.0, "btts_over25_ev": 0.0, "btts_over25_dep": 0.0,
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
    "lose_1h_ev": 0.0, "lose_1h_dep": 0.0,
    "win_btts_ev": 0.0, "win_btts_dep": 0.0, "draw_btts_ev": 0.0, "draw_btts_dep": 0.0,
    "lose_btts_ev": 0.0, "lose_btts_dep": 0.0,
    "win_over15_ev": 0.0, "win_over15_dep": 0.0, "lose_over15_ev": 0.0, "lose_over15_dep": 0.0,
    "takim_ev": "", "takim_dep": "", "skor_ev": 0, "skor_dep": 0,
    "skor_belli": False, "lig_ort_toplam": 0.0, "lig_ust25": 0.0, "lig_kg": 0.0,
    "saat": "", "tarih": "", "ulke": "", "format": "bilinmiyor",
}

MAX_GOL = 8
BELIRSIZLIK = 0.20

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
if "esikler" not in st.session_state: st.session_state.esikler = ayarlar_yukle()
if "bt_market" not in st.session_state:
    st.session_state.bt_market = {"1x2": False, "kg_var": False, "kg_yok": False, "ust": False, "alt": False}
if "bt_market_esik" not in st.session_state:
    st.session_state.bt_market_esik = {"esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0,
                                        "kg_var": 70.0, "kg_yok": 70.0, "ust": 70.0, "alt": 70.0}
if "bt_sonuc" not in st.session_state: st.session_state.bt_sonuc = None
if "bt_detaylar" not in st.session_state: st.session_state.bt_detaylar = []


def admin_mi(): return st.session_state.get("rol") == "admin"
def esik_al(key): return st.session_state.esikler.get(key, 50.0)
def esik_1x2_al(secim):
    km = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}
    return st.session_state.esikler.get(km.get(secim, ""), 55.0)


ULKE_BAYRAK = {
    "switzerland": "🇨🇭", "isviçre": "🇨🇭", "england": "", "ingiltere": "",
    "spain": "🇪🇸", "ispanya": "🇪🇸", "italy": "🇮🇹", "italya": "🇮🇹",
    "germany": "🇩🇪", "almanya": "🇩🇪", "france": "🇫🇷", "fransa": "🇫🇷",
    "netherlands": "🇳🇱", "hollanda": "🇳🇱", "portugal": "🇵🇹", "portekiz": "🇵🇹",
    "belgium": "🇧🇪", "belçika": "🇧🇪", "turkey": "🇹🇷", "türkiye": "🇹🇷",
    "argentina": "🇦🇷", "arjantin": "🇦🇷", "brazil": "🇧🇷", "brezilya": "🇧🇷",
    "mexico": "🇲🇽", "meksika": "🇲🇽", "usa": "🇺🇸", "abd": "🇺🇸",
    "japan": "🇯🇵", "japonya": "🇯🇵", "south korea": "🇰🇷", "güney kore": "🇰🇷",
    "china": "🇨🇳", "çin": "🇨🇳", "russia": "🇷🇺", "rusya": "🇷🇺",
    "ukraine": "🇺🇦", "ukrayna": "🇺🇦", "poland": "🇵🇱", "polonya": "🇵🇱",
    "greece": "🇬🇷", "yunanistan": "🇬🇷", "scotland": "", "i̇skoçya": "",
    "wales": "", "galler": "",
    "ireland": "🇮🇪", "i̇rlanda": "🇮🇪", "austria": "🇦🇹", "avusturya": "🇦🇹",
    "croatia": "🇭🇷", "hırvatistan": "🇭🇷", "serbia": "🇷🇸", "sırbistan": "🇷🇸",
    "romania": "🇷🇴", "romanya": "🇷🇴", "bulgaria": "🇧🇬", "bulgaristan": "🇧🇬",
    "denmark": "🇩🇰", "danimarka": "🇩🇰", "sweden": "🇸🇪", "i̇sveç": "🇸🇪",
    "norway": "🇳🇴", "norveç": "🇳🇴", "finland": "🇫🇮", "finlandiya": "🇫🇮",
    "iceland": "🇮🇸", "i̇zlanda": "🇮🇸", "hungary": "🇭🇺", "macaristan": "🇭🇺",
    "czech": "🇨🇿", "çekya": "🇨🇿", "slovakia": "🇸🇰", "slovakya": "🇸🇰",
    "slovenia": "🇸🇮", "slovenya": "🇸🇮", "saudi": "🇸🇦", "suudi arabistan": "🇸🇦",
    "qatar": "🇶🇦", "katar": "🇶🇦", "egypt": "🇪🇬", "mısır": "🇪🇬",
    "morocco": "🇲🇦", "fas": "🇲🇦", "algeria": "🇩🇿", "cezayir": "🇩🇿",
    "tunisia": "🇹🇳", "tunus": "🇹🇳", "nigeria": "🇳🇬", "nijerya": "🇳🇬",
    "south africa": "🇿🇦", "güney afrika": "🇿🇦", "australia": "🇦🇺", "avustralya": "🇦🇺",
    "new zealand": "🇳🇿", "yeni zelanda": "🇳🇿", "india": "🇮🇳", "hindistan": "🇮🇳",
    "iran": "🇮🇷", "iraq": "🇮🇶", "irak": "🇮🇶", "israel": "🇮🇱", "i̇srail": "🇮🇱",
    "colombia": "🇨🇴", "kolombiya": "🇨🇴", "chile": "🇨🇱", "şili": "🇨🇱",
    "peru": "🇵🇪", "uruguay": "🇺🇾", "ecuador": "🇪🇨", "ekvador": "🇪🇨",
    "paraguay": "🇵🇾", "bolivia": "🇧🇴", "bolivya": "🇧🇴", "venezuela": "🇻🇪",
    "costa rica": "🇨🇷", "panama": "🇵🇦", "jamaica": "🇯🇲",
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
    "andorra": "🇦🇩", "san marino": "🇸🇲", "gibraltar": "🇬🇮", "faroe": "🇫🇴",
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
    s = m.group(1).strip()
    if not s: return ""
    alt = s.lower()
    for a in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if a in alt: return a
    p = s.split()
    return " ".join(p[:2]) if len(p) >= 2 else (p[0] if p else "")


def clamp(x, lo, hi): return max(lo, min(hi, x))


def ort_iki(a, b):
    v = [x for x in [a, b] if x is not None and x > 0]
    return sum(v) / len(v) if v else 0


def guven_seviyesi_bul(o):
    if o >= ESIK_YUKSEK: return ("yuksek", "🟢", "success", "Yüksek")
    if o >= ESIK_ORTA: return ("orta", "🟡", "warning", "Orta")
    if o >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "error", "Belirsiz")
    return ("cok_dusuk", "⚫", "error", "Düşük")


def oneri_istatistik_guncel(gecmis):
    ist = {"1x2": {"tam": 0, "yakin": 0, "yanlis": 0},
           "gol": {"tam": 0, "yakin": 0, "yanlis": 0},
           "kg": {"tam": 0, "yakin": 0, "yanlis": 0}}
    for g in gecmis:
        try:
            v = g["veri"]
            if not v.get("skor_belli", False): continue
            try: ya = yeniden_analiz(v)
            except Exception: ya = g.get("analiz", {})
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


def wilson_aralik(d, t, z=1.96):
    if t <= 0: return 0.0, 0.0
    p = d / t
    payda = 1 + z * z / t
    merkez = (p + z * z / (2 * t)) / payda
    yari = z * math.sqrt(p * (1 - p) / t + z * z / (4 * t * t)) / payda
    return max(0.0, (merkez - yari) * 100), min(100.0, (merkez + yari) * 100)


def _form_ppg(s):
    return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1)


def yeniden_analiz(v):
    v2 = copy.deepcopy(v)
    if v2.get("form_str_ev"): v2["ppg_ev"] = _form_ppg(v2["form_str_ev"])
    if v2.get("form_str_dep"): v2["mpg_dep"] = _form_ppg(v2["form_str_dep"])
    key = json.dumps(v2, sort_keys=True, ensure_ascii=False)
    if "bt_analiz_cache" not in st.session_state: st.session_state.bt_analiz_cache = {}
    cache = st.session_state.bt_analiz_cache
    if key not in cache:
        a = analiz_hesapla(v2)
        cache[key] = {"ust_25": a["ust_25"], "kg_var_model": a["kg_var_model"],
                      "p1": a["p1"], "px": a["px"], "p2": a["p2"]}
    return cache[key]


def backtest_hesapla(gecmis, msec, mesik):
    sonuc = {"1x2": {"dogru": 0, "yanlis": 0}, "kg_var": {"dogru": 0, "yanlis": 0},
             "kg_yok": {"dogru": 0, "yanlis": 0}, "ust": {"dogru": 0, "yanlis": 0},
             "alt": {"dogru": 0, "yanlis": 0}}
    detay = []
    for g in gecmis:
        try:
            v = g["veri"]; an = g.get("analiz", {})
            if not v.get("skor_belli", False): continue
            se = int(v.get("skor_ev", 0)); sd = int(v.get("skor_dep", 0))
            tg = se + sd
            gkg = (se > 0 and sd > 0)
            gust = tg > 2.5
            if se > sd: g1x2 = "1"
            elif se == sd: g1x2 = "X"
            else: g1x2 = "2"
            try:
                ya = yeniden_analiz(v)
                u25 = ya["ust_25"]; kg = ya["kg_var_model"]
                p1y = ya["p1"]; pxy = ya["px"]; p2y = ya["p2"]
            except Exception:
                u25 = an.get("ust_25", 50); kg = an.get("kg_var_model", 50)
                p1y = an.get("p1", 33.33); pxy = an.get("px", 33.33); p2y = an.get("p2", 33.34)
            a25 = 100 - u25; kgy = 100 - kg
            mk = {"takim_ev": v.get("takim_ev", "Ev"), "takim_dep": v.get("takim_dep", "Dep"),
                  "skor": f"{se}-{sd}", "gercek_kg": "Var" if gkg else "Yok",
                  "gercek_gol": "Üst" if gust else "Alt", "gercek_1x2": g1x2, "detaylar": []}
            if msec.get("1x2", False):
                en = max([("1", p1y), ("X", pxy), ("2", p2y)], key=lambda x: x[1])
                sec, yuzde = en
                ek = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}[sec]
                es = mesik.get(ek, 55.0)
                if yuzde >= es:
                    if sec == g1x2: sonuc["1x2"]["dogru"] += 1; mk["detaylar"].append(f"1X2: {sec} ✅")
                    else: sonuc["1x2"]["yanlis"] += 1; mk["detaylar"].append(f"1X2: {sec} ❌")
            if msec.get("kg_var", False):
                if kg >= mesik["kg_var"] and kg >= kgy:
                    if gkg: sonuc["kg_var"]["dogru"] += 1; mk["detaylar"].append("KG Var ✅")
                    else: sonuc["kg_var"]["yanlis"] += 1; mk["detaylar"].append("KG Var ❌")
            if msec.get("kg_yok", False):
                if kgy >= mesik["kg_yok"] and kgy >= kg:
                    if not gkg: sonuc["kg_yok"]["dogru"] += 1; mk["detaylar"].append("KG Yok ✅")
                    else: sonuc["kg_yok"]["yanlis"] += 1; mk["detaylar"].append("KG Yok ❌")
            if msec.get("ust", False):
                if u25 >= mesik["ust"] and u25 >= a25:
                    if gust: sonuc["ust"]["dogru"] += 1; mk["detaylar"].append("Üst ✅")
                    else: sonuc["ust"]["yanlis"] += 1; mk["detaylar"].append("Üst ❌")
            if msec.get("alt", False):
                if a25 >= mesik["alt"] and a25 >= u25:
                    if not gust: sonuc["alt"]["dogru"] += 1; mk["detaylar"].append("Alt ✅")
                    else: sonuc["alt"]["yanlis"] += 1; mk["detaylar"].append("Alt ❌")
            if mk["detaylar"]: detay.append(mk)
        except Exception:
            continue
    return sonuc, detay


MANUEL_ALANLAR = {
    "Sıralama": [("siralama_ev", "Ev Sıralaması", "int", 1), ("siralama_dep", "Dep Sıralaması", "int", 1)],
    "Takım isimleri (Ev)": [("takim_ev", "Ev Takım Adı", "str", "")],
    "Takım isimleri (Dep)": [("takim_dep", "Dep Takım Adı", "str", "")],
    "PPG (Ev Form)": [("ppg_ev", "PPG (Ev)", "float", 0.0)],
    "MPG (Dep Form)": [("mpg_dep", "MPG (Dep)", "float", 0.0)],
    "xG": [("xg_ev", "xG (Ev)", "float", 0.0), ("xg_dep", "xG (Dep)", "float", 0.0)],
    "Atılan Gol": [("atilan_ev", "Atılan Gol (Ev)", "float", 0.0), ("atilan_dep", "Atılan Gol (Dep)", "float", 0.0)],
    "Yenen Gol": [("yenen_ev", "Yenen Gol (Ev)", "float", 0.0), ("yenen_dep", "Yenen Gol (Dep)", "float", 0.0)],
}


def _cift_tab(etiket, blok):
    p = r'([\d.,]+)%?\s*\t\s*' + re.escape(etiket) + r'\s*\t\s*([\d.,]+)%?'
    m = re.search(p, blok, re.IGNORECASE)
    if m:
        try: return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError: pass
    p2 = r'([\d.,]+)%?\s{1,4}' + re.escape(etiket) + r'\s{1,4}([\d.,]+)%?'
    m = re.search(p2, blok, re.IGNORECASE)
    if m:
        try: return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError: pass
    return None, None


def _sira_bul(metin, takim):
    if not takim: return None, None
    p = (r'(?:^|\n)\s*(\d{1,2})\s*\r?\n\s*' + re.escape(takim) + r'\s*\r?\n\s*'
         + re.escape(takim) + r'\s*\r?\n' r'\s*(\d+)\s*\t')
    m = re.search(p, metin, re.MULTILINE)
    if m:
        try:
            s = int(m.group(1))
            if 1 <= s <= 30:
                dev = metin[m.end()-1:]
                mp = re.match(r'[\s\S]{0,80}?\r?\n\s*(\d{1,2})\s*\r?\n', dev)
                pn = int(mp.group(1)) if mp else 0
                return s, pn
        except (ValueError, AttributeError): pass
    return None, None


def sportytrader_veri_cikar(metin):
    veri = {}; ok = []
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
    else: veri["skor_belli"] = False
    te = veri.get("takim_ev", ""); td = veri.get("takim_dep", "")
    idx = metin.find("Main Stats")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for et, k1, k2 in [("Goals scored per game", "atilan_ev", "atilan_dep"),
                            ("Goals conceded per game", "yenen_ev", "yenen_dep"),
                            ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"),
                            ("Team scored", "team_scored_ev", "team_scored_dep"),
                            ("Team scored twice", "team_scored_2_ev", "team_scored_2_dep"),
                            ("Scored in both halves", "scored_both_halves_ev", "scored_both_halves_dep"),
                            ("Goal in both halves", "goal_both_halves_ev", "goal_both_halves_dep")]:
            v1, v2 = _cift_tab(et, blok)
            if v1 is not None: veri[k1] = v1; veri[k2] = v2
    idx = metin.find("Win Draw Lose")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for et, k1, k2 in [("Win and Over 1.5 goals", "win_over15_ev", "win_over15_dep"),
                            ("Lose and Over 1.5 goals", "lose_over15_ev", "lose_over15_dep"),
                            ("Team win first half", "win_1h_ev", "win_1h_dep"),
                            ("Team draw at half time", "draw_ht_ev", "draw_ht_dep"),
                            ("Team lost first half", "lose_1h_ev", "lose_1h_dep")]:
            v1, v2 = _cift_tab(et, blok)
            if v1 is not None: veri[k1] = v1; veri[k2] = v2
        for et, ke, kd in [("Win", "galibiyet_ev", "galibiyet_dep"),
                            ("Draw", "beraberlik_ev", "beraberlik_dep"),
                            ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
            p = r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*' + et + r'\s*\t\s*([\d.,]+)%'
            mm = re.search(p, blok, re.MULTILINE)
            if mm:
                try:
                    veri[ke] = float(mm.group(1).replace(",", "."))
                    veri[kd] = float(mm.group(2).replace(",", "."))
                except ValueError: pass
    idx = metin.find("Both Teams to Score")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for et, k1, k2 in [("BTTS in first-half", "btts_1h_ev", "btts_1h_dep"),
                            ("BBTS in second-half", "btts_2h_ev", "btts_2h_dep"),
                            ("BBTS and Over 1.5", "btts_over15_ev", "btts_over15_dep"),
                            ("BBTS and Over 2.5", "btts_over25_ev", "btts_over25_dep"),
                            ("Win and BTTS", "win_btts_ev", "win_btts_dep"),
                            ("Draw and BTTS", "draw_btts_ev", "draw_btts_dep"),
                            ("Lose and BTTS", "lose_btts_ev", "lose_btts_dep")]:
            v1, v2 = _cift_tab(et, blok)
            if v1 is not None: veri[k1] = v1; veri[k2] = v2
        m = re.search(r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*Both Teams to Score\s*\t\s*([\d.,]+)%', blok, re.MULTILINE)
        if m:
            try:
                veri["kg_siklik_ev"] = float(m.group(1).replace(",", "."))
                veri["kg_siklik_dep"] = float(m.group(2).replace(",", "."))
            except ValueError: pass
    idx = metin.find("Match Total Goals")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for et, k1, k2 in [("Match total goals 0 or 1", "tg_01_ev", "tg_01_dep"),
                            ("Match total goals 2 or 3", "tg_23_ev", "tg_23_dep"),
                            ("Match total goals 4+", "tg_4p_ev", "tg_4p_dep"),
                            ("Match total goals 0", "tg_0_ev", "tg_0_dep"),
                            ("Match total goals 1", "tg_1_ev", "tg_1_dep"),
                            ("Match total goals 2", "tg_2_ev", "tg_2_dep"),
                            ("Match total goals 3", "tg_3_ev", "tg_3_dep")]:
            v1, v2 = _cift_tab(et, blok)
            if v1 is not None: veri[k1] = v1; veri[k2] = v2
        if veri.get("tg_4_ev", 0) == 0 and veri.get("tg_4p_ev", 0) > 0:
            veri["tg_4_ev"] = veri["tg_4p_ev"]; veri["tg_4_dep"] = veri["tg_4p_dep"]
    idx = metin.find("Over Under Goals")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for et, k1, k2 in [("Over 0.5 goals at half-time", "ht_ust05_ev", "ht_ust05_dep"),
                            ("Over 1.5 goals at half-time", "ht_ust15_ev", "ht_ust15_dep"),
                            ("Over 2.5 goals at half-time", "ht_ust25_ev", "ht_ust25_dep"),
                            ("Over 0.5 goals", "ust05_ev", "ust05_dep"),
                            ("Over 1.5 goals", "ust15_ev", "ust15_dep"),
                            ("Over 2.5 goals", "ust25_ev", "ust25_dep"),
                            ("Over 3.5 goals", "ust35_ev", "ust35_dep")]:
            v1, v2 = _cift_tab(et, blok)
            if v1 is not None: veri[k1] = v1; veri[k2] = v2
    idx = metin.find("Half Time-Full Time")
    if idx != -1:
        blok = metin[idx:idx+2000]
        for et, k in [("Win HT - Win FT", "wht_wft"), ("Win HT - Draw FT", "wht_dft"),
                      ("Win HT - Lose FT", "wht_lft"), ("Draw HT - Win FT", "dht_wft"),
                      ("Draw HT - Draw FT", "dht_dft"), ("Draw HT - Lose FT", "dht_lft"),
                      ("Lose HT - Win FT", "lht_wft"), ("Lose HT - Draw FT", "lht_dft"),
                      ("Lose HT - Lose FT", "lht_lft")]:
            v1, v2 = _cift_tab(et, blok)
            if v1 is not None: veri[k + "_ev"] = v1; veri[k + "_dep"] = v2
    if te:
        s, p = _sira_bul(metin, te)
        if s is not None: veri["siralama_ev"] = s
    if td:
        s, p = _sira_bul(metin, td)
        if s is not None: veri["siralama_dep"] = s
    if veri.get("siralama_ev", 0) == 0: ok.append("Sıralama (Ev)")
    if veri.get("siralama_dep", 0) == 0: ok.append("Sıralama (Dep)")
    m = re.search(r'\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\nForm\s*\t?\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])', metin)
    if m:
        fe = m.group(1) + m.group(2) + m.group(3) + m.group(4) + m.group(5)
        fd = m.group(6) + m.group(7) + m.group(8) + m.group(9) + m.group(10)
        veri["form_str_ev"] = fe; veri["form_str_dep"] = fd
        def _fp(s): return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1)
        veri["ppg_ev"] = _fp(fe); veri["mpg_dep"] = _fp(fd)
    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) +
                                  veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2
    veri["format"] = "sportytrader"
    return veri, ok


def _sf(s):
    if s is None: return None
    try: return float(str(s).strip().replace(",", ".").replace("%", ""))
    except (ValueError, AttributeError): return None


def _etiket_esle(etiket):
    e = etiket.lower().strip()
    mp = [(("goals scored", "scored per game", "avg goals for", "goals for"), ("atilan_ev", "atilan_dep")),
          (("goals conceded", "conceded per game", "avg goals against", "goals against"), ("yenen_ev", "yenen_dep")),
          (("clean sheet",), ("clean_sheets_ev", "clean_sheets_dep")),
          (("failed to score",), ("_fail_ev", "_fail_dep")),
          (("scored in", "team scored", "scored at least one"), ("team_scored_ev", "team_scored_dep")),
          (("over 2.5", "over 2,5"), ("ust25_ev", "ust25_dep")),
          (("over 1.5", "over 1,5"), ("ust15_ev", "ust15_dep")),
          (("over 3.5", "over 3,5"), ("ust35_ev", "ust35_dep")),
          (("both teams", "btts"), ("kg_siklik_ev", "kg_siklik_dep"))]
    for kws, keys in mp:
        for kw in kws:
            if kw in e: return keys
    return None


def soccerstats_metin_cikar(metin):
    veri = {}
    satirlar = metin.split("\n")
    for s in satirlar[:30]:
        m = re.search(r'([A-ZÀ-Ý][a-zA-ZÀ-ÿ\s\.\']+?)\s+(?:vs?\.?|v|VS?)\s+([A-ZÀ-Ý][a-zA-ZÀ-ÿ\s\.\']+)', s)
        if m:
            veri["takim_ev"] = m.group(1).strip(); veri["takim_dep"] = m.group(2).strip()
            break
    for satir in satirlar:
        s = satir.strip()
        if len(s) < 5 or len(s) > 200: continue
        say = re.findall(r'\d+[\.,]?\d*%?', s)
        say = [_sf(x) for x in say]
        say = [x for x in say if x is not None]
        if len(say) < 2: continue
        keys = _etiket_esle(s)
        if keys:
            k1, k2 = keys
            if k1.startswith("_fail"):
                veri["team_scored_ev"] = 100 - say[0]
                veri["team_scored_dep"] = 100 - say[1] if len(say) > 1 else 100 - say[0]
            else:
                veri[k1] = say[0]
                veri[k2] = say[1] if len(say) > 1 else say[0]
    veri["format"] = "soccerstats"; veri["skor_belli"] = False
    return veri, []


def metinden_veri_cikar(metin):
    metin = metin.replace(",", ".")
    if "Main Stats" in metin and "Goals scored per game" in metin:
        veri, ok = sportytrader_veri_cikar(metin)
        if not veri.get("takim_ev"): ok.append("Takım isimleri (Ev)")
        if not veri.get("takim_dep"): ok.append("Takım isimleri (Dep)")
        return veri, ok
    if "Goals" in metin and ("Scored" in metin or "Conceded" in metin):
        return soccerstats_metin_cikar(metin)
    return {"format": "genel"}, []


def html_metne_cevir(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "head", "meta", "link"]):
        tag.decompose()
    for table in soup.find_all("table"):
        satirlar = []
        for tr in table.find_all("tr"):
            h = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            if h: satirlar.append("\t".join(h))
        if satirlar: table.replace_with("\n" + "\n".join(satirlar) + "\n")
    metin = soup.get_text(separator="\n")
    satirlar = [s.strip() for s in metin.split("\n") if s.strip()]
    return "\n".join(satirlar)


def _scraper_olustur():
    try:
        return cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "mobile": False})
    except Exception:
        try: return cloudscraper.create_scraper()
        except Exception: return None


def soccerstats_veri_cikar(url):
    if not HTTP_OK: return None, [], "requests/cloudscraper/bs4 kurulu degil."
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
                   "Referer": "https://www.soccerstats.com/"}
        sc = _scraper_olustur()
        if sc is None: return None, [], "Cloudscraper baslatilamadi."
        r = sc.get(url, headers=headers, timeout=25, allow_redirects=True)
        if r.status_code != 200: return None, [], f"HTTP {r.status_code}"
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg"]): tag.decompose()
        veri = {}
        title = soup.find("title")
        if title:
            t = title.get_text()
            m = re.search(r'([A-Za-zÀ-ÿ\s\.\'\-]+?)\s+(?:vs?\.?|v)\s+([A-Za-zÀ-ÿ\s\.\'\-]+?)(?:\s*[-|]|\s+Football|\s*$)', t, re.IGNORECASE)
            if m: veri["takim_ev"] = m.group(1).strip(); veri["takim_dep"] = m.group(2).strip()
        if "league=" in url:
            m = re.search(r'league=([a-z0-9_]+)', url, re.IGNORECASE)
            if m: veri["ulke"] = m.group(1).replace("_", " ").title()
        tm = []; es = 0
        for table in soup.find_all("table"):
            mt = table.get_text(separator=" ", strip=True)
            if not any(k in mt.lower() for k in ["scored", "conceded", "clean sheet", "btts", "both teams", "over 1.5", "over 2.5"]):
                continue
            for tr in table.find_all("tr"):
                hc = tr.find_all(["td", "th"])
                if len(hc) < 3: continue
                hm = [h.get_text(strip=True) for h in hc]
                hm = [h for h in hm if h]
                if len(hm) < 3: continue
                et = hm[0]
                sy = [_sf(h) for h in hm[1:]]
                sy = [s for s in sy if s is not None]
                if len(sy) < 2: continue
                keys = _etiket_esle(et)
                if keys:
                    k1, k2 = keys
                    veri[k1] = sy[0]; veri[k2] = sy[1] if len(sy) > 1 else sy[0]
                    es += 1
                tm.append("\t".join(hm))
        if veri.get("_fail_ev") is not None and not veri.get("team_scored_ev"):
            veri["team_scored_ev"] = 100 - veri["_fail_ev"]
        if veri.get("_fail_dep") is not None and not veri.get("team_scored_dep"):
            veri["team_scored_dep"] = 100 - veri["_fail_dep"]
        veri.pop("_fail_ev", None); veri.pop("_fail_dep", None)
        if not any(k in veri for k in ["atilan_ev", "yenen_ev", "ust25_ev", "kg_siklik_ev"]):
            ft = soup.get_text(separator="\n")
            fb, _ = soccerstats_metin_cikar(ft)
            if fb and any(k in fb for k in ["atilan_ev", "yenen_ev"]):
                veri.update(fb); es += 1
        if es == 0 and not any(k in veri for k in ["atilan_ev", "yenen_ev", "ust25_ev", "kg_siklik_ev"]):
            return None, [], "Istatistikler tanimlanamadi. Metin Yapistir modunu kullan."
        veri["format"] = "soccerstats"; veri["skor_belli"] = False
        return veri, [], None
    except Exception as e: return None, [], "Hata: " + str(e)[:200]


def sportytrader_url_cek(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
                   "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"}
        sc = _scraper_olustur()
        if sc is None: return None, [], "Cloudscraper yok."
        r = sc.get(url, headers=headers, timeout=25, allow_redirects=True)
        if r.status_code != 200: return None, [], f"HTTP {r.status_code}"
        metin = html_metne_cevir(r.text)
        veri, ok = metinden_veri_cikar(metin)
        if not veri or (not veri.get("takim_ev") and not veri.get("atilan_ev")):
            return None, [], "Sportytrader stats sayfasinin URL'ini kullan veya Metin moduna gec."
        return veri, ok, None
    except Exception as e: return None, [], "Hata: " + str(e)[:200]


def genel_url_cek(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
        sc = _scraper_olustur()
        if sc is None: return None, [], "Cloudscraper yok."
        r = sc.get(url, headers=headers, timeout=25, allow_redirects=True)
        if r.status_code != 200: return None, [], f"HTTP {r.status_code}"
        metin = html_metne_cevir(r.text)
        veri, _ = soccerstats_metin_cikar(metin)
        if veri.get("atilan_ev") or veri.get("yenen_ev") or veri.get("ust25_ev"):
            return veri, [], None
        v2, ok = metinden_veri_cikar(metin)
        if v2.get("atilan_ev") or v2.get("takim_ev"):
            return v2, ok, None
        return None, [], "Parser tanimlanamadi. Metin Yapistir modunu kullan."
    except Exception as e: return None, [], "Hata: " + str(e)[:200]


def url_den_veri_cek(url):
    if not HTTP_OK: return None, [], "requests/cloudscraper/bs4 kurulu degil."
    url = url.strip()
    if not url.startswith(("http://", "https://")): url = "https://" + url
    if "soccerstats.com" in url.lower(): return soccerstats_veri_cikar(url)
    elif "sportytrader.com" in url.lower(): return sportytrader_url_cek(url)
    else: return genel_url_cek(url)


# ============ POISSON & MOTOR ============
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


def poisson_matris(le, ld, mg=MAX_GOL):
    return [[poisson_pmf(i, le) * poisson_pmf(j, ld) for j in range(mg)] for i in range(mg)]


def hesapla_lambda(v):
    ae = v.get("atilan_ev", 0.0); ye = v.get("yenen_ev", 0.0)
    ad = v.get("atilan_dep", 0.0); yd = v.get("yenen_dep", 0.0)
    xge = v.get("xg_ev", 0.0); xgd = v.get("xg_dep", 0.0)
    heb = (xge * 0.60 + ae * 0.40) if xge > 0 else (ae if ae > 0 else 1.2)
    hdb = (xgd * 0.60 + ad * 0.40) if xgd > 0 else (ad if ad > 0 else 1.0)
    tse = v.get("team_scored_ev", 0); tsd = v.get("team_scored_dep", 0)
    if tse > 0: heb *= clamp(tse / 60, 0.7, 1.3)
    if tsd > 0: hdb *= clamp(tsd / 60, 0.7, 1.3)
    sdz = yd if yd > 0 else 1.2
    sez = ye if ye > 0 else 1.0
    cse = v.get("clean_sheets_ev", 0.0); csd = v.get("clean_sheets_dep", 0.0)
    def csf(cs):
        if cs <= 0: return 1.0
        if cs < 40.0: return 1.0 - (cs / 250.0)
        return max(0.40, 0.84 - (cs - 40.0) * (0.44 / 60.0))
    dfr = csf(cse); efr = csf(csd)
    leh = heb * 0.60 + sdz * 0.40
    ldh = hdb * 0.60 + sez * 0.40
    u25e = v.get("ust25_ev", 0); u25d = v.get("ust25_dep", 0)
    if u25e > 0: leh *= clamp(u25e / 50, 0.85, 1.15)
    if u25d > 0: ldh *= clamp(u25d / 50, 0.85, 1.15)
    kge = v.get("kg_siklik_ev", 0); kgd = v.get("kg_siklik_dep", 0)
    if kge > 0 and kgd > 0:
        kgo = (kge + kgd) / 2
        if kgo >= 60: leh *= 1.05; ldh *= 1.05
        elif kgo <= 35: leh *= 0.95; ldh *= 0.95
    fe = clamp(1 + (v.get("ppg_ev", 1.5) - 1.5) / 15, 0.85, 1.15)
    fd = clamp(1 + (v.get("mpg_dep", 1.5) - 1.5) / 15, 0.85, 1.15)
    se = v.get("siralama_ev", 10); sd = v.get("siralama_dep", 10)
    db = 1.0
    if 1 <= se <= 5 and sd >= 10: db = 1.20
    gev = v.get("galibiyet_ev", 0); gdp = v.get("galibiyet_dep", 0)
    if gev > 0 and gdp > 0:
        if gev - gdp >= 25: leh *= 1.08; ldh *= 0.95
        elif gdp - gev >= 25: leh *= 0.95; ldh *= 1.08
    ww = v.get("wht_wft_ev", 0); ll = v.get("lht_lft_ev", 0)
    if ww >= 25: leh *= 1.05
    if ll >= 25: ldh *= 1.05
    le = leh * 1.05 * fe * efr * db
    ld = ldh * 0.95 * fd * dfr
    if le > 2.50: le = 2.50 + (le - 2.50) * 0.5
    if ld > 2.50: ld = 2.50 + (ld - 2.50) * 0.5
    return clamp(le, 0.05, 4.5), clamp(ld, 0.05, 4.5), 0.80


def matristen_olasilik(m, mg=MAX_GOL):
    p1 = px = p2 = 0.0
    u05 = u15 = u25 = u35 = 0.0
    kg = 0.0; sk = {}; tp = 0.0
    for i in range(mg):
        for j in range(mg):
            p = m[i][j]; tp += p
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
    return {"1": p1, "X": px, "2": p2, "ust_05": u05, "ust_15": u15,
            "ust_25": u25, "ust_35": u35, "kg_var": kg, "skorlar": sk, "toplam": tp}


def veri_yeterli_mi(v):
    on = [v["atilan_ev"], v["atilan_dep"], v["yenen_ev"], v["yenen_dep"]]
    return sum(1 for x in on if x > 0) >= 2


def mac_ici_sok(le, ld, rng=None):
    r = rng if rng is not None else random
    if r.random() < 0.03:
        if r.random() < 0.5: le *= 0.70
        else: ld *= 0.70
    return le, ld


def monte_carlo(leb, ldb, n=MONTE_CARLO_N):
    seed = int(round(leb * 1_000_000)) * 1_000_003 + int(round(ldb * 1_000_000))
    rng = random.Random(seed)
    sc = {"1": 0, "X": 0, "2": 0, "u25": 0, "kg": 0}
    for _ in range(n):
        sep = rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        sdp = rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        le = leb * sep; ld = ldb * sdp
        le, ld = mac_ici_sok(le, ld, rng)
        eg = min(MAX_GOL - 1, poisson_random(le, rng))
        dg = min(MAX_GOL - 1, poisson_random(ld, rng))
        if eg > dg: sc["1"] += 1
        elif eg == dg: sc["X"] += 1
        else: sc["2"] += 1
        if eg + dg > 2.5: sc["u25"] += 1
        if eg > 0 and dg > 0: sc["kg"] += 1
    def y(s): return s / n * 100 if n > 0 else 0
    return {"p1": y(sc["1"]), "px": y(sc["X"]), "p2": y(sc["2"]),
            "ust25": y(sc["u25"]), "alt25": 100 - y(sc["u25"]),
            "kg_var": y(sc["kg"]), "kg_yok": 100 - y(sc["kg"]), "n": n}


def analiz_hesapla(v):
    le, ld, gv = hesapla_lambda(v)
    m = poisson_matris(le, ld)
    ol = matristen_olasilik(m)
    tp = ol["toplam"] or 1
    p1po = ol["1"] / tp * 100; pxpo = ol["X"] / tp * 100
    p2po = ol["2"] / tp * 100; u25po = ol["ust_25"] / tp * 100
    kgpo = ol["kg_var"] / tp * 100
    mc = monte_carlo(le, ld)
    p1 = p1po * 0.60 + mc["p1"] * 0.40
    px = pxpo * 0.60 + mc["px"] * 0.40
    p2 = p2po * 0.60 + mc["p2"] * 0.40
    gev = v.get("galibiyet_ev", 0); gdp = v.get("galibiyet_dep", 0)
    if gev > 0 and gdp > 0:
        p1 = p1 * 0.85 + gev * 0.15
        p2 = p2 * 0.85 + gdp * 0.15
    bev = v.get("beraberlik_ev", 0); bdp = v.get("beraberlik_dep", 0)
    if bev > 0 and bdp > 0:
        bo = (bev + bdp) / 2
        px = px * 0.85 + bo * 0.15
    t = p1 + px + p2
    if t > 0: p1, px, p2 = p1/t*100, px/t*100, p2/t*100
    lu25 = v.get("lig_ust25", 0.0)
    lkg = v.get("lig_kg", 0.0)
    u25 = (u25po * 0.60 + lu25 * 0.10 + mc["ust25"] * 0.30) if lu25 > 0 else (u25po * 0.65 + mc["ust25"] * 0.35)
    u15e = v.get("ust15_ev", 0); u15d = v.get("ust15_dep", 0)
    if u15e > 0 and u15d > 0:
        u15o = (u15e + u15d) / 2
        if u15o >= 70: u25 = u25 * 0.90 + u15o * 0.10
    u35e = v.get("ust35_ev", 0); u35d = v.get("ust35_dep", 0)
    if u35e > 0 and u35d > 0:
        u35o = (u35e + u35d) / 2
        if u35o >= 40: u25 = u25 * 0.92 + u35o * 0.08
    t3e = v.get("tg_3_ev", 0); t3d = v.get("tg_3_dep", 0)
    t4e = v.get("tg_4_ev", 0); t4d = v.get("tg_4_dep", 0)
    t3p = ort_iki((t3e + t4e) if (t3e > 0 or t4e > 0) else 0, (t3d + t4d) if (t3d > 0 or t4d > 0) else 0)
    if t3p > 0 and t3p >= 50: u25 = u25 * 0.93 + t3p * 0.07
    kg = (kgpo * 0.40 + lkg * 0.30 + mc["kg_var"] * 0.30) if lkg > 0 else (kgpo * 0.60 + mc["kg_var"] * 0.40)
    kse = v.get("kg_siklik_ev", 0); ksd = v.get("kg_siklik_dep", 0)
    if kse > 0 and ksd > 0:
        ko = (kse + ksd) / 2
        kg = kg * 0.85 + ko * 0.15
    b1e = v.get("btts_1h_ev", 0); b1d = v.get("btts_1h_dep", 0)
    if b1e > 0 and b1d > 0:
        b1o = (b1e + b1d) / 2
        if b1o >= 30: kg = kg * 0.95 + b1o * 0.05
    b2e = v.get("btts_2h_ev", 0); b2d = v.get("btts_2h_dep", 0)
    if b2e > 0 and b2d > 0:
        b2o = (b2e + b2d) / 2
        if b2o >= 30: kg = kg * 0.95 + b2o * 0.05
    t0 = ort_iki(v.get("tg_0_ev", 0), v.get("tg_0_dep", 0))
    t1 = ort_iki(v.get("tg_1_ev", 0), v.get("tg_1_dep", 0))
    if t0 >= 15 or t1 >= 15:
        kyl = t0 + t1
        if kyl >= 30: kg = kg * 0.90 + (100 - kyl) * 0.10
    tbg = le + ld
    if tbg < 1.80:
        bf = (1.80 - tbg) / 1.80
        u25 = max(10.0, u25 * (1.0 - bf * 0.8))
        kg = max(15.0, kg * (1.0 - bf * 0.9))
    cse = v.get("clean_sheets_ev", 0.0); csd = v.get("clean_sheets_dep", 0.0)
    if cse >= 50.0 and ld < 1.0: kg *= 0.80
    if csd >= 50.0 and le < 1.0: kg *= 0.80
    kgy = 100 - kg
    if kgy > 68.0 and p1 > 55.0 and le >= 1.70: u25 = min(68.0, u25 * 1.35)
    a25 = 100 - u25
    eo = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    eg = max([("1X", p1+px), ("X2", p2+px), ("12", p1+p2)], key=lambda x: x[1])
    eog = "Üst" if u25 > a25 else "Alt"
    eokg = "Var" if kg > kgy else "Yok"
    return {"lam_ev": le, "lam_dep": ld, "guven": gv, "matris": m, "olas": ol,
            "p1": p1, "px": px, "p2": p2,
            "cifte_1x": p1+px, "cifte_x2": p2+px, "cifte_12": p1+p2,
            "tahmini_gol": tbg, "ust_25": u25, "alt_25": a25,
            "kg_var_model": kg, "kg_yok_model": kgy,
            "en_olasi": eo, "en_guvenli": eg,
            "en_olasi_gol": eog, "en_olasi_kg": eokg,
            "p1_po": p1po, "px_po": pxpo, "p2_po": p2po, "ust25_po": u25po, "kg_var_po": kgpo,
            "p1_mc": mc["p1"], "px_mc": mc["px"], "p2_mc": mc["p2"],
            "ust25_mc": mc["ust25"], "kg_var_mc": mc["kg_var"], "mc_n": mc["n"]}


def kayit_olustur(v, a):
    return {"veri": copy.deepcopy(v), "analiz": {
        "p1": a["p1"], "px": a["px"], "p2": a["p2"],
        "tahmini_gol": a["tahmini_gol"], "kg_var_model": a["kg_var_model"], "ust_25": a["ust_25"],
        "en_olasi_1x2": a["en_olasi"][0], "en_guvenli_cifte": a["en_guvenli"][0],
        "en_olasi_gol": a["en_olasi_gol"], "en_olasi_kg": a["en_olasi_kg"]}}


def sonuc_hesapla(kayit):
    v = kayit["veri"]; an = kayit.get("analiz", {})
    if not v.get("skor_belli", False): return None
    se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    tg = se + sd
    gust = tg > 2.5
    gkg = (se > 0 and sd > 0)
    if se > sd: g1x2 = "1"
    elif se == sd: g1x2 = "X"
    else: g1x2 = "2"
    u25 = an.get("ust_25", 50); a25 = 100 - u25
    kg = an.get("kg_var_model", 50); kgy = 100 - kg
    p1a = an.get("p1", 33.33); pxa = an.get("px", 33.33); p2a = an.get("p2", 33.34)
    en = max([("1", p1a), ("X", pxa), ("2", p2a)], key=lambda x: x[1])
    sec, yuzde = en
    o1 = sec if yuzde >= esik_1x2_al(sec) else None
    og = None
    if u25 >= esik_al("ust") and u25 >= a25: og = "Üst"
    elif a25 >= esik_al("alt") and a25 >= u25: og = "Alt"
    ok = None
    if kg >= esik_al("kg_var") and kg >= kgy: ok = "Var"
    elif kgy >= esik_al("kg_yok") and kgy >= kg: ok = "Yok"
    do1 = None if o1 is None else ("tam" if o1 == g1x2 else "yanlis")
    dog = None
    if og is not None:
        gy = "Üst" if gust else "Alt"; dog = "tam" if og == gy else "yanlis"
    dok = None
    if ok is not None:
        gy = "Var" if gkg else "Yok"; dok = "tam" if ok == gy else "yanlis"
    def _t(d): return None if d is None else (d == "tam")
    return {"oneri_1x2": {"tahmin": o1, "tuttu": _t(do1), "durum": do1},
            "oneri_gol": {"tahmin": og, "tuttu": _t(dog), "durum": dog},
            "oneri_kg": {"tahmin": ok, "tuttu": _t(dok), "durum": dok},
            "gercek_1x2": g1x2, "gercek_gol": "Üst" if gust else "Alt",
            "gercek_kg": "Var" if gkg else "Yok"}


# ============ YORUMLAR ============
def detayli_analiz_yorumu(v):
    y = []
    ppg, mpg = v["ppg_ev"], v["mpg_dep"]
    f = ppg - mpg
    if ppg >= 2.0 and mpg <= 1.0: t = f"Ev sahibi evinde mükemmel form (**PPG {ppg:.2f}**), deplasman zayıf (**MPG {mpg:.2f}**)."
    elif f >= 0.7: t = f"Ev sahibi form olarak önde (**PPG {ppg:.2f}** vs **{mpg:.2f}**)."
    elif f <= -0.7: t = f"Deplasman form olarak önde (**MPG {mpg:.2f}** vs **{ppg:.2f}**)."
    else: t = f"Form dengeli (**PPG {ppg:.2f}** vs **MPG {mpg:.2f}**)."
    y.append(("📈 FORM", t))
    se, sd = v["siralama_ev"], v["siralama_dep"]
    if se > 0 and sd > 0:
        fs = sd - se
        if fs >= 8: t = f"Ev sahibi **{se}.**, deplasman **{sd}.** sırada. **{fs} basamak** ciddi fark."
        elif fs >= 3: t = f"Ev sahibi **{se}.**, deplasman **{sd}.** sırada. Ev sahibi üstün."
        elif fs <= -8: t = f"Deplasman **{sd}.**, ev sahibi **{se}.** sırada. Deplasman **{abs(fs)} basamak** yukarıda."
        else: t = f"Sıralamalar yakın (Ev **{se}.** / Dep **{sd}.**)."
        y.append(("🏆 SIRALAMA", t))
    ae, ad = v["atilan_ev"], v["atilan_dep"]
    if ae - ad >= 0.6: t = f"Ev sahibi maç başına **{ae:.1f}** gol atıyor, deplasman **{ad:.1f}**."
    elif ae - ad <= -0.6: t = f"Deplasman maç başına **{ad:.1f}** gol atıyor, ev sahibi **{ae:.1f}**."
    else: t = f"Atılan goller benzer (Ev **{ae:.1f}** / Dep **{ad:.1f}**)."
    y.append(("⚽ ATILAN GOL", t))
    ye, yd = v["yenen_ev"], v["yenen_dep"]
    if yd - ye >= 0.7: t = f"Ev sahibi savunması sağlam (**{ye:.1f}**), deplasman zayıf (**{yd:.1f}**)."
    elif yd - ye <= -0.7: t = f"Deplasman savunması sağlam (**{yd:.1f}**), ev sahibi zayıf (**{ye:.1f}**)."
    else: t = f"Savunmalar benzer (Ev **{ye:.1f}** / Dep **{yd:.1f}**)."
    y.append(("🛡️ YENEN GOL", t))
    return y


def gol_detayli(v, a):
    u25 = a["ust_25"]; a25 = a["alt_25"]
    le = a["lam_ev"]; ld = a["lam_dep"]; tl = le + ld
    ae = v.get("atilan_ev", 0); ad = v.get("atilan_dep", 0)
    ye = v.get("yenen_ev", 0); yd = v.get("yenen_dep", 0)
    lo = v.get("lig_ort_toplam", 0)
    u15 = ort_iki(v.get("ust15_ev", 0), v.get("ust15_dep", 0))
    u35 = ort_iki(v.get("ust35_ev", 0), v.get("ust35_dep", 0))
    tg23 = ort_iki(v.get("tg_2_ev", 0) + v.get("tg_3_ev", 0), v.get("tg_2_dep", 0) + v.get("tg_3_dep", 0))
    tg4 = ort_iki(v.get("tg_4_ev", 0), v.get("tg_4_dep", 0))
    y = []
    if u25 >= esik_al("ust"):
        y.append(f"🎯 **ÜST 2.5 NEDEN POZİTİF? (%{u25:.1f})**")
        y.append(f"- Toplam beklenen gol: **{tl:.2f}**")
        y.append(f"- Ev sahibi atak gücü: **{ae:.2f}** gol/maç")
        y.append(f"- Deplasman atak gücü: **{ad:.2f}** gol/maç")
        y.append(f"- Ev sahibi yenen: **{ye:.2f}** gol/maç")
        y.append(f"- Deplasman yenen: **{yd:.2f}** gol/maç")
        if lo > 0: y.append(f"- Lig ortalaması: **{lo:.2f}**")
        if u15 > 0: y.append(f"- Üst 1.5: **%{u15:.0f}**")
        if u35 > 0: y.append(f"- Üst 3.5: **%{u35:.0f}**")
        if tg23 > 0: y.append(f"- TG 2-3: **%{tg23:.0f}**")
        if tg4 > 0: y.append(f"- TG 4+: **%{tg4:.0f}**")
    elif a25 >= esik_al("alt"):
        y.append(f"🎯 **ALT 2.5 NEDEN POZİTİF? (%{a25:.1f})**")
        y.append(f"- Toplam beklenen gol: **{tl:.2f}**")
        cse = v.get("clean_sheets_ev", 0); csd = v.get("clean_sheets_dep", 0)
        if cse >= 40: y.append(f"- ✅ Ev clean sheet: **%{cse:.0f}**")
        if csd >= 40: y.append(f"- ✅ Dep clean sheet: **%{csd:.0f}**")
        tg01 = ort_iki(v.get("tg_0_ev", 0) + v.get("tg_1_ev", 0), v.get("tg_0_dep", 0) + v.get("tg_1_dep", 0))
        if tg01 > 0: y.append(f"- TG 0-1: **%{tg01:.0f}**")
    return y


def kg_detayli(v, a):
    kg = a["kg_var_model"]; kgy = a["kg_yok_model"]
    le = a["lam_ev"]; ld = a["lam_dep"]
    kge = v.get("kg_siklik_ev", 0); kgd = v.get("kg_siklik_dep", 0)
    cse = v.get("clean_sheets_ev", 0); csd = v.get("clean_sheets_dep", 0)
    tse = v.get("team_scored_ev", 0); tsd = v.get("team_scored_dep", 0)
    b1 = ort_iki(v.get("btts_1h_ev", 0), v.get("btts_1h_dep", 0))
    b2 = ort_iki(v.get("btts_2h_ev", 0), v.get("btts_2h_dep", 0))
    y = []
    if kg >= esik_al("kg_var"):
        y.append(f"🤝 **KG VAR NEDEN POZİTİF? (%{kg:.1f})**")
        if kge > 0: y.append(f"- Ev KG Var: **%{kge:.1f}**")
        if kgd > 0: y.append(f"- Dep KG Var: **%{kgd:.1f}**")
        y.append(f"- Ev gol beklentisi: **{le:.2f}**")
        y.append(f"- Dep gol beklentisi: **{ld:.2f}**")
        if b1 > 0: y.append(f"- İY KG: **%{b1:.0f}**")
        if b2 > 0: y.append(f"- 2Y KG: **%{b2:.0f}**")
        if tse >= 70: y.append(f"- ✅ Ev gol atmaya yatkın: **%{tse:.0f}**")
        if tsd >= 70: y.append(f"- ✅ Dep gol atmaya yatkın: **%{tsd:.0f}**")
    elif kgy >= esik_al("kg_yok"):
        y.append(f"🤝 **KG YOK NEDEN POZİTİF? (%{kgy:.1f})**")
        if kge > 0: y.append(f"- Ev KG Var: **%{kge:.1f}** (düşük)")
        if kgd > 0: y.append(f"- Dep KG Var: **%{kgd:.1f}** (düşük)")
        if cse > 0: y.append(f"- Ev clean sheet: **%{cse:.0f}**")
        if csd > 0: y.append(f"- Dep clean sheet: **%{csd:.0f}**")
    return y


def birx_detayli(v, a):
    p1, px, p2 = a["p1"], a["px"], a["p2"]
    en = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    sec, yuzde = en; es = esik_1x2_al(sec)
    isim = {"1": "Ev Kazanır (1)", "X": "Beraberlik (X)", "2": "Dep Kazanır (2)"}[sec]
    se = v.get("siralama_ev", 0); sd = v.get("siralama_dep", 0)
    ae = v.get("atilan_ev", 0); ad = v.get("atilan_dep", 0)
    ye = v.get("yenen_ev", 0); yd = v.get("yenen_dep", 0)
    ppg = v.get("ppg_ev", 0); mpg = v.get("mpg_dep", 0)
    ge = v.get("galibiyet_ev", 0); gd = v.get("galibiyet_dep", 0)
    be = v.get("beraberlik_ev", 0); bd = v.get("beraberlik_dep", 0)
    y = [f"🎯 **1X2 NEDEN {sec}? (Ev %{p1:.1f} • X %{px:.1f} • Dep %{p2:.1f})**"]
    if ppg > 0 and mpg > 0:
        f = ppg - mpg
        if f >= 0.5: y.append(f"- ✅ **Form:** Ev {ppg:.2f} vs Dep {mpg:.2f} → Ev önde")
        elif f <= -0.5: y.append(f"- ✅ **Form:** Dep {mpg:.2f} vs Ev {ppg:.2f} → Dep önde")
    if se > 0 and sd > 0:
        fs = sd - se
        if fs >= 5: y.append(f"- ✅ **Sıralama:** Ev **{se}.** vs Dep **{sd}.** → Ev {fs} basamak önde")
        elif fs <= -5: y.append(f"- ✅ **Sıralama:** Dep **{sd}.** vs Ev **{se}.** → Dep {abs(fs)} basamak önde")
    if ge > 0 or gd > 0: y.append(f"- Galibiyet: Ev **%{ge:.0f}** • Dep **%{gd:.0f}**")
    if be > 0 or bd > 0: y.append(f"- Beraberlik: Ev **%{be:.0f}** • Dep **%{bd:.0f}**")
    if yuzde >= es: y.append(f"- **Sonuç:** {isim} (%{yuzde:.1f}) ≥ eşik %{es:.0f} → POZİTİF ✅")
    else: y.append(f"- **Sonuç:** {isim} (%{yuzde:.1f}) < eşik %{es:.0f} → EŞİK ALTI")
    return y


def okunan_veriler_paneli(v):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{v.get('takim_ev', 'Ev')}**")
        st.markdown(f"- Atılan: **{v.get('atilan_ev', 0):.2f}**")
        st.markdown(f"- Yenen: **{v.get('yenen_ev', 0):.2f}**")
        st.markdown(f"- CS: **{v.get('clean_sheets_ev', 0):.1f}%**")
        st.markdown(f"- TS: **{v.get('team_scored_ev', 0):.1f}%**")
        st.markdown(f"- KG Var: **{v.get('kg_siklik_ev', 0):.1f}%**")
        st.markdown(f"- Üst 2.5: **{v.get('ust25_ev', 0):.1f}%**")
    with c2:
        st.markdown(f"**{v.get('takim_dep', 'Dep')}**")
        st.markdown(f"- Atılan: **{v.get('atilan_dep', 0):.2f}**")
        st.markdown(f"- Yenen: **{v.get('yenen_dep', 0):.2f}**")
        st.markdown(f"- CS: **{v.get('clean_sheets_dep', 0):.1f}%**")
        st.markdown(f"- TS: **{v.get('team_scored_dep', 0):.1f}%**")
        st.markdown(f"- KG Var: **{v.get('kg_siklik_dep', 0):.1f}%**")
        st.markdown(f"- Üst 2.5: **{v.get('ust25_dep', 0):.1f}%**")
        # ============ TASARIM ============
def _e(x): return _html.escape(str(x))


def rozet(metin, tip="gray"):
    return f'<span class="fa-badge fa-b-{tip}">{_e(metin)}</span>'


def mac_karti(ev, dep, skor_belli, skor_ev, skor_dep, lam_ev, lam_dep, saat="", ulke="", tarih=""):
    orta = (f'<div class="fa-score">{int(skor_ev)} - {int(skor_dep)}</div>' if skor_belli
            else '<div class="fa-vs">VS</div>')
    bayrak = ulke_bayrak_bul(ulke)
    ust = ""
    if saat or ulke or tarih:
        p = []
        if bayrak != "🌍" or ulke: p.append(f"{bayrak} {_e((ulke or '').title())}")
        if tarih: p.append(f"📅 {_e(tarih)}")
        if saat: p.append(f"🕐 {_e(saat)}")
        if p: ust = f'<div class="fa-sub" style="margin-bottom:8px;">{" • ".join(p)}</div>'
    alt = f'<div class="fa-sub">Model beklenen gol: {lam_ev:.2f} - {lam_dep:.2f}</div>'
    return (f'<div class="fa-hero">{ust}<div class="fa-teams"><div class="fa-team">{_e(ev)}</div>'
            f'{orta}<div class="fa-team">{_e(dep)}</div></div>{alt}</div>')


def mac_tahmin_karti(vg, g=None):
    try:
        try: ya = yeniden_analiz(vg)
        except Exception: ya = (g or {}).get("analiz", {})
        p1 = ya.get("p1", 33.33); px = ya.get("px", 33.33); p2 = ya.get("p2", 33.34)
        u25 = ya.get("ust_25", 50); a25 = 100 - u25
        kg = ya.get("kg_var_model", 50); kgy = 100 - kg
        en = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        s1, y1 = en; e1 = esik_1x2_al(s1); poz1 = y1 >= e1
        isim1 = {"1": "1 — Ev Kazanır", "X": "X — Beraberlik", "2": "2 — Dep Kazanır"}[s1]
        if u25 >= a25: gs = "Üst 2.5"; gy = u25; ge = esik_al("ust")
        else: gs = "Alt 2.5"; gy = a25; ge = esik_al("alt")
        gp = gy >= ge
        if kg >= kgy: ks = "KG Var"; ky = kg; ke = esik_al("kg_var")
        else: ks = "KG Yok"; ky = kgy; ke = esik_al("kg_yok")
        kp = ky >= ke
        def r(p): return "pass" if p else "off"
        def b(p): return "ok" if p else "no"
        def bt(p): return "✓" if p else "○"
        return f'''<div class="fa-mk">
            <div class="fa-mk-row"><span class="fa-mk-lbl">1X2</span><span class="fa-mk-pick {r(poz1)}">{_e(isim1)}</span><span class="fa-mk-pct">%{y1:.0f} <span class="fa-mk-badge {b(poz1)}">{bt(poz1)} eşik %{e1:.0f}</span></span></div>
            <div class="fa-mk-row"><span class="fa-mk-lbl">Gol</span><span class="fa-mk-pick {r(gp)}">{_e(gs)}</span><span class="fa-mk-pct">%{gy:.0f} <span class="fa-mk-badge {b(gp)}">{bt(gp)} eşik %{ge:.0f}</span></span></div>
            <div class="fa-mk-row"><span class="fa-mk-lbl">KG</span><span class="fa-mk-pick {r(kp)}">{_e(ks)}</span><span class="fa-mk-pct">%{ky:.0f} <span class="fa-mk-badge {b(kp)}">{bt(kp)} eşik %{ke:.0f}</span></span></div>
        </div>'''
    except Exception: return ""


def obar(et, yuzde, esik=None, renk="#3b82f6"):
    y = max(0.0, min(100.0, yuzde)); isaret = ""
    if esik is not None:
        renk = "#22c55e" if yuzde >= esik else "#475569"
        isaret = f'<div class="fa-tick" style="left:{esik:.0f}%"></div>'
    return (f'<div class="fa-row"><div class="fa-row-top"><span class="fa-lbl">{_e(et)}</span>'
            f'<span class="fa-val">%{yuzde:.1f}</span></div>'
            f'<div class="fa-bar"><div class="fa-fill" style="width:{y:.1f}%;background:{renk}"></div>{isaret}</div></div>')


def olasilik_paneli(a):
    s = ('<div class="fa-ttl">Maç Sonucu</div>'
         + obar("Ev Sahibi (1)", a["p1"], esik_1x2_al("1"), "#3b82f6")
         + obar("Beraberlik (X)", a["px"], esik_1x2_al("X"), "#94a3b8")
         + obar("Deplasman (2)", a["p2"], esik_1x2_al("2"), "#f59e0b")
         + '<div class="fa-ttl" style="margin-top:12px">Piyasalar</div>'
         + obar("Üst 2.5", a["ust_25"], esik_al("ust"))
         + obar("Alt 2.5", a["alt_25"], esik_al("alt"))
         + obar("KG Var", a["kg_var_model"], esik_al("kg_var"))
         + obar("KG Yok", a["kg_yok_model"], esik_al("kg_yok")))
    return f'<div class="fa-card">{s}</div>'


def oneri_karti(baslik, secim, yuzde, esik, poz, alt):
    if poz:
        sv, em, _k, et = guven_seviyesi_bul(yuzde)
        tip = "green" if sv == "yuksek" else "yellow" if sv == "orta" else "gray"
        durum = rozet(f"{et} güven", tip); sn = "fa-card fa-pos"; ps = "fa-pct"
        ns = f'<div class="fa-mut">{_e(alt)}</div>'
    else:
        durum = rozet("Eşik altı", "gray"); sn = "fa-card fa-neg"; ps = "fa-pct fa-off"
        ns = f'<div class="fa-mut">{_e(alt)} • Gerekli: %{esik:.0f}</div>'
    bar = obar("", yuzde, esik)
    return (f'<div class="{sn}"><div class="fa-ttl">{_e(baslik)}</div>'
            f'<div class="fa-pickrow"><div><div class="fa-pick">{_e(secim)}</div>{durum}</div>'
            f'<div class="{ps}">%{yuzde:.1f}</div></div>{bar}{ns}</div>')


def istat_karti(baslik, ist, esik_m):
    t = ist["tam"]; y = ist["yakin"]; yl = ist["yanlis"]; tp = t + y + yl
    if tp == 0: govde = '<div class="fa-big fa-off">—</div><div class="fa-mut">Henüz bahis yok</div>'
    else:
        isb = (t + y) / tp * 100
        sf = "fa-g" if isb >= 85 else "fa-y" if isb >= 70 else "fa-r"
        govde = (f'<div class="fa-big {sf}">%{isb:.0f}</div>'
                 f'<div class="fa-mut">✓ {t+y} • ✗ {yl} • {tp} bahis</div>')
    return (f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>{govde}'
            f'<div class="fa-mut">{_e(esik_m)}</div></div>')


def backtest_karti(baslik, dogru, yanlis):
    tp = dogru + yanlis
    if tp == 0: return (f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>'
                        f'<div class="fa-mut">Eşiği geçen maç yok.</div></div>')
    yuzde = dogru / tp * 100
    als, us = wilson_aralik(dogru, tp)
    sf = "fa-g" if yuzde >= 85 else "fa-y" if yuzde >= 70 else "fa-r"
    rk = "#22c55e" if yuzde >= 85 else "#f59e0b" if yuzde >= 70 else "#ef4444"
    return (f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>'
            f'<div class="fa-pickrow"><div class="fa-big {sf}">%{yuzde:.1f}</div>'
            f'<div style="text-align:right"><div class="fa-val">✓ {dogru} &nbsp; ✗ {yanlis}</div>'
            f'<div class="fa-mut">{tp} bahis</div></div></div>'
            f'<div class="fa-ci"><div class="fa-ci-fill" style="left:{als:.1f}%;width:{max(us-als,0.5):.1f}%"></div>'
            f'<div class="fa-ci-dot" style="left:{yuzde:.1f}%;background:{rk}"></div></div>'
            f'<div class="fa-mut">%95 güven: %{als:.0f} – %{us:.0f}</div></div>')


def mac_sonuc_ikon(g):
    try:
        v = g["veri"]
        if not v.get("skor_belli", False): return "⚫"
        try: ya = yeniden_analiz(v)
        except Exception: ya = g.get("analiz", {})
        d = sonuc_hesapla({"veri": v, "analiz": ya})
        if not d: return "⚫"
        vr = [x for x in [d["oneri_1x2"]["tuttu"], d["oneri_gol"]["tuttu"], d["oneri_kg"]["tuttu"]] if x is not None]
        if not vr: return "⚫"
        if all(vr): return "✅"
        if not any(vr): return "❌"
        return "🟡"
    except Exception: return "⚫"


def nav_git(h):
    st.session_state.sayfa = h
    st.session_state.kayit_yapildi = False
    st.session_state.gecmisten_gelindi = False
    st.session_state.gelecekten_gelindi = False
    st.session_state.aktif_kayit_idx = None
    st.session_state.aktif_gelecek_idx = None
    st.session_state.okunamayan_alanlar = []
    st.session_state.manuel_bekleyen = []
    st.session_state.tek_silme_onay = None
    st.session_state.tek_silme_gelecek = None
    st.session_state.silme_onay = False
    if h == "backtest":
        st.session_state.bt_sonuc = None
        st.session_state.bt_detaylar = []
    st.rerun()


def nav_bar():
    if st.session_state.sayfa == "giris": return
    try: kutu = st.container(key="fa_nav")
    except TypeError: kutu = st.container()
    with kutu:
        if admin_mi():
            sec = [("🏠", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek"),
                   ("🔬 Test", "backtest"), ("⚙️ Ayar", "ayarlar")]
        else:
            sec = [("🏠 Ana", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek")]
        kol = st.columns(len(sec))
        for k, (e, h) in zip(kol, sec):
            with k:
                ak = st.session_state.sayfa == h
                if st.button(e, key=f"nav_{h}", use_container_width=True,
                             type="primary" if ak else "secondary"):
                    if not ak: nav_git(h)


def giris_ekrani():
    st.markdown('<div class="login-hero"><div class="login-logo">⚽</div><h1 class="login-title">Futbol Analiz Pro</h1><p class="login-subtitle">Akilli mac analizi ve tahmin motoru</p></div>', unsafe_allow_html=True)
    with st.form("giris_form"):
        sifre = st.text_input("Admin Sifresi", type="password", key="sifre_input", placeholder="Sifreni gir...")
        a_btn = st.form_submit_button("Admin Girisi", use_container_width=True, type="primary")
        st.markdown('<div class="login-divider">VEYA</div>', unsafe_allow_html=True)
        m_btn = st.form_submit_button("Misafir Olarak Devam Et", use_container_width=True)
        if a_btn:
            if sifre == ADMIN_SIFRE:
                st.session_state.giris_yapildi = True; st.session_state.rol = "admin"
                st.session_state.sayfa = "giris"; st.rerun()
            else: st.error("Yanlis sifre.")
        if m_btn:
            st.session_state.giris_yapildi = True; st.session_state.rol = "misafir"
            st.session_state.sayfa = "giris"; st.rerun()
    st.markdown('<div class="login-features"><span class="lf-chip">1X2</span><span class="lf-chip">Ust/Alt 2.5</span><span class="lf-chip">KG Var/Yok</span><span class="lf-chip">Backtest</span></div><div class="login-footer">Futbol Analiz Pro • Bilgi amaclidir</div>', unsafe_allow_html=True)


def ust_bar():
    c1, c2 = st.columns([3, 1])
    with c1:
        if admin_mi(): st.markdown("Admin Modu")
        else: st.markdown("Misafir Modu")
    with c2:
        if st.button("Cikis", use_container_width=True, key="cikis_btn"):
            st.session_state.giris_yapildi = False; st.session_state.rol = None
            st.session_state.sayfa = "giris"; st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
            st.session_state.tek_silme_onay = None; st.session_state.tek_silme_gelecek = None
            st.session_state.silme_onay = False; st.session_state.aktif_kayit_idx = None
            st.session_state.aktif_gelecek_idx = None; st.session_state.bt_sonuc = None
            st.session_state.bt_detaylar = []; st.rerun()


def misafir_aciklama():
    with st.expander("Uygulamayi Tani ve Kurallari Oku", expanded=False):
        st.markdown(
            "### Futbol Analiz Pro\n"
            "Futbol maclarinin gecmis istatistiklerini analiz ederek 1X2, Ust/Alt 2.5 ve KG tahminleri uretir.\n\n"
            "### ESIKLER\n"
            "- 1X2 -> %55+ - Ust -> %82 - Alt -> %74 - KG Var -> %73 - KG Yok -> %88\n\n"
            "### 1X2\n"
            "1 = Ev - X = Beraberlik - 2 = Dep\n\n"
            "### STRATEJI\n"
            "- TEKLI: Dusuk risk - 2'LI: Isabet %72 - 3'LU: Isabet %61\n\n"
            "### KURALLAR\n"
            "1. Kaybetmeyi kabul et 2. Bankani koru 3. Martingale yapma\n"
            "4. Sadece onerilere oyna 5. Limit koy 6. Ara ver\n"
            "7. Kazanci cek 8. Alkol/sinirde oynama\n\n"
            "### SORUMLULUK\n"
            "18 yas alti yasak. Yesilay: 115\n\n"
            "Bol sans!"
        )


# ============ UYGULAMA BASLANGIC ============
if not st.session_state.giris_yapildi:
    giris_ekrani(); st.stop()

ust_bar()
nav_bar()


# ============ ANA SAYFA ============
if st.session_state.sayfa == "giris":
    if admin_mi():
        st.markdown("<h1>Futbol Analiz Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>URL ile otomatik cek veya metni elle yapistir.</p>", unsafe_allow_html=True)
        mod = st.radio("Veri giris yontemi",
                       ["URL ile Otomatik Cek", "Metin Yapistir"],
                       horizontal=True, key="veri_mod", label_visibility="collapsed")
        cikan = None; ok = []
        if mod.startswith("URL"):
            st.caption("Cloudscraper aktif.")
            url_input = st.text_input("Mac URL'i",
                                      placeholder="https://www.soccerstats.com/... veya sportytrader.com/...",
                                      key="url_input", label_visibility="collapsed")
            if st.button("URL'DEN CEK ve ANALIZ ET", use_container_width=True, type="primary"):
                if not url_input.strip():
                    st.warning("Once URL yapistir.")
                else:
                    with st.spinner("Sayfa cekiliyor..."):
                        cikan, ok, hata = url_den_veri_cek(url_input)
                    if hata:
                        st.error(hata); st.info("Metin Yapistir modunu deneyin.")
                        cikan = None
                    else:
                        st.success("URL'den veri cekildi!")
                        if ok: st.warning(f"{len(ok)} alan eksik: {', '.join(ok)}")
        else:
            st.caption("Mac istatistiklerini kopyala, buraya yapistir.")
            ym = st.text_area("Yapistirma alani", height=280, key="yapistir_input",
                              label_visibility="collapsed", placeholder="Istatistik metnini buraya yapistir.")
            if st.button("ANALIZ ET", use_container_width=True, type="primary"):
                if not ym.strip():
                    st.warning("Once metni yapistir.")
                else:
                    cikan, ok = metinden_veri_cikar(ym)

        if cikan:
            yv = copy.deepcopy(VARSAYILAN_VERI); yv.update(cikan)
            st.session_state.form_verileri = yv
            st.session_state.kayit_yapildi = False
            st.session_state.gecmisten_gelindi = False
            st.session_state.gelecekten_gelindi = False
            st.session_state.aktif_kayit_idx = None
            st.session_state.aktif_gelecek_idx = None
            st.session_state.okunamayan_alanlar = ok
            st.session_state.manuel_bekleyen = ok.copy()
            if not veri_yeterli_mi(yv):
                st.error("Analiz icin yeterli veri yok.")
            else:
                if ok: st.session_state.sayfa = "manuel_giris"
                else: st.session_state.sayfa = "sonuc"
                st.rerun()

        st.divider()
        c2, c3, c4, c5 = st.columns(4)
        with c2:
            if st.button("Gecmis", use_container_width=True, key="a_g"): nav_git("gecmis")
        with c3:
            if st.button("Gelecek", use_container_width=True, key="a_ge"): nav_git("gelecek")
        with c4:
            if st.button("Backtest", use_container_width=True, key="a_b"): nav_git("backtest")
        with c5:
            if st.button("Ayarlar", use_container_width=True, key="a_a"): nav_git("ayarlar")
    else:
        gs = len(st.session_state.gecmis_analizler)
        gls = len(st.session_state.gelecek_analizler)
        st.markdown(f'''
            <div class="mh-hero">
                <div class="mh-hero-icon">⚽</div>
                <div class="mh-hero-title">Futbol Analiz Pro</div>
                <div class="mh-hero-sub">Akilli mac analizi ve tahmin motoru</div>
                <div class="mh-hero-badge">CANLI VERI</div>
            </div>
            <div class="mh-stat-grid">
                <div class="mh-stat"><div class="mh-stat-icon">📊</div>
                    <div class="mh-stat-num">{gs}</div>
                    <div class="mh-stat-lbl">Gecmis Mac</div></div>
                <div class="mh-stat"><div class="mh-stat-icon">🔮</div>
                    <div class="mh-stat-num">{gls}</div>
                    <div class="mh-stat-lbl">Gelecek Mac</div></div>
            </div>
            <div class="mh-section-title">HIZLI ERISIM</div>
        ''', unsafe_allow_html=True)
        try: kutu = st.container(key="fa_misafir_nav")
        except TypeError: kutu = st.container()
        with kutu:
            cb1, cb2 = st.columns(2)
            with cb1:
                gb = st.button("Gecmis Maclar", use_container_width=True, type="primary", key="m_g")
            with cb2:
                glb = st.button("Gelecek Maclar", use_container_width=True, type="primary", key="m_gl")
        if gb:
            st.session_state.sayfa = "gecmis"; st.session_state.kayit_yapildi = False
            st.session_state.aktif_kayit_idx = None; st.session_state.aktif_gelecek_idx = None
            st.session_state.tek_silme_onay = None; st.rerun()
        if glb:
            st.session_state.sayfa = "gelecek"; st.session_state.kayit_yapildi = False
            st.session_state.aktif_kayit_idx = None; st.session_state.aktif_gelecek_idx = None
            st.session_state.tek_silme_gelecek = None; st.rerun()
        st.markdown('<div class="mh-info">Ipucu: Gecmis maclarda isabet oranlarini incele, gelecek maclarda yuksek guvenli tahminleri filtrele.</div><div class="mh-section-title" style="margin-top:20px;">BILGILENDIRME</div>', unsafe_allow_html=True)
        misafir_aciklama()
        st.markdown('<div class="login-footer" style="margin-top:24px;">Futbol Analiz Pro</div>', unsafe_allow_html=True)


# ============ MANUEL GIRIS ============
elif st.session_state.sayfa == "manuel_giris":
    st.markdown("<h1>Eksik Alanlari Doldur</h1>", unsafe_allow_html=True)
    st.warning(f"Asagidaki {len(st.session_state.manuel_bekleyen)} alan cikarilamadi:")
    v = st.session_state.form_verileri
    with st.form("manuel_form"):
        yd = {}
        for ab in st.session_state.manuel_bekleyen:
            if ab in MANUEL_ALANLAR:
                st.markdown(f"**{ab}**")
                for (key, et, tip, vs) in MANUEL_ALANLAR[ab]:
                    mv = v.get(key, vs)
                    if tip == "int":
                        val = st.number_input(et, value=int(mv) if mv else int(vs), min_value=1, max_value=100, step=1, key=f"m_{key}")
                        yd[key] = int(val)
                    elif tip == "float":
                        val = st.number_input(et, value=float(mv) if mv else float(vs), min_value=0.0, step=0.1, key=f"m_{key}")
                        yd[key] = float(val)
                    else:
                        val = st.text_input(et, value=str(mv) if mv else "", key=f"m_{key}")
                        yd[key] = val
                st.markdown("")
        ca, cb = st.columns(2)
        with ca:
            kyd = st.form_submit_button("Kaydet ve Analiz Et", use_container_width=True, type="primary")
        with cb:
            atl = st.form_submit_button("Atla", use_container_width=True)
        if kyd or atl:
            if kyd: st.session_state.form_verileri.update(yd)
            st.session_state.manuel_bekleyen = []
            st.session_state.sayfa = "sonuc"; st.rerun()
    if st.button("Geri"):
        st.session_state.sayfa = "giris"; st.rerun()


# ============ GECMIS ============
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>Gecmis Maclar</h1>", unsafe_allow_html=True)
    gc = st.session_state.gecmis_analizler; tp = len(gc)
    with st.spinner("Hesaplaniyor..."):
        oi = oneri_istatistik_guncel(gc)
    if tp == 0: st.info("Henuz kayitli mac yok.")
    else:
        st.markdown("### ONERI ISTATISTIKLERI")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(istat_karti("1X2", oi["1x2"],
                                    f"1 %{esik_1x2_al('1'):.0f} • X %{esik_1x2_al('X'):.0f} • 2 %{esik_1x2_al('2'):.0f}"), unsafe_allow_html=True)
        with c2:
            st.markdown(istat_karti("Ust/Alt", oi["gol"],
                                    f"Ust %{esik_al('ust'):.0f} • Alt %{esik_al('alt'):.0f}"), unsafe_allow_html=True)
        with c3:
            st.markdown(istat_karti("KG", oi["kg"],
                                    f"Var %{esik_al('kg_var'):.0f} • Yok %{esik_al('kg_yok'):.0f}"), unsafe_allow_html=True)
    st.divider()
    st.markdown(f"### Maclar ({tp})")
    if tp > 0:
        for i, g in enumerate(reversed(gc)):
            ig = len(gc) - 1 - i
            vg = g["veri"]
            te = vg.get("takim_ev", "Ev") or "Ev"
            td = vg.get("takim_dep", "Dep") or "Dep"
            se = vg.get("skor_ev", 0); sd = vg.get("skor_dep", 0)
            ik = mac_sonuc_ikon(g)
            st.markdown(f"### {ik}", unsafe_allow_html=False)
            st.markdown(mac_karti(te, td, True, se, sd, 0, 0,
                                  saat=vg.get("saat", ""), ulke=vg.get("ulke", ""), tarih=vg.get("tarih", "")),
                        unsafe_allow_html=True)
            th = mac_tahmin_karti(vg, g)
            if th: st.markdown(th, unsafe_allow_html=True)
            if admin_mi():
                cd, csil = st.columns([5, 1])
                with cd:
                    if st.button("Detay", use_container_width=True, key=f"mac_{ig}"):
                        st.session_state.form_verileri = copy.deepcopy(vg)
                        st.session_state.kayit_yapildi = True
                        st.session_state.gecmisten_gelindi = True
                        st.session_state.gelecekten_gelindi = False
                        st.session_state.aktif_kayit_idx = ig
                        st.session_state.aktif_gelecek_idx = None
                        st.session_state.okunamayan_alanlar = []
                        st.session_state.sayfa = "sonuc"; st.rerun()
                with csil:
                    if st.button("Sil", key=f"sil_{ig}"):
                        st.session_state.tek_silme_onay = None if st.session_state.tek_silme_onay == ig else ig
                        st.rerun()
                if st.session_state.tek_silme_onay == ig:
                    st.warning(f"{te} vs {td} silinsin mi?")
                    ce, ch = st.columns(2)
                    with ce:
                        if st.button("Evet Sil", key=f"ev_{ig}", use_container_width=True, type="primary"):
                            if 0 <= ig < len(st.session_state.gecmis_analizler):
                                st.session_state.gecmis_analizler.pop(ig)
                                gecmis_kaydet(st.session_state.gecmis_analizler)
                            st.session_state.tek_silme_onay = None; st.rerun()
                    with ch:
                        if st.button("Iptal", key=f"hy_{ig}", use_container_width=True):
                            st.session_state.tek_silme_onay = None; st.rerun()
            else:
                if st.button("Detay", use_container_width=True, key=f"mac_{ig}"):
                    st.session_state.form_verileri = copy.deepcopy(vg)
                    st.session_state.kayit_yapildi = True
                    st.session_state.gecmisten_gelindi = True
                    st.session_state.gelecekten_gelindi = False
                    st.session_state.aktif_kayit_idx = ig
                    st.session_state.aktif_gelecek_idx = None
                    st.session_state.okunamayan_alanlar = []
                    st.session_state.sayfa = "sonuc"; st.rerun()
            st.divider()
    if admin_mi():
        st.markdown("### Yedekleme")
        c1, c2 = st.columns(2)
        with c1:
            js = json.dumps(st.session_state.gecmis_analizler, ensure_ascii=False, indent=2)
            st.download_button(label=f"Indir ({tp})", data=js,
                               file_name=f"gecmis_{tp}mac.json", mime="application/json",
                               use_container_width=True, key="ind_g")
        with c2:
            yk = st.file_uploader("Yukle", type=["json"], key="yk_g")
            if yk is not None:
                try:
                    v = json.loads(yk.read().decode("utf-8"))
                    if isinstance(v, list):
                        st.session_state.gecmis_analizler = v; gecmis_kaydet(v)
                        st.success(f"{len(v)} mac yuklendi!"); st.rerun()
                except Exception as e: st.error(str(e))
    st.divider()
    if admin_mi():
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Tumunu Temizle", use_container_width=True, key="tmz"):
                st.session_state.silme_onay = True; st.rerun()
        with c2:
            if st.button("Ana Sayfa", use_container_width=True, type="primary", key="gg"):
                st.session_state.sayfa = "giris"; st.session_state.silme_onay = False
                st.session_state.tek_silme_onay = None; st.rerun()
        if st.session_state.silme_onay:
            st.warning("Tum gecmis silinecek. Emin misin?")
            ce, ch = st.columns(2)
            with ce:
                if st.button("Evet", key="she", use_container_width=True, type="primary"):
                    st.session_state.gecmis_analizler = []
                    try:
                        if os.path.exists(GECMIS_DOSYA): os.remove(GECMIS_DOSYA)
                    except Exception: pass
                    st.session_state.silme_onay = False; st.rerun()
            with ch:
                if st.button("Iptal", key="shi", use_container_width=True):
                    st.session_state.silme_onay = False; st.rerun()
    else:
        if st.button("Ana Sayfa", use_container_width=True, type="primary", key="ggm"):
            st.session_state.sayfa = "giris"; st.session_state.tek_silme_onay = None; st.rerun()


# ============ GELECEK ============
elif st.session_state.sayfa == "gelecek":
    st.markdown("<h1>Gelecek Maclar</h1>", unsafe_allow_html=True)
    gl = st.session_state.gelecek_analizler; tpg = len(gl)
    if not gl: st.info("Gelecek mac yok.")
    else:
        for i, g in enumerate(reversed(gl)):
            ig = len(gl) - 1 - i
            vg = g["veri"]
            te = vg.get("takim_ev", "Ev") or "Ev"
            td = vg.get("takim_dep", "Dep") or "Dep"
            try:
                af = analiz_hesapla(vg)
                leh = af["lam_ev"]; ldh = af["lam_dep"]
            except Exception: leh = ldh = 0
            st.markdown(mac_karti(te, td, False, 0, 0, leh, ldh,
                                  saat=vg.get("saat", ""), ulke=vg.get("ulke", ""), tarih=vg.get("tarih", "")),
                        unsafe_allow_html=True)
            th = mac_tahmin_karti(vg, g)
            if th: st.markdown(th, unsafe_allow_html=True)
            if admin_mi():
                cd, csil = st.columns([5, 1])
                with cd:
                    if st.button("Detay", use_container_width=True, key=f"gmac_{ig}"):
                        st.session_state.form_verileri = copy.deepcopy(vg)
                        st.session_state.kayit_yapildi = True
                        st.session_state.gecmisten_gelindi = False
                        st.session_state.gelecekten_gelindi = True
                        st.session_state.aktif_kayit_idx = None
                        st.session_state.aktif_gelecek_idx = ig
                        st.session_state.okunamayan_alanlar = []
                        st.session_state.sayfa = "sonuc"; st.rerun()
                with csil:
                    if st.button("Sil", key=f"gsil_{ig}"):
                        st.session_state.tek_silme_gelecek = None if st.session_state.tek_silme_gelecek == ig else ig
                        st.rerun()
                if st.session_state.tek_silme_gelecek == ig:
                    st.warning(f"{te} vs {td} silinsin mi?")
                    ce, ch = st.columns(2)
                    with ce:
                        if st.button("Evet Sil", key=f"evg_{ig}", use_container_width=True, type="primary"):
                            if 0 <= ig < len(st.session_state.gelecek_analizler):
                                st.session_state.gelecek_analizler.pop(ig)
                                gelecek_kaydet(st.session_state.gelecek_analizler)
                            st.session_state.tek_silme_gelecek = None; st.rerun()
                    with ch:
                        if st.button("Iptal", key=f"hyg_{ig}", use_container_width=True):
                            st.session_state.tek_silme_gelecek = None; st.rerun()
            else:
                if st.button("Detay", use_container_width=True, key=f"gmac_{ig}"):
                    st.session_state.form_verileri = copy.deepcopy(vg)
                    st.session_state.kayit_yapildi = True
                    st.session_state.gecmisten_gelindi = False
                    st.session_state.gelecekten_gelindi = True
                    st.session_state.aktif_kayit_idx = None
                    st.session_state.aktif_gelecek_idx = ig
                    st.session_state.okunamayan_alanlar = []
                    st.session_state.sayfa = "sonuc"; st.rerun()
            st.divider()
    if admin_mi():
        st.markdown("### Yedekleme")
        c1, c2 = st.columns(2)
        with c1:
            js = json.dumps(st.session_state.gelecek_analizler, ensure_ascii=False, indent=2)
            st.download_button(label=f"Indir ({tpg})", data=js,
                               file_name=f"gelecek_{tpg}mac.json", mime="application/json",
                               use_container_width=True, key="ind_gl")
        with c2:
            yk = st.file_uploader("Yukle", type=["json"], key="yk_gl")
            if yk is not None:
                try:
                    v = json.loads(yk.read().decode("utf-8"))
                    if isinstance(v, list):
                        st.session_state.gelecek_analizler = v; gelecek_kaydet(v)
                        st.success(f"{len(v)} mac yuklendi!"); st.rerun()
                except Exception as e: st.error(str(e))
        st.divider()
    if st.button("Ana Sayfa", use_container_width=True, type="primary", key="g_geri"):
        st.session_state.sayfa = "giris"; st.session_state.tek_silme_gelecek = None; st.rerun()


# ============ BACKTEST ============
elif st.session_state.sayfa == "backtest":
    if not admin_mi():
        st.error("Sadece admin.")
        if st.button("Ana Sayfa", use_container_width=True, type="primary"):
            st.session_state.sayfa = "giris"; st.rerun()
        st.stop()
    st.markdown("<h1>Backtest</h1>", unsafe_allow_html=True)
    st.caption("Test etmek istedigin marketleri sec.")
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Mac Sonucu**")
        s1 = st.checkbox("1X2", value=st.session_state.bt_market.get("1x2", False), key="bt_1x2")
        e1 = st.slider("1 esigi %", 0, 100, int(st.session_state.bt_market_esik.get("esik_1", 55.0)), 1, key="sl_1", disabled=not s1)
        ex = st.slider("X esigi %", 0, 100, int(st.session_state.bt_market_esik.get("esik_x", 55.0)), 1, key="sl_x", disabled=not s1)
        e2 = st.slider("2 esigi %", 0, 100, int(st.session_state.bt_market_esik.get("esik_2", 55.0)), 1, key="sl_2", disabled=not s1)
    with c2:
        st.markdown("**KG**")
        skv = st.checkbox("KG Var", value=st.session_state.bt_market["kg_var"], key="bt_kv")
        ekv = st.slider("KG Var %", 0, 100, int(st.session_state.bt_market_esik["kg_var"]), 1, key="sl_kv", disabled=not skv)
        sky = st.checkbox("KG Yok", value=st.session_state.bt_market["kg_yok"], key="bt_ky")
        eky = st.slider("KG Yok %", 0, 100, int(st.session_state.bt_market_esik["kg_yok"]), 1, key="sl_ky", disabled=not sky)
    with c3:
        st.markdown("**Gol**")
        su = st.checkbox("Ust 2.5", value=st.session_state.bt_market["ust"], key="bt_u")
        eu = st.slider("Ust %", 0, 100, int(st.session_state.bt_market_esik["ust"]), 1, key="sl_u", disabled=not su)
        sa = st.checkbox("Alt 2.5", value=st.session_state.bt_market["alt"], key="bt_a")
        ea = st.slider("Alt %", 0, 100, int(st.session_state.bt_market_esik["alt"]), 1, key="sl_a", disabled=not sa)
    sec = {"1x2": s1, "kg_var": skv, "kg_yok": sky, "ust": su, "alt": sa}
    esik = {"esik_1": float(e1), "esik_x": float(ex), "esik_2": float(e2),
            "kg_var": float(ekv), "kg_yok": float(eky),
            "ust": float(eu), "alt": float(ea)}
    st.divider()
    st.markdown("### Mac Araligi")
    tg = st.session_state.gecmis_analizler; tpm = len(tg)
    mod = st.radio("Hangi maclarda?", ["Tumu", "Ayar seti (ilk N)", "Test seti (N'den sonra)"], key="bt_mod")
    bl = tpm // 2
    if mod != "Tümü" and tpm >= 4:
        bl = st.slider("N", 1, tpm - 1, max(1, tpm // 2), 1, key="bt_bl")
    if mod == "Tumu" or tpm < 4:
        sg = tg; me = f"Tumu ({tpm} mac)"
    elif mod.startswith("Ayar"):
        sg = tg[:bl]; me = f"Ayar: ilk {bl}"
    else:
        sg = tg[bl:]; me = f"Test: {bl + 1}+"
    st.divider()
    if st.button("TEST ET", use_container_width=True, type="primary"):
        if not any(sec.values()): st.warning("En az bir market sec.")
        else:
            with st.spinner("Test ediliyor..."):
                st.session_state.bt_mod_etiket = me
                sonuc, det = backtest_hesapla(sg, sec, esik)
                st.session_state.bt_sonuc = sonuc; st.session_state.bt_detaylar = det
                st.session_state.bt_market = sec; st.session_state.bt_market_esik = esik
    if st.session_state.bt_sonuc:
        sc = st.session_state.bt_sonuc
        st.divider(); st.markdown("## SONUC")
        st.caption(f"{st.session_state.get('bt_mod_etiket', '')}")
        for key, b in [("1x2", "1X2"), ("kg_var", "KG Var"), ("kg_yok", "KG Yok"),
                       ("ust", "Ust 2.5"), ("alt", "Alt 2.5")]:
            if sec[key]:
                d = sc[key]
                st.markdown(backtest_karti(b, d["dogru"], d["yanlis"]), unsafe_allow_html=True)
        with st.expander(f"Detaylar ({len(st.session_state.bt_detaylar)} mac)"):
            for m in st.session_state.bt_detaylar:
                st.markdown(f"**{m['takim_ev']} {m['skor']} {m['takim_dep']}**")
                for dd in m["detaylar"]: st.markdown(f" - {dd}")
                st.markdown("")
    st.divider()
    if st.button("Ana Sayfa", use_container_width=True, type="primary", key="bt_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


# ============ AYARLAR ============
elif st.session_state.sayfa == "ayarlar":
    if not admin_mi():
        st.error("Sadece admin."); st.stop()
    st.markdown("<h1>Esik Ayarlari</h1>", unsafe_allow_html=True)
    mv = st.session_state.esikler.copy()
    st.markdown("### 1X2")
    ca, cb, cc = st.columns(3)
    with ca: ye1 = st.slider("1 (Ev) %", 0, 100, int(mv.get("esik_1", 55.0)), 1, key="ay_1")
    with cb: yex = st.slider("X (Ber.) %", 0, 100, int(mv.get("esik_x", 55.0)), 1, key="ay_x")
    with cc: ye2 = st.slider("2 (Dep) %", 0, 100, int(mv.get("esik_2", 55.0)), 1, key="ay_2")
    st.markdown("### Gol")
    c1, c2 = st.columns(2)
    with c1: yu = st.slider("Ust 2.5 %", 0, 100, int(mv["ust"]), 1, key="ay_u")
    with c2: ya = st.slider("Alt 2.5 %", 0, 100, int(mv["alt"]), 1, key="ay_a")
    st.markdown("### KG")
    c3, c4 = st.columns(2)
    with c3: ykv = st.slider("KG Var %", 0, 100, int(mv["kg_var"]), 1, key="ay_kv")
    with c4: yky = st.slider("KG Yok %", 0, 100, int(mv["kg_yok"]), 1, key="ay_ky")
    st.divider()
    ck, cs, cg = st.columns(3)
    with ck:
        if st.button("Kaydet", use_container_width=True, type="primary"):
            ye = {"esik_1": float(ye1), "esik_x": float(yex), "esik_2": float(ye2),
                  "ust": float(yu), "alt": float(ya),
                  "kg_var": float(ykv), "kg_yok": float(yky)}
            st.session_state.esikler = ye; ayarlar_kaydet(ye); st.success("Kaydedildi!")
    with cs:
        if st.button("Sifirla", use_container_width=True):
            v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0,
                 "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0}
            st.session_state.esikler = v; ayarlar_kaydet(v); st.rerun()
    with cg:
        if st.button("Ana Sayfa", use_container_width=True, key="ay_g"):
            st.session_state.sayfa = "giris"; st.rerun()
    st.divider()
    st.info(f"Aktif esikler: 1X2 1:%{st.session_state.esikler.get('esik_1',55):.0f} X:%{st.session_state.esikler.get('esik_x',55):.0f} 2:%{st.session_state.esikler.get('esik_2',55):.0f} • Ust:%{st.session_state.esikler['ust']:.0f} Alt:%{st.session_state.esikler['alt']:.0f} • KG Var:%{st.session_state.esikler['kg_var']:.0f} Yok:%{st.session_state.esikler['kg_yok']:.0f}")


# ============ SONUC ============
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)
    u25 = a["ust_25"]; a25 = a["alt_25"]
    kgm = a["kg_var_model"]; kgym = a["kg_yok_model"]
    te = v.get("takim_ev", "") or "Ev Sahibi"
    td = v.get("takim_dep", "") or "Deplasman"
    sb = v.get("skor_belli", False)
    se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    st.markdown(mac_karti(te, td, sb, se, sd, a["lam_ev"], a["lam_dep"],
                          saat=v.get("saat", ""), ulke=v.get("ulke", ""), tarih=v.get("tarih", "")),
                unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)
    with st.expander("Okunan Veriler", expanded=False):
        okunan_veriler_paneli(v)
    if sb:
        d = sonuc_hesapla({"veri": v, "analiz": a})
        with st.expander("Dogruluk", expanded=True):
            c1, c2, c3 = st.columns(3)
            for col, key, lbl in zip([c1, c2, c3], ["oneri_1x2", "oneri_gol", "oneri_kg"], ["1X2", "Gol", "KG"]):
                o = d[key]
                with col:
                    if o["tuttu"] is None: st.markdown(f"**{lbl}**"); st.markdown("Oneri yok")
                    else:
                        st.markdown(rozet(f"{lbl}", "green" if o["tuttu"] else "red"), unsafe_allow_html=True)
                        st.markdown(f"{o['tahmin']}")
    else: d = None
    with st.expander("Genis Analiz", expanded=True):
        for b, m in detayli_analiz_yorumu(v):
            st.markdown(f"**{b}**"); st.markdown(m); st.markdown("")
        for fn in [birx_detayli, gol_detayli, kg_detayli]:
            y = fn(v, a)
            if y:
                st.markdown("---")
                for s in y:
                    if s.startswith(("🎯", "🤝")): st.markdown(f"### {s}")
                    else: st.markdown(s)
    st.divider()
    st.markdown("## FINAL ONERI")
    en1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    s1, y1 = en1; e1s = esik_1x2_al(s1); p1p = y1 >= e1s
    im = {"1": "1 (Ev)", "X": "X (Ber.)", "2": "2 (Dep)"}
    st.markdown(oneri_karti("1X2", im[s1], y1, e1s, p1p,
                            f"1: %{a['p1']:.1f} - X: %{a['px']:.1f} - 2: %{a['p2']:.1f}"), unsafe_allow_html=True)
    if u25 >= a25: gsec, gy, ge = "Ust 2.5", u25, esik_al("ust")
    else: gsec, gy, ge = "Alt 2.5", a25, esik_al("alt")
    gp = gy >= ge
    st.markdown(oneri_karti("Gol", gsec, gy, ge, gp,
                            f"Ust %{u25:.1f} - Alt %{a25:.1f}"), unsafe_allow_html=True)
    if kgm >= kgym: ksec, ky, ke = "KG Var", kgm, esik_al("kg_var")
    else: ksec, ky, ke = "KG Yok", kgym, esik_al("kg_yok")
    kp = ky >= ke
    st.markdown(oneri_karti("KG", ksec, ky, ke, kp,
                            f"Var %{kgm:.1f} - Yok %{kgym:.1f}"), unsafe_allow_html=True)
    if st.session_state.gelecekten_gelindi and admin_mi():
        ig = st.session_state.aktif_gelecek_idx
        if ig is not None and 0 <= ig < len(st.session_state.gelecek_analizler):
            st.divider()
            st.markdown("### Sonucu Gir ve Tasi")
            sc1, sc2, sc3 = st.columns([1, 1, 1])
            with sc1: yse = st.number_input("Ev Gol", min_value=0, max_value=20, value=int(v.get("skor_ev", 0)), step=1, key=f"gs_{ig}")
            with sc2: ysd = st.number_input("Dep Gol", min_value=0, max_value=20, value=int(v.get("skor_dep", 0)), step=1, key=f"gd_{ig}")
            with sc3:
                st.markdown(""); st.markdown("")
                if st.button("Tasi", key=f"ts_{ig}", use_container_width=True, type="primary"):
                    ky_ = st.session_state.gelecek_analizler[ig]
                    ky_["veri"]["skor_ev"] = int(yse); ky_["veri"]["skor_dep"] = int(ysd)
                    ky_["veri"]["skor_belli"] = True
                    yd_ = sonuc_hesapla(ky_)
                    if yd_: ky_["dogruluk"] = yd_
                    st.session_state.gecmis_analizler.append(ky_)
                    st.session_state.gelecek_analizler.pop(ig)
                    gecmis_kaydet(st.session_state.gecmis_analizler); gelecek_kaydet(st.session_state.gelecek_analizler)
                    st.session_state.gelecekten_gelindi = False; st.session_state.aktif_gelecek_idx = None
                    st.session_state.sayfa = "gelecek"; st.rerun()
    km = gp or kp or p1p
    if not st.session_state.kayit_yapildi and admin_mi():
        yk = kayit_olustur(v, a)
        if d is not None: yk["dogruluk"] = d
        if sb:
            st.session_state.gecmis_analizler.append(yk)
            gecmis_kaydet(st.session_state.gecmis_analizler)
            if km: st.success("Gecmise kaydedildi.")
            else: st.info("Gecmise kaydedildi. (oneri yok)")
        else:
            if km:
                st.session_state.gelecek_analizler.append(yk)
                gelecek_kaydet(st.session_state.gelecek_analizler)
                st.info("Gelecege kaydedildi.")
            else: st.warning("Hicbir market pozitif degil.")
        st.session_state.kayit_yapildi = True
    st.divider()
    if st.button("Yeni Mac Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.sayfa = "giris"; st.rerun()
