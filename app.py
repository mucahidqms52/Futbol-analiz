================================
# ÜST BAR
# ==========================================
def ust_bar():
    c1, c2 = st.columns([3, 1])
    with c1:
        if admin_mi():
            st.markdown('<div style="padding:6px 0; font-size:0.8rem; color:#22c55e; font-weight:700;">👑 Admin Modu</div>', unsafe_allow_html=True)
        elif uye_mi():
            premium = uye_premium_mu()
            if premium:
                badge = '🌟 <span style="color:#22c55e;font-weight:700;">PREMIUM</span>'
                try:
                    k = kullanicilar_yukle().get(uye_adi(), {})
                    bs = k.get("abonelik_bitis")
                    if bs:
                        bt = datetime.strptime(bs, "%Y-%m-%d"); kl = (bt - datetime.now()).days
                        if kl >= 0: badge += f' <span style="color:#8fa0bd;font-size:0.72rem;">({kl} gün kaldı)</span>'
                except Exception: pass
                st.markdown(f'<div style="padding:6px 0; font-size:0.8rem; color:#eaf1fb; font-weight:700;">👤 {_e(uye_adi())} &nbsp; {badge}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="padding:6px 0; font-size:0.8rem; color:#f59e0b; font-weight:700;">👤 {_e(uye_adi())} <span style="color:#8fa0bd;font-size:0.72rem;">(abonelik yok)</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="padding:6px 0; font-size:0.8rem; color:#8fa0bd; font-weight:600;">👤 Misafir Modu</div>', unsafe_allow_html=True)
    with c2:
        if admin_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="cikis_btn"):
                st.session_state.rol = "misafir"; st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"
                st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI); st.rerun()
        elif uye_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="uye_cikis_btn"):
                st.session_state.aktif_kullanici = None; st.session_state.sayfa = "giris"; st.rerun()


def misafir_aciklama():
    with st.expander("📖 Uygulamayı Tanı ve Kuralları Oku", expanded=False):
        st.markdown("""### ⚽ Futbol Analiz Pro
Geçmiş istatistiklere dayalı analiz ve tahminler. Sadece **bilgilendirme amaçlıdır**.

### 🌟 PREMIUM
- Tüm maçlar açık
- Haftalık / Aylık / Yıllık

### 🚫 SORUMLULUK REDDİ
- **18 yaşından küçükler** kullanamaz.
- Yasadışı bahis **suçtur**.
- **Kesin sonuç garantisi yoktur.**
- **YEDAM: 115**
""")


# ==========================================
# NAV BAR
# ==========================================
def nav_git(h):
    st.session_state.sayfa = h
    st.session_state.kayit_yapildi = False
    st.session_state.tek_silme_onay = None
    st.session_state.tek_silme_gelecek = None
    st.session_state.sil_onay_kadi = None
    if h == "backtest": st.session_state.bt_sonuc = None; st.session_state.bt_detaylar = []
    st.rerun()


def nav_bar():
    if st.session_state.sayfa in ("kayit", "uyegirisi", "odeme", "giris_yap"): return
    try: kutu = st.container(key="fa_nav")
    except TypeError: kutu = st.container()
    with kutu:
        if admin_mi():
            sec = [("🏠 Ana Sayfa", "giris"), ("🔮 Gelecek", "gelecek_admin"), ("📊 Geçmiş", "gecmis"), ("🔬 Test", "backtest"), ("💳 Ödemeler", "admin_odemeler"), ("👥 Aboneler", "admin_aboneler"), ("📬 Bildirimler", "admin_bildirimler"), ("⚙️ Ayar", "ayarlar")]
        elif uye_mi():
            sec = [("🏠 Ana Sayfa", "giris"), ("📊 Geçmiş Maçlar", "gecmis"), ("📬 Bildirim", "kullanici_bildirim")]
        else:
            sec = [("🏠 Ana Sayfa", "giris"), ("📊 Geçmiş Maçlar", "gecmis")]
        kl = st.columns(len(sec))
        for k, (e, h) in zip(kl, sec):
            with k:
                aktif = st.session_state.sayfa == h
                if st.button(e, key=f"nav_{h}", use_container_width=True, type="primary" if aktif else "secondary"):
                    if not aktif: nav_git(h)


# ==========================================
# UYGULAMA BAŞLANGIÇ
# ==========================================
_otomatik_baslat()

if st.session_state.admin_login_acik and not admin_mi():
    admin_giris_ekrani()
    st.stop()

ust_bar()
nav_bar()


# ==========================================
# SAYFA: GİRİŞ YAP
# ==========================================
if st.session_state.sayfa == "giris_yap":
    admin_giris_ekrani()


