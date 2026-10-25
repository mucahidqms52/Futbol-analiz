import streamlit as st
import math
import copy
import re
import random
import json
import os
import html as _html
import time
import threading
import requests
import hashlib
import secrets as _secrets
import psycopg2
from psycopg2.extras import Json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import warnings
import extra_streamlit_components as stx

try:
    import bcrypt
    BCRYPT_VAR = True
except ImportError:
    BCRYPT_VAR = False

logging.getLogger('streamlit').setLevel(logging.ERROR)
logging.getLogger('streamlit.runtime.scriptrunner.script_run_context').setLevel(logging.ERROR)
logging.getLogger('streamlit.runtime.scriptrunner').setLevel(logging.ERROR)
warnings.filterwarnings("ignore", message=".*CachedWidgetWarning.*")
warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")

YASAL_METIN = """
# ⚖️ KULLANIM ŞARTLARI VE SORUMLULUK REDDİ

**Yürürlük Tarihi:** Hizmete kayıt olduğunuz tarih itibariyle geçerlidir.

---

## 1. TARAFLAR VE KAPSAM

Bu Kullanım Şartları, **"Futbol Analiz Pro"** (bundan sonra **"Uygulama"** veya **"Hizmet"** olarak anılacaktır) ile bu hizmete kayıt olan kullanıcı (bundan sonra **"Kullanıcı"** olarak anılacaktır) arasında akdedilmiştir. Kullanıcı, Uygulama'ya kayıt olmak, giriş yapmak veya herhangi bir şekilde hizmeti kullanmakla bu şartları **okuduğunu, anladığını ve kabul ettiğini** beyan ve taahhüt eder.

---

## 2. HİZMETİN TANIMI

Uygulama, futbol maçlarına ilişkin olarak **geçmiş istatistiklere dayalı matematiksel ve istatistiksel analizler** üreterek kullanıcıya **bilgilendirme amaçlı tahminler** sunar.

**KESİNLİKLE BELİRTİLİR Kİ:**

- Sunulan içerikler **bahis, yatırım, finansal veya hukuki tavsiye** niteliği taşımaz.
- Uygulama, **hiçbir bahis sitesiyle ortaklık, iş ortaklığı, bayilik veya acentelik ilişkisi içinde değildir.**
- Uygulama, **kullanıcı adına bahis oynamaz, bahis kuponu düzenlemez veya bahis hizmeti sunmaz.**
- Uygulama bir **sosyal medya, sohbet veya para transfer platformu değildir.**

---

## 3. YAŞ SINIRI VE EHLİYET

Uygulama'yı kullanabilmek için:

- **18 (on sekiz) yaşından büyük olmanız**,
- **Fiil ehliyetine sahip olmanız** (TMK m.10 ve devamı),
- **Yasal olarak bahis oynamanın yasak olmadığı bir ülkede bulunmanız** gerekmektedir.

Kullanıcı, bu şartları sağladığını beyan eder. Aksi halde doğacak her türlü hukuki, cezai ve idari sorumluluk **münhasıran Kullanıcı'ya aittir.**

---

## 4. HİZMETİN "OLDUĞU GİBİ" SUNULMASI

Uygulama, **"AS IS" (olduğu gibi)** ve **"AS AVAILABLE" (mevcut olduğu şekilde)** esasına göre sunulmaktadır. Uygulama, aşağıdakiler dahil ancak bunlarla sınırlı olmamak üzere **hiçbir açık veya zımni garanti vermez:**

- Hizmetin kesintisiz, hatasız, virüssüz veya güvenli olacağı,
- Sunulan tahminlerin **doğru, güncel, eksiksiz veya güvenilir** olacağı,
- Hizmetin **belirli bir amaca uygun** olacağı,
- Hizmet sonucunda **herhangi bir kazanç elde edileceği.**

---

## 5. TAHMİN GARANTİSİ YOKTUR

**BU HİZMETTE SUNULAN TÜM TAHMİN, ANALİZ, İSTATİSTİK VE YORUMLAR;**

- Geçmiş verilerin matematiksel modellenmesine dayanır,
- **Gelecektek sonuçları garanti etmez**,
- **Doğruluk oranı %100 değildir ve hiçbir zaman olamaz**,
- **Kayıp veya kazanç garantisi içermez.**

**Kullanıcı, hiçbir tahmine güvenerek hareket etmemesi, bahis oynamaması ve maddi kayba uğramaması gerektiğini kabul eder.** Tahminler yalnızca **eğitim ve bilgi amaçlıdır.**

---

## 6. SORUMLULUĞUN SINIRLANDIRILMASI VE İBRA

Kullanıcı, Uygulama'yı kullanması nedeniyle veya kullanımıyla bağlantılı olarak doğrudan veya dolaylı olarak ortaya çıkabilecek;

- Maddi ve manevi zararlar,
- Kâr kaybı, veri kaybı, itibar kaybı,
- Üçüncü kişilerden gelecek her türlü talep, dava, icra takibi ve cezai sorumluluk,
- Yasadışı bahis, kumar, dolandırıcılık veya benzeri suçlardan doğan her türlü hukuki ve cezai yaptırım,

için **Uygulama'yı işleten gerçek/tüzel kişiyi, geliştiricileri, iş ortaklarını, tedarikçileri ve çalışanlarını tamamen ibra ettiğini** kabul, beyan ve taahhüt eder.

**Uygulama, hiçbir durumda Kullanıcı'nın uğradığı zararlardan sorumlu tutulamaz.** Kullanıcı, olası bir uyuşmazlıkta Uygulama'ya karşı **hiçbir tazminat, iade, cezai şart veya faiz talebinde bulunamaz.**

---

## 7. YASADIŞI BAHİS VE KUMAR UYARISI

Türkiye Cumhuriyeti mevzuatı uyarınca **yasadışı bahis oynamak, oynatmak, yer temin etmek, para transferi yapmak ve reklamını yapmak suçtur** (7258 sayılı Kanun ve ilgili mevzuat).

**KULLANICI:**

- Bu Uygulama'yı **yasadışı bahis oynamak için kullanamaz**,
- Uygulama'da sunulan tahminleri **yasadışı bahis sitelerine aktaramaz, kopyalayamaz, dağıtamaz**,
- Uygulama'yı **kumar bağımlılığını teşvik edici** bir şekilde kullanamaz.

Bu kurala aykırılık tespit edilmesi halinde **Kullanıcı'nın üyeliği derhal iptal edilir ve yasal mercilere bildirilir.**

---

## 8. ÖDEME, ABONELİK VE İADE KOŞULLARI

**Ödeme Yöntemi:** Ödemeler yalnızca **havale / EFT** yoluyla yapılır.

**Abonelik Süreleri:** Haftalık ve Aylık olmak üzere iki paket sunulmaktadır.

**Abonelik Aktivasyonu:** Ödeme yapıldıktan sonra Kullanıcı'nın **"Ödeme Yaptım"** bildirimi üzerine, ödeme kontrol edilerek **manuel olarak** aktive edilir. Aktivasyon **birkaç saat ile 24 saat** arasında tamamlanır.

**İADE VE İPTAL:**

- **Üyelik iptali ve iade talepleriniz için lütfen uygulama içindeki "Bildirim" bölümünden bizimle iletişime geçin.**
- Talebiniz değerlendirilecek ve tarafınıza en kısa sürede dönüş yapılacaktır.

---

## 9. ABONELİK İPTALİ

- Kullanıcı, aboneliğini **Uygulama içindeki "Bildirim"** bölümünden iptal talebi oluşturabilir.
- **Üyelik iptali ve iade talepleriniz için lütfen uygulama içindeki "Bildirim" bölümünden bizimle iletişime geçin.**

---

## 10. KİŞİSEL VERİLERİN KORUNMASI (KVKK)

6698 sayılı KVKK'ya uygun olarak:

- **Kullanıcı adı, şifre (hash'lenmiş), ödeme bildirim bilgileri** toplanır.
- Veriler **yalnızca hizmetin ifası ve abonelik yönetimi** amacıyla kullanılır.
- Veriler **hiçbir üçüncü taraf ile paylaşılmaz, satılmaz.**
- Şifreler **tek yönlü hash** ile saklanır, geri çevrilemez.
- Kullanıcı **dilediği zaman hesabını sildirebilir**; veriler **7 iş günü içinde** silinir.

---

## 11. FİKRİ MÜLKİYET

Uygulama'daki **tüm analizler, modeller, algoritmalar, tahminler, tasarımlar, kodlar, logolar ve metinler** telif hakkı ile korunmaktadır. Kullanıcı bunları **kopyalayamaz, dağıtamaz, satamaz, değiştiremez**.

---

## 12. HİZMET DEĞİŞİKLİKLERİ

Uygulama, önceden bildirimde bulunmaksızın **hizmeti değiştirme, askıya alma, sonlandırma, fiyatları güncelleme, kullanım şartlarını değiştirme, kullanıcı hesaplarını askıya alma** hakkını saklı tutar.

---

## 13. UYUŞMAZLIK VE YETKİLİ MAHKEME

Bu şartlardan doğan uyuşmazlıklarda **Türkiye Cumhuriyeti hukuku** uygulanır. Yetkili mahkemeler, Uygulama'yı işleten kişinin yerleşim yeri mahkemeleridir.

---

## 14. YÜRÜRLÜK VE KABUL

Kullanıcı, bu şartları **okuduğunu, anladığını ve kabul ettiğini** beyan eder. Kayıt işlemini tamamlamak veya abonelik satın almak, bu şartların kabulü anlamına gelir.

---

## 15. İLETİŞİM

Her türlü soru, görüş, şikayet, **iptal ve iade** talepleri için Uygulama içindeki **"Bildirim"** bölümünden iletişime geçebilirsiniz.

---

**SON SÖZ:** Bu uygulama **SADECE bilgilendirme ve analiz amaçlıdır**. Bahis oynamak **yasal risk**, **maddi kayıp riski** ve **bağımlılık riski** içerir. **YEDAM: 115**
"""

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

