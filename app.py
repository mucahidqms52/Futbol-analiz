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
# VARSAYILAN VERİ (20+ ALAN)
# ==========================================
VARSAYILAN_VERI = {
    # Form
    "ppg_ev": 0.0, "mpg_dep": 0.0,
    # Sıralama
    "siralama_ev": 1, "siralama_dep": 1,
    # Reaksiyon
    "reaksiyon_ev": 50.0, "reaksiyon_dep": 50.0,
    # xG
    "xg_ev": 0.0, "xg_dep": 0.0,
    # Atılan
    "atilan_ev": 0.0, "atilan_dep": 0.0,
    # Yenen
    "yenen_ev": 0.0, "yenen_dep": 0.0,
    # Standart Sapma
    "ss_ev": 1.0, "ss_dep": 1.0,
    # KG
    "kg_oran": 50.0,
    # 🆕 Galibiyet/Beraberlik/Mağlubiyet
    "galibiyet_ev": 30.0, "beraberlik_ev": 30.0,
    "galibiyet_dep": 30.0, "beraberlik_dep": 30.0,
    # 🆕 Yenilmezlik
    "yenilmezlik_ev": 30.0, "yenilmezlik_dep": 30.0,
    # 🆕 Hücum Hakimiyeti
    "hucum_hakimiyeti_ev": 50.0, "hucum_hakimiyeti_dep": 50.0,
    # 🆕 Agresiflik (Şut/Maç)
    "agresiflik_ev": 8.0, "agresiflik_dep": 8.0,
    # 🆕 İsabet (%)
    "isabet_ev": 40.0, "isabet_dep": 40.0,
    # 🆕 Hava Topu (Ortalar)
    "hava_topu_ev": 10.0, "hava_topu_dep": 10.0,
    # 🆕 İlk Golü Atar / Yer
    "ilk_gol_atar_ev": 40.0, "ilk_gol_atar_dep": 40.0,
    "ilk_gol_yer_ev": 40.0, "ilk_gol_yer_dep": 40.0,
    # 🆕 Üst Sıklıkları
    "ust05_ev": 80.0, "ust05_dep": 80.0,
    "ust15_ev": 50.0, "ust15_dep": 50.0,
    "ust25_ev": 30.0, "ust25_dep": 30.0,
    "ust35_ev": 20.0, "ust35_dep": 20.0,
    # 🆕 KG Sıklığı (Takım bazlı)
    "kg_siklik_ev": 50.0, "kg_siklik_dep": 50.0,
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
# METİNDEN VERİ ÇIKARMA (GENİŞLETİLMİŞ)
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

    # ---- Galibiyet/Beraberlik/Mağlubiyet (Ev) ----
    # PPG bloğundan sonra 3 satırda yüzdeler var
    idx_ppg = metin.find("PPG")
    if idx_ppg != -1:
        blok = metin[idx_ppg:idx_ppg+400]
        # Sırayla Galibiyet, Beraberlik, Mağlubiyet
        m_g = re.search(r'([\d.]+)%\s*Galibiyet', blok)
        m_b = re.search(r'([\d.]+)%\s*Beraberlik', blok)
        m_m = re.search(r'([\d.]+)%\s*Mağlubiyet', blok)
        if m_g: veri["galibiyet_ev"] = float(m_g.group(1))
        if m_b: veri["beraberlik_ev"] = float(m_b.group(1))
        # Yenilmezlik / Invencibilidade
        m_y = re.search(r'(?:Invencibilidade|Yenilmezlik)[:\s]+([\d.]+)%', blok)
        if m_y: veri["yenilmezlik_ev"] = float(m_y.group(1))

    # ---- Galibiyet/Beraberlik/Mağlubiyet (Dep) ----
    idx_mbp = metin.find("MBP")
    if idx_mbp == -1:
        idx_mbp = metin.find("MPG")
    if idx_mbp != -1:
        blok = metin[idx_mbp:idx_mbp+400]
        m_g = re.search(r'([\d.]+)%\s*Galibiyet', blok)
        m_b = re.search(r'([\d.]+)%\s*Beraberlik', blok)
        m_m = re.search(r'([\d.]+)%\s*Mağlubiyet', blok)
        if m_g: veri["galibiyet_dep"] = float(m_g.group(1))
        if m_b: veri["beraberlik_dep"] = float(m_b.group(1))
        m_y = re.search(r'(?:Invencibilidade|Yenilmezlik)[:\s]+([\d.]+)%', blok)
        if m_y: veri["yenilmezlik_dep"] = float(m_y.group(1))

    # ---- Sıralama ----
    idx = metin.find("Tablo Pozisyonu")
    if idx == -1:
        idx = metin.find("Pozisyon")
    if idx != -1:
        blok = metin[idx:idx+600]
        sayilar = re.findall(r'\n(\d{1,2})\n', blok)
        if len(sayilar) >= 2:
            veri["siralama_ev"] = int(sayilar[0])
            veri["siralama_dep"] = int(sayilar[1])

    # ---- Hücum Hakimiyeti ----
    idx = metin.find("Hücum Hakimiyeti")
    if idx != -1:
        blok = metin[idx:idx+300]
        sayilar = re.findall(r'([\d.]+)%', blok)
        if len(sayilar) >= 2:
            veri["hucum_hakimiyeti_ev"] = float(sayilar[0])
            veri["hucum_hakimiyeti_dep"] = float(sayilar[1])

    # ---- Agresiflik (Şut/Maç) ----
    idx = metin.find("Agresiflik")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)\s*[·•]\s*([\d.]+)', blok)
        if m:
            veri["agresiflik_ev"] = float(m.group(1))
            veri["agresiflik_dep"] = float(m.group(2))

    # ---- İsabet (Doğruluk) ----
    idx = metin.find("İsabet")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)%\s*[·•]\s*([\d.]+)%', blok)
        if m:
            veri["isabet_ev"] = float(m.group(1))
            veri["isabet_dep"] = float(m.group(2))

    # ---- Hava Topu (Ortalar) ----
    idx = metin.find("Hava Topu")
    if idx != -1:
        blok = metin[idx:idx+200]
        m = re.search(r'([\d.]+)\s*[·•]\s*([\d.]+)', blok)
        if m:
            veri["hava_topu_ev"] = float(m.group(1))
            veri["hava_topu_dep"] = float(m.group(2))

    # ---- Psikolojik Faktör: İlk Gol ----
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

    # ---- Reaksiyon Gücü ----
    m = re.search(r'Reaksiyon Gücü\s*\t?\s*([\d.]+)%\s*\t?\s*([\d.]+)%', metin)
    if m:
        veri["reaksiyon_ev"] = float(m.group(1))
        veri["reaksiyon_dep"] = float(m.group(2))

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

    # ---- Atılan Gol ----
    idx = metin.find("Atılan Gol")
    if idx != -1:
        blok = metin[idx:idx+300]
        sayilar = re.findall(r'\n([\d.]+)\n\d+%', blok)
        if len(sayilar) >= 2:
            veri["atilan_ev"] = float(sayilar[0])
            veri["atilan_dep"] = float(sayilar[1])

    # ---- Yenen Gol ----
    idx = metin.find("Yenen Gol")
    if idx != -1:
        blok = metin[idx:idx+300]
        sayilar = re.findall(r'\n([\d.]+)\n\d+%', blok)
        if len(sayilar) >= 2:
            veri["yenen_ev"] = float(sayilar[0])
            veri["yenen_dep"] = float(sayilar[1])

    # ---- Standart Sapma ----
    ss_listesi = re.findall(r'\bSS\s*\n\s*([\d.]+)', metin)
    if len(ss_listesi) >= 2:
        veri["ss_ev"] = float(ss_listesi[0])
        veri["ss_dep"] = float(ss_listesi[1])

    # ---- Üst Sıklıkları ----
    # 0.5 Üst: Alverca 90%, Rio Ave 70%
    m = re.search(r'0\.5 Üst\s*\n\s*(?:\w+\s*\n\s*)?(\d+)%[\s\S]*?(?:\w+\s*\n\s*)?(\d+)%', metin)
    if m:
        veri["ust05_ev"] = float(m.group(1))
        veri["ust05_dep"] = float(m.group(2))

    m = re.search(r'1\.5 Üst\s*\n\s*(?:\w+\s*\n\s*)?(\d+)%[\s\S]*?(?:\w+\s*\n\s*)?(\d+)%', metin)
    if m:
        veri["ust15_ev"] = float(m.group(1))
        veri["ust15_dep"] = float(m.group(2))

    m = re.search(r'2\.5 Üst\s*\n\s*(?:\w+\s*\n\s*)?(\d+)%[\s\S]*?(?:\w+\s*\n\s*)?(\d+)%', metin)
    if m:
        veri["ust25_ev"] = float(m.group(1))
        veri["ust25_dep"] = float(m.group(2))

    m = re.search(r'3\.5 Üst\s*\n\s*(?:\w+\s*\n\s*)?(\d+)%[\s\S]*?(?:\w+\s*\n\s*)?(\d+)%', metin)
    if m:
        veri["ust35_ev"] = float(m.group(1))
        veri["ust35_dep"] = float(m.group(2))

    # ---- KG Oranı (ortalama) ve KG Sıklığı (takım) ----
    idx = metin.find("KG Sıklığı")
    if idx != -1:
        blok = metin[idx:idx+500]
        m = re.search(r'Ortalama\s*\n\s*(\d+)%', blok)
        if m:
            veri["kg_oran"] = float(m.group(1))
        # Takım KG sıklıkları (ilk ve son yüzde)
        yuzdeler = re.findall(r'(\d+)%', blok)
        if len(yuzdeler) >= 2:
            # İlk = Alverca/Ev, son = Rio Ave/Dep
            veri["kg_siklik_ev"] = float(yuzdeler[0])
            veri["kg_siklik_dep"] = float(yuzdeler[-1])

    return veri


