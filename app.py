import streamlit as st
import math
import copy
import re
import random
import json
import os
import html as _html
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

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
    .mh-stat-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin: 0 0 16px 0; }
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
GECMIS_DOSYA = "data/gecmis.json"
GELECEK_DOSYA = "data/gelecek.json"
GELECEK_TAHMIN_DOSYA = "data/gelecek_tahmin.json"
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
        os.makedirs(os.path.dirname(dosya) or ".", exist_ok=True)
        with open(dosya, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def gecmis_yukle(): return _yukle(GECMIS_DOSYA)
def gecmis_kaydet(v): _kaydet(GECMIS_DOSYA, v)
def gelecek_yukle(): return _yukle(GELECEK_DOSYA)
def gelecek_kaydet(v): _kaydet(GELECEK_DOSYA, v)
def gelecek_tahmin_yukle(): return _yukle(GELECEK_TAHMIN_DOSYA)
def gelecek_tahmin_kaydet(v): _kaydet(GELECEK_TAHMIN_DOSYA, v)


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
    "saat": "", "tarih": "", "ulke": "", "format": "bilinmiyor", "kaynak_url": "",
}


# ==========================================
# SESSION STATE
# ==========================================
if "sayfa" not in st.session_state: st.session_state.sayfa = "giris"
if "form_verileri" not in st.session_state: st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
if "gecmis_analizler" not in st.session_state: st.session_state.gecmis_analizler = gecmis_yukle()
if "gelecek_analizler" not in st.session_state: st.session_state.gelecek_analizler = gelecek_yukle()
if "gelecek_tahmin_analizler" not in st.session_state: st.session_state.gelecek_tahmin_analizler = gelecek_tahmin_yukle()
if "kayit_yapildi" not in st.session_state: st.session_state.kayit_yapildi = False
if "gelecekten_gelindi" not in st.session_state: st.session_state.gelecekten_gelindi = False
if "aktif_gelecek_idx" not in st.session_state: st.session_state.aktif_gelecek_idx = None
if "tek_silme_onay" not in st.session_state: st.session_state.tek_silme_onay = None
if "tek_silme_gelecek" not in st.session_state: st.session_state.tek_silme_gelecek = None
if "tek_silme_gelecek_tahmin" not in st.session_state: st.session_state.tek_silme_gelecek_tahmin = None
if "silme_onay" not in st.session_state: st.session_state.silme_onay = False
if "silme_onay_gelecek" not in st.session_state: st.session_state.silme_onay_gelecek = False
if "silme_onay_gelecek_tahmin" not in st.session_state: st.session_state.silme_onay_gelecek_tahmin = False
if "giris_yapildi" not in st.session_state: st.session_state.giris_yapildi = False
if "rol" not in st.session_state: st.session_state.rol = None
if "esikler" not in st.session_state: st.session_state.esikler = ayarlar_yukle()
if "bt_sonuc" not in st.session_state: st.session_state.bt_sonuc = None


def admin_mi(): return st.session_state.get("rol") == "admin"
def esik_al(key): return st.session_state.esikler.get(key, 50.0)
def esik_1x2_al(secim):
    km = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}
    return st.session_state.esikler.get(km.get(secim, ""), 55.0)


# ==========================================
# ÜLKE BAYRAK
# ==========================================
ULKE_BAYRAK = {
    "switzerland": "🇨🇭", "isviçre": "🇨🇭", "england": "🏴󠁧󠁢󠁥󠁮󠁧", "ingiltere": "🏴",
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


def clamp(x, lo, hi): return max(lo, min(hi, x))


def guven_seviyesi_bul(o):
    if o >= ESIK_YUKSEK: return ("yuksek", "🟢", "success", "Yüksek")
    if o >= ESIK_ORTA: return ("orta", "🟡", "warning", "Orta")
    if o >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "error", "Belirsiz")
    return ("cok_dusuk", "⚫", "error", "Düşük")


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


