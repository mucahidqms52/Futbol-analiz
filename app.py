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

    m = re.search(r'Casa\s*\n\s*([\d.]+)\s*\n\s*\|\s*\n\s*(?:E|Empate)\s*\n\s*([\d.]+)\s*\n\s*\|\s*\n\s*(?:Visit|Fora)\s*\n\s*([\d.]+)', metin, re.IGNORECASE)
    if m:
        veri["oran_1"] = float(m.group(1))
        veri["oran_x"] = float(m.group(2))
        veri["oran_2"] = float(m.group(3))

    m = re.search(r'2\.5\s*\t?\s*([\d.]+)\s*\t?\s*([\d.]+)', metin)
    if m:
        ust25 = float(m.group(1))
        alt25 = float(m.group(2))
        if 1.0 < ust25 < 20 and 1.0 < alt25 < 20:
            veri["oran_ust25"] = ust25
            veri["oran_alt25"] = alt25

    m = re.search(r'Sim\s*\n\s*([\d.]+)\s*\n\s*N[ãa]o\s*\n\s*([\d.]+)', metin, re.IGNORECASE)
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


def normalize_olasilik(oranlar: list) -> list:
    ham = [100.0 / o if o > 1 else 0 for o in oranlar]
    toplam = sum(ham)
    if toplam <= 0:
        return ham
    return [(h / toplam) * 100 for h in ham]


# ==========================================
# VALUE BET ANALİZİ
# ==========================================
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


# ==========================================
# FAVORİ KOMBOLAR
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
# VALUE BAZLI KOMBOLAR
# ==========================================
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
                    return lambda i,
