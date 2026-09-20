import streamlit as st
import re

st.set_page_config(page_title="Futbol Analiz V12", page_icon="⚽", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #1f77b4;'>⚽ Futbol Analiz Sistemi</h1>
    <p style='text-align: center; color: gray;'>Sadeleştirilmiş maç verilerini aşağıya yapıştır, analiz et!</p>
""", unsafe_allow_html=True)

st.divider()

ham_veri = st.text_area("📋 Maç Bilgilerini Buraya Yapıştırın:", height=220, placeholder="Örn:\n1 Ev takım VfB Stuttgart\n2 Dep takım Borussia Dortmund\n...")

def sayi_bul(metin, anahtar, varsayilan):
    pattern = rf"{anahtar}\D*([0-9]+[.,]?[0-9]*)"
    eslesme = re.search(pattern, metin, re.IGNORECASE)
    if eslesme:
        try:
            return float(eslesme.group(1).replace(',', '.'))
        except:
            return varsayilan
    return varsayilan

if st.button("🚀 Analizi Çalıştır", type="primary", use_container_width=True):
    if not ham_veri.strip():
        st.warning("⚠️ Lütfen verileri yapıştırın!")
    else:
        # Sizin sadeleştirilmiş ana parametreleriniz
        xg_ev = sayi_bul(ham_veri, "xG Ev", 1.5)
        xg_dep = sayi_bul(ham_veri, "xG Dep", 1.3)
        
        atilan_ev = sayi_bul(ham_veri, "Atılan Ev", 1.5)
        atilan_dep = sayi_bul(ham_veri, "Atılan Dep", 1.2)
        
        yenen_ev = sayi_bul(ham_veri, "Yenen Ev", 1.0)
        yenen_dep = sayi_bul(ham_veri, "Yenen Dep", 1.1)
        
        sut_ev = sayi_bul(ham_veri, "Toplam Şut Ev", 15.0)
        sut_dep = sayi_bul(ham_veri, "Toplam Şut Dep", 10.0)

        # Temel Matematiksel Ağırlıklandırma
        guc_ev = (xg_ev * 1.5) + (atilan_ev * 1.0) + (sut_ev * 0.1)
        guc_dep = (xg_dep * 1.5) + (atilan_dep * 1.0) + (sut_dep * 0.1)
        
        toplam_guc = guc_ev + guc_dep if (guc_ev + guc_dep) > 0 else 1
        oran_ev = min(max((guc_ev / toplam_guc) * 100, 15), 75)
        oran_dep = min(max((guc_dep / toplam_guc) * 100, 15), 75)
        oran_beraberlik = max(100 - (oran_ev + oran_dep), 12)

        st.success("✅ Analiz başarıyla tamamlandı!")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("1 (Ev)", f"%{oran_ev:.1f}")
        col2.metric("X (Berabere)", f"%{oran_beraberlik:.1f}")
        col3.metric("2 (Dep)", f"%{oran_dep:.1f}")
        
        st.divider()
        st.subheader("🎲 Gol & Maç Senaryosu")
        tahmini_gol = (xg_ev + xg_dep + atilan_ev + atilan_dep) / 2
        st.write(f"📊 **Tahmini Gol Ortalaması:** {tahmini_gol:.2f}")
        
        if tahmini_gol > 2.5:
            st.info("🔥 **Öneri:** KG Var ve 2.5 Üst için oldukça uygun bir maç.")
        else:
            st.info("🛡️ **Öneri:** Dengeli/Kısıtlı geçebilir, Alt alternatifleri değerlendirilebilir.")