# ==========================================
# SAYFA: ANA SAYFA
# ==========================================
elif st.session_state.sayfa == "giris":
    if admin_mi():
        st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:gray;'>Admin Paneli</p>", unsafe_allow_html=True)
        log = otomatik_log_yukle()
        if log:
            st.markdown("### 🤖 Otomatik Sistem Durumu")
            c1, c2 = st.columns(2)
            with c1:
                st.caption(f"📥 Son veri çekimi: **{log.get('son_veri_cekimi', 'Yok')}**")
                st.caption(f"Durum: **{log.get('son_veri_durum', '-')}**")
            with c2:
                st.caption(f"⚽ Son skor çekimi: **{log.get('son_skor_cekimi', 'Yok')}**")
                st.caption(f"Durum: **{log.get('son_skor_durum', '-')}**")
            st.info("ℹ️ Her gece **02:30**'da veri, **her saat başı** skor çekilir.")

        st.divider()
        st.markdown("### 📋 İstatistik Metnini Yapıştır")
        ym = st.text_area("Yapıştırma", height=200, key="yapistir_input", label_visibility="collapsed", placeholder="İstatistik metnini buraya yapıştır")
        c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
        with c1: analiz_btn = st.button("🚀 ANALİZ ET", use_container_width=True, type="primary")
        with c2: gecmis_btn = st.button("📊 Geçmiş", use_container_width=True)
        with c3: gelecek_btn = st.button("🔮 Gelecek", use_container_width=True)
        with c4: backtest_btn = st.button("🔬 Test", use_container_width=True)
        with c5: ayarlar_btn = st.button("⚙️ Ayar", use_container_width=True)
        if analiz_btn:
            if not ym.strip(): st.warning("⚠️ Metin yapıştır.")
            else:
                cikan, okunamayanlar = metinden_veri_cikar(ym)
                if not cikan: st.error("❌ Veri çıkarılamadı.")
                else:
                    yv = copy.deepcopy(VARSAYILAN_VERI); yv.update(cikan)
                    st.session_state.form_verileri = yv; st.session_state.kayit_yapildi = False
                    st.session_state.manuel_bekleyen = okunamayanlar.copy() if okunamayanlar else []
                    if not veri_yeterli_mi(yv): st.error("⚠️ Yetersiz veri.")
                    else:
                        if okunamayanlar: st.session_state.sayfa = "manuel_giris"
                        else: st.session_state.sayfa = "sonuc"
                        st.rerun()
        if gecmis_btn: nav_git("gecmis")
        if gelecek_btn: nav_git("gelecek_admin")
        if backtest_btn: nav_git("backtest")
        if ayarlar_btn: nav_git("ayarlar")

        st.divider()
        st.markdown("### 🤖 Otomatik Veri Çekme")
        vs1, vs2, vs3 = st.tabs(["🔄 Bugünün Maçları", "📜 Lig Geçmişi", "🏁 Sonuçları İşle"])
        with vs1:
            if st.session_state.toplu_cek_ozet:
                oz = st.session_state.toplu_cek_ozet
                st.markdown(f"**Son:** Bulunan: **{oz.get('bulunan', 0)}** | Eklenen: **{oz.get('eklenen', 0)}** | Eşik altı: **{oz.get('esik_alti', 0)}** | Veri yok: **{oz.get('veri_yok', 0)}** | Zaten vardı: **{oz.get('zaten_var', 0)}** | Hata: **{oz.get('hata', 0)}**")
                if oz.get("detay_log"):
                    with st.expander(f"🔎 Detay"):
                        for s in oz["detay_log"]: st.text(s)
            c1, c2 = st.columns(2)
            with c1: w = st.number_input("Paralel", 1, 4, 3, 1, key="fw")
            with c2:
                st.markdown("")
                if st.button("🚀 Bugünün Maçlarını Çek", use_container_width=True, type="primary", key="mbtn"):
                    ph = st.empty()
                    def _p(i, t, n):
                        try: ph.progress(min((i + 1) / t, 1.0), text=f"{i+1}/{t}: {n}")
                        except Exception: pass
                    with st.spinner("Çekiliyor..."):
                        mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=_p, max_workers=int(w))
                    ph.empty(); st.rerun()
        with vs2:
            lurl = st.text_input("Lig URL", key="lig_url_input", placeholder="https://www.mutating.com/football-stats/league-...")
            c1, c2 = st.columns(2)
            with c1: la = st.number_input("Kaç maç?", 5, 30, 10, 1, key="lig_adet")
            with c2: lw = st.number_input("Paralel", 1, 4, 3, 1, key="lig_workers")
            if st.button("📜 Ligi Çek", use_container_width=True, type="primary", key="lig_cek_btn"):
                if not lurl.strip(): st.warning("URL gerekli")
                else:
                    ph = st.empty()
                    def _p2(i, t, n):
                        try: ph.progress(min((i + 1) / t, 1.0), text=f"{i+1}/{t}: {n}")
                        except Exception: pass
                    with st.spinner(f"Son {la} maç..."):
                        bas, hat = lig_gecmis_cek(lurl.strip(), int(la), int(lw), _p2)
                    ph.empty()
                    if hat:
                        with st.expander(f"⚠️ {len(hat)} hata"):
                            for h in hat: st.caption(h)
                    if bas:
                        st.success(f"✅ {len(bas)} maç eklendi!"); time.sleep(2); st.rerun()
                    else: st.error("Hiçbir maç eklenemedi.")
        with vs3:
            if st.session_state.skor_ozet:
                oz = st.session_state.skor_ozet
                st.success(f"✅ {oz['tasinan']} taşındı • {oz['bitmemis']} bitmemiş")
            st.markdown(f"Bekleyen: **{len(st.session_state.gelecek_analizler)}**")
            sy = st.checkbox("Tarayıcı ile dene", value=False, key="skor_yedek")
            c1, c2 = st.columns(2)
            with c1: sw = st.number_input("Paralel", 1, 4, 3, 1, key="skor_w")
            with c2:
                if st.button("🏁 Skorları Çek", use_container_width=True, type="primary", key="skor_btn"):
                    if not st.session_state.gelecek_analizler: st.warning("Gelecek'te maç yok")
                    else:
                        with st.spinner("Kontrol..."):
                            st.session_state.skor_ozet = sonuclari_isle(bool(sy), int(sw))
                        st.rerun()

    else:
        gelecek = st.session_state.gelecek_analizler
        toplam = len(gelecek)
        premium = uye_premium_mu()
        kota = int(ayar_al("ucretsiz_kotasi", 3))

        if premium:
            kl = ""
            try:
                bs = kullanicilar_yukle().get(uye_adi(), {}).get("abonelik_bitis")
                if bs:
                    kk = (datetime.strptime(bs, "%Y-%m-%d") - datetime.now()).days
                    if kk >= 0: kl = f'<div class="mh-hero-badge">🌟 PREMIUM — {kk} gün kaldı</div>'
            except Exception: pass
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-title" style="font-size:1.25rem;">Hoş Geldin, {_e(uye_adi())}</div><div class="mh-hero-sub">Premium aktif — tüm analizler açık</div>{kl}</div>', unsafe_allow_html=True)
            modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ")
        elif uye_mi():
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-title" style="font-size:1.25rem;">Hoş Geldin, {_e(uye_adi())}</div><div class="mh-hero-sub">İlk {kota} maç ücretsiz açık</div><div class="mh-hero-badge" style="background:rgba(245,158,11,0.12);border-color:rgba(245,158,11,0.5);color:#f59e0b !important;">⚠️ ABONELİK YOK</div></div>', unsafe_allow_html=True)
            modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ")
            if st.button("💳 Premium'a Geç  •  ✨ Üye Ol", use_container_width=True, type="primary", key="ana_premium_btn"):
                st.session_state["odeme_hedef_kadi"] = uye_adi(); st.session_state.sayfa = "odeme"; st.rerun()
        else:
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-title" style="font-size:1.25rem;">Bugün {toplam} Maç</div><div class="mh-hero-sub">İlk {kota} maç ücretsiz açık</div></div>', unsafe_allow_html=True)
            modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ")
            if st.button("💳 Premium'a Geç  •  ✨ Üye Ol", use_container_width=True, type="primary", key="mis_prem"):
                st.session_state.sayfa = "kayit"; st.rerun()
            if st.button("🔐 Giriş Yap", use_container_width=True, key="mis_giris_btn"):
                st.session_state.sayfa = "giris_yap"; st.rerun()

        st.divider()
        if not gelecek: st.info("ℹ️ Henüz maç yok.")
        else:
            sirali = sorted(enumerate(gelecek), key=lambda x: saat_sirala_anahtari(x[1]))
            acik = 0
            for idx, g in sirali:
                v = g["veri"]; te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
                ulke = v.get("ulke", ""); saat = v.get("saat", ""); tarih = v.get("tarih", "")
                if premium or acik < kota:
                    try:
                        af = analiz_hesapla(v); le = af["lam_ev"]; ld = af["lam_dep"]
                    except Exception: le = ld = 0
                    st.markdown(mac_karti(te, td, False, 0, 0, le, ld, saat, ulke, tarih), unsafe_allow_html=True)
                    th = mac_tahmin_karti(v, g)
                    if th: st.markdown(th, unsafe_allow_html=True)
                    if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"gmac_{idx}"):
                        st.session_state.form_verileri = copy.deepcopy(v); st.session_state.kayit_yapildi = True
                        st.session_state.gelecekten_gelindi = True; st.session_state.aktif_gelecek_idx = idx
                        st.session_state.sayfa = "sonuc"; st.rerun()
                    acik += 1
                else:
                    st.markdown(kilitli_mac_karti(te, td, saat, ulke, tarih), unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("💳 Premium", use_container_width=True, key=f"kp_{idx}", type="primary"):
                            if uye_mi(): st.session_state["odeme_hedef_kadi"] = uye_adi(); st.session_state.sayfa = "odeme"
                            else: st.session_state.sayfa = "kayit"
                            st.rerun()
                    with c2:
                        if st.button("🔑 Giriş", use_container_width=True, key=f"kg_{idx}"):
                            st.session_state.sayfa = "giris_yap"; st.rerun()
                st.divider()

        yasal_metin_goster()
        misafir_aciklama()
        st.markdown('<div class="login-footer" style="margin-top:20px;">© <b>Futbol Analiz Pro</b> • Bilgi amaçlıdır</div>', unsafe_allow_html=True)
        # ==========================================
# SAYFA: KAYIT
# ==========================================
elif st.session_state.sayfa == "kayit":
    st.markdown('''<div class="login-hero"><div class="login-logo">✨</div><h1 class="login-title">Üye Ol</h1><p class="login-subtitle">Kullanıcı adı ve şifre belirle</p></div>''', unsafe_allow_html=True)
    with st.form("kayit_form"):
        yk = st.text_input("👤 Kullanıcı Adı", placeholder="örn: ahmet34", max_chars=30)
        ys = st.text_input("🔐 Şifre", type="password", placeholder="En az 4 karakter")
        yst = st.text_input("🔐 Şifre Tekrar", type="password", placeholder="Şifreyi tekrar gir")
        yasal_onay = st.checkbox("✅ **Kullanım Şartlarını, Sorumluluk Reddini ve KVKK metnini okudum, kabul ediyorum.** 18 yaşından büyük olduğumu beyan ederim.", key="kayit_yasal_onay_cb")
        c1, c2 = st.columns(2)
        with c1: kb = st.form_submit_button("✅ Kayıt Ol", use_container_width=True, type="primary")
        with c2: gb = st.form_submit_button("⬅️ Geri", use_container_width=True)
        if kb:
            if not yk.strip(): st.error("❌ Kullanıcı adı boş olamaz.")
            elif len(yk.strip()) < 3: st.error("❌ En az 3 karakter.")
            elif not yk.replace("_", "").isalnum(): st.error("❌ Sadece harf, rakam, _")
            elif yk.strip() == ADMIN_KULLANICI_ADI: st.error("❌ Bu isim kullanılamaz.")
            elif len(ys) < 4: st.error("❌ Şifre en az 4 karakter.")
            elif ys != yst: st.error("❌ Şifreler uyuşmuyor.")
            elif not yasal_onay: st.error("❌ Kayıt için Kullanım Şartlarını kabul etmelisiniz.")
            else:
                b, m = kullanici_ekle(yk.strip(), ys)
                if b:
                    st.session_state["aktif_kullanici"] = yk.strip()
                    st.session_state["odeme_hedef_kadi"] = yk.strip()
                    st.success(f"✅ {m} Ödeme sayfasına yönlendiriliyorsun...")
                    time.sleep(1.5); st.session_state.sayfa = "odeme"; st.rerun()
                else: st.error(f"❌ {m}")
        if gb: st.session_state.sayfa = "giris"; st.rerun()
    yasal_metin_goster()


# ==========================================
# SAYFA: ÜYE GİRİŞİ
# ==========================================
elif st.session_state.sayfa == "uyegirisi":
    st.markdown('''<div class="login-hero"><div class="login-logo">🔑</div><h1 class="login-title">Üye Girişi</h1></div>''', unsafe_allow_html=True)
    with st.form("uye_giris_form"):
        k = st.text_input("👤 Kullanıcı Adı")
        s = st.text_input("🔐 Şifre", type="password")
        c1, c2 = st.columns(2)
        with c1: g = st.form_submit_button("🔓 Giriş", use_container_width=True, type="primary")
        with c2: gg = st.form_submit_button("⬅️ Geri", use_container_width=True)
        if g:
            if not k.strip() or not s: st.error("❌ Bilgiler gerekli.")
            elif kullanici_dogrula(k.strip(), s):
                st.session_state["aktif_kullanici"] = k.strip()
                st.success(f"✅ Hoş geldin, {k.strip()}!")
                time.sleep(1); st.session_state.sayfa = "giris"; st.rerun()
            else: st.error("❌ Hatalı giriş.")
        if gg: st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: ÖDEME
# ==========================================
elif st.session_state.sayfa == "odeme":
    hedef = st.session_state.get("odeme_hedef_kadi") or uye_adi()
    if not hedef:
        st.error("❌ Kullanıcı yok.")
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary"):
            st.session_state.sayfa = "giris"; st.rerun()
        st.stop()
    iban = ayar_al("iban", "TR00 0000 0000 0000 0000 0000 00")
    hs = ayar_al("hesap_sahibi", "ADINIZ SOYADINIZ")
    fh = float(ayar_al("fiyat_haftalik", 49.0)); fa = float(ayar_al("fiyat_aylik", 149.0)); fy = float(ayar_al("fiyat_yillik", 999.0))
    st.markdown(f'''<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-icon">💳</div><div class="mh-hero-title">Premium'a Geç</div><div class="mh-hero-sub">Havale / EFT ile ödeme</div><div class="mh-hero-badge">● GÜVENLİ ÖDEME</div></div>''', unsafe_allow_html=True)
    st.markdown(f'''<div class="mh-info"><b>👤 Kullanıcı:</b> {_e(hedef)}<br>Açıklama kısmına <b>MUTLAKA</b> kullanıcı adını yaz.</div>''', unsafe_allow_html=True)
    st.markdown("### 📆 Paket Seç")
    sec = st.radio("Süre?", ["haftalik", "aylik", "yillik"], format_func=lambda x: {"haftalik": f"📅 Haftalık — {fh:.0f} ₺", "aylik": f"📆 Aylık — {fa:.0f} ₺", "yillik": f"🎯 Yıllık — {fy:.0f} ₺"}[x], index=1, key="odeme_sure_sec")
    sg = {"haftalik": 7, "aylik": 30, "yillik": 365}[sec]
    fy_ = {"haftalik": fh, "aylik": fa, "yillik": fy}[sec]
    et = {"haftalik": "Haftalık", "aylik": "Aylık", "yillik": "Yıllık"}[sec]
    if sec == "yillik":
        ai = fa * 12
        ind = int((1 - (fy / ai)) * 100) if ai > 0 else 0
        if ind > 0:
            st.markdown(f'<div class="fa-card fa-pos"><div class="fa-ttl">Seçilen</div><div class="fa-pickrow"><div class="fa-pick">🎯 Yıllık</div><div class="fa-pct">{fy_:.0f} ₺</div></div><div class="fa-mut">💸 %{ind} indirim!</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="fa-card fa-pos"><div class="fa-ttl">Seçilen</div><div class="fa-pickrow"><div class="fa-pick">🎯 Yıllık</div><div class="fa-pct">{fy_:.0f} ₺</div></div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="fa-card fa-pos"><div class="fa-ttl">Seçilen</div><div class="fa-pickrow"><div class="fa-pick">{et}</div><div class="fa-pct">{fy_:.0f} ₺</div></div></div>', unsafe_allow_html=True)
    st.markdown("### 🏦 Havale Bilgileri")
    st.markdown(f'<div class="fa-card"><div class="fa-ttl">Alıcı</div><div class="fa-pick" style="margin-bottom:10px;">{_e(hs)}</div><div class="fa-ttl">IBAN</div><div class="fa-pick" style="margin-bottom:10px;font-family:monospace;">{_e(iban)}</div><div class="fa-ttl">Tutar</div><div class="fa-pick" style="margin-bottom:10px;color:#22c55e;">{fy_:.0f} ₺</div><div class="fa-ttl">Açıklama</div><div class="fa-pick" style="color:#22c55e;font-weight:900;">{_e(hedef)}</div></div>', unsafe_allow_html=True)
    st.divider()
    st.markdown("### ✅ Ödemeyi Yaptım")
    bk = bekleyen_yukle()
    if hedef in bk and bk[hedef].get("durum") == "bekliyor":
        st.warning(f"⏳ Zaten bekleyen bildirimin var: **{bk[hedef].get('sure_etiket', '?')}**")
    else:
        iade_onay = st.checkbox("✅ **İade yapılmayacağını, hizmetin dijital olduğunu ve aktivasyon sonrası para iadesi talep edemeyeceğimi okudum, kabul ediyorum.**", key="odeme_yasal_onay_cb")
        if st.button("📤 Ödeme Yaptım — Bildir", use_container_width=True, type="primary", key="odeme_bildir_btn"):
            if not iade_onay: st.error("❌ İade koşullarını kabul etmelisiniz.")
            else:
                bk[hedef] = {"tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "sure_gun": int(sg), "sure_etiket": et, "fiyat": float(fy_), "durum": "bekliyor"}
                bekleyen_kaydet(bk)
                st.success("✅ Bildirimin alındı!"); time.sleep(2); st.rerun()
    yasal_metin_goster()
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="odeme_geri"):
            st.session_state.sayfa = "giris"; st.rerun()
    with c2:
        if st.button("🔄 Kontrol Et", use_container_width=True, key="odeme_kontrol"):
            if abonelik_aktif_mi(hedef):
                st.success("✅ Aboneliğin aktif!"); time.sleep(1.5); st.session_state.sayfa = "giris"; st.rerun()
            else: st.info("⏳ Bekleniyor.")


# ==========================================
# SAYFA: ADMIN ÖDEMELER
# ==========================================
elif st.session_state.sayfa == "admin_odemeler":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>💳 Bekleyen Ödemeler</h1>", unsafe_allow_html=True)
    bk = bekleyen_yukle()
    if not bk: st.info("ℹ️ Bekleyen ödeme yok.")
    else:
        for k, b in list(bk.items()):
            tg = b.get("sure_gun", 0); te = b.get("sure_etiket", "?"); fi = b.get("fiyat", 0); tt = b.get("tarih", "?")
            st.markdown(f'<div class="fa-card"><div class="fa-ttl">👤 {_e(k)}</div><div class="fa-pickrow"><div><div class="fa-pick">{te} — {fi:.0f} ₺</div><div class="fa-mut">📅 {_e(tt)}</div></div></div></div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button(f"✅ Onayla", use_container_width=True, type="primary", key=f"o_{k}"):
                    b_, yb = abonelik_aktif_et(k, tg)
                    if b_:
                        del bk[k]; bekleyen_kaydet(bk)
                        st.success(f"✅ {k} aktif! Bitiş: {yb}"); time.sleep(2); st.rerun()
            with c2:
                if st.button(f"❌ Reddet", use_container_width=True, key=f"r_{k}"):
                    del bk[k]; bekleyen_kaydet(bk); st.info("Silindi."); time.sleep(1.5); st.rerun()
            with c3:
                if st.button(f"🗑️ Sil", use_container_width=True, key=f"s_{k}"):
                    del bk[k]; bekleyen_kaydet(bk); st.rerun()
            st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="og"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: ADMIN ABONELER
# ==========================================
elif st.session_state.sayfa == "admin_aboneler":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>👥 Aboneler</h1>", unsafe_allow_html=True)
    st.caption("Abonelik süresi ekleme sadece 💳 Ödemeler sayfasından yapılır.")
    kl = kullanicilar_yukle()
    if not kl:
        st.info("ℹ️ Kayıtlı kullanıcı yok.")
    else:
        top = len(kl); ak = sum(1 for k in kl if abonelik_aktif_mi(k))
        st.markdown(f'<div class="mh-stat-grid"><div class="mh-stat"><div class="mh-stat-icon">👥</div><div class="mh-stat-num">{top}</div><div class="mh-stat-lbl">Toplam</div></div><div class="mh-stat"><div class="mh-stat-icon">🌟</div><div class="mh-stat-num">{ak}</div><div class="mh-stat-lbl">Aktif</div></div></div>', unsafe_allow_html=True)
        st.divider()
        for k, kd in list(kl.items()):
            kt = kd.get("kayit_tarihi", "?"); bs = kd.get("abonelik_bitis")
            aktif = abonelik_aktif_mi(k); kalan = 0
            if bs:
                try: kalan = (datetime.strptime(bs, "%Y-%m-%d") - datetime.now()).days
                except Exception: pass
            if aktif: dr = "#22c55e"; dt = f"🌟 AKTİF ({kalan} gün)"; ek = f"Bitiş: {bs}"
            elif bs: dr = "#ef4444"; dt = "⛔ SÜRESİ DOLMUŞ"; ek = f"Bitiş: {bs}"
            else: dr = "#94a3b8"; dt = "⚪ YOK"; ek = ""
            st.markdown(f'<div class="fa-card"><div class="fa-pickrow"><div><div class="fa-pick">👤 {_e(k)}</div><div class="fa-mut">📅 {_e(kt)} &nbsp; {_e(ek)}</div></div><div style="color:{dr};font-weight:800;font-size:0.85rem;">{_e(dt)}</div></div></div>', unsafe_allow_html=True)
            ca, cb = st.columns(2)
            with ca:
                if st.button("🚫 İptal Et", use_container_width=True, key=f"ip_{k}"):
                    abonelik_iptal_et(k); st.warning("İptal edildi."); time.sleep(1.5); st.rerun()
            with cb:
                if st.button("🗑️ Sil", use_container_width=True, key=f"ks_{k}"):
                    st.session_state.sil_onay_kadi = k
            if st.session_state.sil_onay_kadi == k:
                st.warning(f"⚠️ **{k}** kullanıcısını silmek istediğinizden emin misiniz?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Evet, Sil", key=f"yes_{k}", use_container_width=True, type="primary"):
                        kullanici_sil(k); st.session_state.sil_onay_kadi = None
                        st.success("Silindi."); time.sleep(1.5); st.rerun()
                with c2:
                    if st.button("❌ Vazgeç", key=f"no_{k}", use_container_width=True):
                        st.session_state.sil_onay_kadi = None; st.rerun()
            st.markdown("")
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="abg"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: ADMIN BİLDİRİMLER
# ==========================================
elif st.session_state.sayfa == "admin_bildirimler":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>📬 Bildirimler</h1>", unsafe_allow_html=True)
    bd = bildirimler_yukle()
    if not bd: st.info("ℹ️ Bildirim yok.")
    else:
        for b in sorted(bd, key=lambda x: x.get("tarih", ""), reverse=True):
            bid = b.get("id"); tip = b.get("tip", "diger")
            tb = BILDIRIM_TIPLERI.get(tip, BILDIRIM_TIPLERI["diger"])
            durum = b.get("durum", "okunmadi")
            border = "#22c55e" if durum == "okunmadi" else "#94a3b8"
            st.markdown(f'''<div class="fa-bildirim {tb['sinif']}" style="border-left-color:{border};"><div class="fa-bildirim-ttl">{tb['ikon']} {tb['isim']} — <b>{_e(b.get('kullanici', '?'))}</b> {"🆕" if durum == "okunmadi" else ""}</div><div class="fa-bildirim-msg"><b>Konu:</b> {_e(b.get('konu', ''))}<br>{_e(b.get('mesaj', ''))}</div><div class="fa-bildirim-meta">📅 {_e(b.get('tarih', '?'))}</div></div>''', unsafe_allow_html=True)
            if b.get("cevap"): st.info(f"💬 Cevabın: {b['cevap']}")
            with st.expander("💬 Cevapla / Sil"):
                yanit = st.text_area("Yanıtın", value=b.get("cevap", ""), key=f"cy_{bid}")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("💬 Kaydet", key=f"kaydet_{bid}", use_container_width=True, type="primary"):
                        bildirim_guncelle(bid, cevap=yanit, durum="okundu")
                        st.success("Kaydedildi."); time.sleep(1); st.rerun()
                with c2:
                    if st.button("✅ Okundu", key=f"ok_{bid}", use_container_width=True):
                        bildirim_guncelle(bid, durum="okundu"); st.rerun()
                with c3:
                    if st.button("🗑️ Sil", key=f"sil_{bid}", use_container_width=True):
                        bildirim_sil(bid); st.rerun()
            st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="bdg"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: KULLANICI BİLDİRİM
# ==========================================
elif st.session_state.sayfa == "kullanici_bildirim":
    if not uye_mi(): st.error("❌ Giriş yap."); st.stop()
    st.markdown("<h1>📬 Bildirim Gönder</h1>", unsafe_allow_html=True)
    st.caption("İptal talebi, şikayet, görüş ve önerilerini buradan iletebilirsin.")
    with st.form("bildirim_form"):
        tip = st.selectbox("Kategori", options=list(BILDIRIM_TIPLERI.keys()), format_func=lambda x: f"{BILDIRIM_TIPLERI[x]['ikon']} {BILDIRIM_TIPLERI[x]['isim']}")
        konu = st.text_input("Konu", placeholder="Kısa başlık...")
        mesaj = st.text_area("Mesaj", placeholder="Detaylı açıklamanı yaz...", height=150)
        c1, c2 = st.columns(2)
        with c1: gb = st.form_submit_button("📤 Gönder", use_container_width=True, type="primary")
        with c2: gb2 = st.form_submit_button("⬅️ Geri", use_container_width=True)
        if gb:
            if not konu.strip() or not mesaj.strip(): st.error("❌ Konu ve mesaj gerekli.")
            else:
                bildirim_ekle(uye_adi(), tip, konu.strip(), mesaj.strip())
                st.success("✅ Bildirimin gönderildi!")
                time.sleep(2); st.rerun()
        if gb2: st.session_state.sayfa = "giris"; st.rerun()
    st.divider()
    st.markdown("### 📋 Gönderdiğin Bildirimler")
    bl = kullanici_bildirimleri(uye_adi())
    if not bl: st.info("Henüz bildirim yok.")
    else:
        for b in sorted(bl, key=lambda x: x.get("tarih", ""), reverse=True):
            tip = b.get("tip", "diger"); tb = BILDIRIM_TIPLERI.get(tip, BILDIRIM_TIPLERI["diger"])
            st.markdown(f'''<div class="fa-bildirim {tb['sinif']}"><div class="fa-bildirim-ttl">{tb['ikon']} {tb['isim']} — {b.get('durum', '?')}</div><div class="fa-bildirim-msg"><b>Konu:</b> {_e(b.get('konu', ''))}<br>{_e(b.get('mesaj', ''))}</div><div class="fa-bildirim-meta">📅 {_e(b.get('tarih', '?'))}</div></div>''', unsafe_allow_html=True)
            if b.get("cevap"):
                st.markdown(f'<div class="fa-card fa-pos"><div class="fa-ttl">💬 Admin Cevabı</div><div class="fa-mut">{_e(b["cevap"])}</div></div>', unsafe_allow_html=True)
            st.divider()


# ==========================================
# SAYFA: GELECEK MAÇLAR (ADMİN)
# ==========================================
elif st.session_state.sayfa == "gelecek_admin":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    gel = st.session_state.gelecek_analizler
    toplam_g = len(gel)

    st.markdown("### 💾 Yedekleme")
    c1, c2 = st.columns(2)
    with c1:
        json_str2 = json.dumps(st.session_state.gelecek_analizler, ensure_ascii=False, indent=2)
        st.download_button(
            label=f"📥 Geleceği İndir ({toplam_g} maç)",
            data=json_str2,
            file_name=f"gelecek_{toplam_g}mac.json",
            mime="application/json",
            use_container_width=True,
            key="ind_gelecek"
        )
    with c2:
        yuk2 = st.file_uploader("📤 Geleceği Yükle (JSON)", type=["json"], key="yuk_gelecek")
        if yuk2 is not None:
            try:
                veri2 = json.loads(yuk2.read().decode("utf-8"))
                if isinstance(veri2, list):
                    st.session_state.gelecek_analizler = veri2
                    gelecek_kaydet(veri2)
                    st.success(f"✅ {len(veri2)} maç yüklendi!")
                    st.rerun()
                else:
                    st.error("❌ Dosya formatı hatalı.")
            except Exception as e:
                st.error(f"❌ Hata: {e}")
    st.divider()

    if not gel:
        st.info("ℹ️ Gelecek maç yok. Admin ana sayfadan maç çekebilirsin.")
    else:
        sirali = sorted(enumerate(gel), key=lambda x: saat_sirala_anahtari(x[1]))
        for idx, g in sirali:
            v = g["veri"]; te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
            ulke = v.get("ulke", ""); saat = v.get("saat", ""); tarih = v.get("tarih", "")
            try: a = analiz_hesapla(v); le = a["lam_ev"]; ld = a["lam_dep"]
            except Exception: le = ld = 0
            st.markdown(mac_karti(te, td, False, 0, 0, le, ld, saat, ulke, tarih), unsafe_allow_html=True)
            th = mac_tahmin_karti(v, g)
            if th: st.markdown(th, unsafe_allow_html=True)
            c1, c2 = st.columns([5, 1])
            with c1:
                if st.button("🔍 Detay", use_container_width=True, key=f"gmac_{idx}"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True; st.session_state.gelecekten_gelindi = True
                    st.session_state.aktif_gelecek_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
            with c2:
                if st.button("🗑️", key=f"gsil_{idx}"):
                    if st.session_state.tek_silme_gelecek == idx: st.session_state.tek_silme_gelecek = None
                    else: st.session_state.tek_silme_gelecek = idx
                    st.rerun()
            if st.session_state.tek_silme_gelecek == idx:
                st.warning(f"⚠️ **{te} vs {td}** silinsin mi?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Sil", key=f"ge_{idx}", use_container_width=True, type="primary"):
                        st.session_state.gelecek_analizler.pop(idx)
                        gelecek_kaydet(st.session_state.gelecek_analizler)
                        st.session_state.tek_silme_gelecek = None; st.rerun()
                with c2:
                    if st.button("❌ İptal", key=f"gh_{idx}", use_container_width=True):
                        st.session_state.tek_silme_gelecek = None; st.rerun()
            st.divider()

    st.divider()
    if st.button("🗑️ Tüm Geleceği Temizle", use_container_width=True, key="temizle_gel"):
        st.session_state.silme_onay_gelecek = True; st.rerun()
    if st.session_state.get("silme_onay_gelecek"):
        st.warning("⚠️ Tüm gelecek silinecek. Emin misin?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Evet, Sil", key="sil_gel_evet", use_container_width=True, type="primary"):
                st.session_state.gelecek_analizler = []
                try:
                    if os.path.exists(GELECEK_DOSYA): os.remove(GELECEK_DOSYA)
                except Exception: pass
                st.session_state.silme_onay_gelecek = False
                st.session_state.tek_silme_gelecek = None
                st.rerun()
        with c2:
            if st.button("❌ İptal", key="sil_gel_iptal", use_container_width=True):
                st.session_state.silme_onay_gelecek = False; st.rerun()

    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gg_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: GEÇMİŞ MAÇLAR
# ==========================================
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gc = st.session_state.gecmis_analizler; top = len(gc)

    if admin_mi():
        st.markdown("### 💾 Yedekleme")
        c1, c2 = st.columns(2)
        with c1:
            json_str = json.dumps(st.session_state.gecmis_analizler, ensure_ascii=False, indent=2)
            st.download_button(
                label=f"📥 Geçmişi İndir ({top} maç)",
                data=json_str,
                file_name=f"gecmis_{top}mac.json",
                mime="application/json",
                use_container_width=True,
                key="ind_gecmis"
            )
        with c2:
            yuk = st.file_uploader("📤 Geçmişi Yükle (JSON)", type=["json"], key="yuk_gecmis")
            if yuk is not None:
                try:
                    veri = json.loads(yuk.read().decode("utf-8"))
                    if isinstance(veri, list):
                        st.session_state.gecmis_analizler = veri
                        gecmis_kaydet(veri)
                        st.success(f"✅ {len(veri)} maç yüklendi!")
                        st.rerun()
                    else:
                        st.error("❌ Dosya formatı hatalı (liste bekleniyor).")
                except Exception as e:
                    st.error(f"❌ Hata: {e}")
        st.divider()

    if top == 0:
        st.info("Henüz kayıt yok.")
    else:
        modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ")
        st.divider()
        st.markdown(f"### 📋 Toplam: {top} maç")
        for i, g in enumerate(reversed(gc)):
            idx = len(gc) - 1 - i; v = g["veri"]
            te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
            se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
            st.markdown(mac_karti(te, td, True, se, sd, 0, 0, v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
            th = mac_tahmin_karti(v, g)
            if th: st.markdown(th, unsafe_allow_html=True)
            if admin_mi():
                c1, c2 = st.columns([5, 1])
                with c1:
                    if st.button("🔍 Detay", use_container_width=True, key=f"mac_{idx}"):
                        st.session_state.form_verileri = copy.deepcopy(v)
                        st.session_state.kayit_yapildi = True; st.session_state.gecmisten_gelindi = True
                        st.session_state.aktif_kayit_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
                with c2:
                    if st.button("🗑️", key=f"sil_{idx}"):
                        if st.session_state.tek_silme_onay == idx: st.session_state.tek_silme_onay = None
                        else: st.session_state.tek_silme_onay = idx
                        st.rerun()
                if st.session_state.tek_silme_onay == idx:
                    st.warning(f"⚠️ **{te} vs {td}** silinsin mi?")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅ Sil", key=f"ev_{idx}", use_container_width=True, type="primary"):
                            st.session_state.gecmis_analizler.pop(idx)
                            gecmis_kaydet(st.session_state.gecmis_analizler)
                            st.session_state.tek_silme_onay = None; st.rerun()
                    with c2:
                        if st.button("❌ İptal", key=f"hh_{idx}", use_container_width=True):
                            st.session_state.tek_silme_onay = None; st.rerun()
            else:
                if st.button("🔍 Detay", use_container_width=True, key=f"mac_{idx}"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True; st.session_state.gecmisten_gelindi = True
                    st.session_state.aktif_kayit_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
            st.divider()

    if admin_mi():
        st.divider()
        if st.button("🗑️ Tüm Geçmişi Temizle", use_container_width=True, key="temizle_g"):
            st.session_state.silme_onay = True; st.rerun()
        if st.session_state.silme_onay:
            st.warning("⚠️ Tüm geçmiş silinecek. Emin misin?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Evet, Sil", key="sil_g_evet", use_container_width=True, type="primary"):
                    st.session_state.gecmis_analizler = []
                    try:
                        if os.path.exists(GECMIS_DOSYA): os.remove(GECMIS_DOSYA)
                    except Exception: pass
                    st.session_state.silme_onay = False
                    st.session_state.tek_silme_onay = None
                    st.rerun()
            with c2:
                if st.button("❌ İptal", key="sil_g_iptal", use_container_width=True):
                    st.session_state.silme_onay = False; st.rerun()

    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gc_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: BACKTEST
# ==========================================
elif st.session_state.sayfa == "backtest":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>🔬 Backtest</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        s1x2 = st.checkbox("1X2", key="bt_1x2")
        e1 = st.slider("1 eşiği", 0, 100, 55, key="sl_bt_1")
        ex = st.slider("X eşiği", 0, 100, 55, key="sl_bt_x")
        e2 = st.slider("2 eşiği", 0, 100, 55, key="sl_bt_2")
    with c2:
        skv = st.checkbox("KG Var", key="bt_kg_var"); ekv = st.slider("KG Var eşiği", 0, 100, 70, key="sl_kg_var")
        sky = st.checkbox("KG Yok", key="bt_kg_yok"); eky = st.slider("KG Yok eşiği", 0, 100, 70, key="sl_kg_yok")
    with c3:
        su = st.checkbox("Üst 2.5", key="bt_ust"); eu = st.slider("Üst eşiği", 0, 100, 70, key="sl_ust")
        sa = st.checkbox("Alt 2.5", key="bt_alt"); ea = st.slider("Alt eşiği", 0, 100, 70, key="sl_alt")
    if st.button("🚀 TEST", use_container_width=True, type="primary"):
        with st.spinner("Test..."):
            sec = {"1x2": s1x2, "kg_var": skv, "kg_yok": sky, "ust": su, "alt": sa}
            esk = {"esik_1": float(e1), "esik_x": float(ex), "esik_2": float(e2), "kg_var": float(ekv), "kg_yok": float(eky), "ust": float(eu), "alt": float(ea)}
            if not any(sec.values()): st.warning("Market seç.")
            else:
                s, d = backtest_hesapla(st.session_state.gecmis_analizler, sec, esk)
                st.session_state.bt_sonuc = s; st.session_state.bt_detaylar = d; st.session_state.bt_sec = sec
    if st.session_state.bt_sonuc and st.session_state.get("bt_sec"):
        for key, b in [("1x2", "1X2"), ("kg_var", "KG Var"), ("kg_yok", "KG Yok"), ("ust", "Üst"), ("alt", "Alt")]:
            if st.session_state.bt_sec.get(key):
                dd = st.session_state.bt_sonuc[key]; tt = dd["dogru"] + dd["yanlis"]
                if tt > 0: st.markdown(f"**{b}:** %{dd['dogru']/tt*100:.1f} ({dd['dogru']}/{tt})")
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="btg"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: AYARLAR
# ==========================================
elif st.session_state.sayfa == "ayarlar":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>⚙️ Ayarlar</h1>", unsafe_allow_html=True)
    mv = st.session_state.esikler.copy()
    st.markdown("### 🏦 Ödeme")
    c1, c2 = st.columns(2)
    with c1: yiban = st.text_input("IBAN", value=mv.get("iban", "TR00 0000 0000 0000 0000 0000 00"))
    with c2: yhs = st.text_input("Hesap Sahibi", value=mv.get("hesap_sahibi", ""))
    st.markdown("### 💰 Fiyatlar")
    c1, c2, c3 = st.columns(3)
    with c1: yfh = st.number_input("Haftalık", min_value=1.0, value=float(mv.get("fiyat_haftalik", 49.0)), step=10.0, key="ay_fh")
    with c2: yfa = st.number_input("Aylık", min_value=1.0, value=float(mv.get("fiyat_aylik", 149.0)), step=10.0, key="ay_fa")
    with c3: yfy = st.number_input("Yıllık", min_value=1.0, value=float(mv.get("fiyat_yillik", 999.0)), step=10.0, key="ay_fy")
    if yfa > 0 and yfy < yfa * 12:
        st.caption(f"💡 Yıllıkta %{int((1 - yfy / (yfa * 12)) * 100)} indirim")
    st.markdown("### 🔓 Ücretsiz Kota")
    yk = st.number_input("Kaç maç ücretsiz?", 0, 50, int(mv.get("ucretsiz_kotasi", 3)), 1, key="ay_kota")
    st.markdown("### 🎯 Eşikler")
    c1, c2, c3 = st.columns(3)
    with c1: ye1 = st.slider("1 %", 0, 100, int(mv.get("esik_1", 55.0)), 1, key="ay_esik_1")
    with c2: yex = st.slider("X %", 0, 100, int(mv.get("esik_x", 55.0)), 1, key="ay_esik_x")
    with c3: ye2 = st.slider("2 %", 0, 100, int(mv.get("esik_2", 55.0)), 1, key="ay_esik_2")
    c4, c5 = st.columns(2)
    with c4: yu = st.slider("Üst %", 0, 100, int(mv["ust"]), 1, key="ay_ust")
    with c5: ya = st.slider("Alt %", 0, 100, int(mv["alt"]), 1, key="ay_alt")
    c6, c7 = st.columns(2)
    with c6: ykv = st.slider("KG Var %", 0, 100, int(mv["kg_var"]), 1, key="ay_kg_var")
    with c7: yky = st.slider("KG Yok %", 0, 100, int(mv["kg_yok"]), 1, key="ay_kg_yok")
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💾 Kaydet", use_container_width=True, type="primary"):
            y = dict(mv); y.update({"iban": yiban, "hesap_sahibi": yhs, "fiyat_haftalik": float(yfh), "fiyat_aylik": float(yfa), "fiyat_yillik": float(yfy), "ucretsiz_kotasi": int(yk), "esik_1": float(ye1), "esik_x": float(yex), "esik_2": float(ye2), "ust": float(yu), "alt": float(ya), "kg_var": float(ykv), "kg_yok": float(yky)})
            st.session_state.esikler = y; ayarlar_kaydet(y); st.success("✅ Kaydedildi!")
    with c2:
        if st.button("🔄 Sıfırla", use_container_width=True):
            v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "iban": "TR00 0000 0000 0000 0000 0000 00", "hesap_sahibi": "ADINIZ SOYADINIZ", "fiyat_haftalik": 49.0, "fiyat_aylik": 149.0, "fiyat_yillik": 999.0, "ucretsiz_kotasi": 3}
            st.session_state.esikler = v; ayarlar_kaydet(v); st.rerun()
    with c3:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="ayg"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: MANUEL GİRİŞ
# ==========================================
elif st.session_state.sayfa == "manuel_giris":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>📝 Eksik Alanlar</h1>", unsafe_allow_html=True)
    st.warning(f"Metinden çıkarılamayan **{len(st.session_state.manuel_bekleyen)}** alan:")
    v = st.session_state.form_verileri
    with st.form("mf"):
        yd = {}
        for a in st.session_state.manuel_bekleyen:
            if a in MANUEL_ALANLAR:
                st.markdown(f"**{a}**")
                for (k, e, t, vs) in MANUEL_ALANLAR[a]:
                    mv = v.get(k, vs)
                    if t == "int":
                        val = st.number_input(e, value=int(mv) if mv else int(vs), min_value=1, max_value=100, step=1, key=f"mk_{k}")
                        yd[k] = int(val)
                    elif t == "float":
                        val = st.number_input(e, value=float(mv) if mv else float(vs), min_value=0.0, step=0.1, key=f"mk_{k}")
                        yd[k] = float(val)
                    else:
                        val = st.text_input(e, value=str(mv) if mv else "", key=f"mk_{k}")
                        yd[k] = val
        c1, c2 = st.columns(2)
        with c1: kb = st.form_submit_button("✅ Kaydet", use_container_width=True, type="primary")
        with c2: ab = st.form_submit_button("⏭️ Atla", use_container_width=True)
        if kb or ab:
            if kb: st.session_state.form_verileri.update(yd)
            st.session_state.manuel_bekleyen = []
            st.session_state.sayfa = "sonuc"; st.rerun()
    if st.button("⬅️ Geri"): st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: SONUÇ
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri; a = analiz_hesapla(v)
    te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
    sb = v.get("skor_belli", False); se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    st.markdown(mac_karti(te, td, sb, se, sd, a["lam_ev"], a["lam_dep"], v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)

    # === AI YORUMU (Okunan Veriler yerine) ===
    ai_html = ai_yorum_paneli(v, a)
    if ai_html:
        st.markdown(ai_html, unsafe_allow_html=True)

    st.divider()
    st.markdown("## 🏆 FİNAL ÖNERİ")
    s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    e1 = esik_1x2_al(s1); p1 = y1 >= e1
    im = {"1": "1 (Ev)", "X": "X (Beraberlik)", "2": "2 (Dep)"}
    st.markdown(oneri_karti("🎯 1X2", im[s1], y1, e1, p1, f"1:%{a['p1']:.1f} X:%{a['px']:.1f} 2:%{a['p2']:.1f}"), unsafe_allow_html=True)
    if a["ust_25"] >= a["alt_25"]: gs = "Üst 2.5"; gy = a["ust_25"]; ge_ = esik_al("ust")
    else: gs = "Alt 2.5"; gy = a["alt_25"]; ge_ = esik_al("alt")
    st.markdown(oneri_karti("⚽ Gol", gs, gy, ge_, gy >= ge_, f"Üst:%{a['ust_25']:.1f} Alt:%{a['alt_25']:.1f}"), unsafe_allow_html=True)
    if a["kg_var_model"] >= a["kg_yok_model"]: ks = "KG Var"; ky = a["kg_var_model"]; ke = esik_al("kg_var")
    else: ks = "KG Yok"; ky = a["kg_yok_model"]; ke = esik_al("kg_yok")
    st.markdown(oneri_karti("🤝 KG", ks, ky, ke, ky >= ke, f"Var:%{a['kg_var_model']:.1f} Yok:%{a['kg_yok_model']:.1f}"), unsafe_allow_html=True)

    if st.session_state.gelecekten_gelindi and admin_mi():
        ig = st.session_state.aktif_gelecek_idx
        if ig is not None and 0 <= ig < len(st.session_state.gelecek_analizler):
            st.divider(); st.markdown("### 📥 Sonuç Gir")
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1: yse = st.number_input("Ev", 0, 20, 0, 1, key=f"gse_{ig}")
            with c2: ysd = st.number_input("Dep", 0, 20, 0, 1, key=f"gsd_{ig}")
            with c3:
                st.markdown(""); st.markdown("")
                if st.button("📥 Taşı", key=f"ts_{ig}", use_container_width=True, type="primary"):
                    k = st.session_state.gelecek_analizler[ig]
                    k["veri"]["skor_ev"] = int(yse); k["veri"]["skor_dep"] = int(ysd); k["veri"]["skor_belli"] = True
                    yd = sonuc_hesapla(k)
                    if yd: k["dogruluk"] = yd
                    st.session_state.gecmis_analizler.append(k)
                    st.session_state.gelecek_analizler.pop(ig)
                    gecmis_kaydet(st.session_state.gecmis_analizler); gelecek_kaydet(st.session_state.gelecek_analizler)
                    st.session_state.gelecekten_gelindi = False; st.session_state.aktif_gelecek_idx = None
                    st.session_state.sayfa = "giris"; st.rerun()

    km = (a["ust_25"] >= esik_al("ust") and a["ust_25"] >= a["alt_25"]) or (a["alt_25"] >= esik_al("alt") and a["alt_25"] >= a["ust_25"]) or p1
    if not st.session_state.kayit_yapildi and admin_mi():
        yk = kayit_olustur(v, a)
        if sb: st.session_state.gecmis_analizler.append(yk); gecmis_kaydet(st.session_state.gecmis_analizler)
        elif km: st.session_state.gelecek_analizler.append(yk); gelecek_kaydet(st.session_state.gelecek_analizler)
        st.session_state.kayit_yapildi = True
    if st.button("🔄 Yeni", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI); st.session_state.sayfa = "giris"; st.rerun()
# ==========================================
# VERİ ÇEKME MOTORU
# ==========================================
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def _son_n_oku(m):
    x = re.search(r'Last\s+(\d+)\s+games', m or "")
    return int(x.group(1)) if x else None


def _tikla_mac_sayisi(pg, ms):
    h = str(ms)
    try:
        for el in pg.locator(f'xpath=//*[normalize-space(text())="{h}"]').all()[:20]:
            try:
                if el.evaluate("e => !!e.closest('table')"): continue
                if el.evaluate("e => e.children.length > 1"): continue
                el.click(timeout=1500); return True
            except Exception: continue
    except Exception: pass
    js = '''(function(h){var t=document.querySelectorAll('label,span,div,button,a,li');for(var i=0;i<t.length;i++){var e=t[i];if(e.children.length>1)continue;if(e.closest('table'))continue;if((e.textContent||'').trim()===h){try{e.click()}catch(x){};var p=e.querySelector('input[type=radio],input[type=checkbox]');if(p&&!p.checked){try{p.click()}catch(x){}};return true}}return false})("%s")''' % h
    try: return bool(pg.evaluate(js))
    except Exception: return False


def _tikla_takim_sekmesi(pg, tadi, sekme):
    if not tadi: return False
    js = r'''(function(ta,sa){var t=document.querySelectorAll('h1,h2,h3,h4,h5,strong,b,span,div,a,p');var el=null;for(var i=0;i<t.length;i++){var e=t[i];if(e.children.length>1)continue;var x=(e.textContent||'').trim();if(x===ta){el=e;break}}if(!el){for(var i=0;i<t.length;i++){var e=t[i];if(e.children.length>1)continue;var x=(e.textContent||'').trim();if(x.indexOf(ta)===0&&x.length<ta.length+5){el=e;break}}}if(!el)return false;var cur=el;for(var k=0;k<12&&cur.parentElement;k++){cur=cur.parentElement;var sm=cur.querySelectorAll('label,span,div,a,button,li');for(var j=0;j<sm.length;j++){var s=sm[j];if(s.children.length>1)continue;if(s.closest('table'))continue;if((s.textContent||'').trim()===sa){try{s.click()}catch(x){};var p=s.querySelector('input[type=radio],input[type=checkbox]');if(p&&!p.checked){try{p.click()}catch(x){}};return true}}}return false})("%s","%s")''' % (tadi.replace('"', '\\"'), sekme)
    try: return bool(pg.evaluate(js))
    except Exception: return False


def _playwright_html(url, ms, timeout, dogrula=False, tev="", tdep=""):
    from playwright.sync_api import sync_playwright
    hedef = int(ms) if str(ms).isdigit() else None
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        try:
            ctx = b.new_context(user_agent=UA, locale="en-US")
            pg = ctx.new_page()
            pg.route("**/*", lambda r: r.abort() if r.request.resource_type in ("image", "media", "font") else r.continue_())
            pg.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
            try: pg.wait_for_load_state("networkidle", timeout=15000)
            except Exception: pass
            pg.wait_for_timeout(2500)
            _tikla_mac_sayisi(pg, ms); pg.wait_for_timeout(3500)
            if tev: _tikla_takim_sekmesi(pg, tev, "Home"); pg.wait_for_timeout(3500)
            if tdep: _tikla_takim_sekmesi(pg, tdep, "Away"); pg.wait_for_timeout(3500)
            if dogrula and hedef:
                try: m = pg.inner_text("body")
                except Exception: m = ""
                n = _son_n_oku(m)
                if n is not None and n != hedef:
                    _tikla_mac_sayisi(pg, ms); pg.wait_for_timeout(3000)
                    try: m = pg.inner_text("body")
                    except Exception: m = ""
                    n = _son_n_oku(m)
                    if n is not None and n != hedef: raise RuntimeError(f"{hedef} filtresi uygulanamadı")
            return pg.content()
        finally:
            try: b.close()
            except Exception: pass


def _scrapingbee_get(url, render_js=True, timeout=90, ms="5", max_retry=3, dogrula=False, tev="", tdep=""):
    hata = None
    try:
        import playwright
        pv = True
    except ImportError:
        pv = False; hata = "playwright yok"
    if pv:
        for d in range(max_retry):
            try:
                h = _playwright_html(url, ms, timeout, dogrula, tev, tdep)
                if h and len(h) > 500: return h, None
                hata = "Boş sayfa"
            except Exception as e:
                hata = f"Tarayıcı: {str(e)[:150]}"
            if d < max_retry - 1: time.sleep(2 + d * 2)
    if dogrula: return None, hata or "Filtre uygulanamadı"
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=30)
        if r.status_code == 200 and r.text: return r.text, None
        hata = f"HTTP {r.status_code}"
    except Exception as e: hata = f"Bağlantı: {str(e)[:100]}"
    return None, hata or "Sayfa alınamadı"


def _html_metne_cevir(html):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "noscript", "svg", "iframe"]): t.decompose()
    for td in soup.find_all(["td", "th"]): td.insert_after("\t")
    for tr in soup.find_all("tr"): tr.insert_after("\n")
    for e in soup.find_all(["div", "p", "li", "h1", "h2", "h3", "h4", "br"]): e.insert_after("\n")
    m = soup.get_text(separator="", strip=False)
    m = re.sub(r'[ \t]+\n', '\n', m); m = re.sub(r'\n{3,}', '\n\n', m)
    return m


def mutating_ana_sayfa_linklerini_al(max_mac=MAX_MAC_SINIRI):
    html, hata = _scrapingbee_get("https://www.mutating.com/football-stats/", render_js=True)
    if hata: return [], [hata]
    if not html: return [], ["Ana sayfa indirilemedi"]
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gor = set()
    for link in soup.find_all("a", href=True):
        if len(maclar) >= max_mac: break
        href = link.get("href", "")
        if not any(x in href for x in ["match-preview", "match/", "/stats/"]): continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gor: continue
        gor.add(href)
        h2 = link.find_all("h2")
        tev = h2[0].get_text(strip=True) if len(h2) > 0 else ""
        tdep = h2[1].get_text(strip=True) if len(h2) > 1 else ""
        s_el = link.find(class_=re.compile(r"nostart|time|match-time"))
        saat = s_el.get_text(strip=True) if s_el else ""
        if saat: saat = saat_2_saat_ileri(saat)
        maclar.append({"url": href, "takim_ev": tev, "takim_dep": tdep, "saat": saat})
    return maclar, []


def _mac_html_parse(html, url=""):
    soup = BeautifulSoup(html, "html.parser")
    veri = {}
    h1 = soup.find("h1")
    if h1:
        b = h1.get_text(strip=True)
        if " - " in b:
            p = b.replace(" Stats", "").replace(" stats", "").split(" - ")
            veri["takim_ev"] = p[0].strip()
            if len(p) > 1: veri["takim_dep"] = p[1].strip()
    m = _html_metne_cevir(html)
    m1 = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', m)
    if m1: veri["tarih"] = m1.group(1)
    m1 = re.search(r'(\d{1,2}:\d{2})', m)
    if m1: veri["saat"] = saat_2_saat_ileri(m1.group(1))
    veri["ulke"] = _ulke_bul(m)
    sk_e = sk_d = None
    m1 = re.search(r'FT\s*\n+\s*(\d{1,2})\s*[-:]\s*(\d{1,2})', m)
    if m1: sk_e = int(m1.group(1)); sk_d = int(m1.group(2))
    if sk_e is not None:
        veri["skor_ev"] = sk_e; veri["skor_dep"] = sk_d; veri["skor_belli"] = True
    else: veri["skor_belli"] = False

    def cf(label):
        for pat in [r'([\d.,]+)\s*%?\s*\t\s*' + re.escape(label) + r'\s*\t\s*([\d.,]+)', r'([\d.,]+)\s*%?\s*\|\s*' + re.escape(label) + r'\s*\|\s*([\d.,]+)', r'([\d.,]+)\s*%?\s+' + re.escape(label) + r'\s+([\d.,]+)\s*%?', r'([\d.,]+)\s*%?\s*\n\s*' + re.escape(label) + r'\s*\n\s*([\d.,]+)']:
            x = re.search(pat, m, re.IGNORECASE)
            if x:
                try: return float(x.group(1).replace(",", ".")), float(x.group(2).replace(",", "."))
                except ValueError: continue
        return None, None

    for lb, ke, kd in [("Goals scored per game", "atilan_ev", "atilan_dep"), ("Goals conceded per game", "yenen_ev", "yenen_dep"), ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"), ("Team scored", "team_scored_ev", "team_scored_dep"), ("Both Teams to Score", "kg_siklik_ev", "kg_siklik_dep"), ("Over 2.5 goals", "ust25_ev", "ust25_dep"), ("Over 1.5 goals", "ust15_ev", "ust15_dep"), ("Over 3.5 goals", "ust35_ev", "ust35_dep")]:
        a, b = cf(lb)
        if a is not None and veri.get(ke, 0) == 0: veri[ke] = a; veri[kd] = b
    for lb, ke, kd in [("Win", "galibiyet_ev", "galibiyet_dep"), ("Draw", "beraberlik_ev", "beraberlik_dep"), ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
        x = re.search(r'([\d.,]+)\s*%\s*\t\s*' + lb + r'\s*\t\s*([\d.,]+)\s*%', m, re.MULTILINE)
        if x:
            try: veri[ke] = float(x.group(1).replace(",", ".")); veri[kd] = float(x.group(2).replace(",", "."))
            except ValueError: pass
    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) + veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2
    veri["format"] = "mutating"
    if url: veri["kaynak_url"] = url
    return veri, []


def _mac_tahmin_var_mi(v):
    try:
        a = analiz_hesapla(v)
        s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
        if y1 >= esik_1x2_al(s1): return True
        if a["ust_25"] >= esik_al("ust") and a["ust_25"] >= a["alt_25"]: return True
        if a["alt_25"] >= esik_al("alt") and a["alt_25"] >= a["ust_25"]: return True
        if a["kg_var_model"] >= esik_al("kg_var") and a["kg_var_model"] >= a["kg_yok_model"]: return True
        if a["kg_yok_model"] >= esik_al("kg_yok") and a["kg_yok_model"] >= a["kg_var_model"]: return True
        return False
    except Exception: return False


def mutating_mac_detay_cek(url, tev="", tdep=""):
    h, hata = _scrapingbee_get(url, render_js=True, ms="5", dogrula=True, tev=tev, tdep=tdep)
    if hata: return None, [hata]
    if not h: return None, ["Sayfa indirilemedi"]
    return _mac_html_parse(h, url)


def _gelecek_mac_isle(mac, mevcut):
    try:
        veri, _ = mutating_mac_detay_cek(mac["url"], mac.get("takim_ev", ""), mac.get("takim_dep", ""))
        if not veri: return ("hata", mac, "Veri yok", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        if not veri.get("saat"): veri["saat"] = saat_2_saat_ileri(mac.get("saat", ""))
        veri["kaynak_url"] = mac["url"]
        if mac["url"] in mevcut: return ("zaten_var", veri, "Zaten var", None)
        ae = veri.get("atilan_ev", 0); ye = veri.get("yenen_ev", 0)
        ad = veri.get("atilan_dep", 0); yd = veri.get("yenen_dep", 0)
        if ae == 0 and ye == 0 and ad == 0 and yd == 0: return ("veri_yok", veri, "Boş veri", None)
        try: a = analiz_hesapla(veri)
        except Exception as e: return ("veri_yok", veri, f"Hata: {str(e)[:50]}", None)
        s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
        e1 = esik_1x2_al(s1)
        gs = "Üst" if a["ust_25"] >= a["alt_25"] else "Alt"
        gy = a["ust_25"] if gs == "Üst" else a["alt_25"]
        ge_ = esik_al("ust") if gs == "Üst" else esik_al("alt")
        ks = "Var" if a["kg_var_model"] >= a["kg_yok_model"] else "Yok"
        ky = a["kg_var_model"] if ks == "Var" else a["kg_yok_model"]
        ke = esik_al("kg_var") if ks == "Var" else esik_al("kg_yok")
        ozet = f"1X2:%{y1:.0f}(eşik {e1:.0f}) • {gs}:%{gy:.0f}(eşik {ge_:.0f}) • KG {ks}:%{ky:.0f}(eşik {ke:.0f})"
        if _mac_tahmin_var_mi(veri):
            kayit = kayit_olustur(veri, a)
            return ("eklendi", veri, f"Eklendi • {ozet}", kayit)
        return ("esik_alti", veri, f"Eşik altı • {ozet}", None)
    except Exception as e:
        return ("hata", mac, f"İstisna: {str(e)[:80]}", None)


def mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=None, max_workers=3):
    _ESIK_CACHE.clear()
    try: _ESIK_CACHE.update(dict(st.session_state.esikler))
    except Exception: pass
    maclar, hatalar = mutating_ana_sayfa_linklerini_al(max_mac=max_mac)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Maç linki yok"]
    mevcut = set()
    for g in st.session_state.gelecek_analizler:
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut.add(u)
    ek = 0; ea = 0; vy = 0; zv = 0; ht = 0; ekl = []; log = []; tam = 0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_gelecek_mac_isle, m, mevcut): m for m in maclar}
        for f in as_completed(futs):
            tam += 1; mac = futs[f]
            isim = f"{mac.get('takim_ev', '?')} - {mac.get('takim_dep', '?')}"
            try:
                r = f.result()
                if len(r) == 4: sonuc, veri, mesaj, kayit = r
                else: sonuc, veri, mesaj = r; kayit = None
                if sonuc == "eklendi":
                    ek += 1; ekl.append(veri)
                    if kayit is not None:
                        try: st.session_state.gelecek_analizler.append(kayit)
                        except Exception: pass
                    log.append(f"✅ {isim} → {mesaj}")
                elif sonuc == "esik_alti": ea += 1; log.append(f"⚠️ {isim} → {mesaj}")
                elif sonuc == "veri_yok": vy += 1; log.append(f"🚫 {isim} → {mesaj}")
                elif sonuc == "zaten_var": zv += 1; log.append(f"↩️ {isim} → Zaten var")
                else: ht += 1; log.append(f"❌ {isim} → {mesaj}")
            except Exception as e:
                ht += 1; log.append(f"❌ {isim} → {str(e)[:80]}")
            if progress_callback:
                try: progress_callback(tam - 1, len(maclar), mac.get("takim_ev", ""))
                except Exception: pass
    try: gelecek_kaydet(st.session_state.gelecek_analizler)
    except Exception: pass
    st.session_state.toplu_cek_ozet = {"bulunan": len(maclar), "eklenen": ek, "esik_alti": ea, "veri_yok": vy, "zaten_var": zv, "hata": ht, "detay_log": log[:300]}
    return ekl, []


def _lig_son_mac_linklerini_al(lig_url, adet=10):
    html, hata = _scrapingbee_get(lig_url, render_js=True, ms="10")
    if hata: return [], [hata]
    if not html: return [], ["Lig sayfası indirilemedi"]
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gor = set()
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        if "match-preview" not in href: continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gor: continue
        gor.add(href)
        takim_ev = ""; takim_dep = ""
        img = link.find_all("img", alt=True)
        if len(img) >= 2:
            takim_ev = img[0].get("alt", "").strip()
            takim_dep = img[1].get("alt", "").strip()
        if not takim_ev:
            txt = link.get_text(" ", strip=True)
            if " - " in txt:
                p = txt.split(" - ")
                takim_ev = p[0].strip(); takim_dep = p[1].strip() if len(p) > 1 else ""
        maclar.append({"url": href, "takim_ev": takim_ev, "takim_dep": takim_dep})
        if len(maclar) >= adet: break
    return maclar, []


def _gecmis_mac_isle(mac, mevcut_urls):
    try:
        if mac["url"] in mevcut_urls:
            return ("atlandi", None, "Zaten var", None)
        html, hata = _scrapingbee_get(mac["url"], render_js=True, ms="5", dogrula=True, tev=mac.get("takim_ev", ""), tdep=mac.get("takim_dep", ""))
        if hata or not html: return ("hata", mac, hata or "HTML yok", None)
        veri, _ = _mac_html_parse(html, mac["url"])
        if not veri.get("skor_belli", False): return ("atlandi", None, "Skor yok (bitmemiş)", None)
        if veri.get("atilan_ev", 0) == 0 or veri.get("yenen_ev", 0) == 0: return ("atlandi", None, "İstatistik eksik", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        yv = copy.deepcopy(VARSAYILAN_VERI); yv.update(veri)
        kayit = kayit_olustur(yv, analiz_hesapla(yv))
        kayit["dogruluk"] = sonuc_hesapla(kayit)
        return ("eklendi", veri, f"{veri['skor_ev']}-{veri['skor_dep']}", kayit)
    except Exception as e:
        return ("hata", mac, str(e)[:80], None)


def lig_gecmis_cek(lig_url, adet=10, max_workers=3, progress_callback=None):
    _ESIK_CACHE.clear()
    try: _ESIK_CACHE.update(dict(st.session_state.esikler))
    except Exception: pass
    maclar, hatalar = _lig_son_mac_linklerini_al(lig_url, adet=adet)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Lig sayfasında maç linki bulunamadı"]
    mevcut_urls = set()
    for g in st.session_state.gecmis_analizler:
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut_urls.add(u)
    bas = []; hat = []; ek = 0; at = 0; tam = 0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_gecmis_mac_isle, m, mevcut_urls): m for m in maclar}
        for f in as_completed(futs):
            tam += 1; mac = futs[f]
            try:
                r = f.result()
                sonuc, veri, mesaj, kayit = r if len(r) == 4 else (r[0], r[1], r[2], None)
                if sonuc == "eklendi":
                    ek += 1; bas.append(veri)
                    if kayit is not None:
                        try: st.session_state.gecmis_analizler.append(kayit)
                        except Exception: pass
                elif sonuc == "atlandi": at += 1
                else: hat.append(f"{mac.get('takim_ev','?')}: {mesaj}")
            except Exception as e:
                hat.append(f"{mac.get('takim_ev','?')}: {e}")
            if progress_callback:
                try: progress_callback(tam - 1, len(maclar), mac.get("takim_ev", ""))
                except Exception: pass
    try: gecmis_kaydet(st.session_state.gecmis_analizler)
    except Exception: pass
    return bas, hat


# ==========================================
# SKOR ÇEKME
# ==========================================
def _skor_parse(html):
    m = _html_metne_cevir(html)
    x = re.search(r'(?<![A-Za-z])FT\s*\n+\s*(\d{1,2})\s*[-:]\s*(\d{1,2})', m)
    if x: return int(x.group(1)), int(x.group(2))
    return None


def _skor_cek(url, yedek=False):
    h = None; hata = None
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=30)
        if r.status_code == 200 and r.text: h = r.text
        else: hata = f"HTTP {r.status_code}"
    except Exception as e: hata = f"Bağlantı: {str(e)[:80]}"
    skor = _skor_parse(h) if h else None
    if skor is None and yedek:
        h2, _ = _scrapingbee_get(url, render_js=True, ms="5")
        if h2: skor = _skor_parse(h2); hata = None
    if skor is None and h: hata = None
    return skor, hata


