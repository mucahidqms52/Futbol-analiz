import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Futbol Analiz Pro Grafik", page_icon="⚽", layout="centered")

# Yazı boyutları ve şık kart tasarımları için CSS
st.markdown("""
    <style>
        p, li, span { font-size: 14px !important; }
        h3 { font-size: 18px !important; }
        h4 { font-size: 15px !important; }
    </style>
""", unsafe_allow_html=True)

if "sayfa" not in st.session_state:
    st.session_state.sayfa = "giris"

if "veriler" not in st.session_state:
    st.session_state.veriler = {
        "ppg_ev": 2.3, "mpg_dep": 2.0,
        "siralama_ev": 14, "siralama_dep": 3,
        "reaksiyon_ev": 66.7, "reaksiyon_dep": 60.0,
        "xg_ev": 1.87, "xg_dep": 1.64,
        "atilan_ev": 2.2, "atilan_dep": 2.0,
        "yenen_ev": 0.7, "yenen_dep": 1.2,
        "ss_ev": 1.55, "ss_dep": 0.94,
        "kg_oran": 55.0
    }

# --- 1. GİRİŞ EKRANI ---
if st.session_state.sayfa == "giris":
    st.markdown("<h3 style='text-align: center; color: #1f77b4; margin-bottom: 0px;'>⚽ Futbol Analiz Pro Grafik</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Veri Giriş Terminali</p>", unsafe_allow_html=True)

    v = st.session_state.veriler

    col1, col2 = st.columns(2)
    with col1:
        v["ppg_ev"] = st.number_input("1. PPG Ev", value=v["ppg_ev"], step=0.1)
        v["siralama_ev"] = st.number_input("3. Sıra Ev", value=int(v["siralama_ev"]), step=1)
        v["reaksiyon_ev"] = st.number_input("5. Reak. Ev", value=v["reaksiyon_ev"], step=0.1)
        v["xg_ev"] = st.number_input("6. xG Ev", value=v["xg_ev"], step=0.01)
        v["atilan_ev"] = st.number_input("7. Atılan Ev", value=v["atilan_ev"], step=0.1)
        v["yenen_ev"] = st.number_input("8. Yenen Ev", value=v["yenen_ev"], step=0.1)
        v["ss_ev"] = st.number_input("9. SS Ev", value=v["ss_ev"], step=0.01)

    with col2:
        v["mpg_dep"] = st.number_input("2. MPG Dep", value=v["mpg_dep"], step=0.1)
        v["siralama_dep"] = st.number_input("4. Sıra Dep", value=int(v["siralama_dep"]), step=1)
        v["reaksiyon_dep"] = st.number_input("5. Reak. Dep", value=v["reaksiyon_dep"], step=0.1)
        v["xg_dep"] = st.number_input("6. xG Dep", value=v["xg_dep"], step=0.01)
        v["atilan_dep"] = st.number_input("7. Atılan Dep", value=v["atilan_dep"], step=0.1)
        v["yenen_dep"] = st.number_input("8. Yenen Dep", value=v["yenen_dep"], step=0.1)
        v["ss_dep"] = st.number_input("9. SS Dep", value=v["ss_dep"], step=0.01)

    v["kg_oran"] = st.number_input("10. KG Oranı (%)", value=v["kg_oran"], step=1.0)

    st.write("")
    if st.button("🚀 Grafiksel Analizi Başlat", type="primary", use_container_width=True):
        st.session_state.sayfa = "sonuc"
        st.rerun()