# ==========================================
# POSTGRESQL VERİ KATMANI
# ==========================================
ADMIN_KULLANICI_ADI = "admin52"


def _admin_sifre_al():
    try:
        if "ADMIN_SIFRE" in st.secrets:
            s = st.secrets["ADMIN_SIFRE"]
            if s and len(s) >= 8:
                return s
    except Exception:
        pass
    s = os.environ.get("ADMIN_SIFRE", "")
    if not s:
        st.error("🚨 **GÜVENLİK HATASI:** ADMIN_SIFRE tanımlı değil!\n\n"
                 "Lütfen Streamlit secrets (`st.secrets['ADMIN_SIFRE']`) "
                 "veya ortam değişkeni (`ADMIN_SIFRE`) olarak en az 8 karakterli "
                 "bir şifre tanımlayın. Kodda varsayılan şifre güvenlik gereği kaldırılmıştır.")
        st.stop()
    if len(s) < 8:
        st.error("🚨 **GÜVENLİK HATASI:** ADMIN_SIFRE en az 8 karakter olmalı!")
        st.stop()
    return s

ADMIN_SIFRE = _admin_sifre_al()
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "adm_" + hashlib.sha256(ADMIN_SIFRE.encode()).hexdigest()[:40])


# ===== GİRİŞ RATE LIMITING =====
_GIRIS_DENEMELERI = {}
_GIRIS_LIMIT_SAYI = 5
_GIRIS_LIMIT_PENCERE = 300
_GIRIS_LIMIT_KILIT = 900


def _giris_limiti_kontrol(kadi):
    simdi = time.time()
    k = (kadi or "").strip().lower()
    if not k: return True, 0
    kayitlar = _GIRIS_DENEMELERI.get(k, [])
    kayitlar = [t for t in kayitlar if simdi - t < _GIRIS_LIMIT_PENCERE]
    _GIRIS_DENEMELERI[k] = kayitlar
    if len(kayitlar) >= _GIRIS_LIMIT_SAYI:
        kalan = int(_GIRIS_LIMIT_KILIT - (simdi - kayitlar[-1]))
        if kalan > 0:
            return False, kalan
        _GIRIS_DENEMELERI[k] = []
    return True, 0


def _giris_denemesi_ekle(kadi):
    k = (kadi or "").strip().lower()
    if not k: return
    _GIRIS_DENEMELERI.setdefault(k, []).append(time.time())


def _giris_basarili_sil(kadi):
    k = (kadi or "").strip().lower()
    _GIRIS_DENEMELERI.pop(k, None)


def _db_baglanti():
    url = os.environ.get("DATABASE_URL", "")
    if not url:
        raise RuntimeError("DATABASE_URL ortam değişkeni tanımlı değil.")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(url, sslmode="require")


@st.cache_resource(show_spinner="Veritabanı hazırlanıyor...")
def _init_db():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS kullanicilar (kullanici_adi TEXT PRIMARY KEY, veri JSONB NOT NULL)")
            cur.execute("CREATE TABLE IF NOT EXISTS bekleyen_odemeler (kullanici_adi TEXT PRIMARY KEY, veri JSONB NOT NULL)")
            cur.execute("CREATE TABLE IF NOT EXISTS bildirimler (id BIGINT PRIMARY KEY, veri JSONB NOT NULL)")
            cur.execute("CREATE TABLE IF NOT EXISTS gecmis (id SERIAL PRIMARY KEY, veri JSONB NOT NULL)")
            cur.execute("CREATE TABLE IF NOT EXISTS gelecek (id SERIAL PRIMARY KEY, veri JSONB NOT NULL)")
            cur.execute("CREATE TABLE IF NOT EXISTS online_kullanicilar (session_id TEXT PRIMARY KEY, son_gorulme TIMESTAMP NOT NULL)")
            cur.execute("CREATE TABLE IF NOT EXISTS gunluk_ziyaretler (tarih DATE PRIMARY KEY, ziyaret_sayisi INT NOT NULL DEFAULT 0)")
            cur.execute("CREATE TABLE IF NOT EXISTS ayarlar (id INT PRIMARY KEY DEFAULT 1, veri JSONB NOT NULL, CONSTRAINT ayarlar_tek_satir CHECK (id = 1))")
        conn.commit()
    finally:
        conn.close()
    return True


try:
    _init_db()
except Exception as _db_hata:
    st.error(f"❌ Veritabanı bağlantı hatası: {_db_hata}")
    st.stop()


def _cookie_manager_al():
    try:
        return stx.CookieManager(key="fa_cookie_mgr_v1")
    except Exception:
        return None

_cookie_mgr = _cookie_manager_al()


def _token_uret(): return _secrets.token_hex(32)


def _token_hash(token):
    return hashlib.sha256(("fa_tok_" + token).encode("utf-8")).hexdigest()


def _token_dogrula(token, kayitli_hash):
    if not token or not kayitli_hash: return False
    return _secrets.compare_digest(_token_hash(token), kayitli_hash)


def _cerez_oku():
    if _cookie_mgr is None: return {}
    try: return _cookie_mgr.get_all() or {}
    except Exception: return {}


def _cerez_yaz(ad, deger):
    if _cookie_mgr is None: return
    try: _cookie_mgr.set(ad, deger, expires_at=datetime.now() + timedelta(days=30))
    except Exception: pass


def _cerez_sil(ad):
    if _cookie_mgr is None: return
    try: _cookie_mgr.delete(ad)
    except Exception: pass


