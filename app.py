import streamlit as st
import math
import copy
import re
import random
import json
import os

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
    "siralama_ev": 0, "siralama_dep": 0,
    "xg_ev": 0.0, "xg_dep": 0.0,
    "atilan_ev": 0.0, "atilan_dep": 0.0,
    "yenen_ev": 0.0, "yenen_dep": 0.0,
    "clean_sheets_ev": 0.0, "clean_sheets_dep": 0.0,
    "team_scored_ev": 0.0, "team_scored_dep": 0.0,
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
    "takim_ev": "", "takim_dep": "", "skor_ev": 0, "skor_dep": 0,
    "skor_belli": False,
    "lig_ort_toplam": 0.0,
    "lig_ust25": 0.0,
    "lig_kg": 0.0,
    "form_str_ev": "", "form_str_dep": "",
    "format": "bilinmiyor",
}

MAX_GOL = 8
BELIRSIZLIK = 0.20

# ==========================================
# VERİ GRUPLARI (BACKTEST İÇİN)
# ==========================================
VERI_GRUPLARI = {
    "📊 Atak/Gol": [
        ("xg_ev", "xG (Ev)", "float", 0.0, 3.0, 0.1),
        ("xg_dep", "xG (Dep)", "float", 0.0, 3.0, 0.1),
        ("atilan_ev", "Atılan Gol (Ev)", "float", 0.0, 3.5, 0.1),
        ("atilan_dep", "Atılan Gol (Dep)", "float", 0.0, 3.5, 0.1),
        ("yenen_ev", "Yenen Gol (Ev)", "float", 0.0, 3.5, 0.1),
        ("yenen_dep", "Yenen Gol (Dep)", "float", 0.0, 3.5, 0.1),
        ("team_scored_ev", "Team Scored (Ev)", "int", 0, 100, 5),
        ("team_scored_dep", "Team Scored (Dep)", "int", 0, 100, 5),
    ],
    "📈 Form": [
        ("ppg_ev", "PPG (Ev)", "float", 0.0, 3.0, 0.1),
        ("mpg_dep", "MPG (Dep)", "float", 0.0, 3.0, 0.1),
    ],
    "🏆 Sıralama": [
        ("siralama_ev", "Sıralama (Ev) ≤", "int", 1, 30, 1),
        ("siralama_dep", "Sıralama (Dep) ≤", "int", 1, 30, 1),
    ],
    "🛡️ Savunma": [
        ("clean_sheets_ev", "Clean Sheets (Ev)", "int", 0, 100, 5),
        ("clean_sheets_dep", "Clean Sheets (Dep)", "int", 0, 100, 5),
    ],
    "⚽ Üst/Alt 2.5": [
        ("ust25_ev", "Üst 2.5 (Ev)", "int", 0, 100, 5),
        ("ust25_dep", "Üst 2.5 (Dep)", "int", 0, 100, 5),
        ("ust15_ev", "Üst 1.5 (Ev)", "int", 0, 100, 5),
        ("ust15_dep", "Üst 1.5 (Dep)", "int", 0, 100, 5),
        ("ust35_ev", "Üst 3.5 (Ev)", "int", 0, 100, 5),
        ("ust35_dep", "Üst 3.5 (Dep)", "int", 0, 100, 5),
        ("ust05_ev", "Üst 0.5 (Ev)", "int", 0, 100, 5),
        ("ust05_dep", "Üst 0.5 (Dep)", "int", 0, 100, 5),
    ],
    "🤝 KG": [
        ("kg_siklik_ev", "KG Sıklık (Ev)", "int", 0, 100, 5),
        ("kg_siklik_dep", "KG Sıklık (Dep)", "int", 0, 100, 5),
        ("btts_1h_ev", "KG 1Y (Ev)", "int", 0, 100, 5),
        ("btts_1h_dep", "KG 1Y (Dep)", "int", 0, 100, 5),
        ("btts_2h_ev", "KG 2Y (Ev)", "int", 0, 100, 5),
        ("btts_2h_dep", "KG 2Y (Dep)", "int", 0, 100, 5),
        ("btts_over15_ev", "KG + Üst 1.5 (Ev)", "int", 0, 100, 5),
        ("btts_over15_dep", "KG + Üst 1.5 (Dep)", "int", 0, 100, 5),
        ("btts_over25_ev", "KG + Üst 2.5 (Ev)", "int", 0, 100, 5),
        ("btts_over25_dep", "KG + Üst 2.5 (Dep)", "int", 0, 100, 5),
    ],
    "📊 Toplam Gol": [
        ("tg_0_ev", "TG 0 Gol (Ev)", "int", 0, 100, 5),
        ("tg_0_dep", "TG 0 Gol (Dep)", "int", 0, 100, 5),
        ("tg_1_ev", "TG 1 Gol (Ev)", "int", 0, 100, 5),
        ("tg_1_dep", "TG 1 Gol (Dep)", "int", 0, 100, 5),
        ("tg_2_ev", "TG 2 Gol (Ev)", "int", 0, 100, 5),
        ("tg_2_dep", "TG 2 Gol (Dep)", "int", 0, 100, 5),
        ("tg_3_ev", "TG 3 Gol (Ev)", "int", 0, 100, 5),
        ("tg_3_dep", "TG 3 Gol (Dep)", "int", 0, 100, 5),
        ("tg_4_ev", "TG 4+ Gol (Ev)", "int", 0, 100, 5),
        ("tg_4_dep", "TG 4+ Gol (Dep)", "int", 0, 100, 5),
    ],
    "⏱️ İlk Yarı": [
        ("ht_ust05_ev", "1Y Üst 0.5 (Ev)", "int", 0, 100, 5),
        ("ht_ust05_dep", "1Y Üst 0.5 (Dep)", "int", 0, 100, 5),
        ("ht_ust15_ev", "1Y Üst 1.5 (Ev)", "int", 0, 100, 5),
        ("ht_ust15_dep", "1Y Üst 1.5 (Dep)", "int", 0, 100, 5),
        ("ht_ust25_ev", "1Y Üst 2.5 (Ev)", "int", 0, 100, 5),
        ("ht_ust25_dep", "1Y Üst 2.5 (Dep)", "int", 0, 100, 5),
    ],
    "🏁 1Y/2Y": [
        ("wht_wft_ev", "W-HT W-FT (Ev)", "int", 0, 100, 5),
        ("wht_wft_dep", "W-HT W-FT (Dep)", "int", 0, 100, 5),
        ("wht_dft_ev", "W-HT D-FT (Ev)", "int", 0, 100, 5),
        ("wht_dft_dep", "W-HT D-FT (Dep)", "int", 0, 100, 5),
        ("dht_wft_ev", "D-HT W-FT (Ev)", "int", 0, 100, 5),
        ("dht_wft_dep", "D-HT W-FT (Dep)", "int", 0, 100, 5),
        ("dht_dft_ev", "D-HT D-FT (Ev)", "int", 0, 100, 5),
        ("dht_dft_dep", "D-HT D-FT (Dep)", "int", 0, 100, 5),
        ("lht_wft_ev", "L-HT W-FT (Ev)", "int", 0, 100, 5),
        ("lht_wft_dep", "L-HT W-FT (Dep)", "int", 0, 100, 5),
        ("lht_lft_ev", "L-HT L-FT (Ev)", "int", 0, 100, 5),
        ("lht_lft_dep", "L-HT L-FT (Dep)", "int", 0, 100, 5),
    ],
    "🎯 1X2": [
        ("galibiyet_ev", "Galibiyet (Ev)", "int", 0, 100, 5),
        ("galibiyet_dep", "Galibiyet (Dep)", "int", 0, 100, 5),
        ("beraberlik_ev", "Beraberlik (Ev)", "int", 0, 100, 5),
        ("beraberlik_dep", "Beraberlik (Dep)", "int", 0, 100, 5),
        ("maglubiyet_ev", "Mağlubiyet (Ev)", "int", 0, 100, 5),
        ("maglubiyet_dep", "Mağlubiyet (Dep)", "int", 0, 100, 5),
    ],
    "🔄 İY/MS": [
        ("win_1h_ev", "1Y Kazanma (Ev)", "int", 0, 100, 5),
        ("win_1h_dep", "1Y Kazanma (Dep)", "int", 0, 100, 5),
        ("draw_ht_ev", "1Y Beraberlik (Ev)", "int", 0, 100, 5),
        ("draw_ht_dep", "1Y Beraberlik (Dep)", "int", 0, 100, 5),
        ("lose_1h_ev", "1Y Kaybetme (Ev)", "int", 0, 100, 5),
        ("lose_1h_dep", "1Y Kaybetme (Dep)", "int", 0, 100, 5),
    ],
    "⚔️ Diğer": [
        ("win_btts_ev", "Kazan+KG (Ev)", "int", 0, 100, 5),
        ("win_btts_dep", "Kazan+KG (Dep)", "int", 0, 100, 5),
        ("draw_btts_ev", "Berabere+KG (Ev)", "int", 0, 100, 5),
        ("draw_btts_dep", "Berabere+KG (Dep)", "int", 0, 100, 5),
        ("lose_btts_ev", "Kaybet+KG (Ev)", "int", 0, 100, 5),
        ("lose_btts_dep", "Kaybet+KG (Dep)", "int", 0, 100, 5),
        ("win_over15_ev", "Kazan+Üst 1.5 (Ev)", "int", 0, 100, 5),
        ("win_over15_dep", "Kazan+Üst 1.5 (Dep)", "int", 0, 100, 5),
        ("lose_over15_ev", "Kaybet+Üst 1.5 (Ev)", "int", 0, 100, 5),
        ("lose_over15_dep", "Kaybet+Üst 1.5 (Dep)", "int", 0, 100, 5),
    ],
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

# ROL YÖNETİMİ
if "giris_yapildi" not in st.session_state: st.session_state.giris_yapildi = False
if "rol" not in st.session_state: st.session_state.rol = None

# EŞİKLER
if "esikler" not in st.session_state:
    st.session_state.esikler = ayarlar_yukle()

# BACKTEST MARKET SEÇENEKLERİ
if "bt_market" not in st.session_state:
    st.session_state.bt_market = {
        "kg_var": False, "kg_yok": False,
        "ust": False, "alt": False
    }
if "bt_market_esik" not in st.session_state:
    st.session_state.bt_market_esik = {
        "kg_var": 70.0, "kg_yok": 70.0,
        "ust": 70.0, "alt": 70.0
    }

# BACKTEST VERİ FİLTRELERİ
if "bt_filtreler" not in st.session_state:
    st.session_state.bt_filtreler = {}

# BACKTEST SONUÇLARI
if "bt_sonuc" not in st.session_state:
    st.session_state.bt_sonuc = None
if "bt_detaylar" not in st.session_state:
    st.session_state.bt_detaylar = []
if "bt_ozet" not in st.session_state:
    st.session_state.bt_ozet = None


def admin_mi():
    return st.session_state.get("rol") == "admin"


def esik_al(key):
    return st.session_state.esikler.get(key, 50.0)


# ==========================================
# YARDIMCI FONKSİYONLAR
# ==========================================
def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def guven_seviyesi_bul(olasilik):
    if olasilik >= ESIK_YUKSEK: return ("yuksek", "🟢", "success", "Yüksek")
    if olasilik >= ESIK_ORTA:   return ("orta", "🟡", "warning", "Orta")
    if olasilik >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "error", "Belirsiz")
    return ("cok_dusuk", "⚫", "error", "Düşük")


