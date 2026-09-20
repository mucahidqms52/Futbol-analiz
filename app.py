import streamlit as st
import math
import copy

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

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


# ==========================================
# SAYFA 1: GİRİŞ (ALAN ALAN: EV-DEP-EV-DEP...)
# ==========================================
if st.session_state.sayfa == "giris":
    st.markdown("""
        <h1 style='text-align: center; color: #1f77b4;'>⚽ Futbol Analiz Pro</h1>
        <p style='text-align: center; color: gray;'>Poisson tabanlı olasılık modeli ile maç analizi</p>
    """, unsafe_allow_html=True)

    st.divider()
    st.subheader("📋 Maç İstatistikleri Girişi")

    v = st.session_state.form_verileri
    fv = st.session_state.form_version

    with st.form(f"analiz_formu_{fv}"):
        # 1. PPG / MPG
        ppg_ev = st.number_input("1. PPG (Ev)", value=float(v["ppg_ev"]), step=0.1, min_value=0.0, key=f"ppg_ev_{fv}")
        mpg_dep = st.number_input("2. MPG (Dep)", value=float(v["mpg_dep"]), step=0.1, min_value=0.0, key=f"mpg_dep_{fv}")

        st.divider()

        # 2. Sıralama
        siralama_ev = st.number_input("3. Sıralama (Ev)", value=int(v["siralama_ev"]), step=1, min_value=1, key=f"siralama_ev_{fv}")
        siralama_dep = st.number_input("4. Sıralama (Dep)", value=int(v["siralama_dep"]), step=1, min_value=1, key=f"siralama_dep_{fv}")

        st.divider()

        # 3. Reaksiyon
        reaksiyon_ev = st.number_input("5. Reaksiyon Gücü % (Ev)", value=float(v["reaksiyon_ev"]), step=1.0, min_value=0.0, max_value=100.0, key=f"reaksiyon_ev_{fv}")
        reaksiyon_dep = st.number_input("6. Reaksiyon Gücü % (Dep)", value=float(v["reaksiyon_dep"]), step=1.0, min_value=0.0, max_value=100.0, key=f"reaksiyon_dep_{fv}")

        st.divider()

        # 4. xG
        xg_ev = st.number_input("7. xG (Ev)", value=float(v["xg_ev"]), step=0.01, min_value=0.0, key=f"xg_ev_{fv}")
        xg_dep = st.number_input("8. xG (Dep)", value=float(v["xg_dep"]), step=0.01, min_value=0.0, key=f"xg_dep_{fv}")

        st.divider()

        # 5. Atılan Gol
        atilan_ev = st.number_input("9. Atılan Gol (Ev)", value=float(v["atilan_ev"]), step=0.1, min_value=0.0, key=f"atilan_ev_{fv}")
        atilan_dep = st.number_input("10. Atılan Gol (Dep)", value=float(v["atilan_dep"]), step=0.1, min_value=0.0, key=f"atilan_dep_{fv}")

        st.divider()

        # 6. Yenen Gol
        yenen_ev = st.number_input("11. Yenen Gol (Ev)", value=float(v["yenen_ev"]), step=0.1, min_value=0.0, key=f"yenen_ev_{fv}")
        yenen_dep = st.number_input("12. Yenen Gol (Dep)", value=float(v["yenen_dep"]), step=0.1, min_value=0.0, key=f"yenen_dep_{fv}")

        st.divider()

        # 7. Standart Sapma
        ss_ev = st.number_input("13. Standart Sapma (Ev)", value=float(v["ss_ev"]), step=0.1, min_value=0.0, key=f"ss_ev_{fv}")
        ss_dep = st.number_input("14. Standart Sapma (Dep)", value=float(v["ss_dep"]), step=0.1, min_value=0.0, key=f"ss_dep_{fv}")

        st.divider()

        # 8. KG Oranı
        kg_oran = st.number_input(
            "15. KG Oranı / Karşılıklı Gol Sıklığı (%)",
            value=float(v["kg_oran"]), step=1.0,
            min_value=0.0, max_value=100.0,
            key=f"kg_oran_{fv}"
        )

        st.divider()
        calistir = st.form_submit_button("🚀 Analizi Çalıştır", use_container_width=True, type="primary")

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
# SAYFA 2: DETAYLI ANALİZ PANELİ
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

    st.markdown("""
        <h1 style='text-align: center; color: #2ca02c;'>🎯 Detaylı Maç Analiz Raporu</h1>
        <p style='text-align: center; color: gray;'>Poisson Dağılımı Tabanlı Olasılık Modeli</p>
    """, unsafe_allow_html=True)
    st.divider()

    # ---- 0. MODEL ÖZETİ ----
    st.subheader("🔬 Model Özeti")
    m1, m2, m3 = st.columns(3)
    m1.metric("Ev Sahibi Beklenen Gol", f"{lam_ev:.2f}")
    m2.metric("Deplasman Beklenen Gol", f"{lam_dep:.2f}")
    m3.metric("Model Güveni", guven_seviyesi(guven))

    st.info(f"📌 **Toplam Beklenen Gol:** {tahmini_gol:.2f} | Güven skoru: {guven:.2f}")

    if guven < 0.4:
        st.warning("⚠️ **Uyarı:** Standart sapmalar yüksek → veriler istikrarsız, tahminler düşük güvenilirlikte.")
    st.divider()

    # ---- 1. 1X2 ----
    st.subheader("📊 1 - X - 2 Maç Sonucu")
    c1, c2, c3 = st.columns(3)
    c1.metric("🏠 1 (Ev)", f"%{p1:.1f}")
    c2.metric("🤝 X (Beraberlik)", f"%{px:.1f}")
    c3.metric("✈️ 2 (Deplasman)", f"%{p2:.1f}")

    st.progress(min(int(p1), 100), text=f"Ev Kazanır: %{p1:.1f}")
    st.progress(min(int(px), 100), text=f"Beraberlik: %{px:.1f}")
    st.progress(min(int(p2), 100), text=f"Deplasman Kazanır: %{p2:.1f}")

    en_olasi = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    st.success(f"🎯 **En Olası Sonuç:** {en_olasi[0]} (%{en_olasi[1]:.1f})")
    st.divider()

    # ---- 2. ÇİFTE ŞANS ----
    st.subheader("🛡️ Çifte Şans")
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("1X", f"%{cifte_1x:.1f}")
    cc2.metric("X2", f"%{cifte_x2:.1f}")
    cc3.metric("12", f"%{cifte_12:.1f}")

    en_guvenli = max([("1X", cifte_1x), ("X2", cifte_x2), ("12", cifte_12)], key=lambda x: x[1])
    st.success(f"✅ **En Güvenli Çifte Şans:** {en_guvenli[0]} (%{en_guvenli[1]:.1f})")
    st.divider()

    # ---- 3. GOL ANALİZİ ----
    st.subheader("⚽ Gol Analizi")

    gol_col1, gol_col2 = st.columns(2)

    with gol_col1:
        st.markdown("**Üst / Alt Bahisleri**")
        ust_05 = olas["ust_05"] / toplam * 100
        ust_15 = olas["ust_15"] / toplam * 100
        ust_25 = olas["ust_25"] / toplam * 100
        ust_35 = olas["ust_35"] / toplam * 100

        st.metric("Üst 0.5", f"%{ust_05:.1f}", f"Alt: %{100-ust_05:.1f}")
        st.metric("Üst 1.5", f"%{ust_15:.1f}", f"Alt: %{100-ust_15:.1f}")
        st.metric("Üst 2.5", f"%{ust_25:.1f}", f"Alt: %{100-ust_25:.1f}")
        st.metric("Üst 3.5", f"%{ust_35:.1f}", f"Alt: %{100-ust_35:.1f}")

    with gol_col2:
        st.markdown("**Karşılıklı Gol (KG)**")
        kg_var_model = olas["kg_var"] / toplam * 100
        kg_yok_model = 100 - kg_var_model

        st.metric("Model KG Var", f"%{kg_var_model:.1f}")
        st.metric("Model KG Yok", f"%{kg_yok_model:.1f}")
        st.metric("Kullanıcı Verisi", f"%{v['kg_oran']:.0f}",
                  delta=f"{v['kg_oran'] - kg_var_model:+.1f}")

        kg_ort = (kg_var_model + v["kg_oran"]) / 2
        if kg_ort >= 60:
            st.success(f"🔥 KG Var güçlü: %{kg_ort:.0f}")
        elif kg_ort <= 40:
            st.info(f"🛡️ KG Yok eğilimi: %{100-kg_ort:.0f}")
        else:
            st.warning(f"⚖️ KG Belirsiz: %{kg_ort:.0f}")

    if tahmini_gol > 3.0:
        st.error(f"🔥 **Yüksek Skor Beklentisi:** Toplam {tahmini_gol:.2f} gol → **2.5 Üst** ve **KG Var** güçlü aday.")
    elif tahmini_gol > 2.4:
        st.warning(f"⚡ **Orta-Yüksek Skor:** {tahmini_gol:.2f} gol → **1.5 Üst** güvenli, 2.5 sınırda.")
    elif tahmini_gol > 1.6:
        st.info(f"⚖️ **Dengeli Maç:** {tahmini_gol:.2f} gol → **2.5 Alt** hafif önde.")
    else:
        st.success(f"🛡️ **Düşük Skor:** {tahmini_gol:.2f} gol → **2.5 Alt** ve **KG Yok** güçlü.")

    st.divider()

    # ---- 4. EN OLASI SKORLAR ----
    st.subheader("🎲 En Olası Skorlar (İlk 6)")
    skorlar = olas["skorlar"]
    en_iyi = sorted(skorlar.items(), key=lambda x: x[1], reverse=True)[:6]

    sk_cols = st.columns(3)
    for idx, (skor, olasilik) in enumerate(en_iyi):
        with sk_cols[idx % 3]:
            st.metric(f"Skor {skor}", f"%{olasilik/toplam*100:.2f}")
    st.divider()

    # ---- 5. TAKIM GÜÇ KARŞILAŞTIRMASI ----
    st.subheader("⚔️ Takım Güç Karşılaştırması")

    guc1, guc2, guc3 = st.columns(3)
    guc1.metric("🏠 Ev Hücumu", f"{v['xg_ev']*0.6 + v['atilan_ev']*0.4:.2f}")
    guc2.metric("🏠 Ev Zaafiyeti", f"{v['yenen_ev']:.2f}")
    guc3.metric("Ev Avantajı", "×1.12")

    guc4, guc5, guc6 = st.columns(3)
    guc4.metric("✈️ Dep Hücumu", f"{v['xg_dep']*0.6 + v['atilan_dep']*0.4:.2f}")
    guc5.metric("✈️ Dep Zaafiyeti", f"{v['yenen_dep']:.2f}")
    guc6.metric("Dep Dezavantajı", "×0.94")
    st.divider()

    # ---- 6. DETAYLI YORUM ----
    st.subheader("📝 Detaylı Analiz Yorumu")

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
        - 🥇 **En Olası Sonuç:** **{en_olasi[0]}** (%{en_olasi[1]:.1f})
        - 🛡️ **En Güvenli Bahis:** Çifte Şans **{en_guvenli[0]}** (%{en_guvenli[1]:.1f})
        - ⚽ **Gol Tercihi:** **{'2.5 Üst' if tahmini_gol > 2.6 else '2.5 Alt'}** (beklenen: {tahmini_gol:.2f})
        - 🤝 **KG Tercihi:** **{'KG Var' if kg_ort > 55 else 'KG Yok' if kg_ort < 45 else 'Belirsiz - kaçınılmalı'}** (%{kg_ort:.0f})
        - 📈 **İkinci Tercih:** {'X2 çifte şans' if p1 > p2 else '1X çifte şans'} (%{max(cifte_1x, cifte_x2):.1f})
        """)

    st.divider()

    # ---- 7. YENİ ANALİZ ----
    if st.button("🔄 Yeni Maç Analizi", type="primary", use_container_width=True):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.form_version += 1
        st.session_state.sayfa = "giris"
        st.rerun()