def _otomatik_giris_dene():
    if st.session_state.get("aktif_kullanici") or st.session_state.get("rol") == "admin": return
    cerezler = _cerez_oku()
    if not cerezler: return
    token = cerezler.get("fa_token"); kadi = cerezler.get("fa_kadi")
    if not token or not kadi: return
    if kadi == ADMIN_KULLANICI_ADI:
        if _secrets.compare_digest(token, ADMIN_TOKEN):
            st.session_state.rol = "admin"
            st.session_state._otomatik_giris_yapildi = True
        return
    try:
        kullanicilar = kullanicilar_yukle()
        k = kullanicilar.get(kadi)
        if k and _token_dogrula(token, k.get("oturum_token") or ""):
            st.session_state.aktif_kullanici = kadi
            st.session_state._otomatik_giris_yapildi = True
    except Exception: pass


@st.cache_data(ttl=30, show_spinner=False)
def _online_durum_guncelle(session_id):
    online_heartbeat(session_id); return online_say()

if "_session_id" not in st.session_state: st.session_state._session_id = _secrets.token_hex(16)
try: _ONLINE_SAYI = _online_durum_guncelle(st.session_state._session_id)
except Exception: _ONLINE_SAYI = 0


if st.session_state.get("rol") == "admin":
    st.markdown(f'''<div style="text-align:center; margin:0 0 10px 0;"><span style="display:inline-block; background:rgba(34,197,94,0.15); border:1px solid rgba(34,197,94,0.5); border-radius:99px; padding:4px 14px; font-size:0.75rem; font-weight:800; color:#22c55e; letter-spacing:0.5px;">🟢 {_ONLINE_SAYI} KİŞİ ONLINE</span></div>''', unsafe_allow_html=True)


def kullanicilar_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT kullanici_adi, veri FROM kullanicilar")
            return {row[0]: row[1] for row in cur.fetchall()}
    finally: conn.close()


def kullanicilar_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM kullanicilar")
            for k, veri in v.items():
                cur.execute("INSERT INTO kullanicilar (kullanici_adi, veri) VALUES (%s, %s)", (k, Json(veri)))
        conn.commit()
    finally: conn.close()


def bekleyen_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT kullanici_adi, veri FROM bekleyen_odemeler")
            return {row[0]: row[1] for row in cur.fetchall()}
    finally: conn.close()


def bekleyen_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM bekleyen_odemeler")
            for k, veri in v.items():
                cur.execute("INSERT INTO bekleyen_odemeler (kullanici_adi, veri) VALUES (%s, %s)", (k, Json(veri)))
        conn.commit()
    finally: conn.close()


def bildirimler_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, veri FROM bildirimler ORDER BY id")
            return [row[1] for row in cur.fetchall()]
    finally: conn.close()


def bildirimler_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM bildirimler")
            for veri in v:
                bid = veri.get("id") or int(time.time() * 1000)
                cur.execute("INSERT INTO bildirimler (id, veri) VALUES (%s, %s)", (bid, Json(veri)))
        conn.commit()
    finally: conn.close()


def gecmis_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT veri FROM gecmis ORDER BY id")
            return [row[0] for row in cur.fetchall()]
    finally: conn.close()


def gecmis_kaydet(v):
    v = list(v)
    if len(v) > 200:
        v = v[-200:]
    try:
        if "gecmis_analizler" in st.session_state:
            st.session_state.gecmis_analizler = v
    except Exception:
        pass
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM gecmis")
            for veri in v:
                cur.execute("INSERT INTO gecmis (veri) VALUES (%s)", (Json(veri),))
        conn.commit()
    finally: conn.close()


def gelecek_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT veri FROM gelecek ORDER BY id")
            return [row[0] for row in cur.fetchall()]
    finally: conn.close()


def gelecek_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM gelecek")
            for veri in v:
                cur.execute("INSERT INTO gelecek (veri) VALUES (%s)", (Json(veri),))
        conn.commit()
    finally: conn.close()


def ayarlar_yukle():
    v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "iban": "TR00 0000 0000 0000 0000 0000 00", "hesap_sahibi": "ADINIZ SOYADINIZ", "fiyat_haftalik": 49.0, "fiyat_aylik": 149.0, "fiyat_yillik": 999.0, "ucretsiz_kotasi": 3}
    try:
        conn = _db_baglanti()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT veri FROM ayarlar WHERE id = 1")
                row = cur.fetchone()
                if row and row[0]: v.update(row[0])
        finally: conn.close()
    except Exception: pass
    return v


def ayarlar_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO ayarlar (id, veri) VALUES (1, %s) ON CONFLICT (id) DO UPDATE SET veri = EXCLUDED.veri", (Json(v),))
        conn.commit()
    finally: conn.close()


def online_heartbeat(session_id):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM online_kullanicilar WHERE session_id = %s AND son_gorulme > NOW() - INTERVAL '5 minutes'",
                (session_id,)
            )
            yeni_ziyaret = cur.fetchone() is None
            cur.execute(
                "INSERT INTO online_kullanicilar (session_id, son_gorulme) VALUES (%s, NOW()) "
                "ON CONFLICT (session_id) DO UPDATE SET son_gorulme = NOW()",
                (session_id,)
            )
            cur.execute("DELETE FROM online_kullanicilar WHERE son_gorulme < NOW() - INTERVAL '2 minutes'")
            if yeni_ziyaret:
                cur.execute(
                    "INSERT INTO gunluk_ziyaretler (tarih, ziyaret_sayisi) VALUES (CURRENT_DATE, 1) "
                    "ON CONFLICT (tarih) DO UPDATE SET ziyaret_sayisi = gunluk_ziyaretler.ziyaret_sayisi + 1"
                )
        conn.commit()
    finally: conn.close()


def gunluk_ziyaret_sayisi(tarih=None):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            if tarih is None: cur.execute("SELECT ziyaret_sayisi FROM gunluk_ziyaretler WHERE tarih = CURRENT_DATE")
            else: cur.execute("SELECT ziyaret_sayisi FROM gunluk_ziyaretler WHERE tarih = %s", (tarih,))
            row = cur.fetchone(); return row[0] if row else 0
    finally: conn.close()


def son_7_gun_ziyaretler():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT tarih, ziyaret_sayisi FROM gunluk_ziyaretler WHERE tarih >= CURRENT_DATE - INTERVAL '6 days' ORDER BY tarih DESC")
            return {str(row[0]): row[1] for row in cur.fetchall()}
    finally: conn.close()


def online_say():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM online_kullanicilar WHERE son_gorulme > NOW() - INTERVAL '2 minutes'")
            row = cur.fetchone(); return row[0] if row else 0
    finally: conn.close()


def sifre_hashle(sifre, salt=None):
    if BCRYPT_VAR:
        h = bcrypt.hashpw(sifre.encode("utf-8"), bcrypt.gensalt(rounds=12))
        return "", h.decode("utf-8")
    if salt is None: salt = _secrets.token_hex(16)
    h = hashlib.sha256((salt + sifre).encode("utf-8")).hexdigest()
    return salt, h


def sifre_dogrula(sifre, salt, kayitli_hash):
    if not kayitli_hash: return False
    if kayitli_hash.startswith("$2"):
        if not BCRYPT_VAR: return False
        try:
            return bcrypt.checkpw(sifre.encode("utf-8"), kayitli_hash.encode("utf-8"))
        except Exception:
            return False
    _, h = sifre_hashle(sifre, salt)
    return _secrets.compare_digest(h, kayitli_hash)