def sonuclari_isle(tarayici_yedek=False, max_workers=3, progress_callback=None):
    gel = st.session_state.gelecek_analizler
    isler = [(i, g) for i, g in enumerate(gel) if g.get("veri", {}).get("kaynak_url")]
    sonuc = {}; tam = 0
    if isler:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futs = {ex.submit(_skor_cek, g["veri"]["kaynak_url"], tarayici_yedek): (i, g) for i, g in isler}
            for f in as_completed(futs):
                i, g = futs[f]; tam += 1
                try: sonuc[i] = f.result()
                except Exception as e: sonuc[i] = (None, str(e)[:80])
                if progress_callback:
                    try: progress_callback(tam - 1, len(isler), g["veri"].get("takim_ev", ""))
                    except Exception: pass
    mevcut = {x.get("veri", {}).get("kaynak_url") for x in st.session_state.gecmis_analizler}
    tas = 0; bm = 0; ht = []; kalan = []
    for i, g in enumerate(gel):
        r = sonuc.get(i)
        if r is None: kalan.append(g); continue
        skor, hata = r
        v = g["veri"]; isim = f"{v.get('takim_ev', '?')} - {v.get('takim_dep', '?')}"
        if hata: ht.append(f"{isim}: {hata}"); kalan.append(g); continue
        if skor is None: bm += 1; kalan.append(g); continue
        v["skor_ev"] = skor[0]; v["skor_dep"] = skor[1]; v["skor_belli"] = True
        d = sonuc_hesapla(g)
        if d: g["dogruluk"] = d
        if v.get("kaynak_url") not in mevcut:
            st.session_state.gecmis_analizler.append(g)
            mevcut.add(v.get("kaynak_url"))
        tas += 1
    st.session_state.gelecek_analizler = kalan
    gecmis_kaydet(st.session_state.gecmis_analizler)
    gelecek_kaydet(st.session_state.gelecek_analizler)
    return {"tasinan": tas, "bitmemis": bm, "hatalar": ht, "toplam": len(isler)}