def oneri_istatistik_guncel(gecmis):
    ist = {"1x2": {"tam": 0, "yakin": 0, "yanlis": 0},
           "gol": {"tam": 0, "yakin": 0, "yanlis": 0},
           "kg": {"tam": 0, "yakin": 0, "yanlis": 0}}
    for g in gecmis:
        try:
            v = g["veri"]
            if not v.get("skor_belli", False): continue
            d = sonuc_hesapla({"veri": v, "analiz": g.get("analiz", {})})
            if not d: continue
            for key in ["oneri_1x2", "oneri_gol", "oneri_kg"]:
                kisa = key.replace("oneri_", "")
                durum = d[key].get("durum")
                if durum == "tam": ist[kisa]["tam"] += 1
                elif durum == "yanlis": ist[kisa]["yanlis"] += 1
        except Exception:
            continue
    return ist


def backtest_hesapla(gecmis, secenekler, esikler):
    sonuc = {"1x2": {"dogru": 0, "yanlis": 0}, "kg_var": {"dogru": 0, "yanlis": 0},
             "kg_yok": {"dogru": 0, "yanlis": 0}, "ust": {"dogru": 0, "yanlis": 0},
             "alt": {"dogru": 0, "yanlis": 0}}
    for g in gecmis:
        try:
            v = g["veri"]
            if not v.get("skor_belli", False): continue
            se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
            tg = se + sd
            gercek_ust = tg > 2.5
            gercek_kg = (se > 0 and sd > 0)
            gercek_1x2 = "1" if se > sd else ("X" if se == sd else "2")
            a = g.get("analiz", {})
            p1 = a.get("p1", 33.33); px = a.get("px", 33.33); p2 = a.get("p2", 33.34)
            u25 = a.get("ust_25", 50); alt = 100 - u25
            kgv = a.get("kg_var_model", 50); kgy = 100 - kgv
            if secenekler.get("1x2", False):
                s, y = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
                esik = {"1": esikler["esik_1"], "X": esikler["esik_x"], "2": esikler["esik_2"]}[s]
                if y >= esik:
                    if s == gercek_1x2: sonuc["1x2"]["dogru"] += 1
                    else: sonuc["1x2"]["yanlis"] += 1
            if secenekler.get("kg_var", False):
                if kgv >= esikler["kg_var"] and kgv >= kgy:
                    if gercek_kg: sonuc["kg_var"]["dogru"] += 1
                    else: sonuc["kg_var"]["yanlis"] += 1
            if secenekler.get("kg_yok", False):
                if kgy >= esikler["kg_yok"] and kgy >= kgv:
                    if not gercek_kg: sonuc["kg_yok"]["dogru"] += 1
                    else: sonuc["kg_yok"]["yanlis"] += 1
            if secenekler.get("ust", False):
                if u25 >= esikler["ust"] and u25 >= alt:
                    if gercek_ust: sonuc["ust"]["dogru"] += 1
                    else: sonuc["ust"]["yanlis"] += 1
            if secenekler.get("alt", False):
                if alt >= esikler["alt"] and alt >= u25:
                    if not gercek_ust: sonuc["alt"]["dogru"] += 1
                    else: sonuc["alt"]["yanlis"] += 1
        except Exception:
            continue
    return sonuc


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


def istat_karti(baslik, ist, esik_metni):
    t = ist["tam"]; y = ist["yakin"]; yl = ist["yanlis"]; top = t + y + yl
    if top == 0:
        govde = '<div class="fa-big fa-off">—</div><div class="fa-mut">Henüz bahis yok</div>'
    else:
        isabet = (t + y) / top * 100
        sinif = "fa-g" if isabet >= 85 else "fa-y" if isabet >= 70 else "fa-r"
        govde = f'<div class="fa-big {sinif}">%{isabet:.0f}</div><div class="fa-mut">✅ {t + y} doğru • ❌ {yl} yanlış</div>'
    return f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>{govde}<div class="fa-mut">{_e(esik_metni)}</div></div>'


