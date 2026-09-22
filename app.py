import streamlit as st
import math
import copy
import re
import random
import json
import os

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

# ==========================================
# KOMPAKT CSS (BAŞLIK AŞAĞI ALINDI)
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

    div[data-testid="stNumberInput"] label p {
        font-size: 0.75rem !important;
        margin: 0 !important;
    }
    div[data-testid="stNumberInput"] input {
        font-size: 0.85rem !important;
        padding: 0.15rem 0.3rem !important;
        height: 1.8rem !important;
    }
    div[data-testid="stNumberInput"] button {
        height: 1.8rem !important;
        padding: 0 !important;
        width: 1.5rem !important;
    }
    div[data-testid="stNumberInput"] > div {
        margin-bottom: 0.2rem !important;
    }

    div[data-testid="stMetric"] { padding: 0.2rem !important; }
    div[data-testid="stMetricValue"] { font-size: 1rem !important; }
    div[data-testid="stMetricLabel"] { font-size: 0.7rem !important; }
    div[data-testid="stMetricDelta"] { font-size: 0.65rem !important; }

    .stButton button {
        padding: 0.4rem 0.6rem !important;
        font-size: 0.9rem !important;
        height: 2.2rem !important;
    }

    div[data-testid="stAlert"] {
        padding: 0.3rem 0.5rem !important;
        font-size: 0.85rem !important;
    }

    details summary {
        font-size: 0.8rem !important;
        padding: 0.2rem 0.4rem !important;
    }

    textarea { font-size: 0.75rem !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# KALICI GEÇMİŞ YARDIMCILARI
# ==========================================
GECMIS_DOSYA = "gecmis.json"


def gecmis_yukle() -> list:
    try:
        if os.path.exists(GECMIS_DOSYA):
            with open(GECMIS_DOSYA, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def gecmis_kaydet(gecmis: list):
    try:
        with open(GECMIS_DOSYA, "w", encoding="utf-8") as f:
            json.dump(gecmis, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ==========================================
# EŞİK SABİTLERİ
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
    "Verimli Hücum": +0.5,
    "Üstün Performans": +0.7,
    "Dengeli": 0.0,
    "Düşük Performans": -0.5,
    "Ortalamanın üstünde": +0.3,
    "Zayıf": -0.3,
}

SAVUNMA_MAP = {
    "Sağlam": +0.5,
    "İyi": +0.3,
    "Orta": 0.0,
    "Geçirgen": -0.5,
    "Zayıf": -0.7,
}

EV_AVANTAJ = 1.12
DEP_DEZAVANTAJ = 0.94
MAX_GOL = 8

MONTE_CARLO_N = 5000
BELIRSIZLIK = 0.10

# ==========================================
# SESSION STATE
# ==========================================
if "sayfa" not in st.session_state:
    st.session_state.sayfa = "giris"
if "form_verileri" not in st.session_state:
    st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
if "form_version" not in st.session_state:
    st.session_state.form_version = 0
if "gecmis_analizler" not in st.session_state:
    st.session_state.gecmis_analizler = gecmis_yukle()
if "kayit_yapildi" not in st.session_state:
    st.session_state.kayit_yapildi = False
if "gecmisten_gelindi" not in st.session_state:
    st.session_state.gecmisten_gelindi = False
if "silme_onay" not in st.session_state:
    st.session_state.silme_onay = False
if "aktif_kayit_idx" not in st.session_state:
    st.session_state.aktif_kayit_idx = None
if "okunamayan_alanlar" not in st.session_state:
    st.session_state.okunamayan_alanlar = []
if "manuel_bekleyen" not in st.session_state:
    st.session_state.manuel_bekleyen = []
if "tek_silme_onay" not in st.session_state:
    st.session_state.tek_silme_onay = None


# ==========================================
# GÜVEN SEVİYESİ
# ==========================================
def guven_seviyesi_bul(olasilik: float) -> tuple:
    if olasilik >= ESIK_YUKSEK:
        return ("yuksek", "🟢", "success", "Yüksek")
    elif olasilik >= ESIK_ORTA:
        return ("orta", "🟡", "warning", "Orta")
    elif olasilik >= ESIK_BELIRSIZ:
        return ("belirsiz", "🔴", "error", "Belirsiz")
    else:
        return ("cok_dusuk", "⚫", "error", "Düşük")


# ==========================================
# MANUEL GİRİŞ ALANLARI
# ==========================================
MANUEL_ALANLAR = {
    "Sıralama": [
        ("siralama_ev", "Ev Sıralaması", "int", 1),
        ("siralama_dep", "Dep Sıralaması", "int", 1),
    ],
    "Takım isimleri (Ev)": [("takim_ev", "Ev Takım Adı", "str", "")],
    "Takım isimleri (Dep)": [("takim_dep", "Dep Takım Adı", "str", "")],
    "PPG (Ev Form)": [("ppg_ev", "PPG (Ev)", "float", 0.0)],
    "MPG (Dep Form)": [("mpg_dep", "MPG (Dep)", "float", 0.0)],
    "Reaksiyon Gücü": [
        ("reaksiyon_ev", "Reaksiyon % (Ev)", "float", 50.0),
        ("reaksiyon_dep", "Reaksiyon % (Dep)", "float", 50.0),
    ],
    "Hücum Hakimiyeti": [
        ("hucum_hakimiyeti_ev", "Hücum Hakimiyeti % (Ev)", "float", 50.0),
        ("hucum_hakimiyeti_dep", "Hücum Hakimiyeti % (Dep)", "float", 50.0),
    ],
    "Agresiflik (Şut/Maç)": [
        ("agresiflik_ev", "Agresiflik (Ev)", "float", 8.0),
        ("agresiflik_dep", "Agresiflik (Dep)", "float", 8.0),
    ],
    "İsabet (Doğruluk)": [
        ("isabet_ev", "İsabet % (Ev)", "float", 40.0),
        ("isabet_dep", "İsabet % (Dep)", "float", 40.0),
    ],
    "Hava Topu (Ortalar)": [
        ("hava_topu_ev", "Hava Topu (Ev)", "float", 10.0),
        ("hava_topu_dep", "Hava Topu (Dep)", "float", 10.0),
    ],
    "xG": [
        ("xg_ev", "xG (Ev)", "float", 0.0),
        ("xg_dep", "xG (Dep)", "float", 0.0),
    ],
    "Atılan Gol": [
        ("atilan_ev", "Atılan Gol (Ev)", "float", 0.0),
        ("atilan_dep", "Atılan Gol (Dep)", "float", 0.0),
    ],
    "Yenen Gol": [
        ("yenen_ev", "Yenen Gol (Ev)", "float", 0.0),
        ("yenen_dep", "Yenen Gol (Dep)", "float", 0.0),
    ],
    "Standart Sapma (SS)": [
        ("ss_ev", "Standart Sapma (Ev)", "float", 1.0),
        ("ss_dep", "Standart Sapma (Dep)", "float", 1.0),
    ],
    "Form bloğu (PPG/MPG)": [
        ("ppg_ev", "PPG (Ev)", "float", 0.0),
        ("mpg_dep", "MPG (Dep)", "float", 0.0),
    ],
}


# ==========================================
# METİNDEN VERİ ÇIKARMA
# ==========================================
def takimlari_cikar(metin: str) -> tuple:
    takim_ev = ""
    takim_dep = ""

    m = re.search(r'([A-ZÇĞİÖŞÜ][\w\s\.]+?)\n\1\n\d{1,2}:\d{2}\nFT\n(\d+)\n:\n(\d+)\n([A-ZÇĞİÖŞÜ][\w\s\.]+?)\n\4', metin)
    if m:
        return m.group(1).strip(), m.group(4).strip(), int(m.group(2)), int(m.group(3)), True

    m = re.search(r'([A-ZÇĞİÖŞÜ][\w\s\.]+?)\n\1\n\d{1,2}:\d{2}\nFT\n(\d+)\n:\n(\d+)\n([A-ZÇĞİÖŞÜ][\w\s\.]+)', metin)
    if m:
        return m.group(1).strip(), m.group(4).strip(), int(m.group(2)), int(m.group(3)), True

    m = re.search(r'([A-ZÇĞİÖŞÜ][\w\s\.]+?)\n\1\nVS\n([A-ZÇĞİÖŞÜ][\w\s\.]+?)\n\2', metin)
    if m:
        return m.group(1).strip(), m.group(2).strip(), 0, 0, False

    m = re.search(r'FT\n(\d+)\n:\n(\d+)', metin)
    if m:
        return takim_ev, takim_dep, int(m.group(1)), int(m.group(2)), True

    return takim_ev, takim_dep, 0, 0, False


def etiket_to_deger(metin_blok: str, etiketler: dict) -> float:
    for etiket, deger in etiketler.items():
        if etiket.lower() in metin_blok.lower():
            return deger
    return 0.0


def metinden_veri_cikar(metin: str) -> tuple:
    veri = {}
    okunamayanlar = []
    metin = metin.replace(",", ".")

    takim_ev, takim_dep, skor_ev, skor_dep, skor_belli = takimlari_cikar(metin)
    veri["takim_ev"] = takim_ev
    veri["takim_dep"] = takim_dep
    veri["skor_ev"] = skor_ev
    veri["skor_dep"] = skor_dep
    veri["skor_belli"] = skor_belli

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
            if not m_perf:
                m_perf = re.search(r'xG Performans[ıi]?[:\s]*\n?\s*([A-ZÇĞİÖŞÜ][\w\s]+?)(?:\n|$)', ev_blok)
            if m_perf:
                veri["xg_perf_ev"] = etiket_to_deger(m_perf.group(1).strip(), XG_PERF_MAP)

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
            if m_perf2:
                veri["xg_perf_dep"] = etiket_to_deger(m_perf2.group(1).strip(), XG_PERF_MAP)

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
    else:
        okunamayanlar.append("Form bloğu (PPG/MPG)")

    idx = metin.find("Tablo Pozisyonu")
    if idx != -1:
        blok = metin[idx:idx+500]
        m = re.search(r'(\d{1,2})\s*\n\s*\w+\s*\n\s*VS\s*\n\s*\w+\s*\n\s*(\d{1,2})', blok)
        if m:
            veri["siralama_ev"] = int(m.group(1))
            veri["siralama_dep"] = int(m.group(2))
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
                    savunma_degerleri.append(deger)
                    break
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
            veri["xg_ev"] = float(m.group(1))
            veri["xg_dep"] = float(m.group(2))
        else: okunamayanlar.append("xG")
    else: okunamayanlar.append("xG")

    idx = metin.find("Atılan Gol (Ort)")
    if idx == -1: idx = metin.find("Atılan Gol")
    if idx != -1:
        blok = metin[idx:idx+400]
        sayilar = re.findall(r'\n\s*([\d.]+)\s*\n\s*\d+%', blok)
        if len(sayilar) >= 2:
            veri["atilan_ev"] = float(sayilar[0])
            veri["atilan_dep"] = float(sayilar[1])
        else: okunamayanlar.append("Atılan Gol")

    idx_tm = metin.find("Toplam Maç Ortalaması")
    if idx_tm == -1: idx_tm = metin.find("Toplam Maç Ort")
    if idx_tm != -1:
        blok = metin[idx_tm:idx_tm+400]
        sayilar = re.findall(r'\n\s*([\d.]+)\s*\n\s*\d+%', blok)
        if len(sayilar) >= 2:
            veri["toplam_mac_ort_ev"] = float(sayilar[0])
            veri["toplam_mac_ort_dep"] = float(sayilar[1])

    idx = metin.find("Yenen Gol (Ort)")
    if idx == -1: idx = metin.find("Yenen Gol")
    if idx != -1:
        blok = metin[idx:idx+400]
        sayilar = re.findall(r'\n\s*([\d.]+)\s*\n\s*\d+%', blok)
        if len(sayilar) >= 2:
            veri["yenen_ev"] = float(sayilar[0])
            veri["yenen_dep"] = float(sayilar[1])
        else: okunamayanlar.append("Yenen Gol")

    idx_lehine = metin.find("Maç başına lehine gol")
    if idx_lehine != -1:
        blok = metin[idx_lehine:idx_lehine+500]
        lehine_sayilar = re.findall(r'\n\s*(\d{1,2}\.\d)\s*\n', blok)
        if len(lehine_sayilar) >= 6:
            veri["lehine_1y_ev"] = float(lehine_sayilar[0])
            veri["lehine_2y_ev"] = float(lehine_sayilar[1])
            veri["lehine_mac_ev"] = float(lehine_sayilar[2])
            veri["lehine_1y_dep"] = float(lehine_sayilar[3])
            veri["lehine_2y_dep"] = float(lehine_sayilar[4])
            veri["lehine_mac_dep"] = float(lehine_sayilar[5])
        elif len(lehine_sayilar) >= 3:
            veri["lehine_mac_ev"] = float(lehine_sayilar[0])
            veri["lehine_mac_dep"] = float(lehine_sayilar[2])
        elif len(lehine_sayilar) >= 2:
            veri["lehine_mac_ev"] = float(lehine_sayilar[0])
            veri["lehine_mac_dep"] = float(lehine_sayilar[1])

    ss_listesi = re.findall(r'\bSS\s*\n\s*([\d.]+)', metin)
    if len(ss_listesi) >= 2:
        veri["ss_ev"] = float(ss_listesi[0])
        veri["ss_dep"] = float(ss_listesi[1])
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
            veri["kg_siklik_ev"] = float(yuzdeler[0])
            veri["kg_oran"] = float(yuzdeler[1])
            veri["kg_siklik_dep"] = float(yuzdeler[-1])
        elif len(yuzdeler) == 2:
            veri["kg_siklik_ev"] = float(yuzdeler[0])
            veri["kg_siklik_dep"] = float(yuzdeler[1])
            veri["kg_oran"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2

    return veri, okunamayanlar


# ==========================================
# İŞ MANTIĞI
# ==========================================
def poisson_pmf(k: int, lam: float) -> float:
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)


def poisson_random(lam: float) -> int:
    if lam <= 0: return 0
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while True:
        k += 1
        p *= random.random()
        if p <= L: return k - 1


def poisson_matris(lam_ev: float, lam_dep: float, max_gol: int = MAX_GOL):
    return [
        [poisson_pmf(i, lam_ev) * poisson_pmf(j, lam_dep) for j in range(max_gol)]
        for i in range(max_gol)
    ]


def hesapla_lambda(v: dict):
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

    hucum_ev *= (isabet_kat_ev * hak_kat_ev * gal_kat_ev * ilk_kat_ev *
                 agres_kat_ev * hava_kat_ev * xgperf_kat_ev * tm_kat_ev * lehine_kat_ev)
    hucum_dep *= (isabet_kat_dep * hak_kat_dep * gal_kat_dep * ilk_kat_dep *
                  agres_kat_dep * hava_kat_dep * xgperf_kat_dep * tm_kat_dep * lehine_kat_dep)

    sav_ev = v["yenen_ev"]
    sav_dep = v["yenen_dep"]

    sav_sag_etki_ev = 1 - v.get("savunma_sag_ev", 0.0) * 0.10
    sav_sag_etki_dep = 1 - v.get("savunma_sag_dep", 0.0) * 0.10

    hucum_dep *= sav_sag_etki_ev
    hucum_ev *= sav_sag_etki_dep

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


def matristen_olasilik(matris, max_gol: int = MAX_GOL) -> dict:
    p1 = px = p2 = 0.0
    ust_05 = ust_15 = ust_25 = ust_35 = 0.0
    kg_var = 0.0
    skorlar = {}
    toplam = 0.0

    for i in range(max_gol):
        for j in range(max_gol):
            p = matris[i][j]
            toplam += p
            if i > j:    p1 += p
            elif i == j: px += p
            else:        p2 += p
            tg = i + j
            if tg > 0.5: ust_05 += p
            if tg > 1.5: ust_15 += p
            if tg > 2.5: ust_25 += p
            if tg > 3.5: ust_35 += p
            if i > 0 and j > 0: kg_var += p
            skorlar[f"{i}-{j}"] = p

    return {
        "1": p1, "X": px, "2": p2,
        "ust_05": ust_05, "ust_15": ust_15,
        "ust_25": ust_25, "ust_35": ust_35,
        "kg_var": kg_var, "skorlar": skorlar, "toplam": toplam,
    }


def veri_yeterli_mi(v: dict) -> bool:
    onemli_alanlar = [
        v["xg_ev"], v["xg_dep"],
        v["atilan_ev"], v["atilan_dep"],
        v["yenen_ev"], v["yenen_dep"],
    ]
    return sum(1 for x in onemli_alanlar if x > 0) >= 2


def takim_form_yorumu(deger: float) -> str:
    if deger > 2.0: return "🟢 Güçlü form"
    if deger < 1.0: return "🔴 Zayıf form"
    return "🟡 Ortalama form"


def monte_carlo_simulasyon(lam_ev_base, lam_dep_base, n=MONTE_CARLO_N):
    sonuclar = {"1": [], "X": [], "2": [], "ust25": [], "kg_var": []}

    for _ in range(n):
        sapma_ev = random.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        sapma_dep = random.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        lam_ev = lam_ev_base * sapma_ev
        lam_dep = lam_dep_base * sapma_dep

        ev_gol = min(MAX_GOL - 1, poisson_random(lam_ev))
        dep_gol = min(MAX_GOL - 1, poisson_random(lam_dep))

        if ev_gol > dep_gol:    sonuclar["1"].append(1)
        elif ev_gol == dep_gol: sonuclar["X"].append(1)
        else:                    sonuclar["2"].append(1)

        if ev_gol + dep_gol > 2.5: sonuclar["ust25"].append(1)
        if ev_gol > 0 and dep_gol > 0: sonuclar["kg_var"].append(1)

    def hesapla_ci(veri, n):
        if not veri: return 0, 0, 0, 0
        basari = len(veri)
        oran = basari / n * 100
        z = 1.645
        p = basari / n
        alt = (p + z*z/(2*n) - z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / (1 + z*z/n) * 100
        ust = (p + z*z/(2*n) + z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / (1 + z*z/n) * 100
        return oran, alt, ust, ust - alt

    sonuc_ci = {}
    for k in sonuclar:
        oran, alt, ust, gen = hesapla_ci(sonuclar[k], n)
        sonuc_ci[k] = {"oran": oran, "alt": alt, "ust": ust, "genislik": gen}

    return sonuc_ci


def risk_seviyesi(genislik: float) -> str:
    if genislik <= 4:   return "🟢 Düşük"
    elif genislik <= 8: return "🟡 Orta"
    else:               return "🔴 Yüksek"


def dogruluk_kontrol(skor_ev, skor_dep, tahminler: dict) -> dict:
    sonuc = {}

    if skor_ev > skor_dep:      gercek_1x2 = "1"
    elif skor_ev == skor_dep:   gercek_1x2 = "X"
    else:                        gercek_1x2 = "2"

    tahmin_1x2 = str(tahminler.get("1x2_tahmin", "")).strip()
    tahmin_1x2_norm = ""
    if "1" in tahmin_1x2 or "ev" in tahmin_1x2.lower(): tahmin_1x2_norm = "1"
    elif "x" in tahmin_1x2.lower() or "beraber" in tahmin_1x2.lower(): tahmin_1x2_norm = "X"
    elif "2" in tahmin_1x2 or "dep" in tahmin_1x2.lower(): tahmin_1x2_norm = "2"

    sonuc["1X2_gercek"] = gercek_1x2
    sonuc["1X2_tahmin"] = tahmin_1x2
    sonuc["1X2_tuttu"] = (gercek_1x2 == tahmin_1x2_norm)

    tahmin_cifte = str(tahminler.get("cifte_tahmin", "")).strip()
    sonuc["cifte_tahmin"] = tahmin_cifte
    sonuc["cifte_tuttu"] = (gercek_1x2 in tahmin_cifte)

    toplam_gol = skor_ev + skor_dep
    gercek_ust_bool = toplam_gol > 2.5

    tahmin_str = str(tahminler.get("gol_tahmin", "")).strip()
    tahmin_str_low = tahmin_str.lower()

    if "üst" in tahmin_str_low or "ust" in tahmin_str_low: tahmin_ust_bool = True
    elif "alt" in tahmin_str_low: tahmin_ust_bool = False
    else: tahmin_ust_bool = None

    sonuc["gol_gercek"] = "Üst 2.5" if gercek_ust_bool else "Alt 2.5"
    sonuc["gol_tahmin"] = tahmin_str
    sonuc["gol_tuttu"] = (tahmin_ust_bool is not None and gercek_ust_bool == tahmin_ust_bool)

    gercek_kg_var_bool = (skor_ev > 0 and skor_dep > 0)

    tahmin_kg = str(tahminler.get("kg_tahmin", "")).strip()
    tahmin_kg_low = tahmin_kg.lower()

    if "var" in tahmin_kg_low: tahmin_kg_bool = True
    elif "yok" in tahmin_kg_low: tahmin_kg_bool = False
    else: tahmin_kg_bool = None

    sonuc["kg_gercek"] = "KG Var" if gercek_kg_var_bool else "KG Yok"
    sonuc["kg_tahmin"] = tahmin_kg
    sonuc["kg_tuttu"] = (tahmin_kg_bool is not None and gercek_kg_var_bool == tahmin_kg_bool)

    tutan = sum([sonuc["1X2_tuttu"], sonuc["cifte_tuttu"], sonuc["gol_tuttu"], sonuc["kg_tuttu"]])
    sonuc["toplam_tutan"] = tutan
    sonuc["toplam_metrik"] = 4

    return sonuc


def dogruluk_hesapla_ve_guncelle(kayit: dict) -> dict:
    v = kayit["veri"]
    analiz = kayit.get("analiz", {})

    if not v.get("skor_belli", False): return None

    skor_ev = v.get("skor_ev", 0)
    skor_dep = v.get("skor_dep", 0)

    tahminler = {
        "1x2_tahmin": analiz.get("en_olasi_1x2", "1"),
        "cifte_tahmin": analiz.get("en_guvenli_cifte", "1X"),
        "gol_tahmin": analiz.get("en_olasi_gol", ""),
        "kg_tahmin": analiz.get("en_olasi_kg", ""),
    }
    return dogruluk_kontrol(skor_ev, skor_dep, tahminler)


def detayli_analiz_yorumu(v: dict):
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

    m_ev, m_dep = v.get("maglubiyet_ev", 30), v.get("maglubiyet_dep", 30)
    if m_ev > 0 or m_dep > 0:
        if m_dep >= m_ev + 15:
            txt = f"Deplasman **%{m_dep:.0f}** mağlubiyet oranıyla savunmasız (Ev: %{m_ev:.0f})."
        elif m_ev >= m_dep + 15:
            txt = f"Ev sahibi **%{m_ev:.0f}** mağlubiyet oranıyla kırılgan (Dep: %{m_dep:.0f})."
        else:
            txt = f"Mağlubiyet oranları benzer (Ev %{m_ev:.0f} / Dep %{m_dep:.0f})."
        yorumlar.append(("📉 MAĞLUBİYET", txt))

    xgperf_ev = v.get("xg_perf_ev", 0.0)
    xgperf_dep = v.get("xg_perf_dep", 0.0)
    if abs(xgperf_ev) >= 0.3 or abs(xgperf_dep) >= 0.3:
        if xgperf_ev > xgperf_dep + 0.3:
            txt = f"Ev sahibi **verimli hücum** performansı sergiliyor, deplasman daha zayıf."
        elif xgperf_dep > xgperf_ev + 0.3:
            txt = f"Deplasman **üstün hücum** performansı gösteriyor, ev sahibi daha zayıf."
        else:
            txt = f"xG performansları benzer."
        yorumlar.append(("⚡ xG PERFORMANCE", txt))

    sav_ev = v.get("savunma_sag_ev", 0.0)
    sav_dep = v.get("savunma_sag_dep", 0.0)
    if abs(sav_ev) >= 0.3 or abs(sav_dep) >= 0.3:
        ev_yorum = "Sağlam" if sav_ev > 0.3 else "Geçirgen" if sav_ev < -0.3 else "Normal"
        dep_yorum = "Sağlam" if sav_dep > 0.3 else "Geçirgen" if sav_dep < -0.3 else "Normal"
        txt = f"Ev savunması: **{ev_yorum}** | Dep savunması: **{dep_yorum}**."
        yorumlar.append(("🛡️ SAVUNMA SAĞLAMLIĞI", txt))

    s_ev, s_dep = v["siralama_ev"], v["siralama_dep"]
    fark_sira = s_dep - s_ev
    if fark_sira >= 8:
        txt = f"Ev sahibi **{s_ev}.**, deplasman **{s_dep}.** sırada. **{fark_sira} basamak** ciddi fark."
    elif fark_sira >= 3:
        txt = f"Ev sahibi **{s_ev}.**, deplasman **{s_dep}.** sırada. Ev sahibi üstün."
    elif fark_sira <= -8:
        txt = f"Deplasman **{s_dep}.**, ev sahibi **{s_ev}.** sırada. Deplasman **{abs(fark_sira)} basamak** yukarıda."
    elif fark_sira <= -3:
        txt = f"Deplasman **{s_dep}.**, ev sahibi **{s_ev}.** sırada. Deplasman biraz üstün."
    else:
        txt = f"Sıralamalar yakın (Ev **{s_ev}.** / Dep **{s_dep}.**)."
    yorumlar.append(("🏆 SIRALAMA", txt))

    xg_ev, xg_dep = v["xg_ev"], v["xg_dep"]
    fark_xg = xg_ev - xg_dep
    if fark_xg >= 0.6:
        txt = f"Ev sahibi hücumda üretken (**xG {xg_ev:.2f}** vs **{xg_dep:.2f}**)."
    elif fark_xg <= -0.6:
        txt = f"Deplasman hücumda daha etkili (**xG {xg_dep:.2f}** vs **{xg_ev:.2f}**)."
    else:
        txt = f"xG yakın (Ev **{xg_ev:.2f}** / Dep **{xg_dep:.2f}**)."
    yorumlar.append(("🎯 HÜCUM (xG)", txt))

    tm_ev = v.get("toplam_mac_ort_ev", 2.5)
    tm_dep = v.get("toplam_mac_ort_dep", 2.5)
    if abs(tm_ev - tm_dep) >= 0.5:
        if tm_ev > tm_dep:
            txt = f"Ev sahibinin maçları daha gollü (**{tm_ev:.2f}** gol/maç vs **{tm_dep:.2f}**)."
        else:
            txt = f"Deplasmanın maçları daha gollü (**{tm_dep:.2f}** gol/maç vs **{tm_ev:.2f}**)."
        yorumlar.append(("⚽ TOPLAM MAÇ ORT.", txt))

    at_ev, at_dep = v["atilan_ev"], v["atilan_dep"]
    fark_at = at_ev - at_dep
    if fark_at >= 0.6:
        txt = f"Ev sahibi maç başına **{at_ev:.1f}** gol atıyor, deplasman **{at_dep:.1f}**."
    elif fark_at <= -0.6:
        txt = f"Deplasman maç başına **{at_dep:.1f}** gol atıyor, ev sahibi **{at_ev:.1f}**."
    else:
        txt = f"Atılan goller benzer (Ev **{at_ev:.1f}** / Dep **{at_dep:.1f}**)."
    yorumlar.append(("⚽ ATILAN GOL", txt))

    y_ev_s, y_dep_s = v["yenen_ev"], v["yenen_dep"]
    fark_ys = y_dep_s - y_ev_s
    if fark_ys >= 0.7:
        txt = f"Ev sahibi savunması sağlam (**{y_ev_s:.1f}**), deplasman zayıf (**{y_dep_s:.1f}**)."
    elif fark_ys <= -0.7:
        txt = f"Deplasman savunması sağlam (**{y_dep_s:.1f}**), ev sahibi zayıf (**{y_ev_s:.1f}**)."
    else:
        txt = f"Savunmalar benzer (Ev **{y_ev_s:.1f}** / Dep **{y_dep_s:.1f}**)."
    yorumlar.append(("🛡️ YENEN GOL", txt))

    lh_1y_ev = v.get("lehine_1y_ev", 0.7)
    lh_1y_dep = v.get("lehine_1y_dep", 0.7)
    lh_2y_ev = v.get("lehine_2y_ev", 0.8)
    lh_2y_dep = v.get("lehine_2y_dep", 0.8)
    if abs(lh_1y_ev - lh_1y_dep) >= 0.2 or abs(lh_2y_ev - lh_2y_dep) >= 0.2:
        txt = (f"İlk yarı lehine gol: Ev **{lh_1y_ev:.1f}** / Dep **{lh_1y_dep:.1f}**. "
               f"İkinci yarı: Ev **{lh_2y_ev:.1f}** / Dep **{lh_2y_dep:.1f}**.")
        yorumlar.append(("⏱️ YARI BAZLI GOL", txt))

    r_ev, r_dep = v["reaksiyon_ev"], v["reaksiyon_dep"]
    fark_r = r_ev - r_dep
    if fark_r >= 15:
        txt = f"Ev sahibi reaksiyon gücü yüksek (**%{r_ev:.0f}** vs **%{r_dep:.0f}**)."
    elif fark_r <= -15:
        txt = f"Deplasman reaksiyon gücü yüksek (**%{r_dep:.0f}** vs **%{r_ev:.0f}**)."
    else:
        txt = f"Reaksiyon güçleri benzer (Ev **%{r_ev:.0f}** / Dep **%{r_dep:.0f}**)."
    yorumlar.append(("💪 REAKSİYON", txt))

    ss_ev, ss_dep = v["ss_ev"], v["ss_dep"]
    def istikrar(ss):
        if ss <= 0.8: return "çok istikrarlı"
        if ss <= 1.3: return "istikrarlı"
        if ss <= 2.0: return "dalgalı"
        return "çok istikrarsız"
    if abs(ss_ev - ss_dep) >= 0.5:
        if ss_ev < ss_dep:
            txt = f"Ev sahibi **{istikrar(ss_ev)}** (SS {ss_ev:.2f}), deplasman **{istikrar(ss_dep)}** (SS {ss_dep:.2f})."
        else:
            txt = f"Deplasman **{istikrar(ss_dep)}** (SS {ss_dep:.2f}), ev sahibi **{istikrar(ss_ev)}** (SS {ss_ev:.2f})."
    else:
        txt = f"İstikrar seviyeleri benzer (Ev **{ss_ev:.2f}** / Dep **{ss_dep:.2f}**)."
    yorumlar.append(("📊 İSTİKRAR", txt))

    u15_ev = v.get("ust15_ev", 50)
    u15_dep = v.get("ust15_dep", 50)
    u25_ev = v.get("ust25_ev", 30)
    u25_dep = v.get("ust25_dep", 30)
    if u15_ev > 0 or u15_dep > 0:
        txt = f"1.5 Üst sıklığı: Ev **%{u15_ev:.0f}** / Dep **%{u15_dep:.0f}**."
        yorumlar.append(("📈 1.5 ÜST SIKLIĞI", txt))

    if u25_ev > 0 or u25_dep > 0:
        txt = f"2.5 Üst sıklığı: Ev **%{u25_ev:.0f}** / Dep **%{u25_dep:.0f}**."
        yorumlar.append(("📈 2.5 ÜST SIKLIĞI", txt))

    return yorumlar


def analiz_hesapla(v: dict):
    lam_ev, lam_dep, guven = hesapla_lambda(v)
    matris = poisson_matris(lam_ev, lam_dep, MAX_GOL)
    olas = matristen_olasilik(matris, MAX_GOL)

    toplam = olas["toplam"] or 1
    p1 = olas["1"] / toplam * 100
    px = olas["X"] / toplam * 100
    p2 = olas["2"] / toplam * 100

    cifte_1x = p1 + px
    cifte_x2 = p2 + px
    cifte_12 = p1 + p2

    tahmini_gol = lam_ev + lam_dep
    ust_25 = olas["ust_25"] / toplam * 100
    alt_25 = 100 - ust_25

    kg_var_model = olas["kg_var"] / toplam * 100
    kg_yok_model = 100 - kg_var_model
    kg_ort = (kg_var_model + v["kg_oran"]) / 2

    en_olasi = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    en_guvenli = max([("1X", cifte_1x), ("X2", cifte_x2), ("12", cifte_12)], key=lambda x: x[1])

    en_olasi_gol = "Üst 2.5" if ust_25 > alt_25 else "Alt 2.5"
    en_olasi_kg = "KG Var" if kg_var_model > kg_yok_model else "KG Yok"

    return {
        "lam_ev": lam_ev, "lam_dep": lam_dep, "guven": guven,
        "matris": matris, "olas": olas,
        "p1": p1, "px": px, "p2": p2,
        "cifte_1x": cifte_1x, "cifte_x2": cifte_x2, "cifte_12": cifte_12,
        "tahmini_gol": tahmini_gol,
        "ust_25": ust_25, "alt_25": alt_25,
        "kg_var_model": kg_var_model, "kg_yok_model": kg_yok_model,
        "kg_ort": kg_ort,
        "en_olasi": en_olasi, "en_guvenli": en_guvenli,
        "en_olasi_gol": en_olasi_gol, "en_olasi_kg": en_olasi_kg,
    }


# ==========================================
# SAYFA 1: GİRİŞ
# ==========================================
if st.session_state.sayfa == "giris":
    st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>İstatistik metnini kopyala → yapıştır → analiz et.</p>", unsafe_allow_html=True)

    st.markdown("### 📋 İstatistik Metnini Yapıştır")

    yapistir_metni = st.text_area("Yapıştırma alanı", height=280, key="yapistir_input", label_visibility="collapsed", placeholder="İstatistik metnini buraya yapıştır.")

    st.divider()

    col_bt1, col_bt2 = st.columns([3, 1])
    with col_bt1:
        analiz_btn = st.button("🚀 ANALİZ ET", use_container_width=True, type="primary")
    with col_bt2:
        gecmis_btn = st.button("📊 Geçmiş", use_container_width=True)

    if gecmis_btn:
        st.session_state.sayfa = "gecmis"
        st.session_state.kayit_yapildi = False
        st.session_state.gecmisten_gelindi = False
        st.session_state.aktif_kayit_idx = None
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
                st.session_state.aktif_kayit_idx = None
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
# SAYFA: MANUEL GİRİŞ
# ==========================================
elif st.session_state.sayfa == "manuel_giris":
    st.markdown("<h1>📝 Eksik Alanları Doldur</h1>", unsafe_allow_html=True)
    st.warning(f"Aşağıdaki **{len(st.session_state.manuel_bekleyen)}** alan metinden çıkarılamadı. Lütfen değerleri manuel girin:")

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
            if kaydet:
                st.session_state.form_verileri.update(yeni_degerler)
            st.session_state.manuel_bekleyen = []
            st.session_state.sayfa = "sonuc"
            st.rerun()

    if st.button("⬅️ Metni Yeniden Yapıştır"):
        st.session_state.sayfa = "giris"
        st.rerun()


# ==========================================
# SAYFA GEÇMİŞ
# ==========================================
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Performans Dashboard</h1>", unsafe_allow_html=True)

    gecmis = st.session_state.gecmis_analizler

    if not gecmis:
        st.info("ℹ️ Henüz kayıtlı analiz yok.")
        if st.button("⬅️ Geri Dön", use_container_width=True, type="primary"):
            st.session_state.sayfa = "giris"
            st.rerun()
        st.stop()

    skorlu = [g for g in gecmis if g["veri"].get("skor_belli", False) and "dogruluk" in g]
    toplam = len(gecmis)
    toplam_skorlu = len(skorlu)

    if skorlu:
        tutan_1x2 = sum(1 for g in skorlu if g["dogruluk"]["1X2_tuttu"])
        tutan_cifte = sum(1 for g in skorlu if g["dogruluk"]["cifte_tuttu"])
        tutan_gol = sum(1 for g in skorlu if g["dogruluk"]["gol_tuttu"])
        tutan_kg = sum(1 for g in skorlu if g["dogruluk"]["kg_tuttu"])

        st.markdown("### 📈 Genel Doğruluk İstatistikleri")
        st.caption(f"Skor girilmiş maç sayısı: **{toplam_skorlu}/{toplam}**")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📊 Market Bazlı İsabet**")
            st.markdown(f"- **1X2:** {tutan_1x2}/{toplam_skorlu} (%{tutan_1x2/toplam_skorlu*100:.0f})")
            st.markdown(f"- **Çifte Şans:** {tutan_cifte}/{toplam_skorlu} (%{tutan_cifte/toplam_skorlu*100:.0f})")
        with c2:
            st.markdown("**📊 Diğer**")
            st.markdown(f"- **Üst/Alt 2.5:** {tutan_gol}/{toplam_skorlu} (%{tutan_gol/toplam_skorlu*100:.0f})")
            st.markdown(f"- **KG:** {tutan_kg}/{toplam_skorlu} (%{tutan_kg/toplam_skorlu*100:.0f})")

        st.divider()

        oranlar = {
            "1X2": tutan_1x2 / toplam_skorlu * 100,
            "Çifte Şans": tutan_cifte / toplam_skorlu * 100,
            "Üst/Alt 2.5": tutan_gol / toplam_skorlu * 100,
            "KG": tutan_kg / toplam_skorlu * 100,
        }
        en_iyi_market = max(oranlar.items(), key=lambda x: x[1])
        en_kotu_market = min(oranlar.items(), key=lambda x: x[1])

        st.markdown(f"🏆 **En iyi market:** {en_iyi_market[0]} (%{en_iyi_market[1]:.0f})")
        st.markdown(f"⚠️ **En kötü market:** {en_kotu_market[0]} (%{en_kotu_market[1]:.0f})")

        st.divider()

    st.markdown("### 📋 Analiz Edilen Maçlar")

    for i, g in enumerate(reversed(gecmis)):
        idx_gercek = len(gecmis) - 1 - i
        v_g = g["veri"]

        takim_ev = v_g.get("takim_ev", "Ev") or "Ev"
        takim_dep = v_g.get("takim_dep", "Dep") or "Dep"
        skor_belli = v_g.get("skor_belli", False)

        if skor_belli:
            baslik = f"⚽ {takim_ev} {v_g.get('skor_ev', 0)} - {v_g.get('skor_dep', 0)} {takim_dep}"
            if "dogruluk" in g:
                d = g["dogruluk"]
                emoji = "✅" if d["toplam_tutan"] >= 3 else "🟡" if d["toplam_tutan"] >= 2 else "❌"
                baslik = f"{emoji} {baslik} ({d['toplam_tutan']}/{d['toplam_metrik']})"
        else:
            baslik = f"⏳ {takim_ev} vs {takim_dep} (skor yok)"

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
            if st.button("🗑️", key=f"sil_{idx_gercek}", help="Bu maçı sil"):
                st.session_state.tek_silme_onay = idx_gercek
                st.rerun()

        if st.session_state.tek_silme_onay == idx_gercek:
            st.warning(f"⚠️ **{takim_ev} vs {takim_dep}** maçını silmek istediğine emin misin?")
            col_evet, col_hayir = st.columns(2)
            with col_evet:
                if st.button("✅ Evet, Sil", use_container_width=True, key=f"evet_{idx_gercek}", type="primary"):
                    st.session_state.gecmis_analizler.pop(idx_gercek)
                    gecmis_kaydet(st.session_state.gecmis_analizler)
                    st.session_state.tek_silme_onay = None
                    st.success("✅ Maç silindi!")
                    st.rerun()
            with col_hayir:
                if st.button("❌ İptal", use_container_width=True, key=f"hayir_{idx_gercek}"):
                    st.session_state.tek_silme_onay = None
                    st.rerun()

    st.divider()

    if not st.session_state.silme_onay:
        c_temizle, c_geri = st.columns(2)
        with c_temizle:
            if st.button("🗑️ Tüm Geçmişi Temizle", use_container_width=True):
                st.session_state.silme_onay = True
                st.rerun()
        with c_geri:
            if st.button("⬅️ Geri Dön", use_container_width=True, type="primary"):
                st.session_state.sayfa = "giris"
                st.rerun()
    else:
        st.warning("⚠️ **Emin misin?** Tüm geçmiş kalıcı olarak silinecek.")
        c_evet, c_hayir = st.columns(2)
        with c_evet:
            if st.button("✅ Evet, Hepsini Sil", use_container_width=True, type="primary"):
                st.session_state.gecmis_analizler = []
                try:
                    if os.path.exists(GECMIS_DOSYA):
                        os.remove(GECMIS_DOSYA)
                except Exception:
                    pass
                st.session_state.silme_onay = False
                st.rerun()
        with c_hayir:
            if st.button("❌ Hayır, İptal", use_container_width=True, key="hayir_hepsi"):
                st.session_state.silme_onay = False
                st.rerun()


# ==========================================
# SAYFA 2: ANALİZ — TÜM SEÇENEKLER
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)

    lam_ev = a["lam_ev"]; lam_dep = a["lam_dep"]; guven = a["guven"]
    matris = a["matris"]
    p1 = a["p1"]; px = a["px"]; p2 = a["p2"]
    cifte_1x = a["cifte_1x"]; cifte_x2 = a["cifte_x2"]; cifte_12 = a["cifte_12"]
    tahmini_gol = a["tahmini_gol"]
    ust_25 = a["ust_25"]; alt_25 = a["alt_25"]
    kg_var_model = a["kg_var_model"]; kg_yok_model = a["kg_yok_model"]
    kg_ort = a["kg_ort"]
    en_olasi = a["en_olasi"]; en_guvenli = a["en_guvenli"]

    takim_ev = v.get("takim_ev", "") or "Ev Sahibi"
    takim_dep = v.get("takim_dep", "") or "Deplasman"
    skor_belli = v.get("skor_belli", False)
    skor_ev = v.get("skor_ev", 0)
    skor_dep = v.get("skor_dep", 0)

    st.markdown(f"<h1>🎯 {takim_ev} vs {takim_dep}</h1>", unsafe_allow_html=True)
    if skor_belli:
        st.markdown(f"<p style='text-align:center; font-size:1.1rem;'><b>Sonuç: {skor_ev} - {skor_dep}</b></p>", unsafe_allow_html=True)

    fark = p1 - p2
    if fark > 25:       senaryo = "Ev sahibi açık ara favori görünüyor."
    elif fark > 10:     senaryo = "Ev sahibi hafif favori konumunda."
    elif fark < -25:    senaryo = "Deplasman ekibi net favori."
    elif fark < -10:    senaryo = "Deplasman hafif favori."
    else:               senaryo = "Maç oldukça dengeli, beraberlik riski yüksek."

    if not skor_belli:
        with st.expander("📝 Maç Sonucu Gir", expanded=False):
            sc1, sc2, sc3 = st.columns([1, 1, 2])
            with sc1:
                yeni_skor_ev = st.number_input(f"{takim_ev} Gol", min_value=0, max_value=20, value=0, step=1, key="skor_gir_ev")
            with sc2:
                yeni_skor_dep = st.number_input(f"{takim_dep} Gol", min_value=0, max_value=20, value=0, step=1, key="skor_gir_dep")
            with sc3:
                st.markdown("")
                st.markdown("")
                if st.button("💾 Skoru Kaydet", use_container_width=True, type="primary"):
                    st.session_state.form_verileri["skor_ev"] = yeni_skor_ev
                    st.session_state.form_verileri["skor_dep"] = yeni_skor_dep
                    st.session_state.form_verileri["skor_belli"] = True

                    if st.session_state.aktif_kayit_idx is not None:
                        idx = st.session_state.aktif_kayit_idx
                        if 0 <= idx < len(st.session_state.gecmis_analizler):
                            st.session_state.gecmis_analizler[idx]["veri"]["skor_ev"] = yeni_skor_ev
                            st.session_state.gecmis_analizler[idx]["veri"]["skor_dep"] = yeni_skor_dep
                            st.session_state.gecmis_analizler[idx]["veri"]["skor_belli"] = True
                            d = dogruluk_hesapla_ve_guncelle(st.session_state.gecmis_analizler[idx])
                            if d is not None:
                                st.session_state.gecmis_analizler[idx]["dogruluk"] = d
                            gecmis_kaydet(st.session_state.gecmis_analizler)

                    st.success("✅ Skor kaydedildi!")
                    st.rerun()

    if skor_belli:
        tahminler = {
            "1x2_tahmin": en_olasi[0],
            "cifte_tahmin": en_guvenli[0],
            "gol_tahmin": a["en_olasi_gol"],
            "kg_tahmin": a["en_olasi_kg"],
        }
        dogruluk = dogruluk_kontrol(skor_ev, skor_dep, tahminler)

        with st.expander("✅ Tahmin Doğruluğu", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                emoji = "✅" if dogruluk["1X2_tuttu"] else "❌"
                st.markdown(f"{emoji} **1X2**")
                st.markdown(f"Tahmin: {dogruluk['1X2_tahmin']}")
                st.markdown(f"Gerçek: {dogruluk['1X2_gercek']}")
            with c2:
                emoji = "✅" if dogruluk["cifte_tuttu"] else "❌"
                st.markdown(f"{emoji} **Çifte**")
                st.markdown(f"Tahmin: {dogruluk['cifte_tahmin']}")
            with c3:
                emoji = "✅" if dogruluk["gol_tuttu"] else "❌"
                st.markdown(f"{emoji} **Gol**")
                st.markdown(f"Tahmin: {dogruluk['gol_tahmin']}")
                st.markdown(f"Gerçek: {dogruluk['gol_gercek']}")
            with c4:
                emoji = "✅" if dogruluk["kg_tuttu"] else "❌"
                st.markdown(f"{emoji} **KG**")
                st.markdown(f"Tahmin: {dogruluk['kg_tahmin']}")
                st.markdown(f"Gerçek: {dogruluk['kg_gercek']}")
    else:
        dogruluk = None

    with st.expander("📋 Analizde Kullanılan Tüm Veriler", expanded=False):
        st.markdown(f"""
        **🏠 Ev:** PPG {v['ppg_ev']} | Sıra {v['siralama_ev']} | xG {v['xg_ev']} | Atılan {v['atilan_ev']} | Yenen {v['yenen_ev']}

        **✈️ Dep:** MPG {v['mpg_dep']} | Sıra {v['siralama_dep']} | xG {v['xg_dep']} | Atılan {v['atilan_dep']} | Yenen {v['yenen_dep']}
        """)

    with st.expander("🏠 Ev Sahibi Analizi", expanded=True):
        st.markdown(f"""
        - **PPG:** {v['ppg_ev']:.2f} → {takim_form_yorumu(v['ppg_ev'])}
        - **Sıralama:** {v['siralama_ev']}. sıra
        - **xG:** {v['xg_ev']} | **Atılan:** {v['atilan_ev']} | **Yenen:** {v['yenen_ev']}
        - **Reaksiyon:** %{v['reaksiyon_ev']:.0f} | **SS:** {v['ss_ev']:.2f}
        """)

    with st.expander("✈️ Deplasman Analizi", expanded=True):
        st.markdown(f"""
        - **MPG:** {v['mpg_dep']:.2f} → {takim_form_yorumu(v['mpg_dep'])}
        - **Sıralama:** {v['siralama_dep']}. sıra
        - **xG:** {v['xg_dep']} | **Atılan:** {v['atilan_dep']} | **Yenen:** {v['yenen_dep']}
        - **Reaksiyon:** %{v['reaksiyon_dep']:.0f} | **SS:** {v['ss_dep']:.2f}
        """)

    with st.expander("🔍 Geniş Kapsamlı Analiz", expanded=True):
        yorumlar = detayli_analiz_yorumu(v)
        for baslik, metin in yorumlar:
            st.markdown(f"**{baslik}**")
            st.markdown(metin)
            st.markdown("")

    with st.expander("🎲 Monte Carlo Simülasyonu", expanded=False):
        mc = monte_carlo_simulasyon(lam_ev, lam_dep, MONTE_CARLO_N)
        st.markdown("### 📊 1 - X - 2")
        c1, c2, c3 = st.columns(3)
        c1.metric("1 (Ev)", f"%{mc['1']['oran']:.1f}")
        c2.metric("X", f"%{mc['X']['oran']:.1f}")
        c3.metric("2 (Dep)", f"%{mc['2']['oran']:.1f}")
        for isim, key in [("1 (Ev)", "1"), ("X", "X"), ("2 (Dep)", "2")]:
            gen = mc[key]["genislik"]
            risk = risk_seviyesi(gen)
            st.markdown(f"**{isim}** — GA (%90): **%{mc[key]['alt']:.1f} - %{mc[key]['ust']:.1f}** → {risk}")
        st.markdown("### ⚽ Üst 2.5")
        st.markdown(f"**Üst 2.5** — %{mc['ust25']['oran']:.1f}")
        st.markdown("### 🤝 KG Var")
        st.markdown(f"**KG Var** — %{mc['kg_var']['oran']:.1f}")

    # FİNAL ÖNERİ
    st.divider()
    st.markdown("## 🏆 FİNAL ÖNERİ")
    st.caption(f"📊 Eşik: ≥%{ESIK_ORTA:.0f} önerilir | %{ESIK_BELIRSIZ:.0f}-{ESIK_ORTA:.0f} belirsiz | <%{ESIK_BELIRSIZ:.0f} gizli")

    # 1X2 TEK SONUÇ
    st.markdown("### 📊 1X2 (Tek Sonuç)")
    tek_secimler = [("1", p1), ("X", px), ("2", p2)]
    en_yuksek_tek = max(tek_secimler, key=lambda x: x[1])
    seviye_t, emoji_t, kutu_t, mesaj_t = guven_seviyesi_bul(en_yuksek_tek[1])

    if seviye_t in ["yuksek", "orta"]:
        if kutu_t == "success":
            st.success(f"{emoji_t} **{en_yuksek_tek[0]}** → %{en_yuksek_tek[1]:.1f} — {mesaj_t}")
        else:
            st.warning(f"{emoji_t} **{en_yuksek_tek[0]}** → %{en_yuksek_tek[1]:.1f} — {mesaj_t}")
    elif seviye_t == "belirsiz":
        st.error(f"{emoji_t} **{en_yuksek_tek[0]}** → %{en_yuksek_tek[1]:.1f} — {mesaj_t}")
    else:
        st.error(f"⚫ 1X2 için yeterli veri yok")

    st.markdown(f"""
    <small>
    1: %{p1:.1f} {guven_seviyesi_bul(p1)[1]} •
    X: %{px:.1f} {guven_seviyesi_bul(px)[1]} •
    2: %{p2:.1f} {guven_seviyesi_bul(p2)[1]}
    </small>
    """, unsafe_allow_html=True)

    # ÇİFTE ŞANS
    st.markdown("### 🛡️ Çifte Şans")
    cift_secimler = [("1X", cifte_1x), ("X2", cifte_x2), ("12", cifte_12)]
    en_yuksek_cift = max(cift_secimler, key=lambda x: x[1])
    seviye_c, emoji_c, kutu_c, mesaj_c = guven_seviyesi_bul(en_yuksek_cift[1])

    if seviye_c in ["yuksek", "orta"]:
        if kutu_c == "success":
            st.success(f"{emoji_c} **{en_yuksek_cift[0]}** → %{en_yuksek_cift[1]:.1f} — {mesaj_c}")
        else:
            st.warning(f"{emoji_c} **{en_yuksek_cift[0]}** → %{en_yuksek_cift[1]:.1f} — {mesaj_c}")
    elif seviye_c == "belirsiz":
        st.error(f"{emoji_c} **{en_yuksek_cift[0]}** → %{en_yuksek_cift[1]:.1f} — {mesaj_c}")
    else:
        st.error(f"⚫ Çifte Şans için yeterli veri yok")

    st.markdown(f"""
    <small>
    1X: %{cifte_1x:.1f} {guven_seviyesi_bul(cifte_1x)[1]} •
    X2: %{cifte_x2:.1f} {guven_seviyesi_bul(cifte_x2)[1]} •
    12: %{cifte_12:.1f} {guven_seviyesi_bul(cifte_12)[1]}
    </small>
    """, unsafe_allow_html=True)

    # GOL
    st.markdown("### ⚽ Gol (Üst / Alt 2.5)")
    seviye_u, emoji_u, _, mesaj_u = guven_seviyesi_bul(ust_25)
    seviye_a, emoji_a, _, mesaj_a = guven_seviyesi_bul(alt_25)

    gol_secimler = [("Üst 2.5", ust_25), ("Alt 2.5", alt_25)]
    en_yuksek_gol = max(gol_secimler, key=lambda x: x[1])
    seviye_g, emoji_g, kutu_g, mesaj_g = guven_seviyesi_bul(en_yuksek_gol[1])

    if seviye_g in ["yuksek", "orta"]:
        if kutu_g == "success":
            st.success(f"{emoji_g} **{en_yuksek_gol[0]}** → %{en_yuksek_gol[1]:.1f} — {mesaj_g}")
        else:
            st.warning(f"{emoji_g} **{en_yuksek_gol[0]}** → %{en_yuksek_gol[1]:.1f} — {mesaj_g}")
    elif seviye_g == "belirsiz":
        st.error(f"{emoji_g} **{en_yuksek_gol[0]}** → %{en_yuksek_gol[1]:.1f} — {mesaj_g}")
        st.caption(f"ℹ️ Gol tahmini belirsiz. Beklenen: {tahmini_gol:.2f}")
    else:
        st.error(f"⚫ Gol için yeterli veri yok")

    col_u, col_a = st.columns(2)
    with col_u:
        st.markdown(f"{emoji_u} **Üst 2.5**")
        st.markdown(f"**%{ust_25:.1f}** — {mesaj_u}")
    with col_a:
        st.markdown(f"{emoji_a} **Alt 2.5**")
        st.markdown(f"**%{alt_25:.1f}** — {mesaj_a}")

    # KG
    st.markdown("### 🤝 KG (Karşılıklı Gol)")
    seviye_kv, emoji_kv, _, mesaj_kv = guven_seviyesi_bul(kg_var_model)
    seviye_ky, emoji_ky, _, mesaj_ky = guven_seviyesi_bul(kg_yok_model)

    kg_secimler = [("KG Var", kg_var_model), ("KG Yok", kg_yok_model)]
    en_yuksek_kg = max(kg_secimler, key=lambda x: x[1])
    seviye_kg, emoji_kg, kutu_kg, mesaj_kg = guven_seviyesi_bul(en_yuksek_kg[1])

    if seviye_kg in ["yuksek", "orta"]:
        if kutu_kg == "success":
            st.success(f"{emoji_kg} **{en_yuksek_kg[0]}** → %{en_yuksek_kg[1]:.1f} — {mesaj_kg}")
        else:
            st.warning(f"{emoji_kg} **{en_yuksek_kg[0]}** → %{en_yuksek_kg[1]:.1f} — {mesaj_kg}")
    elif seviye_kg == "belirsiz":
        st.error(f"{emoji_kg} **{en_yuksek_kg[0]}** → %{en_yuksek_kg[1]:.1f} — {mesaj_kg}")
    else:
        st.error(f"⚫ KG için yeterli veri yok")

    col_kv, col_ky = st.columns(2)
    with col_kv:
        st.markdown(f"{emoji_kv} **KG Var**")
        st.markdown(f"**%{kg_var_model:.1f}** — {mesaj_kv}")
    with col_ky:
        st.markdown(f"{emoji_ky} **KG Yok**")
        st.markdown(f"**%{kg_yok_model:.1f}** — {mesaj_ky}")

    # ÖZET
    st.divider()
    st.markdown("### 📊 ÖZET — Güvenilir Öneriler")

    oneriler = []
    if en_yuksek_tek[1] >= ESIK_ORTA:
        oneriler.append(f"✅ **1X2:** {en_yuksek_tek[0]} (%{en_yuksek_tek[1]:.1f})")
    if en_yuksek_cift[1] >= ESIK_ORTA:
        oneriler.append(f"✅ **Çifte Şans:** {en_yuksek_cift[0]} (%{en_yuksek_cift[1]:.1f})")
    if en_yuksek_gol[1] >= ESIK_ORTA:
        oneriler.append(f"✅ **Gol:** {en_yuksek_gol[0]} (%{en_yuksek_gol[1]:.1f})")
    if en_yuksek_kg[1] >= ESIK_ORTA:
        oneriler.append(f"✅ **KG:** {en_yuksek_kg[0]} (%{en_yuksek_kg[1]:.1f})")

    if oneriler:
        for o in oneriler:
            st.markdown(o)
        st.success(f"✅ **{len(oneriler)} güvenilir öneri** bulundu.")
    else:
        st.warning("⚠️ **Bu maçta güvenilir öneri yok.**")

    # KAYIT
    if not st.session_state.kayit_yapildi:
        yeni_kayit = {
            "veri": copy.deepcopy(v),
            "analiz": {
                "p1": p1, "px": px, "p2": p2,
                "tahmini_gol": tahmini_gol,
                "kg_var_model": kg_var_model,
                "ust_25": ust_25,
                "en_olasi_1x2": en_olasi[0],
                "en_guvenli_cifte": en_guvenli[0],
                "en_olasi_gol": a["en_olasi_gol"],
                "en_olasi_kg": a["en_olasi_kg"],
            },
        }
        if dogruluk is not None:
            yeni_kayit["dogruluk"] = dogruluk

        mevcut = st.session_state.gecmis_analizler
        tekrar_mi = False
        if mevcut:
            son = mevcut[-1]
            if (son["veri"].get("takim_ev") == yeni_kayit["veri"].get("takim_ev")
                and son["veri"].get("takim_dep") == yeni_kayit["veri"].get("takim_dep")
                and son["veri"].get("skor_ev") == yeni_kayit["veri"].get("skor_ev")
                and son["veri"].get("skor_dep") == yeni_kayit["veri"].get("skor_dep")
                and abs(son["analiz"].get("p1", 0) - yeni_kayit["analiz"].get("p1", 0)) < 0.1
                and abs(son["analiz"].get("px", 0) - yeni_kayit["analiz"].get("px", 0)) < 0.1
                and abs(son["analiz"].get("p2", 0) - yeni_kayit["analiz"].get("p2", 0)) < 0.1):
                tekrar_mi = True

        if not tekrar_mi:
            st.session_state.gecmis_analizler.append(yeni_kayit)
            st.session_state.gecmis_analizler = st.session_state.gecmis_analizler[-100:]
            gecmis_kaydet(st.session_state.gecmis_analizler)
            st.session_state.aktif_kayit_idx = len(st.session_state.gecmis_analizler) - 1

        st.session_state.kayit_yapildi = True

    st.divider()

    if st.session_state.gecmisten_gelindi:
        if st.button("⬅️ Geçmişe Dön", use_container_width=True):
            st.session_state.sayfa = "gecmis"
            st.session_state.gecmisten_gelindi = False
            st.session_state.aktif_kayit_idx = None
            st.rerun()
        st.markdown("")

    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.form_version += 1
        st.session_state.kayit_yapildi = False
        st.session_state.gecmisten_gelindi = False
        st.session_state.aktif_kayit_idx = None
        st.session_state.okunamayan_alanlar = []
        st.session_state.manuel_bekleyen = []
        st.session_state.sayfa = "giris"
        st.rerun()