# ==========================================
# TASARIM YARDIMCILARI
# ==========================================
def _e(x): return _html.escape(str(x))
def rozet(m, t="gray"): return f'<span class="fa-badge fa-b-{t}">{_e(m)}</span>'


def _donut_svg(yuzde, renk, boyut=82):
    y = max(0.0, min(100.0, yuzde))
    r = 38
    cevre = 2 * 3.14159265 * r
    offset = cevre * (1 - y / 100)
    return f'''<svg class="fa-donut-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
<circle cx="50" cy="50" r="{r}" fill="none" stroke="#1a2438" stroke-width="8"/>
<circle cx="50" cy="50" r="{r}" fill="none" stroke="{renk}" stroke-width="8"
    stroke-dasharray="{cevre:.2f}" stroke-dashoffset="{offset:.2f}"
    stroke-linecap="round" transform="rotate(-90 50 50)"/>
<text x="50" y="50" text-anchor="middle" dominant-baseline="central"
    fill="{renk}" font-size="22" font-weight="900" font-family="Rajdhani, Inter, sans-serif">%{y:.0f}</text>
</svg>'''


def mac_karti(ev, dep, sb, se, sd, le, ld, saat="", ulke="", tarih=""):
    orta = f'<div class="fa-score">{int(se)} - {int(sd)}</div>' if sb else '<div class="fa-vs">VS</div>'
    br = ulke_bayrak_bul(ulke); ust = ""
    if saat or ulke or tarih:
        p = []
        if br != "🌍" or ulke: p.append(f"{br} {_e((ulke or '').title())}")
        if tarih: p.append(f"📅 {_e(tarih)}")
        if saat: p.append(f"🕐 {_e(saat)}")
        if p: ust = f'<div class="fa-sub" style="margin-bottom:6px;">{" • ".join(p)}</div>'
    alt = f'<div class="fa-sub">Model beklenen gol: {le:.2f} - {ld:.2f}</div>'
    return f'<div class="fa-hero">{ust}<div class="fa-teams"><div class="fa-team">{_e(ev)}</div>{orta}<div class="fa-team">{_e(dep)}</div></div>{alt}</div>'


def kilitli_mac_karti(ev, dep, saat="", ulke="", tarih=""):
    br = ulke_bayrak_bul(ulke); ust = ""
    if saat or ulke or tarih:
        p = []
        if br != "🌍" or ulke: p.append(f"{br} {_e((ulke or '').title())}")
        if tarih: p.append(f"📅 {_e(tarih)}")
        if saat: p.append(f"🕐 {_e(saat)}")
        if p: ust = f'<div class="fa-sub" style="margin-bottom:6px;">{" • ".join(p)}</div>'
    return f'<div class="fa-locked">{ust}<div class="fa-locked-teams"><div class="fa-team">{_e(ev)}</div><div class="fa-vs">VS</div><div class="fa-team">{_e(dep)}</div></div><div class="fa-locked-overlay"><div class="fa-locked-text">🔒 PREMIUM\'A GEÇ</div></div></div>'


def mac_tahmin_karti(v_g, g=None):
    try:
        try: ya = yeniden_analiz(v_g)
        except Exception: ya = (g or {}).get("analiz", {})
        p1 = ya.get("p1", 33.33); px = ya.get("px", 33.33); p2 = ya.get("p2", 33.34)
        u25 = ya.get("ust_25", 50); a25 = 100 - u25
        kgv = ya.get("kg_var_model", 50); kgy = 100 - kgv
        e1 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        s1, y1 = e1; es1 = esik_1x2_al(s1); poz1 = y1 >= es1
        isim1 = {"1": "1 — Ev Kazanır", "X": "X — Beraberlik", "2": "2 — Dep Kazanır"}[s1]
        if u25 >= a25: gs = "Üst 2.5"; gy = u25; ge_ = esik_al("ust")
        else: gs = "Alt 2.5"; gy = a25; ge_ = esik_al("alt")
        gp = gy >= ge_
        if kgv >= kgy: ks = "KG Var"; ky = kgv; ke = esik_al("kg_var")
        else: ks = "KG Yok"; ky = kgy; ke = esik_al("kg_yok")
        kp = ky >= ke
        def r(p): return "pass" if p else "off"
        def b(p): return "ok" if p else "no"
        def bt(p): return "✅" if p else "⚪"
        return f'''<div class="fa-mk"><div class="fa-mk-row"><span class="fa-mk-lbl">🎯 1X2</span><span class="fa-mk-pick {r(poz1)}">{_e(isim1)}</span><span class="fa-mk-pct">%{y1:.0f} <span class="fa-mk-badge {b(poz1)}">{bt(poz1)} eşik %{es1:.0f}</span></span></div><div class="fa-mk-row"><span class="fa-mk-lbl">⚽ Gol</span><span class="fa-mk-pick {r(gp)}">{_e(gs)}</span><span class="fa-mk-pct">%{gy:.0f} <span class="fa-mk-badge {b(gp)}">{bt(gp)} eşik %{ge_:.0f}</span></span></div><div class="fa-mk-row"><span class="fa-mk-lbl">🤝 KG</span><span class="fa-mk-pick {r(kp)}">{_e(ks)}</span><span class="fa-mk-pct">%{ky:.0f} <span class="fa-mk-badge {b(kp)}">{bt(kp)} eşik %{ke:.0f}</span></span></div></div>'''
    except Exception: return ""


def olasilik_bar(e, y, esik=None, renk="#3b82f6"):
    y = max(0.0, min(100.0, y)); isr = ""
    if esik is not None:
        renk = "#22c55e" if y >= esik else "#475569"
        isr = f'<div class="fa-tick" style="left:{esik:.0f}%"></div>'
    return f'<div class="fa-row"><div class="fa-row-top"><span class="fa-lbl">{_e(e)}</span><span class="fa-val">%{y:.1f}</span></div><div class="fa-bar"><div class="fa-fill" style="width:{y:.1f}%;background:{renk}"></div>{isr}</div></div>'


def olasilik_paneli(a):
    s = ('<div class="fa-ttl">Maç Sonucu</div>'
        + olasilik_bar("Ev (1)", a["p1"], esik_1x2_al("1"), "#3b82f6")
        + olasilik_bar("Beraberlik (X)", a["px"], esik_1x2_al("X"), "#94a3b8")
        + olasilik_bar("Dep (2)", a["p2"], esik_1x2_al("2"), "#f59e0b")
        + '<div class="fa-ttl" style="margin-top:10px">Piyasalar</div>'
        + olasilik_bar("Üst 2.5", a["ust_25"], esik_al("ust"))
        + olasilik_bar("Alt 2.5", a["alt_25"], esik_al("alt"))
        + olasilik_bar("KG Var", a["kg_var_model"], esik_al("kg_var"))
        + olasilik_bar("KG Yok", a["kg_yok_model"], esik_al("kg_yok")))
    return f'<div class="fa-card">{s}</div>'


def oneri_karti(b, s, y, e, poz, alt):
    if poz:
        sv, _, _, et = guven_seviyesi_bul(y)
        t = "green" if sv == "yuksek" else "yellow" if sv == "orta" else "gray"
        d = rozet(f"{et} güven", t); sn = "fa-card fa-pos"; ps = "fa-pct"
        ns = f'<div class="fa-mut">{_e(alt)}</div>'
    else:
        d = rozet("Eşik altı", "gray"); sn = "fa-card fa-neg"; ps = "fa-pct fa-off"
        ns = f'<div class="fa-mut">{_e(alt)} • Gerekli: %{e:.0f}</div>'
    bar = olasilik_bar("", y, e)
    return f'<div class="{sn}"><div class="fa-ttl">{_e(b)}</div><div class="fa-pickrow"><div><div class="fa-pick">{_e(s)}</div>{d}</div><div class="{ps}">%{y:.1f}</div></div>{bar}{ns}</div>'