# ==========================================
# İŞ MANTIĞI (GELİŞMİŞ FORMÜLASYON)
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
    # Ana hücum gücü
    hucum_ev = v["xg_ev"] * 0.6 + v["atilan_ev"] * 0.4
    hucum_dep = v["xg_dep"] * 0.6 + v["atilan_dep"] * 0.4

    # 🆕 İsabet çarpanı (şut doğruluğu → hücum verimliliği)
    isabet_kat_ev = 1 + (v.get("isabet_ev", 40) - 40) / 250
    isabet_kat_dep = 1 + (v.get("isabet_dep", 40) - 40) / 250

    # 🆕 Hücum hakimiyeti
    hak_kat_ev = 1 + (v.get("hucum_hakimiyeti_ev", 50) - 50) / 250
    hak_kat_dep = 1 + (v.get("hucum_hakimiyeti_dep", 50) - 50) / 250

    # 🆕 Galibiyet oranı (son 10 maç)
    gal_kat_ev = 1 + (v.get("galibiyet_ev", 30) - 30) / 300
    gal_kat_dep = 1 + (v.get("galibiyet_dep", 30) - 30) / 300

    # 🆕 İlk golü atma
    ilk_kat_ev = 1 + (v.get("ilk_gol_atar_ev", 40) - 40) / 400
    ilk_kat_dep = 1 + (v.get("ilk_gol_atar_dep", 40) - 40) / 400

    # 🆕 Agresiflik (şut sayısı)
    agres_kat_ev = 1 + (v.get("agresiflik_ev", 8) - 8) / 50
    agres_kat_dep = 1 + (v.get("agresiflik_dep", 8) - 8) / 50

    # 🆕 Hava topu (duran top gücü)
    hava_kat_ev = 1 + (v.get("hava_topu_ev", 10) - 10) / 100
    hava_kat_dep = 1 + (v.get("hava_topu_dep", 10) - 10) / 100

    # Hücum gücünü ağırlıklandır
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


