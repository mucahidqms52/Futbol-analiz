import streamlit as st

st.set_page_config(page_title="Futbol Analiz Pro Manuel", page_icon="⚽", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #1f77b4;'>⚽ Futbol Analiz Pro - Manuel Giriş</h1>
    <p style='text-align: center; color: gray;'>İstatistikleri sırasıyla girin, yapay zeka hatasız analiz etsin!</p>
""", unsafe_allow_html=True)

st.divider()

st.subheader("📋 Maç İstatistikleri Giriş Paneli")

# Senin istediğin sırada Ev ve Deplasman verileri için ikili sütun yapısı
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏠 Ev Sahibi")
    ppg_ev = st.number_input("1. PPG Ev", value=2.3, step=0.1)
    siralama_ev = st.number_input("3. Sıralama Ev", value=14, step=1)
    reaksiyon_ev = st.number_input("5. Reaksiyon Gücü Ev (%)", value=66.7, step=0.1)
    xg_ev = st.number_input("6. xG Ev", value=1.87, step=0.01)
    atilan_ev = st.number_input("7. Atılan Gol Ev", value=2.2, step=0.1)
    yenen_ev = st.number_input("8. Yenen Gol Ev", value=0.7, step=0.1)
    ss_ev = st.number_input("9. Standart Sapma Ev", value=1.55, step=0.01)

with col2:
    st.markdown("### ✈️ Deplasman")
    mpg_dep = st.number_input("2. MPG Dep", value=2.0, step=0.1)
    siralama_dep = st.number_input("4. Sıralama Dep", value=3, step=1)
    reaksiyon_dep = st.number_input("5. Reaksiyon Gücü Dep (%)", value=60.0, step=0.1)
    xg_dep = st.number_input("6. xG Dep", value=1.64, step=0.01)
    atilan_dep = st.number_input("7. Atılan Gol Dep", value=2.0, step=0.1)
    yenen_dep = st.number_input("8. Yenen Gol Dep", value=1.2, step=0.1)
    ss_dep = st.number_input("9. Standart Sapma Dep", value=0.94, step=0.01)

st.divider()
kg_oran = st.number_input("10. KG Oranı / Sıklığı (%)", value=55.0, step=1.0)

st.divider()

if st.button("🚀 Manuel Analizi Çalıştır", type="primary", use_container_width=True):
    # Sıralama ve Formülasyon
    siralama_puani_ev = max(20 - siralama_ev, 1) * 0.2
    siralama_puani_dep = max(20 - siralama_dep, 1) * 0.2

    guc_ev = (ppg_ev * 1.5) + (xg_ev * 1.6) + (atilan_ev * 1.1) + (reaksiyon_ev * 0.02) + siralama_puani_ev - (yenen_ev * 0.4)
    guc_dep = (mpg_dep * 1.5) + (xg_dep * 1.6) + (atilan_dep * 1.1) + (reaksiyon_dep * 0.02) + siralama_puani_dep - (yenen_dep * 0.4)
    
    toplam_guc = guc_ev + guc_dep if (guc_ev + guc_dep) > 0 else 1
    
    oran_ev = min(max((guc_ev / toplam_guc) * 100, 15), 72)
    oran_dep = min(max((guc_dep / toplam_guc) * 100, 15), 72)
    oran_beraberlik = max(100 - (oran_ev + oran_dep), 15)
    
    toplam_oran = oran_ev + oran_dep + oran_beraberlik
    oran_ev = (oran_ev / toplam_oran) * 100
    oran_dep = (oran_dep / toplam_oran) * 100
    oran_beraberlik = (oran_beraberlik / toplam_oran) * 100

    cifte_1x = oran_ev + oran_beraberlik
    cifte_x2 = oran_dep + oran_beraberlik
    cifte_12 = oran_ev + oran_dep

    tahmini_gol = (xg_ev + xg_dep + atilan_ev + atilan_dep) / 2

    st.success("🎯 Manuel Girdi Analizi Başarıyla Tamamlandı!")

    # --- 1. ANA MAÇ SONUCU VE ÇİZELGE ---
    st.subheader("📊 1X2 Maç Sonucu Dağılımı")
    c1, c2, c3 = st.columns(3)
    c1.metric("1 (Ev Sahibi)", f"%{oran_ev:.1f}")
    c2.metric("X (Beraberlik)", f"%{oran_beraberlik:.1f}")
    c3.metric("2 (Deplasman)", f"%{oran_dep:.1f}")

    st.progress(int(oran_ev), text=f"Ev Sahibi Kazanma Gücü: %{oran_ev:.1f}")
    st.progress(int(oran_beraberlik), text=f"Beraberlik İhtimali: %{oran_beraberlik:.1f}")
    st.progress(int(oran_dep), text=f"Deplasman Kazanma Gücü: %{oran_dep:.1f}")

    st.divider()

    # --- 2. ÇİFTE ŞANS PANELİ ---
    st.subheader("🛡️ Çifte Şans & Güven Paneli")
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("1X (Ev/Beraberlik)", f"%{cifte_1x:.1f}")
    cc2.metric("X2 (Dep/Beraberlik)", f"%{cifte_x2:.1f}")
    cc3.metric("12 (Sürpriz / Tek Maç)", f"%{cifte_12:.1f}")

    st.divider()

    # --- 3. GOL VE ALT/ÜST ANALİZİ ---
    st.subheader("⚽ Gol & Üst/Alt Senaryoları")
    gc1, gc2 = st.columns(2)
    gc1.metric("📊 Tahmini Maç Golü", f"{tahmini_gol:.2f} Gol")
    gc2.metric("⚡ Karşılıklı Gol (KG) Oranı", f"%{kg_oran}")

    if tahmini_gol > 2.6:
        st.error("🔥 **Yapay Zeka Yorumu:** Girilen veriler yüksek skor potansiyeline işaret ediyor. **2.5 Üst** ve **KG Var** güçlü aday.")
    else:
        st.info("🛡️ **Yapay Zeka Yorumu:** Veriler dengeli ve kontrollü bir oyunu işaret ediyor.")

    st.divider()

    # --- 4. DETAYLI MAÇ SENARYOSU ---
    st.subheader("📝 Detaylı Maç Özeti & Taktiksel Bakış")
    st.markdown(f"""
    * **Form & Sıralama Etkisi:** Ev sahibi PPG ({ppg_ev}) ve sıralama konumu değerlendirildi.
    * **Kriz Yönetimi (Reaksiyon):** Takımların reaksiyon güçleri senaryoya yansıtıldı.
    * **Önerilen Strateji:** Güvenli tercihler için **Çifte Şans ({'1X' if oran_ev >= oran_dep else 'X2'})** ön planda tutulabilir.
    """)