def okunan_veriler_paneli(v):
    if v.get("format") in ("sportytrader", "mutating"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{v.get('takim_ev', 'Ev')}**")
            st.markdown(f"- Atılan: **{v.get('atilan_ev', 0):.2f}**")
            st.markdown(f"- Yenen: **{v.get('yenen_ev', 0):.2f}**")
            st.markdown(f"- CS: **{v.get('clean_sheets_ev', 0):.1f}%**")
            st.markdown(f"- KG: **{v.get('kg_siklik_ev', 0):.1f}%**")
        with c2:
            st.markdown(f"**{v.get('takim_dep', 'Dep')}**")
            st.markdown(f"- Atılan: **{v.get('atilan_dep', 0):.2f}**")
            st.markdown(f"- Yenen: **{v.get('yenen_dep', 0):.2f}**")
            st.markdown(f"- CS: **{v.get('clean_sheets_dep', 0):.1f}%**")
            st.markdown(f"- KG: **{v.get('kg_siklik_dep', 0):.1f}%**")


def _form_detay(form_str):
    if not form_str: return None
    s = str(form_str).upper().replace(" ", "").strip()
    s = "".join(c for c in s if c in "WDL")
    if not s: return None
    return {"W": s.count("W"), "D": s.count("D"), "L": s.count("L"), "n": len(s), "str": s}


def _form_hikaye(form_str, takim, ev_mi=True):
    f = _form_detay(form_str)
    if not f: return None
    n, w, d, l = f["n"], f["W"], f["D"], f["L"]
    p = []
    if w: p.append(f"{w} galibiyet")
    if d: p.append(f"{d} beraberlik")
    if l: p.append(f"{l} mağlubiyet")
    detay = ", ".join(p)
    sinif = "ev" if ev_mi else "dep"
    if w >= n - 1 and n >= 3:
        ton = "muhteşem bir form yakalamış durumda"
    elif w >= (n + 1) // 2:
        ton = "iyi bir form grafiği çiziyor"
    elif l >= (n + 1) // 2:
        ton = "formsuz günler geçiriyor"
    else:
        ton = "istikrarsız bir görünüm sergiliyor"
    return f"<span class='{sinif}'>{takim}</span> son {n} maçında {detay} alarak {ton}"


def _trend_cumleleri(v, taraf):
    key = f"trends_{taraf}"
    trends = v.get(key, [])
    if not trends: return []
    return [str(t).strip() for t in trends if t and str(t).strip()]


def ai_yorum_olustur(v, a):
    """Maç hakkında uzun, akıcı, hikayeli yorum üretir."""
    te = (v.get("takim_ev", "Ev") or "Ev").strip()
    td = (v.get("takim_dep", "Dep") or "Dep").strip()

    ppg_ev = float(v.get("ppg_ev", 0.0) or 0.0)
    mpg_dep = float(v.get("mpg_dep", 0.0) or 0.0)
    ae = float(v.get("atilan_ev", 0.0) or 0.0)
    ad = float(v.get("atilan_dep", 0.0) or 0.0)
    ye = float(v.get("yenen_ev", 0.0) or 0.0)
    yd = float(v.get("yenen_dep", 0.0) or 0.0)
    kg_ev = float(v.get("kg_siklik_ev", 0.0) or 0.0)
    kg_dep = float(v.get("kg_siklik_dep", 0.0) or 0.0)
    u25_ev = float(v.get("ust25_ev", 0.0) or 0.0)
    u25_dep = float(v.get("ust25_dep", 0.0) or 0.0)
    cs_ev = float(v.get("clean_sheets_ev", 0.0) or 0.0)
    cs_dep = float(v.get("clean_sheets_dep", 0.0) or 0.0)
    ts_ev = float(v.get("team_scored_ev", 0.0) or 0.0)
    ts_dep = float(v.get("team_scored_dep", 0.0) or 0.0)
    form_ev = v.get("form_str_ev", "")
    form_dep = v.get("form_str_dep", "")
    s_ev = int(v.get("siralama_ev", 0) or 0)
    s_dep = int(v.get("siralama_dep", 0) or 0)
    xg_ev = float(v.get("xg_ev", 0.0) or 0.0)
    xg_dep = float(v.get("xg_dep", 0.0) or 0.0)
    trends_ev = _trend_cumleleri(v, "ev")
    trends_dep = _trend_cumleleri(v, "dep")

    lam_ev = a["lam_ev"]; lam_dep = a["lam_dep"]
    ust25 = a["ust_25"]; alt25 = a["alt_25"]
    kgvar = a["kg_var_model"]; kgyok = a["kg_yok_model"]
    p1v = a["p1"]; pxv = a["px"]; p2v = a["p2"]

    def V(x): return f"<span class='vurgu'>{x}</span>"
    def U(x): return f"<span class='uyari'>{x}</span>"
    def K(x): return f"<span class='kotu'>{x}</span>"
    def EV(x): return f"<span class='ev'>{x}</span>"
    def DP(x): return f"<span class='dep'>{x}</span>"

    bolumler = []

    # ============================================================
    # 1. MAÇIN TABLOSU
    # ============================================================
    hp = []
    if s_ev and s_dep:
        if s_ev < s_dep:
            fark = s_dep - s_ev
            if fark >= 8:
                hp.append(f"Lig tablosunda {EV(te)} {V(f'{s_ev}.')} sırada, {DP(td)} ise {V(f'{s_dep}.')} sırada yer alıyor. Aradaki {V(fark)} basamaklık fark, iki takım arasındaki form ve kalite uçurumunu net şekilde gösteriyor.")
            elif fark >= 4:
                hp.append(f"{EV(te)} ligde {V(f'{s_ev}.')}, {DP(td)} ise {V(f'{s_dep}.')} sırada. Ev sahibi kağıt üzerinde bir adım önde görünüyor.")
            else:
                hp.append(f"Lig tablosunda {EV(te)} {V(f'{s_ev}.')}, {DP(td)} ise {V(f'{s_dep}.')} sırada. Aradaki fark sadece {V(fark)} basamak — yani kağıt üzerinde iki takım neredeyse eşit seviyede.")
        elif s_dep < s_ev:
            fark = s_ev - s_dep
            if fark >= 8:
                hp.append(f"Lig tablosunda {DP(td)} {V(f'{s_dep}.')} sırada, {EV(te)} ise {V(f'{s_ev}.')} sırada. Deplasman ekibi {V(fark)} basamak daha yukarıda — bu, kağıt üzerinde onları favori yapıyor.")
            elif fark >= 4:
                hp.append(f"{DP(td)} ligde {V(f'{s_dep}.')}, {EV(te)} ise {V(f'{s_ev}.')} sırada. Deplasman bir adım önde.")
            else:
                hp.append(f"İki takım da tabloda çok yakın: {DP(td)} {V(f'{s_dep}.')}, {EV(te)} {V(f'{s_ev}.')}.")
        else:
            hp.append(f"İki takım da ligde {V(f'{s_ev}.')} sırada — tam anlamıyla dengeli bir eşleşme.")

    f_ev_c = _form_hikaye(form_ev, te, ev_mi=True)
    f_dep_c = _form_hikaye(form_dep, td, ev_mi=False)
    if f_ev_c:
        hp.append(f_ev_c + ". Form grafiği işi ilginç bir yere taşıyor.")
    if f_dep_c:
        hp.append(f_dep_c + ".")

    if ae > 0 and ye > 0 and ad > 0 and yd > 0:
        if ye <= 0.8 and yd >= 1.5:
            hp.append(f"Asıl kritik nokta ev/deplasman performansı: {EV(te)} evinde maç başına {V(f'{ae:.2f}')} gol atıp sadece {V(f'{ye:.2f}')} gol yiyor. {DP(td)} ise deplasmanda maç başına {V(f'{ad:.2f}')} gol atarken {K(f'{yd:.2f}')} gol yiyor — yani dış sahada adeta bir savunma faciası yaşıyor.")
        elif yd <= 0.8 and ye >= 1.5:
            hp.append(f"Ev/deplasman tablosu tersine: {DP(td)} deplasmanda maç başına {V(f'{ad:.2f}')} gol atıp sadece {V(f'{yd:.2f}')} gol yiyor. {EV(te)} ise evinde {K(f'{ye:.2f}')} gol yiyor — savunma anlamında ciddi sıkıntıda.")
        elif ye <= 1.0 and yd <= 1.0:
            hp.append(f"Savunma tarafında iki takım da sağlam: {EV(te)} {V(f'{ye:.2f}')}, {DP(td)} {V(f'{yd:.2f}')} gol yiyor. Bu da gol sayısının düşük kalma ihtimalini artırıyor.")
        elif ye >= 1.8 and yd >= 1.8:
            hp.append(f"İki takımın da savunması sıkıntılı — {EV(te)} {K(f'{ye:.2f}')}, {DP(td)} {K(f'{yd:.2f}')} gol yiyor. Bu tabloda karşılıklı goller sürpriz olmaz.")
        else:
            hp.append(f"Ev sahibi {EV(te)} kendi sahasında maç başına {V(f'{ae:.2f}')} gol atıp {V(f'{ye:.2f}')} yiyor. Deplasman {DP(td)} ise dışarıda {V(f'{ad:.2f}')} gol atıp {U(f'{yd:.2f}')} yiyor.")

    if cs_ev or cs_dep:
        cs_list = []
        if cs_ev: cs_list.append(f"{EV(te)} evinde %{V(f'{cs_ev:.0f}')} clean sheet")
        if cs_dep: cs_list.append(f"{DP(td)} deplasmanda %{K(f'{cs_dep:.0f}')} clean sheet")
        if cs_list:
            hp.append("Kale performansına bakınca " + ", ".join(cs_list) + ". " + ("Bu tablo deplasmanın kendi kalesini korumakta ne kadar zorlandığını açıkça gösteriyor." if cs_ev > cs_dep else "Ev sahibi savunmada ciddi sorun yaşıyor."))

    if xg_ev > 0 or xg_dep > 0:
        xs = []
        if xg_ev > 0: xs.append(f"{EV(te)} {V(f'{xg_ev:.2f}')}")
        if xg_dep > 0: xs.append(f"{DP(td)} {V(f'{xg_dep:.2f}')}")
        hp.append("Beklenen gol (xG) verileri de bu tabloyu destekliyor: " + ", ".join(xs) + ".")

    if trends_ev:
        hp.append(f"<b>📈 {te} trendleri:</b> " + " ".join(trends_ev[:3]))
    if trends_dep:
        hp.append(f"<b>📈 {td} trendleri:</b> " + " ".join(trends_dep[:3]))

    if hp:
        bolumler.append(("📖", "MAÇIN TABLOSU", " ".join(hp)))

    # ============================================================
    # 2. 1X2 NEDEN BU?
    # ============================================================
    s1, y1 = max([("1", p1v), ("X", pxv), ("2", p2v)], key=lambda x: x[1])
    p1 = p1v; px = pxv; p2 = p2v
    kp = []

    if s1 == "1":
        kp.append(f"Model bu maçta {EV(te)} tarafını yaklaşık {V(f'%{p1:.0f}')} olasılıkla işaret ediyor. Bunu söylerken birkaç kritik noktaya birlikte baktık:")
        nedenler = []
        if ppg_ev >= 2.2:
            nedenler.append(f"{EV(te)}'in evindeki puan ortalaması {V(f'{ppg_ev:.2f}')} — bu elit seviye bir rakam")
        elif ppg_ev >= 1.7:
            nedenler.append(f"{EV(te)}'in evindeki PPG'si {V(f'{ppg_ev:.2f}')} ile sağlam")
        if mpg_dep <= 0.8 and mpg_dep > 0:
            nedenler.append(f"{DP(td)}'in deplasman MPG'si sadece {K(f'{mpg_dep:.2f}')} — dış sahada adeta kayıp")
        elif mpg_dep <= 1.3 and mpg_dep > 0:
            nedenler.append(f"{DP(td)} deplasmanda {U(f'{mpg_dep:.2f}')} MPG ile zorlanıyor")
        if ye <= 0.8:
            nedenler.append(f"ev sahibi kendi sahasında maç başına yalnızca {V(f'{ye:.2f}')} gol yiyor (neredeyse her 2-3 maçta bir gol)")
        if yd >= 1.5:
            nedenler.append(f"deplasman ekibi dışarıda {K(f'{yd:.2f}')} gol yiyor — savunması delik deşik")
        if ts_ev >= 70:
            nedenler.append(f"ev sahibi maçlarının %{V(f'{ts_ev:.0f}')}'inde gol atmış")
        if 0 < s_ev < s_dep:
            nedenler.append(f"sıralama farkı ({V(f'{s_ev}.')} vs {V(f'{s_dep}.')}) ev sahibinin lehine")
        if cs_ev >= 50:
            nedenler.append(f"evinde %{V(f'{cs_ev:.0f}')} clean sheet yapıyor")
        f_ev_d = _form_detay(form_ev)
        if f_ev_d and f_ev_d["W"] >= f_ev_d["n"] - 1 and f_ev_d["n"] >= 3:
            nedenler.append(f"form grafiği ({V(form_ev)}) çok güçlü")
        if nedenler:
            kp.append("Öncelikle " + ", ".join(nedenler[:5]) + ".")
        karsi = []
        if px > 20: karsi.append(f"beraberlik ihtimali %{px:.0f} ile hiç de az değil")
        if p2 > 15: karsi.append(f"deplasmanın kazanma şansı da %{p2:.0f} seviyesinde")
        if karsi:
            kp.append("Elbette " + " ve ".join(karsi) + " — futbol sürprizlere açık bir oyun. Ama mevcut veriler ışığında ev sahibinin kazanması en olası senaryo olarak öne çıkıyor.")
        kp.append(f"Tüm bunları birleştirdiğimizde <b>1 ({te} Kazanır)</b> demek en mantıklısı oldu.")

    elif s1 == "2":
        kp.append(f"Model bu maçta {DP(td)} tarafını yaklaşık {V(f'%{p2:.0f}')} olasılıkla öne çıkarıyor. Bunu söylerken şu noktalara baktık:")
        nedenler = []
        if mpg_dep >= 2.2:
            nedenler.append(f"{DP(td)}'in deplasman MPG'si {V(f'{mpg_dep:.2f}')} — deplasmanda bile canavar gibi")
        elif mpg_dep >= 1.7:
            nedenler.append(f"{DP(td)} dış sahada {V(f'{mpg_dep:.2f}')} MPG ile etkili")
        if ppg_ev <= 0.8 and ppg_ev > 0:
            nedenler.append(f"{EV(te)}'in evindeki PPG'si {K(f'{ppg_ev:.2f}')} — kendi sahasında bile kayıp")
        elif ppg_ev <= 1.3 and ppg_ev > 0:
            nedenler.append(f"{EV(te)} evinde {U(f'{ppg_ev:.2f}')} PPG ile zorlanıyor")
        if yd <= 0.8:
            nedenler.append(f"deplasman dış sahada sadece {V(f'{yd:.2f}')} gol yiyor")
        if ye >= 1.5:
            nedenler.append(f"ev sahibi {K(f'{ye:.2f}')} gol yiyor")
        if 0 < s_dep < s_ev:
            nedenler.append(f"sıralama farkı ({V(f'{s_dep}.')} vs {V(f'{s_ev}.')}) deplasmanın lehine")
        f_dep_d = _form_detay(form_dep)
        if f_dep_d and f_dep_d["W"] >= f_dep_d["n"] - 1 and f_dep_d["n"] >= 3:
            nedenler.append(f"deplasman formu ({V(form_dep)}) mükemmel")
        if nedenler:
            kp.append("Öncelikle " + ", ".join(nedenler[:5]) + ".")
        karsi = []
        if px > 20: karsi.append(f"beraberlik %{px:.0f} ile hâlâ masada")
        if p1 > 20: karsi.append(f"ev sahibinin de %{p1:.0f} şansı var")
        if karsi:
            kp.append("Ancak " + " ve ".join(karsi) + ". Yani bu maçta kesin bir şey söylemek zor, fakat tüm veriler deplasman lehine eğiliyor.")
        kp.append(f"Bu veriler ışığında <b>2 ({td} Kazanır)</b> en mantıklı tercih olarak öne çıkıyor.")

    else:
        kp.append(f"Model bu maçta beraberliği yaklaşık {V(f'%{px:.0f}')} olasılıkla işaret ediyor. Bu tip maçlarda genelde iki takım birbirini nötralize eder. Neden böyle düşündük:")
        nedenler = []
        if ppg_ev > 0 and mpg_dep > 0 and abs(ppg_ev - mpg_dep) < 0.4:
            nedenler.append(f"iki takımın form ortalamaları neredeyse eşit ({V(f'{ppg_ev:.2f}')} vs {V(f'{mpg_dep:.2f}')})")
        if ae > 0 and ad > 0 and abs(ae - ad) < 0.4:
            nedenler.append(f"hücum güçleri birbirine çok yakın ({V(f'{ae:.2f}')} vs {V(f'{ad:.2f}')})")
        if ye > 0 and yd > 0 and abs(ye - yd) < 0.5:
            nedenler.append("iki savunma da benzer seviyede")
        if s_ev and s_dep and abs(s_ev - s_dep) <= 3:
            nedenler.append(f"lig sıralamaları çok yakın ({V(f'{s_ev}.')} vs {V(f'{s_dep}.')})")
        if nedenler:
            kp.append("Öncelikle " + ", ".join(nedenler[:4]) + ".")
        kp.append(f"Yine de 1 ve 2 ihtimalleri de yabana atılmamalı — ev sahibi %{p1:.0f}, deplasman %{p2:.0f}. Ama beraberlik {V(f'%{px:.0f}')} ile en yüksek olasılık olarak öne çıkıyor.")
        kp.append("Bu veriler ışığında <b>X (Beraberlik)</b> en dengeli tercih gibi görünüyor.")

    if kp:
        bolumler.append(("🎯", "NEDEN BU SONUÇ?", " ".join(kp)))

    # ============================================================
    # 3. GOL BEKLENTİSİ
    # ============================================================
    gp = []
    u25 = ust25; a25 = alt25
    top_at = ae + ad
    top_ye = ye + yd
    lam_top = lam_ev + lam_dep

    if u25 >= a25:
        gp.append(f"Bu maçta <b>Üst 2.5</b> tarafı ağır basıyor (%{u25:.1f}). Neden mi?")
        gn = []
        if top_at >= 3.0:
            gn.append(f"iki takım toplamda maç başına {V(f'{top_at:.2f}')} gol üretiyor")
        if top_ye >= 3.0:
            gn.append(f"toplam {V(f'{top_ye:.2f}')} gol yiyorlar — yani savunmalar delik deşik")
        if u25_ev >= 55 and u25_dep >= 55:
            gn.append(f"her iki takımın da maçlarının yarısından fazlası 2.5 üstü bitmiş (ev %{V(f'{u25_ev:.0f}')}, dep %{V(f'{u25_dep:.0f}')})")
        elif u25_ev >= 55:
            gn.append(f"{EV(te)} maçlarının %{V(f'{u25_ev:.0f}')}'inde 2.5 üstü görmüş")
        elif u25_dep >= 55:
            gn.append(f"{DP(td)} maçlarının %{V(f'{u25_dep:.0f}')}'inde 2.5 üstü görmüş")
        if gn:
            gp.append("Çünkü " + ", ".join(gn[:3]) + ".")
        gp.append(f"Modelin beklediği toplam gol sayısı {V(f'{lam_top:.2f}')} seviyesinde — ev sahibi {V(f'{lam_ev:.2f}')}, deplasman {V(f'{lam_dep:.2f}')} gol beklentisiyle oynuyor.")
        gp.append("Bu yüzden <b>Üst 2.5</b> demek daha mantıklı.")
    else:
        gp.append(f"Bu maçta <b>Alt 2.5</b> tarafı öne çıkıyor (%{a25:.1f}). Sebeplerine bakalım:")
        gn = []
        if top_at <= 2.4 and top_at > 0:
            gn.append(f"iki takım toplamda sadece {V(f'{top_at:.2f}')} gol ortalaması yakalamış")
        if ye <= 1.0 and ye > 0:
            gn.append(f"{EV(te)} evinde maç başına yalnızca {V(f'{ye:.2f}')} gol yiyor — sağlam savunma")
        if yd <= 1.0 and yd > 0:
            gn.append(f"{DP(td)} dışarıda {V(f'{yd:.2f}')} gol yiyor")
        if cs_ev >= 40:
            gn.append(f"{EV(te)} maçlarının %{V(f'{cs_ev:.0f}')}'inde gol yememiş")
        if cs_dep >= 40:
            gn.append(f"{DP(td)} maçlarının %{V(f'{cs_dep:.0f}')}'inde kalesini gole kapatmış")
        if u25_ev > 0 and u25_ev <= 40:
            gn.append(f"{EV(te)} maçlarının sadece %{U(f'{u25_ev:.0f}')}'inde 2.5 üstü görmüş")
        if u25_dep > 0 and u25_dep <= 40:
            gn.append(f"{DP(td)} maçlarında bu oran %{U(f'{u25_dep:.0f}')}")
        if gn:
            gp.append("Çünkü " + ", ".join(gn[:3]) + ".")
        gp.append(f"Modelin beklediği toplam gol de {V(f'{lam_top:.2f}')} seviyesinde — yani 2.5 barajının altı.")
        gp.append("Tüm bu veriler ışığında <b>Alt 2.5</b> demek daha akıllıca.")

    if gp:
        bolumler.append(("⚽", "GOL BEKLENTİSİ", " ".join(gp)))

    # ============================================================
    # 4. KG
    # ============================================================
    kgp = []
    if kgvar >= kgyok:
        kgp.append(f"<b>Karşılıklı Gol Var</b> tarafı ağır basıyor (%{kgvar:.1f}). Neden böyle düşünüyoruz:")
        kn = []
        if kg_ev >= 60:
            kn.append(f"{EV(te)} maçlarının %{V(f'{kg_ev:.0f}')}'inde karşılıklı gol görmüş")
        elif kg_ev >= 50:
            kn.append(f"{EV(te)} maçlarının yaklaşık yarısında iki takım da gol atmış (%{V(f'{kg_ev:.0f}')})")
        if kg_dep >= 60:
            kn.append(f"{DP(td)} maçlarının %{V(f'{kg_dep:.0f}')}'inde KG gerçekleşmiş")
        elif kg_dep >= 50:
            kn.append(f"{DP(td)}'te bu oran %{V(f'{kg_dep:.0f}')} civarında")
        if ye >= 1.0 and yd >= 1.0:
            kn.append(f"her iki takım da maç başına ortalama {V(f'{(ye+yd)/2:.2f}')} gol yiyor")
        if ae >= 1.0 and ad >= 1.0:
            kn.append(f"iki taraf da hücumda etkili ({V(f'{ae:.2f}')} vs {V(f'{ad:.2f}')} gol ortalaması)")
        if kn:
            kgp.append("Çünkü " + ", ".join(kn[:3]) + ".")
        kgp.append("Yani hem ev sahibi hem deplasman gol atma eğiliminde. Bu durumda <b>KG Var</b> tercihi mantıklı.")
    else:
        kgp.append(f"<b>Karşılıklı Gol Yok</b> tarafı açık ara öne çıkıyor (%{kgyok:.1f}). Neden böyle düşünüyoruz:")
        kn = []
        if kg_ev <= 40 and kg_ev > 0:
            kn.append(f"{EV(te)} maçlarının yalnızca %{K(f'{kg_ev:.0f}')}'inde iki takım da gol atmış")
        if kg_dep <= 40 and kg_dep > 0:
            kn.append(f"{DP(td)}'te bu oran sadece %{K(f'{kg_dep:.0f}')}")
        if ye <= 1.0 and ye > 0:
            kn.append(f"{EV(te)} savunması evinde {V(f'{ye:.2f}')} gol yiyor — sağlam")
        if yd <= 1.0 and yd > 0:
            kn.append(f"{DP(td)} dışarıda {V(f'{yd:.2f}')} gol yiyor")
        if cs_ev >= 45:
            kn.append(f"{EV(te)} maçlarının %{V(f'{cs_ev:.0f}')}'inde kalesini gole kapatmış")
        if cs_dep >= 45:
            kn.append(f"{DP(td)} de %{V(f'{cs_dep:.0f}')}'inde gol yememiş")
        if kn:
            kgp.append("Çünkü " + ", ".join(kn[:3]) + ".")
        kgp.append("Bu tabloda en az bir takımın gol atamama ihtimali yüksek görünüyor. Bu yüzden <b>KG Yok</b> daha mantıklı.")

    if kgp:
        bolumler.append(("🤝", "KARŞILIKLI GOL (KG)", " ".join(kgp)))

    # ============================================================
    # 5. GERÇEKÇİ SENARYO
    # ============================================================
    sn = []
    yorum_ev = []
    yorum_dep = []
    if ye <= 0.6: yorum_ev.append(f"{EV(te)} evinde son derece sağlam")
    elif ye >= 1.8: yorum_ev.append(f"{EV(te)} evinde savunmada sıkıntılı")
    if ae >= 1.8: yorum_ev.append(f"hücumda etkili ({V(f'{ae:.2f}')} gol/maç)")
    elif ae <= 0.8: yorum_ev.append(f"hücumda kısır ({K(f'{ae:.2f}')} gol/maç)")

    if yd >= 1.8: yorum_dep.append(f"{DP(td)} deplasmanda savunma faciası yaşıyor")
    elif yd <= 0.8: yorum_dep.append(f"{DP(td)} dış sahada sağlam")
    if ad >= 1.8: yorum_dep.append(f"deplasmanda gol bulmayı biliyor ({V(f'{ad:.2f}')} gol/maç)")
    elif ad <= 0.8: yorum_dep.append(f"dış sahada gol üretmekte zorlanıyor ({U(f'{ad:.2f}')} gol/maç)")

    if yorum_ev:
        sn.append(" ".join(yorum_ev).capitalize() + ".")
    if yorum_dep:
        sn.append(" ".join(yorum_dep).capitalize() + ".")

    se_t = int(round(lam_ev)); sd_t = int(round(lam_dep))
    if se_t == sd_t: skor_t = f"{se_t}-{sd_t}"
    elif s1 == "1": skor_t = f"{max(1, se_t)}-{max(0, sd_t)}"
    else: skor_t = f"{max(0, se_t)}-{max(1, sd_t)}"
    sn.append(f"<b>En olası skor tahmini:</b> {V(skor_t)} civarı. Fakat futbolun sürprizlere açık bir oyun olduğunu unutmayın — hiçbir tahmin %100 kesinlik taşımaz.")

    if sn:
        bolumler.append(("📌", "GERÇEKÇİ SENARYO", " ".join(sn)))

    return bolumler


def ai_yorum_paneli(v, a):
    bolumler = ai_yorum_olustur(v, a)
    if not bolumler:
        return ""

    html_parcalar = []
    for ikon, baslik, metin in bolumler:
        html_parcalar.append(
            f'<div class="fa-ai-bolum">'
            f'<div class="fa-ai-bolum-baslik">{ikon} {baslik}</div>'
            f'<div class="fa-ai-bolum-metin">{metin}</div>'
            f'</div>'
        )

    s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
    karar_isim = {"1": f"1 ({te} Kazanır)", "X": "X (Beraberlik)", "2": f"2 ({td} Kazanır)"}[s1]
    if a["ust_25"] >= a["alt_25"]:
        gol_isim = f"Üst 2.5 (%{a['ust_25']:.0f})"
    else:
        gol_isim = f"Alt 2.5 (%{a['alt_25']:.0f})"
    if a["kg_var_model"] >= a["kg_yok_model"]:
        kg_isim = f"KG Var (%{a['kg_var_model']:.0f})"
    else:
        kg_isim = f"KG Yok (%{a['kg_yok_model']:.0f})"

    karar_html = (
        f'<div class="fa-ai-karar">'
        f'<b>🎯 MODEL ÖZETİ:</b> {karar_isim} &nbsp;•&nbsp; {gol_isim} &nbsp;•&nbsp; {kg_isim}'
        f'</div>'
    )

    return (
        f'<div class="fa-ai-kart">'
        f'<div class="fa-ai-baslik">🤖 AI MAÇ YORUMU</div>'
        f'{"".join(html_parcalar)}'
        f'{karar_html}'
        f'</div>'
    )


def yasal_metin_goster():
    with st.expander("📜 Kullanım Şartları ve Sorumluluk Reddi — OKU", expanded=False):
        st.markdown(YASAL_METIN)


@st.cache_data(ttl=60, show_spinner=False)
def gecmis_istatistik_hesapla_cached(gecmis_hash, _gecmis_ref, e1, ex, e2, eu, ea, ekv, eky):
    g_1x2 = g_gol = g_kg = 0
    g_1x2_t = g_gol_t = g_kg_t = 0
    for gg in _gecmis_ref:
        try:
            vv = gg.get("veri", {})
            if not vv.get("skor_belli", False): continue
            dd = sonuc_hesapla(gg)
            if not dd: continue
            o = dd["oneri_1x2"]
            if o.get("tuttu") is not None:
                g_1x2_t += 1
                if o["tuttu"]: g_1x2 += 1
            o = dd["oneri_gol"]
            if o.get("tuttu") is not None:
                g_gol_t += 1
                if o["tuttu"]: g_gol += 1
            o = dd["oneri_kg"]
            if o.get("tuttu") is not None:
                g_kg_t += 1
                if o["tuttu"]: g_kg += 1
        except Exception: continue
    p1 = (g_1x2 / g_1x2_t * 100) if g_1x2_t > 0 else 0
    pg = (g_gol / g_gol_t * 100) if g_gol_t > 0 else 0
    pk = (g_kg / g_kg_t * 100) if g_kg_t > 0 else 0
    return p1, g_1x2, g_1x2_t, pg, g_gol, g_gol_t, pk, g_kg, g_kg_t


def gecmis_istatistik_hesapla():
    try:
        gc = st.session_state.gecmis_analizler
        son_url = gc[-1].get("veri", {}).get("kaynak_url", "") if gc else ""
        e = st.session_state.esikler
        anahtar = f"{len(gc)}_{son_url}_{e.get('esik_1',55)}_{e.get('esik_x',55)}_{e.get('esik_2',55)}_{e.get('ust',65)}_{e.get('alt',55)}_{e.get('kg_var',57)}_{e.get('kg_yok',72)}"
        return gecmis_istatistik_hesapla_cached(
            anahtar, gc,
            e.get("esik_1", 55.0), e.get("esik_x", 55.0), e.get("esik_2", 55.0),
            e.get("ust", 65.0), e.get("alt", 55.0), e.get("kg_var", 57.0), e.get("kg_yok", 72.0),
        )
    except Exception:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0


def modern_istatistik_grafik(baslik="📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ"):
    p1, t1, s1, pg, tg, sg, pk, tk, sk = gecmis_istatistik_hesapla()
    st.markdown(f'<div class="mh-hero-ust" style="text-align:center;margin-top:14px;">{_e(baslik)}</div>', unsafe_allow_html=True)
    st.markdown(f'''<div class="fa-donut-grid">
    <div class="fa-donut-kart" style="--c:#22c55e;">
        <div class="fa-donut-ttl">🎯 1X2</div>
        {_donut_svg(p1, "#22c55e")}
        <div class="fa-donut-sub"><b>{t1}</b> / {s1}</div>
    </div>
    <div class="fa-donut-kart" style="--c:#3b82f6;">
        <div class="fa-donut-ttl">⚽ GOL</div>
        {_donut_svg(pg, "#3b82f6")}
        <div class="fa-donut-sub"><b>{tg}</b> / {sg}</div>
    </div>
    <div class="fa-donut-kart" style="--c:#f59e0b;">
        <div class="fa-donut-ttl">🤝 KG</div>
        {_donut_svg(pk, "#f59e0b")}
        <div class="fa-donut-sub"><b>{tk}</b> / {sk}</div>
    </div>
    </div>''', unsafe_allow_html=True)


# ==========================================
# ADMİN GİRİŞ EKRANI
# ==========================================
def admin_giris_ekrani():
    st.markdown('''<div class="login-hero"><div class="login-logo">🔐</div><h1 class="login-title">Giriş Yap</h1><p class="login-subtitle">Admin veya üye girişi</p></div>''', unsafe_allow_html=True)
    with st.form("admin_giris_form"):
        kadi = st.text_input("👤 Kullanıcı Adı", placeholder="Kullanıcı adın...", key="admin_kadi_input")
        sifre = st.text_input("🔐 Şifre", type="password", placeholder="Şifren...", key="admin_sifre_input")
        c1, c2 = st.columns(2)
        with c1: giris_btn = st.form_submit_button("✅ Giriş Yap", use_container_width=True, type="primary")
        with c2: iptal_btn = st.form_submit_button("⬅️ Ana Sayfa", use_container_width=True)
        if giris_btn:
            if not kadi.strip() or not sifre: st.error("❌ Kullanıcı adı ve şifre gerekli.")
            elif kadi.strip() == ADMIN_KULLANICI_ADI and sifre == ADMIN_SIFRE:
                st.session_state.rol = "admin"; st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"; st.rerun()
            elif kullanici_dogrula(kadi.strip(), sifre):
                st.session_state.aktif_kullanici = kadi.strip(); st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"
                st.success(f"✅ Hoş geldin, {kadi.strip()}!"); time.sleep(1); st.rerun()
            else: st.error("❌ Kullanıcı adı veya şifre hatalı.")
        if iptal_btn:
            st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"; st.rerun()
    st.markdown('<div class="login-divider">HESABIN YOK MU?</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✨ Üye Ol", use_container_width=True, key="admin_to_kayit", type="primary"):
            st.session_state.admin_login_acik = False; st.session_state.sayfa = "kayit"; st.rerun()
    with c2:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="admin_to_main"):
            st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# ÜST BAR
# ==========================================
def ust_bar():
    c1, c2 = st.columns([3, 1])
    with c1:
        if admin_mi():
            st.markdown('<div style="padding:6px 0; font-size:0.8rem; color:#22c55e; font-weight:700;">👑 Admin Modu</div>', unsafe_allow_html=True)
        elif uye_mi():
            premium = uye_premium_mu()
            if premium:
                badge = '🌟 <span style="color:#22c55e;font-weight:700;">PREMIUM</span>'
                try:
                    k = kullanicilar_yukle().get(uye_adi(), {})
                    bs = k.get("abonelik_bitis")
                    if bs:
                        bt = datetime.strptime(bs, "%Y-%m-%d"); kl = (bt - datetime.now()).days
                        if kl >= 0: badge += f' <span style="color:#8fa0bd;font-size:0.72rem;">({kl} gün kaldı)</span>'
                except Exception: pass
                st.markdown(f'<div style="padding:6px 0; font-size:0.8rem; color:#eaf1fb; font-weight:700;">👤 {_e(uye_adi())} &nbsp; {badge}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="padding:6px 0; font-size:0.8rem; color:#f59e0b; font-weight:700;">👤 {_e(uye_adi())} <span style="color:#8fa0bd;font-size:0.72rem;">(abonelik yok)</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="padding:6px 0; font-size:0.8rem; color:#8fa0bd; font-weight:600;">👤 Misafir Modu</div>', unsafe_allow_html=True)
    with c2:
        if admin_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="cikis_btn"):
                st.session_state.rol = "misafir"; st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"
                st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI); st.rerun()
        elif uye_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="uye_cikis_btn"):
                st.session_state.aktif_kullanici = None; st.session_state.sayfa = "giris"; st.rerun()


