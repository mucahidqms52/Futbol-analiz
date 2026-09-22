import streamlit as st
import math
import copy
import re
import random
import json
import os

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

# ==========================================
# KOMPAKT CSS
# ==========================================
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
# EŞİK
# ==========================================
ESIK_YUKSEK = 65.0
ESIK_ORTA = 55.0
ESIK_BELIRSIZ = 50.0

# ==========================================
# VARSAYILAN VERİ
# ==========================================
VARSAYILAN_VERI = {
    "ppg_ev": 0.0, "mpg_dep": 0.0,
    "siralama_ev": 1, "siralama_dep": 1,
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
}

XG_PERF_MAP = {
    "Verimli Hücum": +0.5, "Üstün Performans": +0.7, "Dengeli": 0.0,
    "Düşük Performans": -0.5, "Ortalamanın üstünde": +0.3, "Zayıf": -0.3,
}

SAVUNMA_MAP = {
    "Sağlam": +0.5, "İyi": +0.3, "Orta": 0.0, "Geçirgen": -0.5, "Zayıf": -0.7,
}

EV_AVANTAJ = 1.12
DEP_DEZAVANTAJ = 0.94
MAX_GOL = 8
MONTE_CARLO_N = 5000
BELIRSIZLIK = 0.10

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
def guven_seviyesi_bul(olasilik):
    if olasilik >= ESIK_YUKSEK: return ("yuksek", "🟢", "success", "Yüksek")
    if olasilik >= ESIK_ORTA:   return ("orta", "🟡", "warning", "Orta")
    if olasilik >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "error", "Belirsiz")
    return ("cok_dusuk", "⚫", "error", "Düşük")


def kayit_yeni_format_mi(g):
    """Bu kayıt yeni doğruluk formatında mı kontrol eder."""
    if "dogruluk" not in g or not g["dogruluk"]:
        return False
    d = g["dogruluk"]
    if "genel_1x2" not in d:
        return False
    if not isinstance(d.get("genel_1x2"), dict):
        return False
    if "tuttu" not in d["genel_1x2"]:
        return False
    return True


def genel_istatistik(gecmis):
    """Tüm maçlardan genel doğruluk istatistikleri. (Eski kayıtları atlar.)"""
    ist = {
        "1x2": {"dogru": 0, "yanlis": 0},
        "cifte": {"dogru": 0, "yanlis": 0},
        "gol": {"dogru": 0, "yanlis": 0},
        "kg": {"dogru": 0, "yanlis": 0},
    }
    for g in gecmis:
        if not kayit_yeni_format_mi(g):
            continue
        d = g["dogruluk"]
        for key in ["genel_1x2", "genel_cifte", "genel_gol", "genel_kg"]:
            kisa = key.replace("genel_", "")
            try:
                if d[key]["tuttu"] is True: ist[kisa]["dogru"] += 1
                elif d[key]["tuttu"] is False: ist[kisa]["yanlis"] += 1
            except (KeyError, TypeError):
                continue
    return ist


def oneri_istatistik(gecmis):
    """Sadece önerilerden (%55+) doğruluk istatistikleri. (Eski kayıtları atlar.)"""
    ist = {
        "1x2": {"dogru": 0, "yanlis": 0},
        "cifte": {"dogru": 0, "yanlis": 0},
        "gol": {"dogru": 0, "yanlis": 0},
        "kg": {"dogru": 0, "yanlis": 0},
    }
    for g in gecmis:
        if not kayit_yeni_format_mi(g):
            continue
        d = g["dogruluk"]
        for key in ["oneri_1x2", "oneri_cifte", "oneri_gol", "oneri_kg"]:
            kisa = key.replace("oneri_", "")
            try:
                if d[key]["tuttu"] is True: ist[kisa]["dogru"] += 1
                elif d[key]["tuttu"] is False: ist[kisa]["yanlis"] += 1
            except (KeyError, TypeError):
                continue
    return ist


# ==========================================
# MANUEL ALANLAR
# ==========================================
MANUEL_ALANLAR = {
    "Sıralama": [("siralama_ev", "Ev Sıralaması", "int", 1), ("siralama_dep", "Dep Sıralaması", "int", 1)],
    "Takım isimleri (Ev)": [("takim_ev", "Ev Takım Adı", "str", "")],
    "Takım isimleri (Dep)": [("takim_dep", "Dep Takım Adı", "str", "")],
    "PPG (Ev Form)": [("ppg_ev", "PPG (Ev)", "float", 0.0)],
    "MPG (Dep Form)": [("mpg_dep", "MPG (Dep)", "float", 0.0)],
    "Reaksiyon Gücü": [("reaksiyon_ev", "Reaksiyon % (Ev)", "float", 50.0), ("reaksiyon_dep", "Reaksiyon % (Dep)", "float", 50.0)],
    "Hücum Hakimiyeti": [("hucum_hakimiyeti_ev", "Hücum Hakimiyeti % (Ev)", "float", 50.0), ("hucum_hakimiyeti_dep", "Hücum Hakimiyeti % (Dep)", "float", 50.0)],
    "Agresiflik (Şut/Maç)": [("agresiflik_ev", "Agresiflik (Ev)", "float", 8.0), ("agresiflik_dep", "Agresiflik (Dep)", "float", 8.0)],
    "İsabet (Doğruluk)": [("isabet_ev", "İsabet % (Ev)", "float", 40.0), ("isabet_dep", "İsabet % (Dep)", "float", 40.0)],
    "Hava Topu (Ortalar)": [("hava_topu_ev", "Hava Topu (Ev)", "float", 10.0), ("hava_topu_dep", "Hava Topu (Dep)", "float", 10.0)],
    "xG": [("xg_ev", "xG (Ev)", "float", 0.0), ("xg_dep", "xG (Dep)", "float", 0.0)],
    "Atılan Gol": [("atilan_ev", "Atılan Gol (Ev)", "float", 0.0), ("atilan_dep", "Atılan Gol (Dep)", "float", 0.0)],
    "Yenen Gol": [("yenen_ev", "Yenen Gol (Ev)", "float", 0.0), ("yenen_dep", "Yenen Gol (Dep)", "float", 0.0)],
    "Standart Sapma (SS)": [("ss_ev", "Standart Sapma (Ev)", "float", 1.0), ("ss_dep", "Standart Sapma (Dep)", "float", 1.0)],
    "Form bloğu (PPG/MPG)": [("ppg_ev", "PPG (Ev)", "float", 0.0), ("mpg_dep", "MPG (Dep)", "float", 0.0)],
}