def backtest_karti(baslik, dogru, yanlis):
    top = dogru + yanlis
    if top == 0:
        return f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div><div class="fa-mut">Eşiği geçen maç yok.</div></div>'
    yuzde = dogru / top * 100
    sinif = "fa-g" if yuzde >= 85 else "fa-y" if yuzde >= 70 else "fa-r"
    return f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div><div class="fa-pickrow"><div class="fa-big {sinif}">%{yuzde:.1f}</div><div style="text-align:right"><div class="fa-val">✅ {dogru} &nbsp; ❌ {yanlis}</div><div class="fa-mut">{top} bahis</div></div></div></div>'


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


def mac_durum_etiketi(v):
    try:
        mac_tarih = (v.get("tarih", "") or "").strip()
        mac_saat = (v.get("saat", "") or "").strip()
        if not mac_tarih or not mac_saat:
            return ""
        mac_dt = datetime.strptime(f"{mac_tarih} {mac_saat}", "%d.%m.%Y %H:%M")
        simdi_tr = datetime.utcnow() + timedelta(hours=3)
        fark_dk = (simdi_tr - mac_dt).total_seconds() / 60
        if fark_dk < -15:
            return ""
        elif fark_dk < 0:
            return '<div style="background:#3b82f6;color:white;padding:6px 12px;border-radius:8px;text-align:center;font-weight:700;margin-bottom:8px;">⏰ MAÇ BAŞLAMAK ÜZERE</div>'
        elif fark_dk <= 60:
            return '<div style="background:#ef4444;color:white;padding:6px 12px;border-radius:8px;text-align:center;font-weight:700;margin-bottom:8px;">🔴 MAÇ BAŞLADI</div>'
        elif fark_dk <= 180:
            return '<div style="background:#f59e0b;color:#0b1220;padding:6px 12px;border-radius:8px;text-align:center;font-weight:700;margin-bottom:8px;">⏱️ MAÇ DEVAM EDİYOR</div>'
        else:
            return '<div style="background:#475569;color:white;padding:6px 12px;border-radius:8px;text-align:center;font-weight:700;margin-bottom:8px;">✅ MAÇ BİTTİ — Sonuç güncellenecek</div>'
    except Exception:
        return ""


