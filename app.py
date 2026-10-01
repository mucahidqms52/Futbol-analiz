import streamlit as st
import math
import copy
import re
import random
import json
import os
import html as _html
import asyncio

# ===== OTOMATİK VERİ ÇEKME =====
try:
    import requests
    import cloudscraper
    from bs4 import BeautifulSoup
    HTTP_OK = True
except ImportError:
    HTTP_OK = False

# ===== LIVESCORE MCP =====
try:
    from mcp import ClientSession
    from mcp.client.sse import sse_client
    import nest_asyncio
    nest_asyncio.apply()
    MCP_OK = True
except ImportError:
    MCP_OK = False

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

st.markdown("""
<style>
    .block-container { padding-top: 2rem !important; padding-bottom: 0.5rem !important;
        padding-left: 0.7rem !important; padding-right: 0.7rem !important; max-width: 100% !important; }
    h1 { font-size: 1.2rem !important; margin: 0.2rem 0 !important; text-align: center; }
    h2 { font-size: 1rem !important; margin: 0.3rem 0 !important; }
    h3 { font-size: 0.9rem !important; margin: 0.15rem 0 !important; }
    p { font-size: 0.85rem !important; margin: 0.2rem 0 !important; }
    hr { margin: 0.3rem 0 !important; }
    div[data-testid="stNumberInput"] label p { font-size: 0.75rem !important; margin: 0 !important; }
    div[data-testid="stNumberInput"] input { font-size: 0.85rem !important; padding: 0.15rem 0.3rem !important; height: 1.8rem !important; }
    div[data-testid="stNumberInput"] button { height: 1.8rem !important; padding: 0 !important; width: 1.5rem !important; }
    .stButton button { padding: 0.4rem 0.6rem !important; font-size: 0.9rem !important; height: 2.2rem !important; }
    div[data-testid="stAlert"] { padding: 0.3rem 0.5rem !important; font-size: 0.85rem !important; }
    textarea { font-size: 0.75rem !important; }
    div[data-testid="stExpander"] summary { font-size: 0.9rem !important; padding: 0.4rem !important; }
    .stApp { background: #0b1220 !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp div[data-testid="stMarkdownContainer"] { color: #e6edf7 !important; }
    .stApp div[data-testid="stCaptionContainer"], .stApp div[data-testid="stCaptionContainer"] *, .stApp small { color: #8fa0bd !important; }
    hr { border-color: #23304a !important; }
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
    div[data-testid="stAlert"] { border-radius: 12px !important; }
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
        box-shadow: 0 12px 48px rgba(0,0,0,0.45), 0 0 0 1px rgba(34,197,94,0.04) inset !important; backdrop-filter: blur(12px); }
    div[data-testid="stForm"] label p { font-size: 0.8rem !important; font-weight: 700 !important; color: #cbd5e1 !important; letter-spacing: 0.4px; margin-bottom: 4px !important; }
    div[data-testid="stForm"] input { height: 46px !important; font-size: 0.95rem !important; padding: 0 14px !important;
        background: rgba(11,18,32,0.85) !important; border: 1.5px solid #23304a !important; border-radius: 12px !important; }
    div[data-testid="stForm"] input:focus { border-color: #22c55e !important; box-shadow: 0 0 0 3px rgba(34,197,94,0.18) !important; }
    div[data-testid="stForm"] button { height: 46px !important; font-size: 0.95rem !important; font-weight: 700 !important; border-radius: 12px !important; }
    div[data-testid="stForm"] button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; box-shadow: 0 6px 20px rgba(34,197,94,0.3) !important; border: none !important; }
    div[data-testid="stForm"] button[kind="secondary"] { background: rgba(30,41,59,0.55) !important; border: 1.5px solid #23304a !important; }
    .login-divider { display: flex; align-items: center; gap: 12px; margin: 10px 0 6px 0; color: #64748b !important; font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; justify-content: center; }
    .login-divider::before, .login-divider::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, transparent, #23304a 50%, transparent); }
    .login-features { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 22px; padding: 0 10px; }
    .lf-chip { display: inline-block; padding: 6px 14px; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.25); border-radius: 99px; font-size: 0.75rem; font-weight: 600; color: #cbd5e1 !important; letter-spacing: 0.3px; }
    .login-footer { text-align: center; margin-top: 26px; font-size: 0.72rem; color: #64748b !important; letter-spacing: 0.5px; }
    .login-footer b { color: #22c55e !important; font-weight: 700; }
    .mh-hero { position: relative; overflow: hidden; text-align: center; padding: 30px 14px 22px 14px;
        background: linear-gradient(135deg, rgba(22,35,61,0.85), rgba(15,26,46,0.9));
        border: 1px solid rgba(34,197,94,0.22); border-radius: 22px; margin: 6px 0 16px 0;
        box-shadow: 0 12px 40px rgba(0,0,0,0.35), 0 0 0 1px rgba(34,197,94,0.05) inset; }
    .mh-hero::before { content: ""; position: absolute; top: -60%; left: -60%; width: 220%; height: 220%;
        background: radial-gradient(circle at 50% 50%, rgba(34,197,94,0.15), transparent 55%);
        animation: mhGlow 5s ease-in-out infinite; pointer-events: none; }
    @keyframes mhGlow { 0%, 100% { opacity: 0.5; transform: scale(1) rotate(0deg); }
        50% { opacity: 1; transform: scale(1.15) rotate(20deg); } }
    .mh-hero-icon { font-size: 3.2rem; line-height: 1; margin-bottom: 10px; display: inline-block;
        filter: drop-shadow(0 0 20px rgba(34,197,94,0.55)); animation: logoPulse 3s ease-in-out infinite; position: relative; z-index: 1; }
    .mh-hero-title { font-size: 1.7rem; font-weight: 900;
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; letter-spacing: 1px; position: relative; z-index: 1; margin: 0; }
    .mh-hero-sub { font-size: 0.84rem; color: #8fa0bd; margin-top: 8px; letter-spacing: 0.4px; position: relative; z-index: 1; }
    .mh-hero-badge { display: inline-block; margin-top: 12px; padding: 4px 14px;
        background: rgba(34,197,94,0.12); border: 1px solid rgba(34,197,94,0.4); border-radius: 99px;
        font-size: 0.72rem; font-weight: 700; color: #22c55e !important; letter-spacing: 0.6px; position: relative; z-index: 1; }
    .mh-stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 0 0 16px 0; }
    .mh-stat { position: relative; background: linear-gradient(145deg, #16233d, #0f1a2e);
        border: 1px solid #23304a; border-radius: 16px; padding: 14px 8px 12px 8px; text-align: center; overflow: hidden; }
    .mh-stat::after { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #22c55e, #3b82f6); }
    .mh-stat-icon { font-size: 1.3rem; margin-bottom: 2px; }
    .mh-stat-num { font-size: 1.85rem; font-weight: 900; color: #22c55e !important; line-height: 1; letter-spacing: -1px; }
    .mh-stat-lbl { font-size: 0.68rem; color: #8fa0bd !important; margin-top: 5px; letter-spacing: 0.6px; text-transform: uppercase; font-weight: 700; }
    .mh-section-title { font-size: 0.78rem; color: #8fa0bd !important; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700;
        margin: 4px 0 8px 4px; text-align: left; border-left: 3px solid #22c55e; padding-left: 8px; }
    .st-key-fa_misafir_nav .stButton button { height: 72px !important; font-size: 1rem !important; font-weight: 800 !important;
        border-radius: 16px !important; letter-spacing: 0.4px; box-shadow: 0 8px 24px rgba(34,197,94,0.25) !important; }
    .st-key-fa_misafir_nav .stButton button p { font-size: 1rem !important; font-weight: 800 !important; }
    .mh-info { background: linear-gradient(145deg, rgba(19,28,46,0.6), rgba(11,18,32,0.8));
        border: 1px solid #23304a; border-radius: 14px; padding: 12px 14px; margin-top: 14px;
        font-size: 0.76rem; color: #8fa0bd !important; line-height: 1.6; }
    .mh-info b { color: #22c55e !important; }
    /* MCP canlı skor kartları */
    .mcp-match { background: linear-gradient(145deg, #16233d, #0f1a2e); border: 1px solid #23304a;
        border-radius: 14px; padding: 10px 12px; margin-bottom: 8px; }
    .mcp-match .mcp-lig { font-size: 0.68rem; color: #8fa0bd !important; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
    .mcp-match .mcp-teams { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
    .mcp-match .mcp-team { flex: 1; font-size: 0.9rem; font-weight: 700; }
    .mcp-match .mcp-team.away { text-align: right; }
    .mcp-match .mcp-score { font-size: 1.3rem; font-weight: 900; color: #22c55e !important; min-width: 60px; text-align: center; }
    .mcp-match .mcp-minute { font-size: 0.7rem; color: #f59e0b !important; margin-top: 4px; text-align: center; font-weight: 700; }
    .mcp-match .mcp-status { font-size: 0.68rem; color: #8fa0bd !important; text-align: center; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DOSYALAR
# ==========================================
GECMIS_DOSYA = "gecmis.json"
GELECEK_DOSYA = "gelecek.json"
AYARLAR_DOSYA = "ayarlar.json"
ADMIN_SIFRE = "Mg153759"
LIVESCORE_MCP_URL = "https://livescoremcp.com/sse"

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
                yuklenen = json.load(f)
                if "1x2" in yuklenen and "esik_1" not in yuklenen:
                    eski = float(yuklenen["1x2"])
                    yuklenen["esik_1"] = eski; yuklenen["esik_x"] = eski; yuklenen["esik_2"] = eski
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
if "goster_yardim" not in st.session_state: st.session_state.goster_yardim = False
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

# MCP durumu
if "mcp_canli_skorlar" not in st.session_state: st.session_state.mcp_canli_skorlar = None
if "mcp_yukleniyor" not in st.session_state: st.session_state.mcp_yukleniyor = False

def admin_mi(): return st.session_state.get("rol") == "admin"

def esik_al(key): return st.session_state.esikler.get(key, 50.0)

def esik_1x2_al(secim):
    key_map = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}
    return st.session_state.esikler.get(key_map.get(secim, ""), 55.0)

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

def wilson_aralik(dogru, toplam, z=1.96):
    if toplam <= 0: return 0.0, 0.0
    p = dogru / toplam
    payda = 1 + z * z / toplam
    merkez = (p + z * z / (2 * toplam)) / payda
    yari = z * math.sqrt(p * (1 - p) / toplam + z * z / (4 * toplam * toplam)) / payda
    return max(0.0, (merkez - yari) * 100), min(100.0, (merkez + yari) * 100)

def _form_ppg(s):
    return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1)

def yeniden_analiz(v):
    v2 = copy.deepcopy(v)
    if v2.get("form_str_ev"): v2["ppg_ev"] = _form_ppg(v2["form_str_ev"])
    if v2.get("form_str_dep"): v2["mpg_dep"] = _form_ppg(v2["form_str_dep"])
    anahtar = json.dumps(v2, sort_keys=True, ensure_ascii=False)
    if "bt_analiz_cache" not in st.session_state: st.session_state.bt_analiz_cache = {}
    cache = st.session_state.bt_analiz_cache
    if anahtar not in cache:
        a = analiz_hesapla(v2)
        cache[anahtar] = {"ust_25": a["ust_25"], "kg_var_model": a["kg_var_model"],
                          "p1": a["p1"], "px": a["px"], "p2": a["p2"]}
    return cache[anahtar]

def backtest_hesapla(gecmis, market_sec, market_esik):
    sonuc = {"1x2": {"dogru": 0, "yanlis": 0}, "kg_var": {"dogru": 0, "yanlis": 0},
             "kg_yok": {"dogru": 0, "yanlis": 0}, "ust": {"dogru": 0, "yanlis": 0},
             "alt": {"dogru": 0, "yanlis": 0}}
    mac_detaylari = []
    for g in gecmis:
        try:
            v = g["veri"]; analiz = g.get("analiz", {})
            if not v.get("skor_belli", False): continue
            skor_ev = int(v.get("skor_ev", 0)); skor_dep = int(v.get("skor_dep", 0))
            toplam_gol = skor_ev + skor_dep
            gercek_kg_var = (skor_ev > 0 and skor_dep > 0)
            gercek_ust = toplam_gol > 2.5
            if skor_ev > skor_dep: gercek_1x2 = "1"
            elif skor_ev == skor_dep: gercek_1x2 = "X"
            else: gercek_1x2 = "2"
            try:
                yeni_analiz = yeniden_analiz(v)
                ust_25 = yeni_analiz["ust_25"]; kg_var = yeni_analiz["kg_var_model"]
                p1_y = yeni_analiz["p1"]; px_y = yeni_analiz["px"]; p2_y = yeni_analiz["p2"]
            except Exception:
                ust_25 = analiz.get("ust_25", 50); kg_var = analiz.get("kg_var_model", 50)
                p1_y = analiz.get("p1", 33.33); px_y = analiz.get("px", 33.33); p2_y = analiz.get("p2", 33.34)
            alt_25 = 100 - ust_25; kg_yok = 100 - kg_var
            mac_kayit = {"takim_ev": v.get("takim_ev", "Ev"), "takim_dep": v.get("takim_dep", "Dep"),
                         "skor": f"{skor_ev}-{skor_dep}",
                         "gercek_kg": "Var" if gercek_kg_var else "Yok",
                         "gercek_gol": "Üst" if gercek_ust else "Alt",
                         "gercek_1x2": gercek_1x2, "detaylar": []}
            if market_sec.get("1x2", False):
                en_yuksek = max([("1", p1_y), ("X", px_y), ("2", p2_y)], key=lambda x: x[1])
                secim, yuzde = en_yuksek
                esik_key = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}[secim]
                esik_secim = market_esik.get(esik_key, 55.0)
                if yuzde >= esik_secim:
                    if secim == gercek_1x2:
                        sonuc["1x2"]["dogru"] += 1; mac_kayit["detaylar"].append(f"1X2: {secim} ✅")
                    else:
                        sonuc["1x2"]["yanlis"] += 1; mac_kayit["detaylar"].append(f"1X2: {secim} ❌ (gerçek: {gercek_1x2})")
            if market_sec.get("kg_var", False):
                if kg_var >= market_esik["kg_var"] and kg_var >= kg_yok:
                    if gercek_kg_var: sonuc["kg_var"]["dogru"] += 1; mac_kayit["detaylar"].append("KG Var ✅")
                    else: sonuc["kg_var"]["yanlis"] += 1; mac_kayit["detaylar"].append("KG Var ❌")
            if market_sec.get("kg_yok", False):
                if kg_yok >= market_esik["kg_yok"] and kg_yok >= kg_var:
                    if not gercek_kg_var: sonuc["kg_yok"]["dogru"] += 1; mac_kayit["detaylar"].append("KG Yok ✅")
                    else: sonuc["kg_yok"]["yanlis"] += 1; mac_kayit["detaylar"].append("KG Yok ❌")
            if market_sec.get("ust", False):
                if ust_25 >= market_esik["ust"] and ust_25 >= alt_25:
                    if gercek_ust: sonuc["ust"]["dogru"] += 1; mac_kayit["detaylar"].append("Üst ✅")
                    else: sonuc["ust"]["yanlis"] += 1; mac_kayit["detaylar"].append("Üst ❌")
            if market_sec.get("alt", False):
                if alt_25 >= market_esik["alt"] and alt_25 >= ust_25:
                    if not gercek_ust: sonuc["alt"]["dogru"] += 1; mac_kayit["detaylar"].append("Alt ✅")
                    else: sonuc["alt"]["yanlis"] += 1; mac_kayit["detaylar"].append("Alt ❌")
            if mac_kayit["detaylar"]: mac_detaylari.append(mac_kayit)
        except Exception:
            continue
    return sonuc, mac_detaylari

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
    pattern = r'([\d.,]+)%?\s*\t\s*' + re.escape(etiket) + r'\s*\t\s*([\d.,]+)%?'
    m = re.search(pattern, blok, re.IGNORECASE)
    if m:
        try: return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError: pass
    pattern2 = r'([\d.,]+)%?\s{1,4}' + re.escape(etiket) + r'\s{1,4}([\d.,]+)%?'
    m = re.search(pattern2, blok, re.IGNORECASE)
    if m:
        try: return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError: pass
    return None, None

def _sira_bul(metin, takim_adi):
    if not takim_adi: return None, None
    pattern = (r'(?:^|\n)\s*(\d{1,2})\s*\r?\n\s*' + re.escape(takim_adi) + r'\s*\r?\n\s*'
               + re.escape(takim_adi) + r'\s*\r?\n' r'\s*(\d+)\s*\t')
    m = re.search(pattern, metin, re.MULTILINE)
    if m:
        try:
            sira = int(m.group(1))
            if 1 <= sira <= 30:
                devam = metin[m.end()-1:]
                m_puan = re.match(r'[\s\S]{0,80}?\r?\n\s*(\d{1,2})\s*\r?\n', devam)
                puan = int(m_puan.group(1)) if m_puan else 0
                return sira, puan
        except (ValueError, AttributeError): pass
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
    else: veri["skor_belli"] = False
    takim_ev = veri.get("takim_ev", ""); takim_dep = veri.get("takim_dep", "")
    idx = metin.find("Main Stats")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for etiket, key1, key2 in [("Goals scored per game", "atilan_ev", "atilan_dep"),
                                    ("Goals conceded per game", "yenen_ev", "yenen_dep"),
                                    ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"),
                                    ("Team scored", "team_scored_ev", "team_scored_dep"),
                                    ("Team scored twice", "team_scored_2_ev", "team_scored_2_dep"),
                                    ("Scored in both halves", "scored_both_halves_ev", "scored_both_halves_dep"),
                                    ("Goal in both halves", "goal_both_halves_ev", "goal_both_halves_dep")]:
            v1, v2 = _cift_tab(etiket, blok)
            if v1 is not None: veri[key1] = v1; veri[key2] = v2
    idx = metin.find("Win Draw Lose")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for etiket, key1, key2 in [("Win and Over 1.5 goals", "win_over15_ev", "win_over15_dep"),
                                    ("Lose and Over 1.5 goals", "lose_over15_ev", "lose_over15_dep"),
                                    ("Team win first half", "win_1h_ev", "win_1h_dep"),
                                    ("Team draw at half time", "draw_ht_ev", "draw_ht_dep"),
                                    ("Team lost first half", "lose_1h_ev", "lose_1h_dep")]:
            v1, v2 = _cift_tab(etiket, blok)
            if v1 is not None: veri[key1] = v1; veri[key2] = v2
        for etiket, key_ev, key_dep in [("Win", "galibiyet_ev", "galibiyet_dep"),
                                         ("Draw", "beraberlik_ev", "beraberlik_dep"),
                                         ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
            pattern = r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*' + etiket + r'\s*\t\s*([\d.,]+)%'
            mm = re.search(pattern, blok, re.MULTILINE)
            if mm:
                try:
                    veri[key_ev] = float(mm.group(1).replace(",", "."))
                    veri[key_dep] = float(mm.group(2).replace(",", "."))
                except ValueError: pass
    idx = metin.find("Both Teams to Score")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for etiket, key1, key2 in [("BTTS in first-half", "btts_1h_ev", "btts_1h_dep"),
                                    ("BBTS in second-half", "btts_2h_ev", "btts_2h_dep"),
                                    ("BBTS and Over 1.5", "btts_over15_ev", "btts_over15_dep"),
                                    ("BBTS and Over 2.5", "btts_over25_ev", "btts_over25_dep"),
                                    ("Win and BTTS", "win_btts_ev", "win_btts_dep"),
                                    ("Draw and BTTS", "draw_btts_ev", "draw_btts_dep"),
                                    ("Lose and BTTS", "lose_btts_ev", "lose_btts_dep")]:
            v1, v2 = _cift_tab(etiket, blok)
            if v1 is not None: veri[key1] = v1; veri[key2] = v2
        m = re.search(r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*Both Teams to Score\s*\t\s*([\d.,]+)%', blok, re.MULTILINE)
        if m:
            try:
                veri["kg_siklik_ev"] = float(m.group(1).replace(",", "."))
                veri["kg_siklik_dep"] = float(m.group(2).replace(",", "."))
            except ValueError: pass
    idx = metin.find("Match Total Goals")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for etiket, key1, key2 in [("Match total goals 0 or 1", "tg_01_ev", "tg_01_dep"),
                                    ("Match total goals 2 or 3", "tg_23_ev", "tg_23_dep"),
                                    ("Match total goals 4+", "tg_4p_ev", "tg_4p_dep"),
                                    ("Match total goals 0", "tg_0_ev", "tg_0_dep"),
                                    ("Match total goals 1", "tg_1_ev", "tg_1_dep"),
                                    ("Match total goals 2", "tg_2_ev", "tg_2_dep"),
                                    ("Match total goals 3", "tg_3_ev", "tg_3_dep")]:
            v1, v2 = _cift_tab(etiket, blok)
            if v1 is not None: veri[key1] = v1; veri[key2] = v2
        if veri.get("tg_4_ev", 0) == 0 and veri.get("tg_4p_ev", 0) > 0:
            veri["tg_4_ev"] = veri["tg_4p_ev"]; veri["tg_4_dep"] = veri["tg_4p_dep"]
    idx = metin.find("Over Under Goals")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for etiket, key1, key2 in [("Over 0.5 goals at half-time", "ht_ust05_ev", "ht_ust05_dep"),
                                    ("Over 1.5 goals at half-time", "ht_ust15_ev", "ht_ust15_dep"),
                                    ("Over 2.5 goals at half-time", "ht_ust25_ev", "ht_ust25_dep"),
                                    ("Over 0.5 goals", "ust05_ev", "ust05_dep"),
                                    ("Over 1.5 goals", "ust15_ev", "ust15_dep"),
                                    ("Over 2.5 goals", "ust25_ev", "ust25_dep"),
                                    ("Over 3.5 goals", "ust35_ev", "ust35_dep")]:
            v1, v2 = _cift_tab(etiket, blok)
            if v1 is not None: veri[key1] = v1; veri[key2] = v2
    idx = metin.find("Half Time-Full Time")
    if idx != -1:
        blok = metin[idx:idx+2000]
        for etiket, key in [("Win HT - Win FT", "wht_wft"), ("Win HT - Draw FT", "wht_dft"),
                            ("Win HT - Lose FT", "wht_lft"), ("Draw HT - Win FT", "dht_wft"),
                            ("Draw HT - Draw FT", "dht_dft"), ("Draw HT - Lose FT", "dht_lft"),
                            ("Lose HT - Win FT", "lht_wft"), ("Lose HT - Draw FT", "lht_dft"),
                            ("Lose HT - Lose FT", "lht_lft")]:
            v1, v2 = _cift_tab(etiket, blok)
            if v1 is not None: veri[key + "_ev"] = v1; veri[key + "_dep"] = v2
    if takim_ev:
        s, p = _sira_bul(metin, takim_ev)
        if s is not None: veri["siralama_ev"] = s
    if takim_dep:
        s, p = _sira_bul(metin, takim_dep)
        if s is not None: veri["siralama_dep"] = s
    if veri.get("siralama_ev", 0) == 0: okunamayanlar.append("Sıralama (Ev)")
    if veri.get("siralama_dep", 0) == 0: okunamayanlar.append("Sıralama (Dep)")
    m = re.search(r'\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\nForm\s*\t?\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])', metin)
    if m:
        form_ev = m.group(1) + m.group(2) + m.group(3) + m.group(4) + m.group(5)
        form_dep = m.group(6) + m.group(7) + m.group(8) + m.group(9) + m.group(10)
        veri["form_str_ev"] = form_ev; veri["form_str_dep"] = form_dep
        def _form_puan(s): return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1)
        veri["ppg_ev"] = _form_puan(form_ev); veri["mpg_dep"] = _form_puan(form_dep)
    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) +
                                  veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2
    veri["format"] = "sportytrader"
    return veri, okunamayanlar

def _sf(s):
    if s is None: return None
    try:
        s2 = str(s).strip().replace(",", ".").replace("%", "")
        return float(s2)
    except (ValueError, AttributeError): return None

def _etiket_esle(etiket):
    e = etiket.lower().strip()
    mapping = [
        (("goals scored", "scored per game", "avg goals for", "goals for"), ("atilan_ev", "atilan_dep")),
        (("goals conceded", "conceded per game", "avg goals against", "goals against"), ("yenen_ev", "yenen_dep")),
        (("clean sheet",), ("clean_sheets_ev", "clean_sheets_dep")),
        (("failed to score",), ("_fail_ev", "_fail_dep")),
        (("scored in", "team scored", "scored at least one"), ("team_scored_ev", "team_scored_dep")),
        (("over 2.5", "over 2,5"), ("ust25_ev", "ust25_dep")),
        (("over 1.5", "over 1,5"), ("ust15_ev", "ust15_dep")),
        (("over 3.5", "over 3,5"), ("ust35_ev", "ust35_dep")),
        (("both teams", "btts", "btts%"), ("kg_siklik_ev", "kg_siklik_dep")),
    ]
    for keywords, keys in mapping:
        for kw in keywords:
            if kw in e: return keys
    return None

def soccerstats_metin_cikar(metin):
    veri = {}
    satirlar = metin.split("\n")
    for i, s in enumerate(satirlar[:30]):
        m = re.search(r'([A-ZÀ-Ý][a-zA-ZÀ-ÿ\s\.\']+?)\s+(?:vs?\.?|v|VS?)\s+([A-ZÀ-Ý][a-zA-ZÀ-ÿ\s\.\']+)', s)
        if m:
            veri["takim_ev"] = m.group(1).strip(); veri["takim_dep"] = m.group(2).strip()
            break
    for i, satir in enumerate(satirlar):
        s = satir.strip()
        if len(s) < 5 or len(s) > 200: continue
        sayilar = re.findall(r'\d+[\.,]?\d*%?', s)
        sayilar = [_sf(x) for x in sayilar]
        sayilar = [x for x in sayilar if x is not None]
        if len(sayilar) < 2: continue
        keys = _etiket_esle(s)
        if keys:
            k1, k2 = keys
            if k1.startswith("_fail"):
                veri["team_scored_ev"] = 100 - sayilar[0]
                veri["team_scored_dep"] = 100 - sayilar[1] if len(sayilar) > 1 else 100 - sayilar[0]
            else:
                veri[k1] = sayilar[0]
                veri[k2] = sayilar[1] if len(sayilar) > 1 else sayilar[0]
    veri["format"] = "soccerstats"
    veri["skor_belli"] = False
    return veri, []

def metinden_veri_cikar(metin):
    metin = metin.replace(",", ".")
    if "Main Stats" in metin and "Goals scored per game" in metin:
        veri, okunamayanlar = sportytrader_veri_cikar(metin)
        if not veri.get("takim_ev"): okunamayanlar.append("Takım isimleri (Ev)")
        if not veri.get("takim_dep"): okunamayanlar.append("Takım isimleri (Dep)")
        return veri, okunamayanlar
    if "Goals" in metin and ("Scored" in metin or "Conceded" in metin):
        return soccerstats_metin_cikar(metin)
    veri = {}; okunamayanlar = []
    veri["format"] = "genel"
    return veri, okunamayanlar

def html_metne_cevir(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "head", "meta", "link"]):
        tag.decompose()
    for table in soup.find_all("table"):
        satirlar = []
        for tr in table.find_all("tr"):
            hucreler = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            if hucreler: satirlar.append("\t".join(hucreler))
        if satirlar: table.replace_with("\n" + "\n".join(satirlar) + "\n")
    metin = soup.get_text(separator="\n")
    satirlar = [s.strip() for s in metin.split("\n")]
    satirlar = [s for s in satirlar if s]
    return "\n".join(satirlar)

def _scraper_olustur():
    try:
        return cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "mobile": False})
    except Exception:
        try: return cloudscraper.create_scraper()
        except Exception: return None

def soccerstats_veri_cikar(url):
    if not HTTP_OK:
        return None, [], "❌ 'requests', 'cloudscraper' veya 'beautifulsoup4' kurulu değil."
    try:
        headers = {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
            "Referer": "https://www.soccerstats.com/",
        }
        scraper = _scraper_olustur()
        if scraper is None: return None, [], "❌ Cloudscraper başlatılamadı."
        r = scraper.get(url, headers=headers, timeout=25, allow_redirects=True)
        if r.status_code != 200:
            return None, [], f"❌ HTTP {r.status_code} — Sayfaya erişilemedi."
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg"]): tag.decompose()
        veri = {}
        title = soup.find("title")
        if title:
            t = title.get_text()
            m = re.search(r'([A-Za-zÀ-ÿ\s\.\'\-]+?)\s+(?:vs?\.?|v)\s+([A-Za-zÀ-ÿ\s\.\'\-]+?)(?:\s*[-|]|\s+Football|\s*$)', t, re.IGNORECASE)
            if m:
                veri["takim_ev"] = m.group(1).strip(); veri["takim_dep"] = m.group(2).strip()
        if "league=" in url:
            m = re.search(r'league=([a-z0-9_]+)', url, re.IGNORECASE)
            if m: veri["ulke"] = m.group(1).replace("_", " ").title()
        tum_metin_parcalari = []; eslesme_sayisi = 0
        for table in soup.find_all("table"):
            metin = table.get_text(separator=" ", strip=True)
            if not any(k in metin.lower() for k in ["scored", "conceded", "clean sheet", "btts", "both teams", "over 1.5", "over 2.5"]):
                continue
            for tr in table.find_all("tr"):
                hucreler = tr.find_all(["td", "th"])
                if len(hucreler) < 3: continue
                hucre_metinleri = [h.get_text(strip=True) for h in hucreler]
                hucre_metinleri = [h for h in hucre_metinleri if h]
                if len(hucre_metinleri) < 3: continue
                etiket = hucre_metinleri[0]
                sayilar = []
                for h in hucre_metinleri[1:]:
                    f = _sf(h)
                    if f is not None: sayilar.append(f)
                if len(sayilar) < 2: continue
                keys = _etiket_esle(etiket)
                if keys:
                    k1, k2 = keys
                    veri[k1] = sayilar[0]
                    veri[k2] = sayilar[1] if len(sayilar) > 1 else sayilar[0]
                    eslesme_sayisi += 1
                tum_metin_parcalari.append("\t".join(hucre_metinleri))
        if veri.get("_fail_ev") is not None and not veri.get("team_scored_ev"):
            veri["team_scored_ev"] = 100 - veri["_fail_ev"]
        if veri.get("_fail_dep") is not None and not veri.get("team_scored_dep"):
            veri["team_scored_dep"] = 100 - veri["_fail_dep"]
        veri.pop("_fail_ev", None); veri.pop("_fail_dep", None)
        if not any(k in veri for k in ["atilan_ev", "yenen_ev", "ust25_ev", "kg_siklik_ev"]):
            full_text = soup.get_text(separator="\n")
            fallback, _ = soccerstats_metin_cikar(full_text)
            if fallback and any(k in fallback for k in ["atilan_ev", "yenen_ev"]):
                veri.update(fallback); eslesme_sayisi += 1
        if eslesme_sayisi == 0 and not any(k in veri for k in ["atilan_ev", "yenen_ev", "ust25_ev", "kg_siklik_ev"]):
            ornek = "\n".join(tum_metin_parcalari[:8]) if tum_metin_parcalari else "(tablo bulunamadı)"
            return None, [], ("⚠️ Soccerstats sayfası çekildi ama istatistikler tanınamadı.\n\n"
                             "**📝 Metin Yapıştır** modunu kullan.\n\n"
                             f"**Bulunan ilk satırlar:**\n```\n{ornek[:500]}\n```")
        veri["format"] = "soccerstats"; veri["skor_belli"] = False
        if veri.get("atilan_ev") and veri.get("yenen_ev"):
            veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) +
                                      veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
        if veri.get("ust25_ev") and veri.get("ust25_dep"):
            veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
        if veri.get("kg_siklik_ev") and veri.get("kg_siklik_dep"):
            veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2
        return veri, [], None
    except requests.exceptions.Timeout: return None, [], "❌ Zaman aşımı (25 sn)."
    except requests.exceptions.ConnectionError: return None, [], "❌ Bağlantı hatası."
    except Exception as e: return None, [], f"❌ Beklenmeyen hata: {str(e)[:200]}"

def sportytrader_url_cek(url):
    try:
        headers = {
            "User-Agent": ("Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        scraper = _scraper_olustur()
        if scraper is None: return None, [], "❌ Cloudscraper başlatılamadı."
        r = scraper.get(url, headers=headers, timeout=25, allow_redirects=True)
        if r.status_code != 200:
            return None, [], f"❌ HTTP {r.status_code} — Sportytrader erişilemedi."
        metin = html_metne_cevir(r.text)
        veri, okunamayanlar = metinden_veri_cikar(metin)
        if not veri or (not veri.get("takim_ev") and not veri.get("atilan_ev")):
            return None, [], ("⚠️ Sportytrader sayfası çekildi ama istatistikler yok. "
                             "Maç **stats** sayfasının URL'ini kullan veya 📝 Metin moduna geç.")
        return veri, okunamayanlar, None
    except Exception as e: return None, [], f"❌ {str(e)[:200]}"

def genel_url_cek(url):
    try:
        headers = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")}
        scraper = _scraper_olustur()
        if scraper is None: return None, [], "❌ Cloudscraper başlatılamadı."
        r = scraper.get(url, headers=headers, timeout=25, allow_redirects=True)
        if r.status_code != 200: return None, [], f"❌ HTTP {r.status_code}"
        metin = html_metne_cevir(r.text)
        veri, _ = soccerstats_metin_cikar(metin)
        if veri.get("atilan_ev") or veri.get("yenen_ev") or veri.get("ust25_ev"):
            return veri, [], None
        veri2, okunamayanlar = metinden_veri_cikar(metin)
        if veri2.get("atilan_ev") or veri2.get("takim_ev"):
            return veri2, okunamayanlar, None
        return None, [], ("⚠️ Parser bu sayfayı tanıyamadı. **📝 Metin Yapıştır** modunu kullan.\n\n"
                         f"**İlk 400 karakter:**\n```\n{metin[:400]}\n```")
    except Exception as e: return None, [], f"❌ {str(e)[:200]}"

def url_den_veri_cek(url):
    if not HTTP_OK:
        return None, [], ("❌ 'requests', 'cloudscraper' veya 'beautifulsoup4' kurulu değil.\n\n"
                          "**pip install requests beautifulsoup4 cloudscraper**")
    url = url.strip()
    if not url.startswith(("http://", "https://")): url = "https://" + url
    if "soccerstats.com" in url.lower(): return soccerstats_veri_cikar(url)
    elif "sportytrader.com" in url.lower(): return sportytrader_url_cek(url)
    else: return genel_url_cek(url)

# ==========================================
# LIVESCORE MCP İSTEMCİSİ
# ==========================================
async def _mcp_cagri(arac_adi, parametreler=None):
    """LiveScore MCP sunucusuna bağlanıp belirtilen aracı çağırır."""
    if parametreler is None: parametreler = {}
    try:
        async with sse_client(LIVESCORE_MCP_URL) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(arac_adi, parametreler)
                return {"basarili": True, "sonuc": result}
    except Exception as e:
        return {"basarili": False, "hata": str(e)[:300]}

def mcp_canli_skorlari_getir():
    """Canlı skorları çeker (senkron sarmalayıcı)."""
    if not MCP_OK:
        return {"basarili": False, "hata": "MCP kütüphanesi kurulu değil. requirements.txt'ye 'mcp' ve 'nest_asyncio' ekleyin."}
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            sonuc = loop.run_until_complete(_mcp_cagri("get_live_scores"))
        finally:
            loop.close()
        return sonuc
    except Exception as e:
        return {"basarili": False, "hata": str(e)[:300]}

def mcp_fiksturleri_getir(tarih=None, lig=None):
    """Fikstürleri çeker. lig verilirse get_league_fixtures, yoksa get_day_fixtures kullanılır."""
    if not MCP_OK:
        return {"basarili": False, "hata": "MCP kütüphanesi kurulu değil."}
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            if lig:
                sonuc = loop.run_until_complete(_mcp_cagri("get_league_fixtures", {"league": lig}))
            elif tarih:
                sonuc = loop.run_until_complete(_mcp_cagri("get_day_fixtures", {"date": tarih}))
            else:
                sonuc = loop.run_until_complete(_mcp_cagri("get_fixtures"))
        finally:
            loop.close()
        return sonuc
    except Exception as e:
        return {"basarili": False, "hata": str(e)[:300]}

def mcp_mac_detay_getir(match_id):
    if not MCP_OK: return {"basarili": False, "hata": "MCP kurulu değil."}
    try:
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        try: sonuc = loop.run_until_complete(_mcp_cagri("get_match", {"match_id": match_id}))
        finally: loop.close()
        return sonuc
    except Exception as e:
        return {"basarili": False, "hata": str(e)[:300]}

def mcp_ara(query):
    if not MCP_OK: return {"basarili": False, "hata": "MCP kurulu değil."}
    try:
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        try: sonuc = loop.run_until_complete(_mcp_cagri("search", {"query": query}))
        finally: loop.close()
        return sonuc
    except Exception as e:
        return {"basarili": False, "hata": str(e)[:300]}

def mcp_saglik_kontrol():
    if not MCP_OK: return {"basarili": False, "hata": "MCP kurulu değil."}
    try:
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        try: sonuc = loop.run_until_complete(_mcp_cagri("health"))
        finally: loop.close()
        return sonuc
    except Exception as e:
        return {"basarili": False, "hata": str(e)[:300]}

def mcp_sonuc_metni(result):
    """MCP tool sonucunu okunabilir metne çevirir."""
    if not result.get("basarili"):
        return f"❌ Hata: {result.get('hata', 'bilinmiyor')}"
    try:
        r = result["sonuc"]
        if hasattr(r, "content") and r.content:
            parcalar = []
            for c in r.content:
                if hasattr(c, "text"): parcalar.append(c.text)
            return "\n".join(parcalar) if parcalar else str(r)
        return str(r)
    except Exception as e:
        return f"⚠️ Sonuç okunamadı: {e}"

def mcp_skor_parse(metin):
    """MCP canlı skor metnini maç listesine çevirir (basit parser)."""
    maclar = []
    if not metin: return maclar
    # JSON denemesi
    try:
        if metin.strip().startswith(("[", "{")):
            data = json.loads(metin)
            if isinstance(data, list):
                for m in data:
                    maclar.append(m)
            elif isinstance(data, dict):
                for key in ["matches", "fixtures", "data", "live_scores", "results"]:
                    if key in data and isinstance(data[key], list):
                        for m in data[key]: maclar.append(m)
                        break
                else:
                    maclar.append(data)
            return maclar
    except (json.JSONDecodeError, TypeError):
        pass
    # Düz metin - satır satır ayır
    for satir in metin.split("\n"):
        satir = satir.strip()
        if not satir: continue
        # "Team A 2-1 Team B" formatı
        m = re.search(r'(.+?)\s+(\d+)\s*[-:]\s*(\d+)\s+(.+)', satir)
        if m:
            maclar.append({
                "home": m.group(1).strip(), "away": m.group(4).strip(),
                "home_score": m.group(2), "away_score": m.group(3),
                "raw": satir
            })
    return maclar

def _e(x): return _html.escape(str(x))

def rozet(metin, tip="gray"):
    return f'<span class="fa-badge fa-b-{tip}">{_e(metin)}</span>'

def mac_karti(ev, dep, skor_belli, skor_ev, skor_dep, lam_ev, lam_dep, saat="", ulke="", tarih=""):
    orta = (f'<div class="fa-score">{int(skor_ev)} - {int(skor_dep)}</div>' if skor_belli
            else '<div class="fa-vs">VS</div>')
    bayrak = ulke_bayrak_bul(ulke)
    ust_bilgi = ""
    if saat or ulke or tarih:
        parcalar = []
        if bayrak != "🌍" or ulke: parcalar.append(f"{bayrak} {_e((ulke or '').title())}")
        if tarih: parcalar.append(f"📅 {_e(tarih)}")
        if saat: parcalar.append(f"🕐 {_e(saat)}")
        if parcalar: ust_bilgi = f'<div class="fa-sub" style="margin-bottom:8px;">{" • ".join(parcalar)}</div>'
    alt = f'<div class="fa-sub">Model beklenen gol: {lam_ev:.2f} - {lam_dep:.2f}</div>'
    return (f'<div class="fa-hero">{ust_bilgi}<div class="fa-teams"><div class="fa-team">{_e(ev)}</div>'
            f'{orta}<div class="fa-team">{_e(dep)}</div></div>{alt}</div>')

def mac_tahmin_karti(v_g, g=None):
    try:
        try: ya = yeniden_analiz(v_g)
        except Exception: ya = (g or {}).get("analiz", {})
        p1 = ya.get("p1", 33.33); px = ya.get("px", 33.33); p2 = ya.get("p2", 33.34)
        ust_25 = ya.get("ust_25", 50); alt_25 = 100 - ust_25
        kg_var = ya.get("kg_var_model", 50); kg_yok = 100 - kg_var
        en1x2 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        sec1x2, y1x2 = en1x2; e1x2 = esik_1x2_al(sec1x2); p1x2_poz = y1x2 >= e1x2
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
        return f'''
        <div class="fa-mk">
            <div class="fa-mk-row"><span class="fa-mk-lbl">🎯 1X2</span>
                <span class="fa-mk-pick {r(p1x2_poz)}">{_e(isim1x2)}</span>
                <span class="fa-mk-pct">%{y1x2:.0f} <span class="fa-mk-badge {b(p1x2_poz)}">{bt(p1x2_poz)} eşik %{e1x2:.0f}</span></span></div>
            <div class="fa-mk-row"><span class="fa-mk-lbl">⚽ Gol</span>
                <span class="fa-mk-pick {r(gol_poz)}">{_e(gol_s)}</span>
                <span class="fa-mk-pct">%{gol_y:.0f} <span class="fa-mk-badge {b(gol_poz)}">{bt(gol_poz)} eşik %{gol_e:.0f}</span></span></div>
            <div class="fa-mk-row"><span class="fa-mk-lbl">🤝 KG</span>
                <span class="fa-mk-pick {r(kg_poz)}">{_e(kg_s)}</span>
                <span class="fa-mk-pct">%{kg_y:.0f} <span class="fa-mk-badge {b(kg_poz)}">{bt(kg_poz)} eşik %{kg_e:.0f}</span></span></div>
        </div>'''
    except Exception: return ""

def olasilik_bar(etiket, yuzde, esik=None, renk="#3b82f6"):
    y = max(0.0, min(100.0, yuzde)); isaret = ""
    if esik is not None:
        renk = "#22c55e" if yuzde >= esik else "#475569"
        isaret = f'<div class="fa-tick" style="left:{esik:.0f}%"></div>'
    return (f'<div class="fa-row"><div class="fa-row-top"><span class="fa-lbl">{_e(etiket)}</span>'
            f'<span class="fa-val">%{yuzde:.1f}</span></div>'
            f'<div class="fa-bar"><div class="fa-fill" style="width:{y:.1f}%;background:{renk}"></div>{isaret}</div></div>')

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
        seviye, emoji, _k, etiket = guven_seviyesi_bul(yuzde)
        tip = "green" if seviye == "yuksek" else "yellow" if seviye == "orta" else "gray"
        durum = rozet(f"{etiket} güven", tip); sinif = "fa-card fa-pos"; pct_sinif = "fa-pct"
        not_satiri = f'<div class="fa-mut">{_e(alt_satir)}</div>'
    else:
        durum = rozet("Eşik altı", "gray"); sinif = "fa-card fa-neg"; pct_sinif = "fa-pct fa-off"
        not_satiri = f'<div class="fa-mut">{_e(alt_satir)} • Gerekli: %{esik:.0f}</div>'
    bar = olasilik_bar("", yuzde, esik)
    return (f'<div class="{sinif}"><div class="fa-ttl">{_e(baslik)}</div>'
            f'<div class="fa-pickrow"><div><div class="fa-pick">{_e(secim)}</div>{durum}</div>'
            f'<div class="{pct_sinif}">%{yuzde:.1f}</div></div>{bar}{not_satiri}</div>')

def istat_karti(baslik, ist, esik_metni):
    t = ist["tam"]; y = ist["yakin"]; yl = ist["yanlis"]; top = t + y + yl
    if top == 0: govde = '<div class="fa-big fa-off">—</div><div class="fa-mut">Henüz bahis yok</div>'
    else:
        isabet = (t + y) / top * 100
        sinif = "fa-g" if isabet >= 85 else "fa-y" if isabet >= 70 else "fa-r"
        govde = (f'<div class="fa-big {sinif}">%{isabet:.0f}</div>'
                 f'<div class="fa-mut">✅ {t + y} doğru • ❌ {yl} yanlış • {top} bahis</div>')
    return (f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>{govde}'
            f'<div class="fa-mut">{_e(esik_metni)}</div></div>')

def backtest_karti(baslik, dogru, yanlis):
    top = dogru + yanlis
    if top == 0: return (f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>'
                         f'<div class="fa-mut">Eşiği geçen maç yok.</div></div>')
    yuzde = dogru / top * 100; alt_s, ust_s = wilson_aralik(dogru, top)
    sinif = "fa-g" if yuzde >= 85 else "fa-y" if yuzde >= 70 else "fa-r"
    renk = "#22c55e" if yuzde >= 85 else "#f59e0b" if yuzde >= 70 else "#ef4444"
    return (f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>'
            f'<div class="fa-pickrow"><div class="fa-big {sinif}">%{yuzde:.1f}</div>'
            f'<div style="text-align:right"><div class="fa-val">✅ {dogru} &nbsp; ❌ {yanlis}</div>'
            f'<div class="fa-mut">{top} bahis</div></div></div>'
            f'<div class="fa-ci"><div class="fa-ci-fill" style="left:{alt_s:.1f}%;width:{max(ust_s - alt_s, 0.5):.1f}%"></div>'
            f'<div class="fa-ci-dot" style="left:{yuzde:.1f}%;background:{renk}"></div></div>'
            f'<div class="fa-mut">%95 güven aralığı: %{alt_s:.0f} – %{ust_s:.0f}</div></div>')

def mac_sonuc_ikon(g):
    try:
        v = g["veri"]
        if not v.get("skor_belli", False): return "⚫"
        try: ya = yeniden_analiz(v)
        except Exception: ya = g.get("analiz", {})
        d = sonuc_hesapla({"veri": v, "analiz": ya})
        if not d: return "⚫"
        verilen = [x for x in [d["oneri_1x2"]["tuttu"], d["oneri_gol"]["tuttu"], d["oneri_kg"]["tuttu"]] if x is not None]
        if not verilen: return "⚫"
        if all(verilen): return "✅"
        if not any(verilen): return "❌"
        return "🟡"
    except Exception: return "⚫"

def nav_git(hedef):
    st.session_state.sayfa = hedef
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
    if hedef == "backtest":
        st.session_state.bt_sonuc = None
        st.session_state.bt_detaylar = []
    st.rerun()

def nav_bar():
    if st.session_state.sayfa == "giris": return
    try: kutu = st.container(key="fa_nav")
    except TypeError: kutu = st.container()
    with kutu:
        if admin_mi():
            secenekler = [("🏠", "giris"), ("🔴 Canlı", "canli"), ("📊 Geçmiş", "gecmis"),
                          ("🔮 Gelecek", "gelecek"), ("🔬 Test", "backtest"), ("⚙️ Ayar", "ayarlar")]
        else:
            secenekler = [("🏠 Ana", "giris"), ("🔴 Canlı", "canli"),
                          ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek")]
        kolonlar = st.columns(len(secenekler))
        for kol, (etiket, hedef) in zip(kolonlar, secenekler):
            with kol:
                aktif = st.session_state.sayfa == hedef
                if st.button(etiket, key=f"nav_{hedef}", use_container_width=True,
                             type="primary" if aktif else "secondary"):
                    if not aktif: nav_git(hedef)

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
                st.session_state.giris_yapildi = True; st.session_state.rol = "admin"
                st.session_state.sayfa = "giris"; st.rerun()
            else: st.error("❌ Yanlış şifre.")
        if misafir_btn:
            st.session_state.giris_yapildi = True; st.session_state.rol = "misafir"
            st.session_state.sayfa = "giris"; st.rerun()
    st.markdown("""
        <div class="login-features">
            <span class="lf-chip">🎯 1X2</span><span class="lf-chip">⚽ Üst/Alt 2.5</span>
            <span class="lf-chip">🤝 KG Var/Yok</span><span class="lf-chip">🔴 Canlı Skorlar</span>
            <span class="lf-chip">🔬 Backtest</span>
        </div>
        <div class="login-footer">© <b>Futbol Analiz Pro</b> • Bilgi amaçlıdır</div>
    """, unsafe_allow_html=True)

def ust_bar():
    c1, c2 = st.columns([3, 1])
    with c1:
        if admin_mi(): st.markdown("👑 **Admin Modu**")
        else: st.markdown("👤 **Misafir Modu**")
    with c2:
        if st.button("🚪 Çıkış", use_container_width=True, key="cikis_btn"):
            st.session_state.giris_yapildi = False; st.session_state.rol = None
            st.session_state.sayfa = "giris"; st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
            st.session_state.tek_silme_onay = None; st.session_state.tek_silme_gelecek = None
            st.session_state.silme_onay = False; st.session_state.aktif_kayit_idx = None
            st.session_state.aktif_gelecek_idx = None; st.session_state.bt_sonuc = None
            st.session_state.bt_detaylar = []; st.rerun()

def misafir_aciklama():
    with st.expander("📖 **Uygulamayı Tanı ve Kuralları Oku**", expanded=False):
        st.markdown("""
### ⚽ Futbol Analiz Pro
Futbol maçlarının **geçmiş istatistiklerini** analiz ederek **1X2**, **Üst/Alt 2.5** ve **KG** tahminleri üretir.

### 🔴 CANLI SKORLAR (YENİ)
LiveScore MCP entegrasyonu ile **anlık maç skorları** görüntülenir.
- 1000+ ligden canlı veri
- Fikstür, takım, oyuncu bilgileri
- IP başına dakikada 30 istek sınırı

### 🎯 EŞİKLER
- 1X2 → %55+ • Üst → %82 • Alt → %74 • KG Var → %73 • KG Yok → %88

### 📊 1X2
- **1** = Ev • **X** = Beraberlik • **2** = Dep

### ⚡ STRATEJİ
- **TEKLİ:** Düşük risk • **2'Lİ:** İsabet %72 • **3'LÜ:** İsabet %61

### ⚠️ KURALLAR
1. Kaybetmeyi kabul et 2. Bankanı koru 3. Martingale yapma
4. Sadece önerilere oyna 5. Limit koy 6. Ara ver
7. Kazancı çek 8. Alkol/sinirde oynama

### 🚫 SORUMLULUK
18 yaş altı yasak. **Yeşilay: 115**

**🍀 Bol şans!**
        """)

if not st.session_state.giris_yapildi:
    giris_ekrani(); st.stop()

ust_bar()
nav_bar()

# ==========================================
# CANLI SKORLAR SAYFASI (LIVESCORE MCP)
# ==========================================
if st.session_state.sayfa == "canli":
    st.markdown("<h1>🔴 Canlı Maç Skorları</h1>", unsafe_allow_html=True)
    st.caption("LiveScore MCP ile 1000+ ligden gerçek zamanlı skorlar")

    if not MCP_OK:
        st.error("""
❌ **MCP kütüphanesi kurulu değil.**

`requirements.txt` dosyasına şu satırları ekleyin:
