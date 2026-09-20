import streamlit as st
import math
import copy
import re

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
    h2 { font-size: 0.95rem !important; margin: 0.2rem 0 !important; }
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
        font-size: 0.8rem !important;
    }

    details summary {
        font-size: 0.8rem !important;
        padding: 0.2rem 0.4rem !important;
    }

    textarea { font-size: 0.75rem !important; }
</style>
""", unsafe_allow_html=True)

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
    # 🆕 ORANLAR
    "oran_1": 0.0, "oran_x": 0.0, "oran_2": 0.0,
    "oran_ust25": 0.0, "oran_alt25": 0.0,
    "oran_kg_var": 0.0, "oran_kg_yok": 0.0,
    "oran_1x": 0.0, "oran_x2": 0.0, "oran_12": 0.0,
}

EV_AVANTAJ = 1.12
DEP_DEZAVANTAJ = 0.94
MAX_GOL = 8

# ==========================================
# SESSION STATE
# ==========================================
if "sayfa" not in st.session_state:
    st.session_state.sayfa = "giris"
if "form_verileri" not in st.session_state:
    st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
if "form_version" not in st.session_state:
    st.session_state.form_version = 0


# ==========================================
# METİNDEN VERİ ÇIKARMA
# ==========================================
def metinden_veri_cikar(metin: str) -> dict:
    veri = {}
    metin = metin.replace(",", ".")

    # ---- PPG ----
    m = re.search(r'PPG[:\s]+([\d.]+)', metin)
    if m: veri["ppg_ev"] = float(m.group(1))

    # ---- MPG / MBP ----
    m = re.search(r'(?:MBP|MPG)[:\s]+([\d.]+)', metin)
    if m: veri["mpg_dep"] = float(m.group(1))

    # ---- Galibiyet/Beraberlik (Ev) ----
    idx_ppg = metin.find("PPG")
    if idx_ppg != -1:
        blok = metin[idx_ppg:idx_ppg+500]
        m_g = re.search(r'([\d.]+)%\s*Galibiyet', blok)
        m_b = re.search(r'([\d.]+)%\s*Beraberlik', blok)
        if m_g: veri["galibiyet_ev"] = float(m_g.group(1))
        if m_b: veri["beraberlik_ev"] = float(m_b.group(1))
        m_y = re.search(r'(?:Invencibilidade|Yenilmezlik)[:\s]+([\d.]+)%', blok)
        if m_y: veri["yenilmezlik_ev"] = float(m_y.group(1))

    # ---- Galibiyet/Beraberlik (Dep) ----
    idx_mbp = metin.find("MBP")
    if idx_mbp == -1:
        idx_mbp = metin.find("MPG")
    if idx_mbp != -1:
        blok = metin[idx_mbp:idx_mbp+500]
        m_g = re.search(r'([\d.]+)%\s*Galibiyet', blok)
        m_b = re.search(r'([\d.]+)%\s*Beraberlik', blok)
        if m_g: veri["galibiyet_dep"] = float(m_g.group(1))
        if m_b: veri["beraberlik_dep"] = float(m_b.group(1))
        m_y = re.search(r'(?:Invencibilidade|Yenilmezlik)[:\s]+([\d.]+)%', blok)
        if m_y: veri["yenilmezlik_dep"] = float(m_y.group(1))

    # ---- Sıralama ----
    m = re.search(r'Sıra[:\s]+(\d{1,2})', metin)
    if m:
        veri["siralama_ev"] = int(m.group(1))
        m2 = re.search(r'Sıra[:\s]+(\d{1,2})', metin[m.end():])
        if m2:
            veri["siralama_dep"] = int(m2.group(1))

    if "siralama_ev" not in veri or "siralama_dep" not in veri:
        idx = metin.find("Tablo Pozisyonu")
        if idx == -1:
            idx = metin.find("Tablo")
        if idx != -1:
            blok = metin[idx:idx+800]
            vs_idx = blok.find("VS")
            if vs_idx == -1:
                vs_idx = blok.find("vs")
            if vs_idx != -1:
                onceki = blok[:vs_idx]
                sonraki = blok[vs_idx:]
                ev_sayilar = re.findall(r'\n\s*(\d{1,2})\s*\n', onceki)
                dep_sayilar = re.findall(r'\n\s*(\d{1,2})\s*\n', sonraki)
                if ev_sayilar:
                    veri["siralama_ev"] = int(ev_sayilar[-1])
                if dep_sayilar:
                    veri["siralama_dep"] = int(dep_sayilar[0])

    # ---- Hücum Hakimiyeti ----
    idx = metin.find("Hücum Hakimiyeti")
    if idx != -1:
        blok = metin[idx:idx+300]
        sayilar = re.findall(r'([\d.]+)%', blok)
        if len(sayilar) >= 2:
            veri["hucum_hakimiyeti_ev"] = float(sayilar[0])
            veri["hucum_hakimiyeti_dep"] = float(sayilar[1])

    # ---- Agresiflik ----
    idx = metin.find("Agresiflik")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)\s*[·•]\s*([\d.]+)', blok)
        if m:
            veri["agresiflik_ev"] = float(m.group(1))
            veri["agresiflik_dep"] = float(m.group(2))
        else:
            m = re.search(r'Agresiflik[:\s]+([\d.]+)', blok)
            if m:
                veri["agresiflik_ev"] = float(m.group(1))

    idx2 = metin.find("Agresiflik", idx + 1) if idx != -1 else -1
    if idx2 != -1 and "agresiflik_dep" not in veri:
        blok2 = metin[idx2:idx2+200]
        m = re.search(r'Agresiflik[:\s]+([\d.]+)', blok2)
        if m:
            veri["agresiflik_dep"] = float(m.group(1))

    # ---- İsabet ----
    idx = metin.find("İsabet")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)%\s*[·•]\s*([\d.]+)%', blok)
        if m:
            veri["isabet_ev"] = float(m.group(1))
            veri["isabet_dep"] = float(m.group(2))

    idx2 = metin.find("İsabet", idx + 1) if idx != -1 else -1
    if idx2 != -1 and "isabet_dep" not in veri:
        blok2 = metin[idx2:idx2+200]
        m = re.search(r'İsabet[:\s]+%?([\d.]+)', blok2)
        if m:
            veri["isabet_dep"] = float(m.group(1))

    # ---- Hava Topu ----
    idx = metin.find("Hava Topu")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)\s*[·•]\s*([\d.]+)', blok)
        if m:
            veri["hava_topu_ev"] = float(m.group(1))
            veri["hava_topu_dep"] = float(m.group(2))

    idx2 = metin.find("Hava Topu", idx + 1) if idx != -1 else -1
    if idx2 != -1 and "hava_topu_dep" not in veri:
        blok2 = metin[idx2:idx2+200]
        m = re.search(r'Hava Topu[:\s]+(\d+)', blok2)
        if m:
            veri["hava_topu_dep"] = float(m.group(1))

    # ---- İlk Gol ----
    idx = metin.find("İlk Golü Atar")
    if idx != -1:
        blok = metin[idx:idx+200]
        sayilar = re.findall(r'([\d.]+)%', blok)
        if len(sayilar) >= 2:
            veri["ilk_gol_atar_ev"] = float(sayilar[0])
            veri["ilk_gol_atar_dep"] = float(sayilar[1])

    idx = metin.find("İlk Golü Yer")
    if idx != -1:
        blok = metin[idx:idx+200]
        sayilar = re.findall(r'([\d.]+)%', blok)
        if len(sayilar) >= 2:
            veri["ilk_gol_yer_ev"] = float(sayilar[0])
            veri["ilk_gol_yer_dep"] = float(sayilar[1])

    # ---- Reaksiyon ----
    m = re.search(r'Reaksiyon Gücü\s*\t?\s*([\d.]+)%\s*\t?\s*([\d.]+)%', metin)
    if m:
        veri["reaksiyon_ev"] = float(m.group(1))
        veri["reaksiyon_dep"] = float(m.group(2))
    else:
        reaks = re.findall(r'Reak[:\s]+%?([\d.]+)', metin)
        if len(reaks) >= 2:
            veri["reaksiyon_ev"] = float(reaks[0])
            veri["reaksiyon_dep"] = float(reaks[1])

    # ---- xG ----
    idx = metin.find("Beklenen goller")
    if idx == -1:
        idx = metin.find("xG)")
    if idx != -1:
        blok = metin[idx:idx+400]
        xg_values = re.findall(r'\n([\d.]+)\n\d+\n', blok)
        if len(xg_values) >= 2:
            veri["xg_ev"] = float(xg_values[0])
            veri["xg_dep"] = float(xg_values[1])

    if "xg_ev" not in veri or "xg_dep" not in veri:
        xgs = re.findall(r'xG[:\s]+([\d.]+)', metin)
        if len(xgs) >= 2:
            veri["xg_ev"] = float(xgs[0])
            veri["xg_dep"] = float(xgs[1])

    # ---- Atılan ----
    idx = metin.find("Atılan Gol")
    if idx != -1:
        blok = metin[idx:idx+300]
        sayilar = re.findall(r'\n([\d.]+)\n\d+%', blok)
        if len(sayilar) >= 2:
            veri["atilan_ev"] = float(sayilar[0])
            veri["atilan_dep"] = float(sayilar[1])

    if "atilan_ev" not in veri or "atilan_dep" not in veri:
        atilanlar = re.findall(r'Atılan[:\s]+([\d.]+)', metin)
        if len(atilanlar) >= 2:
            veri["atilan_ev"] = float(atilanlar[0])
            veri["atilan_dep"] = float(atilanlar[1])

    # ---- Yenen ----
    idx = metin.find("Yenen Gol")
    if idx != -1:
        blok = metin[idx:idx+300]
        sayilar = re.findall(r'\n([\d.]+)\n\d+%', blok)
        if len(sayilar) >= 2:
            veri["yenen_ev"] = float(sayilar[0])
            veri["yenen_dep"] = float(sayilar[1])

    if "yenen_ev" not in veri or "yenen_dep" not in veri:
        yenenler = re.findall(r'Yenen[:\s]+([\d.]+)', metin)
        if len(yenenler) >= 2:
            veri["yenen_ev"] = float(yenenler[0])
            veri["yenen_dep"] = float(yenenler[1])

    # ---- SS ----
    ss_listesi = re.findall(r'\bSS\s*\n\s*([\d.]+)', metin)
    if len(ss_listesi) >= 2:
        veri["ss_ev"] = float(ss_listesi[0])
        veri["ss_dep"] = float(ss_listesi[1])
    else:
        ss_yeni = re.findall(r'\bSS[:\s]+([\d.]+)', metin)
        if len(ss_yeni) >= 2:
            veri["ss_ev"] = float(ss_yeni[0])
            veri["ss_dep"] = float(ss_yeni[1])

    # ---- Yenilmezlik / Galibiyet / Beraberlik (yeni format) ----
    if "yenilmezlik_ev" not in veri:
        yen_listesi = re.findall(r'Yenilmezlik[:\s]+%?([\d.]+)', metin)
        if len(yen_listesi) >= 2:
            veri["yenilmezlik_ev"] = float(yen_listesi[0])
            veri["yenilmezlik_dep"] = float(yen_listesi[1])

    if "galibiyet_ev" not in veri:
        gal_listesi = re.findall(r'Galibiyet[:\s]+%?([\d.]+)', metin)
        if len(gal_listesi) >= 2:
            veri["galibiyet_ev"] = float(gal_listesi[0])
            veri["galibiyet_dep"] = float(gal_listesi[1])

    if "beraberlik_ev" not in veri:
        ber_listesi = re.findall(r'Beraberlik[:\s]+%?([\d.]+)', metin)
        if len(ber_listesi) >= 2:
            veri["beraberlik_ev"] = float(ber_listesi[0])
            veri["beraberlik_dep"] = float(ber_listesi[1])

    # ---- Üst 2.5 ----
    ust25_listesi = re.findall(r'Üst\s*2\.5\s*Sıklığı[:\s]+%?(\d+)', metin)
    if len(ust25_listesi) >= 2:
        veri["ust25_ev"] = float(ust25_listesi[0])
        veri["ust25_dep"] = float(ust25_listesi[1])

    if "ust25_ev" not in veri:
        m = re.search(r'2\.5 Üst\s*\n\s*(?:\w+\s*\n\s*)?(\d+)%[\s\S]*?(?:\w+\s*\n\s*)?(\d+)%', metin)
        if m:
            veri["ust25_ev"] = float(m.group(1))
            veri["ust25_dep"] = float(m.group(2))

    # ---- KG ----
    kg_sik_listesi = re.findall(r'KG\s*Sıklığı[:\s]+%?(\d+)', metin)
    if len(kg_sik_listesi) >= 2:
        veri["kg_siklik_ev"] = float(kg_sik_listesi[0])
        veri["kg_siklik_dep"] = float(kg_sik_listesi[1])

    if "kg_siklik_ev" not in veri:
        idx = metin.find("KG Sıklığı")
        if idx != -1:
            blok = metin[idx:idx+500]
            m = re.search(r'Ortalama\s*\n\s*(\d+)%', blok)
            if m:
                veri["kg_oran"] = float(m.group(1))
            yuzdeler = re.findall(r'(\d+)%', blok)
            if len(yuzdeler) >= 2:
                veri["kg_siklik_ev"] = float(yuzdeler[0])
                veri["kg_siklik_dep"] = float(yuzdeler[-1])

    if "kg_oran" not in veri:
        if "kg_siklik_ev" in veri and "kg_siklik_dep" in veri:
            veri["kg_oran"] = round((veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2)
        else:
            m = re.search(r'KG Oranı[:\s]+%?(\d+)', metin)
            if m:
                veri["kg_oran"] = float(m.group(1))

    # ==========================================
    # 🆕 ORAN ÇIKARMA
    # ==========================================
    # Format 1: "Casa\n1.85\n|\nE\n4.10\n|\nVisit\n3.80"
    m = re.search(r'Casa\s*\n\s*([\d.]+)\s*\n\s*\|\s*\n\s*E\s*\n\s*([\d.]+)\s*\n\s*\|\s*\n\s*Visit\s*\n\s*([\d.]+)', metin, re.IGNORECASE)
    if m:
        veri["oran_1"] = float(m.group(1))
        veri["oran_x"] = float(m.group(2))
        veri["oran_2"] = float(m.group(3))
    else:
        # Format 2: "Casa 1.85 | E 4.10 | Visit 3.80"
        m = re.search(r'Casa[:\s]+([\d.]+)\s*\|\s*E[:\s]+([\d.]+)\s*\|\s*Visit[:\s]+([\d.]+)', metin, re.IGNORECASE)
        if m:
            veri["oran_1"] = float(m.group(1))
            veri["oran_x"] = float(m.group(2))
            veri["oran_2"] = float(m.group(3))

    # Format 3: "Hat\tOver\tUnder\n2.5\t1.53\t2.40"
    m = re.search(r'2\.5\s*\t?\s*([\d.]+)\s*\t?\s*([\d.]+)', metin)
    if m:
        ust25 = float(m.group(1))
        alt25 = float(m.group(2))
        if 1.0 < ust25 < 20 and 1.0 < alt25 < 20:
            veri["oran_ust25"] = ust25
            veri["oran_alt25"] = alt25

    # BTTS: "Sim 1.50 Não 2.50"
    m = re.search(r'Sim[:\s]+([\d.]+)\s*\n?\s*N[ãa]o[:\s]+([\d.]+)', metin, re.IGNORECASE)
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
    lam_dep_ham = ((hucum_dep + sav_ev) / 2) * DEP_DEZAVANTAJ * form_dep * moral_dep * s ira_dep if False else ((hucum_dep + sav_ev) / 2) * DEP_DEZAVANTAJ * form_dep * moral_dep * sira_dep

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


def takim_form_yorumu(deger: float) -> str:
    if deger > 2.0: return "🟢 Güçlü form"
    if deger < 1.0: return "🔴 Zayıf form"
    return "🟡 Ortalama form"


def veri_yeterli_mi(v: dict) -> bool:
    onemli_alanlar = [
        v["xg_ev"], v["xg_dep"],
        v["atilan_ev"], v["atilan_dep"],
        v["yenen_ev"], v["yenen_dep"],
    ]
    return sum(1 for x in onemli_alanlar if x > 0) >= 2


def oran_olasiligi(oran: float) -> float:
    """Oranı olasılığa çevirir (marj dahil)."""
    if oran <= 1.0:
        return 0.0
    return 100.0 / oran


def normalize_olasilik(oranlar: list) -> list:
    """1X2 gibi marketlerde marjı çıkarıp normalize eder."""
    ham = [100.0 / o if o > 1 else 0 for o in oranlar]
    toplam = sum(ham)
    if toplam <= 0:
        return ham
    return [(h / toplam) * 100 for h in ham]


# ==========================================
# VALUE BET ANALİZİ
# ==========================================
def value_bet_analizi(v: dict, p1: float, px: float, p2: float,
                     ust25_model: float, kg_var_model: float):
    """Model ve piyasa olasılıklarını karşılaştırır."""
    sonuclar = []

    # --- 1X2 ---
    if v.get("oran_1", 0) > 0 and v.get("oran_x", 0) > 0 and v.get("oran_2", 0) > 0:
        piyasa = normalize_olasilik([v["oran_1"], v["oran_x"], v["oran_2"]])
        for isim, model, piy, oran in [
            ("1 (Ev)", p1, piyasa[0], v["oran_1"]),
            ("X (Beraberlik)", px, piyasa[1], v["oran_x"]),
            ("2 (Dep)", p2, piyasa[2], v["oran_2"]),
        ]:
            fark = model - piy
            if fark >= 5:
                karar = "✅ VALUE"
            elif fark >= 2:
                karar = "🟡 Sınırda"
            else:
                karar = "❌ Value yok"
            sonuclar.append(("1X2", isim, model, piy, fark, oran, karar))

    # --- 2.5 Üst/Alt ---
    if v.get("oran_ust25", 0) > 0 and v.get("oran_alt25", 0) > 0:
        piyasa = normalize_olasilik([v["oran_ust25"], v["oran_alt25"]])
        alt25_model = 100 - ust25_model
        for isim, model, piy, oran in [
            ("Üst 2.5", ust25_model, piyasa[0], v["oran_ust25"]),
            ("Alt 2.5", alt25_model, piyasa[1], v["oran_alt25"]),
        ]:
            fark = model - piy
            if fark >= 5:
                karar = "✅ VALUE"
            elif fark >= 2:
                karar = "🟡 Sınırda"
            else:
                karar = "❌ Value yok"
            sonuclar.append(("Üst/Alt 2.5", isim, model, piy, fark, oran, karar))

    # --- KG ---
    if v.get("oran_kg_var", 0) > 0 and v.get("oran_kg_yok", 0) > 0:
        piyasa = normalize_olasilik([v["oran_kg_var"], v["oran_kg_yok"]])
        kg_yok_model = 100 - kg_var_model
        for isim, model, piy, oran in [
            ("KG Var", kg_var_model, piyasa[0], v["oran_kg_var"]),
            ("KG Yok", kg_yok_model, piyasa[1], v["oran_kg_yok"]),
        ]:
            fark = model - piy
            if fark >= 5:
                karar = "✅ VALUE"
            elif fark >= 2:
                karar = "🟡 Sınırda"
            else:
                karar = "❌ Value yok"
            sonuclar.append(("KG", isim, model, piy, fark, oran, karar))

    return sonuclar


# ==========================================
# DETAYLI YORUM
# ==========================================
def detayli_analiz_yorumu(v: dict):
    yorumlar = []

    # FORM
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

    # SIRALAMA
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

    # xG
    xg_ev, xg_dep = v["xg_ev"], v["xg_dep"]
    fark_xg = xg_ev - xg_dep
    if fark_xg >= 0.6:
        txt = f"Ev sahibi hücumda üretken (**xG {xg_ev:.2f}** vs **{xg_dep:.2f}**)."
    elif fark_xg <= -0.6:
        txt = f"Deplasman hücumda daha etkili (**xG {xg_dep:.2f}** vs **{xg_ev:.2f}**)."
    else:
        txt = f"xG yakın (Ev **{xg_ev:.2f}** / Dep **{xg_dep:.2f}**)."
    yorumlar.append(("🎯 HÜCUM (xG)", txt))

    # HÜCUM HAKİMİYETİ
    h_ev, h_dep = v.get("hucum_hakimiyeti_ev", 50), v.get("hucum_hakimiyeti_dep", 50)
    if abs(h_ev - h_dep) >= 10:
        if h_ev > h_dep:
            txt = f"Ev sahibi **%{h_ev:.0f}** hücum hakimiyetiyle oyunu domine ediyor (Dep: %{h_dep:.0f})."
        else:
            txt = f"Deplasman **%{h_dep:.0f}** hücum hakimiyetiyle oyunu yönlendiriyor (Ev: %{h_ev:.0f})."
    else:
        txt = f"Hücum hakimiyeti dengeli (Ev %{h_ev:.0f} / Dep %{h_dep:.0f})."
    yorumlar.append(("⚡ HÜCUM HAKİMİYETİ", txt))

    # AGRESİFLİK
    a_ev, a_dep = v.get("agresiflik_ev", 8), v.get("agresiflik_dep", 8)
    if abs(a_ev - a_dep) >= 2:
        if a_ev > a_dep:
            txt = f"Ev sahibi maç başına **{a_ev:.1f}** şut atıyor (Dep: {a_dep:.1f})."
        else:
            txt = f"Deplasman maç başına **{a_dep:.1f}** şut atıyor (Ev: {a_ev:.1f})."
    else:
        txt = f"Şut sayıları benzer (Ev {a_ev:.1f} / Dep {a_dep:.1f})."
    yorumlar.append(("🎯 AGRESİFLİK", txt))

    # İSABET
    i_ev, i_dep = v.get("isabet_ev", 40), v.get("isabet_dep", 40)
    if abs(i_ev - i_dep) >= 8:
        if i_ev > i_dep:
            txt = f"Ev sahibi şut isabeti **%{i_ev:.0f}** ile keskin (Dep: %{i_dep:.0f})."
        else:
            txt = f"Deplasman şut isabeti **%{i_dep:.0f}** ile etkili (Ev: %{i_ev:.0f})."
    else:
        txt = f"Şut isabeti yakın (Ev %{i_ev:.0f} / Dep %{i_dep:.0f})."
    yorumlar.append(("🎯 İSABET", txt))

    # ATILAN
    at_ev, at_dep = v["atilan_ev"], v["atilan_dep"]
    fark_at = at_ev - at_dep
    if fark_at >= 0.6:
        txt = f"Ev sahibi maç başına **{at_ev:.1f}** gol atıyor, deplasman **{at_dep:.1f}**."
    elif fark_at <= -0.6:
        txt = f"Deplasman maç başına **{at_dep:.1f}** gol atıyor, ev sahibi **{at_ev:.1f}**."
    else:
        txt = f"Atılan goller benzer (Ev **{at_ev:.1f}** / Dep **{at_dep:.1f}**)."
    yorumlar.append(("⚽ ATILAN GOL", txt))

    # SAVUNMA
    y_ev_s, y_dep_s = v["yenen_ev"], v["yenen_dep"]
    fark_ys = y_dep_s - y_ev_s
    if fark_ys >= 0.7:
        txt = f"Ev sahibi savunması sağlam (**{y_ev_s:.1f}**), deplasman zayıf (**{y_dep_s:.1f}**)."
    elif fark_ys <= -0.7:
        txt = f"Deplasman savunması sağlam (**{y_dep_s:.1f}**), ev sahibi zayıf (**{y_ev_s:.1f}**)."
    else:
        txt = f"Savunmalar benzer (Ev **{y_ev_s:.1f}** / Dep **{y_dep_s:.1f}**)."
    yorumlar.append(("🛡️ SAVUNMA", txt))

    # REAKSİYON
    r_ev, r_dep = v["reaksiyon_ev"], v["reaksiyon_dep"]
    fark_r = r_ev - r_dep
    if fark_r >= 15:
        txt = f"Ev sahibi reaksiyon gücü yüksek (**%{r_ev:.0f}** vs **%{r_dep:.0f}**)."
    elif fark_r <= -15:
        txt = f"Deplasman reaksiyon gücü yüksek (**%{r_dep:.0f}** vs **%{r_ev:.0f}**)."
    else:
        txt = f"Reaksiyon güçleri benzer (Ev **%{r_ev:.0f}** / Dep **%{r_dep:.0f}**)."
    yorumlar.append(("💪 REAKSİYON", txt))

    # İSTİKRAR
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


# ==========================================
# FAVORİ KOMBO
# ==========================================
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


# ==========================================
# SAYFA 1: YAPIŞTIRMA
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
        placeholder="İstatistik sitesinden TÜM metni + oranları buraya yapıştır.\n\n"
                    "Örnek:\n"
                    "PPG: 1.2 | Sıra: 19 | Reak: %40\n"
                    "xG: 1.17 | Atılan: 1.4 | Yenen: 1.2\n"
                    "...\n"
                    "Casa\n1.85\n|\nE\n4.10\n|\nVisit\n3.80\n"
                    "2.5\t1.53\t2.40\n"
                    "Sim\n1.50\nNão\n2.50"
    )

    st.divider()

    analiz_btn = st.button("🚀 ANALİZ ET", use_container_width=True, type="primary")

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

                if not veri_yeterli_mi(yeni_veri):
                    st.error(f"⚠️ Sadece {len(cikan)} alan bulundu. En az 2 gol verisi gerekli.")
                    st.info(f"Bulunan alanlar: {', '.join(cikan.keys())}")
                else:
                    st.session_state.sayfa = "sonuc"
                    st.rerun()


# ==========================================
# SAYFA 2: DETAYLI ANALİZ
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri

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

    st.markdown("<h1>🎯 Detaylı Analiz Raporu</h1>", unsafe_allow_html=True)

    fark = p1 - p2
    if fark > 25:       senaryo = "Ev sahibi açık ara favori görünüyor."
    elif fark > 10:     senaryo = "Ev sahibi hafif favori konumunda."
    elif fark < -25:    senaryo = "Deplasman ekibi net favori."
    elif fark < -10:    senaryo = "Deplasman hafif favori."
    else:               senaryo = "Maç oldukça dengeli, beraberlik riski yüksek."

    with st.expander("📋 Analizde Kullanılan Tüm Veriler", expanded=False):
        st.markdown(f"""
        **🏠 Ev:** PPG {v['ppg_ev']} | Sıra {v['siralama_ev']} | xG {v['xg_ev']} | Atılan {v['atilan_ev']} | Yenen {v['yenen_ev']}

        **✈️ Dep:** MPG {v['mpg_dep']} | Sıra {v['siralama_dep']} | xG {v['xg_dep']} | Atılan {v['atilan_dep']} | Yenen {v['yenen_dep']}

        **📊 Oranlar:** 1: {v.get('oran_1', 0)} | X: {v.get('oran_x', 0)} | 2: {v.get('oran_2', 0)}
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
        - 🛡️ **En Güvenli Bahis:** Çifte Şans **{en_guvenli[0]}** → 1X: %{cifte_1x:.1f} • X2: %{cifte_x2:.1f} • 12: %{cifte_12:.1f}
        - ⚽ **Gol Tercihi:** **{'2.5 Üst' if tahmini_gol > 2.6 else '2.5 Alt'}** (beklenen: {tahmini_gol:.2f}) → Üst: %{ust_25:.0f} • Alt: %{100-ust_25:.0f}
        - 🤝 **KG Tercihi:** **{'KG Var' if kg_ort > 55 else 'KG Yok' if kg_ort < 45 else 'Belirsiz'}** → Var: %{kg_ort:.0f} • Yok: %{100-kg_ort:.0f}
        - 📈 **İkinci Tercih:** {'X2' if p1 > p2 else '1X'} (%{max(cifte_1x, cifte_x2):.1f})
        """)

    # 🆕 VALUE BET ANALİZİ
    vb = value_bet_analizi(v, p1, px, p2, ust_25, kg_var_model)
    if vb:
        with st.expander("💎 Value Bet Analizi (Model vs Piyasa)", expanded=True):
            st.markdown("**Model ile piyasa karşılaştırması:**")
            for market, isim, model, piy, fark, oran, karar in vb:
                st.markdown(f"**{market} — {isim}** (Oran {oran})")
                st.markdown(f"Model: **%{model:.1f}** | Piyasa: **%{piy:.1f}** | Fark: **{fark:+.1f}** {karar}")
                st.markdown("")

            # En iyi value bet
            en_iyi_vb = max(vb, key=lambda x: x[4])
            if en_iyi_vb[4] >= 5:
                st.success(f"🔥 **En Değerli Bahis:** {en_iyi_vb[1]} @ {en_iyi_vb[5]} → %{en_iyi_vb[4]:+.1f} fark")
    else:
        with st.expander("💎 Value Bet Analizi", expanded=False):
            st.info("ℹ️ Oran bulunamadı. Value bet analizi için oranları da yapıştır.")

    with st.expander("🎰 Favori Komboları", expanded=True):
        kombolar, favoriler = favori_kombolar(matris, MAX_GOL)
        st.markdown(f"**Favoriler:** `{favoriler[0]}` • `{favoriler[1]}` • `{favoriler[2]}`")
        for isim, yuzde in kombolar:
            emoji = "🟢" if yuzde >= 50 else "🟡" if yuzde >= 35 else "🔴"
            st.markdown(f"{emoji} **{isim}** → %{yuzde:.1f}")
        en_iyi = kombolar[0]
        st.success(f"🔥 **En İyi Kombo:** {en_iyi[0]} → %{en_iyi[1]:.1f}")

    st.divider()

    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.form_version += 1
        st.session_state.sayfa = "giris"
        st.rerun()