# ==========================================
# GENİŞ KAPSAMLI YORUM (GENİŞLETİLMİŞ)
# ==========================================
def detayli_analiz_yorumu(v: dict):
    yorumlar = []

    # FORM
    ppg, mpg = v["ppg_ev"], v["mpg_dep"]
    fark = ppg - mpg
    if ppg >= 2.0 and mpg <= 1.0:
        txt = f"Ev sahibi evinde mükemmel bir form yakalamış (**PPG {ppg:.2f}**), deplasman deplasmanda zorlanıyor (**MPG {mpg:.2f}**). Ev sahibi açık ara üstün."
    elif fark >= 0.7:
        txt = f"Ev sahibi form olarak önde (**PPG {ppg:.2f}** vs **{mpg:.2f}**). Sahasında kaybetmeye alışkın değil."
    elif fark <= -0.7:
        txt = f"Deplasman form olarak önde (**MPG {mpg:.2f}** vs **PPG {ppg:.2f}**). Deplasmanda iyi performans sergiliyor."
    else:
        txt = f"Form dengeli (**PPG {ppg:.2f}** vs **MPG {mpg:.2f}**)."
    yorumlar.append(("📈 FORM", txt))

    # GALİBİYET ORANI
    g_ev, g_dep = v.get("galibiyet_ev", 0), v.get("galibiyet_dep", 0)
    if g_ev > 0 or g_dep > 0:
        if g_ev >= g_dep + 20:
            txt = f"Son maçlarda ev sahibi **%{g_ev:.0f}** galibiyet oranıyla açık ara üstün (Dep: %{g_dep:.0f}). Kazanma alışkanlığı yüksek."
        elif g_dep >= g_ev + 20:
            txt = f"Deplasman **%{g_dep:.0f}** galibiyet oranıyla önde (Ev: %{g_ev:.0f}). Deplasman formda."
        else:
            txt = f"Galibiyet oranları yakın (Ev %{g_ev:.0f} / Dep %{g_dep:.0f})."
        yorumlar.append(("🏅 GALİBİYET ORANI", txt))

    # YENİLMEZLİK
    y_ev, y_dep = v.get("yenilmezlik_ev", 0), v.get("yenilmezlik_dep", 0)
    if y_ev > 0 or y_dep > 0:
        if y_ev >= 50:
            txt = f"Ev sahibi **%{y_ev:.0f}** yenilmezlik oranıyla çok sağlam. Kolay kaybetmiyor."
        elif y_dep >= 50:
            txt = f"Deplasman **%{y_dep:.0f}** yenilmezlik oranıyla dirençli. Zor mağlup oluyor."
        else:
            txt = f"Yenilmezlik oranları düşük (Ev %{y_ev:.0f} / Dep %{y_dep:.0f}). İkisi de mağlubiyet görebiliyor."
        yorumlar.append(("💎 YENİLMEZLİK", txt))

    # SIRALAMA
    s_ev, s_dep = v["siralama_ev"], v["siralama_dep"]
    fark_sira = s_dep - s_ev
    if fark_sira >= 8:
        txt = f"Ev sahibi **{s_ev}.** sırada, deplasman **{s_dep}.** sırada. Aradaki **{fark_sira} basamak** ciddi güç farkı."
    elif fark_sira >= 3:
        txt = f"Ev sahibi **{s_ev}.**, deplasman **{s_dep}.** sırada. Ev sahibi üstün konumda."
    elif fark_sira <= -8:
        txt = f"Deplasman **{s_dep}.**, ev sahibi **{s_ev}.** sırada. Deplasman **{abs(fark_sira)} basamak** yukarıda, sürpriz yapabilir."
    elif fark_sira <= -3:
        txt = f"Deplasman **{s_dep}.**, ev sahibi **{s_ev}.** sırada. Deplasman biraz üstün."
    else:
        txt = f"Sıralamalar yakın (Ev **{s_ev}.** / Dep **{s_dep}.**). Dengeli eşleşme."
    yorumlar.append(("🏆 SIRALAMA", txt))

    # xG
    xg_ev, xg_dep = v["xg_ev"], v["xg_dep"]
    fark_xg = xg_ev - xg_dep
    if fark_xg >= 0.6:
        txt = f"Ev sahibi hücumda üretken (**xG {xg_ev:.2f}** vs **{xg_dep:.2f}**). Deplasman savunması zorlanabilir."
    elif fark_xg <= -0.6:
        txt = f"Deplasman hücumda daha etkili (**xG {xg_dep:.2f}** vs **{xg_ev:.2f}**). Ev sahibi savunmada dikkatli olmalı."
    else:
        txt = f"xG değerleri yakın (Ev **{xg_ev:.2f}** / Dep **{xg_dep:.2f}**)."
    yorumlar.append(("🎯 HÜCUM (xG)", txt))

    # 🆕 HÜCUM HAKİMİYETİ
    h_ev, h_dep = v.get("hucum_hakimiyeti_ev", 50), v.get("hucum_hakimiyeti_dep", 50)
    if abs(h_ev - h_dep) >= 10:
        if h_ev > h_dep:
            txt = f"Ev sahibi **%{h_ev:.0f}** topa sahip olma/tehlikeli atak üstünlüğüyle oyunu domine ediyor (Dep: %{h_dep:.0f})."
        else:
            txt = f"Deplasman **%{h_dep:.0f}** hücum hakimiyeti ile oyunu yönlendiriyor (Ev: %{h_ev:.0f})."
    else:
        txt = f"Hücum hakimiyeti dengeli (Ev %{h_ev:.0f} / Dep %{h_dep:.0f})."
    yorumlar.append(("⚡ HÜCUM HAKİMİYETİ", txt))

    # 🆕 AGRESİFLİK (ŞUT/MAÇ)
    a_ev, a_dep = v.get("agresiflik_ev", 8), v.get("agresiflik_dep", 8)
    if abs(a_ev - a_dep) >= 2:
        if a_ev > a_dep:
            txt = f"Ev sahibi maç başına **{a_ev:.1f}** şut atıyor (Dep: {a_dep:.1f}). Rakip kaleye çok gidiyor."
        else:
            txt = f"Deplasman maç başına **{a_dep:.1f}** şut atıyor (Ev: {a_ev:.1f}). Daha agresif hücum ediyor."
    else:
        txt = f"Şut sayıları benzer (Ev {a_ev:.1f} / Dep {a_dep:.1f})."
    yorumlar.append(("🎯 AGRESİFLİK (Şut)", txt))

    # 🆕 İSABET
    i_ev, i_dep = v.get("isabet_ev", 40), v.get("isabet_dep", 40)
    if abs(i_ev - i_dep) >= 8:
        if i_ev > i_dep:
            txt = f"Ev sahibi şut isabeti **%{i_ev:.0f}** ile keskin nişancı (Dep: %{i_dep:.0f}). Az pozisyonu gole çeviriyor."
        else:
            txt = f"Deplasman şut isabeti **%{i_dep:.0f}** ile etkili (Ev: %{i_ev:.0f}). Fırsatları iyi değerlendiriyor."
    else:
        txt = f"Şut isabeti yakın (Ev %{i_ev:.0f} / Dep %{i_dep:.0f})."
    yorumlar.append(("🎯 İSABET (Doğruluk)", txt))

    # 🆕 HAVA TOPU (ORTALAR)
    ht_ev, ht_dep = v.get("hava_topu_ev", 10), v.get("hava_topu_dep", 10)
    if abs(ht_ev - ht_dep) >= 3:
        if ht_ev > ht_dep:
            txt = f"Ev sahibi maç başına **{ht_ev:.0f}** orta yapıyor (Dep: {ht_dep:.0f}). Kanat oyunu ve duran top silahı güçlü."
        else:
            txt = f"Deplasman **{ht_dep:.0f}** orta yapıyor (Ev: {ht_ev:.0f}). Kanatları iyi kullanıyor."
    else:
        txt = f"Orta sayıları benzer (Ev {ht_ev:.0f} / Dep {ht_dep:.0f})."
    yorumlar.append(("📡 HAVA TOPU (Ortalar)", txt))

    # ATILAN
    at_ev, at_dep = v["atilan_ev"], v["atilan_dep"]
    fark_at = at_ev - at_dep
    if fark_at >= 0.6:
        txt = f"Ev sahibi maç başına **{at_ev:.1f}** gol atıyor, deplasman **{at_dep:.1f}**. Gerçekleşen performansta üstün."
    elif fark_at <= -0.6:
        txt = f"Deplasman maç başına **{at_dep:.1f}** gol atıyor, ev sahibi **{at_ev:.1f}**. Deplasman hücumda daha verimli."
    else:
        txt = f"Atılan goller benzer (Ev **{at_ev:.1f}** / Dep **{at_dep:.1f}**)."
    yorumlar.append(("⚽ ATILAN GOL", txt))

    # SAVUNMA
    y_ev_s, y_dep_s = v["yenen_ev"], v["yenen_dep"]
    fark_ys = y_dep_s - y_ev_s
    if fark_ys >= 0.7:
        txt = f"Ev sahibi savunması sağlam (**{y_ev_s:.1f}**/maç), deplasman zayıf (**{y_dep_s:.1f}**). Deplasman gol yiyebilir."
    elif fark_ys <= -0.7:
        txt = f"Deplasman savunması sağlam (**{y_dep_s:.1f}**/maç), ev sahibi zayıf (**{y_ev_s:.1f}**). Deplasman gol bulabilir."
    else:
        txt = f"Savunmalar benzer (Ev **{y_ev_s:.1f}** / Dep **{y_dep_s:.1f}**)."
    yorumlar.append(("🛡️ SAVUNMA", txt))

    # 🆕 İLK GOLÜ ATAR
    iga_ev = v.get("ilk_gol_atar_ev", 40)
    iga_dep = v.get("ilk_gol_atar_dep", 40)
    if abs(iga_ev - iga_dep) >= 10:
        if iga_ev > iga_dep:
            txt = f"Ev sahibi ilk golü **%{iga_ev:.0f}** oranında atıyor (Dep: %{iga_dep:.0f}). Öne geçme alışkanlığı var."
        else:
            txt = f"Deplasman ilk golü **%{iga_dep:.0f}** oranında atıyor (Ev: %{iga_ev:.0f}). Erken gol potansiyeli yüksek."
    else:
        txt = f"İlk golü atma oranları yakın (Ev %{iga_ev:.0f} / Dep %{iga_dep:.0f})."
    yorumlar.append(("⚡ İLK GOLÜ ATAR", txt))

    # 🆕 İLK GOLÜ YER
    igy_ev = v.get("ilk_gol_yer_ev", 40)
    igy_dep = v.get("ilk_gol_yer_dep", 40)
    if abs(igy_ev - igy_dep) >= 10:
        if igy_ev > igy_dep:
            txt = f"Ev sahibi ilk golü **%{igy_ev:.0f}** oranında yiyor (Dep: %{igy_dep:.0f}). Erken gol riski yüksek."
        else:
            txt = f"Deplasman ilk golü **%{igy_dep:.0f}** oranında yiyor (Ev: %{igy_ev:.0f}). Erken gol yeme riski var."
    else:
        txt = f"İlk golü yeme oranları yakın (Ev %{igy_ev:.0f} / Dep %{igy_dep:.0f})."
    yorumlar.append(("🥅 İLK GOLÜ YER", txt))

    # REAKSİYON
    r_ev, r_dep = v["reaksiyon_ev"], v["reaksiyon_dep"]
    fark_r = r_ev - r_dep
    if fark_r >= 15:
        txt = f"Ev sahibi reaksiyon gücü yüksek (**%{r_ev:.0f}** vs **%{r_dep:.0f}**). Geriye düştüğünde toparlanma kabiliyeti fazla."
    elif fark_r <= -15:
        txt = f"Deplasman reaksiyon gücü yüksek (**%{r_dep:.0f}** vs **%{r_ev:.0f}**). Skor dezavantajında pes etmiyor."
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
            txt = f"Ev sahibi **{istikrar(ss_ev)}** (SS {ss_ev:.2f}), deplasman **{istikrar(ss_dep)}** (SS {ss_dep:.2f}). Ev sahibi daha güvenilir."
        else:
            txt = f"Deplasman **{istikrar(ss_dep)}** (SS {ss_dep:.2f}), ev sahibi **{istikrar(ss_ev)}** (SS {ss_ev:.2f}). Deplasman daha öngörülebilir."
    else:
        txt = f"İstikrar seviyeleri benzer (Ev **{ss_ev:.2f}** / Dep **{ss_dep:.2f}**)."
    yorumlar.append(("📊 İSTİKRAR", txt))

    # 🆕 ÜST SIKLIKLARI (Takım bazlı)
    u25_ev, u25_dep = v.get("ust25_ev", 30), v.get("ust25_dep", 30)
    if u25_ev > 0 or u25_dep > 0:
        if u25_ev >= 50 or u25_dep >= 50:
            txt = f"Üst 2.5 gol sıklığı: Ev **%{u25_ev:.0f}** / Dep **%{u25_dep:.0f}**. En az bir takım sık gol görüyor → Üst sinyali."
        elif u25_ev <= 20 and u25_dep <= 20:
            txt = f"Üst 2.5 gol sıklığı düşük: Ev **%{u25_ev:.0f}** / Dep **%{u25_dep:.0f}**. Alt sinyali güçlü."
        else:
            txt = f"Üst 2.5 sıklığı: Ev **%{u25_ev:.0f}** / Dep **%{u25_dep:.0f}**. Kararsız sinyal."
        yorumlar.append(("📈 ÜST 2.5 SIKLIĞI", txt))

    # 🆕 KG SIKLIĞI (Takım bazlı)
    kg_ev, kg_dep = v.get("kg_siklik_ev", 50), v.get("kg_siklik_dep", 50)
    if abs(kg_ev - kg_dep) >= 20 or kg_ev >= 70 or kg_dep >= 70:
        if kg_ev > kg_dep:
            txt = f"Ev sahibi **%{kg_ev:.0f}** oranında KG görüyor (Dep: %{kg_dep:.0f}). Maçlarında karşılıklı gol sık."
        elif kg_dep > kg_ev:
            txt = f"Deplasman **%{kg_dep:.0f}** oranında KG görüyor (Ev: %{kg_ev:.0f}). Deplasman maçlarında gol karşılıklı."
        yorumlar.append(("🥅 KG SIKLIĞI", txt))

    return yorumlar


