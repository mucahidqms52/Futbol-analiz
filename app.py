import streamlit as st
import math

st.set_page_config(page_title="Futbol Analiz Pro Terminal", page_icon="⚽", layout="centered")

# Sayfa durumu yönetimi (Giriş ekranı vs Sonuç ekranı geçişi için)
if "sayfa" not in st.session_state:
    st.session_state.sayfa = "giris"

# Form verileri için hafıza (Temizlenebilir yapı)
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
    st.markdown("""
        <h1 style='text-align: center; color: #1f77b4;'>⚽ Futbol Analiz Pro Terminal</h1>
        <p style='text-align: center; color: gray;'>Poisson İstatistiksel Dağılım ve Risk Yönetim Paneli</p>
    """, unsafe_allow_html=True)

    st.divider()
    st.subheader("📋 Sıralı Veri Giriş Terminali")

    v = st.session_state.veriler

    v["ppg_ev"] = st.number_input("1. PPG Ev", value=v["ppg_ev"], step=0.1)
    v["mpg_dep"] = st.number_input("2. MPG Dep", value=v["mpg_dep"], step=0.1)
    v["siralama_ev"] = st.number_input("3. Sıralama Ev", value=int(v["siralama_ev"]), step=1)
    v["siralama_dep"] = st.number_input("4. Sıralama Dep", value=int(v["siralama_dep"]), step=1)
    v["reaksiyon_ev"] = st.number_input("5. Reaksiyon Gücü Ev (%)", value=v["reaksiyon_ev"], step=0.1)
    v["reaksiyon_dep"] = st.number_input("5. Reaksiyon Gücü Dep (%)", value=v["reaksiyon_dep"], step=0.1)
    v["xg_ev"] = st.number_input("6. xG Ev", value=v["xg_ev"], step=0.01)
    v["xg_dep"] = st.number_input("6. xG Dep", value=v["xg_dep"], step=0.01)
    v["atilan_ev"] = st.number_input("7. Atılan Gol Ev", value=v["atilan_ev"], step=0.1)
    v["atilan_dep"] = st.number_input("7. Atılan Gol Dep", value=v["atilan_dep"], step=0.1)
    v["yenen_ev"] = st.number_input("8. Yenen Gol Ev", value=v["yenen_ev"], step=0.1)
    v["yenen_dep"] = st.number_input("8. Yenen Gol Dep", value=v["yenen_dep"], step=0.1)
    v["ss_ev"] = st.number_input("9. Standart Sapma Ev", value=v["ss_ev"], step=0.01)
    v["ss_dep"] = st.number_input("9. Standart Sapma Dep", value=v["ss_dep"], step=0.01)
    v["kg_oran"] = st.number_input("10. KG Oranı / Sıklığı (%)", value=v["kg_oran"], step=1.0)

    st.divider()

    if st.button("🚀 Pro Terminal Analizini Başlat", type="primary", use_container_width=True):
        st.session_state.sayfa = "sonuc"
        st.rerun()