def misafir_aciklama():
    with st.expander("📖 Uygulamayı Tanı ve Kuralları Oku", expanded=False):
        st.markdown("""### ⚽ Futbol Analiz Pro
Geçmiş istatistiklere dayalı analiz ve tahminler. Sadece **bilgilendirme amaçlıdır**.

### 🌟 PREMIUM
- Tüm maçlar açık
- Haftalık / Aylık / Yıllık

### 🚫 SORUMLULUK REDDİ
- **18 yaşından küçükler** kullanamaz.
- Yasadışı bahis **suçtur**.
- **Kesin sonuç garantisi yoktur.**
- **YEDAM: 115**
""")


# ==========================================
# NAV BAR
# ==========================================
def nav_git(h):
    st.session_state.sayfa = h
    st.session_state.kayit_yapildi = False
    st.session_state.tek_silme_onay = None
    st.session_state.tek_silme_gelecek = None
    st.session_state.sil_onay_kadi = None
    if h == "backtest": st.session_state.bt_sonuc = None; st.session_state.bt_detaylar = []
    st.rerun()


def nav_bar():
    if st.session_state.sayfa in ("kayit", "uyegirisi", "odeme", "giris_yap"): return
    try: kutu = st.container(key="fa_nav")
    except TypeError: kutu = st.container()
    with kutu:
        if admin_mi():
            sec = [("🏠 Ana Sayfa", "giris"), ("🔮 Gelecek", "gelecek_admin"), ("📊 Geçmiş", "gecmis"), ("🔬 Test", "backtest"), ("💳 Ödemeler", "admin_odemeler"), ("👥 Aboneler", "admin_aboneler"), ("📬 Bildirimler", "admin_bildirimler"), ("⚙️ Ayar", "ayarlar")]
        elif uye_mi():
            sec = [("🏠 Ana Sayfa", "giris"), ("📊 Geçmiş Maçlar", "gecmis"), ("📬 Bildirim", "kullanici_bildirim")]
        else:
            sec = [("🏠 Ana Sayfa", "giris"), ("📊 Geçmiş Maçlar", "gecmis")]
        kl = st.columns(len(sec))
        for k, (e, h) in zip(kl, sec):
            with k:
                aktif = st.session_state.sayfa == h
                if st.button(e, key=f"nav_{h}", use_container_width=True, type="primary" if aktif else "secondary"):
                    if not aktif: nav_git(h)


# ==========================================
# UYGULAMA BAŞLANGIÇ
# ==========================================
if st.session_state.admin_login_acik and not admin_mi():
    admin_giris_ekrani()
    st.stop()

ust_bar()
nav_bar()


# ==========================================
# SAYFA: GİRİŞ YAP
# ==========================================
if st.session_state.sayfa == "giris_yap":
    admin_giris_ekrani()


