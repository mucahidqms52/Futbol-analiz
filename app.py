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
</style>
""", unsafe_allow_html=True)

# ==========================================
# DOSYALAR
# ==========================================
GECMIS_DOSYA = "gecmis.json"
GELECEK_DOSYA = "gelecek.json"


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
    "reaksiyon_ev": 50.0, "reaksiyon_dep": 50.0,
    "xg_ev": 0.0, "xg_dep": 0.0,
    "atilan_ev": 0.0, "atilan_dep": 0.0,
    "yenen_ev": 0.0, "yenen_dep": 0.0,
    "ss_ev": 1.0, "ss_dep": 1.0,
    "kg_oran": 50.0,
    "galibiyet_ev": 30.0, "beraberlik_ev": 30.0, "maglubiyet_ev": 30.0,
    "galibiyet_dep": 30.0, "beraberlik_dep": 30.0, "maglubiyet_dep": 30.0,
    "yenilmezlik_ev": 30.0, "yenilmezlik_dep": 30.0,
    "hucum_hakimiyeti_ev": 50.0, "hucum_hakimiyeti_dep": 50.0,
    "agresiflik_ev": 8.0, "agresiflik_dep": 8.0,
    "isabet_ev": 40.0, "isabet_dep": 40.0,
    "hava_topu_ev": 10.0, "hava_topu_dep": 10.0,
    "ilk_gol_atar_ev": 40.0, "ilk_gol_atar_dep": 40.0,
    "ilk_gol_yer_ev": 40.0, "ilk_gol_yer_dep": 40.0,
    "ust05_ev": 80.0, "ust05_dep": 80.0,
    "ust15_ev": 50.0, "ust15_dep": 50.0,
    "ust25_ev": 30.0, "ust25_dep": 30.0,
    "ust35_ev": 20.0, "ust35_dep": 20.0,
    "kg_siklik_ev": 50.0, "kg_siklik_dep": 50.0,
    "toplam_mac_ort_ev": 2.5, "toplam_mac_ort_dep": 2.5,
    "lehine_1y_ev": 0.7, "lehine_1y_dep": 0.7,
    "lehine_2y_ev": 0.8, "lehine_2y_dep": 0.8,
    "lehine_mac_ev": 1.5, "lehine_mac_dep": 1.5,
    "xg_perf_ev": 0.0, "xg_perf_dep": 0.0,
    "savunma_sag_ev": 0.0, "savunma_sag_dep": 0.0,
    "takim_ev": "", "takim_dep": "", "skor_ev": 0, "skor_dep": 0,
    "skor_belli": False,
    "lig_ort_ev": 0.0, "lig_ort_dep": 0.0, "lig_ort_toplam": 0.0,
    "lig_ust05": 0.0, "lig_ust15": 0.0, "lig_ust25": 0.0,
    "lig_ust35": 0.0, "lig_ust45": 0.0, "lig_ust55": 0.0,
    "lig_kg": 0.0, "lig_kg_yok": 0.0,
    "lig_ilk_gol_ev": 0.0, "lig_ilk_gol_dep": 0.0,
    "clean_sheets_ev": 0.0, "clean_sheets_dep": 0.0,
    "team_scored_ev": 0.0, "team_scored_dep": 0.0,
    "team_scored_2_ev": 0.0, "team_scored_2_dep": 0.0,
    "scored_both_halves_ev": 0.0, "scored_both_halves_dep": 0.0,
    "goal_both_halves_ev": 0.0, "goal_both_halves_dep": 0.0,
    "win_over15_ev": 0.0, "win_over15_dep": 0.0,
    "lose_over15_ev": 0.0, "lose_over15_dep": 0.0,
    "win_1h_ev": 0.0, "win_1h_dep": 0.0,
    "draw_ht_ev": 0.0, "draw_ht_dep": 0.0,
    "lose_1h_ev": 0.0, "lose_1h_dep": 0.0,
    "btts_1h_ev": 0.0, "btts_1h_dep": 0.0,
    "btts_2h_ev": 0.0, "btts_2h_dep": 0.0,
    "btts_over15_ev": 0.0, "btts_over15_dep": 0.0,
    "btts_over25_ev": 0.0, "btts_over25_dep": 0.0,
    "win_btts_ev": 0.0, "win_btts_dep": 0.0,
    "draw_btts_ev": 0.0, "draw_btts_dep": 0.0,
    "lose_btts_ev": 0.0, "lose_btts_dep": 0.0,
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
    "puan_ev": 0, "puan_dep": 0,
    "form_str_ev": "", "form_str_dep": "",
    "form_puan_ev": 0.0, "form_puan_dep": 0.0,
    "format": "bilinmiyor",
}

# ==========================================
# SABİTLER
# ==========================================
MAX_GOL = 8
BELIRSIZLIK = 0.20

# ==========================================
# SESSION STATE
# ==========================================
if "sayfa" not in st.session_state: st.session_state.sayfa = "giris"
if "form_verileri" not in st.session_state: st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
if "form_version" not in st.session_state: st.session_state.form_version = 0
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
    if "genel_1x2" not in d: return False
    if not isinstance(d.get("genel_1x2"), dict): return False
    if "tuttu" not in d["genel_1x2"]: return False
    return True


def genel_istatistik(gecmis):
    ist = {"1x2": {"tam": 0, "yakin": 0, "yanlis": 0}, "cifte": {"tam": 0, "yakin": 0, "yanlis": 0},
           "gol": {"tam": 0, "yakin": 0, "yanlis": 0}, "kg": {"tam": 0, "yakin": 0, "yanlis": 0}}
    for g in gecmis:
        if not kayit_yeni_format_mi(g): continue
        d = g["dogruluk"]
        for key in ["genel_1x2", "genel_cifte", "genel_gol", "genel_kg"]:
            kisa = key.replace("genel_", "")
            try:
                durum = d[key].get("durum", None); tuttu = d[key].get("tuttu", None)
                if durum == "tam": ist[kisa]["tam"] += 1
                elif durum == "yakin": ist[kisa]["yakin"] += 1
                elif durum == "yanlis": ist[kisa]["yanlis"] += 1
                elif tuttu is True: ist[kisa]["tam"] += 1
                elif tuttu is False: ist[kisa]["yanlis"] += 1
            except (KeyError, TypeError): continue
    return ist


def oneri_istatistik(gecmis):
    ist = {"1x2": {"tam": 0, "yakin": 0, "yanlis": 0}, "cifte": {"tam": 0, "yakin": 0, "yanlis": 0},
           "gol": {"tam": 0, "yakin": 0, "yanlis": 0}, "kg": {"tam": 0, "yakin": 0, "yanlis": 0}}
    for g in gecmis:
        if not kayit_yeni_format_mi(g): continue
        d = g["dogruluk"]
        for key in ["oneri_1x2", "oneri_cifte", "oneri_gol", "oneri_kg"]:
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
# SPORTYTRADER FORMAT ÇIKARICI
# ==========================================
def _cift_tab(etiket, blok):
    pattern = r'([\d.,]+)%?\s*\t\s*' + re.escape(etiket) + r'\s*\t\s*([\d.,]+)%?'
    m = re.search(pattern, blok, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError:
            pass
    pattern2 = r'([\d.,]+)%?\s{1,4}' + re.escape(etiket) + r'\s{1,4}([\d.,]+)%?'
    m = re.search(pattern2, blok, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError:
            pass
    return None, None


def _sira_bul(metin, takim_adi):
    if not takim_adi:
        return None, None
    pattern = (
        r'(?:^|\n)\s*(\d{1,2})\s*\r?\n\s*'
        + re.escape(takim_adi) + r'\s*\r?\n\s*'
        + re.escape(takim_adi) + r'\s*\r?\n'
        r'\s*(\d+)\s*\t'
    )
    m = re.search(pattern, metin, re.MULTILINE)
    if m:
        try:
            sira = int(m.group(1))
            if 1 <= sira <= 30:
                devam = metin[m.end()-1:]
                m_puan = re.match(r'[\s\S]{0,80}?\r?\n\s*(\d{1,2})\s*\r?\n', devam)
                puan = int(m_puan.group(1)) if m_puan else 0
                return sira, puan
        except (ValueError, AttributeError):
            pass
    pattern2 = (
        r'(?:^|\n)\s*(\d{1,2})\s*\r?\n\s*\r?\n\s*'
        + re.escape(takim_adi) + r'\s*\r?\n\s*'
        + re.escape(takim_adi)
    )
    m = re.search(pattern2, metin, re.MULTILINE)
    if m:
        try:
            sira = int(m.group(1))
            if 1 <= sira <= 30:
                return sira, 0
        except ValueError:
            pass
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
    else:
        veri["skor_belli"] = False

    takim_ev = veri.get("takim_ev", "")
    takim_dep = veri.get("takim_dep", "")

    # MAIN STATS
    idx = metin.find("Main Stats")
    if idx != -1:
        blok = metin[idx:idx+1000]

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

        v1, v2 = _cift_tab("Scored in both halves", blok)
        if v1 is not None: veri["scored_both_halves_ev"] = v1; veri["scored_both_halves_dep"] = v2

        v1, v2 = _cift_tab("Goal in both halves", blok)
        if v1 is not None: veri["goal_both_halves_ev"] = v1; veri["goal_both_halves_dep"] = v2

    # WIN DRAW LOSE
    idx = metin.find("Win Draw Lose")
    if idx != -1:
        blok = metin[idx:idx+1200]

        v1, v2 = _cift_tab("Win and Over 1.5 goals", blok)
        if v1 is not None: veri["win_over15_ev"] = v1; veri["win_over15_dep"] = v2

        v1, v2 = _cift_tab("Lose and Over 1.5 goals", blok)
        if v1 is not None: veri["lose_over15_ev"] = v1; veri["lose_over15_dep"] = v2

        v1, v2 = _cift_tab("Team win first half", blok)
        if v1 is not None: veri["win_1h_ev"] = v1; veri["win_1h_dep"] = v2

        v1, v2 = _cift_tab("Team draw at half time", blok)
        if v1 is not None: veri["draw_ht_ev"] = v1; veri["draw_ht_dep"] = v2

        v1, v2 = _cift_tab("Team lost first half", blok)
        if v1 is not None: veri["lose_1h_ev"] = v1; veri["lose_1h_dep"] = v2

        # Win/Draw/Lose ana satırları — satır başından
        for etiket, key_ev, key_dep in [
            ("Win", "galibiyet_ev", "galibiyet_dep"),
            ("Draw", "beraberlik_ev", "beraberlik_dep"),
            ("Lose", "maglubiyet_ev", "maglubiyet_dep"),
        ]:
            pattern = r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*' + etiket + r'\s*\t\s*([\d.,]+)%'
            mm = re.search(pattern, blok, re.MULTILINE)
            if mm:
                try:
                    veri[key_ev] = float(mm.group(1).replace(",", "."))
                    veri[key_dep] = float(mm.group(2).replace(",", "."))
                except ValueError:
                    pass

    # BOTH TEAMS TO SCORE
    idx = metin.find("Both Teams to Score")
    if idx != -1:
        blok = metin[idx:idx+1200]

        v1, v2 = _cift_tab("BTTS in first-half", blok)
        if v1 is not None: veri["btts_1h_ev"] = v1; veri["btts_1h_dep"] = v2

        v1, v2 = _cift_tab("BBTS in second-half", blok)
        if v1 is not None: veri["btts_2h_ev"] = v1; veri["btts_2h_dep"] = v2

        v1, v2 = _cift_tab("BBTS and Over 1.5", blok)
        if v1 is not None: veri["btts_over15_ev"] = v1; veri["btts_over15_dep"] = v2

        v1, v2 = _cift_tab("BBTS and Over 2.5", blok)
        if v1 is not None: veri["btts_over25_ev"] = v1; veri["btts_over25_dep"] = v2

        v1, v2 = _cift_tab("Win and BTTS", blok)
        if v1 is not None: veri["win_btts_ev"] = v1; veri["win_btts_dep"] = v2

        v1, v2 = _cift_tab("Draw and BTTS", blok)
        if v1 is not None: veri["draw_btts_ev"] = v1; veri["draw_btts_dep"] = v2

        v1, v2 = _cift_tab("Lose and BTTS", blok)
        if v1 is not None: veri["lose_btts_ev"] = v1; veri["lose_btts_dep"] = v2

        m = re.search(r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*Both Teams to Score\s*\t\s*([\d.,]+)%', blok, re.MULTILINE)
        if m:
            try:
                veri["kg_siklik_ev"] = float(m.group(1).replace(",", "."))
                veri["kg_siklik_dep"] = float(m.group(2).replace(",", "."))
                veri["kg_oran"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2
            except ValueError: pass

    # MATCH TOTAL GOALS
    idx = metin.find("Match Total Goals")
    if idx != -1:
        blok = metin[idx:idx+1200]

        v1, v2 = _cift_tab("Match total goals 0 or 1", blok)
        if v1 is not None: veri["tg_01_ev"] = v1; veri["tg_01_dep"] = v2

        v1, v2 = _cift_tab("Match total goals 2 or 3", blok)
        if v1 is not None: veri["tg_23_ev"] = v1; veri["tg_23_dep"] = v2

        v1, v2 = _cift_tab("Match total goals 4+", blok)
        if v1 is not None: veri["tg_4p_ev"] = v1; veri["tg_4p_dep"] = v2

        v1, v2 = _cift_tab("Match total goals 0", blok)
        if v1 is not None: veri["tg_0_ev"] = v1; veri["tg_0_dep"] = v2

        v1, v2 = _cift_tab("Match total goals 1", blok)
        if v1 is not None: veri["tg_1_ev"] = v1; veri["tg_1_dep"] = v2

        v1, v2 = _cift_tab("Match total goals 2", blok)
        if v1 is not None: veri["tg_2_ev"] = v1; veri["tg_2_dep"] = v2

        v1, v2 = _cift_tab("Match total goals 3", blok)
        if v1 is not None: veri["tg_3_ev"] = v1; veri["tg_3_dep"] = v2

        if veri.get("tg_4_ev", 0) == 0 and veri.get("tg_4p_ev", 0) > 0:
            veri["tg_4_ev"] = veri["tg_4p_ev"]
            veri["tg_4_dep"] = veri["tg_4p_dep"]

    # OVER UNDER GOALS
    idx = metin.find("Over Under Goals")
    if idx != -1:
        blok = metin[idx:idx+1200]

        v1, v2 = _cift_tab("Over 0.5 goals at half-time", blok)
        if v1 is not None: veri["ht_ust05_ev"] = v1; veri["ht_ust05_dep"] = v2

        v1, v2 = _cift_tab("Over 1.5 goals at half-time", blok)
        if v1 is not None: veri["ht_ust15_ev"] = v1; veri["ht_ust15_dep"] = v2

        v1, v2 = _cift_tab("Over 2.5 goals at half-time", blok)
        if v1 is not None: veri["ht_ust25_ev"] = v1; veri["ht_ust25_dep"] = v2

        v1, v2 = _cift_tab("Over 1.5 goals", blok)
        if v1 is not None: veri["ust15_ev"] = v1; veri["ust15_dep"] = v2

        v1, v2 = _cift_tab("Over 2.5 goals", blok)
        if v1 is not None: veri["ust25_ev"] = v1; veri["ust25_dep"] = v2

        v1, v2 = _cift_tab("Over 3.5 goals", blok)
        if v1 is not None: veri["ust35_ev"] = v1; veri["ust35_dep"] = v2

    # HALF TIME - FULL TIME
    idx = metin.find("Half Time-Full Time")
    if idx != -1:
        blok = metin[idx:idx+1500]

        for etiket, key in [
            ("Win HT - Win FT", "wht_wft"),
            ("Win HT - Draw FT", "wht_dft"),
            ("Win HT - Lose FT", "wht_lft"),
            ("Draw HT - Win FT", "dht_wft"),
            ("Draw HT - Draw FT", "dht_dft"),
            ("Draw HT - Lose FT", "dht_lft"),
            ("Lose HT - Win FT", "lht_wft"),
            ("Lose HT - Draw FT", "lht_dft"),
            ("Lose HT - Lose FT", "lht_lft"),
        ]:
            v1, v2 = _cift_tab(etiket, blok)
            if v1 is not None:
                veri[key + "_ev"] = v1
                veri[key + "_dep"] = v2

    # SIRALAMA
    if takim_ev:
        s, p = _sira_bul(metin, takim_ev)
        if s is not None:
            veri["siralama_ev"] = s
            if p: veri["puan_ev"] = p
    if takim_dep:
        s, p = _sira_bul(metin, takim_dep)
        if s is not None:
            veri["siralama_dep"] = s
            if p: veri["puan_dep"] = p

    if veri.get("siralama_ev", 0) == 0: okunamayanlar.append("Sıralama (Ev)")
    if veri.get("siralama_dep", 0) == 0: okunamayanlar.append("Sıralama (Dep)")

    # FORM
    m = re.search(
        r'\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\nForm\s*\t?\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])',
        metin
    )
    if m:
        form_ev = m.group(1) + m.group(2) + m.group(3) + m.group(4) + m.group(5)
        form_dep = m.group(6) + m.group(7) + m.group(8) + m.group(9) + m.group(10)
        veri["form_str_ev"] = form_ev
        veri["form_str_dep"] = form_dep
        def _form_puan(s):
            return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1) * 3
        veri["form_puan_ev"] = _form_puan(form_ev)
        veri["form_puan_dep"] = _form_puan(form_dep)

    # TÜRETİLMİŞ DEĞERLER
    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) +
                                  veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
        veri["lig_ort_ev"] = veri.get("atilan_ev", 0)
        veri["lig_ort_dep"] = veri.get("atilan_dep", 0)

    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2

    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2

    if veri.get("form_puan_ev", 0) > 0:
        veri["ppg_ev"] = veri["form_puan_ev"]
    if veri.get("form_puan_dep", 0) > 0:
        veri["mpg_dep"] = veri["form_puan_dep"]

    veri["format"] = "sportytrader"
    return veri, okunamayanlar


def metinden_veri_cikar(metin):
    metin_ori = metin
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
# POISSON & LAMBDA
# ==========================================
def poisson_pmf(k, lam):
    if lam <= 0: return 1.0 if k == 0 else 0.0
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)


def poisson_random(lam):
    if lam <= 0: return 0
    L = math.exp(-lam); k = 0; p = 1.0
    while True:
        k += 1; p *= random.random()
        if p <= L: return k - 1


def poisson_matris(lam_ev, lam_dep, max_gol=MAX_GOL):
    return [[poisson_pmf(i, lam_ev) * poisson_pmf(j, lam_dep) for j in range(max_gol)] for i in range(max_gol)]


def hesapla_lambda(v):
    atilan_e = v.get("atilan_ev", 0.0)
    yenen_e = v.get("yenen_ev", 0.0)
    atilan_d = v.get("atilan_dep", 0.0)
    yenen_d = v.get("yenen_dep", 0.0)

    xg_e = v.get("xg_ev", 0.0)
    xg_d = v.get("xg_dep", 0.0)

    if xg_e > 0:
        hucum_ev_baz = (xg_e * 0.70) + (atilan_e * 0.30)
    else:
        hucum_ev_baz = atilan_e if atilan_e > 0 else 1.2

    if xg_d > 0:
        hucum_dep_baz = (xg_d * 0.70) + (atilan_d * 0.30)
    else:
        hucum_dep_baz = atilan_d if atilan_d > 0 else 1.0

    savunma_dep_zaaf = yenen_d if yenen_d > 0 else 1.2
    savunma_ev_zaaf = yenen_e if yenen_e > 0 else 1.0

    lam_ev_ham = (hucum_ev_baz * 0.60) + (savunma_dep_zaaf * 0.40)
    lam_dep_ham = (hucum_dep_baz * 0.60) + (savunma_ev_zaaf * 0.40)

    EV_ETKISI = 1.05
    DEP_ETKISI = 0.95

    form_ev = clamp(1 + (v.get("ppg_ev", 1.5) - 1.5) / 15, 0.85, 1.15)
    form_dep = clamp(1 + (v.get("mpg_dep", 1.5) - 1.5) / 15, 0.85, 1.15)

    cs_ev = v.get("clean_sheets_ev", 0.0)
    cs_dep = v.get("clean_sheets_dep", 0.0)

    def clean_sheet_freni(cs_orani):
        if cs_orani >= 40.0:
            return max(0.40, 1.0 - (cs_orani / 100.0 * 0.75))
        return 1.0 - (cs_orani / 250.0) if cs_orani > 0 else 1.0

    dep_freni = clean_sheet_freni(cs_ev)
    ev_freni = clean_sheet_freni(cs_dep)

    sira_e = v.get("siralama_ev", 10)
    sira_d = v.get("siralama_dep", 10)
    dominasyon_bonus_ev = 1.0
    if 1 <= sira_e <= 5 and sira_d >= 10:
        dominasyon_bonus_ev = 1.25

    lam_ev = lam_ev_ham * EV_ETKISI * form_ev * ev_freni * dominasyon_bonus_ev
    lam_dep = lam_dep_ham * DEP_ETKISI * form_dep * dep_freni

    if lam_ev > 2.50: lam_ev = 2.50 + (lam_ev - 2.50) * 0.5
    if lam_dep > 2.50: lam_dep = 2.50 + (lam_dep - 2.50) * 0.5

    lam_ev = clamp(lam_ev, 0.05, 4.5)
    lam_dep = clamp(lam_dep, 0.05, 4.5)

    guven = 0.80
    return lam_ev, lam_dep, guven


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


def veri_yeterli_mi(v):
    onemli = [v["atilan_ev"], v["atilan_dep"], v["yenen_ev"], v["yenen_dep"]]
    return sum(1 for x in onemli if x > 0) >= 2


def mac_ici_sok(lam_ev, lam_dep):
    if random.random() < 0.03:
        if random.random() < 0.5: lam_ev *= 0.70
        else: lam_dep *= 0.70
    return lam_ev, lam_dep


def monte_carlo_simulasyon(lam_ev_base, lam_dep_base, n=MONTE_CARLO_N):
    sayac = {"1": 0, "X": 0, "2": 0, "ust25": 0, "kg_var": 0}
    for _ in range(n):
        sapma_ev = random.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        sapma_dep = random.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        lam_ev = lam_ev_base * sapma_ev
        lam_dep = lam_dep_base * sapma_dep
        lam_ev, lam_dep = mac_ici_sok(lam_ev, lam_dep)
        ev_gol = min(MAX_GOL - 1, poisson_random(lam_ev))
        dep_gol = min(MAX_GOL - 1, poisson_random(lam_dep))
        if ev_gol > dep_gol: sayac["1"] += 1
        elif ev_gol == dep_gol: sayac["X"] += 1
        else: sayac["2"] += 1
        if ev_gol + dep_gol > 2.5: sayac["ust25"] += 1
        if ev_gol > 0 and dep_gol > 0: sayac["kg_var"] += 1

    def yuzde(s): return s / n * 100 if n > 0 else 0
    return {"p1": yuzde(sayac["1"]), "px": yuzde(sayac["X"]), "p2": yuzde(sayac["2"]),
            "ust25": yuzde(sayac["ust25"]), "alt25": 100 - yuzde(sayac["ust25"]),
            "kg_var": yuzde(sayac["kg_var"]), "kg_yok": 100 - yuzde(sayac["kg_var"]), "n": n}


# ==========================================
# DOĞRULUK
# ==========================================
def _durum_1x2(p1, px, p2, gercek):
    olas = {"1": p1, "X": px, "2": p2}
    if gercek not in olas: return "yanlis", None
    en_y = max(olas, key=olas.get)
    if gercek == en_y: return "tam", gercek
    if olas[gercek] >= olas[en_y] - 5: return "yakin", gercek
    return "yanlis", en_y


def _durum_cifte(c1x, cx2, c12, gercek):
    olas = {"1X": c1x, "X2": cx2, "12": c12}
    en_y = max(olas, key=olas.get)
    if gercek in en_y: return "tam", en_y
    sirali = sorted(olas.items(), key=lambda x: -x[1])
    if len(sirali) >= 2:
        ik = sirali[1][0]
        if gercek in ik and olas[ik] >= olas[en_y] - 5: return "yakin", ik
    return "yanlis", en_y


def sonuc_hesapla(kayit):
    v = kayit["veri"]; analiz = kayit.get("analiz", {})
    if not v.get("skor_belli", False): return None

    skor_ev = v.get("skor_ev", 0); skor_dep = v.get("skor_dep", 0)
    if skor_ev > skor_dep: gercek_1x2 = "1"
    elif skor_ev == skor_dep: gercek_1x2 = "X"
    else: gercek_1x2 = "2"
    toplam_gol = skor_ev + skor_dep
    gercek_ust = toplam_gol > 2.5
    gercek_kg_var = (skor_ev > 0 and skor_dep > 0)

    p1 = analiz.get("p1", 0); px = analiz.get("px", 0); p2 = analiz.get("p2", 0)
    cifte_1x = p1 + px; cifte_x2 = p2 + px; cifte_12 = p1 + p2
    ust_25 = analiz.get("ust_25", 50); alt_25 = 100 - ust_25
    kg_var = analiz.get("kg_var_model", 50); kg_yok = 100 - kg_var

    genel_1x2 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])[0]
    genel_cifte = max([("1X", cifte_1x), ("X2", cifte_x2), ("12", cifte_12)], key=lambda x: x[1])[0]
    genel_gol = "Üst" if ust_25 > alt_25 else "Alt"
    genel_kg = "Var" if kg_var > kg_yok else "Yok"

    dg1, _ = _durum_1x2(p1, px, p2, gercek_1x2)
    dgc, _ = _durum_cifte(cifte_1x, cifte_x2, cifte_12, gercek_1x2)
    dgg, _ = ("tam", "Üst") if (gercek_ust and ust_25 > alt_25) or (not gercek_ust and alt_25 > ust_25) else ("yanlis", "Alt")
    dgk, _ = ("tam", "Var") if (gercek_kg_var and kg_var > kg_yok) or (not gercek_kg_var and kg_yok > kg_var) else ("yanlis", "Yok")

    oneri_1x2 = None
    if p1 >= ESIK_ORTA and p1 >= max(px, p2): oneri_1x2 = "1"
    elif px >= ESIK_ORTA and px >= max(p1, p2): oneri_1x2 = "X"
    elif p2 >= ESIK_ORTA and p2 >= max(p1, px): oneri_1x2 = "2"

    oneri_cifte = None
    if cifte_1x >= ESIK_ORTA and cifte_1x >= max(cifte_x2, cifte_12): oneri_cifte = "1X"
    elif cifte_x2 >= ESIK_ORTA and cifte_x2 >= max(cifte_1x, cifte_12): oneri_cifte = "X2"
    elif cifte_12 >= ESIK_ORTA and cifte_12 >= max(cifte_1x, cifte_x2): oneri_cifte = "12"

    oneri_gol = None
    if ust_25 >= ESIK_ORTA and ust_25 >= alt_25: oneri_gol = "Üst"
    elif alt_25 >= ESIK_ORTA and alt_25 >= ust_25: oneri_gol = "Alt"

    oneri_kg = None
    if kg_var >= ESIK_ORTA and kg_var >= kg_yok: oneri_kg = "Var"
    elif kg_yok >= ESIK_ORTA and kg_yok >= kg_var: oneri_kg = "Yok"

    if oneri_1x2 is None: d_o1 = None
    elif oneri_1x2 == gercek_1x2: d_o1 = "tam"
    else: d_o1 = "yanlis"

    if oneri_cifte is None: d_oc = None
    elif gercek_1x2 in oneri_cifte: d_oc = "tam"
    else: d_oc = "yanlis"

    if oneri_gol is None: d_og = None
    else:
        gy = "Üst" if gercek_ust else "Alt"
        d_og = "tam" if oneri_gol == gy else "yanlis"

    if oneri_kg is None: d_ok = None
    else:
        gy = "Var" if gercek_kg_var else "Yok"
        d_ok = "tam" if oneri_kg == gy else "yanlis"

    def _t(d): return None if d is None else (d == "tam")

    return {
        "genel_1x2": {"tahmin": genel_1x2, "tuttu": _t(dg1), "durum": dg1},
        "genel_cifte": {"tahmin": genel_cifte, "tuttu": _t(dgc), "durum": dgc},
        "genel_gol": {"tahmin": genel_gol, "tuttu": _t(dgg), "durum": dgg},
        "genel_kg": {"tahmin": genel_kg, "tuttu": _t(dgk), "durum": dgk},
        "oneri_1x2": {"tahmin": oneri_1x2, "tuttu": _t(d_o1), "durum": d_o1},
        "oneri_cifte": {"tahmin": oneri_cifte, "tuttu": _t(d_oc), "durum": d_oc},
        "oneri_gol": {"tahmin": oneri_gol, "tuttu": _t(d_og), "durum": d_og},
        "oneri_kg": {"tahmin": oneri_kg, "tuttu": _t(d_ok), "durum": d_ok},
        "gercek_1x2": gercek_1x2, "gercek_gol": "Üst" if gercek_ust else "Alt",
        "gercek_kg": "Var" if gercek_kg_var else "Yok",
    }


# ==========================================
# YORUM
# ==========================================
def detayli_analiz_yorumu(v):
    yorumlar = []
    ppg, mpg = v["ppg_ev"], v["mpg_dep"]
    fark = ppg - mpg
    if ppg >= 2.0 and mpg <= 1.0:
        txt = f"Ev sahibi evinde mükemmel form (**PPG {ppg:.2f}**), deplasman zayıf (**MPG {mpg:.2f}**)."
    elif fark >= 0.7: txt = f"Ev sahibi form olarak önde (**PPG {ppg:.2f}** vs **{mpg:.2f}**)."
    elif fark <= -0.7: txt = f"Deplasman form olarak önde (**MPG {mpg:.2f}** vs **{ppg:.2f}**)."
    else: txt = f"Form dengeli (**PPG {ppg:.2f}** vs **MPG {mpg:.2f}**)."
    yorumlar.append(("📈 FORM", txt))

    s_ev, s_dep = v["siralama_ev"], v["siralama_dep"]
    if s_ev > 0 and s_dep > 0:
        fark_sira = s_dep - s_ev
        if fark_sira >= 8: txt = f"Ev sahibi **{s_ev}.**, deplasman **{s_dep}.** sırada. **{fark_sira} basamak** ciddi fark."
        elif fark_sira >= 3: txt = f"Ev sahibi **{s_ev}.**, deplasman **{s_dep}.** sırada. Ev sahibi üstün."
        elif fark_sira <= -8: txt = f"Deplasman **{s_dep}.**, ev sahibi **{s_ev}.** sırada. Deplasman **{abs(fark_sira)} basamak** yukarıda."
        else: txt = f"Sıralamalar yakın (Ev **{s_ev}.** / Dep **{s_dep}.**)."
        yorumlar.append(("🏆 SIRALAMA", txt))

    at_ev, at_dep = v["atilan_ev"], v["atilan_dep"]
    if at_ev - at_dep >= 0.6: txt = f"Ev sahibi maç başına **{at_ev:.1f}** gol atıyor, deplasman **{at_dep:.1f}**."
    elif at_ev - at_dep <= -0.6: txt = f"Deplasman maç başına **{at_dep:.1f}** gol atıyor, ev sahibi **{at_ev:.1f}**."
    else: txt = f"Atılan goller benzer (Ev **{at_ev:.1f}** / Dep **{at_dep:.1f}**)."
    yorumlar.append(("⚽ ATILAN GOL", txt))

    y_ev, y_dep = v["yenen_ev"], v["yenen_dep"]
    if y_dep - y_ev >= 0.7: txt = f"Ev sahibi savunması sağlam (**{y_ev:.1f}**), deplasman zayıf (**{y_dep:.1f}**)."
    elif y_dep - y_ev <= -0.7: txt = f"Deplasman savunması sağlam (**{y_dep:.1f}**), ev sahibi zayıf (**{y_ev:.1f}**)."
    else: txt = f"Savunmalar benzer (Ev **{y_ev:.1f}** / Dep **{y_dep:.1f}**)."
    yorumlar.append(("🛡️ YENEN GOL", txt))

    return yorumlar


# ==========================================
# ANALİZ
# ==========================================
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
    p1_mc = mc["p1"]; px_mc = mc["px"]; p2_mc = mc["p2"]
    ust25_mc = mc["ust25"]; kg_var_mc = mc["kg_var"]

    lig_ust25 = v.get("lig_ust25", 0.0)
    lig_kg = v.get("lig_kg", 0.0)

    p1 = (p1_po * 0.60) + (p1_mc * 0.40)
    px = (px_po * 0.60) + (px_mc * 0.40)
    p2 = (p2_po * 0.60) + (p2_mc * 0.40)
    t = p1 + px + p2
    if t > 0: p1, px, p2 = (p1 / t) * 100, (px / t) * 100, (p2 / t) * 100

    if lig_ust25 > 0:
        ust_25 = (ust25_po * 0.50) + (lig_ust25 * 0.20) + (ust25_mc * 0.30)
    else:
        ust_25 = (ust25_po * 0.60) + (ust25_mc * 0.40)

    if lig_kg > 0:
        kg_var_model = (kg_var_po * 0.40) + (lig_kg * 0.35) + (kg_var_mc * 0.25)
    else:
        kg_var_model = (kg_var_po * 0.60) + (kg_var_mc * 0.40)

    toplam_beklenen_gol = lam_ev + lam_dep

    if toplam_beklenen_gol < 1.80:
        baski_faktoru = (1.80 - toplam_beklenen_gol) / 1.80
        ust_25 = max(10.0, ust_25 * (1.0 - baski_faktoru * 0.8))
        kg_var_model = max(15.0, kg_var_model * (1.0 - baski_faktoru * 0.9))

    cs_ev = v.get("clean_sheets_ev", 0.0)
    cs_dep = v.get("clean_sheets_dep", 0.0)

    if cs_ev >= 50.0 and lam_dep < 1.0:
        kg_var_model *= 0.80
    if cs_dep >= 50.0 and lam_ev < 1.0:
        kg_var_model *= 0.80

    kg_yok_model = 100.0 - kg_var_model

    if kg_yok_model > 68.0 and p1 > 55.0 and lam_ev >= 1.70:
        ust_25 = min(68.0, ust_25 * 1.35)

    alt_25 = 100.0 - ust_25

    cifte_1x = p1 + px
    cifte_x2 = p2 + px
    cifte_12 = p1 + p2

    tahmini_gol = lam_ev + lam_dep
    en_olasi = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    en_guvenli = max([("1X", cifte_1x), ("X2", cifte_x2), ("12", cifte_12)], key=lambda x: x[1])
    en_olasi_gol = "Üst" if ust_25 > alt_25 else "Alt"
    en_olasi_kg = "Var" if kg_var_model > kg_yok_model else "Yok"

    return {
        "lam_ev": lam_ev, "lam_dep": lam_dep, "guven": guven, "matris": matris, "olas": olas,
        "p1": p1, "px": px, "p2": p2, "cifte_1x": cifte_1x, "cifte_x2": cifte_x2, "cifte_12": cifte_12,
        "tahmini_gol": tahmini_gol, "ust_25": ust_25, "alt_25": alt_25,
        "kg_var_model": kg_var_model, "kg_yok_model": kg_yok_model, "kg_ort": kg_var_model,
        "en_olasi": en_olasi, "en_guvenli": en_guvenli,
        "en_olasi_gol": en_olasi_gol, "en_olasi_kg": en_olasi_kg,
        "p1_po": p1_po, "px_po": px_po, "p2_po": p2_po, "ust25_po": ust25_po, "kg_var_po": kg_var_po,
        "p1_lig": 0, "px_lig": 0, "p2_lig": 0,
        "ust25_lig": lig_ust25, "kg_var_lig": lig_kg,
        "p1_mc": p1_mc, "px_mc": px_mc, "p2_mc": p2_mc, "ust25_mc": ust25_mc, "kg_var_mc": kg_var_mc,
        "mc_n": mc["n"]
    }


def kayit_olustur(v, a):
    return {"veri": copy.deepcopy(v), "analiz": {
        "p1": a["p1"], "px": a["px"], "p2": a["p2"],
        "tahmini_gol": a["tahmini_gol"], "kg_var_model": a["kg_var_model"], "ust_25": a["ust_25"],
        "en_olasi_1x2": a["en_olasi"][0], "en_guvenli_cifte": a["en_guvenli"][0],
        "en_olasi_gol": a["en_olasi_gol"], "en_olasi_kg": a["en_olasi_kg"]}}
    # ==========================================
# OKUNAN VERİLER PANELİ
# ==========================================
def okunan_veriler_paneli(v):
    format_tip = v.get("format", "bilinmiyor")

    if format_tip == "sportytrader":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{v.get('takim_ev', 'Ev')}**")
            st.markdown(f"- Atılan: **{v.get('atilan_ev', 0):.2f}**")
            st.markdown(f"- Yenen: **{v.get('yenen_ev', 0):.2f}**")
            st.markdown(f"- Clean sheets: **{v.get('clean_sheets_ev', 0):.1f}%**")
            st.markdown(f"- Team scored: **{v.get('team_scored_ev', 0):.1f}%**")
            st.markdown(f"- Galibiyet: **{v.get('galibiyet_ev', 0):.1f}%**")
            st.markdown(f"- Beraberlik: **{v.get('beraberlik_ev', 0):.1f}%**")
            st.markdown(f"- Mağlubiyet: **{v.get('maglubiyet_ev', 0):.1f}%**")
            st.markdown(f"- KG Var: **{v.get('kg_siklik_ev', 0):.1f}%**")
            st.markdown(f"- Üst 2.5: **{v.get('ust25_ev', 0):.1f}%**")
            st.markdown(f"- Form: **{v.get('form_str_ev', '')}**")
            st.markdown(f"- Sıralama: **{v.get('siralama_ev', 0)}**")
            st.markdown(f"- Puan: **{v.get('puan_ev', 0)}**")
        with c2:
            st.markdown(f"**{v.get('takim_dep', 'Dep')}**")
            st.markdown(f"- Atılan: **{v.get('atilan_dep', 0):.2f}**")
            st.markdown(f"- Yenen: **{v.get('yenen_dep', 0):.2f}**")
            st.markdown(f"- Clean sheets: **{v.get('clean_sheets_dep', 0):.1f}%**")
            st.markdown(f"- Team scored: **{v.get('team_scored_dep', 0):.1f}%**")
            st.markdown(f"- Galibiyet: **{v.get('galibiyet_dep', 0):.1f}%**")
            st.markdown(f"- Beraberlik: **{v.get('beraberlik_dep', 0):.1f}%**")
            st.markdown(f"- Mağlubiyet: **{v.get('maglubiyet_dep', 0):.1f}%**")
            st.markdown(f"- KG Var: **{v.get('kg_siklik_dep', 0):.1f}%**")
            st.markdown(f"- Üst 2.5: **{v.get('ust25_dep', 0):.1f}%**")
            st.markdown(f"- Form: **{v.get('form_str_dep', '')}**")
            st.markdown(f"- Sıralama: **{v.get('siralama_dep', 0)}**")
            st.markdown(f"- Puan: **{v.get('puan_dep', 0)}**")


# ==========================================
# SAYFA 1: GİRİŞ
# ==========================================
if st.session_state.sayfa == "giris":
    st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>İstatistik metnini kopyala → yapıştır → analiz et.</p>", unsafe_allow_html=True)
    st.markdown("### 📋 İstatistik Metnini Yapıştır")

    yapistir_metni = st.text_area("Yapıştırma alanı", height=280, key="yapistir_input", label_visibility="collapsed", placeholder="İstatistik metnini buraya yapıştır.")
    st.divider()

    col_bt1, col_bt2, col_bt3 = st.columns([2, 1, 1])
    with col_bt1:
        analiz_btn = st.button("🚀 ANALİZ ET", use_container_width=True, type="primary")
    with col_bt2:
        gecmis_btn = st.button("📊 Geçmiş", use_container_width=True)
    with col_bt3:
        gelecek_btn = st.button("🔮 Gelecek", use_container_width=True)

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
    oneri_ist = oneri_istatistik(gecmis); genel_ist = genel_istatistik(gecmis)
    toplam = len(gecmis)

    if toplam == 0:
        st.info("ℹ️ Henüz kayıtlı maç yok.")
    else:
        st.markdown("### 🎯 ÖNERİ İSTATİSTİKLERİ")
        col_1, col_2 = st.columns(2)
        with col_1:
            st.markdown("**1X2**"); st.markdown(ist_skor_metni(oneri_ist["1x2"]))
            st.markdown("**Çifte Şans**"); st.markdown(ist_skor_metni(oneri_ist["cifte"]))
        with col_2:
            st.markdown("**Üst / Alt 2.5**"); st.markdown(ist_skor_metni(oneri_ist["gol"]))
            st.markdown("**KG (Var / Yok)**"); st.markdown(ist_skor_metni(oneri_ist["kg"]))
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

            col_maç, col_sil = st.columns([5, 1])
            with col_maç:
                if st.button(baslik, use_container_width=True, key=f"mac_{idx_gercek}"):
                    st.session_state.form_verileri = copy.deepcopy(v_g)
                    st.session_state.kayit_yapildi = True
                    st.session_state.gecmisten_gelindi = True
                    st.session_state.aktif_kayit_idx = idx_gercek
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

    st.divider()
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
                    if os.path.exists(GECMIS_DOSYA):
                        os.remove(GECMIS_DOSYA)
                except Exception:
                    pass
                st.session_state.silme_onay = False
                st.session_state.tek_silme_onay = None
                st.rerun()
        with c_h:
            if st.button("❌ İptal", use_container_width=True, key="sil_hepsi_iptal"):
                st.session_state.silme_onay = False
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
            st.markdown(f"**⚽ {takim_ev} vs {takim_dep}**")
            sc1, sc2, sc3, sc4 = st.columns([1, 1, 1, 1])
            with sc1:
                yeni_skor_ev = st.number_input(f"Ev", min_value=0, max_value=20, value=0, step=1, key=f"gskor_ev_{idx_gercek}")
            with sc2:
                yeni_skor_dep = st.number_input(f"Dep", min_value=0, max_value=20, value=0, step=1, key=f"gskor_dep_{idx_gercek}")
            with sc3:
                st.markdown(""); st.markdown("")
                if st.button("📥 Taşı", key=f"tası_{idx_gercek}", use_container_width=True, type="primary"):
                    if 0 <= idx_gercek < len(st.session_state.gelecek_analizler):
                        st.session_state.gelecek_analizler[idx_gercek]["veri"]["skor_ev"] = yeni_skor_ev
                        st.session_state.gelecek_analizler[idx_gercek]["veri"]["skor_dep"] = yeni_skor_dep
                        st.session_state.gelecek_analizler[idx_gercek]["veri"]["skor_belli"] = True
                        d = sonuc_hesapla(st.session_state.gelecek_analizler[idx_gercek])
                        if d: st.session_state.gelecek_analizler[idx_gercek]["dogruluk"] = d
                        st.session_state.gecmis_analizler.append(st.session_state.gelecek_analizler[idx_gercek])
                        st.session_state.gelecek_analizler.pop(idx_gercek)
                        gecmis_kaydet(st.session_state.gecmis_analizler)
                        gelecek_kaydet(st.session_state.gelecek_analizler)
                    st.rerun()
            with sc4:
                st.markdown(""); st.markdown("")
                if st.button("🗑️", key=f"silg_{idx_gercek}", use_container_width=True):
                    if st.session_state.tek_silme_gelecek == idx_gercek:
                        st.session_state.tek_silme_gelecek = None
                    else:
                        st.session_state.tek_silme_gelecek = idx_gercek
                    st.rerun()

            if st.session_state.tek_silme_gelecek == idx_gercek:
                st.warning(f"⚠️ Silinsin mi?")
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
            st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="g_geri"):
        st.session_state.sayfa = "giris"
        st.session_state.tek_silme_gelecek = None
        st.rerun()


# ==========================================
# ANALİZ SONUÇ
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)

    p1 = a["p1"]; px = a["px"]; p2 = a["p2"]
    cifte_1x = a["cifte_1x"]; cifte_x2 = a["cifte_x2"]; cifte_12 = a["cifte_12"]
    tahmini_gol = a["tahmini_gol"]
    ust_25 = a["ust_25"]; alt_25 = a["alt_25"]
    kg_var_model = a["kg_var_model"]; kg_yok_model = a["kg_yok_model"]

    takim_ev = v.get("takim_ev", "") or "Ev Sahibi"
    takim_dep = v.get("takim_dep", "") or "Deplasman"
    skor_belli = v.get("skor_belli", False)
    skor_ev = v.get("skor_ev", 0); skor_dep = v.get("skor_dep", 0)

    st.markdown(f"<h1>🎯 {takim_ev} vs {takim_dep}</h1>", unsafe_allow_html=True)

    if skor_belli:
        st.markdown(f"<p style='text-align:center;'><b>Sonuç: {skor_ev} - {skor_dep}</b></p>", unsafe_allow_html=True)

    with st.expander("📋 Okunan Tüm Veriler", expanded=False):
        okunan_veriler_paneli(v)

    if skor_belli:
        d = sonuc_hesapla({"veri": v, "analiz": a})
        with st.expander("✅ Tahmin Doğruluğu", expanded=True):
            st.markdown("**🎯 Öneri Tahminleri (%55+)**")
            c1, c2, c3, c4 = st.columns(4)
            for col, key in zip([c1, c2, c3, c4], ["oneri_1x2", "oneri_cifte", "oneri_gol", "oneri_kg"]):
                o = d[key]
                etiket = {"oneri_1x2": "1X2", "oneri_cifte": "Çifte", "oneri_gol": "Gol", "oneri_kg": "KG"}[key]
                with col:
                    if o["tuttu"] is None:
                        st.markdown(f"⚫ **{etiket}**"); st.markdown("Öneri yok")
                    else:
                        ikon = "✅" if o["tuttu"] else "❌"
                        st.markdown(f"{ikon} **{etiket}**"); st.markdown(f"{o['tahmin']}")
            st.divider()
            st.markdown("**📊 Genel Tahminler**")
            c1, c2, c3, c4 = st.columns(4)
            for col, key in zip([c1, c2, c3, c4], ["genel_1x2", "genel_cifte", "genel_gol", "genel_kg"]):
                o = d[key]
                etiket = {"genel_1x2": "1X2", "genel_cifte": "Çifte", "genel_gol": "Gol", "genel_kg": "KG"}[key]
                with col:
                    ikon = "✅" if o["tuttu"] else "❌"
                    st.markdown(f"{ikon} **{etiket}**"); st.markdown(f"{o['tahmin']}")
    else:
        d = None

    with st.expander("🔍 Geniş Kapsamlı Analiz", expanded=True):
        for baslik, metin in detayli_analiz_yorumu(v):
            st.markdown(f"**{baslik}**"); st.markdown(metin); st.markdown("")

    with st.expander("🎲 Monte Carlo", expanded=False):
        st.markdown(f"**{a['mc_n']} deneme** • Belirsizlik ±%{BELIRSIZLIK*100:.0f}")
        c1, c2, c3 = st.columns(3)
        c1.metric("1", f"%{a['p1_mc']:.1f}")
        c2.metric("X", f"%{a['px_mc']:.1f}")
        c3.metric("2", f"%{a['p2_mc']:.1f}")
        c4, c5 = st.columns(2)
        c4.metric("Üst 2.5", f"%{a['ust25_mc']:.1f}")
        c5.metric("Alt 2.5", f"%{100 - a['ust25_mc']:.1f}")
        c6, c7 = st.columns(2)
        c6.metric("KG Var", f"%{a['kg_var_mc']:.1f}")
        c7.metric("KG Yok", f"%{100 - a['kg_var_mc']:.1f}")

    st.divider()
    st.markdown("## 🏆 FİNAL ÖNERİ")

    with st.expander("🔬 Kaynak Karşılaştırması", expanded=False):
        c_po, c_lg, c_mc, c_fin = st.columns(4)
        with c_po:
            st.markdown("**🤖 Poisson**")
            st.markdown(f"1: %{a['p1_po']:.1f}")
            st.markdown(f"X: %{a['px_po']:.1f}")
            st.markdown(f"2: %{a['p2_po']:.1f}")
            st.markdown(f"Üst: %{a['ust25_po']:.1f}")
            st.markdown(f"KG Var: %{a['kg_var_po']:.1f}")
        with c_lg:
            st.markdown("**📊 Lig**")
            if a['ust25_lig'] > 0:
                st.markdown(f"Üst 2.5: %{a['ust25_lig']:.1f}")
            else:
                st.markdown("Üst: —")
            if a['kg_var_lig'] > 0:
                st.markdown(f"KG Var: %{a['kg_var_lig']:.1f}")
            else:
                st.markdown("KG Var: —")
        with c_mc:
            st.markdown("**🎲 Monte Carlo**")
            st.markdown(f"1: %{a['p1_mc']:.1f}")
            st.markdown(f"X: %{a['px_mc']:.1f}")
            st.markdown(f"2: %{a['p2_mc']:.1f}")
            st.markdown(f"Üst: %{a['ust25_mc']:.1f}")
            st.markdown(f"KG Var: %{a['kg_var_mc']:.1f}")
        with c_fin:
            st.markdown("**🎯 FİNAL**")
            st.markdown(f"1: %{p1:.1f}")
            st.markdown(f"X: %{px:.1f}")
            st.markdown(f"2: %{p2:.1f}")
            st.markdown(f"Üst: %{ust_25:.1f}")
            st.markdown(f"KG Var: %{kg_var_model:.1f}")

    st.markdown("### 📊 1X2")
    en_t = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    s, e, k, m = guven_seviyesi_bul(en_t[1])
    if s in ["yuksek", "orta"]: st.success(f"{e} **{en_t[0]}** → %{en_t[1]:.1f} — {m}")
    else: st.error(f"{e} **{en_t[0]}** → %{en_t[1]:.1f} — {m}")

    st.markdown("### 🛡️ Çifte Şans")
    en_c = max([("1X", cifte_1x), ("X2", cifte_x2), ("12", cifte_12)], key=lambda x: x[1])
    s, e, k, m = guven_seviyesi_bul(en_c[1])
    if s in ["yuksek", "orta"]: st.success(f"{e} **{en_c[0]}** → %{en_c[1]:.1f} — {m}")
    else: st.error(f"{e} **{en_c[0]}** → %{en_c[1]:.1f} — {m}")

    st.markdown("### ⚽ Gol")
    en_g = max([("Üst", ust_25), ("Alt", alt_25)], key=lambda x: x[1])
    s, e, k, m = guven_seviyesi_bul(en_g[1])
    if s in ["yuksek", "orta"]: st.success(f"{e} **{en_g[0]} 2.5** → %{en_g[1]:.1f} — {m}")
    else: st.error(f"{e} **{en_g[0]} 2.5** → %{en_g[1]:.1f} — {m}")
    st.markdown(f"<small>Üst: %{ust_25:.1f} • Alt: %{alt_25:.1f}</small>", unsafe_allow_html=True)

    st.markdown("### 🤝 KG")
    en_kg = max([("Var", kg_var_model), ("Yok", kg_yok_model)], key=lambda x: x[1])
    s, e, k, m = guven_seviyesi_bul(en_kg[1])
    if s in ["yuksek", "orta"]: st.success(f"{e} **KG {en_kg[0]}** → %{en_kg[1]:.1f} — {m}")
    else: st.error(f"{e} **KG {en_kg[0]}** → %{en_kg[1]:.1f} — {m}")
    st.markdown(f"<small>Var: %{kg_var_model:.1f} • Yok: %{kg_yok_model:.1f}</small>", unsafe_allow_html=True)

    if not st.session_state.kayit_yapildi:
        yeni_kayit = kayit_olustur(v, a)
        if d is not None: yeni_kayit["dogruluk"] = d
        if skor_belli:
            st.session_state.gecmis_analizler.append(yeni_kayit)
            gecmis_kaydet(st.session_state.gecmis_analizler)
            st.success("📊 Geçmişe kaydedildi.")
        else:
            st.session_state.gelecek_analizler.append(yeni_kayit)
            gelecek_kaydet(st.session_state.gelecek_analizler)
            st.info("🔮 Gelecek Maçlar'a kaydedildi.")
        st.session_state.kayit_yapildi = True

    st.divider()
    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.sayfa = "giris"
        st.rerun()