def kayit_yeni_format_mi(g):
    if "dogruluk" not in g or not g["dogruluk"]:
        return False
    d = g["dogruluk"]
    if "oneri_gol" not in d: return False
    if not isinstance(d.get("oneri_gol"), dict): return False
    if "tuttu" not in d["oneri_gol"]: return False
    return True


def oneri_istatistik(gecmis):
    ist = {"gol": {"tam": 0, "yakin": 0, "yanlis": 0}, "kg": {"tam": 0, "yakin": 0, "yanlis": 0}}
    for g in gecmis:
        if not kayit_yeni_format_mi(g): continue
        d = g["dogruluk"]
        for key in ["oneri_gol", "oneri_kg"]:
            kisa = key.replace("oneri_", "")
            try:
                durum = d[key].get("durum", None); tuttu = d[key].get("tuttu", None)
                if durum == "tam": ist[kisa]["tam"] += 1
                elif durum == "yakin": ist[kisa]["yakin"] += 1
                elif durum == "yanlis": ist[kisa]["yanlis"] += 1
                elif tuttu is True: ist[kisa]["tam"] += 1
                elif tuttu is False: ist[kisa]["yanlis"] += 1
            except (KeyError, TypeError): continue
    return ist


def ist_skor_metni(ist_kayit):
    t = ist_kayit["tam"]; y = ist_kayit["yakin"]; yl = ist_kayit["yanlis"]
    top = t + y + yl
    if top == 0: return "— veri yok"
    return f"✅{t} 🟡{y} ❌{yl} → **%{(t+y)/top*100:.0f}** isabet"


