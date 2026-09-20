import streamlit as st

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

# Sayfa yönetimi için hafıza kontrolü
if "sayfa" not in st.session_state:
    st.session_state.sayfa = "giris"

# Form verileri için hafıza (İlk açılışta veya temizlendiğinde sıfır/boş başlar)
if "veriler" not in st.session_state:
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

# ==========================================
# 1. SAYFA: İSTATİSTİK GİRİŞ EKRANI (BOŞ BAŞLAR)
# ==========================================
if st.session_state.sayfa == "giris":
    st.markdown("""
        <h1 style='text-align: center; color: #1f77b4;'>⚽ Futbol Analiz Pro Sistemi</h1>
        <p style='text-align: center; color: gray;'>İstatistikleri gir, profesyonel analiz sayfasına geçiş yap!</p>
    """, unsafe_allow_html=True)

    st.divider()
    st.subheader("📋 Sıralı Maç İstatistikleri Giriş Paneli")

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

    col_b1, col_b2 = st.columns(2)
    calistir = col_b1.button("🚀 Analizi Çalıştır (Sonuç Sayfasına Git)", type="primary", use_container_width=True)
    temizle = col_b2.button("🧹 Alanları Temizle", use_container_width=True)

    if temizle:
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
        st.rerun()

    if calistir:
        st.session_state.sayfa = "sonuc"
        st.rerun()

# ==========================================
# 2. SAYFA: TEK SAYFA ANALİZ SONUÇ EKRANI
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.veriler

    # Sıralama ve Formülasyon
    siralama_puani_ev = max(20 - v["siralama_ev"], 1) * 0.2
    siralama_puani_dep = max(20 - v["siralama_dep"], 1) * 0.2

    guc_ev = (v["ppg_ev"] * 1.5) + (v["xg_ev"] * 1.6) + (v["atilan_ev"] * 1.1) + (v["reaksiyon_ev"] * 0.02) + siralama_puani_ev - (v["yenen_ev"] * 0.4)
    guc_dep = (v["mpg_dep"] * 1.5) + (v["xg_dep"] * 1.6) + (v["atilan_dep"] * 1.1) + (v["reaksiyon_dep"] * 0.02) + siralama_puani_dep - (v["yenen_dep"] * 0.4)
    
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

    tahmini_gol = (v["xg_ev"] + v["xg_dep"] + v["atilan_ev"] + v["atilan_dep"]) / 2

    st.markdown("""
        <h1 style='text-align: center; color: #2ca02c;'>🎯 Maç Analiz Sonuç Paneli</h1>
        <p style='text-align: center; color: gray;'>Yapay Zeka Değerlendirme Raporu</p>
    """, unsafe_allow_html=True)

    st.divider()

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
    gc2.metric("⚡ Karşılıklı Gol (KG) Oranı", f"%{v['kg_oran']}")

    if tahmini_gol > 2.6:
        st.error("🔥 **Yapay Zeka Yorumu:** Girilen veriler yüksek skor potansiyeline işaret ediyor. **2.5 Üst** ve **KG Var** güçlü aday.")
    else:
        st.info("🛡️ **Yapay Zeka Yorumu:** Veriler dengeli ve kontrollü bir oyunu işaret ediyor.")

    st.divider()

    # --- 4. DETAYLI MAÇ SENARYOSU ---
    st.subheader("📝 Detaylı Maç Özeti & Taktiksel Bakış")
    st.markdown(f"""
    * **Form & Sıralama Etkisi:** Ev sahibi PPG ({v['ppg_ev']}) ve sıralama konumu değerlendirildi.
    * **Kriz Yönetimi (Reaksiyon):** Takımların reaksiyon güçleri senaryoya yansıtıldı.
    * **Önerilen Strateji:** Güvenli tercihler için **Çifte Şans ({'1X' if oran_ev >= oran_dep else 'X2'})** ön planda tutulabilir.
    """)

    st.divider()

    # --- 5. YENİ ANALİZ / İSTATİSTİK SAYFASINA DÖNÜŞ BUTONU ---
    if st.button("🔄 Yeni Maç / Yeni Analiz (İstatistik Sayfasına Dön)", type="primary", use_container_width=True):
        # Alanları sıfırla ve giriş sayfasına git
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
