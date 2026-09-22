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
        padding-top: 0.5rem !important;
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

    div[data-testid="stMetric"] { padding: 0.2rem !important; }
    div[data-testid="stMetricValue"] { font-size: 1rem !important; }
    div[data-testid="stMetricLabel"] { font-size: 0.7rem !important; }

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
    "galibiyet_ev": 30.0, "beraberlik_ev": 30.0,
    "galibiyet_dep": 30.0, "beraberlik_dep": 30.0,
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
    "oran_1": 0.0, "oran_x": 0.0, "oran_2": 0.0,
    "oran_ust25": 0.0, "oran_alt25": 0.0,
    "oran_kg_var": 0.0, "oran_kg_yok": 0.0,
    "takim_ev": "", "takim_dep": "", "skor_ev": 0, "skor_dep": 0,
    "skor_belli": False,
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


def metinden_veri_cikar(metin: str) -> dict:
    veri = {}
    metin = metin.replace(",", ".")

    takim_ev, takim_dep, skor_ev, skor_dep, skor_belli = takimlari_cikar(metin)
    veri["takim_ev"] = takim_ev
    veri["takim_dep"] = takim_dep
    veri["skor_ev"] = skor_ev
    veri["skor_dep"] = skor_dep
    veri["skor_belli"] = skor_belli

    idx = metin.find("Güvenilirlik ve Form")
    if idx == -1:
        idx = metin.find("PPG")
    if idx != -1:
        blok = metin[idx:idx+1200]
        m = re.search(r'PPG[:\s]+([\d.]+)', blok)
        if m: veri["ppg_ev"] = float(m.group(1))
        m = re.search(r'(?:MBP|MPG)[:\s]+([\d.]+)', blok)
        if m: veri["mpg_dep"] = float(m.group(1))

        idx_ppg = blok.find("PPG")
        if idx_ppg != -1:
            ev_blok = blok[idx_ppg:idx_ppg+400]
            m_g = re.search(r'([\d.]+)%\s*\n\s*Galibiyet', ev_blok)
            m_b = re.search(r'([\d.]+)%\s*\n\s*Beraberlik', ev_blok)
            if m_g: veri["galibiyet_ev"] = float(m_g.group(1))
            if m_b: veri["beraberlik_ev"] = float(m_b.group(1))
            m_y = re.search(r'(?:Invencibilidade|Yenilmezlik)[:\s]+([\d.]+)%', ev_blok)
            if m_y: veri["yenilmezlik_ev"] = float(m_y.group(1))

        idx_mbp = blok.find("MBP")
        if idx_mbp == -1:
            idx_mbp = blok.find("MPG")
        if idx_mbp != -1:
            dep_blok = blok[idx_mbp:idx_mbp+400]
            m_g2 = re.search(r'([\d.]+)%\s*\n\s*Galibiyet', dep_blok)
            m_b2 = re.search(r'([\d.]+)%\s*\n\s*Beraberlik', dep_blok)
            if m_g2: veri["galibiyet_dep"] = float(m_g2.group(1))
            if m_b2: veri["beraberlik_dep"] = float(m_b2.group(1))
            m_y2 = re.search(r'(?:Invencibilidade|Yenilmezlik)[:\s]+([\d.]+)%', dep_blok)
            if m_y2: veri["yenilmezlik_dep"] = float(m_y2.group(1))

        idx_psy = metin.find("Psikolojik Faktör")
        if idx_psy != -1:
            psy_blok = metin[idx_psy:idx_psy+600]
            m = re.search(r'Reaksiyon Gücü\s*\t?\s*([\d.]+)%\s*\t?\s*([\d.]+)%', psy_blok)
            if m:
                veri["reaksiyon_ev"] = float(m.group(1))
                veri["reaksiyon_dep"] = float(m.group(2))
            m_atar = re.search(r'İlk Golü Atar\s*\t?\s*([\d.]+)%\s*\t?\s*([\d.]+)%', psy_blok)
            if m_atar:
                veri["ilk_gol_atar_ev"] = float(m_atar.group(1))
                veri["ilk_gol_atar_dep"] = float(m_atar.group(2))
            m_yer = re.search(r'İlk Golü Yer\s*\t?\s*([\d.]+)%\s*\t?\s*([\d.]+)%', psy_blok)
            if m_yer:
                veri["ilk_gol_yer_ev"] = float(m_yer.group(1))
                veri["ilk_gol_yer_dep"] = float(m_yer.group(2))

    idx = metin.find("Tablo Pozisyonu")
    if idx != -1:
        blok = metin[idx:idx+500]
        m = re.search(r'(\d{1,2})\s*\n\s*\w+\s*\n\s*VS\s*\n\s*\w+\s*\n\s*(\d{1,2})', blok)
        if m:
            veri["siralama_ev"] = int(m.group(1))
            veri["siralama_dep"] = int(m.group(2))

    idx = metin.find("Hücum Hakimiyeti")
    if idx != -1:
        blok = metin[idx:idx+300]
        yuzdeler = re.findall(r'([\d.]+)%', blok)
        if len(yuzdeler) >= 2:
            veri["hucum_hakimiyeti_ev"] = float(yuzdeler[0])
            veri["hucum_hakimiyeti_dep"] = float(yuzdeler[1])

    idx = metin.find("Agresiflik")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)\s*[·•]\s*([\d.]+)', blok)
        if m:
            veri["agresiflik_ev"] = float(m.group(1))
            veri["agresiflik_dep"] = float(m.group(2))

    idx = metin.find("İsabet")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)%\s*[·•]\s*([\d.]+)%', blok)
        if m:
            veri["isabet_ev"] = float(m.group(1))
            veri["isabet_dep"] = float(m.group(2))

    idx = metin.find("Hava Topu")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)\s*[·•]\s*([\d.]+)', blok)
        if m:
            veri["hava_topu_ev"] = float(m.group(1))
            veri["hava_topu_dep"] = float(m.group(2))

    idx = metin.find("Beklenen goller (maç öncesi xG)")
    if idx == -1:
        idx = metin.find("Beklenen goller")
    if idx != -1:
        blok = metin[idx:idx+500]
        m = re.search(r'\n([\d.]+)\n\d+\n[\w\s]+\n[×xX]\s*\n\w[\w\s]*\n([\d.]+)\n\d+', blok)
        if m:
            veri["xg_ev"] = float(m.group(1))
            veri["xg_dep"] = float(m.group(2))

    idx = metin.find("Atılan Gol (Ort)")
    if idx == -1:
        idx = metin.find("Atılan Gol")
    if idx != -1:
        blok = metin[idx:idx+400]
        sayilar = re.findall(r'\n\s*([\d.]+)\s*\n\s*\d+%', blok)
        if len(sayilar) >= 2:
            veri["atilan_ev"] = float(sayilar[0])
            veri["atilan_dep"] = float(sayilar[1])

    idx = metin.find("Yenen Gol (Ort)")
    if idx == -1:
        idx = metin.find("Yenen Gol")
    if idx != -1:
        blok = metin[idx:idx+400]
        sayilar = re.findall(r'\n\s*([\d.]+)\s*\n\s*\d+%', blok)
        if len(sayilar) >= 2:
            veri["yenen_ev"] = float(sayilar[0])
            veri["yenen_dep"] = float(sayilar[1])

    ss_listesi = re.findall(r'\bSS\s*\n\s*([\d.]+)', metin)
    if len(ss_listesi) >= 2:
        veri["ss_ev"] = float(ss_listesi[0])
        veri["ss_dep"] = float(ss_listesi[1])

    idx = metin.find("2.5 Üst")
    if idx != -1:
        blok = metin[idx:idx+400]
        yuzdeler = re.findall(r'(\d+)%', blok)
        if len(yuzdeler) >= 2:
            veri["ust25_ev"] = float(yuzdeler[0])
            if len(yuzdeler) >= 4:
                veri["ust25_dep"] = float(yuzdeler[-1])
            else:
                veri["ust25_dep"] = float(yuzdeler[1])

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

    # ---- 1X2 ORANLARI ----
    m = re.search(r'Casa\s*\n\s*([\d.]+)\s*\n\s*\|\s*\n\s*(?:E|Empate)\s*\n\s*([\d.]+)\s*\n\s*\|\s*\n\s*(?:Visit|Fora)\s*\n\s*([\d.]+)', metin, re.IGNORECASE)
    if m:
        veri["oran_1"] = float(m.group(1))
        veri["oran_x"] = float(m.group(2))
        veri["oran_2"] = float(m.group(3))

    # ---- ÜST/ALT 2.5 ORANLARI (ÇOKLU FORMAT) ----
    ust_alt_bulundu = False

    # Format 1: "2.5 1.73 2.10" (tab/boşluk)
    if not ust_alt_bulundu:
        m = re.search(r'\b2\.5\s+([\d.]+)\s+([\d.]+)', metin)
        if m:
            ust25 = float(m.group(1))
            alt25 = float(m.group(2))
            if 1.0 < ust25 < 20 and 1.0 < alt25 < 20:
                veri["oran_ust25"] = ust25
                veri["oran_alt25"] = alt25
                ust_alt_bulundu = True

    # Format 2: "2.5\n1.73\n2.10" (satır bazlı)
    if not ust_alt_bulundu:
        m = re.search(r'\b2\.5\s*\n\s*([\d.]+)\s*\n\s*([\d.]+)', metin)
        if m:
            ust25 = float(m.group(1))
            alt25 = float(m.group(2))
            if 1.0 < ust25 < 20 and 1.0 < alt25 < 20:
                veri["oran_ust25"] = ust25
                veri["oran_alt25"] = alt25
                ust_alt_bulundu = True

    # Format 3: "Hat\tOver\tUnder\n2.5\t1.73\t2.10"
    if not ust_alt_bulundu:
        m = re.search(r'Hat[\s\t]+Over[\s\t]+Under\s*\n\s*2\.5[\s\t]+([\d.]+)[\s\t]+([\d.]+)', metin)
        if m:
            ust25 = float(m.group(1))
            alt25 = float(m.group(2))
            if 1.0 < ust25 < 20 and 1.0 < alt25 < 20:
                veri["oran_ust25"] = ust25
                veri["oran_alt25"] = alt25
                ust_alt_bulundu = True

    # Format 4: "Gols Over/Under" bloğundan
    if not ust_alt_bulundu:
        idx = metin.find("Over/Under")
        if idx != -1:
            blok = metin[idx:idx+500]
            m = re.search(r'2\.5[\s\t]+([\d.]+)[\s\t]+([\d.]+)', blok)
            if m:
                ust25 = float(m.group(1))
                alt25 = float(m.group(2))
                if 1.0 < ust25 < 20 and 1.0 < alt25 < 20:
                    veri["oran_ust25"] = ust25
                    veri["oran_alt25"] = alt25
                    ust_alt_bulundu = True

    # ---- KG ORANLARI (ÇOKLU FORMAT) ----
    # Format 1: "Sim\n1.50\nNão\n2.50"
    m = re.search(r'Sim\s*\n\s*([\d.]+)\s*\n\s*N[ãa]o\s*\n\s*([\d.]+)', metin, re.IGNORECASE)
    if m:
        veri["oran_kg_var"] = float(m.group(1))
        veri["oran_kg_yok"] = float(m.group(2))
    else:
        # Format 2: "Sim 1.50 Não 2.50"
        m = re.search(r'Sim\s+([\d.]+)\s+N[ãa]o\s+([\d.]+)', metin, re.IGNORECASE)
        if m:
            veri["oran_kg_var"] = float(m.group(1))
            veri["oran_kg_yok"] = float(m.group(2))

    return veri