# ==========================================
# FİLTRE KONTROLÜ
# ==========================================
def filtre_geciyor_mu(v, filtreler):
    """
    filtreler: {"alan_key": {"aktif": True, "esik": 50, "tip": "int/float", "yon": "gte/lte"}, ...}
    Tüm aktif filtreleri geçen maçlar True döner.
    """
    for key, f in filtreler.items():
        if not f.get("aktif", False):
            continue
        deger = v.get(key, 0)
        if deger is None: deger = 0
        esik = f.get("esik", 0)
        yon = f.get("yon", "gte")

        try:
            deger = float(deger)
            esik = float(esik)
        except (ValueError, TypeError):
            continue

        if yon == "gte":
            if deger < esik:
                return False
        elif yon == "lte":
            if deger > esik:
                return False
    return True


def aktif_filtre_sayisi(filtreler):
    return sum(1 for f in filtreler.values() if f.get("aktif", False))


def filtre_ozeti(filtreler):
    aktifler = []
    for key, f in filtreler.items():
        if f.get("aktif", False):
            yon_sym = "≥" if f.get("yon") == "gte" else "≤"
            aktifler.append(f"{f.get('etiket', key)} {yon_sym} {f.get('esik', 0)}")
    return aktifler


# ==========================================
# BACKTEST FONKSİYONU (FİLTRELİ)
# ==========================================
def backtest_filtreli_hesapla(gecmis, market_sec, market_esik, filtreler):
    """
    market_sec: {"kg_var": bool, "kg_yok": bool, "ust": bool, "alt": bool}
    market_esik: {"kg_var": 70, ...}
    filtreler: {"alan_key": {"aktif": True, "esik": 50, "yon": "gte"}, ...}
    """
    sonuc = {
        "kg_var": {"dogru": 0, "yanlis": 0, "toplam_sec": 0, "toplam_gecen": 0},
        "kg_yok": {"dogru": 0, "yanlis": 0, "toplam_sec": 0, "toplam_gecen": 0},
        "ust": {"dogru": 0, "yanlis": 0, "toplam_sec": 0, "toplam_gecen": 0},
        "alt": {"dogru": 0, "yanlis": 0, "toplam_sec": 0, "toplam_gecen": 0},
    }
    # Filtresiz referans (aynı market eşikleriyle)
    sonuc_filtresiz = {
        "kg_var": {"dogru": 0, "yanlis": 0},
        "kg_yok": {"dogru": 0, "yanlis": 0},
        "ust": {"dogru": 0, "yanlis": 0},
        "alt": {"dogru": 0, "yanlis": 0},
    }
    mac_detaylari = []
    toplam_gecen = 0

    for g in gecmis:
        try:
            v = g["veri"]
            analiz = g.get("analiz", {})
            if not v.get("skor_belli", False):
                continue

            # Filtresiz test (referans)
            for market_key in ["kg_var", "kg_yok", "ust", "alt"]:
                if not market_sec.get(market_key, False):
                    continue
                sonuc_filtresiz = _market_test(v, analiz, market_key, market_esik[market_key], sonuc_filtresiz)

            # Filtre kontrolü
            if not filtre_geciyor_mu(v, filtreler):
                continue

            toplam_gecen += 1

            mac_kayit = {
                "takim_ev": v.get("takim_ev", "Ev"),
                "takim_dep": v.get("takim_dep", "Dep"),
                "skor": f"{v.get('skor_ev', 0)}-{v.get('skor_dep', 0)}",
                "gercek": {},
                "tahminler": []
            }

            skor_ev = int(v.get("skor_ev", 0))
            skor_dep = int(v.get("skor_dep", 0))
            toplam_gol = skor_ev + skor_dep
            gercek_kg_var = (skor_ev > 0 and skor_dep > 0)
            gercek_ust = toplam_gol > 2.5

            mac_kayit["gercek"]["kg"] = "Var" if gercek_kg_var else "Yok"
            mac_kayit["gercek"]["gol"] = "Üst" if gercek_ust else "Alt"

            for market_key in ["kg_var", "kg_yok", "ust", "alt"]:
                if not market_sec.get(market_key, False):
                    continue
                sonuc, mac_kayit = _market_test(v, analiz, market_key, market_esik[market_key], sonuc, mac_kayit)

            if mac_kayit["tahminler"]:
                mac_detaylari.append(mac_kayit)

        except Exception:
            continue

    return sonuc, sonuc_filtresiz, mac_detaylari, toplam_gecen