# ==========================================
# METİNDEN VERİ ÇIKARMA
# ==========================================
def takimlari_cikar(metin):
    takim_ev = ""; takim_dep = ""
    m = re.search(r'([A-ZÇĞİÖŞÜ][\w\s\.]+?)\n\1\n\d{1,2}:\d{2}\nFT\n(\d+)\n:\n(\d+)\n([A-ZÇĞİÖŞÜ][\w\s\.]+?)\n\4', metin)
    if m: return m.group(1).strip(), m.group(4).strip(), int(m.group(2)), int(m.group(3)), True

    m = re.search(r'([A-ZÇĞİÖŞÜ][\w\s\.]+?)\n\1\n\d{1,2}:\d{2}\nFT\n(\d+)\n:\n(\d+)\n([A-ZÇĞİÖŞÜ][\w\s\.]+)', metin)
    if m: return m.group(1).strip(), m.group(4).strip(), int(m.group(2)), int(m.group(3)), True

    m = re.search(r'([A-ZÇĞİÖŞÜ][\w\s\.]+?)\n\1\nVS\n([A-ZÇĞİÖŞÜ][\w\s\.]+?)\n\2', metin)
    if m: return m.group(1).strip(), m.group(2).strip(), 0, 0, False

    m = re.search(r'FT\n(\d+)\n:\n(\d+)', metin)
    if m: return takim_ev, takim_dep, int(m.group(1)), int(m.group(2)), True

    return takim_ev, takim_dep, 0, 0, False


def etiket_to_deger(metin_blok, etiketler):
    for etiket, deger in etiketler.items():
        if etiket.lower() in metin_blok.lower(): return deger
    return 0.0