# ==========================================
# İŞ MANTIĞI
# ==========================================
def poisson_pmf(k: int, lam: float) -> float:
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)


def poisson_random(lam: float) -> int:
    if lam <= 0:
        return 0
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while True:
        k += 1
        p *= random.random()
        if p <= L:
            return k - 1


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

    hucum_ev *= isabet_kat_ev * hak_kat_ev * gal_kat_ev * ilk_kat_ev * agres_kat_ev * hava_kat_ev
    hucum_dep *= isabet_kat_dep * hak_kat_dep * gal_kat_dep * ilk_kat_dep * agres_kat_dep * hava_kat_dep

    sav_ev = v["yenen_ev"]
    sav_dep = v["yenen_dep"]

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


def normalize_olasilik(oranlar: list) -> list:
    ham = [100.0 / o if o > 1 else 0 for o in oranlar]
    toplam = sum(ham)
    if toplam <= 0:
        return ham
    return [(h / toplam) * 100 for h in ham]


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
        if not veri:
            return 0, 0, 0, 0
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
    if "1" in tahmin_1x2 or "ev" in tahmin_1x2.lower():
        tahmin_1x2_norm = "1"
    elif "x" in tahmin_1x2.lower() or "beraber" in tahmin_1x2.lower():
        tahmin_1x2_norm = "X"
    elif "2" in tahmin_1x2 or "dep" in tahmin_1x2.lower():
        tahmin_1x2_norm = "2"

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

    if "üst" in tahmin_str_low or "ust" in tahmin_str_low:
        tahmin_ust_bool = True
    elif "alt" in tahmin_str_low:
        tahmin_ust_bool = False
    else:
        tahmin_ust_bool = None

    sonuc["gol_gercek"] = "Üst 2.5" if gercek_ust_bool else "Alt 2.5"
    sonuc["gol_tahmin"] = tahmin_str
    sonuc["gol_tuttu"] = (tahmin_ust_bool is not None and gercek_ust_bool == tahmin_ust_bool)

    gercek_kg_var_bool = (skor_ev > 0 and skor_dep > 0)

    tahmin_kg = str(tahminler.get("kg_tahmin", "")).strip()
    tahmin_kg_low = tahmin_kg.lower()

    if "var" in tahmin_kg_low:
        tahmin_kg_bool = True
    elif "yok" in tahmin_kg_low:
        tahmin_kg_bool = False
    else:
        tahmin_kg_bool = None

    sonuc["kg_gercek"] = "KG Var" if gercek_kg_var_bool else "KG Yok"
    sonuc["kg_tahmin"] = tahmin_kg
    sonuc["kg_tuttu"] = (tahmin_kg_bool is not None and gercek_kg_var_bool == tahmin_kg_bool)

    tutan = sum([sonuc["1X2_tuttu"], sonuc["cifte_tuttu"], sonuc["gol_tuttu"], sonuc["kg_tuttu"]])
    sonuc["toplam_tutan"] = tutan
    sonuc["toplam_metrik"] = 4

    return sonuc