def _market_test(v, analiz, market_key, esik, sonuc, mac_kayit=None):
    """
    Tek bir market için test yapar, sonucu günceller.
    """
    skor_ev = int(v.get("skor_ev", 0))
    skor_dep = int(v.get("skor_dep", 0))
    toplam_gol = skor_ev + skor_dep
    gercek_kg_var = (skor_ev > 0 and skor_dep > 0)
    gercek_ust = toplam_gol > 2.5

    ust_25 = analiz.get("ust_25", 50)
    alt_25 = 100 - ust_25
    kg_var = analiz.get("kg_var_model", 50)
    kg_yok = 100 - kg_var

    if market_key == "kg_var":
        sonuc["kg_var"]["toplam_sec"] = sonuc["kg_var"].get("toplam_sec", 0) + 1
        if kg_var >= esik and kg_var >= kg_yok:
            sonuc["kg_var"]["toplam_gecen"] = sonuc["kg_var"].get("toplam_gecen", 0) + 1
            if gercek_kg_var:
                sonuc["kg_var"]["dogru"] += 1
                if mac_kayit is not None:
                    mac_kayit["tahminler"].append("KG Var ✅")
            else:
                sonuc["kg_var"]["yanlis"] += 1
                if mac_kayit is not None:
                    mac_kayit["tahminler"].append("KG Var ❌")

    elif market_key == "kg_yok":
        sonuc["kg_yok"]["toplam_sec"] = sonuc["kg_yok"].get("toplam_sec", 0) + 1
        if kg_yok >= esik and kg_yok >= kg_var:
            sonuc["kg_yok"]["toplam_gecen"] = sonuc["kg_yok"].get("toplam_gecen", 0) + 1
            if not gercek_kg_var:
                sonuc["kg_yok"]["dogru"] += 1
                if mac_kayit is not None:
                    mac_kayit["tahminler"].append("KG Yok ✅")
            else:
                sonuc["kg_yok"]["yanlis"] += 1
                if mac_kayit is not None:
                    mac_kayit["tahminler"].append("KG Yok ❌")

    elif market_key == "ust":
        sonuc["ust"]["toplam_sec"] = sonuc["ust"].get("toplam_sec", 0) + 1
        if ust_25 >= esik and ust_25 >= alt_25:
            sonuc["ust"]["toplam_gecen"] = sonuc["ust"].get("toplam_gecen", 0) + 1
            if gercek_ust:
                sonuc["ust"]["dogru"] += 1
                if mac_kayit is not None:
                    mac_kayit["tahminler"].append("Üst ✅")
            else:
                sonuc["ust"]["yanlis"] += 1
                if mac_kayit is not None:
                    mac_kayit["tahminler"].append("Üst ❌")

    elif market_key == "alt":
        sonuc["alt"]["toplam_sec"] = sonuc["alt"].get("toplam_sec", 0) + 1
        if alt_25 >= esik and alt_25 >= ust_25:
            sonuc["alt"]["toplam_gecen"] = sonuc["alt"].get("toplam_gecen", 0) + 1
            if not gercek_ust:
                sonuc["alt"]["dogru"] += 1
                if mac_kayit is not None:
                    mac_kayit["tahminler"].append("Alt ✅")
            else:
                sonuc["alt"]["yanlis"] += 1
                if mac_kayit is not None:
                    mac_kayit["tahminler"].append("Alt ❌")

    if mac_kayit is None:
        return sonuc
    return sonuc, mac_kayit