def metinden_veri_cikar(metin):
    veri = {}; okunamayanlar = []
    metin = metin.replace(",", ".")

    takim_ev, takim_dep, skor_ev, skor_dep, skor_belli = takimlari_cikar(metin)
    veri["takim_ev"] = takim_ev; veri["takim_dep"] = takim_dep
    veri["skor_ev"] = skor_ev; veri["skor_dep"] = skor_dep; veri["skor_belli"] = skor_belli

    if not takim_ev: okunamayanlar.append("Takım isimleri (Ev)")
    if not takim_dep: okunamayanlar.append("Takım isimleri (Dep)")

    idx = metin.find("Güvenilirlik ve Form")
    if idx == -1: idx = metin.find("PPG")
    if idx != -1:
        blok = metin[idx:idx+1500]
        m = re.search(r'PPG[:\s]+([\d.]+)', blok)
        if m: veri["ppg_ev"] = float(m.group(1))
        else: okunamayanlar.append("PPG (Ev Form)")

        m = re.search(r'(?:MBP|MPG)[:\s]+([\d.]+)', blok)
        if m: veri["mpg_dep"] = float(m.group(1))
        else: okunamayanlar.append("MPG (Dep Form)")

        idx_ppg = blok.find("PPG")
        if idx_ppg != -1:
            ev_blok = blok[idx_ppg:idx_ppg+600]
            m_g = re.search(r'([\d.]+)%\s*\n\s*Galibiyet', ev_blok)
            m_b = re.search(r'([\d.]+)%\s*\n\s*Beraberlik', ev_blok)
            m_m = re.search(r'([\d.]+)%\s*\n\s*Mağlubiyet', ev_blok)
            m_y = re.search(r'(?:Invencibilidade|Yenilmezlik)[:\s]+([\d.]+)%', ev_blok)
            if m_g: veri["galibiyet_ev"] = float(m_g.group(1))
            if m_b: veri["beraberlik_ev"] = float(m_b.group(1))
            if m_m: veri["maglubiyet_ev"] = float(m_m.group(1))
            if m_y: veri["yenilmezlik_ev"] = float(m_y.group(1))

            m_perf = re.search(r'xG Performance[sı]?[:\s]*\n?\s*([A-ZÇĞİÖŞÜ][\w\s]+?)(?:\n|$)', ev_blok)
            if not m_perf: m_perf = re.search(r'xG Performans[ıi]?[:\s]*\n?\s*([A-ZÇĞİÖŞÜ][\w\s]+?)(?:\n|$)', ev_blok)
            if m_perf: veri["xg_perf_ev"] = etiket_to_deger(m_perf.group(1).strip(), XG_PERF_MAP)

        idx_mbp = blok.find("MBP")
        if idx_mbp == -1: idx_mbp = blok.find("MPG")
        if idx_mbp != -1:
            dep_blok = blok[idx_mbp:idx_mbp+600]
            m_g2 = re.search(r'([\d.]+)%\s*\n\s*Galibiyet', dep_blok)
            m_b2 = re.search(r'([\d.]+)%\s*\n\s*Beraberlik', dep_blok)
            m_m2 = re.search(r'([\d.]+)%\s*\n\s*Mağlubiyet', dep_blok)
            m_y2 = re.search(r'(?:Invencibilidade|Yenilmezlik)[:\s]+([\d.]+)%', dep_blok)
            if m_g2: veri["galibiyet_dep"] = float(m_g2.group(1))
            if m_b2: veri["beraberlik_dep"] = float(m_b2.group(1))
            if m_m2: veri["maglubiyet_dep"] = float(m_m2.group(1))
            if m_y2: veri["yenilmezlik_dep"] = float(m_y2.group(1))

            m_perf2 = re.search(r'xG Performans[ıi]?[:\s]*\n?\s*([A-ZÇĞİÖŞÜ][\w\s]+?)(?:\n|$)', dep_blok)
            if m_perf2: veri["xg_perf_dep"] = etiket_to_deger(m_perf2.group(1).strip(), XG_PERF_MAP)

        idx_psy = metin.find("Psikolojik Faktör")
        if idx_psy != -1:
            psy_blok = metin[idx_psy:idx_psy+700]
            m = re.search(r'Reaksiyon Gücü\s*\t?\s*([\d.]+)%\s*\t?\s*([\d.]+)%', psy_blok)
            if m:
                veri["reaksiyon_ev"] = float(m.group(1))
                veri["reaksiyon_dep"] = float(m.group(2))
            else: okunamayanlar.append("Reaksiyon Gücü")

            m_atar = re.search(r'İlk Golü Atar\s*\t?\s*([\d.]+)%\s*\t?\s*([\d.]+)%', psy_blok)
            if m_atar:
                veri["ilk_gol_atar_ev"] = float(m_atar.group(1))
                veri["ilk_gol_atar_dep"] = float(m_atar.group(2))
            m_yer = re.search(r'İlk Golü Yer\s*\t?\s*([\d.]+)%\s*\t?\s*([\d.]+)%', psy_blok)
            if m_yer:
                veri["ilk_gol_yer_ev"] = float(m_yer.group(1))
                veri["ilk_gol_yer_dep"] = float(m_yer.group(2))
    else: okunamayanlar.append("Form bloğu (PPG/MPG)")

    # Sıralama
    idx = metin.find("Tablo Pozisyonu")
    if idx != -1:
        blok = metin[idx:idx+800]
        m = re.search(r'(\d{1,2})\s*\n\s*[A-ZÇĞİÖŞÜ][\w\s\.]+\n\s*VS\s*\n\s*[A-ZÇĞİÖŞÜ][\w\s\.]+\n\s*(\d{1,2})', blok)
        if m:
            veri["siralama_ev"] = int(m.group(1)); veri["siralama_dep"] = int(m.group(2))
        else:
            m = re.search(r'\n[A-ZÇĞİÖŞÜ][\w\s\.]+\n(\d{1,2})\n[A-ZÇĞİÖŞÜ][\w\s\.]+\nVS\n[A-ZÇĞİÖŞÜ][\w\s\.]+\n(\d{1,2})\n', blok)
            if m:
                veri["siralama_ev"] = int(m.group(1)); veri["siralama_dep"] = int(m.group(2))
            else:
                sayilar = re.findall(r'\n(\d{1,2})\n', blok)
                if len(sayilar) >= 2:
                    veri["siralama_ev"] = int(sayilar[0]); veri["siralama_dep"] = int(sayilar[1])
                else: okunamayanlar.append("Sıralama")
    else: okunamayanlar.append("Sıralama")

    idx = metin.find("Hücum Hakimiyeti")
    if idx != -1:
        blok = metin[idx:idx+300]
        yuzdeler = re.findall(r'([\d.]+)%', blok)
        if len(yuzdeler) >= 2:
            veri["hucum_hakimiyeti_ev"] = float(yuzdeler[0])
            veri["hucum_hakimiyeti_dep"] = float(yuzdeler[1])
    else: okunamayanlar.append("Hücum Hakimiyeti")

    idx = metin.find("Agresiflik")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)\s*[·•]\s*([\d.]+)', blok)
        if m:
            veri["agresiflik_ev"] = float(m.group(1))
            veri["agresiflik_dep"] = float(m.group(2))
    else: okunamayanlar.append("Agresiflik (Şut/Maç)")

    idx = metin.find("İsabet")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)%\s*[·•]\s*([\d.]+)%', blok)
        if m:
            veri["isabet_ev"] = float(m.group(1))
            veri["isabet_dep"] = float(m.group(2))
    else: okunamayanlar.append("İsabet (Doğruluk)")

    idx = metin.find("Savunma Sağlamlığı")
    if idx != -1:
        blok = metin[idx:idx+200]
        satirlar = [s.strip() for s in blok.split("\n") if s.strip()]
        savunma_degerleri = []
        for s in satirlar:
            for etiket, deger in SAVUNMA_MAP.items():
                if etiket.lower() == s.lower():
                    savunma_degerleri.append(deger); break
        if len(savunma_degerleri) >= 2:
            veri["savunma_sag_ev"] = savunma_degerleri[0]
            veri["savunma_sag_dep"] = savunma_degerleri[1]

    idx = metin.find("Hava Topu")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)\s*[·•]\s*([\d.]+)', blok)
        if m:
            veri["hava_topu_ev"] = float(m.group(1))
            veri["hava_topu_dep"] = float(m.group(2))
    else: okunamayanlar.append("Hava Topu (Ortalar)")

    idx = metin.find("Beklenen goller (maç öncesi xG)")
    if idx == -1: idx = metin.find("Beklenen goller")
    if idx != -1:
        blok = metin[idx:idx+500]
        m = re.search(r'\n([\d.]+)\n\d+\n[\w\s]+\n[×xX]\s*\n\w[\w\s]*\n([\d.]+)\n\d+', blok)
        if m:
            veri["xg_ev"] = float(m.group(1)); veri["xg_dep"] = float(m.group(2))
        else: okunamayanlar.append("xG")
    else: okunamayanlar.append("xG")

    idx = metin.find("Atılan Gol (Ort)")
    if idx == -1: idx = metin.find("Atılan Gol")
    if idx != -1:
        blok = metin[idx:idx+400]
        sayilar = re.findall(r'\n\s*([\d.]+)\s*\n\s*\d+%', blok)
        if len(sayilar) >= 2:
            veri["atilan_ev"] = float(sayilar[0]); veri["atilan_dep"] = float(sayilar[1])
        else: okunamayanlar.append("Atılan Gol")

    idx_tm = metin.find("Toplam Maç Ortalaması")
    if idx_tm == -1: idx_tm = metin.find("Toplam Maç Ort")
    if idx_tm != -1:
        blok = metin[idx_tm:idx_tm+400]
        sayilar = re.findall(r'\n\s*([\d.]+)\s*\n\s*\d+%', blok)
        if len(sayilar) >= 2:
            veri["toplam_mac_ort_ev"] = float(sayilar[0]); veri["toplam_mac_ort_dep"] = float(sayilar[1])

    idx = metin.find("Yenen Gol (Ort)")
    if idx == -1: idx = metin.find("Yenen Gol")
    if idx != -1:
        blok = metin[idx:idx+400]
        sayilar = re.findall(r'\n\s*([\d.]+)\s*\n\s*\d+%', blok)
        if len(sayilar) >= 2:
            veri["yenen_ev"] = float(sayilar[0]); veri["yenen_dep"] = float(sayilar[1])
        else: okunamayanlar.append("Yenen Gol")

    idx_lehine = metin.find("Maç başına lehine gol")
    if idx_lehine != -1:
        blok = metin[idx_lehine:idx_lehine+500]
        lehine_sayilar = re.findall(r'\n\s*(\d{1,2}\.\d)\s*\n', blok)
        if len(lehine_sayilar) >= 6:
            veri["lehine_1y_ev"] = float(lehine_sayilar[0]); veri["lehine_2y_ev"] = float(lehine_sayilar[1])
            veri["lehine_mac_ev"] = float(lehine_sayilar[2])
            veri["lehine_1y_dep"] = float(lehine_sayilar[3]); veri["lehine_2y_dep"] = float(lehine_sayilar[4])
            veri["lehine_mac_dep"] = float(lehine_sayilar[5])
        elif len(lehine_sayilar) >= 3:
            veri["lehine_mac_ev"] = float(lehine_sayilar[0]); veri["lehine_mac_dep"] = float(lehine_sayilar[2])
        elif len(lehine_sayilar) >= 2:
            veri["lehine_mac_ev"] = float(lehine_sayilar[0]); veri["lehine_mac_dep"] = float(lehine_sayilar[1])

    ss_listesi = re.findall(r'\bSS\s*\n\s*([\d.]+)', metin)
    if len(ss_listesi) >= 2:
        veri["ss_ev"] = float(ss_listesi[0]); veri["ss_dep"] = float(ss_listesi[1])
    else: okunamayanlar.append("Standart Sapma (SS)")

    idx_05 = metin.find("0.5 Üst")
    if idx_05 != -1:
        blok = metin[idx_05:idx_05+400]
        yuzdeler = re.findall(r'(\d+)%', blok)
        if len(yuzdeler) >= 2:
            veri["ust05_ev"] = float(yuzdeler[0])
            veri["ust05_dep"] = float(yuzdeler[-1]) if len(yuzdeler) >= 4 else float(yuzdeler[1])

    idx_15 = metin.find("1.5 Üst")
    if idx_15 != -1:
        blok = metin[idx_15:idx_15+400]
        yuzdeler = re.findall(r'(\d+)%', blok)
        if len(yuzdeler) >= 2:
            veri["ust15_ev"] = float(yuzdeler[0])
            veri["ust15_dep"] = float(yuzdeler[-1]) if len(yuzdeler) >= 4 else float(yuzdeler[1])

    idx_25 = metin.find("2.5 Üst")
    if idx_25 != -1:
        blok = metin[idx_25:idx_25+400]
        yuzdeler = re.findall(r'(\d+)%', blok)
        if len(yuzdeler) >= 2:
            veri["ust25_ev"] = float(yuzdeler[0])
            veri["ust25_dep"] = float(yuzdeler[-1]) if len(yuzdeler) >= 4 else float(yuzdeler[1])

    idx_35 = metin.find("3.5 Üst")
    if idx_35 != -1:
        blok = metin[idx_35:idx_35+400]
        yuzdeler = re.findall(r'(\d+)%', blok)
        if len(yuzdeler) >= 2:
            veri["ust35_ev"] = float(yuzdeler[0])
            veri["ust35_dep"] = float(yuzdeler[-1]) if len(yuzdeler) >= 4 else float(yuzdeler[1])

    idx = metin.find("KG Sıklığı")
    if idx != -1:
        blok = metin[idx:idx+500]
        yuzdeler = re.findall(r'(\d+)%', blok)
        if len(yuzdeler) >= 3:
            veri["kg_siklik_ev"] = float(yuzdeler[0]); veri["kg_oran"] = float(yuzdeler[1])
            veri["kg_siklik_dep"] = float(yuzdeler[-1])
        elif len(yuzdeler) == 2:
            veri["kg_siklik_ev"] = float(yuzdeler[0]); veri["kg_siklik_dep"] = float(yuzdeler[1])
            veri["kg_oran"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2

    return veri, okunamayanlar


# ==========================================
# İŞ MANTIĞI
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
    hucum_ev = v["xg_ev"] * 0.6 + v["atilan_ev"] * 0.4
    hucum_dep = v["xg_dep"] * 0.6 + v["atilan_dep"] * 0.4

    isabet_kat_ev = 1 + (v.get("isabet_ev", 40) - 40) / 250
    isabet_kat_dep = 1 + (v.get("isabet_dep", 40) - 40) / 250
    hak_kat_ev = 1 + (v.get("hucum_hakimiyeti_ev", 50) - 50) / 250
    hak_kat_dep = 1 + (v.get("hucum_hakimiyeti_dep", 50) - 50) / 250
    gal_kat_ev = 1 + (v.get("galibiyet_ev", 30) - 30) / 300
    gal_kat_dep = 1 + (v.get("galibiyet_dep", 30) - 30) / 300
    ilk_kat_ev = 1 + (v.get("ilk_gol_atar_ev", 40) - 40) / 400
    ilk_kat_dep = 1 + (v.get("ilk_gol_atar_dep", 40) - 40) / 400
    agres_kat_ev = 1 + (v.get("agresiflik_ev", 8) - 8) / 50
    agres_kat_dep = 1 + (v.get("agresiflik_dep", 8) - 8) / 50
    hava_kat_ev = 1 + (v.get("hava_topu_ev", 10) - 10) / 100
    hava_kat_dep = 1 + (v.get("hava_topu_dep", 10) - 10) / 100
    xgperf_kat_ev = 1 + v.get("xg_perf_ev", 0.0) * 0.10
    xgperf_kat_dep = 1 + v.get("xg_perf_dep", 0.0) * 0.10
    tm_kat_ev = 1 + (v.get("toplam_mac_ort_ev", 2.5) - 2.5) / 25
    tm_kat_dep = 1 + (v.get("toplam_mac_ort_dep", 2.5) - 2.5) / 25
    lehine_kat_ev = 1 + (v.get("lehine_mac_ev", 1.5) - 1.5) / 15
    lehine_kat_dep = 1 + (v.get("lehine_mac_dep", 1.5) - 1.5) / 15

    hucum_ev *= (isabet_kat_ev * hak_kat_ev * gal_kat_ev * ilk_kat_ev * agres_kat_ev * hava_kat_ev * xgperf_kat_ev * tm_kat_ev * lehine_kat_ev)
    hucum_dep *= (isabet_kat_dep * hak_kat_dep * gal_kat_dep * ilk_kat_dep * agres_kat_dep * hava_kat_dep * xgperf_kat_dep * tm_kat_dep * lehine_kat_dep)

    sav_ev = v["yenen_ev"]; sav_dep = v["yenen_dep"]
    sav_sag_etki_ev = 1 - v.get("savunma_sag_ev", 0.0) * 0.10
    sav_sag_etki_dep = 1 - v.get("savunma_sag_dep", 0.0) * 0.10
    hucum_dep *= sav_sag_etki_ev; hucum_ev *= sav_sag_etki_dep

    form_ev = 1 + (v["ppg_ev"] - 1.5) / 12
    form_dep = 1 + (v["mpg_dep"] - 1.5) / 12
    moral_ev = 1 + (v["reaksiyon_ev"] - 50) / 500
    moral_dep = 1 + (v["reaksiyon_dep"] - 50) / 500
    sira_ev = 1 + (10 - v["siralama_ev"]) / 150
    sira_dep = 1 + (10 - v["siralama_dep"]) / 150

    lam_ev_ham = ((hucum_ev + sav_dep) / 2) * EV_AVANTAJ * form_ev * moral_ev * sira_ev
    lam_dep_ham = ((hucum_dep + sav_ev) / 2) * DEP_DEZAVANTAJ * form_dep * moral_dep * sira_dep

    ort = (lam_ev_ham + lam_dep_ham) / 2
    guven_ev = max(0.0, min(1.0, 1 - v["ss_ev"] / 5))
    guven_dep = max(0.0, min(1.0, 1 - v["ss_dep"] / 5))

    lam_ev = lam_ev_ham * guven_ev + ort * (1 - guven_ev)
    lam_dep = lam_dep_ham * guven_dep + ort * (1 - guven_dep)

    return max(lam_ev, 0.1), max(lam_dep, 0.1), (guven_ev + guven_dep) / 2


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
    onemli_alanlar = [v["xg_ev"], v["xg_dep"], v["atilan_ev"], v["atilan_dep"], v["yenen_ev"], v["yenen_dep"]]
    return sum(1 for x in onemli_alanlar if x > 0) >= 2


def takim_form_yorumu(deger):
    if deger > 2.0: return "🟢 Güçlü form"
    if deger < 1.0: return "🔴 Zayıf form"
    return "🟡 Ortalama form"


def monte_carlo_simulasyon(lam_ev_base, lam_dep_base, n=MONTE_CARLO_N):
    sonuclar = {"1": [], "X": [], "2": [], "ust25": [], "kg_var": []}
    for _ in range(n):
        sapma_ev = random.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        sapma_dep = random.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        lam_ev = lam_ev_base * sapma_ev; lam_dep = lam_dep_base * sapma_dep
        ev_gol = min(MAX_GOL - 1, poisson_random(lam_ev))
        dep_gol = min(MAX_GOL - 1, poisson_random(lam_dep))
        if ev_gol > dep_gol: sonuclar["1"].append(1)
        elif ev_gol == dep_gol: sonuclar["X"].append(1)
        else: sonuclar["2"].append(1)
        if ev_gol + dep_gol > 2.5: sonuclar["ust25"].append(1)
        if ev_gol > 0 and dep_gol > 0: sonuclar["kg_var"].append(1)

    def hesapla_ci(veri, n):
        if not veri: return 0, 0, 0, 0
        basari = len(veri); oran = basari / n * 100
        z = 1.645; p = basari / n
        alt = (p + z*z/(2*n) - z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / (1 + z*z/n) * 100
        ust = (p + z*z/(2*n) + z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / (1 + z*z/n) * 100
        return oran, alt, ust, ust - alt

    sonuc_ci = {}
    for k in sonuclar:
        oran, alt, ust, gen = hesapla_ci(sonuclar[k], n)
        sonuc_ci[k] = {"oran": oran, "alt": alt, "ust": ust, "genislik": gen}
    return sonuc_ci


def risk_seviyesi(genislik):
    if genislik <= 4: return "🟢 Düşük"
    if genislik <= 8: return "🟡 Orta"
    return "🔴 Yüksek"


# ==========================================
# DOĞRULUK HESAPLAMA — İKİ SİSTEM
# ==========================================
def sonuc_hesapla(kayit):
    v = kayit["veri"]
    analiz = kayit.get("analiz", {})
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

    # GENEL
    genel_1x2 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])[0]
    genel_cifte = max([("1X", cifte_1x), ("X2", cifte_x2), ("12", cifte_12)], key=lambda x: x[1])[0]
    genel_gol = "Üst" if ust_25 > alt_25 else "Alt"
    genel_kg = "Var" if kg_var > kg_yok else "Yok"

    # ÖNERİ (sadece %55+)
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

    return {
        "genel_1x2": {"tahmin": genel_1x2, "tuttu": gercek_1x2 == genel_1x2},
        "genel_cifte": {"tahmin": genel_cifte, "tuttu": gercek_1x2 in genel_cifte},
        "genel_gol": {"tahmin": genel_gol, "tuttu": gercek_ust == (genel_gol == "Üst")},
        "genel_kg": {"tahmin": genel_kg, "tuttu": gercek_kg_var == (genel_kg == "Var")},
        "oneri_1x2": {"tahmin": oneri_1x2, "tuttu": None if oneri_1x2 is None else (gercek_1x2 == oneri_1x2)},
        "oneri_cifte": {"tahmin": oneri_cifte, "tuttu": None if oneri_cifte is None else (gercek_1x2 in oneri_cifte)},
        "oneri_gol": {"tahmin": oneri_gol, "tuttu": None if oneri_gol is None else (gercek_ust == (oneri_gol == "Üst"))},
        "oneri_kg": {"tahmin": oneri_kg, "tuttu": None if oneri_kg is None else (gercek_kg_var == (oneri_kg == "Var"))},
        "gercek_1x2": gercek_1x2,
        "gercek_gol": "Üst" if gercek_ust else "Alt",
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
        txt = f"Ev sahibi evinde mükemmel form (**PPG {ppg:.2f}**), deplasman deplasmanda zayıf (**MPG {mpg:.2f}**)."
    elif fark >= 0.7:
        txt = f"Ev sahibi form olarak önde (**PPG {ppg:.2f}** vs **{mpg:.2f}**)."
    elif fark <= -0.7:
        txt = f"Deplasman form olarak önde (**MPG {mpg:.2f}** vs **{ppg:.2f}**)."
    else:
        txt = f"Form dengeli (**PPG {ppg:.2f}** vs **MPG {mpg:.2f}**)."
    yorumlar.append(("📈 FORM", txt))

    s_ev, s_dep = v["siralama_ev"], v["siralama_dep"]
    fark_sira = s_dep - s_ev
    if fark_sira >= 8: txt = f"Ev sahibi **{s_ev}.**, deplasman **{s_dep}.** sırada. **{fark_sira} basamak** ciddi fark."
    elif fark_sira >= 3: txt = f"Ev sahibi **{s_ev}.**, deplasman **{s_dep}.** sırada. Ev sahibi üstün."
    elif fark_sira <= -8: txt = f"Deplasman **{s_dep}.**, ev sahibi **{s_ev}.** sırada. Deplasman **{abs(fark_sira)} basamak** yukarıda."
    elif fark_sira <= -3: txt = f"Deplasman **{s_dep}.**, ev sahibi **{s_ev}.** sırada. Deplasman biraz üstün."
    else: txt = f"Sıralamalar yakın (Ev **{s_ev}.** / Dep **{s_dep}.**)."
    yorumlar.append(("🏆 SIRALAMA", txt))

    xg_ev, xg_dep = v["xg_ev"], v["xg_dep"]
    if xg_ev - xg_dep >= 0.6: txt = f"Ev sahibi hücumda üretken (**xG {xg_ev:.2f}** vs **{xg_dep:.2f}**)."
    elif xg_ev - xg_dep <= -0.6: txt = f"Deplasman hücumda daha etkili (**xG {xg_dep:.2f}** vs **{xg_ev:.2f}**)."
    else: txt = f"xG yakın (Ev **{xg_ev:.2f}** / Dep **{xg_dep:.2f}**)."
    yorumlar.append(("🎯 HÜCUM (xG)", txt))

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

    r_ev, r_dep = v["reaksiyon_ev"], v["reaksiyon_dep"]
    if r_ev - r_dep >= 15: txt = f"Ev sahibi reaksiyon gücü yüksek (**%{r_ev:.0f}** vs **%{r_dep:.0f}**)."
    elif r_ev - r_dep <= -15: txt = f"Deplasman reaksiyon gücü yüksek (**%{r_dep:.0f}** vs **%{r_ev:.0f}**)."
    else: txt = f"Reaksiyon güçleri benzer (Ev **%{r_ev:.0f}** / Dep **%{r_dep:.0f}**)."
    yorumlar.append(("💪 REAKSİYON", txt))

    ss_ev, ss_dep = v["ss_ev"], v["ss_dep"]
    def ist(ss):
        if ss <= 0.8: return "çok istikrarlı"
        if ss <= 1.3: return "istikrarlı"
        if ss <= 2.0: return "dalgalı"
        return "çok istikrarsız"
    if abs(ss_ev - ss_dep) >= 0.5:
        if ss_ev < ss_dep: txt = f"Ev sahibi **{ist(ss_ev)}** (SS {ss_ev:.2f}), deplasman **{ist(ss_dep)}** (SS {ss_dep:.2f})."
        else: txt = f"Deplasman **{ist(ss_dep)}** (SS {ss_dep:.2f}), ev sahibi **{ist(ss_ev)}** (SS {ss_ev:.2f})."
    else: txt = f"İstikrar seviyeleri benzer (Ev **{ss_ev:.2f}** / Dep **{ss_dep:.2f}**)."
    yorumlar.append(("📊 İSTİKRAR", txt))

    return yorumlar


def analiz_hesapla(v):
    lam_ev, lam_dep, guven = hesapla_lambda(v)
    matris = poisson_matris(lam_ev, lam_dep, MAX_GOL)
    olas = matristen_olasilik(matris, MAX_GOL)
    toplam = olas["toplam"] or 1
    p1 = olas["1"] / toplam * 100; px = olas["X"] / toplam * 100; p2 = olas["2"] / toplam * 100
    cifte_1x = p1 + px; cifte_x2 = p2 + px; cifte_12 = p1 + p2
    tahmini_gol = lam_ev + lam_dep
    ust_25 = olas["ust_25"] / toplam * 100; alt_25 = 100 - ust_25
    kg_var_model = olas["kg_var"] / toplam * 100; kg_yok_model = 100 - kg_var_model
    kg_ort = (kg_var_model + v["kg_oran"]) / 2
    en_olasi = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    en_guvenli = max([("1X", cifte_1x), ("X2", cifte_x2), ("12", cifte_12)], key=lambda x: x[1])
    en_olasi_gol = "Üst" if ust_25 > alt_25 else "Alt"
    en_olasi_kg = "Var" if kg_var_model > kg_yok_model else "Yok"
    return {"lam_ev": lam_ev, "lam_dep": lam_dep, "guven": guven, "matris": matris, "olas": olas,
            "p1": p1, "px": px, "p2": p2, "cifte_1x": cifte_1x, "cifte_x2": cifte_x2, "cifte_12": cifte_12,
            "tahmini_gol": tahmini_gol, "ust_25": ust_25, "alt_25": alt_25,
            "kg_var_model": kg_var_model, "kg_yok_model": kg_yok_model, "kg_ort": kg_ort,
            "en_olasi": en_olasi, "en_guvenli": en_guvenli,
            "en_olasi_gol": en_olasi_gol, "en_olasi_kg": en_olasi_kg}


def kayit_olustur(v, a):
    return {"veri": copy.deepcopy(v), "analiz": {
        "p1": a["p1"], "px": a["px"], "p2": a["p2"],
        "tahmini_gol": a["tahmini_gol"], "kg_var_model": a["kg_var_model"], "ust_25": a["ust_25"],
        "en_olasi_1x2": a["en_olasi"][0], "en_guvenli_cifte": a["en_guvenli"][0],
        "en_olasi_gol": a["en_olasi_gol"], "en_olasi_kg": a["en_olasi_kg"]}}


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

    # Yeni format istatistikleri
    oneri_ist = oneri_istatistik(gecmis)
    genel_ist = genel_istatistik(gecmis)

    # Kayıt sayıları
    toplam = len(gecmis)
    yeni_fmt = sum(1 for g in gecmis if kayit_yeni_format_mi(g))
    eski_fmt = toplam - yeni_fmt

    if toplam == 0:
        st.info("ℹ️ Henüz kayıtlı maç yok.")
    else:
        if eski_fmt > 0:
            st.warning(f"⚠️ **{eski_fmt} eski formatta kayıt** var. İstatistiğe katılmıyor. Temizlemek istersen aşağıdaki 'Tüm Geçmişi Temizle' butonunu kullan.")

        # ÖNERİ İSTATİSTİKLERİ
        st.markdown("### 🎯 ÖNERİ İSTATİSTİKLERİ")
        st.caption(f"Sadece %{ESIK_ORTA:.0f}+ önerilerin doğruluğu — {yeni_fmt} maç sayılıyor")

        toplam_o_dogru = 0; toplam_o_yanlis = 0

        col_1, col_2 = st.columns(2)
        with col_1:
            st.markdown("**1X2**")
            d = oneri_ist["1x2"]["dogru"]; y = oneri_ist["1x2"]["yanlis"]; t = d + y
            st.markdown(f"✅ {d} / ❌ {y}" + (f" → **%{d/t*100:.0f}**" if t > 0 else " — öneri yok"))
            toplam_o_dogru += d; toplam_o_yanlis += y

            st.markdown("**Çifte Şans**")
            d = oneri_ist["cifte"]["dogru"]; y = oneri_ist["cifte"]["yanlis"]; t = d + y
            st.markdown(f"✅ {d} / ❌ {y}" + (f" → **%{d/t*100:.0f}**" if t > 0 else " — öneri yok"))
            toplam_o_dogru += d; toplam_o_yanlis += y

        with col_2:
            st.markdown("**Üst / Alt 2.5**")
            d = oneri_ist["gol"]["dogru"]; y = oneri_ist["gol"]["yanlis"]; t = d + y
            st.markdown(f"✅ {d} / ❌ {y}" + (f" → **%{d/t*100:.0f}**" if t > 0 else " — öneri yok"))
            toplam_o_dogru += d; toplam_o_yanlis += y

            st.markdown("**KG (Var / Yok)**")
            d = oneri_ist["kg"]["dogru"]; y = oneri_ist["kg"]["yanlis"]; t = d + y
            st.markdown(f"✅ {d} / ❌ {y}" + (f" → **%{d/t*100:.0f}**" if t > 0 else " — öneri yok"))
            toplam_o_dogru += d; toplam_o_yanlis += y

        st.divider()
        toplam_o = toplam_o_dogru + toplam_o_yanlis
        if toplam_o > 0:
            st.success(f"🎯 **TOPLAM ÖNERİ:** ✅ {toplam_o_dogru} / ❌ {toplam_o_yanlis} → **%{toplam_o_dogru/toplam_o*100:.0f}** (toplam {toplam_o} öneri)")

        st.divider()

        # GENEL İSTATİSTİKLER
        st.markdown("### 📊 GENEL İSTATİSTİKLER")
        st.caption("Tüm tahminlerin doğruluğu (eşik üstü + altı)")

        toplam_g_dogru = 0; toplam_g_yanlis = 0

        col_3, col_4 = st.columns(2)
        with col_3:
            st.markdown("**1X2**")
            d = genel_ist["1x2"]["dogru"]; y = genel_ist["1x2"]["yanlis"]; t = d + y
            st.markdown(f"✅ {d} / ❌ {y}" + (f" → **%{d/t*100:.0f}**" if t > 0 else ""))
            toplam_g_dogru += d; toplam_g_yanlis += y

            st.markdown("**Çifte Şans**")
            d = genel_ist["cifte"]["dogru"]; y = genel_ist["cifte"]["yanlis"]; t = d + y
            st.markdown(f"✅ {d} / ❌ {y}" + (f" → **%{d/t*100:.0f}**" if t > 0 else ""))
            toplam_g_dogru += d; toplam_g_yanlis += y

        with col_4:
            st.markdown("**Üst / Alt 2.5**")
            d = genel_ist["gol"]["dogru"]; y = genel_ist["gol"]["yanlis"]; t = d + y
            st.markdown(f"✅ {d} / ❌ {y}" + (f" → **%{d/t*100:.0f}**" if t > 0 else ""))
            toplam_g_dogru += d; toplam_g_yanlis += y

            st.markdown("**KG (Var / Yok)**")
            d = genel_ist["kg"]["dogru"]; y = genel_ist["kg"]["yanlis"]; t = d + y
            st.markdown(f"✅ {d} / ❌ {y}" + (f" → **%{d/t*100:.0f}**" if t > 0 else ""))
            toplam_g_dogru += d; toplam_g_yanlis += y

        st.divider()
        toplam_g = toplam_g_dogru + toplam_g_yanlis
        if toplam_g > 0:
            st.info(f"📊 **TOPLAM GENEL:** ✅ {toplam_g_dogru} / ❌ {toplam_g_yanlis} → **%{toplam_g_dogru/toplam_g*100:.0f}** (toplam {toplam_g} tahmin)")

        # KARŞILAŞTIRMA
        if toplam_o > 0 and toplam_g > 0:
            st.divider()
            fark = (toplam_o_dogru/toplam_o*100) - (toplam_g_dogru/toplam_g*100)
            if fark > 5:
                st.success(f"💡 **Öneriler genelden %{fark:.1f} daha başarılı!** Eşik sistemi işe yarıyor.")
            elif fark < -5:
                st.warning(f"⚠️ **Öneriler genelden %{abs(fark):.1f} daha düşük.** Eşik değeri gözden geçirilebilir.")
            else:
                st.info(f"⚖️ Öneriler genel ile benzer performansta (fark: %{fark:+.1f}).")

    st.divider()
    st.markdown(f"### ⚽ Skoru Belli Maçlar ({toplam})")

    if toplam == 0:
        st.info("ℹ️ Kayıtlı maç yok.")
    else:
        for i, g in enumerate(reversed(gecmis)):
            idx_gercek = len(gecmis) - 1 - i
            v_g = g["veri"]
            takim_ev = v_g.get("takim_ev", "Ev") or "Ev"
            takim_dep = v_g.get("takim_dep", "Dep") or "Dep"
            skor_ev = v_g.get("skor_ev", 0); skor_dep = v_g.get("skor_dep", 0)

            d = g.get("dogruluk")
            if kayit_yeni_format_mi(g):
                oneri_say = sum(1 for k in ["oneri_1x2", "oneri_cifte", "oneri_gol", "oneri_kg"] if d[k]["tuttu"] is not None)
                oneri_tutan = sum(1 for k in ["oneri_1x2", "oneri_cifte", "oneri_gol", "oneri_kg"] if d[k]["tuttu"] is True)
                baslik = f"⚽ {takim_ev} {skor_ev}-{skor_dep} {takim_dep} — Öneri: {oneri_tutan}/{oneri_say}"
            else:
                baslik = f"⚽ {takim_ev} {skor_ev}-{skor_dep} {takim_dep} (eski format)"

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
                    st.session_state.tek_silme_onay = idx_gercek
                    st.rerun()

            if st.session_state.tek_silme_onay == idx_gercek:
                st.warning(f"⚠️ **{takim_ev} vs {takim_dep}** silinsin mi?")
                col_e, col_h = st.columns(2)
                with col_e:
                    if st.button("✅ Sil", key=f"evet_{idx_gercek}", use_container_width=True, type="primary"):
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
        if st.button("🗑️ Tüm Geçmişi Temizle", use_container_width=True):
            st.session_state.silme_onay = True
            st.rerun()
    with c_geri:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary"):
            st.session_state.sayfa = "giris"
            st.rerun()

    if st.session_state.silme_onay:
        st.warning("⚠️ Tüm geçmiş silinecek. Emin misin?")
        c_e, c_h = st.columns(2)
        with c_e:
            if st.button("✅ Evet", use_container_width=True, type="primary", key="sil_hepsi"):
                st.session_state.gecmis_analizler = []
                try:
                    if os.path.exists(GECMIS_DOSYA): os.remove(GECMIS_DOSYA)
                except: pass
                st.session_state.silme_onay = False
                st.rerun()
        with c_h:
            if st.button("❌ İptal", use_container_width=True, key="iptal_hepsi"):
                st.session_state.silme_onay = False
                st.rerun()


# ==========================================
# GELECEK
# ==========================================
elif st.session_state.sayfa == "gelecek":
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    st.caption("Skor belli olmayan maçlar. Skor gir → Geçmiş'e Taşı.")
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
                    gelecek[idx_gercek]["veri"]["skor_ev"] = yeni_skor_ev
                    gelecek[idx_gercek]["veri"]["skor_dep"] = yeni_skor_dep
                    gelecek[idx_gercek]["veri"]["skor_belli"] = True
                    d = sonuc_hesapla(gelecek[idx_gercek])
                    if d: gelecek[idx_gercek]["dogruluk"] = d
                    st.session_state.gecmis_analizler.append(gelecek[idx_gercek])
                    gelecek.pop(idx_gercek)
                    gecmis_kaydet(st.session_state.gecmis_analizler)
                    gelecek_kaydet(st.session_state.gelecek_analizler)
                    st.success("✅ Geçmişe taşındı!")
                    st.rerun()
            with sc4:
                st.markdown(""); st.markdown("")
                if st.button("🗑️", key=f"silg_{idx_gercek}", use_container_width=True):
                    st.session_state.tek_silme_gelecek = idx_gercek
                    st.rerun()

            if st.session_state.tek_silme_gelecek == idx_gercek:
                st.warning(f"⚠️ Silinsin mi?")
                c_e, c_h = st.columns(2)
                with c_e:
                    if st.button("✅ Sil", key=f"evet_g_{idx_gercek}", use_container_width=True, type="primary"):
                        gelecek.pop(idx_gercek)
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
                        st.markdown(f"{'✅' if o['tuttu'] else '❌'} **{etiket}**"); st.markdown(f"{o['tahmin']}")

            st.divider()
            st.markdown("**📊 Genel Tahminler**")
            c1, c2, c3, c4 = st.columns(4)
            for col, key in zip([c1, c2, c3, c4], ["genel_1x2", "genel_cifte", "genel_gol", "genel_kg"]):
                o = d[key]
                etiket = {"genel_1x2": "1X2", "genel_cifte": "Çifte", "genel_gol": "Gol", "genel_kg": "KG"}[key]
                with col:
                    st.markdown(f"{'✅' if o['tuttu'] else '❌'} **{etiket}**"); st.markdown(f"{o['tahmin']}")
    else:
        d = None

    with st.expander("🔍 Geniş Kapsamlı Analiz", expanded=True):
        for baslik, metin in detayli_analiz_yorumu(v):
            st.markdown(f"**{baslik}**"); st.markdown(metin); st.markdown("")

    with st.expander("🎲 Monte Carlo", expanded=False):
        mc = monte_carlo_simulasyon(a["lam_ev"], a["lam_dep"], MONTE_CARLO_N)
        c1, c2, c3 = st.columns(3)
        c1.metric("1", f"%{mc['1']['oran']:.1f}")
        c2.metric("X", f"%{mc['X']['oran']:.1f}")
        c3.metric("2", f"%{mc['2']['oran']:.1f}")

    st.divider()
    st.markdown("## 🏆 FİNAL ÖNERİ")

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
    st.markdown(f"<small>Üst: %{ust_25:.1f} {guven_seviyesi_bul(ust_25)[1]} • Alt: %{alt_25:.1f} {guven_seviyesi_bul(alt_25)[1]}</small>", unsafe_allow_html=True)

    st.markdown("### 🤝 KG")
    en_kg = max([("Var", kg_var_model), ("Yok", kg_yok_model)], key=lambda x: x[1])
    s, e, k, m = guven_seviyesi_bul(en_kg[1])
    if s in ["yuksek", "orta"]: st.success(f"{e} **KG {en_kg[0]}** → %{en_kg[1]:.1f} — {m}")
    else: st.error(f"{e} **KG {en_kg[0]}** → %{en_kg[1]:.1f} — {m}")
    st.markdown(f"<small>Var: %{kg_var_model:.1f} {guven_seviyesi_bul(kg_var_model)[1]} • Yok: %{kg_yok_model:.1f} {guven_seviyesi_bul(kg_yok_model)[1]}</small>", unsafe_allow_html=True)

    if not st.session_state.kayit_yapildi:
        yeni_kayit = kayit_olustur(v, a)
        if d is not None:
            yeni_kayit["dogruluk"] = d
        if skor_belli:
            st.session_state.gecmis_analizler.append(yeni_kayit)
            st.session_state.gecmis_analizler = st.session_state.gecmis_analizler[-200:]
            gecmis_kaydet(st.session_state.gecmis_analizler)
            st.success("📊 Geçmişe kaydedildi.")
        else:
            st.session_state.gelecek_analizler.append(yeni_kayit)
            st.session_state.gelecek_analizler = st.session_state.gelecek_analizler[-200:]
            gelecek_kaydet(st.session_state.gelecek_analizler)
            st.info("🔮 Gelecek Maçlar'a kaydedildi.")
        st.session_state.kayit_yapildi = True

    st.divider()
    if st.session_state.gecmisten_gelindi:
        if st.button("⬅️ Geçmişe Dön", use_container_width=True):
            st.session_state.sayfa = "gecmis"
            st.session_state.gecmisten_gelindi = False
            st.rerun()
        st.markdown("")

    if st.session_state.gelecekten_gelindi:
        if st.button("⬅️ Geleceğe Dön", use_container_width=True):
            st.session_state.sayfa = "gelecek"
            st.session_state.gelecekten_gelindi = False
            st.rerun()
        st.markdown("")

    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.form_version += 1
        st.session_state.kayit_yapildi = False
        st.session_state.gecmisten_gelindi = False
        st.session_state.gelecekten_gelindi = False
        st.session_state.okunamayan_alanlar = []
        st.session_state.manuel_bekleyen = []
        st.session_state.sayfa = "giris"
        st.rerun()