def value_bet_analizi(v: dict, p1, px, p2, ust25_model, kg_var_model):
    sonuclar = []

    if v.get("oran_1", 0) > 0 and v.get("oran_x", 0) > 0 and v.get("oran_2", 0) > 0:
        piyasa = normalize_olasilik([v["oran_1"], v["oran_x"], v["oran_2"]])
        for isim, model, piy, oran in [
            ("1 (Ev)", p1, piyasa[0], v["oran_1"]),
            ("X", px, piyasa[1], v["oran_x"]),
            ("2 (Dep)", p2, piyasa[2], v["oran_2"]),
        ]:
            fark = model - piy
            if fark >= 5:    karar = "✅ VALUE"
            elif fark >= 2:  karar = "🟡 Sınırda"
            else:            karar = "❌ Value yok"
            sonuclar.append(("1X2", isim, model, piy, fark, oran, karar))

    if v.get("oran_ust25", 0) > 0 and v.get("oran_alt25", 0) > 0:
        piyasa = normalize_olasilik([v["oran_ust25"], v["oran_alt25"]])
        alt25_model = 100 - ust25_model
        for isim, model, piy, oran in [
            ("Üst 2.5", ust25_model, piyasa[0], v["oran_ust25"]),
            ("Alt 2.5", alt25_model, piyasa[1], v["oran_alt25"]),
        ]:
            fark = model - piy
            if fark >= 5:    karar = "✅ VALUE"
            elif fark >= 2:  karar = "🟡 Sınırda"
            else:            karar = "❌ Value yok"
            sonuclar.append(("Üst/Alt 2.5", isim, model, piy, fark, oran, karar))

    if v.get("oran_kg_var", 0) > 0 and v.get("oran_kg_yok", 0) > 0:
        piyasa = normalize_olasilik([v["oran_kg_var"], v["oran_kg_yok"]])
        kg_yok_model = 100 - kg_var_model
        for isim, model, piy, oran in [
            ("KG Var", kg_var_model, piyasa[0], v["oran_kg_var"]),
            ("KG Yok", kg_yok_model, piyasa[1], v["oran_kg_yok"]),
        ]:
            fark = model - piy
            if fark >= 5:    karar = "✅ VALUE"
            elif fark >= 2:  karar = "🟡 Sınırda"
            else:            karar = "❌ Value yok"
            sonuclar.append(("KG", isim, model, piy, fark, oran, karar))

    return sonuclar