# ==========================================
# MANUEL ALANLAR
# ==========================================
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
# UYGULAMA BAŞLANGIÇ
# ==========================================
if not st.session_state.giris_yapildi:
    giris_ekrani()
    st.stop()

ust_bar()


# ==========================================
# SAYFA: ANA SAYFA
# ==========================================
if st.session_state.sayfa == "giris":
    st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)

    if admin_mi():
        st.markdown("<p style='text-align:center; color:gray;'>İstatistik metnini kopyala → yapıştır → analiz et.</p>", unsafe_allow_html=True)
        st.markdown("### 📋 İstatistik Metnini Yapıştır")

        yapistir_metni = st.text_area("Yapıştırma alanı", height=280, key="yapistir_input", label_visibility="collapsed", placeholder="İstatistik metnini buraya yapıştır.")
        st.divider()

        col_bt1, col_bt2, col_bt3, col_bt4, col_bt5 = st.columns([2, 1, 1, 1, 1])
        with col_bt1:
            analiz_btn = st.button("🚀 ANALİZ ET", use_container_width=True, type="primary")
        with col_bt2:
            gecmis_btn = st.button("📊 Geçmiş", use_container_width=True)
        with col_bt3:
            gelecek_btn = st.button("🔮 Gelecek", use_container_width=True)
        with col_bt4:
            backtest_btn = st.button("🔬 Backtest", use_container_width=True)
        with col_bt5:
            ayarlar_btn = st.button("⚙️ Ayarlar", use_container_width=True)

        if analiz_btn:
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
                    st.session_state.gecmisten_gelindi = False
                    st.session_state.gelecekten_gelindi = False
                    st.session_state.aktif_kayit_idx = None
                    st.session_state.aktif_gelecek_idx = None
                    st.session_state.okunamayan_alanlar = okunamayanlar
                    st.session_state.manuel_bekleyen = okunamayanlar.copy()

                    if not veri_yeterli_mi(yeni_veri):
                        st.error(f"⚠️ Analiz için yeterli veri yok.")
                    else:
                        if okunamayanlar:
                            st.session_state.sayfa = "manuel_giris"
                        else:
                            st.session_state.sayfa = "sonuc"
                        st.rerun()

        if gecmis_btn:
            st.session_state.sayfa = "gecmis"
            st.session_state.kayit_yapildi = False
            st.session_state.gecmisten_gelindi = False
            st.session_state.gelecekten_gelindi = False
            st.session_state.aktif_kayit_idx = None
            st.session_state.aktif_gelecek_idx = None
            st.session_state.okunamayan_alanlar = []
            st.session_state.manuel_bekleyen = []
            st.session_state.tek_silme_onay = None
            st.session_state.silme_onay = False
            st.rerun()

        if gelecek_btn:
            st.session_state.sayfa = "gelecek"
            st.session_state.kayit_yapildi = False
            st.session_state.gecmisten_gelindi = False
            st.session_state.gelecekten_gelindi = False
            st.session_state.aktif_kayit_idx = None
            st.session_state.aktif_gelecek_idx = None
            st.session_state.okunamayan_alanlar = []
            st.session_state.manuel_bekleyen = []
            st.session_state.tek_silme_gelecek = None
            st.rerun()

        if backtest_btn:
            st.session_state.sayfa = "backtest"
            st.session_state.bt_sonuc = None
            st.session_state.bt_detaylar = []
            st.session_state.bt_ozet = None
            st.rerun()

        if ayarlar_btn:
            st.session_state.sayfa = "ayarlar"
            st.rerun()
    else:
        st.markdown("<p style='text-align:center; color:gray;'>Analizleri görüntülemek için aşağıdaki butonları kullan.</p>", unsafe_allow_html=True)
        st.markdown("")
        st.divider()
        col_bt2, col_bt3 = st.columns(2)
        with col_bt2:
            gecmis_btn = st.button("📊 Geçmiş Maçlar", use_container_width=True, type="primary")
        with col_bt3:
            gelecek_btn = st.button("🔮 Gelecek Maçlar", use_container_width=True, type="primary")

        if gecmis_btn:
            st.session_state.sayfa = "gecmis"
            st.session_state.kayit_yapildi = False
            st.session_state.gecmisten_gelindi = False
            st.session_state.gelecekten_gelindi = False
            st.session_state.aktif_kayit_idx = None
            st.session_state.aktif_gelecek_idx = None
            st.session_state.okunamayan_alanlar = []
            st.session_state.manuel_bekleyen = []
            st.session_state.tek_silme_onay = None
            st.session_state.silme_onay = False
            st.rerun()

        if gelecek_btn:
            st.session_state.sayfa = "gelecek"
            st.session_state.kayit_yapildi = False
            st.session_state.gecmisten_gelindi = False
            st.session_state.gelecekten_gelindi = False
            st.session_state.aktif_kayit_idx = None
            st.session_state.aktif_gelecek_idx = None
            st.session_state.okunamayan_alanlar = []
            st.session_state.manuel_bekleyen = []
            st.session_state.tek_silme_gelecek = None
            st.rerun()


