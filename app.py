import streamlit as st
import math
import copy

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

    div[data-testid="stMetric"] {
        padding: 0.2rem !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1rem !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.7rem !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 0.65rem !important;
    }

    .stButton button {
        padding: 0.3rem 0.5rem !important;
        font-size: 0.85rem !important;
        height: 2rem !important;
    }

    div[data-testid="stAlert"] {
        padding: 0.3rem 0.5rem !important;
        font-size: 0.8rem !important;
    }

    details summary {
        font-size: 0.8rem !important;
        padding: 0.2rem 0.4rem !important;
    }

    div[data-testid="column"] {
        padding: 0 0.1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SABİTLER
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

            if i > j:   p1 += p
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
        "kg_var": kg_var,
        "skorlar": skorlar,
        "toplam": toplam,
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
    dolu_sayisi = sum(1 for x in onemli_alanlar if x > 0)
    return dolu_sayisi >= 2


# ==========================================
# GENİŞ KAPSAMLI ANALİZ FONKSİYONU
# ==========================================
def detayli_analiz_yorumu(v: dict):
    yorumlar = []

    # 1. FORM
    ppg, mpg = v["ppg_ev"], v["mpg_dep"]
    fark = ppg - mpg
    if ppg >= 2.0 and mpg <= 1.0:
        txt = f"Ev sahibi evinde mükemmel bir form yakalamış (**PPG {ppg:.2f}**), deplasman ise deplasmanda zorlanıyor (**MPG {mpg:.2f}**). Ev sahibi form olarak açık ara üstün."
    elif fark >= 0.7:
        txt = f"Ev sahibi form olarak önde (**PPG {ppg:.2f}** vs **MPG {mpg:.2f}**). Sahasında kaybetmeye alışkın değil."
    elif fark <= -0.7:
        txt = f"Deplasman form olarak önde (**MPG {mpg:.2f}** vs **PPG {ppg:.2f}**). Deplasmanda beklenmedik bir performans sergiliyor."
    else:
        txt = f"Form dengeli (**PPG {ppg:.2f}** vs **MPG {mpg:.2f}**). İki takım da benzer ritimde."
    yorumlar.append(("📈 FORM", txt))

    # 2. SIRALAMA
    s_ev, s_dep = v["siralama_ev"], v["siralama_dep"]
    fark_sira = s_dep - s_ev
    if fark_sira >= 8:
        txt = f"Ev sahibi **{s_ev}.** sırada, deplasman **{s_dep}.** sırada. Aradaki **{fark_sira} basamak** ciddi bir güç farkına işaret ediyor. Ev sahibi kağıt üzerinde net favori."
    elif fark_sira >= 3:
        txt = f"Ev sahibi **{s_ev}.**, deplasman **{s_dep}.** sırada. Ev sahibi lig tablosunda üstün konumda."
    elif fark_sira <= -8:
        txt = f"Deplasman **{s_dep}.** sırada, ev sahibi **{s_ev}.** sırada. Deplasman **{abs(fark_sira)} basamak** yukarıda, sürpriz yapabilir."
    elif fark_sira <= -3:
        txt = f"Deplasman **{s_dep}.** sırada, ev sahibi **{s_ev}.** sırada. Deplasman kağıt üzerinde biraz üstün."
    else:
        txt = f"Sıralamalar yakın (Ev **{s_ev}.** / Dep **{s_dep}.**). Dengeli bir eşleşme."
    yorumlar.append(("🏆 SIRALAMA", txt))

    # 3. HÜCUM (xG)
    xg_ev, xg_dep = v["xg_ev"], v["xg_dep"]
    fark_xg = xg_ev - xg_dep
    if fark_xg >= 0.6:
        txt = f"Ev sahibi hücumda üretken (**xG {xg_ev:.2f}** vs **{xg_dep:.2f}**). Rakip kaleye sürekli tehlike taşıyor. Deplasman savunması zor bir maç geçirebilir."
    elif fark_xg <= -0.6:
        txt = f"Deplasman hücumda daha etkili (**xG {xg_dep:.2f}** vs **{xg_ev:.2f}**). Ev sahibi savunmada dikkatli olmalı."
    else:
        txt = f"xG değerleri yakın (Ev **{xg_ev:.2f}** / Dep **{xg_dep:.2f}**). Hücum güçleri dengeli."
    yorumlar.append(("🎯 HÜCUM (xG)", txt))

    # 4. ATILAN GOL
    at_ev, at_dep = v["atilan_ev"], v["atilan_dep"]
    fark_at = at_ev - at_dep
    if fark_at >= 0.6:
        txt = f"Ev sahibi maç başına **{at_ev:.1f}** gol atıyor, deplasman **{at_dep:.1f}**. Gerçekleşen performansta ev sahibi üstün."
    elif fark_at <= -0.6:
        txt = f"Deplasman maç başına **{at_dep:.1f}** gol atıyor, ev sahibi **{at_ev:.1f}**. Deplasman hücumda daha verimli."
    else:
        txt = f"Atılan gol ortalamaları benzer (Ev **{at_ev:.1f}** / Dep **{at_dep:.1f}**)."
    yorumlar.append(("⚽ ATILAN GOL", txt))

    # 5. SAVUNMA (Yenen Gol)
    y_ev, y_dep = v["yenen_ev"], v["yenen_dep"]
    fark_y = y_dep - y_ev
    if fark_y >= 0.7:
        txt = f"Ev sahibi savunması sağlam (**{y_ev:.1f}** gol/maç), deplasman savunması zayıf (**{y_dep:.1f}** gol/maç). Deplasman bu maçta gol yemesi sürpriz olmaz."
    elif fark_y <= -0.7:
        txt = f"Deplasman savunması sağlam (**{y_dep:.1f}** gol/maç), ev sahibi savunması zayıf (**{y_ev:.1f}**). Deplasman gol bulabilir."
    else:
        txt = f"İki takımın da savunması benzer seviyede (Ev **{y_ev:.1f}** / Dep **{y_dep:.1f}**)."
    yorumlar.append(("🛡️ SAVUNMA", txt))

    # 6. REAKSİYON GÜCÜ
    r_ev, r_dep = v["reaksiyon_ev"], v["reaksiyon_dep"]
    fark_r = r_ev - r_dep
    if fark_r >= 15:
        txt = f"Ev sahibi maç içi reaksiyon gücü yüksek (**%{r_ev:.0f}** vs **%{r_dep:.0f}**). Geriye düştüğünde toparlanma kabiliyeti fazla. Deplasman kriz anlarında dağılabilir."
    elif fark_r <= -15:
        txt = f"Deplasman reaksiyon gücü yüksek (**%{r_dep:.0f}** vs **%{r_ev:.0f}**). Skor dezavantajında olsa bile pes etmiyor."
    else:
        txt = f"Reaksiyon güçleri benzer (Ev **%{r_ev:.0f}** / Dep **%{r_dep:.0f}**). Her iki takım da baskı altında benzer davranış sergiliyor."
    yorumlar.append(("💪 REAKSİYON", txt))

    # 7. İSTİKRAR
    ss_ev, ss_dep = v["ss_ev"], v["ss_dep"]
    def istikrar(ss):
        if ss <= 0.8: return "çok istikrarlı"
        if ss <= 1.3: return "istikrarlı"
        if ss <= 2.0: return "dalgalı"
        return "çok istikrarsız"
    if abs(ss_ev - ss_dep) >= 0.5:
        if ss_ev < ss_dep:
            txt = f"Ev sahibi performansı **{istikrar(ss_ev)}** (SS {ss_ev:.2f}), deplasman ise **{istikrar(ss_dep)}** (SS {ss_dep:.2f}). Tahmin edilebilirlik açısından ev sahibi daha güvenilir."
        else:
            txt = f"Deplasman performansı **{istikrar(ss_dep)}** (SS {ss_dep:.2f}), ev sahibi **{istikrar(ss_ev)}** (SS {ss_ev:.2f}). Deplasman sonuçları daha öngörülebilir."
    else:
        txt = f"İki takımın da istikrar seviyesi benzer (Ev **{ss_ev:.2f}** / Dep **{ss_dep:.2f}**)."
    yorumlar.append(("📊 İSTİKRAR", txt))

    return yorumlar


# ==========================================
# FAVORİ KOMBO ÜRETİCİ (SADECE 2'Lİ)
# ==========================================
def favori_kombolar(matris, max_gol: int = MAX_GOL):
    """
    Sadece bu maçın favorilerinden 2'li kombolar üretir.
    1X2, Alt/Üst 2.5, KG Var/Yok kategorilerinin her birinden favoriyi bulur,
    sonra bu 3 favori arasından 2'li kombinasyonlar üretir.
    """
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

    def filtre_sonuc(kod):
        if kod == "1": return lambda i, j: i > j
        if kod == "X": return lambda i, j: i == j
        return lambda i, j: i < j

    def filtre_gol(kod):
        if kod == "Alt": return lambda i, j: i + j < 2.5
        return lambda i, j: i + j > 2.5

    def filtre_kg(kod):
        if kod == "Var": return lambda i, j: i > 0 and j > 0
        return lambda i, j: i == 0 or j == 0

    kombinasyonlar = [
        (favori_sonuc, favori_gol,   filtre_sonuc, filtre_gol),
        (favori_sonuc, favori_kg,    filtre_sonuc, filtre_kg),
        (favori_gol,   favori_kg,    filtre_gol,   filtre_kg),
    ]

    kombolar = []
    for (f1, f2, fn1, fn2) in kombinasyonlar:
        isim = f"{f1[0]} {f2[0]}"
        toplam = 0.0
        for i in range(max_gol):
            for j in range(max_gol):
                if fn1(i, j) and fn2(i, j):
                    toplam += matris[i][j]
        kombolar.append((isim, toplam * 100))

    kombolar.sort(key=lambda x: x[1], reverse=True)
    return kombolar, (favori_sonuc[0], favori_gol[0], favori_kg[0])


# ==========================================
# SAYFA 1: İSTATİSTİK GİRİŞİ
# ==========================================
if st.session_state.sayfa == "giris":
    st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)

    v = st.session_state.form_verileri
    fv = st.session_state.form_version

    with st.form(f"analiz_formu_{fv}"):
        hc1, hc2 = st.columns(2)
        hc1.markdown("**🏠 EV**")
        hc2.markdown("**✈️ DEP**")

        c1, c2 = st.columns(2)
        ppg_ev = c1.number_input("PPG", value=float(v["ppg_ev"]), step=0.1, min_value=0.0, key=f"ppg_ev_{fv}")
        mpg_dep = c2.number_input("MPG", value=float(v["mpg_dep"]), step=0.1, min_value=0.0, key=f"mpg_dep_{fv}")

        c1, c2 = st.columns(2)
        siralama_ev = c1.number_input("Sıra", value=int(v["siralama_ev"]), step=1, min_value=1, key=f"siralama_ev_{fv}")
        siralama_dep = c2.number_input("Sıra", value=int(v["siralama_dep"]), step=1, min_value=1, key=f"siralama_dep_{fv}")

        c1, c2 = st.columns(2)
        reaksiyon_ev = c1.number_input("Reak. %", value=float(v["reaksiyon_ev"]), step=1.0, min_value=0.0, max_value=100.0, key=f"reaksiyon_ev_{fv}")
        reaksiyon_dep = c2.number_input("Reak. %", value=float(v["reaksiyon_dep"]), step=1.0, min_value=0.0, max_value=100.0, key=f"reaksiyon_dep_{fv}")

        c1, c2 = st.columns(2)
        xg_ev = c1.number_input("xG", value=float(v["xg_ev"]), step=0.01, min_value=0.0, key=f"xg_ev_{fv}")
        xg_dep = c2.number_input("xG", value=float(v["xg_dep"]), step=0.01, min_value=0.0, key=f"xg_dep_{fv}")

        c1, c2 = st.columns(2)
        atilan_ev = c1.number_input("Atılan", value=float(v["atilan_ev"]), step=0.1, min_value=0.0, key=f"atilan_ev_{fv}")
        atilan_dep = c2.number_input("Atılan", value=float(v["atilan_dep"]), step=0.1, min_value=0.0, key=f"atilan_dep_{fv}")

        c1, c2 = st.columns(2)
        yenen_ev = c1.number_input("Yenen", value=float(v["yenen_ev"]), step=0.1, min_value=0.0, key=f"yenen_ev_{fv}")
        yenen_dep = c2.number_input("Yenen", value=float(v["yenen_dep"]), step=0.1, min_value=0.0, key=f"yenen_dep_{fv}")

        c1, c2 = st.columns(2)
        ss_ev = c1.number_input("Std.Sap.", value=float(v["ss_ev"]), step=0.1, min_value=0.0, key=f"ss_ev_{fv}")
        ss_dep = c2.number_input("Std.Sap.", value=float(v["ss_dep"]), step=0.1, min_value=0.0, key=f"ss_dep_{fv}")

        kg_oran = st.number_input("KG Oranı (%)", value=float(v["kg_oran"]), step=1.0, min_value=0.0, max_value=100.0, key=f"kg_oran_{fv}")

        calistir = st.form_submit_button("🚀 ANALİZ ET", use_container_width=True, type="primary")

        if calistir:
            st.session_state.form_verileri = {
                "ppg_ev": ppg_ev, "mpg_dep": mpg_dep,
                "siralama_ev": siralama_ev, "siralama_dep": siralama_dep,
                "reaksiyon_ev": reaksiyon_ev, "reaksiyon_dep": reaksiyon_dep,
                "xg_ev": xg_ev, "xg_dep": xg_dep,
                "atilan_ev": atilan_ev, "atilan_dep": atilan_dep,
                "yenen_ev": yenen_ev, "yenen_dep": yenen_dep,
                "ss_ev": ss_ev, "ss_dep": ss_dep,
                "kg_oran": kg_oran,
            }
            st.session_state.form_version += 1
            st.session_state.sayfa = "sonuc"
            st.rerun()