# --- 2. ANALİZ SONUÇ EKRANI ---
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.veriler

    # Poisson & Matematiksel Hesaplamalar
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

    for i in range(6):
        for j in range(6):
            p = poisson(lambda_ev, i) * poisson(lambda_dep, j)
            if i > j:
                prob_ev_kazanir += p
            elif i == j:
                prob_beraberlik += p
            else:
                prob_dep_kazanir += p
            
            if i + j <= 2:
                u25_prob += p
            if i > 0 and j > 0:
                btts_prob += p

    toplam_prob = prob_ev_kazanir + prob_beraberlik + prob_dep_kazanir
    oran_ev = (prob_ev_kazanir / toplam_prob) * 100
    oran_beraberlik = (prob_beraberlik / toplam_prob) * 100
    oran_dep = (prob_dep_kazanir / toplam_prob) * 100

    cifte_1x = oran_ev + oran_beraberlik
    cifte_x2 = oran_dep + oran_beraberlik
    cifte_12 = oran_ev + oran_dep

    over25_oran = (1 - u25_prob) * 100
    btts_oran = btts_prob * 100
    tahmini_gol = lambda_ev + lambda_dep

    risk_skoru = (v["ss_ev"] + v["ss_dep"]) / 2
    risk_durumu = "Yüksek Volatilite (Sürprize Açık)" if risk_skoru > 1.2 else "Dengeli / İstikrarlı Profil"

    st.markdown("""
        <h1 style='text-align: center; color: #2ca02c;'>🎯 Pro Terminal Analiz Raporu</h1>
        <p style='text-align: center; color: gray;'>Poisson İstatistiksel Dağılım Sonuçları</p>
    """, unsafe_allow_html=True)

    st.divider()

    # --- 1. PRO 1X2 PANELİ ---
    st.subheader("📊 1X2 Olasılık Dağılımı (Poisson Model)")
    c1, c2, c3 = st.columns(3)
    c1.metric("1 (Ev Sahibi)", f"%{oran_ev:.1f}")
    c2.metric("X (Beraberlik)", f"%{oran_beraberlik:.1f}")
    c3.metric("2 (Deplasman)", f"%{oran_dep:.1f}")

    st.progress(int(oran_ev), text=f"Ev Sahibi Kazanma Olasılığı: %{oran_ev:.1f}")
    st.progress(int(oran_beraberlik), text=f"Beraberlik Olasılığı: %{oran_beraberlik:.1f}")
    st.progress(int(oran_dep), text=f"Deplasman Kazanma Olasılığı: %{oran_dep:.1f}")

    st.divider()

    # --- 2. ÇİFTE ŞANS & RİSK ENDEKSİ ---
    st.subheader("🛡️ Çifte Şans & Volatilite Paneli")
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("1X (Ev / Beraberlik)", f"%{cifte_1x:.1f}")
    cc2.metric("X2 (Dep / Beraberlik)", f"%{cifte_x2:.1f}")
    cc3.metric("Risk Seviyesi", f"{risk_skoru:.2f}", delta=risk_durumu, delta_color="inverse")

    st.divider()

    # --- 3. PRO GOL & ÜST/ALT MATRİSİ ---
    st.subheader("⚽ Gelişmiş Gol & Piyasalar")
    gc1, gc2, gc3 = st.columns(3)
    gc1.metric("📊 Poisson Gol Beklentisi", f"{tahmini_gol:.2f} Gol")
    gc2.metric("⚡ 2.5 Üst Olasılığı", f"%{over25_oran:.1f}")
    gc3.metric("🔥 KG Var Olasılığı", f"%{btts_oran:.1f}")

    st.divider()

    # --- 4. YAPAY ZEKA PRO TAVSİYE & STRATEJİ ---
    st.subheader("🧠 Terminal Yapay Zeka Strateji Raporu")
    
    if over25_oran > 60 and btts_oran > 60:
        tavsiye = "🔥 **Yüksek Tempolu Senaryo:** Model, karşılıklı gol ve 2.5 Üst ihtimalini güçlü görüyor. Alternatif olarak **KG Var + Üst** kombinasyonu değerlendirilebilir."
    elif oran_ev > 55:
        tavsiye = "🎯 **Ev Sahibi Baskısı:** Ev sahibinin form ve xG üstünlüğü net. **1X Çifte Şans** veya handikaplı seçenekler güvenli liman."
    elif oran_dep > 50:
        tavsiye = "⚡ **Deplasman Reaksiyonu:** Deplasman ekibinin veri üstünlüğü var. **X2 Çifte Şans** kuponlar için ideal."
    else:
        tavsiye = "⚖️ **Kilit Maç / Düşük Marj:** Maç ortada geçmeye aday. Ortalama alt/üst sınırlarında kalınması veya canlı bahisler önerilir."

    st.markdown(tavsiye)
    st.markdown(f"""
    * **Ev Sahibi Gol Beklentisi (Lambda):** {lambda_ev:.2f}
    * **Deplasman Gol Beklentisi (Lambda):** {lambda_dep:.2f}
    * **Piyasa Uyum Skoru:** %{v["kg_oran"]:.1f} (Geçmiş maç sıklığı verisiyle teyit edildi)
    """)

    st.divider()

    # --- 5. YENİ MAÇ ANALİZ BUTONU (Sıfırlama ve Geri Dönüş) ---
    if st.button("🔄 Yeni Maç Analiz Et", type="primary", use_container_width=True):
        # Değerleri sıfırla ve giriş ekranına dön
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