def favori_kombolar(matris, max_gol: int = MAX_GOL):
    p1 = p_x = p2 = 0.0
    alt = ust = 0.0
    kg_var = kg_yok = 0.0

    for i in range(max_gol):
        for j in range(max_gol):
            p = matris[i][j]
            if i > j:    p1 += p
            elif i == j: p_x += p
            else:        p2 += p
            if i + j < 2.5:   alt += p
            elif i + j > 2.5: ust += p
            if i > 0 and j > 0: kg_var += p
            else:                kg_yok += p

    favori_sonuc = max([("1", p1), ("X", p_x), ("2", p2)], key=lambda x: x[1])
    favori_gol   = max([("Alt", alt), ("Üst", ust)], key=lambda x: x[1])
    favori_kg    = max([("Var", kg_var), ("Yok", kg_yok)], key=lambda x: x[1])

    def fn_sonuc(kod):
        if kod == "1": return lambda i, j: i > j
        if kod == "X": return lambda i, j: i == j
        return lambda i, j: i < j

    def fn_gol(kod):
        if kod == "Alt": return lambda i, j: i + j < 2.5
        return lambda i, j: i + j > 2.5

    def fn_kg(kod):
        if kod == "Var": return lambda i, j: i > 0 and j > 0
        return lambda i, j: i == 0 or j == 0

    kombinasyonlar = [
        (f"{favori_sonuc[0]} {favori_gol[0]}", fn_sonuc(favori_sonuc[0]), fn_gol(favori_gol[0])),
        (f"{favori_sonuc[0]} {favori_kg[0]}",  fn_sonuc(favori_sonuc[0]), fn_kg(favori_kg[0])),
        (f"{favori_gol[0]} {favori_kg[0]}",    fn_gol(favori_gol[0]),     fn_kg(favori_kg[0])),
    ]

    kombolar = []
    for isim, f1, f2 in kombinasyonlar:
        toplam = 0.0
        for i in range(max_gol):
            for j in range(max_gol):
                if f1(i, j) and f2(i, j):
                    toplam += matris[i][j]
        kombolar.append((isim, toplam * 100))

    kombolar.sort(key=lambda x: x[1], reverse=True)
    return kombolar, (favori_sonuc[0], favori_gol[0], favori_kg[0])