def kullanici_ekle(kullanici_adi, sifre):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi in kullanicilar: return False, "Bu kullanıcı adı zaten alınmış."
    salt, s_hash = sifre_hashle(sifre)
    kullanicilar[kullanici_adi] = {"salt": salt, "sifre_hash": s_hash, "kayit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"), "abonelik_bitis": None, "son_odeme": None, "son_odeme_gun": 0, "yasal_kabul_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"), "oturum_token": None}
    kullanicilar_kaydet(kullanicilar)
    return True, "Kayıt başarılı."


def kullanici_dogrula(kullanici_adi, sifre):
    kullanicilar = kullanicilar_yukle()
    k = kullanicilar.get(kullanici_adi)
    if not k: return False
    if not sifre_dogrula(sifre, k.get("salt", ""), k["sifre_hash"]):
        return False
    if BCRYPT_VAR and not k["sifre_hash"].startswith("$2"):
        try:
            yeni_salt, yeni_hash = sifre_hashle(sifre)
            k["salt"] = yeni_salt
            k["sifre_hash"] = yeni_hash
            kullanicilar[kullanici_adi] = k
            kullanicilar_kaydet(kullanicilar)
        except Exception: pass
    return True


def abonelik_aktif_mi(kullanici_adi):
    kullanicilar = kullanicilar_yukle()
    k = kullanicilar.get(kullanici_adi)
    if not k: return False
    bitis_str = k.get("abonelik_bitis")
    if not bitis_str: return False
    try: return datetime.strptime(bitis_str, "%Y-%m-%d") >= datetime.now()
    except Exception: return False


def abonelik_aktif_et(kullanici_adi, gun_sayisi):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi not in kullanicilar: return False, "Kullanıcı bulunamadı."
    k = kullanicilar[kullanici_adi]
    mevcut_bitis = None
    if k.get("abonelik_bitis"):
        try: mevcut_bitis = datetime.strptime(k["abonelik_bitis"], "%Y-%m-%d")
        except Exception: mevcut_bitis = None
    bugun = datetime.now()
    baslangic = mevcut_bitis if (mevcut_bitis and mevcut_bitis > bugun) else bugun
    yeni_bitis = baslangic + timedelta(days=int(gun_sayisi))
    k["abonelik_bitis"] = yeni_bitis.strftime("%Y-%m-%d")
    k["son_odeme"] = bugun.strftime("%Y-%m-%d %H:%M"); k["son_odeme_gun"] = int(gun_sayisi)
    kullanicilar_kaydet(kullanicilar)
    return True, yeni_bitis.strftime("%Y-%m-%d")


def abonelik_iptal_et(kullanici_adi):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi not in kullanicilar: return False
    kullanicilar[kullanici_adi]["abonelik_bitis"] = None
    kullanicilar_kaydet(kullanicilar); return True


def kullanici_sil(kullanici_adi):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi in kullanicilar:
        del kullanicilar[kullanici_adi]
        kullanicilar_kaydet(kullanicilar)
        bd = bildirimler_yukle()
        bd = [b for b in bd if b.get("kullanici") != kullanici_adi]
        bildirimler_kaydet(bd); return True
    return False


def yeni_kayit_say(saat=24):
    try:
        kl = kullanicilar_yukle(); simdi = datetime.now(); count = 0
        for k, kd in kl.items():
            kt = kd.get("kayit_tarihi", "")
            try:
                kayit = datetime.strptime(kt, "%Y-%m-%d %H:%M")
                if (simdi - kayit).total_seconds() < saat * 3600: count += 1
            except Exception: pass
        return count
    except Exception: return 0


BILDIRIM_TIPLERI = {
    "iptal": {"ikon": "🚫", "isim": "Abonelik İptal Talebi", "sinif": "fa-bildirim-iptal"},
    "sikayet": {"ikon": "⚠️", "isim": "Şikayet", "sinif": "fa-bildirim-sikayet"},
    "gorus": {"ikon": "💬", "isim": "Görüş / Öneri", "sinif": "fa-bildirim-gorus"},
    "diger": {"ikon": "📩", "isim": "Diğer", "sinif": "fa-bildirim-diger"},
}