def nav_bar():
    if st.session_state.sayfa == "giris": return
    try: k = st.container(key="fa_nav")
    except TypeError: k = st.container()
    with k:
        if admin_mi():
            sc = [("🏠", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek"), ("🎯 Tahmin", "gelecek_tahmin"), ("🔬 Test", "backtest"), ("⚙️ Ayar", "ayarlar")]
        else:
            sc = [("🏠 Ana", "giris"), ("📊 Geçmiş", "gecmis"), ("🎯 Tahminler", "gelecek_tahmin")]
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
                        st.session_state.tek_silme_gelecek_tahmin = None
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


def misafir_aciklama():
    with st.expander("📖 **Uygulamayı Tanı ve Kuralları Oku**", expanded=False):
        st.markdown("""
### ⚽ Futbol Analiz Pro Nedir?

Bu uygulama, futbol maçlarının **geçmiş istatistiklerini** analiz ederek 
**1X2 (Maç Sonucu)**, **Üst/Alt 2.5** ve **Karşılıklı Gol (KG)** tahminleri üretir. 
Sadece **bilgilendirme amaçlıdır.** Kesin sonuç garantisi **YOKTUR.**

---

### 🎯 EŞİKLER NEDİR? NEDEN KULLANILIR?

**Eşik** = Bir tahminin "oynanabilir" sayılması için geçmesi gereken minimum yüzde.

**Örnek eşikler:**
- 1X2 → %55+
- Üst 2.5 → %65
- Alt 2.5 → %55
- KG Var → %57
- KG Yok → %72

**Neden eşik?** Belirsiz maçları elemek için. Sadece yüksek olasılıklı maçlara odaklanılır.

---

### 📊 1X2 NEDİR?
- **1** = Ev sahibi kazanır
- **X** = Beraberlik
- **2** = Deplasman kazanır

En yüksek olasılıklı sonuç **en olası** sonuçtur. 1X2 en zor markettir.

---

### 📊 GEÇMİŞ VERİLER NASIL OKUNUR?
- ✅ = Her iki tahmin de tuttu
- 🟡 = Sadece biri tuttu
- ❌ = İki tahmin de yanlış
- ⚫ = O maçta öneri yoktu

---

### ⚠️ DİKKATLİ BAHİS KURALLARI

**1. KAYBETMEYİ KABUL ET** — Hiçbir sistem %100 değildir.
**2. BANKANI KORU** — Her bahis bankanın %2-5'i.
**3. MARTINGALE YAPMA** — Kayıptan sonra 2 katı basma.
**4. SADECE ÖNERİLERE OYNA** — Eşiği geçmeyen maçlara oynama.
**5. HAFTALIK LİMİT KOY** — Örn: max 20 bahis.
**6. KAYIP SERİSİNDE ARA VER** — 3-4 kayıp sonrası 2-3 gün mola.
**7. KAZANCI ÇEK** — %30-50'sini hemen çek.
**8. ALKOL/SİNİR DURUMUNDA OYNAMA**

---

### 🚫 SORUMLULUK REDDİ

- Bu uygulama **SADECE bilgi amaçlıdır.**
- Hiçbir kayıptan **sorumlu değiliz.**
- **18 yaşından küçükler** bahis oynayamaz.
- **Yeşilay Danışma: 115**

**Bol şans! BU BİR ANALİZ, KUMAR DEĞİL.** 🍀
        """)


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
        st.markdown("<p style='text-align:center; color:gray;'>Veriler GitHub Actions tarafından 2 saatte bir güncellenir.</p>", unsafe_allow_html=True)

        st.info("🤖 **Bot her 2 saatte bir çalışır.** Veriler otomatik güncellenir.")
        st.caption(f"📊 Şu an: **{len(st.session_state.gecmis_analizler)}** geçmiş, **{len(st.session_state.gelecek_analizler)}** gelecek, **{len(st.session_state.gelecek_tahmin_analizler)}** tahmin")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("📊 Geçmiş", use_container_width=True, type="primary"):
                st.session_state.sayfa = "gecmis"; st.rerun()
        with c2:
            if st.button("🔮 Gelecek", use_container_width=True, type="primary"):
                st.session_state.sayfa = "gelecek"; st.rerun()
        with c3:
            if st.button("🎯 Tahmin", use_container_width=True, type="primary"):
                st.session_state.sayfa = "gelecek_tahmin"; st.rerun()
        with c4:
            if st.button("⚙️ Ayarlar", use_container_width=True):
                st.session_state.sayfa = "ayarlar"; st.rerun()
    else:
        gs = len(st.session_state.gecmis_analizler)
        gl = len(st.session_state.gelecek_analizler)
        gt = len(st.session_state.gelecek_tahmin_analizler)
        st.markdown(f"""
            <div class="mh-hero">
                <div class="mh-hero-icon">⚽</div>
                <div class="mh-hero-title">Futbol Analiz Pro</div>
                <div class="mh-hero-sub">Akıllı maç analizi ve tahmin motoru</div>
                <div class="mh-hero-badge">● CANLI VERİ</div>
            </div>
            <div class="mh-stat-grid">
                <div class="mh-stat"><div class="mh-stat-icon">📊</div><div class="mh-stat-num">{gs}</div><div class="mh-stat-lbl">Geçmiş</div></div>
                <div class="mh-stat"><div class="mh-stat-icon">🔮</div><div class="mh-stat-num">{gl}</div><div class="mh-stat-lbl">Gelecek</div></div>
                <div class="mh-stat"><div class="mh-stat-icon">🎯</div><div class="mh-stat-num">{gt}</div><div class="mh-stat-lbl">Tahmin</div></div>
            </div>
            <div class="mh-section-title">HIZLI ERİŞİM</div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📊  Geçmiş Maçlar", use_container_width=True, type="primary", key="m_gecmis"):
                st.session_state.sayfa = "gecmis"; st.rerun()
        with c2:
            if st.button("🎯  Tahmin Edilenler", use_container_width=True, type="primary", key="m_tahmin"):
                st.session_state.sayfa = "gelecek_tahmin"; st.rerun()

        st.markdown("""
            <div class="mh-info">
                💡 <b>İpucu:</b> "Tahmin Edilen Maçlar" bölümünde sadece <b>eşikleri geçen</b> maçlar listelenir.
                Her maçta <b>1X2</b>, <b>Üst/Alt 2.5</b> ve <b>KG Var/Yok</b> tahminlerini görürsün.
            </div>
            <div class="mh-section-title" style="margin-top:20px;">BİLGİLENDİRME</div>
        """, unsafe_allow_html=True)
        misafir_aciklama()

        st.markdown("""
            <div class="login-footer" style="margin-top:24px;">
                © <b>Futbol Analiz Pro</b> • Bilgi amaçlıdır • Kesin sonuç garantisi yoktur
            </div>
        """, unsafe_allow_html=True)


# ==========================================
# GEÇMİŞ
# ==========================================
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gec = st.session_state.gecmis_analizler
    toplam = len(gec)

    ist = oneri_istatistik_guncel(gec)
    st.markdown("### 🎯 ÖNERİ İSTATİSTİKLERİ")
    st.caption("Güncel eşiklerle yeniden hesaplanır")
    c_1, c_2, c_3 = st.columns(3)
    with c_1:
        st.markdown(istat_karti("🎯 1X2", ist["1x2"],
            f"1 %{esik_1x2_al('1'):.0f} • X %{esik_1x2_al('X'):.0f} • 2 %{esik_1x2_al('2'):.0f}"),
            unsafe_allow_html=True)
    with c_2:
        st.markdown(istat_karti("⚽ Üst/Alt 2.5", ist["gol"],
            f"Üst %{esik_al('ust'):.0f} • Alt %{esik_al('alt'):.0f}"),
            unsafe_allow_html=True)
    with c_3:
        st.markdown(istat_karti("🤝 KG Var/Yok", ist["kg"],
            f"Var %{esik_al('kg_var'):.0f} • Yok %{esik_al('kg_yok'):.0f}"),
            unsafe_allow_html=True)

    st.divider()
    st.markdown(f"### ⚽ Maçlar ({toplam})")

    if not gec:
        st.info("ℹ️ Kayıt yok.")
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
                        st.error("❌ Format hatalı.")
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
# GELECEK (Tüm oynanmamış — admin)
# ==========================================
elif st.session_state.sayfa == "gelecek":
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    st.caption("Tüm oynanmamış maçlar. Eşiği geçenler 'Tahmin' bölümünde de görünür.")
    gel = st.session_state.gelecek_analizler
    toplam_g = len(gel)
    if not gel:
        st.info("ℹ️ Gelecek maç yok. Bot 2 saatte bir otomatik çalışır.")
    for i, g in enumerate(reversed(gel)):
        ig = len(gel) - 1 - i
        v = g["veri"]
        te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
        try:
            a = analiz_hesapla(v); le = a["lam_ev"]; ld = a["lam_dep"]
        except Exception: le = ld = 0

        durum = mac_durum_etiketi(v)
        if durum:
            st.markdown(durum, unsafe_allow_html=True)

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
        st.divider()

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
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gel_geri"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# GELECEK TAHMİN (Sadece eşiği geçenler)
# ==========================================
elif st.session_state.sayfa == "gelecek_tahmin":
    st.markdown("<h1>🎯 Tahmin Edilen Maçlar</h1>", unsafe_allow_html=True)
    st.caption("Sadece eşikleri geçen maçlar.")
    gel = st.session_state.gelecek_tahmin_analizler
    toplam_g = len(gel)
    if not gel:
        st.info("ℹ️ Şu an tahmin edilen maç yok. Bot 2 saatte bir otomatik çalışır.")
    for i, g in enumerate(reversed(gel)):
        ig = len(gel) - 1 - i
        v = g["veri"]
        te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
        try:
            a = analiz_hesapla(v); le = a["lam_ev"]; ld = a["lam_dep"]
        except Exception: le = ld = 0

        durum = mac_durum_etiketi(v)
        if durum:
            st.markdown(durum, unsafe_allow_html=True)

        st.markdown(mac_karti(te, td, False, 0, 0, le, ld, saat=v.get("saat", ""), ulke=v.get("ulke", ""), tarih=v.get("tarih", "")), unsafe_allow_html=True)
        th = mac_tahmin_karti(v, g)
        if th: st.markdown(th, unsafe_allow_html=True)
        if admin_mi():
            cd, csil = st.columns([5, 1])
            with cd:
                if st.button("🔍 Detaylı", use_container_width=True, key=f"gtmac_{ig}"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True
                    st.session_state.gelecekten_gelindi = True
                    st.session_state.aktif_gelecek_idx = ig
                    st.session_state.sayfa = "sonuc"; st.rerun()
            with csil:
                if st.button("🗑️", key=f"gtsil_{ig}"):
                    st.session_state.tek_silme_gelecek_tahmin = ig if st.session_state.tek_silme_gelecek_tahmin != ig else None
                    st.rerun()
            if st.session_state.tek_silme_gelecek_tahmin == ig:
                ce, ch = st.columns(2)
                with ce:
                    if st.button("✅ Sil", key=f"gtevet_{ig}", use_container_width=True, type="primary"):
                        if 0 <= ig < len(st.session_state.gelecek_tahmin_analizler):
                            st.session_state.gelecek_tahmin_analizler.pop(ig)
                            gelecek_tahmin_kaydet(st.session_state.gelecek_tahmin_analizler)
                        st.session_state.tek_silme_gelecek_tahmin = None; st.rerun()
                with ch:
                    if st.button("❌ İptal", key=f"gthayir_{ig}", use_container_width=True):
                        st.session_state.tek_silme_gelecek_tahmin = None; st.rerun()
        else:
            if st.button("🔍 Detaylı", use_container_width=True, key=f"gtmac_{ig}"):
                st.session_state.form_verileri = copy.deepcopy(v)
                st.session_state.kayit_yapildi = True
                st.session_state.gelecekten_gelindi = True
                st.session_state.aktif_gelecek_idx = ig
                st.session_state.sayfa = "sonuc"; st.rerun()
        st.divider()

    if admin_mi():
        st.markdown("### 💾 Yedekleme (Tahmin)")
        cind, cyuk = st.columns(2)
        with cind:
            st.download_button(
                label=f"📥 Tahminleri İndir ({toplam_g} maç)",
                data=json.dumps(st.session_state.gelecek_tahmin_analizler, ensure_ascii=False, indent=2),
                file_name=f"tahmin_{toplam_g}mac.json",
                mime="application/json",
                use_container_width=True,
                key="ind_tahmin"
            )
        with cyuk:
            yuk = st.file_uploader("📤 Tahminleri Yükle (JSON)", type=["json"], key="yuk_tahmin")
            if yuk is not None:
                try:
                    veri = json.loads(yuk.read().decode("utf-8"))
                    if isinstance(veri, list):
                        st.session_state.gelecek_tahmin_analizler = veri
                        gelecek_tahmin_kaydet(veri)
                        st.success(f"✅ {len(veri)} maç yüklendi!")
                        st.rerun()
                    else:
                        st.error("❌ Format hatalı.")
                except Exception as ex:
                    st.error(f"❌ Hata: {ex}")

        st.divider()
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gt_geri"):
            st.session_state.sayfa = "giris"; st.rerun()
    else:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gt_geri_m"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# BACKTEST
# ==========================================
elif st.session_state.sayfa == "backtest":
    if not admin_mi():
        st.error("❌ Sadece admin.")
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary"):
            st.session_state.sayfa = "giris"; st.rerun()
        st.stop()

    st.markdown("<h1>🔬 Backtest</h1>", unsafe_allow_html=True)
    st.caption("Geçmiş maçlarda seçtiğin marketleri test et.")

    gec = st.session_state.gecmis_analizler
    if not gec:
        st.warning("⚠️ Geçmiş maç yok.")
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary"):
            st.session_state.sayfa = "giris"; st.rerun()
        st.stop()

    st.markdown("### ⚙️ Test Seçenekleri")
    with st.expander("Marketleri ve Eşikleri Ayarla", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**🎯 Maç Sonucu**")
            sec_1x2 = st.checkbox("1X2", value=True, key="bt_1x2")
            esik_bt_1 = st.slider("1 eşiği %", 0, 100, 55, 1, key="bt_e1")
            esik_bt_x = st.slider("X eşiği %", 0, 100, 55, 1, key="bt_ex")
            esik_bt_2 = st.slider("2 eşiği %", 0, 100, 55, 1, key="bt_e2")
        with c2:
            st.markdown("**🤝 KG**")
            sec_kg_var = st.checkbox("KG Var", value=True, key="bt_kgv")
            esik_kg_var = st.slider("KG Var eşiği %", 0, 100, 57, 1, key="bt_kgve")
            sec_kg_yok = st.checkbox("KG Yok", value=True, key="bt_kgy")
            esik_kg_yok = st.slider("KG Yok eşiği %", 0, 100, 72, 1, key="bt_kgye")
        with c3:
            st.markdown("**⚽ Gol**")
            sec_ust = st.checkbox("Üst 2.5", value=True, key="bt_ust")
            esik_ust = st.slider("Üst eşiği %", 0, 100, 65, 1, key="bt_uste")
            sec_alt = st.checkbox("Alt 2.5", value=True, key="bt_alt")
            esik_alt = st.slider("Alt eşiği %", 0, 100, 55, 1, key="bt_alte")

    secenekler = {"1x2": sec_1x2, "kg_var": sec_kg_var, "kg_yok": sec_kg_yok, "ust": sec_ust, "alt": sec_alt}
    esikler = {
        "esik_1": float(esik_bt_1), "esik_x": float(esik_bt_x), "esik_2": float(esik_bt_2),
        "kg_var": float(esik_kg_var), "kg_yok": float(esik_kg_yok),
        "ust": float(esik_ust), "alt": float(esik_alt),
    }

    if st.button("🚀 Test Et", use_container_width=True, type="primary", key="bt_btn"):
        if not any(secenekler.values()):
            st.warning("⚠️ En az bir market seç.")
        else:
            with st.spinner("Test ediliyor..."):
                st.session_state.bt_sonuc = backtest_hesapla(gec, secenekler, esikler)

    if st.session_state.bt_sonuc:
        sonuc = st.session_state.bt_sonuc
        st.divider()
        st.markdown("## 📊 BACKTEST SONUCU")
        for key, baslik in [
            ("1x2", "🎯 1X2"), ("kg_var", "🤝 KG Var"), ("kg_yok", "🤝 KG Yok"),
            ("ust", "⚽ Üst 2.5"), ("alt", "⚽ Alt 2.5"),
        ]:
            if secenekler.get(key, False):
                d = sonuc.get(key, {"dogru": 0, "yanlis": 0})
                st.markdown(backtest_karti(baslik, d["dogru"], d["yanlis"]), unsafe_allow_html=True)

    st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="bt_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# AYARLAR
# ==========================================
elif st.session_state.sayfa == "ayarlar":
    if not admin_mi():
        st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>⚙️ Eşik Ayarları</h1>", unsafe_allow_html=True)
    st.caption("⚠️ Bu ayarlar bot için geçerli değil. Bot için scraper.py'deki ESIKLER'i güncelle.")
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

    st.divider()
    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.sayfa = "giris"
        st.rerun()