# ==========================================
# FAVORİ KOMBO ÜRETİCİ
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
        "<p style='text-align:center; color:gray;'>İstatistik sitesinden metni kopyala → yapıştır → analiz et.</p>",
        unsafe_allow_html=True
    )

    st.markdown("### 📋 İstatistik Metnini Yapıştır")

    yapistir_metni = st.text_area(
        "Yapıştırma alanı",
        height=250,
        key="yapistir_input",
        label_visibility="collapsed",
        placeholder="İstatistik sitesinden kopyaladığın TÜM metni buraya yapıştır.\n\n"
                    "Ne kadar çok veri olursa analiz o kadar detaylı olur:\n"
                    "PPG, MBP, Galibiyet %, Beraberlik %, İsabet %, Agresiflik, "
                    "Hücum Hakimiyeti, İlk Gol, Üst Sıklıkları, KG Sıklığı..."
    )

    st.divider()

    analiz_btn = st.button("🚀 ANALİZ ET", use_container_width=True, type="primary")

    if analiz_btn:
        if not yapistir_metni.strip():
            st.warning("⚠️ Önce metni yapıştır.")
        else:
            cikan = metinden_veri_cikar(yapistir_metni)
            if not cikan:
                st.error("❌ Metinden hiçbir veri çıkarılamadı. Formatı kontrol et.")
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

    # ---- KULLANILAN VERİLER ----
    with st.expander("📋 Analizde Kullanılan Tüm Veriler", expanded=False):
        st.markdown(f"""
        **🏠 Ev Sahibi**
        - PPG: {v['ppg_ev']} | Sıra: {v['siralama_ev']}
        - Reak: %{v['reaksiyon_ev']:.0f} | Yenilmezlik: %{v.get('yenilmezlik_ev', 0):.0f}
        - Galibiyet: %{v.get('galibiyet_ev', 0):.0f} | Beraberlik: %{v.get('beraberlik_ev', 0):.0f}
        - xG: {v['xg_ev']} | Atılan: {v['atilan_ev']} | Yenen: {v['yenen_ev']}
        - SS: {v['ss_ev']} | İsabet: %{v.get('isabet_ev', 0):.0f}
        - Agresiflik: {v.get('agresiflik_ev', 0):.1f} şut/maç
        - Hücum Hakimiyeti: %{v.get('hucum_hakimiyeti_ev', 0):.0f}
        - Hava Topu: {v.get('hava_topu_ev', 0):.0f} orta
        - İlk Golü Atar: %{v.get('ilk_gol_atar_ev', 0):.0f} | Yer: %{v.get('ilk_gol_yer_ev', 0):.0f}
        - Üst 2.5 Sıklığı: %{v.get('ust25_ev', 0):.0f} | KG Sıklığı: %{v.get('kg_siklik_ev', 0):.0f}

        **✈️ Deplasman**
        - MPG: {v['mpg_dep']} | Sıra: {v['siralama_dep']}
        - Reak: %{v['reaksiyon_dep']:.0f} | Yenilmezlik: %{v.get('yenilmezlik_dep', 0):.0f}
        - Galibiyet: %{v.get('galibiyet_dep', 0):.0f} | Beraberlik: %{v.get('beraberlik_dep', 0):.0f}
        - xG: {v['xg_dep']} | Atılan: {v['atilan_dep']} | Yenen: {v['yenen_dep']}
        - SS: {v['ss_dep']} | İsabet: %{v.get('isabet_dep', 0):.0f}
        - Agresiflik: {v.get('agresiflik_dep', 0):.1f} şut/maç
        - Hücum Hakimiyeti: %{v.get('hucum_hakimiyeti_dep', 0):.0f}
        - Hava Topu: {v.get('hava_topu_dep', 0):.0f} orta
        - İlk Golü Atar: %{v.get('ilk_gol_atar_dep', 0):.0f} | Yer: %{v.get('ilk_gol_yer_dep', 0):.0f}
        - Üst 2.5 Sıklığı: %{v.get('ust25_dep', 0):.0f} | KG Sıklığı: %{v.get('kg_siklik_dep', 0):.0f}

        **🤝 Ortak:** KG Oranı: %{v['kg_oran']:.0f}
        """)

    with st.expander("🏠 Ev Sahibi Analizi", expanded=True):
        st.markdown(f"""
        - **PPG (Form):** {v['ppg_ev']:.2f} → {takim_form_yorumu(v['ppg_ev'])}
        - **Sıralama:** {v['siralama_ev']}. sıra
        - **xG:** {v['xg_ev']} | **Atılan:** {v['atilan_ev']} | **Yenen:** {v['yenen_ev']}
        - **Reaksiyon Gücü:** %{v['reaksiyon_ev']:.0f} → {'Güçlü direnç' if v['reaksiyon_ev'] > 65 else 'Zayıf direnç' if v['reaksiyon_ev'] < 35 else 'Normal'}
        - **Standart Sapma:** {v['ss_ev']:.2f} → {'⚠️ İstikrarsız' if v['ss_ev'] > 2 else '✅ İstikrarlı' if v['ss_ev'] < 1 else 'Normal'}
        """)

    with st.expander("✈️ Deplasman Analizi", expanded=True):
        st.markdown(f"""
        - **MPG (Form):** {v['mpg_dep']:.2f} → {takim_form_yorumu(v['mpg_dep'])}
        - **Sıralama:** {v['siralama_dep']}. sıra
        - **xG:** {v['xg_dep']} | **Atılan:** {v['atilan_dep']} | **Yenen:** {v['yenen_dep']}
        - **Reaksiyon Gücü:** %{v['reaksiyon_dep']:.0f} → {'Güçlü direnç' if v['reaksiyon_dep'] > 65 else 'Zayıf direnç' if v['reaksiyon_dep'] < 35 else 'Normal'}
        - **Standart Sapma:** {v['ss_dep']:.2f} → {'⚠️ İstikrarsız' if v['ss_dep'] > 2 else '✅ İstikrarlı' if v['ss_dep'] < 1 else 'Normal'}
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
        - 🤝 **KG Tercihi:** **{'KG Var' if kg_ort > 55 else 'KG Yok' if kg_ort < 45 else 'Belirsiz - kaçınılmalı'}** → Var: %{kg_ort:.0f} • Yok: %{100-kg_ort:.0f}
        - 📈 **İkinci Tercih:** {'X2 çifte şans' if p1 > p2 else '1X çifte şans'} (%{max(cifte_1x, cifte_x2):.1f})
        """)

    with st.expander("🎰 Favori Komboları", expanded=True):
        kombolar, favoriler = favori_kombolar(matris, MAX_GOL)
        st.markdown(
            f"**Bu maçın favorileri:** "
            f"`{favoriler[0]}` • `{favoriler[1]}` • `{favoriler[2]}`"
        )
        st.markdown("**Favorilerden 2'li kombolar:**")
        for isim, yuzde in kombolar:
            if yuzde >= 50:   emoji = "🟢"
            elif yuzde >= 35: emoji = "🟡"
            else:             emoji = "🔴"
            st.markdown(f"{emoji} **{isim}** → %{yuzde:.1f}")

        st.markdown("---")
        en_iyi = kombolar[0]
        st.success(f"🔥 **En İyi Kombo:** {en_iyi[0]} → %{en_iyi[1]:.1f}")

    st.divider()

    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.form_version += 1
        st.session_state.sayfa = "giris"
        st.rerun()