def bildirim_ekle(kullanici_adi, tip, konu, mesaj):
    bd = bildirimler_yukle()
    yeni = {"id": int(time.time() * 1000), "kullanici": kullanici_adi, "tip": tip, "konu": konu, "mesaj": mesaj, "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "durum": "okunmadi", "cevap": ""}
    bd.append(yeni); bildirimler_kaydet(bd); return yeni["id"]


def bildirim_guncelle(bid, **kwargs):
    bd = bildirimler_yukle()
    for b in bd:
        if b.get("id") == bid: b.update(kwargs); break
    bildirimler_kaydet(bd)


def bildirim_sil(bid):
    bd = bildirimler_yukle(); bd = [b for b in bd if b.get("id") != bid]; bildirimler_kaydet(bd)


def kullanici_bildirimleri(kullanici_adi):
    bd = bildirimler_yukle()
    return [b for b in bd if b.get("kullanici") == kullanici_adi]


def saat_2_saat_ileri(s):
    if not s: return s
    m = re.match(r'^(\d{1,2}):(\d{2})$', str(s).strip())
    if not m: return s
    try: return f"{(int(m.group(1)) + 2) % 24:02d}:{int(m.group(2)):02d}"
    except Exception: return s


def saat_sirala_anahtari(g):
    try:
        v = g.get("veri", {}) if isinstance(g, dict) else {}
        tarih = str(v.get("tarih", "")).strip(); saat = str(v.get("saat", "")).strip()
        gun, ay, yil = 99, 99, 9999
        if tarih:
            m = re.match(r'^(\d{1,2})\.(\d{1,2})\.(\d{2,4})$', tarih)
            if m:
                gun = int(m.group(1)); ay = int(m.group(2)); yr = m.group(3); yil = int(yr) if len(yr) == 4 else 2000 + int(yr)
        sh, sm = 99, 99
        if saat:
            m2 = re.match(r'^(\d{1,2}):(\d{2})$', saat)
            if m2: sh = int(m2.group(1)); sm = int(m2.group(2))
        return (yil, ay, gun, sh, sm)
    except Exception: return (9999, 99, 99, 99, 99)


ESIK_YUKSEK = 65.0; ESIK_ORTA = 55.0; ESIK_BELIRSIZ = 50.0; MONTE_CARLO_N = 3000


VARSAYILAN_VERI = {k: v for k, v in {
    "ppg_ev": 0.0, "mpg_dep": 0.0, "form_str_ev": "", "form_str_dep": "",
    "siralama_ev": 0, "siralama_dep": 0, "puan_ev": 0, "puan_dep": 0,
    "xg_ev": 0.0, "xg_dep": 0.0, "atilan_ev": 0.0, "atilan_dep": 0.0,
    "yenen_ev": 0.0, "yenen_dep": 0.0, "clean_sheets_ev": 0.0, "clean_sheets_dep": 0.0,
    "team_scored_ev": 0.0, "team_scored_dep": 0.0, "team_scored_2_ev": 0.0, "team_scored_2_dep": 0.0,
    "scored_both_halves_ev": 0.0, "scored_both_halves_dep": 0.0,
    "goal_both_halves_ev": 0.0, "goal_both_halves_dep": 0.0,
    "ust05_ev": 80.0, "ust05_dep": 80.0, "ust15_ev": 50.0, "ust15_dep": 50.0,
    "ust25_ev": 30.0, "ust25_dep": 30.0, "ust35_ev": 20.0, "ust35_dep": 20.0,
    "kg_siklik_ev": 50.0, "kg_siklik_dep": 50.0, "btts_1h_ev": 0.0, "btts_1h_dep": 0.0,
    "btts_2h_ev": 0.0, "btts_2h_dep": 0.0, "btts_over15_ev": 0.0, "btts_over15_dep": 0.0,
    "btts_over25_ev": 0.0, "btts_over25_dep": 0.0, "tg_0_ev": 0.0, "tg_0_dep": 0.0,
    "tg_1_ev": 0.0, "tg_1_dep": 0.0, "tg_2_ev": 0.0, "tg_2_dep": 0.0,
    "tg_3_ev": 0.0, "tg_3_dep": 0.0, "tg_4_ev": 0.0, "tg_4_dep": 0.0,
    "tg_01_ev": 0.0, "tg_01_dep": 0.0, "tg_23_ev": 0.0, "tg_23_dep": 0.0,
    "tg_4p_ev": 0.0, "tg_4p_dep": 0.0, "ht_ust05_ev": 0.0, "ht_ust05_dep": 0.0,
    "ht_ust15_ev": 0.0, "ht_ust15_dep": 0.0, "ht_ust25_ev": 0.0, "ht_ust25_dep": 0.0,
    "wht_wft_ev": 0.0, "wht_wft_dep": 0.0, "wht_dft_ev": 0.0, "wht_dft_dep": 0.0,
    "wht_lft_ev": 0.0, "wht_lft_dep": 0.0, "dht_wft_ev": 0.0, "dht_wft_dep": 0.0,
    "dht_dft_ev": 0.0, "dht_dft_dep": 0.0, "dht_lft_ev": 0.0, "dht_lft_dep": 0.0,
    "lht_wft_ev": 0.0, "lht_wft_dep": 0.0, "lht_dft_ev": 0.0, "lht_dft_dep": 0.0,
    "lht_lft_ev": 0.0, "lht_lft_dep": 0.0,
    "galibiyet_ev": 30.0, "galibiyet_dep": 30.0, "beraberlik_ev": 30.0, "beraberlik_dep": 30.0,
    "maglubiyet_ev": 30.0, "maglubiyet_dep": 30.0,
    "win_1h_ev": 0.0, "win_1h_dep": 0.0, "draw_ht_ev": 0.0, "draw_ht_dep": 0.0,
    "lose_1h_ev": 0.0, "lose_1h_dep": 0.0, "win_btts_ev": 0.0, "win_btts_dep": 0.0,
    "draw_btts_ev": 0.0, "draw_btts_dep": 0.0, "lose_btts_ev": 0.0, "lose_btts_dep": 0.0,
    "win_over15_ev": 0.0, "win_over15_dep": 0.0, "lose_over15_ev": 0.0, "lose_over15_dep": 0.0,
    "takim_ev": "", "takim_dep": "", "skor_ev": 0, "skor_dep": 0, "skor_belli": False,
    "lig_ort_toplam": 0.0, "lig_ust25": 0.0, "lig_kg": 0.0,
    "saat": "", "tarih": "", "ulke": "", "format": "bilinmiyor", "kaynak_url": "",
    "trends_ev": [], "trends_dep": [],
}.items()}

MAX_GOL = 8; BELIRSIZLIK = 0.20; MAX_MAC_SINIRI = 500
_kilit = threading.Lock(); _ESIK_CACHE = {}
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gc = st.session_state.gecmis_analizler; top = len(gc)
    if admin_mi():
        st.markdown("### 💾 Yedekleme")
        c1, c2 = st.columns(2)
        with c1:
            json_str = json.dumps(st.session_state.gecmis_analizler, ensure_ascii=False, indent=2)
            st.download_button(label=f"📥 Geçmişi İndir ({top} maç)", data=json_str, file_name=f"gecmis_{top}mac.json", mime="application/json", use_container_width=True, key="ind_gecmis")
        with c2:
            yuk = st.file_uploader("📤 Geçmişi Yükle (JSON)", type=["json"], key="yuk_gecmis")
            if yuk is not None:
                try:
                    veri = json.loads(yuk.read().decode("utf-8"))
                    if isinstance(veri, list):
                        st.session_state.gecmis_analizler = veri; gecmis_kaydet(veri)
                        st.success(f"✅ {len(veri)} maç yüklendi!"); st.rerun()
                    else: st.error("❌ Dosya formatı hatalı (liste bekleniyor).")
                except Exception as e: st.error(f"❌ Hata: {e}")
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
            ulke = v.get("ulke", ""); saat = v.get("saat", ""); tarih = v.get("tarih", "")
            bayrak = ulke_bayrak_bul(ulke)

            meta_parcalar = []
            if ulke: meta_parcalar.append(f"{bayrak} {ulke.title()[:14]}")
            if tarih: meta_parcalar.append(f"📅 {tarih}")
            meta_html = "".join(f"<span>{m}</span>" for m in meta_parcalar)

            st.markdown(f'''<div class="mh2-match"><div class="mh2-match-ust"><span>🕐 <span class="saat">{_e(saat or "—")}</span></span><span class="mh2-live gecti">BİTMİŞ</span></div><div class="mh2-match-takimlar"><div class="mh2-takim mh2-takim-ev">{_e(te)}</div><div class="mh2-skor">{se} - {sd}</div><div class="mh2-takim mh2-takim-dep">{_e(td)}</div></div><div class="mh2-match-meta">{meta_html}</div></div>''', unsafe_allow_html=True)

            dogruluk = g.get("dogruluk") or sonuc_hesapla(g)
            if dogruluk:
                o1 = dogruluk.get("oneri_1x2", {}); og = dogruluk.get("oneri_gol", {}); okg = dogruluk.get("oneri_kg", {})
                def _cls(tuttu): return "hit" if tuttu is True else ("miss" if tuttu is False else "neutral")
                def _lbl(tahmin, tuttu):
                    if tahmin is None: return "—"
                    ikon = "✅" if tuttu else "❌"
                    return f"{tahmin} {ikon}"
                st.markdown(f'''<div class="mh2-result-row"><div class="mh2-result-item"><div class="mh2-result-lbl">1X2</div><div class="mh2-result-val {_cls(o1.get("tuttu"))}">{_lbl(o1.get("tahmin"), o1.get("tuttu"))}</div></div><div class="mh2-result-item"><div class="mh2-result-lbl">GOL</div><div class="mh2-result-val {_cls(og.get("tuttu"))}">{_lbl(og.get("tahmin"), og.get("tuttu"))}</div></div><div class="mh2-result-item"><div class="mh2-result-lbl">KG</div><div class="mh2-result-val {_cls(okg.get("tuttu"))}">{_lbl(okg.get("tahmin"), okg.get("tuttu"))}</div></div></div>''', unsafe_allow_html=True)

            if admin_mi():
                c1, c2 = st.columns([5, 1])
                with c1:
                    if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"mac_{idx}", type="primary"):
                        st.session_state.form_verileri = copy.deepcopy(v)
                        st.session_state.kayit_yapildi = True; st.session_state.gecmisten_gelindi = True
                        st.session_state.aktif_kayit_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
                with c2:
                    if st.button("🗑️ Sil", use_container_width=True, key=f"sil_{idx}"):
                        if st.session_state.get("tek_silme_onay") == idx: st.session_state.tek_silme_onay = None
                        else: st.session_state.tek_silme_onay = idx
                        st.rerun()
                if st.session_state.get("tek_silme_onay") == idx:
                    st.warning(f"⚠️ **{te} vs {td}** maçını silmek istediğinden emin misin?")
                    oc1, oc2 = st.columns(2)
                    with oc1:
                        if st.button("✅ Evet, Sil", key=f"ev_{idx}", use_container_width=True, type="primary"):
                            try:
                                st.session_state.gecmis_analizler.pop(idx)
                                gecmis_kaydet(st.session_state.gecmis_analizler)
                                st.session_state.tek_silme_onay = None
                                st.rerun()
                            except Exception as e: st.error(f"❌ Silme hatası: {e}")
                    with oc2:
                        if st.button("❌ Vazgeç", key=f"hh_{idx}", use_container_width=True):
                            st.session_state.tek_silme_onay = None; st.rerun()
            else:
                if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"mac_{idx}", type="primary"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True; st.session_state.gecmisten_gelindi = True
                    st.session_state.aktif_kayit_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

    if admin_mi() and top > 0:
        st.markdown(f'<div style="background:linear-gradient(135deg,rgba(239,68,68,0.15),rgba(239,68,68,0.05));border:1.5px solid rgba(239,68,68,0.5);border-radius:14px;padding:14px;margin-bottom:16px;"><div style="font-size:0.95rem;font-weight:900;color:#ef4444;letter-spacing:0.5px;margin-bottom:4px;">🚨 TEHLİKELİ BÖLGE — TOPLU SİLME</div><div style="font-size:0.78rem;color:#fca5a5;font-weight:600;">Bu butona bastığınızda <b>TÜM GEÇMİŞ MAÇLAR ({top} maç)</b> kalıcı olarak silinir. Bu işlem geri alınamaz!</div></div>', unsafe_allow_html=True)
        if st.session_state.get("silme_onay"):
            st.error(f"⚠️ **SON ONAY:** Tüm geçmiş silinecek (**{top} maç**). Emin misin?")
            oc1, oc2 = st.columns(2)
            with oc1:
                if st.button("✅ EVET, TÜMÜNÜ SİL", key="sil_g_evet", use_container_width=True, type="primary"):
                    try:
                        st.session_state.gecmis_analizler = []; gecmis_kaydet([])
                        st.session_state.silme_onay = False; st.session_state.tek_silme_onay = None
                        st.success("✅ Tüm geçmiş silindi!"); time.sleep(1); st.rerun()
                    except Exception as e: st.error(f"❌ Silme hatası: {e}")
            with oc2:
                if st.button("❌ Vazgeç", key="sil_g_iptal", use_container_width=True):
                    st.session_state.silme_onay = False; st.rerun()
        else:
            def _toplu_sil_toggle(): st.session_state.silme_onay = True
            st.button(f"🗑️ TÜM GEÇMİŞİ SİL ({top} MAÇ)", use_container_width=True, key="temizle_g", type="primary", on_click=_toplu_sil_toggle)
        st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gc_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "backtest":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>🔬 Model Test (Backtest)</h1>", unsafe_allow_html=True)
    with st.expander("📊 Test Ayarları", expanded=(st.session_state.bt_sonuc is None)):
        st.caption("Hangi marketleri ve hangi eşikleri test etmek istediğini seç.")
        c1, c2, c3 = st.columns(3)
        with c1:
            s1x2 = st.checkbox("⚽ 1X2", key="bt_1x2")
            e1 = st.slider("1 eşiği", 0, 100, 55, key="sl_bt_1")
            ex = st.slider("X eşiği", 0, 100, 55, key="sl_bt_x")
            e2 = st.slider("2 eşiği", 0, 100, 55, key="sl_bt_2")
        with c2:
            skv = st.checkbox("🤝 KG Var", key="bt_kg_var"); ekv = st.slider("KG Var eşiği", 0, 100, 70, key="sl_kg_var")
            sky = st.checkbox("🚫 KG Yok", key="bt_kg_yok"); eky = st.slider("KG Yok eşiği", 0, 100, 70, key="sl_kg_yok")
        with c3:
            su = st.checkbox("⬆️ Üst 2.5", key="bt_ust"); eu = st.slider("Üst eşiği", 0, 100, 70, key="sl_ust")
            sa = st.checkbox("⬇️ Alt 2.5", key="bt_alt"); ea = st.slider("Alt eşiği", 0, 100, 70, key="sl_alt")
        if st.button("🚀 TESTİ ÇALIŞTIR", use_container_width=True, type="primary", key="bt_run"):
            with st.spinner("Test ediliyor..."):
                sec = {"1x2": s1x2, "kg_var": skv, "kg_yok": sky, "ust": su, "alt": sa}
                esk = {"esik_1": float(e1), "esik_x": float(ex), "esik_2": float(e2), "kg_var": float(ekv), "kg_yok": float(eky), "ust": float(eu), "alt": float(ea)}
                if not any(sec.values()): st.warning("⚠️ En az bir market seç.")
                else:
                    s, d = backtest_hesapla(st.session_state.gecmis_analizler, sec, esk)
                    st.session_state.bt_sonuc = s; st.session_state.bt_detaylar = d; st.session_state.bt_sec = sec
    if st.session_state.bt_sonuc and st.session_state.get("bt_sec"):
        sec = st.session_state.bt_sec; sonuc = st.session_state.bt_sonuc
        gecmis_len = len(st.session_state.gecmis_analizler)
        st.markdown(f'''<div style="text-align:center;margin:10px 0 6px 0;"><span style="display:inline-block; background:rgba(59,130,246,0.12); border:1px solid rgba(59,130,246,0.5); border-radius:99px; padding:4px 14px; font-size:0.72rem; font-weight:800; color:#3b82f6; letter-spacing:0.5px;">🔎 {gecmis_len} MAÇ ÜZERİNDE TEST EDİLDİ</span></div>''', unsafe_allow_html=True)
        def _bt_kart(baslik, ikon, d, renk, acik_renk):
            dog = d["dogru"]; yan = d["yanlis"]; tt = dog + yan
            yuzde = (dog / tt * 100) if tt > 0 else 0
            if tt == 0:
                return f'''<div class="fa-bt-kart" style="--c:{renk};--c-l:{acik_renk};"><div class="fa-bt-ust"><span class="fa-bt-lbl">{ikon} {baslik}</span><span class="fa-bt-pct">%—</span></div><div class="fa-bt-bar"><div class="fa-bt-fill" style="width:0%"></div></div><div class="fa-bt-sub"><span>Hiç sinyal yok</span><span>0 maç</span></div></div>'''
            return f'''<div class="fa-bt-kart" style="--c:{renk};--c-l:{acik_renk};"><div class="fa-bt-ust"><span class="fa-bt-lbl">{ikon} {baslik}<small>{tt} sinyal</small></span><span class="fa-bt-pct">%{yuzde:.1f}</span></div><div class="fa-bt-bar"><div class="fa-bt-fill" style="width:{yuzde:.1f}%"></div></div><div class="fa-bt-sub"><span><span class="fa-bt-dog">✓ {dog} doğru</span> &nbsp; <span class="fa-bt-yan">✗ {yan} yanlış</span></span><span>Başarı %{yuzde:.1f}</span></div></div>'''
        kartlar = []
        if sec.get("1x2"): kartlar.append(_bt_kart("1X2", "⚽", sonuc["1x2"], "#22c55e", "#4ade80"))
        if sec.get("kg_var"): kartlar.append(_bt_kart("KG Var", "🤝", sonuc["kg_var"], "#3b82f6", "#60a5fa"))
        if sec.get("kg_yok"): kartlar.append(_bt_kart("KG Yok", "🚫", sonuc["kg_yok"], "#8b5cf6", "#a78bfa"))
        if sec.get("ust"): kartlar.append(_bt_kart("Üst 2.5", "⬆️", sonuc["ust"], "#f59e0b", "#fbbf24"))
        if sec.get("alt"): kartlar.append(_bt_kart("Alt 2.5", "⬇️", sonuc["alt"], "#ef4444", "#f87171"))
        if not kartlar: st.markdown('<div class="fa-bt-bos"><span class="fa-bt-bos-ikon">📭</span>Hiç market seçilmedi.</div>', unsafe_allow_html=True)
        else: st.markdown(f'<div class="fa-bt-grid">{"".join(kartlar)}</div>', unsafe_allow_html=True)
        tum_dog = sum(sonuc[k]["dogru"] for k in sonuc)
        tum_yan = sum(sonuc[k]["yanlis"] for k in sonuc)
        tum_tt = tum_dog + tum_yan
        if tum_tt > 0:
            genel = tum_dog / tum_tt * 100
            sv = "yuksek" if genel >= 65 else "orta" if genel >= 55 else "dusuk"
            renk = "#22c55e" if sv == "yuksek" else "#f59e0b" if sv == "orta" else "#ef4444"
            st.markdown(f'''<div class="fa-bt-kart" style="--c:{renk};--c-l:{renk};margin-top:14px;"><div class="fa-bt-ust"><span class="fa-bt-lbl">📊 GENEL TOPLAM<small>{tum_tt} sinyal</small></span><span class="fa-bt-pct">%{genel:.1f}</span></div><div class="fa-bt-bar"><div class="fa-bt-fill" style="width:{genel:.1f}%"></div></div><div class="fa-bt-sub"><span><span class="fa-bt-dog">✓ {tum_dog} doğru</span> &nbsp; <span class="fa-bt-yan">✗ {tum_yan} yanlış</span></span><span>Tüm marketler</span></div></div>''', unsafe_allow_html=True)
    else:
        st.markdown('<div class="fa-bt-bos"><span class="fa-bt-bos-ikon">🔬</span>Yukarıdaki ayarları yap ve <b>Testi Çalıştır</b> butonuna bas.</div>', unsafe_allow_html=True)
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="btg"):
        st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "ayarlar":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>⚙️ Ayarlar</h1>", unsafe_allow_html=True)
    mv = st.session_state.esikler.copy()
    st.markdown("### 🏦 Ödeme")
    c1, c2 = st.columns(2)
    with c1: yiban = st.text_input("IBAN", value=mv.get("iban", "TR00 0000 0000 0000 0000 0000 00"))
    with c2: yhs = st.text_input("Hesap Sahibi", value=mv.get("hesap_sahibi", ""))
    st.markdown("### 💰 Fiyatlar")
    c1, c2 = st.columns(2)
    with c1: yfh = st.number_input("Haftalık", min_value=1.0, value=float(mv.get("fiyat_haftalik", 49.0)), step=10.0, key="ay_fh")
    with c2: yfa = st.number_input("Aylık", min_value=1.0, value=float(mv.get("fiyat_aylik", 149.0)), step=10.0, key="ay_fa")
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
            y = dict(mv); y.update({"iban": yiban, "hesap_sahibi": yhs, "fiyat_haftalik": float(yfh), "fiyat_aylik": float(yfa), "ucretsiz_kotasi": int(yk), "esik_1": float(ye1), "esik_x": float(yex), "esik_2": float(ye2), "ust": float(yu), "alt": float(ya), "kg_var": float(ykv), "kg_yok": float(yky)})
            st.session_state.esikler = y; ayarlar_kaydet(y); st.success("✅ Kaydedildi!")
    with c2:
        if st.button("🔄 Sıfırla", use_container_width=True):
            v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "iban": "TR00 0000 0000 0000 0000 0000 00", "hesap_sahibi": "ADINIZ SOYADINIZ", "fiyat_haftalik": 49.0, "fiyat_aylik": 149.0, "fiyat_yillik": 999.0, "ucretsiz_kotasi": 3}
            st.session_state.esikler = v; ayarlar_kaydet(v); st.rerun()
    with c3:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="ayg"):
            st.session_state.sayfa = "giris"; st.rerun()


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


elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)
    te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
    sb = v.get("skor_belli", False); se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    ulke = v.get("ulke", ""); saat = v.get("saat", ""); tarih = v.get("tarih", "")
    bayrak = ulke_bayrak_bul(ulke)
    meta_parcalar = []
    if ulke: meta_parcalar.append(f"{bayrak} {ulke.title()}")
    elif bayrak != "🌍": meta_parcalar.append(bayrak)
    if tarih: meta_parcalar.append(f"📅 {tarih}")
    if saat: meta_parcalar.append(f"🕐 {saat}")
    meta = " &nbsp;•&nbsp; ".join(meta_parcalar) if meta_parcalar else "MAÇ ANALİZİ"
    skor_html = f'<div class="an-skor">{se} - {sd}</div>' if sb else '<div class="an-vs">VS</div>'
    st.markdown(f'''<div class="an-hero"><div class="an-hero-meta"><span class="an-pulse-dot"></span> {meta}</div><div class="an-hero-teams"><div class="an-team an-team-ev">{_e(te)}</div><div class="an-hero-mid">{skor_html}</div><div class="an-team an-team-dep">{_e(td)}</div></div><div class="an-hero-xg">⚡ Beklenen Gol: <b>{a["lam_ev"]:.2f}</b> – <b>{a["lam_dep"]:.2f}</b>&nbsp;•&nbsp; Toplam: <b>{a["lam_ev"]+a["lam_dep"]:.2f}</b></div></div>''', unsafe_allow_html=True)

    st.markdown('<div class="an-section-ttl">📋 TAKIM FORMLARI (SON 5 MAÇ)</div>', unsafe_allow_html=True)
    def _form_buyuk_html(form_str, takim, ev_mi=True):
        cls_takim = "ev" if ev_mi else "dep"
        renk_kart = "#3b82f6" if ev_mi else "#f59e0b"
        s = "".join(c for c in str(form_str or "").upper() if c in "WDL")
        if not s:
            icerik = '<div class="an-form-bos">Veri yok</div>'
        else:
            boxes = "".join(f'<span class="an-form-box-buyuk an-form-{c}">{c}</span>' for c in s)
            icerik = f'<div class="an-form-row-buyuk">{boxes}</div>'
        return f'<div class="an-form-kart" style="--c:{renk_kart};"><div class="an-form-takim {cls_takim}">{_e(takim)}</div>{icerik}</div>'
    f_ev = _form_buyuk_html(v.get("form_str_ev", ""), te, ev_mi=True)
    f_dep = _form_buyuk_html(v.get("form_str_dep", ""), td, ev_mi=False)
    st.markdown(f'<div style="display:grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 0 0 16px 0;">{f_ev}{f_dep}</div>', unsafe_allow_html=True)

    st.markdown('<div class="an-section-ttl">⚔️ Takım Karşılaştırması</div>', unsafe_allow_html=True)
    ae = float(v.get("atilan_ev", 0) or 0); ad = float(v.get("atilan_dep", 0) or 0)
    ye = float(v.get("yenen_ev", 0) or 0); yd = float(v.get("yenen_dep", 0) or 0)
    xge = float(v.get("xg_ev", 0) or 0); xgd = float(v.get("xg_dep", 0) or 0)
    u25e = float(v.get("ust25_ev", 0) or 0); u25d = float(v.get("ust25_dep", 0) or 0)
    kge = float(v.get("kg_siklik_ev", 0) or 0); kgd = float(v.get("kg_siklik_dep", 0) or 0)
    cs_e = float(v.get("clean_sheets_ev", 0) or 0); cs_d = float(v.get("clean_sheets_dep", 0) or 0)
    def _cmp_row(lbl, ev_val, dep_val, ev_max=100, dep_max=100, fmt=".1f", suffix=""):
        ev_p = max(0, min(100, (ev_val / ev_max * 100) if ev_max else 0)); dep_p = max(0, min(100, (dep_val / dep_max * 100) if dep_max else 0))
        return f'''<div class="an-cmp-row"><div><div class="an-cmp-val ev">{ev_val:{fmt}}{suffix}</div><div class="an-cmp-bar ev"><div class="an-cmp-fill" style="--r:{100-ev_p:.0f}%; width:{ev_p:.0f}%"></div></div></div><div class="an-cmp-lbl">{lbl}</div><div><div class="an-cmp-val dep">{dep_val:{fmt}}{suffix}</div><div class="an-cmp-bar dep"><div class="an-cmp-fill" style="--l:0%; width:{dep_p:.0f}%"></div></div></div></div>'''
    rows = []
    if ae or ad: rows.append(_cmp_row("Atılan Gol", ae, ad, 4.0, 4.0, ".2f"))
    if ye or yd: rows.append(_cmp_row("Yenen Gol", ye, yd, 4.0, 4.0, ".2f"))
    if xge or xgd: rows.append(_cmp_row("xG", xge, xgd, 3.0, 3.0, ".2f"))
    if u25e or u25d: rows.append(_cmp_row("Üst 2.5", u25e, u25d, 100, 100, ".0f", "%"))
    if kge or kgd: rows.append(_cmp_row("KG Sıklık", kge, kgd, 100, 100, ".0f", "%"))
    if cs_e or cs_d: rows.append(_cmp_row("Clean Sheet", cs_e, cs_d, 100, 100, ".0f", "%"))
    if rows: st.markdown(f'''<div class="an-cmp-wrap"><div class="an-cmp-header"><div class="an-team-name ev">{_e(te)}</div><div class="an-cmp-vs">VS</div><div class="an-team-name dep">{_e(td)}</div></div>{"".join(rows)}</div>''', unsafe_allow_html=True)
    st.markdown('<div class="an-section-ttl">🎯 Maç Sonucu Olasılıkları</div>', unsafe_allow_html=True)
    def _donut(yuzde, renk, boyut=82):
        y = max(0.0, min(100.0, yuzde)); r = 34; cevre = 2 * 3.14159 * r; offset = cevre * (1 - y / 100)
        return f'''<svg class="an-prob-donut" viewBox="0 0 82 82" xmlns="http://www.w3.org/2000/svg"><circle class="an-ring-bg" cx="41" cy="41" r="{r}" fill="none" stroke-width="7"/><circle class="an-ring-fg" cx="41" cy="41" r="{r}" fill="none" stroke="{renk}" stroke-width="7" stroke-dasharray="{cevre:.2f}" stroke-dashoffset="{offset:.2f}" stroke-linecap="round" style="--full:{cevre:.2f}; --off:{offset:.2f}; filter:drop-shadow(0 0 6px {renk});"/><text x="41" y="41" text-anchor="middle" dominant-baseline="central" fill="{renk}" font-size="20" font-weight="900">%{y:.0f}</text></svg>'''
    def _prob_donut(lbl, yuzde, renk, aktif=False, esik=""):
        cls = "an-active" if aktif else ""
        return f'''<div class="an-prob-kart {cls}" style="--c:{renk};"><div class="an-prob-lbl">{lbl}</div>{_donut(yuzde, renk)}<div class="an-prob-alt">{esik}</div></div>'''
    p1, px, p2 = a["p1"], a["px"], a["p2"]
    e1_ = esik_1x2_al("1"); eX_ = esik_1x2_al("X"); e2_ = esik_1x2_al("2")
    kartlar_1x2 = []
    if p1 >= e1_: kartlar_1x2.append(_prob_donut("EV KAZANIR", p1, "#3b82f6", True, f"Eşik %{e1_:.0f}"))
    if px >= eX_: kartlar_1x2.append(_prob_donut("BERABERLİK", px, "#94a3b8", True, f"Eşik %{eX_:.0f}"))
    if p2 >= e2_: kartlar_1x2.append(_prob_donut("DEP KAZANIR", p2, "#f59e0b", True, f"Eşik %{e2_:.0f}"))
    if kartlar_1x2: st.markdown(f'<div class="an-olasilik-grid">{"".join(kartlar_1x2)}</div>', unsafe_allow_html=True)
    else: st.markdown('<div class="an-glow-kart" style="text-align:center;padding:16px;"><div style="color:#8fa0bd;font-size:0.8rem;">⚠️ Maç sonucu için hiçbir tahmin eşik değerini geçmedi</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="an-section-ttl">⚽ Gol & KG Piyasaları</div>', unsafe_allow_html=True)
    u25, a25 = a["ust_25"], a["alt_25"]
    kgv, kgy = a["kg_var_model"], a["kg_yok_model"]
    e_ust = esik_al("ust"); e_alt = esik_al("alt"); e_kgv = esik_al("kg_var"); e_kgy = esik_al("kg_yok")
    kartlar_gol = []
    if u25 >= e_ust and u25 >= a25: kartlar_gol.append(_prob_donut("ÜST 2.5", u25, "#22c55e", True, f"Eşik %{e_ust:.0f}"))
    if a25 >= e_alt and a25 >= u25: kartlar_gol.append(_prob_donut("ALT 2.5", a25, "#ef4444", True, f"Eşik %{e_alt:.0f}"))
    if kartlar_gol: st.markdown(f'<div class="an-olasilik-grid an-2col">{"".join(kartlar_gol)}</div>', unsafe_allow_html=True)
    else: st.markdown('<div class="an-glow-kart" style="text-align:center;padding:16px;"><div style="color:#8fa0bd;font-size:0.8rem;">⚠️ Gol tahmini eşik değerini geçmedi</div></div>', unsafe_allow_html=True)
    kartlar_kg = []
    if kgv >= e_kgv and kgv >= kgy: kartlar_kg.append(_prob_donut("KG VAR", kgv, "#8b5cf6", True, f"Eşik %{e_kgv:.0f}"))
    if kgy >= e_kgy and kgy >= kgv: kartlar_kg.append(_prob_donut("KG YOK", kgy, "#ec4899", True, f"Eşik %{e_kgy:.0f}"))
    if kartlar_kg: st.markdown(f'<div class="an-olasilik-grid an-2col">{"".join(kartlar_kg)}</div>', unsafe_allow_html=True)
    else: st.markdown('<div class="an-glow-kart" style="text-align:center;padding:16px;"><div style="color:#8fa0bd;font-size:0.8rem;">⚠️ KG tahmini eşik değerini geçmedi</div></div>', unsafe_allow_html=True)
    ai_html = ai_yorum_paneli(v, a)
    if ai_html:
        st.markdown('<div class="an-section-ttl">🤖 Yapay Zeka Detaylı Analizi</div>', unsafe_allow_html=True)
        st.markdown(ai_html, unsafe_allow_html=True)
    s1, y1 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    e1 = esik_1x2_al(s1)
    km = (u25 >= esik_al("ust") and u25 >= a25) or (a25 >= esik_al("alt") and a25 >= u25) or (y1 >= e1)
    if not st.session_state.kayit_yapildi and admin_mi():
        yk = kayit_olustur(v, a)
        if sb:
            st.session_state.gecmis_analizler.append(yk); gecmis_kaydet(st.session_state.gecmis_analizler)
        elif km:
            st.session_state.gelecek_analizler.append(yk); gelecek_kaydet(st.session_state.gelecek_analizler)
        st.session_state.kayit_yapildi = True
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Geri Dön", use_container_width=True, key="sonuc_geri_btn"):
            if st.session_state.get("gecmisten_gelindi"): st.session_state.sayfa = "gecmis"
            elif st.session_state.get("gelecekten_gelindi"): st.session_state.sayfa = "gelecek_admin" if admin_mi() else "giris"
            else: st.session_state.sayfa = "giris"
            st.session_state.gecmisten_gelindi = False; st.session_state.gelecekten_gelindi = False
            st.rerun()
    with c2:
        if st.button("🔄 Yeni Analiz", use_container_width=True, type="primary", key="sonuc_yeni_btn"):
            st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
            st.session_state.kayit_yapildi = False
            st.session_state.gecmisten_gelindi = False; st.session_state.gelecekten_gelindi = False
            st.session_state.sayfa = "giris"; st.rerun()