def value_kombolar(v: dict, matris, max_gol: int = MAX_GOL):
    p1 = p_x = p2 = 0.0
    alt = ust = 0.0
    kg_var = kg_yok = 0.0

    for i in range(max_gol):
        for j in range(max_gol):
            p = matris[i][j]
            if i > j:    p1 += p
            elif i == j: p_x += p
            else:        p2 += p
            if i + j < 2.5:   alt += p
            elif i + j > 2.5: ust += p
            if i > 0 and j > 0: kg_var += p
            else:                kg_yok += p

    p1 *= 100; p_x *= 100; p2 *= 100
    alt *= 100; ust *= 100
    kg_var *= 100; kg_yok *= 100

    piyasa_1x2 = normalize_olasilik([v.get("oran_1", 0), v.get("oran_x", 0), v.get("oran_2", 0)]) if v.get("oran_1", 0) > 0 else [0, 0, 0]
    piyasa_ou = normalize_olasilik([v.get("oran_ust25", 0), v.get("oran_alt25", 0)]) if v.get("oran_ust25", 0) > 0 else [0, 0]
    piyasa_kg = normalize_olasilik([v.get("oran_kg_var", 0), v.get("oran_kg_yok", 0)]) if v.get("oran_kg_var", 0) > 0 else [0, 0]

    value_bets = []

    if v.get("oran_1", 0) > 0:
        for isim, model, piy, oran, f in [
            ("1", p1, piyasa_1x2[0], v["oran_1"], p1 - piyasa_1x2[0]),
            ("X", p_x, piyasa_1x2[1], v["oran_x"], p_x - piyasa_1x2[1]),
            ("2", p2, piyasa_1x2[2], v["oran_2"], p2 - piyasa_1x2[2]),
        ]:
            if f >= 5:
                value_bets.append(("1X2", isim, model, f, oran))

    if v.get("oran_ust25", 0) > 0:
        for isim, model, piy, oran, f in [
            ("Üst 2.5", ust, piyasa_ou[0], v["oran_ust25"], ust - piyasa_ou[0]),
            ("Alt 2.5", alt, piyasa_ou[1], v["oran_alt25"], alt - piyasa_ou[1]),
        ]:
            if f >= 5:
                value_bets.append(("O/U", isim, model, f, oran))

    if v.get("oran_kg_var", 0) > 0:
        for isim, model, piy, oran, f in [
            ("KG Var", kg_var, piyasa_kg[0], v["oran_kg_var"], kg_var - piyasa_kg[0]),
            ("KG Yok", kg_yok, piyasa_kg[1], v["oran_kg_yok"], kg_yok - piyasa_kg[1]),
        ]:
            if f >= 5:
                value_bets.append(("KG", isim, model, f, oran))

    kombolar = []
    for i in range(len(value_bets)):
        for j in range(i + 1, len(value_bets)):
            vb1 = value_bets[i]
            vb2 = value_bets[j]

            if vb1[0] == vb2[0]:
                continue

            isim = f"{vb1[1]} + {vb2[1]}"
            kombine_oran = vb1[4] * vb2[4]

            def filtre_vb(kod, market):
                if market == "1X2":
                    if kod == "1": return lambda i, j: i > j
                    if kod == "X": return lambda i, j: i == j
                    return lambda i, j: i < j
                if market == "O/U":
                    if kod == "Üst 2.5": return lambda i, j: i + j > 2.5
                    return lambda i, j: i + j < 2.5
                if market == "KG":
                    if kod == "KG Var": return lambda i, j: i > 0 and j > 0
                    return lambda i, j: i == 0 or j == 0
                return None

            f1 = filtre_vb(vb1[1], vb1[0])
            f2 = filtre_vb(vb2[1], vb2[0])

            if f1 is None or f2 is None:
                continue

            model_p = 0.0
            for ii in range(max_gol):
                for jj in range(max_gol):
                    if f1(ii, jj) and f2(ii, jj):
                        model_p += matris[ii][jj]
            model_p *= 100

            piyasa_p = (100.0 / kombine_oran) if kombine_oran > 0 else 0
            fark = model_p - piyasa_p

            if fark >= 5:
                kombolar.append({
                    "isim": isim,
                    "model": model_p,
                    "piyasa": piyasa_p,
                    "oran": kombine_oran,
                    "fark": fark,
                })

    kombolar.sort(key=lambda x: x["fark"], reverse=True)
    return kombolar


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
    yorumlar.append(("🛡️ SAVUNMA", txt))

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

    kg_var_model = olas["kg_var"] / toplam * 100
    kg_ort = (kg_var_model + v["kg_oran"]) / 2

    en_olasi = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    en_guvenli = max([("1X", cifte_1x), ("X2", cifte_x2), ("12", cifte_12)], key=lambda x: x[1])

    en_olasi_gol = "Üst 2.5" if tahmini_gol > 2.6 else "Alt 2.5"
    en_olasi_kg = "KG Var" if kg_ort > 55 else "KG Yok" if kg_ort < 45 else "Belirsiz"

    vb = value_bet_analizi(v, p1, px, p2, ust_25, kg_var_model)
    kombolar_fav, favoriler = favori_kombolar(matris, MAX_GOL)

    oran_map = {
        "1": v.get("oran_1", 0), "X": v.get("oran_x", 0), "2": v.get("oran_2", 0),
        "Üst": v.get("oran_ust25", 0), "Alt": v.get("oran_alt25", 0),
        "Var": v.get("oran_kg_var", 0), "Yok": v.get("oran_kg_yok", 0),
    }

    adaylar = []
    for isim, yuzde in kombolar_fav:
        parcalar = isim.split()
        if len(parcalar) == 2:
            o1 = oran_map.get(parcalar[0], 0)
            o2 = oran_map.get(parcalar[1], 0)
            if o1 > 0 and o2 > 0:
                kombine_oran = o1 * o2
                ev = (yuzde / 100) * kombine_oran
                adaylar.append({"tip": "🎯 Favori Kombo", "isim": isim, "yuzde": yuzde, "oran": kombine_oran, "ev": ev})

    tekli_value = [x for x in vb if x[4] >= 5] if vb else []
    for market, isim, model, piy, fark_vb, oran, karar in tekli_value:
        ev = (model / 100) * oran
        adaylar.append({"tip": "💎 Tekli Value", "isim": isim, "yuzde": model, "oran": oran, "ev": ev})

    vk = value_kombolar(v, matris, MAX_GOL)
    for k in vk[:5]:
        ev = (k["model"] / 100) * k["oran"]
        adaylar.append({"tip": "💎💎 Value Kombo", "isim": k["isim"], "yuzde": k["model"], "oran": k["oran"], "ev": ev})

    adaylar.sort(key=lambda x: x["ev"], reverse=True)

    return {
        "lam_ev": lam_ev, "lam_dep": lam_dep, "guven": guven,
        "matris": matris, "olas": olas,
        "p1": p1, "px": px, "p2": p2,
        "cifte_1x": cifte_1x, "cifte_x2": cifte_x2, "cifte_12": cifte_12,
        "tahmini_gol": tahmini_gol, "ust_25": ust_25,
        "kg_var_model": kg_var_model, "kg_ort": kg_ort,
        "en_olasi": en_olasi, "en_guvenli": en_guvenli,
        "en_olasi_gol": en_olasi_gol, "en_olasi_kg": en_olasi_kg,
        "vb": vb, "kombolar_fav": kombolar_fav, "favoriler": favoriler,
        "vk": vk, "adaylar": adaylar,
        "en_iyi_3": adaylar[:3],
    }