# ==========================================
# MANUEL GİRİŞ
# ==========================================
elif st.session_state.sayfa == "manuel_giris":
    st.markdown("<h1>📝 Eksik Alanları Doldur</h1>", unsafe_allow_html=True)
    st.warning(f"Aşağıdaki **{len(st.session_state.manuel_bekleyen)}** alan metinden çıkarılamadı:")
    v = st.session_state.form_verileri

    with st.form("manuel_form"):
        yeni_degerler = {}
        for alan_basligi in st.session_state.manuel_bekleyen:
            if alan_basligi in MANUEL_ALANLAR:
                st.markdown(f"**{alan_basligi}**")
                for (key, etiket, tip, varsayilan) in MANUEL_ALANLAR[alan_basligi]:
                    mevcut = v.get(key, varsayilan)
                    if tip == "int":
                        val = st.number_input(etiket, value=int(mevcut) if mevcut else int(varsayilan), min_value=1, max_value=100, step=1, key=f"manuel_{key}")
                        yeni_degerler[key] = int(val)
                    elif tip == "float":
                        val = st.number_input(etiket, value=float(mevcut) if mevcut else float(varsayilan), min_value=0.0, step=0.1, key=f"manuel_{key}")
                        yeni_degerler[key] = float(val)
                    else:
                        val = st.text_input(etiket, value=str(mevcut) if mevcut else "", key=f"manuel_{key}")
                        yeni_degerler[key] = val
                st.markdown("")
        col_a, col_b = st.columns(2)
        with col_a:
            kaydet = st.form_submit_button("✅ Kaydet ve Analiz Et", use_container_width=True, type="primary")
        with col_b:
            atla = st.form_submit_button("⏭️ Atla (Varsayılan)", use_container_width=True)
        if kaydet or atla:
            if kaydet: st.session_state.form_verileri.update(yeni_degerler)
            st.session_state.manuel_bekleyen = []
            st.session_state.sayfa = "sonuc"
            st.rerun()
    if st.button("⬅️ Metni Yeniden Yapıştır"):
        st.session_state.sayfa = "giris"
        st.rerun()