# --- 2. GRAFİKSEL VE DETAYLI PRO SONUÇ EKRANI ---
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.veriler

    # Matematiksel Hesaplamalar
    lambda_ev = (v["xg_ev"] * 0.45) + (v["atilan_ev"] * 0.35) + (v["yenen_dep"] * 0.2)
    lambda_dep = (v["xg_dep"] * 0.45) + (v["atilan_dep"] * 0.35) + (v["yenen_ev"] * 0.2)
    
    form_faktoru_ev = (v["ppg_ev"] / 3.0) * (max(21 - v["siralama_ev"], 1) / 20) * (1 + (v["reaksiyon_ev"] / 200))
    form_faktoru_dep = (v["mpg_dep"] / 3.0) * (max(21 - v["siralama_dep"], 1) / 20) * (1 + (v["reaksiyon_dep"] / 200))
    
    lambda_ev = lambda_ev * (0.7 + (form_faktoru_ev * 0.3))
    lambda_dep = lambda_dep * (0.7 + (form_faktoru_dep * 0.3))

    def poisson(lmbda, k):
        return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

    prob_ev_kazanir = 0
    prob_beraberlik = 0
    prob_dep_kazanir = 0
    u25_prob = 0
    btts_prob = 0
    skor_matrisi = {}

    for i in range(6):
        for j in range(6):
            p = poisson(lambda_ev, i) * poisson(lambda_dep, j)
            skor_matrisi[(i, j)] = p * 100
            if i > j: prob_ev_kazanir += p
            elif i == j: prob_beraberlik += p
            else: prob_dep_kazanir += p
            if i + j <= 2: u25_prob += p
            if i > 0 and j > 0: btts_prob += p

    toplam_prob = prob_ev_kazanir + prob_beraberlik + prob_dep_kazanir
    oran_ev = (prob_ev_kazanir / toplam_prob) * 100
    oran_beraberlik = (prob_beraberlik / toplam_prob) * 100
    oran_dep = (prob_dep_kazanir / toplam_prob) * 100

    cifte_1x = oran_ev + oran_beraberlik
    cifte_x2 = oran_dep + oran_beraberlik

    over25_oran = (1 - u25_prob) * 100
    btts_oran = btts_prob * 100
    tahmini_gol = lambda_ev + lambda_dep
    risk_skoru = (v["ss_ev"] + v["ss_dep"]) / 2

    en_yuksek_skor = max(skor_matrisi, key=skor_matrisi.get)

    # Başlık
    st.markdown("<h4 style='text-align: center; color: #1f77b4; margin-bottom: 0px;'>📊 Grafiksel Analiz Paneli</h4>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 6px 0px;'>", unsafe_allow_html=True)

    # 1. 1X2 Grafik Görselleştirmesi (Streamlit Bar Chart)
    st.markdown("<b>1. Maç Sonucu Olasılık Grafiği</b>", unsafe_allow_html=True)
    df_1x2 = pd.DataFrame({
        "Sonuç": ["Ev Sahibi (1)", "Beraberlik (X)", "Deplasman (2)"],
        "Olasılık (%)": [round(oran_ev, 1), round(oran_beraberlik, 1), round(oran_dep, 1)]
    }).set_index("Sonuç")
    st.bar_chart(df_1x2, color="#1f77b4")

    # 2. Çifte Şans ve Gol Piyasaları (Metrik Kartları)
    st.markdown("<b>2. Çifte Şans ve Piyasalar</b>", unsafe_allow_html=True)
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("1X Şans", f"%{cifte_1x:.1f}")
    cc2.metric("X2 Şans", f"%{cifte_x2:.1f}")
    cc3.metric("Risk Seviyesi", f"{risk_skoru:.2f}")

    gc1, gc2, gc3 = st.columns(3)
    gc1.metric("Gol Bekl.", f"{tahmini_gol:.2f}")
    gc2.metric("2.5 Üst", f"%{over25_oran:.1f}")
    gc3.metric("KG Var", f"%{btts_oran:.1f}")

    st.markdown("<hr style='margin: 6px 0px;'>", unsafe_allow_html=True)

    # 3. Gol Beklentisi Karşılaştırma Grafiği
    st.markdown("<b>3. Takım xG / Gol Beklentisi Kıyaslaması</b>", unsafe_allow_html=True)
    df_xg = pd.DataFrame({
        "Takım": ["Ev Sahibi", "Deplasman"],
        "Gol Beklentisi (Lambda)": [round(lambda_ev, 2), round(lambda_dep, 2)]
    }).set_index("Takım")
    st.bar_chart(df_xg, color="#2ca02c")

    # Model Sonuç Kartı
    st.info(f"🎯 **En Muhtemel Skor Tahmini:** `{en_yuksek_skor[0]} - {en_yuksek_skor[1]}` (Olasılık: %{skor_matrisi[en_yuksek_skor]:.1f})")

    if over25_oran > 60 and btts_oran > 60:
        st.error("🔥 **Strateji:** Tempolu oyun bekleniyor. 2.5 Üst ve KG Var öncelikli.")
    elif oran_ev > 55:
        st.success("🎯 **Strateji:** Ev sahibinin üstünlüğü net. 1X Şans değerlendirilebilir.")
    else:
        st.warning("⚖️ **Strateji:** Dengeli eşleşme. Canlı oran takibi önerilir.")

    st.write("")

    # Sıfırlama Butonu
    if st.button("🔄 Yeni Maç Analiz Et", type="primary", use_container_width=True):
        st.session_state.veriler = {
            "ppg_ev": 0.0, "mpg_dep": 0.0,
            "siralama_ev": 1, "siralama_dep": 1,
            "reaksiyon_ev": 0.0, "reaksiyon_dep": 0.0,
            "xg_ev": 0.0, "xg_dep": 0.0,
            "atilan_ev": 0.0, "atilan_dep": 0.0,
            "yenen_ev": 0.0, "yenen_dep": 0.0,
            "ss_ev": 0.0, "ss_dep": 0.0,
            "kg_oran": 50.0
        }
        st.session_state.sayfa = "giris"
        st.rerun()