# ==========================================
# SAYFA 1
# ==========================================
if st.session_state.sayfa == "giris":
    st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:gray;'>İstatistik + oran metnini kopyala → yapıştır → analiz et.</p>",
        unsafe_allow_html=True
    )

    st.markdown("### 📋 İstatistik ve Oranları Yapıştır")

    yapistir_metni = st.text_area(
        "Yapıştırma alanı",
        height=280,
        key="yapistir_input",
        label_visibility="collapsed",
        placeholder="İstatistik + oran metnini buraya yapıştır."
    )

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
        st.rerun()

    if analiz_btn:
        if not yapistir_metni.strip():
            st.warning("⚠️ Önce metni yapıştır.")
        else:
            cikan = metinden_veri_cikar(yapistir_metni)
            if not cikan:
                st.error("❌ Metinden hiçbir veri çıkarılamadı.")
            else:
                yeni_veri = copy.deepcopy(VARSAYILAN_VERI)
                yeni_veri.update(cikan)
                st.session_state.form_verileri = yeni_veri
                st.session_state.kayit_yapildi = False
                st.session_state.gecmisten_gelindi = False

                if not veri_yeterli_mi(yeni_veri):
                    st.error(f"⚠️ Sadece {len(cikan)} alan bulundu.")
                    st.info(f"Bulunan: {', '.join(cikan.keys())}")
                else:
                    st.session_state.sayfa = "sonuc"
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
    st.caption("Bir maça tıkla → o maçın **tam analiz ekranı** açılır")

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
            baslik = f"⚽ {takim_ev} vs {takim_dep}"

        if st.button(baslik, use_container_width=True, key=f"mac_{idx_gercek}"):
            st.session_state.form_verileri = copy.deepcopy(v_g)
            st.session_state.kayit_yapildi = True
            st.session_state.gecmisten_gelindi = True
            st.session_state.sayfa = "sonuc"
            st.rerun()

    st.divider()

    c_temizle, c_geri = st.columns(2)
    with c_temizle:
        if st.button("🗑️ Geçmişi Temizle", use_container_width=True):
            st.session_state.gecmis_analizler = []
            try:
                if os.path.exists(GECMIS_DOSYA):
                    os.remove(GECMIS_DOSYA)
            except Exception:
                pass
            st.rerun()
    with c_geri:
        if st.button("⬅️ Geri Dön", use_container_width=True, type="primary"):
            st.session_state.sayfa = "giris"
            st.rerun()


