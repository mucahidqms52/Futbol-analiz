import streamlit as st
import math
import copy
import re
import random
import json
import os
import html as _html
import cloudscraper
from bs4 import BeautifulSoup

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.7rem !important;
        padding-right: 0.7rem !important;
        max-width: 100% !important;
    }
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
    /* ===== PRO KOYU TEMA ===== */
    .stApp { background: #0b1220 !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp div[data-testid="stMarkdownContainer"] { color: #e6edf7 !important; }
    .stApp div[data-testid="stCaptionContainer"], .stApp div[data-testid="stCaptionContainer"] *, .stApp small { color: #8fa0bd !important; }
    hr { border-color: #23304a !important; }
    h1 { letter-spacing: 0.2px; }
    h2, h3 { border-left: 3px solid #22c55e; padding-left: 0.45rem; }

    .stTextArea textarea, .stTextInput input, div[data-testid="stNumberInput"] input {
        background: #131c2e !important; color: #e6edf7 !important; border: 1px solid #23304a !important; border-radius: 10px !important;
    }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="base-input"] { background: #131c2e !important; border-radius: 10px !important; }

    .stButton button, div[data-testid="stDownloadButton"] button, div[data-testid="stFormSubmitButton"] button {
        background: #18233a !important; border: 1px solid #23304a !important; border-radius: 12px !important; font-weight: 600 !important;
    }
    .stButton button p, div[data-testid="stDownloadButton"] button p, div[data-testid="stFormSubmitButton"] button p { color: #e6edf7 !important; }
    .stButton button:hover, div[data-testid="stDownloadButton"] button:hover { border-color: #22c55e !important; }
    .stButton button[kind="primary"], button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] {
        background: linear-gradient(135deg, #16a34a, #22c55e) !important; border: none !important;
    }
    .stButton button[kind="primary"] p, button[data-testid="stBaseButton-primary"] p, button[data-testid="stBaseButton-primaryFormSubmit"] p { color: #04130a !important; }

    div[data-testid="stExpander"] { background: #131c2e !important; border: 1px solid #23304a !important; border-radius: 14px !important; }
    div[data-testid="stExpander"] details { border: none !important; }
    div[data-testid="stAlert"] { border-radius: 12px !important; }
    div[data-testid="stFileUploader"] section { background: #131c2e !important; border: 1px dashed #23304a !important; border-radius: 12px !important; }
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
    varsayilan = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0}
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
# EŞİKLER
# ==========================================
ESIK_YUKSEK = 65.0
ESIK_ORTA = 55.0
ESIK_BELIRSIZ = 50.0
MONTE_CARLO_N = 10000

# ==========================================
# VARSAYILAN VERİ
# ==========================================
VARSAYILAN_VERI = {
    "ppg_ev": 0.0, "mpg_dep": 0.0,
    "form_str_ev": "", "form_str_dep": "",
    "siralama_ev": 0, "siralama_dep": 0,
    "puan_ev": 0, "puan_dep": 0,
    "xg_ev": 0.0, "xg_dep": 0.0,
    "atilan_ev": 0.0, "atilan_dep": 0.0,
    "yenen_ev": 0.0, "yenen_dep": 0.0,
    "clean_sheets_ev": 0.0, "clean_sheets_dep": 0.0,
    "team_scored_ev": 0.0, "team_scored_dep": 0.0,
    "team_scored_2_ev": 0.0, "team_scored_2_dep": 0.0,
    "scored_both_halves_ev": 0.0, "scored_both_halves_dep": 0.0,
    "goal_both_halves_ev": 0.0, "goal_both_halves_dep": 0.0,
    "ust05_ev": 80.0, "ust05_dep": 80.0,
    "ust15_ev": 50.0, "ust15_dep": 50.0,
    "ust25_ev": 30.0, "ust25_dep": 30.0,
    "ust35_ev": 20.0, "ust35_dep": 20.0,
    "kg_siklik_ev": 50.0, "kg_siklik_dep": 50.0,
    "btts_1h_ev": 0.0, "btts_1h_dep": 0.0,
    "btts_2h_ev": 0.0, "btts_2h_dep": 0.0,
    "btts_over15_ev": 0.0, "btts_over15_dep": 0.0,
    "btts_over25_ev": 0.0, "btts_over25_dep": 0.0,
    "tg_0_ev": 0.0, "tg_0_dep": 0.0,
    "tg_1_ev": 0.0, "tg_1_dep": 0.0,
    "tg_2_ev": 0.0, "tg_2_dep": 0.0,
    "tg_3_ev": 0.0, "tg_3_dep": 0.0,
    "tg_4_ev": 0.0, "tg_4_dep": 0.0,
    "tg_01_ev": 0.0, "tg_01_dep": 0.0,
    "tg_23_ev": 0.0, "tg_23_dep": 0.0,
    "tg_4p_ev": 0.0, "tg_4p_dep": 0.0,
    "ht_ust05_ev": 0.0, "ht_ust05_dep": 0.0,
    "ht_ust15_ev": 0.0, "ht_ust15_dep": 0.0,
    "ht_ust25_ev": 0.0, "ht_ust25_dep": 0.0,
    "wht_wft_ev": 0.0, "wht_wft_dep": 0.0,
    "wht_dft_ev": 0.0, "wht_dft_dep": 0.0,
    "wht_lft_ev": 0.0, "wht_lft_dep": 0.0,
    "dht_wft_ev": 0.0, "dht_wft_dep": 0.0,
    "dht_dft_ev": 0.0, "dht_dft_dep": 0.0,
    "dht_lft_ev": 0.0, "dht_lft_dep": 0.0,
    "lht_wft_ev": 0.0, "lht_wft_dep": 0.0,
    "lht_dft_ev": 0.0, "lht_dft_dep": 0.0,
    "lht_lft_ev": 0.0, "lht_lft_dep": 0.0,
    "galibiyet_ev": 30.0, "galibiyet_dep": 30.0,
    "beraberlik_ev": 30.0, "beraberlik_dep": 30.0,
    "maglubiyet_ev": 30.0, "maglubiyet_dep": 30.0,
    "win_1h_ev": 0.0, "win_1h_dep": 0.0,
    "draw_ht_ev": 0.0, "draw_ht_dep": 0.0,
    "lose_1h_ev": 0.0, "lose_1h_dep": 0.0,
    "win_btts_ev": 0.0, "win_btts_dep": 0.0,
    "draw_btts_ev": 0.0, "draw_btts_dep": 0.0,
    "lose_btts_ev": 0.0, "lose_btts_dep": 0.0,
    "win_over15_ev": 0.0, "win_over15_dep": 0.0,
    "lose_over15_ev": 0.0, "lose_over15_dep": 0.0,
    "takim_ev": "", "takim_dep": "",
    "skor_ev": 0, "skor_dep": 0,
    "skor_belli": False,
    "lig_ort_toplam": 0.0,
    "lig_ust25": 0.0,
    "lig_kg": 0.0,
    "format": "bilinmiyor",
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
if "bt_market" not in st.session_state: st.session_state.bt_market = {"kg_var": False, "kg_yok": False, "ust": False, "alt": False}
if "bt_market_esik" not in st.session_state: st.session_state.bt_market_esik = {"kg_var": 70.0, "kg_yok": 70.0, "ust": 70.0, "alt": 70.0}
if "bt_sonuc" not in st.session_state: st.session_state.bt_sonuc = None
if "bt_detaylar" not in st.session_state: st.session_state.bt_detaylar = []

def admin_mi(): return st.session_state.get("rol") == "admin"
def esik_al(key): return st.session_state.esikler.get(key, 50.0)

# ==========================================
# YARDIMCI FONKSİYONLAR
# ==========================================
def clamp(x, lo, hi): return max(lo, min(hi, x))

def ort_iki(a, b):
    vals = [x for x in [a, b] if x is not None and x > 0]
    if not vals: return 0
    return sum(vals) / len(vals)

def guven_seviyesi_bul(olasilik):
    if olasilik >= ESIK_YUKSEK: return ("yuksek", "🟢", "success", "Yüksek")
    if olasilik >= ESIK_ORTA:   return ("orta", "🟡", "warning", "Orta")
    if olasilik >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "error", "Belirsiz")
    return ("cok_dusuk", "⚫", "error", "Düşük")

def kayit_yeni_format_mi(g):
    if "dogruluk" not in g or not g["dogruluk"]: return False
    d = g["dogruluk"]
    if "oneri_gol" not in d: return False
    if not isinstance(d.get("oneri_gol"), dict): return False
    if "tuttu" not in d["oneri_gol"]: return False
    return True

def oneri_istatistik_guncel(gecmis):
    ist = {"gol": {"tam": 0, "yakin": 0, "yanlis": 0}, "kg": {"tam": 0, "yakin": 0, "yanlis": 0}}
    for g in gecmis:
        try:
            v = g["veri"]
            if not v.get("skor_belli", False): continue
            try: ya = yeniden_analiz(v)
            except Exception: ya = g.get("analiz", {})
            d = sonuc_hesapla({"veri": v, "analiz": ya})
            if not d: continue
            for key in ["oneri_gol", "oneri_kg"]:
                kisa = key.replace("oneri_", "")
                durum = d[key].get("durum")
                if durum == "tam": ist[kisa]["tam"] += 1
                elif durum == "yanlis": ist[kisa]["yanlis"] += 1
        except Exception: continue
    return ist

def wilson_aralik(dogru, toplam, z=1.96):
    if toplam <= 0: return 0.0, 0.0
    p = dogru / toplam
    payda = 1 + z * z / toplam
    merkez = (p + z * z / (2 * toplam)) / payda
    yari = z * math.sqrt(p * (1 - p) / toplam + z * z / (4 * toplam * toplam)) / payda
    return max(0.0, (merkez - yari) * 100), min(100.0, (merkez + yari) * 100)

def _form_ppg(s): return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1)

def yeniden_analiz(v):
    v2 = copy.deepcopy(v)
    if v2.get("form_str_ev"): v2["ppg_ev"] = _form_ppg(v2["form_str_ev"])
    if v2.get("form_str_dep"): v2["mpg_dep"] = _form_ppg(v2["form_str_dep"])
    anahtar = json.dumps(v2, sort_keys=True, ensure_ascii=False)
    if "bt_analiz_cache" not in st.session_state: st.session_state.bt_analiz_cache = {}
    cache = st.session_state.bt_analiz_cache
    if anahtar not in cache:
        a = analiz_hesapla(v2)
        cache[anahtar] = {"ust_25": a["ust_25"], "kg_var_model": a["kg_var_model"]}
    return cache[anahtar]

def backtest_hesapla(gecmis, market_sec, market_esik):
    sonuc = {
        "kg_var": {"dogru": 0, "yanlis": 0}, "kg_yok": {"dogru": 0, "yanlis": 0},
        "ust": {"dogru": 0, "yanlis": 0}, "alt": {"dogru": 0, "yanlis": 0},
    }
    mac_detaylari = []
    for g in gecmis:
        try:
            v = g["veri"]
            analiz = g.get("analiz", {})
            if not v.get("skor_belli", False): continue
            skor_ev = int(v.get("skor_ev", 0)); skor_dep = int(v.get("skor_dep", 0))
            toplam_gol = skor_ev + skor_dep
            gercek_kg_var = (skor_ev > 0 and skor_dep > 0)
            gercek_ust = toplam_gol > 2.5
            try:
                yeni_analiz = yeniden_analiz(v)
                ust_25 = yeni_analiz["ust_25"]; kg_var = yeni_analiz["kg_var_model"]
            except Exception:
                ust_25 = analiz.get("ust_25", 50); kg_var = analiz.get("kg_var_model", 50)
            alt_25 = 100 - ust_25; kg_yok = 100 - kg_var

            mac_kayit = {
                "takim_ev": v.get("takim_ev", "Ev"), "takim_dep": v.get("takim_dep", "Dep"),
                "skor": f"{skor_ev}-{skor_dep}", "gercek_kg": "Var" if gercek_kg_var else "Yok",
                "gercek_gol": "Üst" if gercek_ust else "Alt", "detaylar": []
            }

            if market_sec.get("kg_var", False) and kg_var >= market_esik["kg_var"] and kg_var >= kg_yok:
                if gercek_kg_var: sonuc["kg_var"]["dogru"] += 1; mac_kayit["detaylar"].append("KG Var ✅")
                else: sonuc["kg_var"]["yanlis"] += 1; mac_kayit["detaylar"].append("KG Var ❌")

            if market_sec.get("kg_yok", False) and kg_yok >= market_esik["kg_yok"] and kg_yok >= kg_var:
                if not gercek_kg_var: sonuc["kg_yok"]["dogru"] += 1; mac_kayit["detaylar"].append("KG Yok ✅")
                else: sonuc["kg_yok"]["yanlis"] += 1; mac_kayit["detaylar"].append("KG Yok ❌")

            if market_sec.get("ust", False) and ust_25 >= market_esik["ust"] and ust_25 >= alt_25:
                if gercek_ust: sonuc["ust"]["dogru"] += 1; mac_kayit["detaylar"].append("Üst ✅")
                else: sonuc["ust"]["yanlis"] += 1; mac_kayit["detaylar"].append("Üst ❌")

            if market_sec.get("alt", False) and alt_25 >= market_esik["alt"] and alt_25 >= ust_25:
                if not gercek_ust: sonuc["alt"]["dogru"] += 1; mac_kayit["detaylar"].append("Alt ✅")
                else: sonuc["alt"]["yanlis"] += 1; mac_kayit["detaylar"].append("Alt ❌")

            if mac_kayit["detaylar"]: mac_detaylari.append(mac_kayit)
        except Exception: continue
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

# ==========================================
# CANLI WEB SCRAPER & OTOMATİK VERİ ÇEKME
# ==========================================
def gunun_maclarini_otomatik_cek():
    """Sportytrader üzerinden günün maçlarını tarar ve veri dict listesi döner."""
    scraper = cloudscraper.create_scraper()
    base_url = "https://www.sportytrader.com/en/football/predictions/"
    
    try:
        response = scraper.get(base_url)
        if response.status_code != 200:
            return [], f"Sayfa yüklenemedi. HTTP Durum Kodu: {response.status_code}"
            
        soup = BeautifulSoup(response.content, "html.parser")
        
        mac_linkleri = []
        for a_tag in soup.select('a[href*="/predictions/"]'):
            href = a_tag.get('href')
            if href and href not in mac_linkleri and href.count("-") >= 2:
                mac_linkleri.append(href)
                
        if not mac_linkleri:
            return [], "Günün fikstüründe çekilecek uygun maç bulunamadı."
            
        cekilen_veri_listesi = []
        
        # İlk 15 maç sınırı (hız açısından)
        for link in mac_linkleri[:15]:
            full_url = link if link.startswith("http") else f"https://www.sportytrader.com{link}"
            mac_resp = scraper.get(full_url)
            
            if mac_resp.status_code == 200:
                mac_soup = BeautifulSoup(mac_resp.content, "html.parser")
                raw_text = mac_soup.get_text(separator="\n")
                
                veri, okunamayanlar = metinden_veri_cikar(raw_text)
                if veri and veri.get("takim_ev") and veri.get("atilan_ev", 0) > 0:
                    cekilen_veri_listesi.append(veri)
                    
        return cekilen_veri_listesi, None

    except Exception as e:
        return [], f"Veri çekme sırasında hata oluştu: {str(e)}"

# ==========================================
# SPORTYTRADER METİN ÇIKARICI
# ==========================================
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
    pattern = (r'(?:^|\n)\s*(\d{1,2})\s*\r?\n\s*' + re.escape(takim_adi) + r'\s*\r?\n\s*' + re.escape(takim_adi) + r'\s*\r?\n\s*(\d+)\s*\t')
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
        veri["takim_ev"] = m.group(1).strip()
        veri["takim_dep"] = m.group(2).strip()

    m = re.search(r'FT\s*\r?\n\s*(\d+)\s*-\s*(\d+)', metin)
    if m:
        veri["skor_ev"] = int(m.group(1)); veri["skor_dep"] = int(m.group(2))
        veri["skor_belli"] = True
    else: veri["skor_belli"] = False

    takim_ev = veri.get("takim_ev", ""); takim_dep = veri.get("takim_dep", "")

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
        v1, v2 = _cift_tab("Team scored twice", blok)
        if v1 is not None: veri["team_scored_2_ev"] = v1; veri["team_scored_2_dep"] = v2

    idx = metin.find("Win Draw Lose")
    if idx != -1:
        blok = metin[idx:idx+1500]
        v1, v2 = _cift_tab("Win and Over 1.5 goals", blok)
        if v1 is not None: veri["win_over15_ev"] = v1; veri["win_over15_dep"] = v2
        v1, v2 = _cift_tab("Lose and Over 1.5 goals", blok)
        if v1 is not None: veri["lose_over15_ev"] = v1; veri["lose_over15_dep"] = v2

    idx = metin.find("Both Teams to Score")
    if idx != -1:
        blok = metin[idx:idx+1500]
        m = re.search(r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*Both Teams to Score\s*\t\s*([\d.,]+)%', blok, re.MULTILINE)
        if m:
            try:
                veri["kg_siklik_ev"] = float(m.group(1).replace(",", "."))
                veri["kg_siklik_dep"] = float(m.group(2).replace(",", "."))
            except ValueError: pass

    idx = metin.find("Over Under Goals")
    if idx != -1:
        blok = metin[idx:idx+1500]
        v1, v2 = _cift_tab("Over 1.5 goals", blok)
        if v1 is not None: veri["ust15_ev"] = v1; veri["ust15_dep"] = v2
        v1, v2 = _cift_tab("Over 2.5 goals", blok)
        if v1 is not None: veri["ust25_ev"] = v1; veri["ust25_dep"] = v2

    if takim_ev:
        s, p = _sira_bul(metin, takim_ev)
        if s is not None: veri["siralama_ev"] = s; veri["puan_ev"] = p if p else 0
    if takim_dep:
        s, p = _sira_bul(metin, takim_dep)
        if s is not None: veri["siralama_dep"] = s; veri["puan_dep"] = p if p else 0

    m = re.search(r'\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\nForm\s*\t?\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])', metin)
    if m:
        form_ev = m.group(1) + m.group(2) + m.group(3) + m.group(4) + m.group(5)
        form_dep = m.group(6) + m.group(7) + m.group(8) + m.group(9) + m.group(10)
        veri["form_str_ev"] = form_ev; veri["form_str_dep"] = form_dep
        def _form_puan(s): return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1)
        veri["ppg_ev"] = _form_puan(form_ev); veri["mpg_dep"] = _form_puan(form_dep)

    veri["format"] = "sportytrader"
    return veri, okunamayanlar

def metinden_veri_cikar(metin):
    metin = metin.replace(",", ".")
    if "Main Stats" in metin and "Goals scored per game" in metin:
        veri, okunamayanlar = sportytrader_veri_cikar(metin)
        if not veri.get("takim_ev"): okunamayanlar.append("Takım isimleri (Ev)")
        if not veri.get("takim_dep"): okunamayanlar.append("Takım isimleri (Dep)")
        return veri, okunamayanlar
    veri = {}; okunamayanlar = []
    veri["format"] = "genel"
    return veri, okunamayanlar

# ==========================================
# POISSON & LAMBDA & ANALİZ
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

def poisson_matris(lam_ev, lam_dep, max_gol=MAX_GOL):
    return [[poisson_pmf(i, lam_ev) * poisson_pmf(j, lam_dep) for j in range(max_gol)] for i in range(max_gol)]

def hesapla_lambda(v):
    atilan_e = v.get("atilan_ev", 0.0); yenen_e = v.get("yenen_ev", 0.0)
    atilan_d = v.get("atilan_dep", 0.0); yenen_d = v.get("yenen_dep", 0.0)
    xg_e = v.get("xg_ev", 0.0); xg_d = v.get("xg_dep", 0.0)

    hucum_ev_baz = (xg_e * 0.60) + (atilan_e * 0.40) if xg_e > 0 else (atilan_e if atilan_e > 0 else 1.2)
    hucum_dep_baz = (xg_d * 0.60) + (atilan_d * 0.40) if xg_d > 0 else (atilan_d if atilan_d > 0 else 1.0)

    ts_ev = v.get("team_scored_ev", 0); ts_dep = v.get("team_scored_dep", 0)
    if ts_ev > 0: hucum_ev_baz *= clamp(ts_ev / 60, 0.7, 1.3)
    if ts_dep > 0: hucum_dep_baz *= clamp(ts_dep / 60, 0.7, 1.3)

    savunma_dep_zaaf = yenen_d if yenen_d > 0 else 1.2
    savunma_ev_zaaf = yenen_e if yenen_e > 0 else 1.0

    cs_ev = v.get("clean_sheets_ev", 0.0); cs_dep = v.get("clean_sheets_dep", 0.0)
    def clean_sheet_freni(cs_orani):
        if cs_orani <= 0: return 1.0
        if cs_orani < 40.0: return 1.0 - (cs_orani / 250.0)
        return max(0.40, 0.84 - (cs_orani - 40.0) * (0.44 / 60.0))

    dep_freni = clean_sheet_freni(cs_ev); ev_freni = clean_sheet_freni(cs_dep)
    lam_ev_ham = (hucum_ev_baz * 0.60) + (savunma_dep_zaaf * 0.40)
    lam_dep_ham = (hucum_dep_baz * 0.60) + (savunma_ev_zaaf * 0.40)

    form_ev = clamp(1 + (v.get("ppg_ev", 1.5) - 1.5) / 15, 0.85, 1.15)
    form_dep = clamp(1 + (v.get("mpg_dep", 1.5) - 1.5) / 15, 0.85, 1.15)

    lam_ev = clamp(lam_ev_ham * 1.05 * form_ev * ev_freni, 0.05, 4.5)
    lam_dep = clamp(lam_dep_ham * 0.95 * form_dep * dep_freni, 0.05, 4.5)
    return lam_ev, lam_dep, 0.80

def matristen_olasilik(matris, max_gol=MAX_GOL):
    p1 = px = p2 = 0.0
    ust_05 = ust_15 = ust_25 = ust_35 = 0.0
    kg_var = 0.0; skorlar = {}; toplam = 0.0
    for i in range(max_gol):
        for j in range(max_gol):
            p = matris[i][j]; toplam += p
            if i > j: p1 += p
            elif i == j: px += p
            else: p2 += p
            tg = i + j
            if tg > 0.5: ust_05 += p
            if tg > 1.5: ust_15 += p
            if tg > 2.5: ust_25 += p
            if tg > 3.5: ust_35 += p
            if i > 0 and j > 0: kg_var += p
            skorlar[f"{i}-{j}"] = p
    return {"1": p1, "X": px, "2": p2, "ust_05": ust_05, "ust_15": ust_15,
            "ust_25": ust_25, "ust_35": ust_35, "kg_var": kg_var, "skorlar": skorlar, "toplam": toplam}

def monte_carlo_simulasyon(lam_ev_base, lam_dep_base, n=MONTE_CARLO_N):
    seed = int(round(lam_ev_base * 1_000_000)) * 1_000_003 + int(round(lam_dep_base * 1_000_000))
    rng = random.Random(seed)
    sayac = {"1": 0, "X": 0, "2": 0, "ust25": 0, "kg_var": 0}
    for _ in range(n):
        sapma_ev = rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        sapma_dep = rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        lam_ev = lam_ev_base * sapma_ev; lam_dep = lam_dep_base * sapma_dep
        ev_gol = min(MAX_GOL - 1, poisson_random(lam_ev, rng))
        dep_gol = min(MAX_GOL - 1, poisson_random(lam_dep, rng))
        if ev_gol > dep_gol: sayac["1"] += 1
        elif ev_gol == dep_gol: sayac["X"] += 1
        else: sayac["2"] += 1
        if ev_gol + dep_gol > 2.5: sayac["ust25"] += 1
        if ev_gol > 0 and dep_gol > 0: sayac["kg_var"] += 1
    def yuzde(s): return s / n * 100 if n > 0 else 0
    return {"p1": yuzde(sayac["1"]), "px": yuzde(sayac["X"]), "p2": yuzde(sayac["2"]),
            "ust25": yuzde(sayac["ust25"]), "alt25": 100 - yuzde(sayac["ust25"]),
            "kg_var": yuzde(sayac["kg_var"]), "kg_yok": 100 - yuzde(sayac["kg_var"]), "n": n}

def analiz_hesapla(v):
    lam_ev, lam_dep, guven = hesapla_lambda(v)
    matris = poisson_matris(lam_ev, lam_dep, MAX_GOL)
    olas = matristen_olasilik(matris, MAX_GOL)
    toplam = olas["toplam"] or 1

    p1_po = olas["1"] / toplam * 100; px_po = olas["X"] / toplam * 100; p2_po = olas["2"] / toplam * 100
    ust25_po = olas["ust_25"] / toplam * 100; kg_var_po = olas["kg_var"] / toplam * 100

    mc = monte_carlo_simulasyon(lam_ev, lam_dep, MONTE_CARLO_N)
    p1 = (p1_po * 0.60) + (mc["p1"] * 0.40)
    px = (px_po * 0.60) + (mc["px"] * 0.40)
    p2 = (p2_po * 0.60) + (mc["p2"] * 0.40)

    t = p1 + px + p2
    if t > 0: p1, px, p2 = (p1 / t) * 100, (px / t) * 100, (p2 / t) * 100

    ust_25 = (ust25_po * 0.65) + (mc["ust25"] * 0.35)
    kg_var_model = (kg_var_po * 0.60) + (mc["kg_var"] * 0.40)
    kg_yok_model = 100.0 - kg_var_model
    alt_25 = 100.0 - ust_25

    return {
        "lam_ev": lam_ev, "lam_dep": lam_dep, "guven": guven, "matris": matris, "olas": olas,
        "p1": p1, "px": px, "p2": p2, "ust_25": ust_25, "alt_25": alt_25,
        "kg_var_model": kg_var_model, "kg_yok_model": kg_yok_model,
        "tahmini_gol": lam_ev + lam_dep, "en_olasi": max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1]),
        "en_guvenli": max([("1X", p1+px), ("X2", p2+px), ("12", p1+p2)], key=lambda x: x[1]),
        "en_olasi_gol": "Üst" if ust_25 > alt_25 else "Alt", "en_olasi_kg": "Var" if kg_var_model > kg_yok_model else "Yok"
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

    ust_25 = analiz.get("ust_25", 50); alt_25 = 100 - ust_25
    kg_var = analiz.get("kg_var_model", 50); kg_yok = 100 - kg_var

    oneri_gol = "Üst" if ust_25 >= esik_al("ust") and ust_25 >= alt_25 else ("Alt" if alt_25 >= esik_al("alt") and alt_25 >= ust_25 else None)
    oneri_kg = "Var" if kg_var >= esik_al("kg_var") and kg_var >= kg_yok else ("Yok" if kg_yok >= esik_al("kg_yok") and kg_yok >= kg_var else None)

    d_og = "tam" if oneri_gol == ("Üst" if gercek_ust else "Alt") else ("yanlis" if oneri_gol else None)
    d_ok = "tam" if oneri_kg == ("Var" if gercek_kg_var else "Yok") else ("yanlis" if oneri_kg else None)

    return {"oneri_gol": {"tahmin": oneri_gol, "tuttu": (d_og == "tam") if d_og else None, "durum": d_og},
            "oneri_kg": {"tahmin": oneri_kg, "tuttu": (d_ok == "tam") if d_ok else None, "durum": d_ok},
            "gercek_gol": "Üst" if gercek_ust else "Alt", "gercek_kg": "Var" if gercek_kg_var else "Yok"}

def veri_yeterli_mi(v):
    onemli = [v["atilan_ev"], v["atilan_dep"], v["yenen_ev"], v["yenen_dep"]]
    return sum(1 for x in onemli if x > 0) >= 2

# ==========================================
# TASARIM BİLEŞENLERİ
# ==========================================
def _e(x): return _html.escape(str(x))
def rozet(metin, tip="gray"): return f'<span class="fa-badge fa-b-{tip}">{_e(metin)}</span>'

def mac_karti(ev, dep, skor_belli, skor_ev, skor_dep, lam_ev, lam_dep):
    orta = f'<div class="fa-score">{int(skor_ev)} - {int(skor_dep)}</div>' if skor_belli else '<div class="fa-vs">VS</div>'
    alt = f'<div class="fa-sub">Model beklenen gol: {lam_ev:.2f} - {lam_dep:.2f}</div>'
    return f'<div class="fa-hero"><div class="fa-teams"><div class="fa-team">{_e(ev)}</div>{orta}<div class="fa-team">{_e(dep)}</div></div>{alt}</div>'

def olasilik_bar(etiket, yuzde, esik=None, renk="#3b82f6"):
    y = max(0.0, min(100.0, yuzde))
    isaret = f'<div class="fa-tick" style="left:{esik:.0f}%"></div>' if esik is not None else ""
    renk = ("#22c55e" if yuzde >= esik else "#475569") if esik is not None else renk
    return f'<div class="fa-row"><div class="fa-row-top"><span class="fa-lbl">{_e(etiket)}</span><span class="fa-val">%{yuzde:.1f}</span></div><div class="fa-bar"><div class="fa-fill" style="width:{y:.1f}%;background:{renk}"></div>{isaret}</div></div>'

def olasilik_paneli(a):
    return f'<div class="fa-card"><div class="fa-ttl">Maç Sonucu</div>{olasilik_bar("Ev Sahibi (1)", a["p1"], None, "#3b82f6")}{olasilik_bar("Beraberlik (X)", a["px"], None, "#94a3b8")}{olasilik_bar("Deplasman (2)", a["p2"], None, "#f59e0b")}<div class="fa-ttl" style="margin-top:12px">Piyasalar</div>{olasilik_bar("Üst 2.5", a["ust_25"], esik_al("ust"))}{olasilik_bar("Alt 2.5", a["alt_25"], esik_al("alt"))}{olasilik_bar("KG Var", a["kg_var_model"], esik_al("kg_var"))}{olasilik_bar("KG Yok", a["kg_yok_model"], esik_al("kg_yok"))}</div>'

def oneri_karti(baslik, secim, yuzde, esik, poz, alt_satir):
    if poz:
        seviye, _, _, etiket = guven_seviyesi_bul(yuzde)
        durum = rozet(f"{etiket} güven", "green" if seviye == "yuksek" else "yellow")
        sinif = "fa-card fa-pos"; pct_sinif = "fa-pct"
        not_satiri = f'<div class="fa-mut">{_e(alt_satir)}</div>'
    else:
        durum = rozet("Eşik altı", "gray")
        sinif = "fa-card fa-neg"; pct_sinif = "fa-pct fa-off"
        not_satiri = f'<div class="fa-mut">{_e(alt_satir)} • Gerekli: %{esik:.0f}</div>'
    bar = olasilik_bar("", yuzde, esik)
    return f'<div class="{sinif}"><div class="fa-ttl">{_e(baslik)}</div><div class="fa-pickrow"><div><div class="fa-pick">{_e(secim)}</div>{durum}</div><div class="{pct_sinif}">%{yuzde:.1f}</div></div>{bar}{not_satiri}</div>'

def istat_karti(baslik, ist, esik_metni):
    t = ist["tam"]; y = ist["yakin"]; yl = ist["yanlis"]; top = t + y + yl
    if top == 0: govde = '<div class="fa-big fa-off">—</div><div class="fa-mut">Henüz bahis yok</div>'
    else:
        isabet = (t + y) / top * 100
        sinif = "fa-g" if isabet >= 85 else "fa-y" if isabet >= 70 else "fa-r"
        govde = f'<div class="fa-big {sinif}">%{isabet:.0f}</div><div class="fa-mut">✅ {t + y} doğru • ❌ {yl} yanlış • {top} bahis</div>'
    return f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>{govde}<div class="fa-mut">{_e(esik_metni)}</div></div>'

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
    kutu = st.container(key="fa_nav")
    with kutu:
        secenekler = [("🏠", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek"), ("🔬 Test", "backtest"), ("⚙️ Ayar", "ayarlar")] if admin_mi() else [("🏠 Ana", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek")]
        kolonlar = st.columns(len(secenekler))
        for kol, (etiket, hedef) in zip(kolonlar, secenekler):
            with kol:
                if st.button(etiket, key=f"nav_{hedef}", use_container_width=True, type="primary" if st.session_state.sayfa == hedef else "secondary"):
                    if st.session_state.sayfa != hedef: nav_git(hedef)

def giris_ekrani():
    st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Giriş yap veya misafir olarak devam et.</p>", unsafe_allow_html=True)
    with st.form("giris_form"):
        sifre = st.text_input("🔐 Şifre (Admin)", type="password", key="sifre_input")
        c1, c2 = st.columns(2)
        with c1: admin_btn = st.form_submit_button("👑 Admin Girişi", use_container_width=True, type="primary")
        with c2: misafir_btn = st.form_submit_button("👤 Misafir Girişi", use_container_width=True)
        if admin_btn:
            if sifre == ADMIN_SIFRE:
                st.session_state.giris_yapildi = True; st.session_state.rol = "admin"; st.session_state.sayfa = "giris"; st.rerun()
            else: st.error("❌ Yanlış şifre.")
        if misafir_btn:
            st.session_state.giris_yapildi = True; st.session_state.rol = "misafir"; st.session_state.sayfa = "giris"; st.rerun()

def ust_bar():
    c1, c2 = st.columns([3, 1])
    with c1: st.markdown("👑 **Admin Modu**" if admin_mi() else "👤 **Misafir Modu**")
    with c2:
        if st.button("🚪 Çıkış", use_container_width=True, key="cikis_btn"):
            st.session_state.giris_yapildi = False; st.session_state.rol = None; st.session_state.sayfa = "giris"
            st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI); st.rerun()

# ==========================================
# UYGULAMA AKIŞI
# ==========================================
if not st.session_state.giris_yapildi:
    giris_ekrani()
    st.stop()

ust_bar()
nav_bar()

# ==========================================
# SAYFA: ANA SAYFA
# ==========================================
if st.session_state.sayfa == "giris":
    st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)

    if admin_mi():
        st.markdown("### 🌐 Canlı Veri Çekme (Otomatik)")
        if st.button("🔄 Günün Maçlarını İnternetten Otomatik Çek ve Analiz Et", type="primary", use_container_width=True):
            with st.spinner("Günün maçları taranıyor ve analiz ediliyor..."):
                maclar, hata = gunun_maclarini_otomatik_cek()
                if hata:
                    st.error(f"❌ {hata}")
                elif not maclar:
                    st.warning("⚠️ Çekilecek maç bulunamadı.")
                else:
                    eklenen = 0
                    for v in maclar:
                        a = analiz_hesapla(v)
                        yeni_kayit = kayit_olustur(v, a)
                        ust_25, alt_25 = a["ust_25"], a["alt_25"]
                        kg_var, kg_yok = a["kg_var_model"], a["kg_yok_model"]
                        gol_poz = (ust_25 >= esik_al("ust") and ust_25 >= alt_25) or (alt_25 >= esik_al("alt") and alt_25 >= ust_25)
                        kg_poz = (kg_var >= esik_al("kg_var") and kg_var >= kg_yok) or (kg_yok >= esik_al("kg_yok") and kg_yok >= kg_var)
                        
                        if gol_poz or kg_poz:
                            st.session_state.gelecek_analizler.append(yeni_kayit)
                            eklenen += 1
                    gelecek_kaydet(st.session_state.gelecek_analizler)
                    st.success(f"✅ {len(maclar)} maç çekildi, {eklenen} tanesi kriterlere uyarak Gelecek Maçlar'a kaydedildi!")
                    st.rerun()

        st.divider()
        st.markdown("### 📋 İstatistik Metnini Yapıştır (Manuel)")
        yapistir_metni = st.text_area("Yapıştırma alanı", height=200, key="yapistir_input", label_visibility="collapsed", placeholder="İstatistik metnini yapıştırın.")
        
        col_bt1, col_bt2, col_bt3 = st.columns([2, 1, 1])
        with col_bt1: analiz_btn = st.button("🚀 METNİ ANALİZ ET", use_container_width=True, type="primary")
        with col_bt2: gecmis_btn = st.button("📊 Geçmiş", use_container_width=True)
        with col_bt3: gelecek_btn = st.button("🔮 Gelecek", use_container_width=True)

        if analiz_btn:
            if not yapistir_metni.strip(): st.warning("⚠️ Önce metni yapıştırın.")
            else:
                cikan, okunamayanlar = metinden_veri_cikar(yapistir_metni)
                if not cikan: st.error("❌ Veri çıkarılamadı.")
                else:
                    yeni_veri = copy.deepcopy(VARSAYILAN_VERI)
                    yeni_veri.update(cikan)
                    st.session_state.form_verileri = yeni_veri
                    st.session_state.sayfa = "manuel_giris" if okunamayanlar else "sonuc"
                    st.rerun()

        if gecmis_btn: nav_git("gecmis")
        if gelecek_btn: nav_git("gelecek")

    else:
        col_bt2, col_bt3 = st.columns(2)
        with col_bt2: 
            if st.button("📊 Geçmiş Maçlar", use_container_width=True, type="primary"): nav_git("gecmis")
        with col_bt3: 
            if st.button("🔮 Gelecek Maçlar", use_container_width=True, type="primary"): nav_git("gelecek")

# ==========================================
# DİĞER SAYFALAR (MANUEL GİRİŞ, GEÇMİŞ, GELECEK, BACKTEST, AYARLAR, SONUÇ)
# ==========================================
elif st.session_state.sayfa == "manuel_giris":
    st.markdown("<h1>📝 Eksik Alanları Doldur</h1>", unsafe_allow_html=True)
    v = st.session_state.form_verileri
    with st.form("manuel_form"):
        yeni_degerler = {}
        for alan_basligi in st.session_state.manuel_bekleyen:
            if alan_basligi in MANUEL_ALANLAR:
                for (key, etiket, tip, varsayilan) in MANUEL_ALANLAR[alan_basligi]:
                    mevcut = v.get(key, varsayilan)
                    if tip == "int": val = st.number_input(etiket, value=int(mevcut) if mevcut else int(varsayilan), min_value=1, step=1, key=f"manuel_{key}")
                    elif tip == "float": val = st.number_input(etiket, value=float(mevcut) if mevcut else float(varsayilan), min_value=0.0, step=0.1, key=f"manuel_{key}")
                    else: val = st.text_input(etiket, value=str(mevcut) if mevcut else "", key=f"manuel_{key}")
                    yeni_degerler[key] = val
        kaydet = st.form_submit_button("✅ Kaydet ve Analiz Et", use_container_width=True, type="primary")
        if kaydet:
            st.session_state.form_verileri.update(yeni_degerler)
            st.session_state.sayfa = "sonuc"
            st.rerun()

elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gecmis = st.session_state.gecmis_analizler
    if not gecmis: st.info("ℹ️ Henüz kayıtlı maç yok.")
    else:
        oneri_ist = oneri_istatistik_guncel(gecmis)
        col_1, col_2 = st.columns(2)
        with col_1: st.markdown(istat_karti("Üst / Alt 2.5", oneri_ist["gol"], f"Eşikler: Üst %{esik_al('ust'):.0f} • Alt %{esik_al('alt'):.0f}"), unsafe_allow_html=True)
        with col_2: st.markdown(istat_karti("KG Var / Yok", oneri_ist["kg"], f"Eşikler: Var %{esik_al('kg_var'):.0f} • Yok %{esik_al('kg_yok'):.0f}"), unsafe_allow_html=True)
        st.divider()
        for i, g in enumerate(reversed(gecmis)):
            idx_gercek = len(gecmis) - 1 - i; v_g = g["veri"]
            baslik = f"⚽ {v_g.get('takim_ev', 'Ev')} {v_g.get('skor_ev', 0)}-{v_g.get('skor_dep', 0)} {v_g.get('takim_dep', 'Dep')}"
            if st.button(baslik, use_container_width=True, key=f"mac_{idx_gercek}"):
                st.session_state.form_verileri = copy.deepcopy(v_g)
                st.session_state.sayfa = "sonuc"
                st.rerun()

elif st.session_state.sayfa == "gelecek":
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    gelecek = st.session_state.gelecek_analizler
    if not gelecek: st.info("ℹ️ Gelecek maç yok.")
    else:
        for i, g in enumerate(reversed(gelecek)):
            idx_gercek = len(gelecek) - 1 - i; v_g = g["veri"]
            baslik = f"⚽ {v_g.get('takim_ev', 'Ev')} vs {v_g.get('takim_dep', 'Dep')}"
            if st.button(baslik, use_container_width=True, key=f"gmac_{idx_gercek}"):
                st.session_state.form_verileri = copy.deepcopy(v_g)
                st.session_state.gelecekten_gelindi = True
                st.session_state.aktif_gelecek_idx = idx_gercek
                st.session_state.sayfa = "sonuc"
                st.rerun()

elif st.session_state.sayfa == "ayarlar":
    st.markdown("<h1>⚙️ Eşik Ayarları</h1>", unsafe_allow_html=True)
    mevcut = st.session_state.esikler
    c1, c2 = st.columns(2)
    with c1: yeni_ust = st.slider("Üst 2.5 eşiği (%)", 0, 100, int(mevcut["ust"]), 1)
    with c2: yeni_alt = st.slider("Alt 2.5 eşiği (%)", 0, 100, int(mevcut["alt"]), 1)
    c3, c4 = st.columns(2)
    with c3: yeni_kg_var = st.slider("KG Var eşiği (%)", 0, 100, int(mevcut["kg_var"]), 1)
    with c4: yeni_kg_yok = st.slider("KG Yok eşiği (%)", 0, 100, int(mevcut["kg_yok"]), 1)
    if st.button("💾 Kaydet", use_container_width=True, type="primary"):
        yeni_esikler = {"ust": float(yeni_ust), "alt": float(yeni_alt), "kg_var": float(yeni_kg_var), "kg_yok": float(yeni_kg_yok)}
        st.session_state.esikler = yeni_esikler; ayarlar_kaydet(yeni_esikler)
        st.success("✅ Kaydedildi!")

elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)
    ust_25, alt_25 = a["ust_25"], a["alt_25"]
    kg_var_model, kg_yok_model = a["kg_var_model"], a["kg_yok_model"]

    st.markdown(mac_karti(v.get("takim_ev", "Ev Sahibi"), v.get("takim_dep", "Deplasman"), v.get("skor_belli", False), v.get("skor_ev", 0), v.get("skor_dep", 0), a["lam_ev"], a["lam_dep"]), unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)

    st.markdown("## 🏆 FİNAL ÖNERİ")
    gol_secim = "Üst 2.5" if ust_25 >= alt_25 else "Alt 2.5"
    gol_yuzde = ust_25 if ust_25 >= alt_25 else alt_25
    gol_esik = esik_al("ust") if ust_25 >= alt_25 else esik_al("alt")
    st.markdown(oneri_karti("⚽ Gol", gol_secim, gol_yuzde, gol_esik, gol_yuzde >= gol_esik, f"Üst %{ust_25:.1f} • Alt %{alt_25:.1f}"), unsafe_allow_html=True)

    kg_secim = "KG Var" if kg_var_model >= kg_yok_model else "KG Yok"
    kg_yuzde = kg_var_model if kg_var_model >= kg_yok_model else kg_yok_model
    kg_esik = esik_al("kg_var") if kg_var_model >= kg_yok_model else esik_al("kg_yok")
    st.markdown(oneri_karti("🤝 Karşılıklı Gol", kg_secim, kg_yuzde, kg_esik, kg_yuzde >= kg_esik, f"Var %{kg_var_model:.1f} • Yok %{kg_yok_model:.1f}"), unsafe_allow_html=True)

    if st.session_state.gelecekten_gelindi and admin_mi():
        idx_g = st.session_state.aktif_gelecek_idx
        if idx_g is not None and 0 <= idx_g < len(st.session_state.gelecek_analizler):
            st.divider()
            sc1, sc2, sc3 = st.columns([1, 1, 1])
            with sc1: yeni_skor_ev = st.number_input("Ev Gol", min_value=0, max_value=20, value=0)
            with sc2: yeni_skor_dep = st.number_input("Dep Gol", min_value=0, max_value=20, value=0)
            with sc3:
                st.markdown(""); st.markdown("")
                if st.button("📥 Geçmişe Taşı", use_container_width=True, type="primary"):
                    kayit = st.session_state.gelecek_analizler[idx_g]
                    kayit["veri"]["skor_ev"] = int(yeni_skor_ev); kayit["veri"]["skor_dep"] = int(yeni_skor_dep)
                    kayit["veri"]["skor_belli"] = True
                    st.session_state.gecmis_analizler.append(kayit)
                    st.session_state.gelecek_analizler.pop(idx_g)
                    gecmis_kaydet(st.session_state.gecmis_analizler)
                    gelecek_kaydet(st.session_state.gelecek_analizler)
                    nav_git("gelecek")

    st.divider()
    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.sayfa = "giris"
        st.rerun()