# ==========================================
# GEÇMİŞ
# ==========================================
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gecmis = st.session_state.gecmis_analizler
    oneri_ist = oneri_istatistik(gecmis)
    toplam = len(gecmis)

    if toplam == 0:
        st.info("ℹ️ Henüz kayıtlı maç yok.")
    else:
        st.markdown("### 🎯 ÖNERİ İSTATİSTİKLERİ")
        st.caption("Gol (Üst/Alt ayrı) • KG (Var/Yok ayrı)")
        col_1, col_2 = st.columns(2)
        with col_1:
            st.markdown("**Üst / Alt 2.5**")
            st.caption(f"Eşikler: Üst %{esik_al('ust'):.0f} • Alt %{esik_al('alt'):.0f}")
            st.markdown(ist_skor_metni(oneri_ist["gol"]))
        with col_2:
            st.markdown("**KG (Var / Yok)**")
            st.caption(f"Eşikler: Var %{esik_al('kg_var'):.0f} • Yok %{esik_al('kg_yok'):.0f}")
            st.markdown(ist_skor_metni(oneri_ist["kg"]))

    st.divider()
    st.markdown(f"### ⚽ Skoru Belli Maçlar ({toplam})")

    if toplam > 0:
        for i, g in enumerate(reversed(gecmis)):
            idx_gercek = len(gecmis) - 1 - i
            v_g = g["veri"]
            takim_ev = v_g.get("takim_ev", "Ev") or "Ev"
            takim_dep = v_g.get("takim_dep", "Dep") or "Dep"
            skor_ev = v_g.get("skor_ev", 0); skor_dep = v_g.get("skor_dep", 0)
            baslik = f"⚽ {takim_ev} {skor_ev}-{skor_dep} {takim_dep}"

            if admin_mi():
                col_maç, col_sil = st.columns([5, 1])
                with col_maç:
                    if st.button(baslik, use_container_width=True, key=f"mac_{idx_gercek}"):
                        st.session_state.form_verileri = copy.deepcopy(v_g)
                        st.session_state.kayit_yapildi = True
                        st.session_state.gecmisten_gelindi = True
                        st.session_state.gelecekten_gelindi = False
                        st.session_state.aktif_kayit_idx = idx_gercek
                        st.session_state.aktif_gelecek_idx = None
                        st.session_state.okunamayan_alanlar = []
                        st.session_state.sayfa = "sonuc"
                        st.rerun()
                with col_sil:
                    if st.button("🗑️", key=f"sil_{idx_gercek}"):
                        if st.session_state.tek_silme_onay == idx_gercek:
                            st.session_state.tek_silme_onay = None
                        else:
                            st.session_state.tek_silme_onay = idx_gercek
                        st.rerun()

                if st.session_state.tek_silme_onay == idx_gercek:
                    st.warning(f"⚠️ **{takim_ev} vs {takim_dep}** silinsin mi?")
                    col_e, col_h = st.columns(2)
                    with col_e:
                        if st.button("✅ Sil", key=f"evet_{idx_gercek}", use_container_width=True, type="primary"):
                            if 0 <= idx_gercek < len(st.session_state.gecmis_analizler):
                                st.session_state.gecmis_analizler.pop(idx_gercek)
                                gecmis_kaydet(st.session_state.gecmis_analizler)
                            st.session_state.tek_silme_onay = None
                            st.rerun()
                    with col_h:
                        if st.button("❌ İptal", key=f"hayir_{idx_gercek}", use_container_width=True):
                            st.session_state.tek_silme_onay = None
                            st.rerun()
            else:
                if st.button(baslik, use_container_width=True, key=f"mac_{idx_gercek}"):
                    st.session_state.form_verileri = copy.deepcopy(v_g)
                    st.session_state.kayit_yapildi = True
                    st.session_state.gecmisten_gelindi = True
                    st.session_state.gelecekten_gelindi = False
                    st.session_state.aktif_kayit_idx = idx_gercek
                    st.session_state.aktif_gelecek_idx = None
                    st.session_state.okunamayan_alanlar = []
                    st.session_state.sayfa = "sonuc"
                    st.rerun()

    st.divider()
    if admin_mi():
        c_temizle, c_geri = st.columns(2)
        with c_temizle:
            if st.button("🗑️ Tüm Geçmişi Temizle", use_container_width=True, key="temizle_btn"):
                st.session_state.silme_onay = True
                st.rerun()
        with c_geri:
            if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gecmis_geri"):
                st.session_state.sayfa = "giris"
                st.session_state.silme_onay = False
                st.session_state.tek_silme_onay = None
                st.rerun()

        if st.session_state.silme_onay:
            st.warning("⚠️ Tüm geçmiş silinecek. Emin misin?")
            c_e, c_h = st.columns(2)
            with c_e:
                if st.button("✅ Evet, Sil", use_container_width=True, type="primary", key="sil_hepsi_evet"):
                    st.session_state.gecmis_analizler = []
                    try:
                        if os.path.exists(GECMIS_DOSYA): os.remove(GECMIS_DOSYA)
                    except Exception: pass
                    st.session_state.silme_onay = False
                    st.session_state.tek_silme_onay = None
                    st.rerun()
            with c_h:
                if st.button("❌ İptal", use_container_width=True, key="sil_hepsi_iptal"):
                    st.session_state.silme_onay = False
                    st.rerun()
    else:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gecmis_geri_misafir"):
            st.session_state.sayfa = "giris"
            st.session_state.tek_silme_onay = None
            st.rerun()


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
            baslik = f"⚽ {takim_ev} vs {takim_dep}"

            if admin_mi():
                col_maç, col_sil = st.columns([5, 1])
                with col_maç:
                    if st.button(baslik, use_container_width=True, key=f"gmac_{idx_gercek}"):
                        st.session_state.form_verileri = copy.deepcopy(v_g)
                        st.session_state.kayit_yapildi = True
                        st.session_state.gecmisten_gelindi = False
                        st.session_state.gelecekten_gelindi = True
                        st.session_state.aktif_kayit_idx = None
                        st.session_state.aktif_gelecek_idx = idx_gercek
                        st.session_state.okunamayan_alanlar = []
                        st.session_state.sayfa = "sonuc"
                        st.rerun()
                with col_sil:
                    if st.button("🗑️", key=f"gsil_{idx_gercek}"):
                        if st.session_state.tek_silme_gelecek == idx_gercek:
                            st.session_state.tek_silme_gelecek = None
                        else:
                            st.session_state.tek_silme_gelecek = idx_gercek
                        st.rerun()

                if st.session_state.tek_silme_gelecek == idx_gercek:
                    st.warning(f"⚠️ **{takim_ev} vs {takim_dep}** silinsin mi?")
                    c_e, c_h = st.columns(2)
                    with c_e:
                        if st.button("✅ Sil", key=f"evet_g_{idx_gercek}", use_container_width=True, type="primary"):
                            if 0 <= idx_gercek < len(st.session_state.gelecek_analizler):
                                st.session_state.gelecek_analizler.pop(idx_gercek)
                                gelecek_kaydet(st.session_state.gelecek_analizler)
                            st.session_state.tek_silme_gelecek = None
                            st.rerun()
                    with c_h:
                        if st.button("❌ İptal", key=f"hayir_g_{idx_gercek}", use_container_width=True):
                            st.session_state.tek_silme_gelecek = None
                            st.rerun()
            else:
                if st.button(baslik, use_container_width=True, key=f"gmac_{idx_gercek}"):
                    st.session_state.form_verileri = copy.deepcopy(v_g)
                    st.session_state.kayit_yapildi = True
                    st.session_state.gecmisten_gelindi = False
                    st.session_state.gelecekten_gelindi = True
                    st.session_state.aktif_kayit_idx = None
                    st.session_state.aktif_gelecek_idx = idx_gercek
                    st.session_state.okunamayan_alanlar = []
                    st.session_state.sayfa = "sonuc"
                    st.rerun()

            st.divider()

    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="g_geri"):
        st.session_state.sayfa = "giris"
        st.session_state.tek_silme_gelecek = None
        st.rerun()