# ==========================================
# SAYFA 2: ANALİZ
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)

    lam_ev = a["lam_ev"]; lam_dep = a["lam_dep"]; guven = a["guven"]
    matris = a["matris"]
    p1 = a["p1"]; px = a["px"]; p2 = a["p2"]
    cifte_1x = a["cifte_1x"]; cifte_x2 = a["cifte_x2"]; cifte_12 = a["cifte_12"]
    tahmini_gol = a["tahmini_gol"]; ust_25 = a["ust_25"]
    kg_var_model = a["kg_var_model"]; kg_ort = a["kg_ort"]
    en_olasi = a["en_olasi"]; en_guvenli = a["en_guvenli"]
    vb = a["vb"]; kombolar_fav = a["kombolar_fav"]; favoriler = a["favoriler"]
    vk = a["vk"]; adaylar = a["adaylar"]; en_iyi_3 = a["en_iyi_3"]

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

    with st.expander("🎯 Strateji Önerileri", expanded=True):
        st.markdown(f"**Ana Senaryo:** {senaryo}")
        st.markdown(f"""
        - 🥇 **En Olası Sonuç:** **{en_olasi[0]}** → 1: %{p1:.1f} • X: %{px:.1f} • 2: %{p2:.1f}
        - 🛡️ **En Güvenli:** Çifte Şans **{en_guvenli[0]}** → 1X: %{cifte_1x:.1f} • X2: %{cifte_x2:.1f} • 12: %{cifte_12:.1f}
        - ⚽ **Gol:** **{a['en_olasi_gol']}** (beklenen: {tahmini_gol:.2f}) → Üst: %{ust_25:.0f} • Alt: %{100-ust_25:.0f}
        - 🤝 **KG:** **{a['en_olasi_kg']}** → Var: %{kg_ort:.0f} • Yok: %{100-kg_ort:.0f}
        - 📈 **İkinci Tercih:** {'X2' if p1 > p2 else '1X'} (%{max(cifte_1x, cifte_x2):.1f})
        """)

    with st.expander("🤝 Karşılıklı Gol (KG) Tahmini", expanded=True):
        st.markdown(f"""
        - **KG Var Olasılığı (Model):** **%{kg_var_model:.1f}**
        - **KG Yok Olasılığı (Model):** **%{100-kg_var_model:.1f}**
        - **Ortalama:** %{kg_ort:.1f}
        """)

    with st.expander("🎲 Monte Carlo Simülasyonu (5000 sim)", expanded=False):
        mc = monte_carlo_simulasyon(lam_ev, lam_dep, MONTE_CARLO_N)

        st.markdown("### 📊 1 - X - 2")
        c1, c2, c3 = st.columns(3)
        c1.metric("1 (Ev)", f"%{mc['1']['oran']:.1f}")
        c2.metric("X", f"%{mc['X']['oran']:.1f}")
        c3.metric("2 (Dep)", f"%{mc['2']['oran']:.1f}")

        for isim, key in [("1 (Ev)", "1"), ("X", "X"), ("2 (Dep)", "2")]:
            gen = mc[key]["genislik"]
            risk = risk_seviyesi(gen)
            st.markdown(
                f"**{isim}** — GA (%90): **%{mc[key]['alt']:.1f} - %{mc[key]['ust']:.1f}** "
                f"(genişlik: %{gen:.1f}) → {risk}"
            )

        st.markdown("### ⚽ Üst 2.5")
        st.markdown(f"**Üst 2.5** — %{mc['ust25']['oran']:.1f} (GA: %{mc['ust25']['alt']:.1f} - %{mc['ust25']['ust']:.1f})")

        st.markdown("### 🤝 KG Var")
        st.markdown(f"**KG Var** — %{mc['kg_var']['oran']:.1f} (GA: %{mc['kg_var']['alt']:.1f} - %{mc['kg_var']['ust']:.1f})")

    # ==========================================
    # 💎 ORAN ANALİZİ (Boş başlık gösterme)
    # ==========================================
    with st.expander("💎 Oran Analizi", expanded=True):
        if vb:
            # 1X2
            x12_satirlar = [x for x in vb if x[0] == "1X2"]
            if x12_satirlar:
                st.markdown("### 📊 1 - X - 2")
                for market, isim, model, piy, fark_vb, oran, karar in x12_satirlar:
                    st.markdown(f"**{isim}** (Oran: {oran})")
                    st.markdown(f"Model: **%{model:.1f}** | Piyasa: **%{piy:.1f}** | Fark: **{fark_vb:+.1f}** {karar}")

            # Üst/Alt 2.5
            ust_alt_satirlar = [x for x in vb if x[0] == "Üst/Alt 2.5"]
            if ust_alt_satirlar:
                st.markdown("---")
                st.markdown("### ⚽ Üst / Alt 2.5")
                for market, isim, model, piy, fark_vb, oran, karar in ust_alt_satirlar:
                    st.markdown(f"**{isim}** (Oran: {oran})")
                    st.markdown(f"Model: **%{model:.1f}** | Piyasa: **%{piy:.1f}** | Fark: **{fark_vb:+.1f}** {karar}")

            # KG
            kg_satirlar = [x for x in vb if x[0] == "KG"]
            if kg_satirlar:
                st.markdown("---")
                st.markdown("### 🤝 KG Var / Yok")
                for market, isim, model, piy, fark_vb, oran, karar in kg_satirlar:
                    st.markdown(f"**{isim}** (Oran: {oran})")
                    st.markdown(f"Model: **%{model:.1f}** | Piyasa: **%{piy:.1f}** | Fark: **{fark_vb:+.1f}** {karar}")
        else:
            st.info("ℹ️ Oran verisi bulunamadı.")

    st.divider()
    st.markdown("## 🏆 FİNAL ÖNERİ — EN İYİ 3 BAHİS")

    if en_iyi_3:
        madalya = ["🥇", "🥈", "🥉"]
        for i, ad in enumerate(en_iyi_3):
            if ad["ev"] >= 1.5:
                ev_yorumu = "🟢 Çok Kârlı"; kutu = st.success
            elif ad["ev"] >= 1.2:
                ev_yorumu = "🟢 Kârlı"; kutu = st.success
            elif ad["ev"] >= 1.0:
                ev_yorumu = "🟡 Sınırda"; kutu = st.warning
            else:
                ev_yorumu = "🔴 Kârsız"; kutu = st.error

            kutu(f"""
{madalya[i]} **{ad['isim']}** — {ad['tip']}

📊 Model: **%{ad['yuzde']:.1f}** | 💰 Oran: **{ad['oran']:.2f}** | 🎲 EV: **{ad['ev']:.2f}** → {ev_yorumu}
""")

        st.markdown(f"💡 **Yorum:** Her 1 TL yatırımda ortalama **{en_iyi_3[0]['ev']:.2f} TL** geri kazanç beklenir.")

        if len(adaylar) > 3:
            with st.expander(f"📋 Diğer Adaylar ({len(adaylar) - 3})", expanded=False):
                for i, ad in enumerate(adaylar[3:], 4):
                    emoji = "🟢" if ad["ev"] >= 1.2 else "🟡" if ad["ev"] >= 1.0 else "🔴"
                    st.markdown(f"{i}. {emoji} **{ad['isim']}** ({ad['tip']}) → **EV {ad['ev']:.2f}**")
    else:
        st.info("ℹ️ Oran verisi olmadığı için final öneri hesaplanamadı.")

    # GEÇMİŞE KAYDET — SADECE BİR KEZ
    if en_iyi_3 and not st.session_state.kayit_yapildi:
        yeni_kayit = {
            "veri": copy.deepcopy(v),
            "analiz": {
                "p1": p1, "px": px, "p2": p2,
                "tahmini_gol": tahmini_gol,
                "kg_var_model": kg_var_model,
                "ust_25": ust_25,
                "en_iyi_3": en_iyi_3,
                "en_olasi_gol": a["en_olasi_gol"],
                "en_olasi_kg": a["en_olasi_kg"],
                "en_olasi_1x2": en_olasi[0],
                "en_guvenli_cifte": en_guvenli[0],
            },
            "en_iyi_bahis": en_iyi_3[0]["isim"],
            "en_iyi_ev": en_iyi_3[0]["ev"],
        }
        if dogruluk is not None:
            yeni_kayit["dogruluk"] = dogruluk

        mevcut = st.session_state.gecmis_analizler
        tekrar_mi = False
        if mevcut:
            son = mevcut[-1]
            if (
                son["veri"].get("takim_ev") == yeni_kayit["veri"].get("takim_ev")
                and son["veri"].get("takim_dep") == yeni_kayit["veri"].get("takim_dep")
                and son["veri"].get("skor_ev") == yeni_kayit["veri"].get("skor_ev")
                and son["veri"].get("skor_dep") == yeni_kayit["veri"].get("skor_dep")
                and abs(son["analiz"].get("p1", 0) - yeni_kayit["analiz"].get("p1", 0)) < 0.1
                and abs(son["analiz"].get("px", 0) - yeni_kayit["analiz"].get("px", 0)) < 0.1
                and abs(son["analiz"].get("p2", 0) - yeni_kayit["analiz"].get("p2", 0)) < 0.1
            ):
                tekrar_mi = True

        if not tekrar_mi:
            st.session_state.gecmis_analizler.append(yeni_kayit)
            st.session_state.gecmis_analizler = st.session_state.gecmis_analizler[-100:]
            gecmis_kaydet(st.session_state.gecmis_analizler)

        st.session_state.kayit_yapildi = True

    st.divider()

    if st.session_state.gecmisten_gelindi:
        if st.button("⬅️ Geçmişe Dön", use_container_width=True):
            st.session_state.sayfa = "gecmis"
            st.session_state.gecmisten_gelindi = False
            st.rerun()
        st.markdown("")

    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.form_version += 1
        st.session_state.kayit_yapildi = False
        st.session_state.gecmisten_gelindi = False
        st.session_state.sayfa = "giris"
        st.rerun()
