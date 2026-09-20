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


def guven_seviyesi(g: float) -> str:
    if g >= 0.7: return "🟢 Yüksek"
    if g >= 0.4: return "🟡 Orta"
    return "🔴 Düşük"


def takim_form_yorumu(deger: float) -> str:
    if deger > 2.0: return "🟢 Güçlü form"
    if deger < 1.0: return "🔴 Zayıf form"
    return "🟡 Ortalama form"


def veri_yeterli_mi(v: dict) -> bool:
    """En az 2 hücum verisi girilmiş mi kontrol eder."""
    onemli_alanlar = [
        v["xg_ev"], v["xg_dep"],
        v["atilan_ev"], v["atilan_dep"],
        v["yenen_ev"], v["yenen_dep"],
    ]
    dolu_sayisi = sum(1 for x in onemli_alanlar if x > 0)
    return dolu_sayisi >= 2


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

    # ---- VERİ YETERLİLİK KONTROLÜ ----
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

    # ---- Hesaplamalar ----
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

    ust_05 = olas["ust_05"] / toplam * 100
    ust_15 = olas["ust_15"] / toplam * 100
    ust_25 = olas["ust_25"] / toplam * 100
    ust_35 = olas["ust_35"] / toplam * 100

    kg_var_model = olas["kg_var"] / toplam * 100
    kg_yok_model = 100 - kg_var_model
    kg_ort = (kg_var_model + v["kg_oran"]) / 2

    en_olasi = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    en_guvenli = max([("1X", cifte_1x), ("X2", cifte_x2), ("12", cifte_12)], key=lambda x: x[1])

    st.markdown("<h1>🎯 Detaylı Analiz Raporu</h1>", unsafe_allow_html=True)

    # ---- 📋 TAKIM İSTATİSTİKLERİ ----
    st.markdown("### 📋 Takım İstatistikleri")

    stat_c1, stat_c2 = st.columns(2)
    with stat_c1:
        st.markdown("**🏠 Ev Sahibi**")
        st.markdown(f"""
        - PPG: **{v['ppg_ev']:.2f}** ({takim_form_yorumu(v['ppg_ev'])})
        - Sıra: **{v['siralama_ev']}**
        - Reaksiyon: **%{v['reaksiyon_ev']:.0f}**
        - xG: **{v['xg_ev']:.2f}**
        - Atılan: **{v['atilan_ev']:.1f}**
        - Yenen: **{v['yenen_ev']:.1f}**
        - Std.Sapma: **{v['ss_ev']:.2f}**
        """)
    with stat_c2:
        st.markdown("**✈️ Deplasman**")
        st.markdown(f"""
        - MPG: **{v['mpg_dep']:.2f}** ({takim_form_yorumu(v['mpg_dep'])})
        - Sıra: **{v['siralama_dep']}**
        - Reaksiyon: **%{v['reaksiyon_dep']:.0f}**
        - xG: **{v['xg_dep']:.2f}**
        - Atılan: **{v['atilan_dep']:.1f}**
        - Yenen: **{v['yenen_dep']:.1f}**
        - Std.Sapma: **{v['ss_dep']:.2f}**
        """)

    st.markdown(f"**KG Oranı:** %{v['kg_oran']:.0f}")

    st.divider()

    # ---- 🔬 MODEL ÖZETİ ----
    st.markdown("### 🔬 Model Özeti")
    m1, m2, m3 = st.columns(3)
    m1.metric("Ev Beklenen Gol", f"{lam_ev:.2f}")
    m2.metric("Dep Beklenen Gol", f"{lam_dep:.2f}")
    m3.metric("Model Güveni", guven_seviyesi(guven))

    st.info(f"📌 **Toplam Beklenen Gol:** {tahmini_gol:.2f} | Güven: {guven:.2f}")

    if guven < 0.4:
        st.warning("⚠️ Standart sapmalar yüksek → tahminler düşük güvenilirlikte.")

    st.divider()

    # ---- 📊 1X2 ----
    st.markdown("### 📊 1 - X - 2 Maç Sonucu")
    c1, c2, c3 = st.columns(3)
    c1.metric("🏠 1 (Ev)", f"%{p1:.1f}")
    c2.metric("🤝 X (Beraberlik)", f"%{px:.1f}")
    c3.metric("✈️ 2 (Deplasman)", f"%{p2:.1f}")

    st.success(f"🎯 **En Olası Sonuç:** {en_olasi[0]} (%{en_olasi[1]:.1f}) → 1: %{p1:.1f} • X: %{px:.1f} • 2: %{p2:.1f}")

    st.divider()

    # ---- 🛡️ ÇİFTE ŞANS ----
    st.markdown("### 🛡️ Çifte Şans")
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("1X", f"%{cifte_1x:.1f}")
    cc2.metric("X2", f"%{cifte_x2:.1f}")
    cc3.metric("12", f"%{cifte_12:.1f}")

    st.success(f"✅ **En Güvenli:** Çifte Şans **{en_guvenli[0]}** (%{en_guvenli[1]:.1f}) → 1X: %{cifte_1x:.1f} • X2: %{cifte_x2:.1f} • 12: %{cifte_12:.1f}")

    st.divider()

    # ---- ⚽ GOL ANALİZİ ----
    st.markdown("### ⚽ Gol Analizi")

    st.markdown("**Üst / Alt Bahisleri**")
    gc1, gc2, gc3, gc4 = st.columns(4)
    gc1.metric("Üst 0.5", f"%{ust_05:.0f}", f"Alt: %{100-ust_05:.0f}")
    gc2.metric("Üst 1.5", f"%{ust_15:.0f}", f"Alt: %{100-ust_15:.0f}")
    gc3.metric("Üst 2.5", f"%{ust_25:.0f}", f"Alt: %{100-ust_25:.0f}")
    gc4.metric("Üst 3.5", f"%{ust_35:.0f}", f"Alt: %{100-ust_35:.0f}")

    st.markdown("**Karşılıklı Gol (KG)**")
    kc1, kc2, kc3 = st.columns(3)
    kc1.metric("Model KG Var", f"%{kg_var_model:.1f}")
    kc2.metric("Model KG Yok", f"%{kg_yok_model:.1f}")
    kc3.metric("Kullanıcı Verisi", f"%{v['kg_oran']:.0f}", delta=f"{v['kg_oran']-kg_var_model:+.1f}")

    if kg_ort >= 60:
        st.success(f"🔥 KG Var güçlü: %{kg_ort:.0f}")
    elif kg_ort <= 40:
        st.info(f"🛡️ KG Yok eğilimi: %{100-kg_ort:.0f}")
    else:
        st.warning(f"⚖️ KG Belirsiz: %{kg_ort:.0f}")

    if tahmini_gol > 3.0:
        st.error(f"🔥 **Yüksek Skor Beklentisi:** {tahmini_gol:.2f} gol → **2.5 Üst** ve **KG Var** güçlü aday.")
    elif tahmini_gol > 2.4:
        st.warning(f"⚡ **Orta-Yüksek Skor:** {tahmini_gol:.2f} gol → **1.5 Üst** güvenli, 2.5 sınırda.")
    elif tahmini_gol > 1.6:
        st.info(f"⚖️ **Dengeli Maç:** {tahmini_gol:.2f} gol → **2.5 Alt** hafif önde.")
    else:
        st.success(f"🛡️ **Düşük Skor:** {tahmini_gol:.2f} gol → **2.5 Alt** ve **KG Yok** güçlü.")

    st.divider()

    # ---- 🎲 EN OLASI SKORLAR ----
    st.markdown("### 🎲 En Olası Skorlar (İlk 6)")
    en_iyi = sorted(olas["skorlar"].items(), key=lambda x: x[1], reverse=True)[:6]
    sk_cols = st.columns(6)
    for idx, (skor, olasilik) in enumerate(en_iyi):
        sk_cols[idx].metric(skor, f"%{olasilik/toplam*100:.1f}")

    st.divider()

    # ---- ⚔️ TAKIM GÜÇ KARŞILAŞTIRMASI ----
    st.markdown("### ⚔️ Takım Güç Karşılaştırması")

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("**🏠 Ev Sahibi**")
        st.metric("Hücum", f"{v['xg_ev']*0.6 + v['atilan_ev']*0.4:.2f}")
        st.metric("Zaafiyet", f"{v['yenen_ev']:.2f}")
        st.metric("Avantaj", "×1.12")
    with g2:
        st.markdown("**✈️ Deplasman**")
        st.metric("Hücum", f"{v['xg_dep']*0.6 + v['atilan_dep']*0.4:.2f}")
        st.metric("Zaafiyet", f"{v['yenen_dep']:.2f}")
        st.metric("Dezavantaj", "×0.94")

    st.divider()

    # ---- 📝 DETAYLI ANALİZ YORUMU ----
    st.markdown("### 📝 Detaylı Analiz Yorumu")

    fark = p1 - p2
    if fark > 25:       senaryo = "Ev sahibi açık ara favori görünüyor."
    elif fark > 10:     senaryo = "Ev sahibi hafif favori konumunda."
    elif fark < -25:    senaryo = "Deplasman ekibi net favori."
    elif fark < -10:    senaryo = "Deplasman hafif favori."
    else:               senaryo = "Maç oldukça dengeli, beraberlik riski yüksek."

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

    with st.expander("🎯 Strateji Önerileri", expanded=True):
        st.markdown(f"**Ana Senaryo:** {senaryo}")
        st.markdown(f"""
        - 🥇 **En Olası Sonuç:** **{en_olasi[0]}** (%{en_olasi[1]:.1f}) → 1: %{p1:.1f} • X: %{px:.1f} • 2: %{p2:.1f}
        - 🛡️ **En Güvenli Bahis:** Çifte Şans **{en_guvenli[0]}** (%{en_guvenli[1]:.1f}) → 1X: %{cifte_1x:.1f} • X2: %{cifte_x2:.1f} • 12: %{cifte_12:.1f}
        - ⚽ **Gol Tercihi:** **{'2.5 Üst' if tahmini_gol > 2.6 else '2.5 Alt'}** (beklenen: {tahmini_gol:.2f}) → Üst: %{ust_25:.0f} • Alt: %{100-ust_25:.0f}
        - 🤝 **KG Tercihi:** **{'KG Var' if kg_ort > 55 else 'KG Yok' if kg_ort < 45 else 'Belirsiz - kaçınılmalı'}** (%{kg_ort:.0f}) → Var: %{kg_ort:.0f} • Yok: %{100-kg_ort:.0f}
        - 📈 **İkinci Tercih:** {'X2 çifte şans' if p1 > p2 else '1X çifte şans'} (%{max(cifte_1x, cifte_x2):.1f})
        """)

    st.divider()

    # ---- 🔄 YENİ ANALİZ ----
    if st.button("🔄 Yeni Analiz", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.form_version += 1
        st.session_state.sayfa = "giris"
        st.rerun()