# ==========================================
# SAYFA: ANA SAYFA
# ==========================================
elif st.session_state.sayfa == "giris":
    if admin_mi():
        st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:gray;'>Admin Paneli</p>", unsafe_allow_html=True)

        st.divider()
        st.markdown("### 📋 İstatistik Metnini Yapıştır")
        ym = st.text_area("Yapıştırma", height=200, key="yapistir_input", label_visibility="collapsed", placeholder="İstatistik metnini buraya yapıştır")
        c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
        with c1: analiz_btn = st.button("🚀 ANALİZ ET", use_container_width=True, type="primary")
        with c2: gecmis_btn = st.button("📊 Geçmiş", use_container_width=True)
        with c3: gelecek_btn = st.button("🔮 Gelecek", use_container_width=True)
        with c4: backtest_btn = st.button("🔬 Test", use_container_width=True)
        with c5: ayarlar_btn = st.button("⚙️ Ayar", use_container_width=True)
        if analiz_btn:
            if not ym.strip(): st.warning("⚠️ Metin yapıştır.")
            else:
                cikan, okunamayanlar = metinden_veri_cikar(ym)
                if not cikan: st.error("❌ Veri çıkarılamadı.")
                else:
                    yv = copy.deepcopy(VARSAYILAN_VERI); yv.update(cikan)
                    st.session_state.form_verileri = yv; st.session_state.kayit_yapildi = False
                    st.session_state.manuel_bekleyen = okunamayanlar.copy() if okunamayanlar else []
                    if not veri_yeterli_mi(yv): st.error("⚠️ Yetersiz veri.")
                    else:
                        if okunamayanlar: st.session_state.sayfa = "manuel_giris"
                        else: st.session_state.sayfa = "sonuc"
                        st.rerun()
        if gecmis_btn: nav_git("gecmis")
        if gelecek_btn: nav_git("gelecek_admin")
        if backtest_btn: nav_git("backtest")
        if ayarlar_btn: nav_git("ayarlar")

        st.divider()
        st.markdown("### 🤖 Manuel Veri Çekme")
        vs1, vs2, vs3 = st.tabs(["🔄 Bugünün Maçları", "📜 Lig Geçmişi", "🏁 Sonuçları İşle"])
        with vs1:
            if st.session_state.toplu_cek_ozet:
                oz = st.session_state.toplu_cek_ozet
                st.markdown(f"**Son:** Bulunan: **{oz.get('bulunan', 0)}** | Eklenen: **{oz.get('eklenen', 0)}** | Eşik altı: **{oz.get('esik_alti', 0)}** | Veri yok: **{oz.get('veri_yok', 0)}** | Zaten vardı: **{oz.get('zaten_var', 0)}** | Hata: **{oz.get('hata', 0)}**")
                if oz.get("detay_log"):
                    with st.expander(f"🔎 Detay"):
                        for s in oz["detay_log"]: st.text(s)
            c1, c2 = st.columns(2)
            with c1: w = st.number_input("Paralel", 1, 4, 3, 1, key="fw")
            with c2:
                st.markdown("")
                if st.button("🚀 Bugünün Maçlarını Çek", use_container_width=True, type="primary", key="mbtn"):
                    ph = st.empty()
                    def _p(i, t, n):
                        try: ph.progress(min((i + 1) / t, 1.0), text=f"{i+1}/{t}: {n}")
                        except Exception: pass
                    with st.spinner("Çekiliyor..."):
                        mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=_p, max_workers=int(w))
                    ph.empty(); st.rerun()
        with vs2:
            lurl = st.text_input("Lig URL", key="lig_url_input", placeholder="https://www.mutating.com/football-stats/league-...")
            c1, c2 = st.columns(2)
            with c1: la = st.number_input("Kaç maç?", 5, 30, 10, 1, key="lig_adet")
            with c2: lw = st.number_input("Paralel", 1, 4, 3, 1, key="lig_workers")
            if st.button("📜 Ligi Çek", use_container_width=True, type="primary", key="lig_cek_btn"):
                if not lurl.strip(): st.warning("URL gerekli")
                else:
                    ph = st.empty()
                    def _p2(i, t, n):
                        try: ph.progress(min((i + 1) / t, 1.0), text=f"{i+1}/{t}: {n}")
                        except Exception: pass
                    with st.spinner(f"Son {la} maç..."):
                        bas, hat = lig_gecmis_cek(lurl.strip(), int(la), int(lw), _p2)
                    ph.empty()
                    if hat:
                        with st.expander(f"⚠️ {len(hat)} hata"):
                            for h in hat: st.caption(h)
                    if bas:
                        st.success(f"✅ {len(bas)} maç eklendi!"); time.sleep(2); st.rerun()
                    else: st.error("Hiçbir maç eklenemedi.")
        with vs3:
            if st.session_state.skor_ozet:
                oz = st.session_state.skor_ozet
                st.success(f"✅ {oz['tasinan']} taşındı • {oz['bitmemis']} bitmemiş")
            st.markdown(f"Bekleyen: **{len(st.session_state.gelecek_analizler)}**")
            sy = st.checkbox("Tarayıcı ile dene", value=False, key="skor_yedek")
            c1, c2 = st.columns(2)
            with c1: sw = st.number_input("Paralel", 1, 4, 3, 1, key="skor_w")
            with c2:
                if st.button("🏁 Skorları Çek", use_container_width=True, type="primary", key="skor_btn"):
                    if not st.session_state.gelecek_analizler: st.warning("Gelecek'te maç yok")
                    else:
                        with st.spinner("Kontrol..."):
                            st.session_state.skor_ozet = sonuclari_isle(bool(sy), int(sw))
                        st.rerun()

    else:
        gelecek = st.session_state.gelecek_analizler
        toplam = len(gelecek)
        premium = uye_premium_mu()
        kota = int(ayar_al("ucretsiz_kotasi", 3))

        if premium:
            kl = ""
            try:
                bs = kullanicilar_yukle().get(uye_adi(), {}).get("abonelik_bitis")
                if bs:
                    kk = (datetime.strptime(bs, "%Y-%m-%d") - datetime.now()).days
                    if kk >= 0: kl = f'<div class="mh-hero-badge">🌟 PREMIUM — {kk} gün kaldı</div>'
            except Exception: pass
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-title" style="font-size:1.25rem;">Hoş Geldin, {_e(uye_adi())}</div><div class="mh-hero-sub">Premium aktif — tüm analizler açık</div>{kl}</div>', unsafe_allow_html=True)
            modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ")
        elif uye_mi():
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-title" style="font-size:1.25rem;">Hoş Geldin, {_e(uye_adi())}</div><div class="mh-hero-sub">İlk {kota} maç ücretsiz açık</div><div class="mh-hero-badge" style="background:rgba(245,158,11,0.12);border-color:rgba(245,158,11,0.5);color:#f59e0b !important;">⚠️ ABONELİK YOK</div></div>', unsafe_allow_html=True)
            modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ")
            if st.button("💳 Premium'a Geç  •  ✨ Üye Ol", use_container_width=True, type="primary", key="ana_premium_btn"):
                st.session_state["odeme_hedef_kadi"] = uye_adi(); st.session_state.sayfa = "odeme"; st.rerun()
        else:
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-title" style="font-size:1.25rem;">Bugün {toplam} Maç</div><div class="mh-hero-sub">İlk {kota} maç ücretsiz açık</div></div>', unsafe_allow_html=True)
            modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ")
            if st.button("💳 Premium'a Geç  •  ✨ Üye Ol", use_container_width=True, type="primary", key="mis_prem"):
                st.session_state.sayfa = "kayit"; st.rerun()
            if st.button("🔐 Giriş Yap", use_container_width=True, key="mis_giris_btn"):
                st.session_state.sayfa = "giris_yap"; st.rerun()

        st.divider()
        if not gelecek: st.info("ℹ️ Henüz maç yok.")
        else:
            sirali = sorted(enumerate(gelecek), key=lambda x: saat_sirala_anahtari(x[1]))
            acik = 0
            for idx, g in sirali:
                v = g["veri"]; te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
                ulke = v.get("ulke", ""); saat = v.get("saat", ""); tarih = v.get("tarih", "")
                if premium or acik < kota:
                    try:
                        af = analiz_hesapla(v); le = af["lam_ev"]; ld = af["lam_dep"]
                    except Exception: le = ld = 0
                    st.markdown(mac_karti(te, td, False, 0, 0, le, ld, saat, ulke, tarih), unsafe_allow_html=True)
                    th = mac_tahmin_karti(v, g)
                    if th: st.markdown(th, unsafe_allow_html=True)
                    if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"gmac_{idx}"):
                        st.session_state.form_verileri = copy.deepcopy(v); st.session_state.kayit_yapildi = True
                        st.session_state.gelecekten_gelindi = True; st.session_state.aktif_gelecek_idx = idx
                        st.session_state.sayfa = "sonuc"; st.rerun()
                    acik += 1
                else:
                    st.markdown(kilitli_mac_karti(te, td, saat, ulke, tarih), unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("💳 Premium", use_container_width=True, key=f"kp_{idx}", type="primary"):
                            if uye_mi(): st.session_state["odeme_hedef_kadi"] = uye_adi(); st.session_state.sayfa = "odeme"
                            else: st.session_state.sayfa = "kayit"
                            st.rerun()
                    with c2:
                        if st.button("🔑 Giriş", use_container_width=True, key=f"kg_{idx}"):
                            st.session_state.sayfa = "giris_yap"; st.rerun()
                st.divider()

        yasal_metin_goster()
        misafir_aciklama()
        st.markdown('<div class="login-footer" style="margin-top:20px;">© <b>Futbol Analiz Pro</b> • Bilgi amaçlıdır</div>', unsafe_allow_html=True)
        # ==========================================
# SAYFA: KAYIT
# ==========================================
elif st.session_state.sayfa == "kayit":
    st.markdown('''<div class="login-hero"><div class="login-logo">✨</div><h1 class="login-title">Üye Ol</h1><p class="login-subtitle">Kullanıcı adı ve şifre belirle</p></div>''', unsafe_allow_html=True)
    with st.form("kayit_form"):
        yk = st.text_input("👤 Kullanıcı Adı", placeholder="örn: ahmet34", max_chars=30)
        ys = st.text_input("🔐 Şifre", type="password", placeholder="En az 4 karakter")
        yst = st.text_input("🔐 Şifre Tekrar", type="password", placeholder="Şifreyi tekrar gir")
        yasal_onay = st.checkbox("✅ **Kullanım Şartlarını, Sorumluluk Reddini ve KVKK metnini okudum, kabul ediyorum.** 18 yaşından büyük olduğumu beyan ederim.", key="kayit_yasal_onay_cb")
        c1, c2 = st.columns(2)
        with c1: kb = st.form_submit_button("✅ Kayıt Ol", use_container_width=True, type="primary")
        with c2: gb = st.form_submit_button("⬅️ Geri", use_container_width=True)
        if kb:
            if not yk.strip(): st.error("❌ Kullanıcı adı boş olamaz.")
            elif len(yk.strip()) < 3: st.error("❌ En az 3 karakter.")
            elif not yk.replace("_", "").isalnum(): st.error("❌ Sadece harf, rakam, _")
            elif yk.strip() == ADMIN_KULLANICI_ADI: st.error("❌ Bu isim kullanılamaz.")
            elif len(ys) < 4: st.error("❌ Şifre en az 4 karakter.")
            elif ys != yst: st.error("❌ Şifreler uyuşmuyor.")
            elif not yasal_onay: st.error("❌ Kayıt için Kullanım Şartlarını kabul etmelisiniz.")
            else:
                b, m = kullanici_ekle(yk.strip(), ys)
                if b:
                    st.session_state["aktif_kullanici"] = yk.strip()
                    st.session_state["odeme_hedef_kadi"] = yk.strip()
                    st.success(f"✅ {m} Ödeme sayfasına yönlendiriliyorsun...")
                    time.sleep(1.5); st.session_state.sayfa = "odeme"; st.rerun()
                else: st.error(f"❌ {m}")
        if gb: st.session_state.sayfa = "giris"; st.rerun()
    yasal_metin_goster()


# ==========================================
# SAYFA: ÜYE GİRİŞİ
# ==========================================
elif st.session_state.sayfa == "uyegirisi":
    st.markdown('''<div class="login-hero"><div class="login-logo">🔑</div><h1 class="login-title">Üye Girişi</h1></div>''', unsafe_allow_html=True)
    with st.form("uye_giris_form"):
        k = st.text_input("👤 Kullanıcı Adı")
        s = st.text_input("🔐 Şifre", type="password")
        c1, c2 = st.columns(2)
        with c1: g = st.form_submit_button("🔓 Giriş", use_container_width=True, type="primary")
        with c2: gg = st.form_submit_button("⬅️ Geri", use_container_width=True)
        if g:
            if not k.strip() or not s: st.error("❌ Bilgiler gerekli.")
            elif kullanici_dogrula(k.strip(), s):
                st.session_state["aktif_kullanici"] = k.strip()
                st.success(f"✅ Hoş geldin, {k.strip()}!")
                time.sleep(1); st.session_state.sayfa = "giris"; st.rerun()
            else: st.error("❌ Hatalı giriş.")
        if gg: st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: ÖDEME
# ==========================================
elif st.session_state.sayfa == "odeme":
    hedef = st.session_state.get("odeme_hedef_kadi") or uye_adi()
    if not hedef:
        st.error("❌ Kullanıcı yok.")
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary"):
            st.session_state.sayfa = "giris"; st.rerun()
        st.stop()
    iban = ayar_al("iban", "TR00 0000 0000 0000 0000 0000 00")
    hs = ayar_al("hesap_sahibi", "ADINIZ SOYADINIZ")
    fh = float(ayar_al("fiyat_haftalik", 49.0)); fa = float(ayar_al("fiyat_aylik", 149.0)); fy = float(ayar_al("fiyat_yillik", 999.0))
    st.markdown(f'''<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-icon">💳</div><div class="mh-hero-title">Premium'a Geç</div><div class="mh-hero-sub">Havale / EFT ile ödeme</div><div class="mh-hero-badge">● GÜVENLİ ÖDEME</div></div>''', unsafe_allow_html=True)
    st.markdown(f'''<div class="mh-info"><b>👤 Kullanıcı:</b> {_e(hedef)}<br>Açıklama kısmına <b>MUTLAKA</b> kullanıcı adını yaz.</div>''', unsafe_allow_html=True)
    st.markdown("### 📆 Paket Seç")
    sec = st.radio("Süre?", ["haftalik", "aylik", "yillik"], format_func=lambda x: {"haftalik": f"📅 Haftalık — {fh:.0f} ₺", "aylik": f"📆 Aylık — {fa:.0f} ₺", "yillik": f"🎯 Yıllık — {fy:.0f} ₺"}[x], index=1, key="odeme_sure_sec")
    sg = {"haftalik": 7, "aylik": 30, "yillik": 365}[sec]
    fy_ = {"haftalik": fh, "aylik": fa, "yillik": fy}[sec]
    et = {"haftalik": "Haftalık", "aylik": "Aylık", "yillik": "Yıllık"}[sec]
    if sec == "yillik":
        ai = fa * 12
        ind = int((1 - (fy / ai)) * 100) if ai > 0 else 0
        if ind > 0:
            st.markdown(f'<div class="fa-card fa-pos"><div class="fa-ttl">Seçilen</div><div class="fa-pickrow"><div class="fa-pick">🎯 Yıllık</div><div class="fa-pct">{fy_:.0f} ₺</div></div><div class="fa-mut">💸 %{ind} indirim!</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="fa-card fa-pos"><div class="fa-ttl">Seçilen</div><div class="fa-pickrow"><div class="fa-pick">🎯 Yıllık</div><div class="fa-pct">{fy_:.0f} ₺</div></div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="fa-card fa-pos"><div class="fa-ttl">Seçilen</div><div class="fa-pickrow"><div class="fa-pick">{et}</div><div class="fa-pct">{fy_:.0f} ₺</div></div></div>', unsafe_allow_html=True)
    st.markdown("### 🏦 Havale Bilgileri")
    st.markdown(f'<div class="fa-card"><div class="fa-ttl">Alıcı</div><div class="fa-pick" style="margin-bottom:10px;">{_e(hs)}</div><div class="fa-ttl">IBAN</div><div class="fa-pick" style="margin-bottom:10px;font-family:monospace;">{_e(iban)}</div><div class="fa-ttl">Tutar</div><div class="fa-pick" style="margin-bottom:10px;color:#22c55e;">{fy_:.0f} ₺</div><div class="fa-ttl">Açıklama</div><div class="fa-pick" style="color:#22c55e;font-weight:900;">{_e(hedef)}</div></div>', unsafe_allow_html=True)
    st.divider()
    st.markdown("### ✅ Ödemeyi Yaptım")
    bk = bekleyen_yukle()
    if hedef in bk and bk[hedef].get("durum") == "bekliyor":
        st.warning(f"⏳ Zaten bekleyen bildirimin var: **{bk[hedef].get('sure_etiket', '?')}**")
    else:
        iade_onay = st.checkbox("✅ **İade yapılmayacağını, hizmetin dijital olduğunu ve aktivasyon sonrası para iadesi talep edemeyeceğimi okudum, kabul ediyorum.**", key="odeme_yasal_onay_cb")
        if st.button("📤 Ödeme Yaptım — Bildir", use_container_width=True, type="primary", key="odeme_bildir_btn"):
            if not iade_onay: st.error("❌ İade koşullarını kabul etmelisiniz.")
            else:
                bk[hedef] = {"tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "sure_gun": int(sg), "sure_etiket": et, "fiyat": float(fy_), "durum": "bekliyor"}
                bekleyen_kaydet(bk)
                st.success("✅ Bildirimin alındı!"); time.sleep(2); st.rerun()
    yasal_metin_goster()
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="odeme_geri"):
            st.session_state.sayfa = "giris"; st.rerun()
    with c2:
        if st.button("🔄 Kontrol Et", use_container_width=True, key="odeme_kontrol"):
            if abonelik_aktif_mi(hedef):
                st.success("✅ Aboneliğin aktif!"); time.sleep(1.5); st.session_state.sayfa = "giris"; st.rerun()
            else: st.info("⏳ Bekleniyor.")


# ==========================================
# SAYFA: ADMIN ÖDEMELER
# ==========================================
elif st.session_state.sayfa == "admin_odemeler":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>💳 Bekleyen Ödemeler</h1>", unsafe_allow_html=True)
    bk = bekleyen_yukle()
    if not bk: st.info("ℹ️ Bekleyen ödeme yok.")
    else:
        for k, b in list(bk.items()):
            tg = b.get("sure_gun", 0); te = b.get("sure_etiket", "?"); fi = b.get("fiyat", 0); tt = b.get("tarih", "?")
            st.markdown(f'<div class="fa-card"><div class="fa-ttl">👤 {_e(k)}</div><div class="fa-pickrow"><div><div class="fa-pick">{te} — {fi:.0f} ₺</div><div class="fa-mut">📅 {_e(tt)}</div></div></div></div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button(f"✅ Onayla", use_container_width=True, type="primary", key=f"o_{k}"):
                    b_, yb = abonelik_aktif_et(k, tg)
                    if b_:
                        del bk[k]; bekleyen_kaydet(bk)
                        st.success(f"✅ {k} aktif! Bitiş: {yb}"); time.sleep(2); st.rerun()
            with c2:
                if st.button(f"❌ Reddet", use_container_width=True, key=f"r_{k}"):
                    del bk[k]; bekleyen_kaydet(bk); st.info("Silindi."); time.sleep(1.5); st.rerun()
            with c3:
                if st.button(f"🗑️ Sil", use_container_width=True, key=f"s_{k}"):
                    del bk[k]; bekleyen_kaydet(bk); st.rerun()
            st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="og"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: ADMIN ABONELER
# ==========================================
elif st.session_state.sayfa == "admin_aboneler":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>👥 Aboneler</h1>", unsafe_allow_html=True)
    st.caption("Abonelik süresi ekleme sadece 💳 Ödemeler sayfasından yapılır.")
    kl = kullanicilar_yukle()
    if not kl:
        st.info("ℹ️ Kayıtlı kullanıcı yok.")
    else:
        top = len(kl); ak = sum(1 for k in kl if abonelik_aktif_mi(k))
        st.markdown(f'<div class="mh-stat-grid"><div class="mh-stat"><div class="mh-stat-icon">👥</div><div class="mh-stat-num">{top}</div><div class="mh-stat-lbl">Toplam</div></div><div class="mh-stat"><div class="mh-stat-icon">🌟</div><div class="mh-stat-num">{ak}</div><div class="mh-stat-lbl">Aktif</div></div></div>', unsafe_allow_html=True)
        st.divider()
        for k, kd in list(kl.items()):
            kt = kd.get("kayit_tarihi", "?"); bs = kd.get("abonelik_bitis")
            aktif = abonelik_aktif_mi(k); kalan = 0
            if bs:
                try: kalan = (datetime.strptime(bs, "%Y-%m-%d") - datetime.now()).days
                except Exception: pass
            if aktif: dr = "#22c55e"; dt = f"🌟 AKTİF ({kalan} gün)"; ek = f"Bitiş: {bs}"
            elif bs: dr = "#ef4444"; dt = "⛔ SÜRESİ DOLMUŞ"; ek = f"Bitiş: {bs}"
            else: dr = "#94a3b8"; dt = "⚪ YOK"; ek = ""
            st.markdown(f'<div class="fa-card"><div class="fa-pickrow"><div><div class="fa-pick">👤 {_e(k)}</div><div class="fa-mut">📅 {_e(kt)} &nbsp; {_e(ek)}</div></div><div style="color:{dr};font-weight:800;font-size:0.85rem;">{_e(dt)}</div></div></div>', unsafe_allow_html=True)
            ca, cb = st.columns(2)
            with ca:
                if st.button("🚫 İptal Et", use_container_width=True, key=f"ip_{k}"):
                    abonelik_iptal_et(k); st.warning("İptal edildi."); time.sleep(1.5); st.rerun()
            with cb:
                if st.button("🗑️ Sil", use_container_width=True, key=f"ks_{k}"):
                    st.session_state.sil_onay_kadi = k
            if st.session_state.sil_onay_kadi == k:
                st.warning(f"⚠️ **{k}** kullanıcısını silmek istediğinizden emin misiniz?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Evet, Sil", key=f"yes_{k}", use_container_width=True, type="primary"):
                        kullanici_sil(k); st.session_state.sil_onay_kadi = None
                        st.success("Silindi."); time.sleep(1.5); st.rerun()
                with c2:
                    if st.button("❌ Vazgeç", key=f"no_{k}", use_container_width=True):
                        st.session_state.sil_onay_kadi = None; st.rerun()
            st.markdown("")
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="abg"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: ADMIN BİLDİRİMLER
# ==========================================
elif st.session_state.sayfa == "admin_bildirimler":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>📬 Bildirimler</h1>", unsafe_allow_html=True)
    bd = bildirimler_yukle()
    if not bd: st.info("ℹ️ Bildirim yok.")
    else:
        for b in sorted(bd, key=lambda x: x.get("tarih", ""), reverse=True):
            bid = b.get("id"); tip = b.get("tip", "diger")
            tb = BILDIRIM_TIPLERI.get(tip, BILDIRIM_TIPLERI["diger"])
            durum = b.get("durum", "okunmadi")
            border = "#22c55e" if durum == "okunmadi" else "#94a3b8"
            st.markdown(f'''<div class="fa-bildirim {tb['sinif']}" style="border-left-color:{border};"><div class="fa-bildirim-ttl">{tb['ikon']} {tb['isim']} — <b>{_e(b.get('kullanici', '?'))}</b> {"🆕" if durum == "okunmadi" else ""}</div><div class="fa-bildirim-msg"><b>Konu:</b> {_e(b.get('konu', ''))}<br>{_e(b.get('mesaj', ''))}</div><div class="fa-bildirim-meta">📅 {_e(b.get('tarih', '?'))}</div></div>''', unsafe_allow_html=True)
            if b.get("cevap"): st.info(f"💬 Cevabın: {b['cevap']}")
            with st.expander("💬 Cevapla / Sil"):
                yanit = st.text_area("Yanıtın", value=b.get("cevap", ""), key=f"cy_{bid}")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("💬 Kaydet", key=f"kaydet_{bid}", use_container_width=True, type="primary"):
                        bildirim_guncelle(bid, cevap=yanit, durum="okundu")
                        st.success("Kaydedildi."); time.sleep(1); st.rerun()
                with c2:
                    if st.button("✅ Okundu", key=f"ok_{bid}", use_container_width=True):
                        bildirim_guncelle(bid, durum="okundu"); st.rerun()
                with c3:
                    if st.button("🗑️ Sil", key=f"sil_{bid}", use_container_width=True):
                        bildirim_sil(bid); st.rerun()
            st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="bdg"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: KULLANICI BİLDİRİM
# ==========================================
elif st.session_state.sayfa == "kullanici_bildirim":
    if not uye_mi(): st.error("❌ Giriş yap."); st.stop()
    st.markdown("<h1>📬 Bildirim Gönder</h1>", unsafe_allow_html=True)
    st.caption("İptal talebi, şikayet, görüş ve önerilerini buradan iletebilirsin.")
    with st.form("bildirim_form"):
        tip = st.selectbox("Kategori", options=list(BILDIRIM_TIPLERI.keys()), format_func=lambda x: f"{BILDIRIM_TIPLERI[x]['ikon']} {BILDIRIM_TIPLERI[x]['isim']}")
        konu = st.text_input("Konu", placeholder="Kısa başlık...")
        mesaj = st.text_area("Mesaj", placeholder="Detaylı açıklamanı yaz...", height=150)
        c1, c2 = st.columns(2)
        with c1: gb = st.form_submit_button("📤 Gönder", use_container_width=True, type="primary")
        with c2: gb2 = st.form_submit_button("⬅️ Geri", use_container_width=True)
        if gb:
            if not konu.strip() or not mesaj.strip(): st.error("❌ Konu ve mesaj gerekli.")
            else:
                bildirim_ekle(uye_adi(), tip, konu.strip(), mesaj.strip())
                st.success("✅ Bildirimin gönderildi!")
                time.sleep(2); st.rerun()
        if gb2: st.session_state.sayfa = "giris"; st.rerun()
    st.divider()
    st.markdown("### 📋 Gönderdiğin Bildirimler")
    bl = kullanici_bildirimleri(uye_adi())
    if not bl: st.info("Henüz bildirim yok.")
    else:
        for b in sorted(bl, key=lambda x: x.get("tarih", ""), reverse=True):
            tip = b.get("tip", "diger"); tb = BILDIRIM_TIPLERI.get(tip, BILDIRIM_TIPLERI["diger"])
            st.markdown(f'''<div class="fa-bildirim {tb['sinif']}"><div class="fa-bildirim-ttl">{tb['ikon']} {tb['isim']} — {b.get('durum', '?')}</div><div class="fa-bildirim-msg"><b>Konu:</b> {_e(b.get('konu', ''))}<br>{_e(b.get('mesaj', ''))}</div><div class="fa-bildirim-meta">📅 {_e(b.get('tarih', '?'))}</div></div>''', unsafe_allow_html=True)
            if b.get("cevap"):
                st.markdown(f'<div class="fa-card fa-pos"><div class="fa-ttl">💬 Admin Cevabı</div><div class="fa-mut">{_e(b["cevap"])}</div></div>', unsafe_allow_html=True)
            st.divider()


# ==========================================
# SAYFA: GELECEK MAÇLAR (ADMİN)
# ==========================================
elif st.session_state.sayfa == "gelecek_admin":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    gel = st.session_state.gelecek_analizler
    toplam_g = len(gel)

    st.markdown("### 💾 Yedekleme")
    c1, c2 = st.columns(2)
    with c1:
        json_str2 = json.dumps(st.session_state.gelecek_analizler, ensure_ascii=False, indent=2)
        st.download_button(
            label=f"📥 Geleceği İndir ({toplam_g} maç)",
            data=json_str2,
            file_name=f"gelecek_{toplam_g}mac.json",
            mime="application/json",
            use_container_width=True,
            key="ind_gelecek"
        )
    with c2:
        yuk2 = st.file_uploader("📤 Geleceği Yükle (JSON)", type=["json"], key="yuk_gelecek")
        if yuk2 is not None:
            try:
                veri2 = json.loads(yuk2.read().decode("utf-8"))
                if isinstance(veri2, list):
                    st.session_state.gelecek_analizler = veri2
                    gelecek_kaydet(veri2)
                    st.success(f"✅ {len(veri2)} maç yüklendi!")
                    st.rerun()
                else:
                    st.error("❌ Dosya formatı hatalı.")
            except Exception as e:
                st.error(f"❌ Hata: {e}")
    st.divider()

    if not gel:
        st.info("ℹ️ Gelecek maç yok. Admin ana sayfadan maç çekebilirsin.")
    else:
        sirali = sorted(enumerate(gel), key=lambda x: saat_sirala_anahtari(x[1]))
        for idx, g in sirali:
            v = g["veri"]; te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
            ulke = v.get("ulke", ""); saat = v.get("saat", ""); tarih = v.get("tarih", "")
            try: a = analiz_hesapla(v); le = a["lam_ev"]; ld = a["lam_dep"]
            except Exception: le = ld = 0
            st.markdown(mac_karti(te, td, False, 0, 0, le, ld, saat, ulke, tarih), unsafe_allow_html=True)
            th = mac_tahmin_karti(v, g)
            if th: st.markdown(th, unsafe_allow_html=True)
            c1, c2 = st.columns([5, 1])
            with c1:
                if st.button("🔍 Detay", use_container_width=True, key=f"gmac_{idx}"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True; st.session_state.gelecekten_gelindi = True
                    st.session_state.aktif_gelecek_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
            with c2:
                if st.button("🗑️", key=f"gsil_{idx}"):
                    if st.session_state.tek_silme_gelecek == idx: st.session_state.tek_silme_gelecek = None
                    else: st.session_state.tek_silme_gelecek = idx
                    st.rerun()
            if st.session_state.tek_silme_gelecek == idx:
                st.warning(f"⚠️ **{te} vs {td}** silinsin mi?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Sil", key=f"ge_{idx}", use_container_width=True, type="primary"):
                        st.session_state.gelecek_analizler.pop(idx)
                        gelecek_kaydet(st.session_state.gelecek_analizler)
                        st.session_state.tek_silme_gelecek = None; st.rerun()
                with c2:
                    if st.button("❌ İptal", key=f"gh_{idx}", use_container_width=True):
                        st.session_state.tek_silme_gelecek = None; st.rerun()
            st.divider()

    st.divider()
    if st.button("🗑️ Tüm Geleceği Temizle", use_container_width=True, key="temizle_gel"):
        st.session_state.silme_onay_gelecek = True; st.rerun()
    if st.session_state.get("silme_onay_gelecek"):
        st.warning("⚠️ Tüm gelecek silinecek. Emin misin?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Evet, Sil", key="sil_gel_evet", use_container_width=True, type="primary"):
                st.session_state.gelecek_analizler = []
                try:
                    if os.path.exists(GELECEK_DOSYA): os.remove(GELECEK_DOSYA)
                except Exception: pass
                st.session_state.silme_onay_gelecek = False
                st.session_state.tek_silme_gelecek = None
                st.rerun()
        with c2:
            if st.button("❌ İptal", key="sil_gel_iptal", use_container_width=True):
                st.session_state.silme_onay_gelecek = False; st.rerun()

    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gg_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: GEÇMİŞ MAÇLAR
# ==========================================
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gc = st.session_state.gecmis_analizler; top = len(gc)

    if admin_mi():
        st.markdown("### 💾 Yedekleme")
        c1, c2 = st.columns(2)
        with c1:
            json_str = json.dumps(st.session_state.gecmis_analizler, ensure_ascii=False, indent=2)
            st.download_button(
                label=f"📥 Geçmişi İndir ({top} maç)",
                data=json_str,
                file_name=f"gecmis_{top}mac.json",
                mime="application/json",
                use_container_width=True,
                key="ind_gecmis"
            )
        with c2:
            yuk = st.file_uploader("📤 Geçmişi Yükle (JSON)", type=["json"], key="yuk_gecmis")
            if yuk is not None:
                try:
                    veri = json.loads(yuk.read().decode("utf-8"))
                    if isinstance(veri, list):
                        st.session_state.gecmis_analizler = veri
                        gecmis_kaydet(veri)
                        st.success(f"✅ {len(veri)} maç yüklendi!")
                        st.rerun()
                    else:
                        st.error("❌ Dosya formatı hatalı (liste bekleniyor).")
                except Exception as e:
                    st.error(f"❌ Hata: {e}")
        st.divider()

    if top == 0:
        st.info("Henüz kayıt yok.")
    else:
        modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ")
        st.divider()
        st.markdown(f"### 📋 Toplam: {top} maç")
        for i, g in enumerate(reversed(gc)):
            idx = len(gc) - 1 - i; v = g["veri"]
            te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
            se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
            st.markdown(mac_karti(te, td, True, se, sd, 0, 0, v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
            th = mac_tahmin_karti(v, g)
            if th: st.markdown(th, unsafe_allow_html=True)
            if admin_mi():
                c1, c2 = st.columns([5, 1])
                with c1:
                    if st.button("🔍 Detay", use_container_width=True, key=f"mac_{idx}"):
                        st.session_state.form_verileri = copy.deepcopy(v)
                        st.session_state.kayit_yapildi = True; st.session_state.gecmisten_gelindi = True
                        st.session_state.aktif_kayit_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
                with c2:
                    if st.button("🗑️", key=f"sil_{idx}"):
                        if st.session_state.tek_silme_onay == idx: st.session_state.tek_silme_onay = None
                        else: st.session_state.tek_silme_onay = idx
                        st.rerun()
                if st.session_state.tek_silme_onay == idx:
                    st.warning(f"⚠️ **{te} vs {td}** silinsin mi?")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅ Sil", key=f"ev_{idx}", use_container_width=True, type="primary"):
                            st.session_state.gecmis_analizler.pop(idx)
                            gecmis_kaydet(st.session_state.gecmis_analizler)
                            st.session_state.tek_silme_onay = None; st.rerun()
                    with c2:
                        if st.button("❌ İptal", key=f"hh_{idx}", use_container_width=True):
                            st.session_state.tek_silme_onay = None; st.rerun()
            else:
                if st.button("🔍 Detay", use_container_width=True, key=f"mac_{idx}"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True; st.session_state.gecmisten_gelindi = True
                    st.session_state.aktif_kayit_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
            st.divider()

    if admin_mi():
        st.divider()
        if st.button("🗑️ Tüm Geçmişi Temizle", use_container_width=True, key="temizle_g"):
            st.session_state.silme_onay = True; st.rerun()
        if st.session_state.silme_onay:
            st.warning("⚠️ Tüm geçmiş silinecek. Emin misin?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Evet, Sil", key="sil_g_evet", use_container_width=True, type="primary"):
                    st.session_state.gecmis_analizler = []
                    try:
                        if os.path.exists(GECMIS_DOSYA): os.remove(GECMIS_DOSYA)
                    except Exception: pass
                    st.session_state.silme_onay = False
                    st.session_state.tek_silme_onay = None
                    st.rerun()
            with c2:
                if st.button("❌ İptal", key="sil_g_iptal", use_container_width=True):
                    st.session_state.silme_onay = False; st.rerun()

    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gc_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: BACKTEST
# ==========================================
elif st.session_state.sayfa == "backtest":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>🔬 Backtest</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        s1x2 = st.checkbox("1X2", key="bt_1x2")
        e1 = st.slider("1 eşiği", 0, 100, 55, key="sl_bt_1")
        ex = st.slider("X eşiği", 0, 100, 55, key="sl_bt_x")
        e2 = st.slider("2 eşiği", 0, 100, 55, key="sl_bt_2")
    with c2:
        skv = st.checkbox("KG Var", key="bt_kg_var"); ekv = st.slider("KG Var eşiği", 0, 100, 70, key="sl_kg_var")
        sky = st.checkbox("KG Yok", key="bt_kg_yok"); eky = st.slider("KG Yok eşiği", 0, 100, 70, key="sl_kg_yok")
    with c3:
        su = st.checkbox("Üst 2.5", key="bt_ust"); eu = st.slider("Üst eşiği", 0, 100, 70, key="sl_ust")
        sa = st.checkbox("Alt 2.5", key="bt_alt"); ea = st.slider("Alt eşiği", 0, 100, 70, key="sl_alt")
    if st.button("🚀 TEST", use_container_width=True, type="primary"):
        with st.spinner("Test..."):
            sec = {"1x2": s1x2, "kg_var": skv, "kg_yok": sky, "ust": su, "alt": sa}
            esk = {"esik_1": float(e1), "esik_x": float(ex), "esik_2": float(e2), "kg_var": float(ekv), "kg_yok": float(eky), "ust": float(eu), "alt": float(ea)}
            if not any(sec.values()): st.warning("Market seç.")
            else:
                s, d = backtest_hesapla(st.session_state.gecmis_analizler, sec, esk)
                st.session_state.bt_sonuc = s; st.session_state.bt_detaylar = d; st.session_state.bt_sec = sec
    if st.session_state.bt_sonuc and st.session_state.get("bt_sec"):
        for key, b in [("1x2", "1X2"), ("kg_var", "KG Var"), ("kg_yok", "KG Yok"), ("ust", "Üst"), ("alt", "Alt")]:
            if st.session_state.bt_sec.get(key):
                dd = st.session_state.bt_sonuc[key]; tt = dd["dogru"] + dd["yanlis"]
                if tt > 0: st.markdown(f"**{b}:** %{dd['dogru']/tt*100:.1f} ({dd['dogru']}/{tt})")
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="btg"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: AYARLAR
# ==========================================
elif st.session_state.sayfa == "ayarlar":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>⚙️ Ayarlar</h1>", unsafe_allow_html=True)
    mv = st.session_state.esikler.copy()
    st.markdown("### 🏦 Ödeme")
    c1, c2 = st.columns(2)
    with c1: yiban = st.text_input("IBAN", value=mv.get("iban", "TR00 0000 0000 0000 0000 0000 00"))
    with c2: yhs = st.text_input("Hesap Sahibi", value=mv.get("hesap_sahibi", ""))
    st.markdown("### 💰 Fiyatlar")
    c1, c2, c3 = st.columns(3)
    with c1: yfh = st.number_input("Haftalık", min_value=1.0, value=float(mv.get("fiyat_haftalik", 49.0)), step=10.0, key="ay_fh")
    with c2: yfa = st.number_input("Aylık", min_value=1.0, value=float(mv.get("fiyat_aylik", 149.0)), step=10.0, key="ay_fa")
    with c3: yfy = st.number_input("Yıllık", min_value=1.0, value=float(mv.get("fiyat_yillik", 999.0)), step=10.0, key="ay_fy")
    if yfa > 0 and yfy < yfa * 12:
        st.caption(f"💡 Yıllıkta %{int((1 - yfy / (yfa * 12)) * 100)} indirim")
    st.markdown("### 🔓 Ücretsiz Kota")
    yk = st.number_input("Kaç maç ücretsiz?", 0, 50, int(mv.get("ucretsiz_kotasi", 3)), 1, key="ay_kota")
    st.markdown("### 🎯 Eşikler")
    c1, c2, c3 = st.columns(3)
    with c1: ye1 = st.slider("1 %", 0, 100, int(mv.get("esik_1", 55.0)), 1, key="ay_esik_1")
    with c2: yex = st.slider("X %", 0, 100, int(mv.get("esik_x", 55.0)), 1, key="ay_esik_x")
    with c3: ye2 = st.slider("2 %", 0, 100, int(mv.get("esik_2", 55.0)), 1, key="ay_esik_2")
    c4, c5 = st.columns(2)
    with c4: yu = st.slider("Üst %", 0, 100, int(mv["ust"]), 1, key="ay_ust")
    with c5: ya = st.slider("Alt %", 0, 100, int(mv["alt"]), 1, key="ay_alt")
    c6, c7 = st.columns(2)
    with c6: ykv = st.slider("KG Var %", 0, 100, int(mv["kg_var"]), 1, key="ay_kg_var")
    with c7: yky = st.slider("KG Yok %", 0, 100, int(mv["kg_yok"]), 1, key="ay_kg_yok")
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💾 Kaydet", use_container_width=True, type="primary"):
            y = dict(mv); y.update({"iban": yiban, "hesap_sahibi": yhs, "fiyat_haftalik": float(yfh), "fiyat_aylik": float(yfa), "fiyat_yillik": float(yfy), "ucretsiz_kotasi": int(yk), "esik_1": float(ye1), "esik_x": float(yex), "esik_2": float(ye2), "ust": float(yu), "alt": float(ya), "kg_var": float(ykv), "kg_yok": float(yky)})
            st.session_state.esikler = y; ayarlar_kaydet(y); st.success("✅ Kaydedildi!")
    with c2:
        if st.button("🔄 Sıfırla", use_container_width=True):
            v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "iban": "TR00 0000 0000 0000 0000 0000 00", "hesap_sahibi": "ADINIZ SOYADINIZ", "fiyat_haftalik": 49.0, "fiyat_aylik": 149.0, "fiyat_yillik": 999.0, "ucretsiz_kotasi": 3}
            st.session_state.esikler = v; ayarlar_kaydet(v); st.rerun()
    with c3:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="ayg"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: MANUEL GİRİŞ
# ==========================================
elif st.session_state.sayfa == "manuel_giris":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>📝 Eksik Alanlar</h1>", unsafe_allow_html=True)
    st.warning(f"Metinden çıkarılamayan **{len(st.session_state.manuel_bekleyen)}** alan:")
    v = st.session_state.form_verileri
    with st.form("mf"):
        yd = {}
        for a in st.session_state.manuel_bekleyen:
            if a in MANUEL_ALANLAR:
                st.markdown(f"**{a}**")
                for (k, e, t, vs) in MANUEL_ALANLAR[a]:
                    mv = v.get(k, vs)
                    if t == "int":
                        val = st.number_input(e, value=int(mv) if mv else int(vs), min_value=1, max_value=100, step=1, key=f"mk_{k}")
                        yd[k] = int(val)
                    elif t == "float":
                        val = st.number_input(e, value=float(mv) if mv else float(vs), min_value=0.0, step=0.1, key=f"mk_{k}")
                        yd[k] = float(val)
                    else:
                        val = st.text_input(e, value=str(mv) if mv else "", key=f"mk_{k}")
                        yd[k] = val
        c1, c2 = st.columns(2)
        with c1: kb = st.form_submit_button("✅ Kaydet", use_container_width=True, type="primary")
        with c2: ab = st.form_submit_button("⏭️ Atla", use_container_width=True)
        if kb or ab:
            if kb: st.session_state.form_verileri.update(yd)
            st.session_state.manuel_bekleyen = []
            st.session_state.sayfa = "sonuc"; st.rerun()
    if st.button("⬅️ Geri"): st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: SONUÇ
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri; a = analiz_hesapla(v)
    te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
    sb = v.get("skor_belli", False); se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    st.markdown(mac_karti(te, td, sb, se, sd, a["lam_ev"], a["lam_dep"], v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)

    # === AI YORUMU (Okunan Veriler yerine) ===
    ai_html = ai_yorum_paneli(v, a)
    if ai_html:
        st.markdown(ai_html, unsafe_allow_html=True)

    st.divider()
    st.markdown("## 🏆 FİNAL ÖNERİ")
    s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    e1 = esik_1x2_al(s1); p1 = y1 >= e1
    im = {"1": "1 (Ev)", "X": "X (Beraberlik)", "2": "2 (Dep)"}
    st.markdown(oneri_karti("🎯 1X2", im[s1], y1, e1, p1, f"1:%{a['p1']:.1f} X:%{a['px']:.1f} 2:%{a['p2']:.1f}"), unsafe_allow_html=True)
    if a["ust_25"] >= a["alt_25"]: gs = "Üst 2.5"; gy = a["ust_25"]; ge_ = esik_al("ust")
    else: gs = "Alt 2.5"; gy = a["alt_25"]; ge_ = esik_al("alt")
    st.markdown(oneri_karti("⚽ Gol", gs, gy, ge_, gy >= ge_, f"Üst:%{a['ust_25']:.1f} Alt:%{a['alt_25']:.1f}"), unsafe_allow_html=True)
    if a["kg_var_model"] >= a["kg_yok_model"]: ks = "KG Var"; ky = a["kg_var_model"]; ke = esik_al("kg_var")
    else: ks = "KG Yok"; ky = a["kg_yok_model"]; ke = esik_al("kg_yok")
    st.markdown(oneri_karti("🤝 KG", ks, ky, ke, ky >= ke, f"Var:%{a['kg_var_model']:.1f} Yok:%{a['kg_yok_model']:.1f}"), unsafe_allow_html=True)

    if st.session_state.gelecekten_gelindi and admin_mi():
        ig = st.session_state.aktif_gelecek_idx
        if ig is not None and 0 <= ig < len(st.session_state.gelecek_analizler):
            st.divider(); st.markdown("### 📥 Sonuç Gir")
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1: yse = st.number_input("Ev", 0, 20, 0, 1, key=f"gse_{ig}")
            with c2: ysd = st.number_input("Dep", 0, 20, 0, 1, key=f"gsd_{ig}")
            with c3:
                st.markdown(""); st.markdown("")
                if st.button("📥 Taşı", key=f"ts_{ig}", use_container_width=True, type="primary"):
                    k = st.session_state.gelecek_analizler[ig]
                    k["veri"]["skor_ev"] = int(yse); k["veri"]["skor_dep"] = int(ysd); k["veri"]["skor_belli"] = True
                    yd = sonuc_hesapla(k)
                    if yd: k["dogruluk"] = yd
                    st.session_state.gecmis_analizler.append(k)
                    st.session_state.gelecek_analizler.pop(ig)
                    gecmis_kaydet(st.session_state.gecmis_analizler); gelecek_kaydet(st.session_state.gelecek_analizler)
                    st.session_state.gelecekten_gelindi = False; st.session_state.aktif_gelecek_idx = None
                    st.session_state.sayfa = "giris"; st.rerun()

    km = (a["ust_25"] >= esik_al("ust") and a["ust_25"] >= a["alt_25"]) or (a["alt_25"] >= esik_al("alt") and a["alt_25"] >= a["ust_25"]) or p1
    if not st.session_state.kayit_yapildi and admin_mi():
        yk = kayit_olustur(v, a)
        if sb: st.session_state.gecmis_analizler.append(yk); gecmis_kaydet(st.session_state.gecmis_analizler)
        elif km: st.session_state.gelecek_analizler.append(yk); gelecek_kaydet(st.session_state.gelecek_analizler)
        st.session_state.kayit_yapildi = True
    if st.button("🔄 Yeni", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI); st.session_state.sayfa = "giris"; st.rerun()
