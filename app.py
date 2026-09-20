import streamlit as st
import re

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #1f77b4;'>⚽ Futbol Analiz Pro Sistemi</h1>
    <p style='text-align: center; color: gray;'>Gelişmiş Yapay Zeka Destekli Maç Tahmin ve Senaryo Paneli</p>
""", unsafe_allow_html=True)

st.divider()

# Metin kutusu (Tertemiz ve donmasız)
ham_veri = st.text_area(
    "📋 Maç Bilgilerini Buraya Yapıştırın:", 
    height=180, 
    placeholder="1 Ev takım ... \n2 Dep takım ... \n..."
)

def sayi_bul(metin, anahtar, varsayilan):
    pattern = rf"{anahtar}\D*([0-9]+[.,]?[0-9]*)"
    eslesme = re.search(pattern, metin, re.IGNORECASE)
    if eslesme:
        try:
            return float(eslesme.group(1).replace(',', '.'))
        except:
            return varsayilan
    return varsayilan

if st.button("🚀 Gelişmiş Analizi Çalıştır", type="primary", use_container_width=True):
    if not ham_veri.strip():
        st.warning("⚠️ Lütfen analizi yapılacak verileri yapıştırın!")
    else:
        # Verileri ayıkla
        xg_ev = sayi_bul(ham_veri, "xG Ev", 1.5)
        xg_dep = sayi_bul(ham_veri, "xG Dep", 1.3)
        atilan_ev = sayi_bul(ham_veri, "Atılan Ev", 1.5)
        atilan_dep = sayi_bul(ham_veri, "Atılan Dep", 1.2)
        yenen_ev = sayi_bul(ham_veri, "Yenen Ev", 1.0)
        yenen_dep = sayi_bul(ham_veri, "Yenen Dep", 1.1)
        sut_ev = sayi_bul(ham_veri, "Toplam Şut Ev", 15.0)
        sut_dep = sayi_bul(ham_veri, "Toplam Şut Dep", 10.0)

        # Gelişmiş Matematiksel Model
        guc_ev = (xg_ev * 1.6) + (atilan_ev * 1.1) + (sut_ev * 0.08) - (yenen_ev * 0.4)
        guc_dep = (xg_dep * 1.6) + (atilan_dep * 1.1) + (sut_dep * 0.08) - (yenen_dep * 0.4)
        
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

        st.success("🎯 Gelişmiş Yapay Zeka Analizi Tamamlandı!")

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
        
        kg_ihtimali = min(max(((xg_ev + xg_dep) / 3) * 100, 25), 88)
        gc2.metric("⚡ Karşılıklı Gol (KG) Var", f"%{kg_ihtimali:.1f}")

        if tahmini_gol > 2.6:
            st.error("🔥 **Yapay Zeka Yorumu:** Maç yüksek skor potansiyeline sahip. **2.5 Üst** ve **KG Var** seçenekleri kuponlar için oldukça ideal bir profil çiziyor.")
        elif tahmini_gol >= 2.0:
            st.warning("⚖️ **Yapay Zeka Yorumu:** Karşılaşma ortalama bir gol temposunda geçmeye aday. **1.5 Üst** ve karşılıklı kontrollü bir oyun bekleniyor.")
        else:
            st.info("🛡️ **Yapay Zeka Yorumu:** Kısıtlı ve düşük tempolu geçmesi muhtemel. **ALT** seçenekleri ve az gol senaryoları değerlendirilebilir.")

        st.divider()

        # --- 4. DETAYLI MAÇ SENARYOSU ---
        st.subheader("📝 Detaylı Maç Özeti & Taktiksel Bakış")
        st.markdown(f"""
        * **Hücum Üstünlüğü:** Ev sahibi takımın xG ({xg_ev}) ve şut hacmi verileri, baskılı başlamak istediklerini gösteriyor.
        * **Deplasman Reaksiyonu:** Deplasman ekibinin xG değeri ({xg_dep}) skoru eşitleme veya maçta kalma potansiyelinin yüksek olduğuna işaret ediyor.
        * **Önerilen Strateji:** Risk severler için yüksek oranlı tercihler, garanti arayanlar için ise **Çifte Şans ({'1X' if oran_ev >= oran_dep else 'X2'})** ve gol limitleri ön planda tutulabilir.
        """)