# ==========================================
# SAYFA 2: DETAYLI ANALİZ
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri

    if not veri_yeterli_mi(v):
        st.markdown("<h1>⚠️ Yetersiz Veri</h1>", unsafe_allow_html=True)
        st.error("""
        **Analiz için yeterli istatistik girilmedi.**
        
        Lütfen forma dönüp en az **2 alan** doldur:
        - xG (Ev / Dep)
        - Atılan Gol (Ev / Dep)
        - Yenen Gol (Ev / Dep)
        """)
        if st.button("⬅️ Forma Dön", use_container_width=True, type="primary"):
            st.session_state.sayfa = "giris"
            st.rerun()
        st.stop()

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

    # ---- 🏠 EV SAHİBİ ANALİZİ ----
    with st.expander("🏠 Ev Sahibi Analizi", expanded=True):
        st.markdown(f"""
        - **PPG (Form):** {v['ppg_ev']:.2f} → {takim_form_yorumu(v['ppg_ev'])}
        - **Sıralama:** {v['siralama_ev']}. sıra
        - **xG:** {v['xg_ev']} | **Atılan:** {v['atilan_ev']} | **Yenen:** {v['yenen_ev']}
        - **Reaksiyon Gücü:** %{v['reaksiyon_ev']:.0f} → {'Güçlü direnç' if v['reaksiyon_ev'] > 65 else 'Zayıf direnç' if v['reaksiyon_ev'] < 35 else 'Normal'}
        - **Standart Sapma:** {v['ss_ev']:.2f} → {'⚠️ İstikrarsız' if v['ss_ev'] > 2 else '✅ İstikrarlı' if v['ss_ev'] < 1 else 'Normal'}
        """)

    # ---- ✈️ DEPLASMAN ANALİZİ ----
    with st.expander("✈️ Deplasman Analizi", expanded=True):
        st.markdown(f"""
        - **MPG (Form):** {v['mpg_dep']:.2f} → {takim_form_yorumu(v['mpg_dep'])}
        - **Sıralama:** {v['siralama_dep']}. sıra
        - **xG:** {v['xg_dep']} | **Atılan:** {v['atilan_dep']} | **Yenen:** {v['yenen_dep']}
        - **Reaksiyon Gücü:** %{v['reaksiyon_dep']:.0f} → {'Güçlü direnç' if v['reaksiyon_dep'] > 65 else 'Zayıf direnç' if v['reaksiyon_dep'] < 35 else 'Normal'}
        - **Standart Sapma:** {v['ss_dep']:.2f} → {'⚠️ İstikrarsız' if v['ss_dep'] > 2 else '✅ İstikrarlı' if v['ss_dep'] < 1 else 'Normal'}
        """)

    # ---- 🔍 GENİŞ KAPSAMLI ANALİZ ----
    with st.expander("🔍 Geniş Kapsamlı Analiz", expanded=True):
        yorumlar = detayli_analiz_yorumu(v)
        for baslik, metin in yorumlar:
            st.markdown(f"**{baslik}**")
            st.markdown(metin)
            st.markdown("")

    # ---- 🎯 STRATEJİ ÖNERİLERİ ----
    with st.expander("🎯 Strateji Önerileri", expanded=True):
        st.markdown(f"**Ana Senaryo:** {senaryo}")
        st.markdown(f"""
        - 🥇 **En Olası Sonuç:** **{en_olasi[0]}** → 1: %{p1:.1f} • X: %{px:.1f} • 2: %{p2:.1f}
        - 🛡️ **En Güvenli Bahis:** Çifte Şans **{en_guvenli[0]}** → 1X: %{cifte_1x:.1f} • X2: %{cifte_x2:.1f} • 12: %{cifte_12:.1f}
        - ⚽ **Gol Tercihi:** **{'2.5 Üst' if tahmini_gol > 2.6 else '2.5 Alt'}** (beklenen: {tahmini_gol:.2f}) → Üst: %{ust_25:.0f} • Alt: %{100-ust_25:.0f}
        - 🤝 **KG Tercihi:** **{'KG Var' if kg_ort > 55 else 'KG Yok' if kg_ort < 45 else 'Belirsiz - kaçınılmalı'}** → Var: %{kg_ort:.0f} • Yok: %{100-kg_ort:.0f}
        - 📈 **İkinci Tercih:** {'X2 çifte şans' if p1 > p2 else '1X çifte şans'} (%{max(cifte_1x, cifte_x2):.1f})
        """)

    # ---- 🎰 FAVORİ KOMBOLAR (SADECE 2'Lİ) ----
    with st.expander("🎰 Favori Komboları (Bu Maça Özel)", expanded=True):
        kombolar, favoriler = favori_kombolar(matris, MAX_GOL)

        st.markdown(
            f"**Bu maçın favorileri:** "
            f"`{favoriler[0]}` • `{favoriler[1]}` • `{favoriler[2]}`"
        )
        st.markdown("**Favorilerden 2'li kombolar:**")

        for isim, yuzde in kombolar:
            if yuzde >= 50:
                emoji = "🟢"
            elif yuzde >= 35:
                emoji = "🟡"
            else:
                emoji = "🔴"
            st.markdown(f"{emoji} **{isim}** → %{yuzde:.1f}")

        st.markdown("---")
        en_iyi = kombolar[0]
        st.success(f"🔥 **En İyi Kombo:** {en_iyi[0]} → %{en_iyi[1]:.1f}")

    st.divider()

    if st.button("🔄 Yeni Analiz", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.form_version += 1
        st.session_state.sayfa = "giris"
        st.rerun()
