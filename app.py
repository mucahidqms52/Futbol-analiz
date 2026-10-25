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
Yürürlük Tarihi: Hizmete kayıt olduğunuz tarih itibariyle geçerlidir.

## 1. TARAFLAR VE KAPSAM
Bu Kullanım Şartları, **"Futbol Analiz Pro"** (bundan sonra **"Uygulama"** veya **"Hizmet"** olarak anılacaktır) ile bu hizmete kayıt olan kullanıcı (bundan sonra **"Kullanıcı"** olarak anılacaktır) arasında akdedilmiştir.

## 2. HİZMETİN TANIMI
Uygulama, futbol maçlarına ilişkin olarak **geçmiş istatistiklere dayalı matematiksel ve istatistiksel analizler** üreterek kullanıcıya **bilgilendirme amaçlı tahminler** sunar.

## 3. YAŞ SINIRI VE EHLİYET
Uygulama'yı kullanabilmek için 18 yaşından büyük olmanız ve fiil ehliyetine sahip olmanız gerekmektedir.

## 4. HİZMETİN "OLDUĞU GİBİ" SUNULMASI
Uygulama, "AS IS" ve "AS AVAILABLE" esasına göre sunulmaktadır.

## 5. TAHMİN GARANTİSİ YOKTUR
Sunulan tüm tahminler geçmiş verilere dayanır ve gelecek sonuçları garanti etmez.

## 6. SORUMLULUĞUN SINIRLANDIRILMASI VE İBRA
Kullanıcı, Uygulama'yı kullanması nedeniyle doğabilecek her türlü zarardan Uygulama'yı ibra eder.

## 7. YASADIŞI BAHİS VE KUMAR UYARISI
Yasadışı bahis oynamak suçtur.

## 8. ÖDEME, ABONELİK VE İADE KOŞULLARI
Ödemeler havale/EFT ile yapılır. İade talepleri bildirim bölümünden iletilir.

## 9. ABONELİK İPTALİ
Kullanıcı aboneliğini bildirim bölümünden iptal edebilir.

## 10. KİŞİSEL VERİLERİN KORUNMASI (KVKK)
Veriler KVKK kapsamında korunur, 3. taraflarla paylaşılmaz.

## 11. FİKRİ MÜLKİYET
Tüm içerikler telif hakkı ile korunmaktadır.

## 12. HİZMET DEĞİŞİKLİKLERİ
Uygulama, hizmeti değiştirme hakkını saklı tutar.

## 13. UYUŞMAZLIK VE YETKİLİ MAHKEME
Türkiye Cumhuriyeti hukuku uygulanır.

## 14. YÜRÜRLÜK VE KABUL
Kayıt olmak bu şartların kabulü anlamına gelir.

## 15. İLETİŞİM
Her türlü talep için "Bildirim" bölümünü kullanın.

**SON SÖZ:** Bu uygulama SADECE bilgilendirme amaçlıdır. YEDAM: 115
"""

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
    html, body { overscroll-behavior: none !important; }
    .stApp { overscroll-behavior: none !important; }
    html { font-size: 13px !important; }
    body, .stApp { font-size: 0.85rem !important; }
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    h1, h2, h3, h4 { font-family: 'Rajdhani', 'Inter', sans-serif !important; letter-spacing: 0.4px; }
    .block-container { padding: 0.8rem !important; max-width: 100% !important; }
    :root { --bg-0: #060a14; --bg-1: #0b1220; --card: #131c2e; --border: #1f2c44; --text: #eaf1fb; --muted: #7f92b3; --green: #22c55e; --blue: #3b82f6; --yellow: #f59e0b; --red: #ef4444; }
    .stApp { background: radial-gradient(1200px 600px at 10% -10%, rgba(34,197,94,0.08), transparent 60%), radial-gradient(900px 500px at 100% 0%, rgba(59,130,246,0.07), transparent 60%), linear-gradient(180deg, #060a14 0%, #0b1220 100%) !important; }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp div[data-testid="stMarkdownContainer"] { color: var(--text) !important; }
    h1 { font-size: 1.35rem !important; font-weight: 800 !important; text-align: center; background: linear-gradient(135deg, #eaf1fb 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    h2 { font-size: 1rem !important; font-weight: 700 !important; }
    h3 { font-size: 0.88rem !important; font-weight: 700 !important; border-left: 3px solid var(--green); padding-left: 0.5rem; }
    p { font-size: 0.8rem !important; line-height: 1.45; }
    .stTextArea textarea, .stTextInput input, div[data-testid="stNumberInput"] input { background: var(--card) !important; color: var(--text) !important; border: 1.5px solid var(--border) !important; border-radius: 10px !important; }
    .stTextArea textarea:focus, .stTextInput input:focus, div[data-testid="stNumberInput"] input:focus { border-color: var(--green) !important; box-shadow: 0 0 0 4px rgba(34,197,94,0.12) !important; }
    .stButton button, div[data-testid="stFormSubmitButton"] button { background: linear-gradient(145deg, #18233a, #131c2e) !important; border: 1.5px solid var(--border) !important; border-radius: 10px !important; font-weight: 700 !important; font-size: 0.8rem !important; color: var(--text) !important; padding: 0.35rem 0.5rem !important; }
    .stButton button[kind="primary"], button[data-testid="stBaseButton-primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; border: none !important; color: #04130a !important; }
    div[data-testid="stExpander"] { background: linear-gradient(145deg, var(--card), #0f1829) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; overflow: hidden; margin-bottom: 8px !important; }
    div[data-testid="stExpander"] details > summary { padding: 0.5rem 0.8rem !important; font-size: 0.82rem !important; font-weight: 700 !important; }
    .st-key-fa_nav .stButton button { padding: 0.3rem 0.25rem !important; height: 2.1rem !important; background: rgba(19,28,46,0.6) !important; border: 1px solid var(--border) !important; }
    .st-key-fa_nav .stButton button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; }
    .mh-stat { background: linear-gradient(145deg, #16233d, #0f1a2e); border: 1px solid var(--border); border-radius: 16px; padding: 14px 10px; text-align: center; }
    .mh-stat-num { font-size: 1.8rem; font-weight: 900; color: var(--green) !important; }
    .mh-stat-lbl { font-size: 0.65rem; color: var(--muted) !important; text-transform: uppercase; font-weight: 800; }
    .fa-card { background: linear-gradient(145deg, var(--card), #0f1829); border: 1px solid var(--border); border-radius: 14px; padding: 10px 12px; margin-bottom: 10px; }
    .fa-card.fa-pos { border-color: rgba(34,197,94,0.55); }
    .fa-ttl { font-size: 0.68rem; font-weight: 800; color: var(--muted) !important; text-transform: uppercase; }
    .fa-pickrow { display: flex; align-items: center; justify-content: space-between; }
    .fa-pick { font-size: 1rem; font-weight: 800; }
    .fa-pct { font-size: 1.35rem; font-weight: 900; color: var(--green) !important; }
    .fa-mut { font-size: 0.68rem; color: var(--muted) !important; }
    .fa-row { margin: 7px 0; }
    .fa-row-top { display: flex; justify-content: space-between; font-size: 0.76rem; }
    .fa-bar { position: relative; height: 8px; background: #1a2438; border-radius: 99px; overflow: hidden; }
    .fa-fill { height: 100%; border-radius: 99px; }
    .fa-badge { display: inline-block; padding: 3px 9px; border-radius: 99px; font-size: 0.65rem; font-weight: 800; }
    .fa-b-green { background: rgba(34,197,94,0.15); color: var(--green) !important; }
    .fa-b-gray { background: rgba(148,163,184,0.12); color: #94a3b8 !important; }
    .login-hero { text-align: center; padding: 40px 10px 24px 10px; }
    .login-title { font-size: 2rem !important; font-weight: 900 !important; color: var(--green) !important; }
    div[data-testid="stForm"] { background: linear-gradient(145deg, rgba(19,28,46,0.9), rgba(11,18,32,0.98)) !important; border: 1.5px solid rgba(34,197,94,0.2) !important; border-radius: 20px !important; padding: 22px 18px !important; }
    .mh2-hero { background: linear-gradient(135deg, #14243e 0%, #0d1729 100%); border: 1.5px solid rgba(34,197,94,0.28); border-radius: 22px; padding: 24px 18px; margin: 6px 0 18px 0; text-align: center; }
    .mh2-hero-title { font-size: 1.85rem; font-weight: 900; color: var(--green) !important; }
    .mh2-badge { display: inline-flex; padding: 5px 12px; border-radius: 99px; font-size: 0.7rem; font-weight: 800; }
    .mh2-badge.green { background: rgba(34,197,94,0.14); color: #22c55e !important; }
    .mh2-badge.blue { background: rgba(59,130,246,0.14); color: #3b82f6 !important; }
    .mh2-badge.amber { background: rgba(245,158,11,0.14); color: #f59e0b !important; }
    .mh2-badge.purple { background: rgba(139,92,246,0.14); color: #8b5cf6 !important; }
    .mh2-match-v2 { background: linear-gradient(145deg, rgba(19,28,46,0.95), rgba(11,18,32,1)); border: 1px solid #1d2940; border-radius: 20px; padding: 12px; margin: 10px 0; }
    .mh2-v2-tk { font-size: 1rem; font-weight: 900; text-align: center; }
    .mh2-v2-tk-ev { color: #93c5fd !important; }
    .mh2-v2-tk-dep { color: #fbbf24 !important; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# POSTGRESQL VERİ KATMANI
# ==========================================
ADMIN_KULLANICI_ADI = "admin52"

def _admin_sifre_al():
    try:
        if "ADMIN_SIFRE" in st.secrets:
            s = st.secrets["ADMIN_SIFRE"]
            if s and len(s) >= 8: return s
    except Exception: pass
    s = os.environ.get("ADMIN_SIFRE", "")
    if not s or len(s) < 8:
        st.error("🚨 **GÜVENLİK HATASI:** ADMIN_SIFRE tanımlı değil veya 8 karakterden kısa!")
        st.stop()
    return s

ADMIN_SIFRE = _admin_sifre_al()
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "adm_" + hashlib.sha256(ADMIN_SIFRE.encode()).hexdigest()[:40])

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
        if kalan > 0: return False, kalan
        _GIRIS_DENEMELERI[k] = []
    return True, 0

def _giris_denemesi_ekle(kadi):
    k = (kadi or "").strip().lower()
    if not k: return
    _GIRIS_DENEMELERI.setdefault(k, []).append(time.time())

def _giris_basarili_sil(kadi):
    _GIRIS_DENEMELERI.pop((kadi or "").strip().lower(), None)

def _db_baglanti():
    url = os.environ.get("DATABASE_URL", "")
    if not url: raise RuntimeError("DATABASE_URL ortam değişkeni tanımlı değil.")
    if url.startswith("postgres://"): url = url.replace("postgres://", "postgresql://", 1)
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
            cur.execute("CREATE TABLE IF NOT EXISTS ayarlar (id INT PRIMARY KEY DEFAULT 1, veri JSONB NOT NULL)")
        conn.commit()
    finally: conn.close()
    return True

try: _init_db()
except Exception as _db_hata:
    st.error(f"❌ Veritabanı bağlantı hatası: {_db_hata}")
    st.stop()

def _cookie_manager_al():
    try: return stx.CookieManager(key="fa_cookie_mgr_v1")
    except Exception: return None

_cookie_mgr = _cookie_manager_al()

def _token_uret(): return _secrets.token_hex(32)
def _token_hash(token): return hashlib.sha256(("fa_tok_" + token).encode("utf-8")).hexdigest()
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
        return
    try:
        kl = kullanicilar_yukle()
        k = kl.get(kadi)
        if k and _token_dogrula(token, k.get("oturum_token") or ""):
            st.session_state.aktif_kullanici = kadi
    except Exception: pass

@st.cache_data(ttl=30, show_spinner=False)
def _online_durum_guncelle(session_id):
    online_heartbeat(session_id); return online_say()

if "_session_id" not in st.session_state: st.session_state._session_id = _secrets.token_hex(16)
try: _ONLINE_SAYI = _online_durum_guncelle(st.session_state._session_id)
except Exception: _ONLINE_SAYI = 0

if st.session_state.get("rol") == "admin":
    st.markdown(f'''<div style="text-align:center; margin:0 0 10px 0;"><span style="display:inline-block; background:rgba(34,197,94,0.15); border:1px solid rgba(34,197,94,0.5); border-radius:99px; padding:4px 14px; font-size:0.75rem; font-weight:800; color:#22c55e;">🟢 {_ONLINE_SAYI} KİŞİ ONLINE</span></div>''', unsafe_allow_html=True)

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
    v = list(v)[-200:]
    try: st.session_state.gecmis_analizler = v
    except Exception: pass
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM gecmis")
            for veri in v: cur.execute("INSERT INTO gecmis (veri) VALUES (%s)", (Json(veri),))
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
            for veri in v: cur.execute("INSERT INTO gelecek (veri) VALUES (%s)", (Json(veri),))
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
            cur.execute("SELECT 1 FROM online_kullanicilar WHERE session_id = %s AND son_gorulme > NOW() - INTERVAL '5 minutes'", (session_id,))
            yeni_ziyaret = cur.fetchone() is None
            cur.execute("INSERT INTO online_kullanicilar (session_id, son_gorulme) VALUES (%s, NOW()) ON CONFLICT (session_id) DO UPDATE SET son_gorulme = NOW()", (session_id,))
            cur.execute("DELETE FROM online_kullanicilar WHERE son_gorulme < NOW() - INTERVAL '2 minutes'")
            if yeni_ziyaret:
                cur.execute("INSERT INTO gunluk_ziyaretler (tarih, ziyaret_sayisi) VALUES (CURRENT_DATE, 1) ON CONFLICT (tarih) DO UPDATE SET ziyaret_sayisi = gunluk_ziyaretler.ziyaret_sayisi + 1")
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
    return salt, hashlib.sha256((salt + sifre).encode("utf-8")).hexdigest()

def sifre_dogrula(sifre, salt, kayitli_hash):
    if not kayitli_hash: return False
    if kayitli_hash.startswith("$2"):
        if not BCRYPT_VAR: return False
        try: return bcrypt.checkpw(sifre.encode("utf-8"), kayitli_hash.encode("utf-8"))
        except Exception: return False
    _, h = sifre_hashle(sifre, salt)
    return _secrets.compare_digest(h, kayitli_hash)

def kullanici_ekle(kullanici_adi, sifre):
    kl = kullanicilar_yukle()
    if kullanici_adi in kl: return False, "Bu kullanıcı adı zaten alınmış."
    salt, s_hash = sifre_hashle(sifre)
    kl[kullanici_adi] = {"salt": salt, "sifre_hash": s_hash, "kayit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"), "abonelik_bitis": None, "son_odeme": None, "son_odeme_gun": 0, "yasal_kabul_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"), "oturum_token": None}
    kullanicilar_kaydet(kl)
    return True, "Kayıt başarılı."

def kullanici_dogrula(kullanici_adi, sifre):
    kl = kullanicilar_yukle()
    k = kl.get(kullanici_adi)
    if not k: return False
    return sifre_dogrula(sifre, k.get("salt", ""), k["sifre_hash"])

def abonelik_aktif_mi(kullanici_adi):
    kl = kullanicilar_yukle()
    k = kl.get(kullanici_adi)
    if not k: return False
    bs = k.get("abonelik_bitis")
    if not bs: return False
    try: return datetime.strptime(bs, "%Y-%m-%d") >= datetime.now()
    except Exception: return False

def abonelik_aktif_et(kullanici_adi, gun_sayisi):
    kl = kullanicilar_yukle()
    if kullanici_adi not in kl: return False, "Kullanıcı bulunamadı."
    k = kl[kullanici_adi]
    mevcut = None
    if k.get("abonelik_bitis"):
        try: mevcut = datetime.strptime(k["abonelik_bitis"], "%Y-%m-%d")
        except Exception: pass
    bugun = datetime.now()
    bas = mevcut if (mevcut and mevcut > bugun) else bugun
    yeni = bas + timedelta(days=int(gun_sayisi))
    k["abonelik_bitis"] = yeni.strftime("%Y-%m-%d")
    k["son_odeme"] = bugun.strftime("%Y-%m-%d %H:%M"); k["son_odeme_gun"] = int(gun_sayisi)
    kullanicilar_kaydet(kl)
    return True, yeni.strftime("%Y-%m-%d")

def abonelik_iptal_et(kullanici_adi):
    kl = kullanicilar_yukle()
    if kullanici_adi not in kl: return False
    kl[kullanici_adi]["abonelik_bitis"] = None
    kullanicilar_kaydet(kl); return True

def kullanici_sil(kullanici_adi):
    kl = kullanicilar_yukle()
    if kullanici_adi in kl:
        del kl[kullanici_adi]; kullanicilar_kaydet(kl)
        bd = [b for b in bildirimler_yukle() if b.get("kullanici") != kullanici_adi]
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
    "iptal": {"ikon": "🚫", "isim": "Abonelik İptal Talebi"},
    "sikayet": {"ikon": "⚠️", "isim": "Şikayet"},
    "gorus": {"ikon": "💬", "isim": "Görüş / Öneri"},
    "diger": {"ikon": "📩", "isim": "Diğer"},
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
    bd = [b for b in bildirimler_yukle() if b.get("id") != bid]; bildirimler_kaydet(bd)

def kullanici_bildirimleri(kullanici_adi):
    return [b for b in bildirimler_yukle() if b.get("kullanici") == kullanici_adi]

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
    "ust05_ev": 80.0, "ust05_dep": 80.0, "ust15_ev": 50.0, "ust15_dep": 50.0,
    "ust25_ev": 30.0, "ust25_dep": 30.0, "ust35_ev": 20.0, "ust35_dep": 20.0,
    "kg_siklik_ev": 50.0, "kg_siklik_dep": 50.0,
    "galibiyet_ev": 30.0, "galibiyet_dep": 30.0, "beraberlik_ev": 30.0, "beraberlik_dep": 30.0,
    "maglubiyet_ev": 30.0, "maglubiyet_dep": 30.0,
    "takim_ev": "", "takim_dep": "", "skor_ev": 0, "skor_dep": 0, "skor_belli": False,
    "lig_ort_toplam": 0.0, "lig_ust25": 0.0, "lig_kg": 0.0,
    "saat": "", "tarih": "", "ulke": "", "format": "bilinmiyor", "kaynak_url": "",
    "trends_ev": [], "trends_dep": [],
    "son5_xg_atak": 0.0, "son5_xg_savunma": 0.0, "son5_ppg": 0.0,
    "son5_btts_yuzde": 0.0, "son5_ust25_yuzde": 0.0, "son5_cs_yuzde": 0.0,
}.items()}

MAX_GOL = 8; BELIRSIZLIK = 0.20; MAX_MAC_SINIRI = 500
_kilit = threading.Lock(); _ESIK_CACHE = {}

# ==========================================
# 🎯 LİG FİLTRESİ — Sadece 1. ve 2. Ligler
# ==========================================
# Her ülke için izin verilen ligler (1. ve 2. ligler)
# Ülke adı -> o ülkenin 1. ve 2. lig anahtar kelimeleri
LIG_FILTRESI = {
    "turkey": ["süper lig", "super lig", "1. lig", "1. lig", "tff 1. lig", "tff first league", "turkish super lig", "turkish first league"],
    "italy": ["serie a", "serie b", "serie a", "serie b"],
    "spain": ["la liga", "laliga", "segunda division", "la liga 2", "segunda"],
    "england": ["premier league", "championship", "efl championship"],
    "germany": ["bundesliga", "2. bundesliga", "2. bundesliga", "zweite bundesliga"],
    "france": ["ligue 1", "ligue 2"],
    "netherlands": ["eredivisie", "eerste divisie"],
    "portugal": ["primeira liga", "liga portugal", "liga 2", "segunda liga"],
    "belgium": ["jupiler pro league", "first division a", "challenger pro league", "first division b"],
    "scotland": ["premiership", "championship"],
    "austria": ["bundesliga", "2. liga", "erste liga"],
    "switzerland": ["super league", "challenge league"],
    "croatia": ["hnl", "1. hnl", "2. hnl"],
    "serbia": ["super liga", "prva liga"],
    "denmark": ["superliga", "1. division"],
    "sweden": ["allsvenskan", "superettan"],
    "norway": ["eliteserien", "obos-ligaen", "1. divisjon"],
    "finland": ["veikkausliiga", "ykkonen"],
    "poland": ["ekstraklasa", "i liga"],
    "greece": ["super league", "super league 2"],
    "ukraine": ["premier league", "persha liga"],
    "russia": ["premier league", "fnn", "1. division"],
    "brazil": ["serie a", "serie b"],
    "argentina": ["primera division", "primera nacional"],
    "saudi arabia": ["pro league", "first division"],
    "usa": ["mls", "usl championship"],
    "mexico": ["liga mx", "liga de expansion mx"],
    "japan": ["j1 league", "j2 league"],
    "south korea": ["k league 1", "k league 2"],
    "china": ["super league", "china league one"],
    "australia": ["a-league", "a league"],
    "europe": ["champions league", "europa league", "conference league"],
    "world": ["world cup", "nations league"],
    "international": ["nations league", "world cup", "euro"],
}

# Ülke adı -> Türkçe/İngilizce eşleşme
ULKE_ESLESME = {
    "turkey": ["turkey", "türkiye", "turkiye"],
    "italy": ["italy", "italya"],
    "spain": ["spain", "ispanya"],
    "england": ["england", "ingiltere", "i̇ngiltere"],
    "germany": ["germany", "almanya"],
    "france": ["france", "fransa"],
    "netherlands": ["netherlands", "hollanda"],
    "portugal": ["portugal", "portekiz"],
    "belgium": ["belgium", "belçika", "belcika"],
    "scotland": ["scotland"],
    "austria": ["austria", "avusturya"],
    "switzerland": ["switzerland", "isviçre", "isvicre"],
    "croatia": ["croatia", "hırvatistan", "hirvatistan"],
    "serbia": ["serbia", "sırbistan", "sirbistan"],
    "denmark": ["denmark", "danimarka"],
    "sweden": ["sweden", "i̇sveç", "isveç", "isvec"],
    "norway": ["norway", "norveç", "norvec"],
    "finland": ["finland", "finlandiya"],
    "poland": ["poland", "polonya"],
    "greece": ["greece", "yunanistan"],
    "ukraine": ["ukraine", "ukrayna"],
    "russia": ["russia", "rusya"],
    "brazil": ["brazil", "brezilya"],
    "argentina": ["argentina", "arjantin"],
    "saudi arabia": ["saudi arabia", "suudi arabistan", "saudi"],
    "usa": ["usa", "abd", "united states"],
    "mexico": ["mexico", "meksika"],
    "japan": ["japan", "japonya"],
    "south korea": ["south korea", "güney kore", "guney kore"],
    "china": ["china", "çin", "cin"],
    "australia": ["australia", "avustralya"],
    "europe": ["europe", "avrupa", "uefa"],
    "world": ["world", "dünya", "dunya", "fifa"],
    "international": ["international", "uluslararası", "uluslararasi"],
}

YASAKLI_KELIMELER = {
    "women", "womens", "women's", "kadın", "kadin", "female", "ladies", "kizlar", "kızlar", "kiz", "kız",
    "u15", "u16", "u17", "u18", "u19", "u20", "u21", "u22", "u23",
    "youth", "genç", "genc", "gençlik", "genclik",
    "friendly", "friendlies", "hazırlık", "hazirlik",
    "reserve", "reserves", "yedek",
    "academy", "akademi",
    "b team", "ii team",
}

def _lig_adi_bul(metin):
    """Metinden lig adını çıkarır (Standings satırından)."""
    m = re.search(r'Standings\s+([^\n]+)', metin)
    if not m: return ""
    return m.group(1).strip().lower()

def _ulke_bul_lig_ile(metin):
    """Metinden ülkeyi bulur ve lig adını döndürür."""
    lig = _lig_adi_bul(metin)
    ulke = _ulke_bul(metin) or ""
    return ulke, lig

def _ulke_izinli_mi(ulke, takim_ev="", takim_dep=""):
    """
    Sadece 1. ve 2. ligleri kabul eder. Diğer tüm ligleri reddeder.
    """
    if not ulke: return False
    u = str(ulke).strip().lower()
    if not u: return False
    
    # Yasaklı kelimeler kontrolü (kadın, genç, hazırlık vb.)
    tum_metin = f"{u} {takim_ev} {takim_dep}".lower()
    for yasak in YASAKLI_KELIMELER:
        if yasak in tum_metin: return False
    
    # Hangi ülkeye ait olduğunu bul
    bulunan_ulke = None
    for anahtar, eslesmeler in ULKE_ESLESME.items():
        for es in eslesmeler:
            if es in u:
                bulunan_ulke = anahtar
                break
        if bulunan_ulke: break
    
    if not bulunan_ulke: return False
    
    # O ülkenin izinli ligleri var mı?
    if bulunan_ulke not in LIG_FILTRESI: return False
    
    # Lig adını kontrol et
    # Not: _ulke_izinli_mi sadece ülke alıyor, lig adı ayrıca kontrol edilmeli
    # Bu yüzden bu fonksiyonu güncelleyip lig adını da alacak şekilde düzenliyoruz.
    return True

# YENİ: Lig adı da kontrol eden fonksiyon
def _lig_izinli_mi(ulke, lig_adi, takim_ev="", takim_dep=""):
    """
    Ülke + lig adı kombinasyonunu kontrol eder.
    Sadece 1. ve 2. ligleri kabul eder.
    """
    if not ulke: return False
    u = str(ulke).strip().lower()
    l = str(lig_adi).strip().lower() if lig_adi else ""
    
    # Yasaklı kelimeler kontrolü
    tum_metin = f"{u} {l} {takim_ev} {takim_dep}".lower()
    for yasak in YASAKLI_KELIMELER:
        if yasak in tum_metin: return False
    
    # Hangi ülkeye ait olduğunu bul
    bulunan_ulke = None
    for anahtar, eslesmeler in ULKE_ESLESME.items():
        for es in eslesmeler:
            if es in u:
                bulunan_ulke = anahtar
                break
        if bulunan_ulke: break
    
    if not bulunan_ulke: return False
    
    # O ülkenin izinli ligleri var mı?
    if bulunan_ulke not in LIG_FILTRESI: return False
    
    izinli_ligler = LIG_FILTRESI[bulunan_ulke]
    
    # Lig adı boşsa reddet (güvenlik)
    if not l: return False
    
    # Lig adı izinli liglerden birini içeriyor mu?
    for izinli in izinli_ligler:
        if izinli in l: return True
    
    return False

if "sayfa" not in st.session_state: st.session_state.sayfa = "giris"
if "form_verileri" not in st.session_state: st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
if "gecmis_analizler" not in st.session_state: st.session_state.gecmis_analizler = gecmis_yukle()
if "gelecek_analizler" not in st.session_state: st.session_state.gelecek_analizler = gelecek_yukle()
if "kayit_yapildi" not in st.session_state: st.session_state.kayit_yapildi = False
if "gecmisten_gelindi" not in st.session_state: st.session_state.gecmisten_gelindi = False
if "gelecekten_gelindi" not in st.session_state: st.session_state.gelecekten_gelindi = False
if "silme_onay" not in st.session_state: st.session_state.silme_onay = False
if "silme_onay_gelecek" not in st.session_state: st.session_state.silme_onay_gelecek = False
if "aktif_kayit_idx" not in st.session_state: st.session_state.aktif_kayit_idx = None
if "aktif_gelecek_idx" not in st.session_state: st.session_state.aktif_gelecek_idx = None
if "okunamayan_alanlar" not in st.session_state: st.session_state.okunamayan_alanlar = []
if "manuel_bekleyen" not in st.session_state: st.session_state.manuel_bekleyen = []
if "tek_silme_onay" not in st.session_state: st.session_state.tek_silme_onay = None
if "tek_silme_gelecek" not in st.session_state: st.session_state.tek_silme_gelecek = None
if "giris_yapildi" not in st.session_state: st.session_state.giris_yapildi = True
if "rol" not in st.session_state: st.session_state.rol = "misafir"
if "admin_login_acik" not in st.session_state: st.session_state.admin_login_acik = False
if "esikler" not in st.session_state: st.session_state.esikler = ayarlar_yukle()
if "bt_sonuc" not in st.session_state: st.session_state.bt_sonuc = None
if "toplu_cek_ozet" not in st.session_state: st.session_state.toplu_cek_ozet = None
if "skor_ozet" not in st.session_state: st.session_state.skor_ozet = None
if "aktif_kullanici" not in st.session_state: st.session_state.aktif_kullanici = None
if "odeme_hedef_kadi" not in st.session_state: st.session_state.odeme_hedef_kadi = None
if "sil_onay_kadi" not in st.session_state: st.session_state.sil_onay_kadi = None

def admin_mi(): return st.session_state.get("rol") == "admin"
def uye_mi(): return st.session_state.get("aktif_kullanici") is not None
def uye_adi(): return st.session_state.get("aktif_kullanici", "")
def uye_premium_mu():
    if not uye_mi(): return False
    return abonelik_aktif_mi(uye_adi())

def esik_al(key):
    try:
        v = st.session_state.esikler.get(key)
        if v is not None: return v
    except Exception: pass
    return _ESIK_CACHE.get(key, 50.0)

def esik_1x2_al(secim):
    km = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}; k = km.get(secim, "")
    try:
        v = st.session_state.esikler.get(k)
        if v is not None: return v
    except Exception: pass
    return _ESIK_CACHE.get(k, 55.0)

def ayar_al(key, default=None):
    try: return st.session_state.esikler.get(key, default)
    except Exception: return default

ULKE_BAYRAK = {"switzerland": "🇨🇭", "isviçre": "🇨🇭", "england": "🏴", "ingiltere": "🏴", "spain": "🇪🇸", "ispanya": "🇪🇸", "italy": "🇮🇹", "italya": "🇮🇹", "germany": "🇩🇪", "almanya": "🇩🇪", "france": "🇫🇷", "fransa": "🇫🇷", "netherlands": "🇳🇱", "hollanda": "🇳🇱", "portugal": "🇵🇹", "portekiz": "🇵🇹", "belgium": "🇧🇪", "belçika": "🇧🇪", "turkey": "🇹🇷", "türkiye": "🇹🇷", "argentina": "🇦🇷", "arjantin": "🇦🇷", "brazil": "🇧🇷", "brezilya": "🇧🇷", "mexico": "🇲🇽", "meksika": "🇲🇽", "usa": "🇺🇸", "abd": "🇺🇸", "japan": "🇯🇵", "japonya": "🇯🇵", "south korea": "🇰🇷", "güney kore": "🇰🇷", "china": "🇨🇳", "çin": "🇨🇳", "russia": "🇷🇺", "rusya": "🇷🇺", "ukraine": "🇺🇦", "ukrayna": "🇺🇦", "poland": "🇵🇱", "polonya": "🇵🇱", "greece": "🇬🇷", "yunanistan": "🇬🇷", "scotland": "🏴", "wales": "🏴", "ireland": "🇮🇪", "austria": "🇦🇹", "avusturya": "🇦🇹", "croatia": "🇭🇷", "hırvatistan": "🇭🇷", "serbia": "🇷🇸", "sırbistan": "🇷🇸", "denmark": "🇩🇰", "danimarka": "🇩🇰", "sweden": "🇸🇪", "norway": "🇳🇴", "norveç": "🇳🇴", "finland": "🇫🇮", "finlandiya": "🇫🇮", "iceland": "🇮🇸", "hungary": "🇭🇺", "macaristan": "🇭🇺", "czech": "🇨🇿", "slovakia": "🇸🇰", "slovenia": "🇸🇮", "saudi": "🇸🇦", "suudi arabistan": "🇸🇦", "australia": "🇦🇺", "avustralya": "🇦🇺"}

def ulke_bayrak_bul(ulke_adi):
    if not ulke_adi: return "🌍"
    u = ulke_adi.lower().strip()
    for a in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if a in u: return ULKE_BAYRAK[a]
    return "🌍"

def _ulke_bul(metin):
    m = re.search(r'Standings\s+([^\n]+)', metin)
    if not m: return ""
    s = m.group(1).strip()
    if not s: return ""
    alt = s.lower()
    for a in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if a in alt: return a
    p = s.split(); return " ".join(p[:2]) if len(p) >= 2 else (p[0] if p else "")

def clamp(x, lo, hi): return max(lo, min(hi, x))

def guven_seviyesi_bul(o):
    if o >= ESIK_YUKSEK: return ("yuksek", "🟢", "Yüksek")
    if o >= ESIK_ORTA: return ("orta", "🟡", "Orta")
    if o >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "Belirsiz")
    return ("cok_dusuk", "⚫", "Düşük")

def poisson_pmf(k, lam):
    if lam <= 0: return 1.0 if k == 0 else 0.0
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)

def poisson_random(lam, rng=None):
    r = rng if rng is not None else random
    if lam <= 0: return 0
    L = math.exp(-lam); k = 0; p = 1.0
    while True:
        k += 1; p *= r.random()
        if p <= L: return k - 1

def poisson_matris(lam_ev, lam_dep, mg=MAX_GOL):
    return [[poisson_pmf(i, lam_ev) * poisson_pmf(j, lam_dep) for j in range(mg)] for i in range(mg)]

def hesapla_lambda(v):
    if v.get("son5_xg_atak", 0) > 0:
        ae = v.get("son5_xg_atak", 0.0); ye = v.get("son5_xg_savunma", 0.0)
        ad = v.get("son5_xg_atak", 0.0); yd = v.get("son5_xg_savunma", 0.0)
    else:
        ae = v.get("atilan_ev", 0.0); ye = v.get("yenen_ev", 0.0)
        ad = v.get("atilan_dep", 0.0); yd = v.get("yenen_dep", 0.0)
    he = ae if ae > 0 else 1.2
    hd = ad if ad > 0 else 1.0
    tse = v.get("team_scored_ev", 0); tsd = v.get("team_scored_dep", 0)
    if tse > 0: he *= clamp(tse / 60, 0.7, 1.3)
    if tsd > 0: hd *= clamp(tsd / 60, 0.7, 1.3)
    sd = yd if yd > 0 else 1.2; se = ye if ye > 0 else 1.0
    cse = v.get("son5_cs_yuzde", v.get("clean_sheets_ev", 0.0))
    csd = v.get("son5_cs_yuzde", v.get("clean_sheets_dep", 0.0))
    def cf(cs):
        if cs <= 0: return 1.0
        if cs < 40.0: return 1.0 - (cs / 250.0)
        return max(0.40, 0.84 - (cs - 40.0) * (0.44 / 60.0))
    df = cf(cse); ef = cf(csd)
    le = he * 0.60 + sd * 0.40; ld = hd * 0.60 + se * 0.40
    u25e = v.get("son5_ust25_yuzde", v.get("ust25_ev", 0))
    u25d = v.get("son5_ust25_yuzde", v.get("ust25_dep", 0))
    if u25e > 0: le *= clamp(u25e / 50, 0.85, 1.15)
    if u25d > 0: ld *= clamp(u25d / 50, 0.85, 1.15)
    kge = v.get("son5_btts_yuzde", v.get("kg_siklik_ev", 0))
    kgd = v.get("son5_btts_yuzde", v.get("kg_siklik_dep", 0))
    if kge > 0 and kgd > 0:
        ko = (kge + kgd) / 2
        if ko >= 60: le *= 1.05; ld *= 1.05
        elif ko <= 35: le *= 0.95; ld *= 0.95
    fe = clamp(1 + (v.get("ppg_ev", 1.5) - 1.5) / 15, 0.85, 1.15)
    fd = clamp(1 + (v.get("mpg_dep", 1.5) - 1.5) / 15, 0.85, 1.15)
    se_s = v.get("siralama_ev", 10); sd_s = v.get("siralama_dep", 10)
    dom = 1.20 if (1 <= se_s <= 5 and sd_s >= 10) else 1.0
    ge = v.get("galibiyet_ev", 0); gd = v.get("galibiyet_dep", 0)
    if ge > 0 and gd > 0:
        if ge - gd >= 25: le *= 1.08; ld *= 0.95
        elif gd - ge >= 25: le *= 0.95; ld *= 1.08
    le = le * 1.05 * fe * ef * dom; ld = ld * 0.95 * fd * df
    if le > 2.50: le = 2.50 + (le - 2.50) * 0.5
    if ld > 2.50: ld = 2.50 + (ld - 2.50) * 0.5
    return clamp(le, 0.05, 4.5), clamp(ld, 0.05, 4.5), 0.80

def matristen_olasilik(matris, mg=MAX_GOL):
    p1 = px = p2 = u05 = u15 = u25 = u35 = kg = 0.0; sk = {}; tot = 0.0
    for i in range(mg):
        for j in range(mg):
            p = matris[i][j]; tot += p
            if i > j: p1 += p
            elif i == j: px += p
            else: p2 += p
            tg = i + j
            if tg > 0.5: u05 += p
            if tg > 1.5: u15 += p
            if tg > 2.5: u25 += p
            if tg > 3.5: u35 += p
            if i > 0 and j > 0: kg += p
            sk[f"{i}-{j}"] = p
    return {"1": p1, "X": px, "2": p2, "ust_05": u05, "ust_15": u15, "ust_25": u25, "ust_35": u35, "kg_var": kg, "skorlar": sk, "toplam": tot}

def veri_yeterli_mi(v):
    o = [v.get("atilan_ev", 0), v.get("atilan_dep", 0), v.get("yenen_ev", 0), v.get("yenen_dep", 0)]
    return sum(1 for x in o if x > 0) >= 2

def mac_ici_sok(le, ld, rng=None):
    r = rng if rng is not None else random
    if r.random() < 0.03:
        if r.random() < 0.5: le *= 0.70
        else: ld *= 0.70
    return le, ld

def monte_carlo_simulasyon(leb, ldb, n=MONTE_CARLO_N):
    seed = int(round(leb * 1_000_000)) * 1_000_003 + int(round(ldb * 1_000_000))
    rng = random.Random(seed)
    s = {"1": 0, "X": 0, "2": 0, "u25": 0, "kg": 0}
    for _ in range(n):
        le = leb * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        ld = ldb * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        le, ld = mac_ici_sok(le, ld, rng)
        eg = min(MAX_GOL - 1, poisson_random(le, rng))
        dg = min(MAX_GOL - 1, poisson_random(ld, rng))
        if eg > dg: s["1"] += 1
        elif eg == dg: s["X"] += 1
        else: s["2"] += 1
        if eg + dg > 2.5: s["u25"] += 1
        if eg > 0 and dg > 0: s["kg"] += 1
    def yz(x): return x / n * 100 if n > 0 else 0
    return {"p1": yz(s["1"]), "px": yz(s["X"]), "p2": yz(s["2"]), "ust25": yz(s["u25"]), "alt25": 100 - yz(s["u25"]), "kg_var": yz(s["kg"]), "kg_yok": 100 - yz(s["kg"]), "n": n}

def analiz_hesapla(v):
    le, ld, gv = hesapla_lambda(v)
    matris = poisson_matris(le, ld, MAX_GOL)
    o = matristen_olasilik(matris, MAX_GOL)
    tot = o["toplam"] or 1
    p1p = o["1"] / tot * 100; pxp = o["X"] / tot * 100; p2p = o["2"] / tot * 100
    u25p = o["ust_25"] / tot * 100; kgp = o["kg_var"] / tot * 100
    mc = monte_carlo_simulasyon(le, ld, MONTE_CARLO_N)
    lu = v.get("lig_ust25", 0.0); lk = v.get("lig_kg", 0.0)
    p1 = p1p * 0.60 + mc["p1"] * 0.40
    px = pxp * 0.60 + mc["px"] * 0.40
    p2 = p2p * 0.60 + mc["p2"] * 0.40
    ge = v.get("galibiyet_ev", 0); gd = v.get("galibiyet_dep", 0)
    if ge > 0 and gd > 0:
        p1 = p1 * 0.85 + ge * 0.15; p2 = p2 * 0.85 + gd * 0.15
    be = v.get("beraberlik_ev", 0); bd = v.get("beraberlik_dep", 0)
    if be > 0 and bd > 0: px = px * 0.85 + ((be + bd) / 2) * 0.15
    t = p1 + px + p2
    if t > 0: p1, px, p2 = (p1 / t) * 100, (px / t) * 100, (p2 / t) * 100
    u25 = u25p * 0.60 + lu * 0.10 + mc["ust25"] * 0.30 if lu > 0 else u25p * 0.65 + mc["ust25"] * 0.35
    kgm = kgp * 0.40 + lk * 0.30 + mc["kg_var"] * 0.30 if lk > 0 else kgp * 0.60 + mc["kg_var"] * 0.40
    kge = v.get("kg_siklik_ev", 0); kgd = v.get("kg_siklik_dep", 0)
    if kge > 0 and kgd > 0: kgm = kgm * 0.85 + ((kge + kgd) / 2) * 0.15
    tbg = le + ld
    if tbg < 1.80:
        bf = (1.80 - tbg) / 1.80
        u25 = max(10.0, u25 * (1.0 - bf * 0.8))
        kgm = max(15.0, kgm * (1.0 - bf * 0.9))
    kgy = 100.0 - kgm; alt = 100.0 - u25
    eo = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    eg = max([("1X", p1 + px), ("X2", p2 + px), ("12", p1 + p2)], key=lambda x: x[1])
    return {"lam_ev": le, "lam_dep": ld, "guven": gv, "p1": p1, "px": px, "p2": p2, "ust_25": u25, "alt_25": alt, "kg_var_model": kgm, "kg_yok_model": kgy, "en_olasi": eo, "en_guvenli": eg, "en_olasi_gol": "Üst" if u25 > alt else "Alt", "en_olasi_kg": "Var" if kgm > kgy else "Yok"}

def kayit_olustur(v, a):
    return {"veri": copy.deepcopy(v), "analiz": {"p1": a["p1"], "px": a["px"], "p2": a["p2"], "tahmini_gol": a["lam_ev"] + a["lam_dep"], "kg_var_model": a["kg_var_model"], "ust_25": a["ust_25"], "en_olasi_1x2": a["en_olasi"][0], "en_guvenli_cifte": a["en_guvenli"][0], "en_olasi_gol": a["en_olasi_gol"], "en_olasi_kg": a["en_olasi_kg"]}}

def sonuc_hesapla(kayit):
    v = kayit["veri"]; a = kayit.get("analiz", {})
    if not v.get("skor_belli", False): return None
    se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    tg = se + sd; gu = tg > 2.5; gk = (se > 0 and sd > 0)
    g1 = "1" if se > sd else ("X" if se == sd else "2")
    u25 = a.get("ust_25", 50); alt = 100 - u25
    kgv = a.get("kg_var_model", 50); kgy = 100 - kgv
    p1a = a.get("p1", 33.33); pxa = a.get("px", 33.33); p2a = a.get("p2", 33.34)
    s1, y1 = max([("1", p1a), ("X", pxa), ("2", p2a)], key=lambda x: x[1])
    o1 = s1 if y1 >= esik_1x2_al(s1) else None
    og = None
    if u25 >= esik_al("ust") and u25 >= alt: og = "Üst"
    elif alt >= esik_al("alt") and alt >= u25: og = "Alt"
    okg = None
    if kgv >= esik_al("kg_var") and kgv >= kgy: okg = "Var"
    elif kgy >= esik_al("kg_yok") and kgy >= kgv: okg = "Yok"
    def _t(o, g):
        if o is None: return None, None
        d = "tam" if o == g else "yanlis"; return d == "tam", d
    t1, d1 = _t(o1, g1); tg_, dg_ = _t(og, "Üst" if gu else "Alt"); tk, dk = _t(okg, "Var" if gk else "Yok")
    return {"oneri_1x2": {"tahmin": o1, "tuttu": t1, "durum": d1}, "oneri_gol": {"tahmin": og, "tuttu": tg_, "durum": dg_}, "oneri_kg": {"tahmin": okg, "tuttu": tk, "durum": dk}, "gercek_1x2": g1, "gercek_gol": "Üst" if gu else "Alt", "gercek_kg": "Var" if gk else "Yok"}

def _form_ppg(s):
    return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1)

def yeniden_analiz(v):
    v2 = copy.deepcopy(v)
    if v2.get("form_str_ev"): v2["ppg_ev"] = _form_ppg(v2["form_str_ev"])
    if v2.get("form_str_dep"): v2["mpg_dep"] = _form_ppg(v2["form_str_dep"])
    a = analiz_hesapla(v2)
    return {"ust_25": a["ust_25"], "kg_var_model": a["kg_var_model"], "p1": a["p1"], "px": a["px"], "p2": a["p2"]}

def backtest_hesapla(gecmis, ms, me):
    sonuc = {"1x2": {"dogru": 0, "yanlis": 0}, "kg_var": {"dogru": 0, "yanlis": 0}, "kg_yok": {"dogru": 0, "yanlis": 0}, "ust": {"dogru": 0, "yanlis": 0}, "alt": {"dogru": 0, "yanlis": 0}}
    detaylar = []
    for g in gecmis:
        try:
            v = g["veri"]; analiz = g.get("analiz", {})
            if not v.get("skor_belli", False): continue
            se = int(v.get("skor_ev", 0)); sd = int(v.get("skor_dep", 0))
            tg = se + sd; gkv = (se > 0 and sd > 0); gust = tg > 2.5
            g1 = "1" if se > sd else ("X" if se == sd else "2")
            ya = yeniden_analiz(v)
            u25 = ya["ust_25"]; kgv = ya["kg_var_model"]
            p1y = ya["p1"]; pxy = ya["px"]; p2y = ya["p2"]
            alt = 100 - u25; kgy = 100 - kgv
            mk = {"takim_ev": v.get("takim_ev", "Ev"), "takim_dep": v.get("takim_dep", "Dep"), "skor": f"{se}-{sd}", "detaylar": []}
            if ms.get("1x2", False):
                s, y = max([("1", p1y), ("X", pxy), ("2", p2y)], key=lambda x: x[1])
                ek = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}[s]; esc = me.get(ek, 55.0)
                if y >= esc:
                    if s == g1: sonuc["1x2"]["dogru"] += 1; mk["detaylar"].append(f"1X2: {s} ✅")
                    else: sonuc["1x2"]["yanlis"] += 1; mk["detaylar"].append(f"1X2: {s} ❌")
            if ms.get("kg_var", False) and kgv >= me["kg_var"] and kgv >= kgy:
                if gkv: sonuc["kg_var"]["dogru"] += 1
                else: sonuc["kg_var"]["yanlis"] += 1
            if ms.get("kg_yok", False) and kgy >= me["kg_yok"] and kgy >= kgv:
                if not gkv: sonuc["kg_yok"]["dogru"] += 1
                else: sonuc["kg_yok"]["yanlis"] += 1
            if ms.get("ust", False) and u25 >= me["ust"] and u25 >= alt:
                if gust: sonuc["ust"]["dogru"] += 1
                else: sonuc["ust"]["yanlis"] += 1
            if ms.get("alt", False) and alt >= me["alt"] and alt >= u25:
                if not gust: sonuc["alt"]["dogru"] += 1
                else: sonuc["alt"]["yanlis"] += 1
            if mk["detaylar"]: detaylar.append(mk)
        except Exception: continue
    return sonuc, detaylar

def _cift_tab(etiket, blok):
    pattern = r'([\d.,]+)%?\s*\t\s*' + re.escape(etiket) + r'\s*\t\s*([\d.,]+)%?'
    m = re.search(pattern, blok, re.IGNORECASE)
    if m:
        try: return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError: pass
    return None, None

def _sira_bul(metin, takim_adi):
    if not takim_adi: return None, None
    pattern = (r'(?:^|\n)\s*(\d{1,2})\s*\r?\n\s*' + re.escape(takim_adi) + r'\s*\r?\n\s*' + re.escape(takim_adi) + r'\s*\r?\n' r'\s*(\d+)\s*\t')
    m = re.search(pattern, metin, re.MULTILINE)
    if m:
        try:
            sira = int(m.group(1))
            if 1 <= sira <= 30: return sira, 0
        except (ValueError, AttributeError): pass
    return None, None
    
# ===== YENİ EKLENEN FONKSİYON =====
def son_5_mac_analizi_yap(metin):
    """
    Metin içindeki maç skorlarını bulur, ilk 5'ini (en güncel 5 maç) alır
    ve xG, PPG, MPG, BTTS, 2.5 Üst/Alt ve Clean Sheet yüzdelerini hesaplar.
    """
    sonuc = {
        "son5_xg_atak": 0.0, "son5_xg_savunma": 0.0, "son5_ppg": 0.0, 
        "son5_btts_yuzde": 0.0, "son5_ust25_yuzde": 0.0, "son5_cs_yuzde": 0.0
    }
    
    skorlar = re.findall(r'(?<![\d\.])(\d{1,2})\s*-\s*(\d{1,2})(?![\d\.])', metin)
    gecerli_skorlar = []
    for skor in skorlar:
        try:
            ev_gol = int(skor[0]); dep_gol = int(skor[1])
            if ev_gol <= 10 and dep_gol <= 10:
                gecerli_skorlar.append((ev_gol, dep_gol))
        except: continue
            
    if len(gecerli_skorlar) < 5:
        alt = re.findall(r'FT\s*\r?\n\s*(\d+)\s*-\s*(\d+)', metin)
        for ev, dep in alt:
            gecerli_skorlar.append((int(ev), int(dep)))
            
    son_5 = gecerli_skorlar[:5]
    if len(son_5) < 5: return sonuc
        
    toplam_atilan = 0; toplam_yenilen = 0; toplam_puan = 0
    btts_sayisi = 0; ust25_sayisi = 0; clean_sheet_sayisi = 0
    
    for ev_gol, dep_gol in son_5:
        toplam_atilan += ev_gol; toplam_yenilen += dep_gol
        if ev_gol > dep_gol: toplam_puan += 3
        elif ev_gol == dep_gol: toplam_puan += 1
        if ev_gol > 0 and dep_gol > 0: btts_sayisi += 1
        if (ev_gol + dep_gol) > 2.5: ust25_sayisi += 1
        if dep_gol == 0: clean_sheet_sayisi += 1
            
    sonuc["son5_xg_atak"] = toplam_atilan / 5
    sonuc["son5_xg_savunma"] = toplam_yenilen / 5
    sonuc["son5_ppg"] = toplam_puan / 5
    sonuc["son5_btts_yuzde"] = (btts_sayisi / 5) * 100
    sonuc["son5_ust25_yuzde"] = (ust25_sayisi / 5) * 100
    sonuc["son5_cs_yuzde"] = (clean_sheet_sayisi / 5) * 100
    return sonuc


def sportytrader_veri_cikar(metin):
    veri = {}; okunamayanlar = []
    m = re.search(r'^([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s*-\s*([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s+Stats', metin, re.MULTILINE)
    if m:
        veri["takim_ev"] = m.group(1).strip(); veri["takim_dep"] = m.group(2).strip()
    m = re.search(r'Time\s*\t\s*(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1).strip()
    m = re.search(r'Date\s*\t\s*(\d{1,2}\.\d{1,2}\.\d{2,4})', metin)
    if m: veri["tarih"] = m.group(1).strip()
    veri["ulke"] = _ulke_bul(metin)
    m = re.search(r'FT\s*\r?\n\s*(\d+)\s*-\s*(\d+)', metin)
    if m:
        veri["skor_ev"] = int(m.group(1)); veri["skor_dep"] = int(m.group(2)); veri["skor_belli"] = True
    else: veri["skor_belli"] = False
    takim_ev = veri.get("takim_ev", ""); takim_dep = veri.get("takim_dep", "")
    idx = metin.find("Main Stats")
    if idx != -1:
        blok = metin[idx:idx+1500]
        v1, v2 = _cift_tab("Goals scored per game", blok)
        if v1 is not None: veri["atilan_ev"] = v1; veri["atilan_dep"] = v2
        v1, v2 = _cift_tab("Goals conceded per game", blok)
        if v1 is not None: veri["yenen_ev"] = v1; veri["yenen_dep"] = v2
        v1, v2 = _cift_tab("Clean sheets", blok)
        if v1 is not None: veri["clean_sheets_ev"] = v1; veri["clean_sheets_dep"] = v2
        v1, v2 = _cift_tab("Team scored", blok)
        if v1 is not None: veri["team_scored_ev"] = v1; veri["team_scored_dep"] = v2
    idx = metin.find("Win Draw Lose")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for etiket, key_ev, key_dep in [("Win", "galibiyet_ev", "galibiyet_dep"), ("Draw", "beraberlik_ev", "beraberlik_dep"), ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
            pattern = r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*' + etiket + r'\s*\t\s*([\d.,]+)%'
            mm = re.search(pattern, blok, re.MULTILINE)
            if mm:
                try:
                    veri[key_ev] = float(mm.group(1).replace(",", "."))
                    veri[key_dep] = float(mm.group(2).replace(",", "."))
                except ValueError: pass
    idx = metin.find("Both Teams to Score")
    if idx != -1:
        blok = metin[idx:idx+1500]
        m = re.search(r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*Both Teams to Score\s*\t\s*([\d.,]+)%', blok, re.MULTILINE)
        if m:
            try:
                veri["kg_siklik_ev"] = float(m.group(1).replace(",", "."))
                veri["kg_siklik_dep"] = float(m.group(2).replace(",", "."))
            except ValueError: pass
    idx = metin.find("Over Under Goals")
    if idx != -1:
        blok = metin[idx:idx+1500]
        v1, v2 = _cift_tab("Over 1.5 goals", blok)
        if v1 is not None: veri["ust15_ev"] = v1; veri["ust15_dep"] = v2
        v1, v2 = _cift_tab("Over 2.5 goals", blok)
        if v1 is not None: veri["ust25_ev"] = v1; veri["ust25_dep"] = v2
        v1, v2 = _cift_tab("Over 3.5 goals", blok)
        if v1 is not None: veri["ust35_ev"] = v1; veri["ust35_dep"] = v2
    if takim_ev:
        s, p = _sira_bul(metin, takim_ev)
        if s is not None: veri["siralama_ev"] = s
    if takim_dep:
        s, p = _sira_bul(metin, takim_dep)
        if s is not None: veri["siralama_dep"] = s
    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) + veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2
    try:
        m_form = re.search(
            r'(?:^|\n)\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*Form\b[\s\S]{0,20}?\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])',
            metin, re.MULTILINE
        )
        if m_form:
            veri["form_str_ev"] = "".join(m_form.group(i) for i in range(1, 6))
            veri["form_str_dep"] = "".join(m_form.group(i) for i in range(6, 11))
    except Exception: pass
    try:
        for taraf_k, taraf in [("trends_ev", takim_ev), ("trends_dep", takim_dep)]:
            if not taraf: continue
            idx_t = metin.find(f"{taraf} Trends")
            if idx_t == -1: idx_t = metin.find(f"{taraf} trends")
            if idx_t != -1:
                blok_t = metin[idx_t:idx_t + 900]
                cumleler = re.findall(r'([A-Z][a-zA-Z\s]+?[^\n\.]{5,180}\.)', blok_t)
                temiz = []
                for c in cumleler:
                    c = c.strip()
                    if not c: continue
                    if "trends last games" in c.lower(): continue
                    if taraf.lower() not in c.lower(): continue
                    temiz.append(c)
                if temiz: veri[taraf_k] = temiz[:5]
    except Exception: pass
    
    son5_veri = son_5_mac_analizi_yap(metin)
    veri.update(son5_veri)
    
    veri["format"] = "sportytrader"
    return veri, okunamayanlar


def metinden_veri_cikar(metin):
    metin = metin.replace(",", ".")
    if "Main Stats" in metin and "Goals scored per game" in metin:
        veri, okunamayanlar = sportytrader_veri_cikar(metin)
        if veri.get("saat"): veri["saat"] = saat_2_saat_ileri(veri["saat"])
        return veri, okunamayanlar
    veri = {}; okunamayanlar = []
    veri["format"] = "genel"
    return veri, okunamayanlar


# ==========================================
# VERİ ÇEKME MOTORU
# ==========================================
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
TARAYICI_ESZAMANLI = int(os.environ.get("TARAYICI_ESZAMANLI", "3"))
_TARAYICI_SEM = threading.Semaphore(TARAYICI_ESZAMANLI)


def _playwright_skor_cek(url, timeout=25):
    try:
        import subprocess as _sp, sys as _sys
        _sp.run([_sys.executable, "-m", "playwright", "install", "chromium"], check=False, timeout=600, stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
    except Exception: pass
    from playwright.sync_api import sync_playwright
    with _TARAYICI_SEM:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
            try:
                ctx = b.new_context(user_agent=UA, locale="en-US")
                pg = ctx.new_page()
                pg.route("**/*", lambda route: route.abort() if route.request.resource_type in ("image", "media", "font", "stylesheet") else route.continue_())
                pg.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
                pg.wait_for_timeout(2000)
                return pg.content()
            finally:
                try: b.close()
                except Exception: pass


def _mac_detay_cek_5games_playwright(url, timeout=35):
    try:
        import subprocess as _sp, sys as _sys
        _sp.run([_sys.executable, "-m", "playwright", "install", "chromium"], check=False, timeout=600, stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
    except Exception: pass
    from playwright.sync_api import sync_playwright
    with _TARAYICI_SEM:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
            try:
                ctx = b.new_context(user_agent=UA, locale="en-US")
                pg = ctx.new_page()
                pg.route("**/*", lambda route: route.abort() if route.request.resource_type in ("image", "media", "font", "stylesheet") else route.continue_())
                pg.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
                pg.wait_for_timeout(2500)
                tiklandi = False
                try:
                    tiklandi = pg.evaluate("""() => {
                        const labels = document.querySelectorAll('label.containerbutton, label');
                        for (const lb of labels) {
                            const num = lb.querySelector('.numbergames, .num, span');
                            if (!num) continue;
                            const t = (num.textContent || '').trim();
                            if (t === '5' || t === '5 ') {
                                const inp = lb.querySelector('input[type="radio"]');
                                if (inp) { inp.checked = true; inp.dispatchEvent(new Event('change', { bubbles: true })); inp.dispatchEvent(new Event('input', { bubbles: true })); inp.click(); lb.click(); return true; }
                            }
                        }
                        const inp2 = document.querySelector('input[type="radio"][value="5"]');
                        if (inp2) { inp2.checked = true; inp2.dispatchEvent(new Event('change', { bubbles: true })); inp2.click(); return true; }
                        return false;
                    }""")
                except Exception: tiklandi = False
                if not tiklandi:
                    for sel in ["input[type='radio'][value='5']", "input#game_count_5"]:
                        try:
                            pg.click(sel, timeout=2000); tiklandi = True; break
                        except Exception: continue
                pg.wait_for_timeout(3500)
                return pg.content()
            finally:
                try: b.close()
                except Exception: pass


def _mac_detay_cek_5games(url):
    html = None
    try: html = _mac_detay_cek_5games_playwright(url)
    except Exception: pass
    if html and len(html) > 500: return _mac_html_parse(html, url)
    return mutating_mac_detay_cek(url)


def _scrapingbee_get(url, render_js=True, timeout=30, mac_sec="5", max_retry=3, dogrula=False):
    hata = None
    for d in range(max_retry):
        try:
            r = requests.get(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml", "Accept-Language": "en-US,en;q=0.9", "Connection": "keep-alive"}, timeout=timeout)
            if r.status_code == 200 and r.text and len(r.text) > 500: return r.text, None
            hata = f"HTTP {r.status_code}"
        except Exception as e:
            hata = f"Bağlantı: {str(e)[:150]}"
        if d < max_retry - 1: time.sleep(1 + d)
    return None, hata or "Sayfa alınamadı."


def _html_metne_cevir(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe"]): tag.decompose()
    for td in soup.find_all(["td", "th"]): td.insert_after("\t")
    for tr in soup.find_all("tr"): tr.insert_after("\n")
    for e in soup.find_all(["div", "p", "li", "h1", "h2", "h3", "h4", "br"]): e.insert_after("\n")
    metin = soup.get_text(separator="", strip=False)
    metin = re.sub(r'[ \t]+\n', '\n', metin)
    metin = re.sub(r'\n{3,}', '\n\n', metin)
    return metin


def mutating_ana_sayfa_linklerini_al(max_mac=MAX_MAC_SINIRI):
    html, hata = _scrapingbee_get("https://www.mutating.com/football-stats/", render_js=True)
    if hata: return [], [hata]
    if not html: return [], ["Ana sayfa indirilemedi."]
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gorulen = set()
    for link in soup.find_all("a", href=True):
        if len(maclar) >= max_mac: break
        href = link.get("href", "")
        if not any(x in href for x in ["match-preview", "match/", "/stats/"]): continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gorulen: continue
        gorulen.add(href)
        h2_list = link.find_all("h2")
        takim_ev = h2_list[0].get_text(strip=True) if len(h2_list) > 0 else ""
        takim_dep = h2_list[1].get_text(strip=True) if len(h2_list) > 1 else ""
        saat_el = link.find(class_=re.compile(r"nostart|time|match-time"))
        saat = saat_el.get_text(strip=True) if saat_el else ""
        maclar.append({"url": href, "takim_ev": takim_ev, "takim_dep": takim_dep, "saat": saat})
    return maclar, []


def mutating_mac_detay_cek(url):
    html, hata = _scrapingbee_get(url, render_js=True, mac_sec="5", dogrula=True)
    if hata: return None, [hata]
    if not html: return None, ["Sayfa indirilemedi."]
    return _mac_html_parse(html, url)


def _mac_html_parse(html, url=""):
    soup = BeautifulSoup(html, "html.parser")
    veri = {}; okunamayanlar = []
    h1 = soup.find("h1")
    if h1:
        baslik = h1.get_text(strip=True)
        if " - " in baslik:
            p = baslik.replace(" Stats", "").split(" - ")
            veri["takim_ev"] = p[0].strip()
            if len(p) > 1: veri["takim_dep"] = p[1].strip()
    metin = _html_metne_cevir(html)
    m = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', metin)
    if m: veri["tarih"] = m.group(1)
    m = re.search(r'(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1)
    veri["ulke"] = _ulke_bul(metin)
    skor = _skor_parse(html)
    if skor:
        veri["skor_ev"] = skor[0]; veri["skor_dep"] = skor[1]; veri["skor_belli"] = True
    else: veri["skor_belli"] = False
    def _cift(label):
        for pat in [r'([\d.,]+)\s*%?\s*\t\s*' + re.escape(label) + r'\s*\t\s*([\d.,]+)', r'([\d.,]+)\s*%?\s*\|\s*' + re.escape(label) + r'\s*\|\s*([\d.,]+)', r'([\d.,]+)\s*%?\s+' + re.escape(label) + r'\s+([\d.,]+)\s*%?']:
            mm = re.search(pat, metin, re.IGNORECASE)
            if mm:
                try: return float(mm.group(1).replace(",", ".")), float(mm.group(2).replace(",", "."))
                except ValueError: continue
        return None, None
    for label, k_ev, k_dep in [("Goals scored per game", "atilan_ev", "atilan_dep"), ("Goals conceded per game", "yenen_ev", "yenen_dep"), ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"), ("Team scored", "team_scored_ev", "team_scored_dep"), ("Both Teams to Score", "kg_siklik_ev", "kg_siklik_dep"), ("Over 2.5 goals", "ust25_ev", "ust25_dep")]:
        a, b = _cift(label)
        if a is not None and veri.get(k_ev, 0) == 0: veri[k_ev] = a; veri[k_dep] = b
    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) + veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2
    veri["format"] = "mutating"
    if url: veri["kaynak_url"] = url
    try:
        form_bloklari = re.findall(r'(?:^|\n)\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*(?=\r?\n)', metin, re.MULTILINE)
        if form_bloklari and len(form_bloklari) >= 2:
            veri["form_str_ev"] = "".join(form_bloklari[0])
            veri["form_str_dep"] = "".join(form_bloklari[1])
    except Exception: pass
    son5_veri = son_5_mac_analizi_yap(metin)
    veri.update(son5_veri)
    return veri, okunamayanlar


def _mac_tahmin_var_mi(v, esikler=None):
    try:
        if esikler is None:
            try: esikler = st.session_state.esikler
            except Exception: esikler = {}
        def _e(k, d):
            val = esikler.get(k) if isinstance(esikler, dict) else None
            return val if val is not None else d
        a = analiz_hesapla(v)
        s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
        km = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}
        if y1 >= _e(km[s1], 55.0): return True
        if a["ust_25"] >= _e("ust", 65.0) and a["ust_25"] >= a["alt_25"]: return True
        if a["alt_25"] >= _e("alt", 55.0) and a["alt_25"] >= a["ust_25"]: return True
        if a["kg_var_model"] >= _e("kg_var", 57.0) and a["kg_var_model"] >= a["kg_yok_model"]: return True
        if a["kg_yok_model"] >= _e("kg_yok", 72.0) and a["kg_yok_model"] >= a["kg_var_model"]: return True
        return False
    except Exception: return False


def _inline_skor_tasi_callback(idx):
    try:
        yse_val = int(st.session_state.get(f"ise_{idx}", 0)); ysd_val = int(st.session_state.get(f"isd_{idx}", 0))
        gel_list = st.session_state.get("gelecek_analizler", [])
        if idx < 0 or idx >= len(gel_list): return
        k = gel_list[idx]
        k["veri"]["skor_ev"] = yse_val; k["veri"]["skor_dep"] = ysd_val; k["veri"]["skor_belli"] = True
        yd = sonuc_hesapla(k)
        if yd: k["dogruluk"] = yd
        st.session_state.gecmis_analizler.append(k); st.session_state.gelecek_analizler.pop(idx)
        gecmis_kaydet(st.session_state.gecmis_analizler); gelecek_kaydet(st.session_state.gelecek_analizler)
    except Exception: pass


def _gelecek_mac_isle(mac, mevcut_urls, esikler=None):
    try:
        veri, _ = _mac_detay_cek_5games(mac["url"])
        if not veri: return ("hata", mac, "Veri çekilemedi", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        if not veri.get("saat"): veri["saat"] = mac.get("saat", "")
        if veri.get("saat"): veri["saat"] = saat_2_saat_ileri(veri["saat"])
        veri["kaynak_url"] = mac["url"]
        if not str(veri.get("ulke", "") or "").strip():
            return ("ulke_yok", veri, "Ülke bilgisi yok", None)
        # YENİ: Lig filtresi
        lig_adi = _lig_adi_bul(veri.get("ulke", ""))
        if not _lig_izinli_mi(veri.get("ulke", ""), lig_adi, veri.get("takim_ev", ""), veri.get("takim_dep", "")):
            return ("ulke_yok", veri, "İzin verilmeyen lig/ülke", None)
        if mac["url"] in mevcut_urls: return ("atlandi", veri, "Zaten var", None)
        if _mac_tahmin_var_mi(veri, esikler):
            kayit = kayit_olustur(veri, analiz_hesapla(veri))
            return ("eklendi", veri, "Gelecek'e eklendi", kayit)
        return ("atlandi", veri, "Tahmin yok (eşik altı)", None)
    except Exception as e: return ("hata", mac, str(e), None)


def mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=None, max_workers=2):
    maclar, hatalar = mutating_ana_sayfa_linklerini_al(max_mac=max_mac)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Ana sayfada maç linki bulunamadı."]
    mevcut_urls = set()
    for g in st.session_state.gelecek_analizler:
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut_urls.add(u)
    try: esikler_kopya = dict(st.session_state.esikler)
    except Exception: esikler_kopya = {}
    basarili = []; hatali = []; eklenecekler = []
    eklenen = 0; atlanan = 0; tamamlanan = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_gelecek_mac_isle, m, mevcut_urls, esikler_kopya): m for m in maclar}
        for fut in as_completed(futures):
            tamamlanan += 1
            mac = futures[fut]
            try:
                r = fut.result()
                sonuc, veri, mesaj = r[0], r[1], r[2]
                kayit = r[3] if len(r) == 4 else None
                if sonuc == "ulke_yok": pass
                elif sonuc == "eklendi":
                    eklenen += 1; basarili.append(veri)
                    if kayit is not None: eklenecekler.append(kayit)
                elif sonuc == "atlandi":
                    atlanan += 1; basarili.append(veri)
                else: hatali.append(f"{mac.get('takim_ev','?')}: {mesaj}")
            except Exception as e: hatali.append(f"{mac.get('takim_ev','?')}: {e}")
            if progress_callback:
                try: progress_callback(tamamlanan - 1, len(maclar), mac.get("takim_ev", ""))
                except Exception: pass
    if eklenecekler:
        st.session_state.gelecek_analizler.extend(eklenecekler)
        gelecek_kaydet(st.session_state.gelecek_analizler)
    st.session_state.toplu_cek_ozet = {"eklenen": eklenen, "atlanan": atlanan, "toplam": len(basarili)}
    return basarili, hatali


def _lig_son_mac_linklerini_al(lig_url, adet=10):
    html, hata = _scrapingbee_get(lig_url, render_js=True, mac_sec="10")
    if hata: return [], [hata]
    if not html: return [], ["Lig sayfası indirilemedi."]
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gorulen = set()
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        if "match-preview" not in href: continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gorulen: continue
        gorulen.add(href)
        takim_ev = ""; takim_dep = ""
        img = link.find_all("img", alt=True)
        if len(img) >= 2:
            takim_ev = img[0].get("alt", "").strip(); takim_dep = img[1].get("alt", "").strip()
        maclar.append({"url": href, "takim_ev": takim_ev, "takim_dep": takim_dep})
        if len(maclar) >= adet: break
    return maclar, []


def _gecmis_mac_isle(mac, mevcut_urls):
    try:
        if mac["url"] in mevcut_urls: return ("atlandi", None, "Zaten var", None)
        html, hata = _scrapingbee_get(mac["url"], render_js=True, mac_sec="5", dogrula=True)
        if hata or not html: return ("hata", mac, hata or "HTML yok", None)
        veri, _ = _mac_html_parse(html, mac["url"])
        if not veri.get("skor_belli", False): return ("atlandi", None, "Skor yok", None)
        if veri.get("atilan_ev", 0) == 0 or veri.get("yenen_ev", 0) == 0: return ("atlandi", None, "İstatistik eksik", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        # Lig filtresi
        lig_adi = _lig_adi_bul(veri.get("ulke", ""))
        if not _lig_izinli_mi(veri.get("ulke", ""), lig_adi, veri.get("takim_ev", ""), veri.get("takim_dep", "")):
            return ("ulke_yok", veri, "İzin verilmeyen lig/ülke", None)
        yv = copy.deepcopy(VARSAYILAN_VERI); yv.update(veri)
        kayit = kayit_olustur(yv, analiz_hesapla(yv))
        kayit["dogruluk"] = sonuc_hesapla(kayit)
        return ("eklendi", veri, f"{veri['skor_ev']}-{veri['skor_dep']}", kayit)
    except Exception as e: return ("hata", mac, str(e), None)


def lig_gecmis_cek(lig_url, adet=10, max_workers=2, progress_callback=None):
    maclar, hatalar = _lig_son_mac_linklerini_al(lig_url, adet=adet)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Lig sayfasında maç linki bulunamadı."]
    mevcut_urls = set()
    for g in st.session_state.gecmis_analizler:
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut_urls.add(u)
    basarili = []; hatali = []; eklenecekler = []
    eklenen = 0; atlanan = 0; tamamlanan = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_gecmis_mac_isle, m, mevcut_urls): m for m in maclar}
        for fut in as_completed(futures):
            tamamlanan += 1
            mac = futures[fut]
            try:
                r = fut.result()
                sonuc, veri, mesaj = r[0], r[1], r[2]
                kayit = r[3] if len(r) == 4 else None
                if sonuc == "eklendi":
                    eklenen += 1; basarili.append(veri)
                    if kayit is not None: eklenecekler.append(kayit)
                elif sonuc == "atlandi": atlanan += 1
                else: hatali.append(f"{mac.get('takim_ev','?')}: {mesaj}")
            except Exception as e: hatali.append(f"{mac.get('takim_ev','?')}: {e}")
            if progress_callback:
                try: progress_callback(tamamlanan - 1, len(maclar), mac.get("takim_ev", ""))
                except Exception: pass
    if eklenecekler:
        st.session_state.gecmis_analizler.extend(eklenecekler)
        gecmis_kaydet(st.session_state.gecmis_analizler)
    st.session_state.gecmis_cek_ozet = {"eklenen": eklenen, "atlanan": atlanan}
    return basarili, hatali


def _takim_normalize(isim):
    if not isim: return ""
    s = str(isim).lower().strip()
    s = (s.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c"))
    s = re.sub(r'[^\w\s]', ' ', s)
    for ek in [" fc", " sc", " cf", " sk", " ac", " as"]:
        if s.endswith(ek): s = s[:-len(ek)].strip()
    return re.sub(r'\s+', ' ', s).strip()


def _benzerlik(a, b):
    if not a or not b: return 0.0
    if a == b: return 1.0
    sa, sb = set(a.split()), set(b.split())
    if not sa or not sb: return 0.0
    return len(sa & sb) / len(sa | sb)


def _flashscore_feed_parse(metin):
    maclar = []
    if not metin: return maclar
    for blok in metin.split("¬~"):
        if not blok.strip(): continue
        alanlar = {}
        for parca in blok.split("¬"):
            if "÷" not in parca: continue
            k, _, v = parca.partition("÷")
            if k and k not in alanlar: alanlar[k] = v
        if "AA" not in alanlar or "AE" not in alanlar or "AF" not in alanlar: continue
        se, sd = alanlar.get("AG"), alanlar.get("AH")
        if se in (None, "") or sd in (None, ""): continue
        try: maclar.append({"ev": alanlar["AE"].strip(), "dep": alanlar["AF"].strip(), "skor_ev": int(se), "skor_dep": int(sd), "durum": alanlar.get("AB", "")})
        except (ValueError, TypeError): continue
    return maclar


@st.cache_data(ttl=120, show_spinner=False)
def _flashscore_gun_maclari(day_offset=0):
    url = f"https://global.flashscore.ninja/2/x/feed/f_1_{day_offset}_3_en_1"
    try:
        r = requests.get(url, headers={"x-fsign": "SW9D1eZo", "User-Agent": UA}, timeout=20)
        if r.status_code != 200: return []
        return _flashscore_feed_parse(r.text)
    except Exception: return []


def _flashscore_skor_bul(takim_ev, takim_dep, tarih=""):
    ev_n = _takim_normalize(takim_ev); dep_n = _takim_normalize(takim_dep)
    if not ev_n or not dep_n: return None
    tum = []
    for off in [0]:
        try: tum.extend(_flashscore_gun_maclari(off))
        except Exception: continue
    for m in tum:
        if m.get("durum") != "3": continue
        if _takim_normalize(m["ev"]) == ev_n and _takim_normalize(m["dep"]) == dep_n: return (m["skor_ev"], m["skor_dep"])
    return None


def _skor_parse(html):
    metin = _html_metne_cevir(html)
    m = re.search(r'\bFT\b[\s\r\n:]*(\d{1,2})\s*[-:]\s*(\d{1,2})\b', metin)
    if m: return int(m.group(1)), int(m.group(2))
    return None


def _skor_cek(url, takim_ev="", takim_dep="", tarih="", tarayici_yedek=False):
    if takim_ev and takim_dep:
        try:
            skor = _flashscore_skor_bul(takim_ev, takim_dep, tarih)
            if skor: return skor, None
        except Exception: pass
    html = None; hata = None
    if url:
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
            if r.status_code == 200 and r.text: html = r.text
        except Exception as e: hata = f"Bağlantı: {str(e)[:80]}"
    skor = _skor_parse(html) if html else None
    return skor, (hata if skor is None else None)


def sonuclari_isle(tarayici_yedek=False, max_workers=3, progress_callback=None):
    gel = st.session_state.gelecek_analizler
    isler = [(i, g) for i, g in enumerate(gel) if g.get("veri", {}).get("takim_ev") and g.get("veri", {}).get("takim_dep")]
    sonuc = {}; tamam = 0
    if isler:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            fut = {ex.submit(_skor_cek, g["veri"].get("kaynak_url", ""), g["veri"].get("takim_ev", ""), g["veri"].get("takim_dep", ""), g["veri"].get("tarih", ""), tarayici_yedek): (i, g) for i, g in isler}
            for f in as_completed(fut):
                i, g = fut[f]; tamam += 1
                try: sonuc[i] = f.result()
                except Exception as e: sonuc[i] = (None, str(e)[:80])
                if progress_callback:
                    try: progress_callback(tamam - 1, len(isler), g["veri"].get("takim_ev", ""))
                    except Exception: pass
    mevcut = {x.get("veri", {}).get("kaynak_url") for x in st.session_state.gecmis_analizler}
    tasinan = 0; bitmemis = 0; hatalar = []; kalan = []
    for i, g in enumerate(gel):
        r = sonuc.get(i)
        if r is None: kalan.append(g); continue
        skor, hata = r
        v = g["veri"]; isim = f"{v.get('takim_ev', '?')} - {v.get('takim_dep', '?')}"
        if hata: hatalar.append(f"{isim}: {hata}"); kalan.append(g); continue
        if skor is None: bitmemis += 1; kalan.append(g); continue
        v["skor_ev"], v["skor_dep"], v["skor_belli"] = skor[0], skor[1], True
        d = sonuc_hesapla(g)
        if d: g["dogruluk"] = d
        if v.get("kaynak_url") not in mevcut:
            st.session_state.gecmis_analizler.append(g); mevcut.add(v.get("kaynak_url"))
        tasinan += 1
    st.session_state.gelecek_analizler = kalan
    gecmis_kaydet(st.session_state.gecmis_analizler); gelecek_kaydet(st.session_state.gelecek_analizler)
    return {"tasinan": tasinan, "bitmemis": bitmemis, "hatalar": hatalar, "toplam": len(isler)}


# ==========================================
# TASARIM YARDIMCILARI
# ==========================================
def _e(x): return _html.escape(str(x))


def mac_karti(ev, dep, skor_belli, skor_ev, skor_dep, lam_ev, lam_dep, saat="", ulke="", tarih=""):
    bayrak = ulke_bayrak_bul(ulke); ust = ""
    if saat or ulke or tarih:
        parcalar = []
        if ulke: parcalar.append(f"{bayrak} {(ulke or '').title()}")
        if tarih: parcalar.append(f"📅 {tarih}")
        if saat: parcalar.append(f"🕐 {saat}")
        if parcalar: ust = f'<div style="font-size:0.7rem;color:#7f92b3;margin-bottom:10px;text-align:center;">{" • ".join(parcalar)}</div>'
    skor_html = f'<div style="font-size:1.8rem;font-weight:900;color:#22c55e;">{skor_ev} - {skor_dep}</div>' if skor_belli else '<div style="font-size:1.2rem;font-weight:800;color:#7f92b3;">VS</div>'
    gol = f'<div style="font-size:0.75rem;color:#7f92b3;margin-top:6px;">Model: {lam_ev:.2f} - {lam_dep:.2f}</div>' if (lam_ev > 0 or lam_dep > 0) else ""
    return f"""<div style="background:linear-gradient(145deg,#131c2e,#0f1829);border:1px solid #1f2c44;border-radius:16px;padding:16px;margin:8px 0;">{ust}<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;"><div style="flex:1;text-align:center;font-weight:800;color:#eaf1fb;">{ev}</div><div style="flex:1;text-align:center;">{skor_html}</div><div style="flex:1;text-align:center;font-weight:800;color:#eaf1fb;">{dep}</div></div>{gol}</div>"""


def kilitli_mac_karti(ev, dep, saat="", ulke="", tarih=""):
    return f'''<div style="background:linear-gradient(145deg,#131c2e,#0f1829);border:1px solid #1f2c44;border-radius:16px;padding:16px;margin:8px 0;position:relative;overflow:hidden;opacity:0.7;"><div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:3rem;opacity:0.15;">🔒</div><div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;filter:blur(3px);"><div style="flex:1;text-align:center;font-weight:800;">{ev}</div><div style="flex:1;text-align:center;">VS</div><div style="flex:1;text-align:center;font-weight:800;">{dep}</div></div><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(34,197,94,0.08);z-index:2;"><div style="background:linear-gradient(135deg,#16a34a,#22c55e);color:#04130a;font-weight:900;padding:10px 20px;border-radius:99px;">🔒 PREMIUM'A GEÇ</div></div></div>'''


def mac_tahmin_karti(v_g, g=None):
    try:
        try: ya = yeniden_analiz(v_g)
        except Exception: ya = (g or {}).get("analiz", {})
        p1 = ya.get("p1", 33.33); px = ya.get("px", 33.33); p2 = ya.get("p2", 33.34)
        u25 = ya.get("ust_25", 50); a25 = 100 - u25
        kgv = ya.get("kg_var_model", 50); kgy = 100 - kgv
        s1, y1 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        es1 = esik_1x2_al(s1); poz1 = y1 >= es1
        isim1 = {"1": "1 — Ev Kazanır", "X": "X — Beraberlik", "2": "2 — Dep Kazanır"}[s1]
        if u25 >= a25: gs = "Üst 2.5"; gy = u25; ge_ = esik_al("ust")
        else: gs = "Alt 2.5"; gy = a25; ge_ = esik_al("alt")
        gp = gy >= ge_
        if kgv >= kgy: ks = "KG Var"; ky = kgv; ke = esik_al("kg_var")
        else: ks = "KG Yok"; ky = kgy; ke = esik_al("kg_yok")
        kp = ky >= ke
        def r(p): return "pass" if p else "off"
        return f'''<div style="background:linear-gradient(145deg,#131c2e,#0f1829);border:1px solid #1f2c44;border-radius:12px;padding:8px 12px;margin:-4px 0 8px 0;"><div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px dashed #1d2940;"><span>🎯 1X2</span><span style="font-weight:{'800' if poz1 else '400'};color:{'#22c55e' if poz1 else '#94a3b8'};">{isim1} (%{y1:.0f})</span></div><div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px dashed #1d2940;"><span>⚽ Gol</span><span style="font-weight:{'800' if gp else '400'};color:{'#22c55e' if gp else '#94a3b8'};">{gs} (%{gy:.0f})</span></div><div style="display:flex;justify-content:space-between;padding:6px 0;"><span>🤝 KG</span><span style="font-weight:{'800' if kp else '400'};color:{'#22c55e' if kp else '#94a3b8'};">{ks} (%{ky:.0f})</span></div></div>'''
    except Exception: return ""


def _form_detay(form_str):
    if not form_str: return None
    s = "".join(c for c in str(form_str).upper() if c in "WDL")
    if not s: return None
    return {"W": s.count("W"), "D": s.count("D"), "L": s.count("L"), "n": len(s)}


def _form_hikaye(form_str, takim, ev_mi=True):
    f = _form_detay(form_str)
    if not f: return None
    n, w, d, l = f["n"], f["W"], f["D"], f["L"]
    p = []
    if w: p.append(f"{w} galibiyet")
    if d: p.append(f"{d} beraberlik")
    if l: p.append(f"{l} mağlubiyet")
    detay = ", ".join(p); sinif = "ev" if ev_mi else "dep"
    if w >= n - 1 and n >= 3: ton = "muhteşem bir form yakalamış durumda"
    elif w >= (n + 1) // 2: ton = "iyi bir form grafiği çiziyor"
    elif l >= (n + 1) // 2: ton = "formsuz günler geçiriyor"
    else: ton = "istikrarsız bir görünüm sergiliyor"
    return f"<span style='{sinif}'>{takim}</span> son {n} maçında {detay} alarak {ton}"


def ai_yorum_olustur(v, a):
    te = (v.get("takim_ev", "Ev") or "Ev").strip()
    td = (v.get("takim_dep", "Dep") or "Dep").strip()
    s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    p1 = a["p1"]; px = a["px"]; p2 = a["p2"]
    ust25 = a["ust_25"]; alt25 = a["alt_25"]
    kgvar = a["kg_var_model"]; kgyok = a["kg_yok_model"]
    _es1x = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}[s1]
    _1x2_gec = y1 >= esik_al(_es1x)
    _ust_gec = ust25 >= esik_al("ust") and ust25 >= alt25
    _alt_gec = alt25 >= esik_al("alt") and alt25 >= ust25
    _gol_gec = _ust_gec or _alt_gec
    _kgv_gec = kgvar >= esik_al("kg_var") and kgvar >= kgyok
    _kgy_gec = kgyok >= esik_al("kg_yok") and kgyok >= kgvar
    _kg_gec = _kgv_gec or _kgy_gec
    if not (_1x2_gec or _gol_gec or _kg_gec): return []
    def V(x): return f"<span class='vurgu'>{x}</span>"
    def EV(x): return f"<span class='ev'>{x}</span>"
    def DP(x): return f"<span class='dep'>{x}</span>"
    bolumler = []
    kp = []
    if s1 == "1":
        kp.append(f"Model bu maçta {EV(te)} tarafını yaklaşık {V(f'%{p1:.0f}')} olasılıkla işaret ediyor.")
        kp.append(f"Tüm bunları birleştirdiğimizde <b>1 ({te} Kazanır)</b> demek en mantıklısı oldu.")
    elif s1 == "2":
        kp.append(f"Model bu maçta {DP(td)} tarafını yaklaşık {V(f'%{p2:.0f}')} olasılıkla öne çıkarıyor.")
        kp.append(f"Bu veriler ışığında <b>2 ({td} Kazanır)</b> en mantıklı tercih olarak öne çıkıyor.")
    else:
        kp.append(f"Model bu maçta beraberliği yaklaşık {V(f'%{px:.0f}')} olasılıkla işaret ediyor.")
        kp.append("Bu veriler ışığında <b>X (Beraberlik)</b> en dengeli tercih gibi görünüyor.")
    if kp and _1x2_gec: bolumler.append(("🎯", "NEDEN BU SONUÇ?", " ".join(kp)))
    gp = []
    if ust25 >= alt25:
        gp.append(f"Bu maçta <b>Üst 2.5</b> tarafı ağır basıyor (%{ust25:.1f}).")
        gp.append("Bu yüzden <b>Üst 2.5</b> demek daha mantıklı.")
    else:
        gp.append(f"Bu maçta <b>Alt 2.5</b> tarafı öne çıkıyor (%{alt25:.1f}).")
        gp.append("Tüm bu veriler ışığında <b>Alt 2.5</b> demek daha akıllıca.")
    if gp and _gol_gec: bolumler.append(("⚽", "GOL BEKLENTİSİ", " ".join(gp)))
    kgp = []
    if kgvar >= kgyok:
        kgp.append(f"<b>Karşılıklı Gol Var</b> tarafı ağır basıyor (%{kgvar:.1f}).")
    else:
        kgp.append(f"<b>Karşılıklı Gol Yok</b> tarafı açık ara öne çıkıyor (%{kgyok:.1f}).")
    if kgp and _kg_gec: bolumler.append(("🤝", "KARŞILIKLI GOL (KG)", " ".join(kgp)))
    return bolumler


def ai_yorum_paneli(v, a):
    bolumler = ai_yorum_olustur(v, a)
    if not bolumler: return ""
    html_parcalar = []
    for ikon, baslik, metin in bolumler:
        html_parcalar.append(f'<div style="margin-bottom:14px;"><div style="font-size:0.72rem;font-weight:900;color:#8fa0bd;text-transform:uppercase;margin-bottom:6px;">{ikon} {baslik}</div><div style="font-size:0.86rem;line-height:1.7;color:#eaf1fb;">{metin}</div></div>')
    s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
    karar_isim = {"1": f"1 ({te} Kazanır)", "X": "X (Beraberlik)", "2": f"2 ({td} Kazanır)"}[s1]
    return f'<div style="background:linear-gradient(145deg,rgba(19,28,46,0.92),rgba(11,18,32,0.98));border:1px solid rgba(59,130,246,0.35);border-radius:16px;padding:16px;"><div style="font-size:0.78rem;font-weight:900;color:#3b82f6;margin-bottom:14px;">🤖 AI MAÇ YORUMU</div>{"".join(html_parcalar)}</div>'


def yasal_metin_goster():
    with st.expander("📜 Kullanım Şartları ve Sorumluluk Reddi — OKU", expanded=False):
        st.markdown(YASAL_METIN)


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
        e = st.session_state.esikler
        return gecmis_istatistik_hesapla_cached("x", gc, e.get("esik_1", 55.0), e.get("esik_x", 55.0), e.get("esik_2", 55.0), e.get("ust", 65.0), e.get("alt", 55.0), e.get("kg_var", 57.0), e.get("kg_yok", 72.0))
    except Exception: return 0, 0, 0, 0, 0, 0, 0, 0, 0


def modern_istatistik_grafik(baslik="📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ", stil="donut"):
    p1, t1, s1, pg, tg, sg, pk, tk, sk = gecmis_istatistik_hesapla()
    st.markdown(f'<div style="text-align:center;font-size:0.7rem;color:#8fa0bd;font-weight:800;margin:14px 0;">{_e(baslik)}</div>', unsafe_allow_html=True)
    st.markdown(f'''<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;"><div style="background:#131c2e;border:1px solid #1d2940;border-radius:16px;padding:12px;text-align:center;"><div style="font-size:0.62rem;color:#8fa0bd;font-weight:800;">🎯 1X2</div><div style="font-size:1.5rem;font-weight:900;color:#22c55e;">%{p1:.0f}</div><div style="font-size:0.62rem;color:#64748b;">{t1}/{s1}</div></div><div style="background:#131c2e;border:1px solid #1d2940;border-radius:16px;padding:12px;text-align:center;"><div style="font-size:0.62rem;color:#8fa0bd;font-weight:800;">⚽ GOL</div><div style="font-size:1.5rem;font-weight:900;color:#3b82f6;">%{pg:.0f}</div><div style="font-size:0.62rem;color:#64748b;">{tg}/{sg}</div></div><div style="background:#131c2e;border:1px solid #1d2940;border-radius:16px;padding:12px;text-align:center;"><div style="font-size:0.62rem;color:#8fa0bd;font-weight:800;">🤝 KG</div><div style="font-size:1.5rem;font-weight:900;color:#f59e0b;">%{pk:.0f}</div><div style="font-size:0.62rem;color:#64748b;">{tk}/{sk}</div></div></div>''', unsafe_allow_html=True)


def admin_giris_ekrani():
    st.markdown('''<div style="text-align:center;padding:40px 10px 24px 10px;"><div style="font-size:4rem;margin-bottom:14px;">🔐</div><h1 style="font-size:2rem;font-weight:900;color:#22c55e;">Giriş Yap</h1></div>''', unsafe_allow_html=True)
    with st.form("admin_giris_form"):
        kadi = st.text_input("👤 Kullanıcı Adı", key="admin_kadi_input")
        sifre = st.text_input("🔐 Şifre", type="password", key="admin_sifre_input")
        c1, c2 = st.columns(2)
        with c1: giris_btn = st.form_submit_button("✅ Giriş Yap", use_container_width=True, type="primary")
        with c2: iptal_btn = st.form_submit_button("⬅️ Ana Sayfa", use_container_width=True)
        if giris_btn:
            if not kadi.strip() or not sifre: st.error("❌ Bilgiler gerekli.")
            else:
                izin, kalan = _giris_limiti_kontrol(kadi.strip())
                if not izin: st.error(f"🚫 {kalan} saniye sonra tekrar dene.")
                elif kadi.strip() == ADMIN_KULLANICI_ADI and _secrets.compare_digest(sifre, ADMIN_SIFRE):
                    _giris_basarili_sil(kadi.strip())
                    _cerez_yaz("fa_token", ADMIN_TOKEN); _cerez_yaz("fa_kadi", ADMIN_KULLANICI_ADI)
                    st.session_state.rol = "admin"; st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"; st.rerun()
                elif kullanici_dogrula(kadi.strip(), sifre):
                    _giris_basarili_sil(kadi.strip())
                    try:
                        _u_token = _token_uret()
                        _kk = kullanicilar_yukle()
                        if kadi.strip() in _kk:
                            _kk[kadi.strip()]["oturum_token"] = _token_hash(_u_token)
                            kullanicilar_kaydet(_kk)
                        _cerez_yaz("fa_token", _u_token); _cerez_yaz("fa_kadi", kadi.strip())
                    except Exception: pass
                    st.session_state.aktif_kullanici = kadi.strip(); st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"
                    st.success(f"✅ Hoş geldin, {kadi.strip()}!"); time.sleep(1); st.rerun()
                else:
                    _giris_denemesi_ekle(kadi.strip())
                    st.error("❌ Kullanıcı adı veya şifre hatalı.")
        if iptal_btn:
            st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"; st.rerun()


def ust_bar():
    c1, c2 = st.columns([3, 1])
    with c1:
        if admin_mi(): st.markdown('<div style="padding:6px 0;color:#22c55e;font-weight:700;">👑 Admin Modu</div>', unsafe_allow_html=True)
        elif uye_mi():
            premium = uye_premium_mu()
            if premium: st.markdown(f'<div style="padding:6px 0;color:#eaf1fb;font-weight:700;">👤 {_e(uye_adi())} &nbsp; 🌟 PREMIUM</div>', unsafe_allow_html=True)
            else: st.markdown(f'<div style="padding:6px 0;color:#f59e0b;font-weight:700;">👤 {_e(uye_adi())} (abonelik yok)</div>', unsafe_allow_html=True)
        else: st.markdown('<div style="padding:6px 0;color:#8fa0bd;font-weight:600;">👤 Misafir Modu</div>', unsafe_allow_html=True)
    with c2:
        if admin_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="cikis_btn"):
                _cerez_sil("fa_token"); _cerez_sil("fa_kadi")
                st.session_state.rol = "misafir"; st.session_state.sayfa = "giris"
                st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI); st.rerun()
        elif uye_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="uye_cikis_btn"):
                try:
                    _kk = kullanicilar_yukle()
                    if uye_adi() in _kk:
                        _kk[uye_adi()]["oturum_token"] = None
                        kullanicilar_kaydet(_kk)
                except Exception: pass
                _cerez_sil("fa_token"); _cerez_sil("fa_kadi")
                st.session_state.aktif_kullanici = None; st.session_state.sayfa = "giris"; st.rerun()


def nav_git(h):
    st.session_state.sayfa = h
    st.session_state.kayit_yapildi = False
    st.session_state.tek_silme_onay = None
    st.session_state.tek_silme_gelecek = None
    st.session_state.sil_onay_kadi = None
    st.rerun()


def nav_bar():
    if st.session_state.sayfa in ("kayit", "uyegirisi", "odeme", "giris_yap"): return
    try: kutu = st.container(key="fa_nav")
    except TypeError: kutu = st.container()
    with kutu:
        if admin_mi():
            sec = [("🏠 Ana Sayfa", "giris"), ("🔮 Gelecek", "gelecek_admin"), ("📊 Geçmiş", "gecmis"), ("🔬 Test", "backtest"), ("💳 Ödemeler", "admin_odemeler"), ("👥 Aboneler", "admin_aboneler"), ("📬 Bildirimler", "admin_bildirimler"), ("⚙️ Ayar", "ayarlar")]
        elif uye_mi(): sec = [("🏠 Ana Sayfa", "giris"), ("📊 Geçmiş Maçlar", "gecmis"), ("📬 Bildirim", "kullanici_bildirim")]
        else: sec = [("🏠 Ana Sayfa", "giris"), ("📊 Geçmiş Maçlar", "gecmis")]
        kl = st.columns(len(sec))
        for k, (e, h) in zip(kl, sec):
            with k:
                aktif = st.session_state.sayfa == h
                if st.button(e, key=f"nav_{h}", use_container_width=True, type="primary" if aktif else "secondary"):
                    if not aktif: nav_git(h)


_otomatik_giris_dene()

if st.session_state.admin_login_acik and not admin_mi():
    admin_giris_ekrani()
    st.stop()

ust_bar()
nav_bar()

if st.session_state.sayfa == "giris_yap":
    admin_giris_ekrani()
    
elif st.session_state.sayfa == "giris":
    if admin_mi():
        st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:gray;'>Admin Paneli</p>", unsafe_allow_html=True)
        try:
            bugun = gunluk_ziyaret_sayisi(); son7 = son_7_gun_ziyaretler()
            st.markdown("### 📈 Ziyaretçi İstatistikleri")
            c1, c2 = st.columns(2)
            with c1: st.markdown(f"""<div class="mh-stat"><div class="mh-stat-num">{bugun}</div><div class="mh-stat-lbl">Bugünkü</div></div>""", unsafe_allow_html=True)
            with c2: st.markdown(f"""<div class="mh-stat"><div class="mh-stat-num">{sum(son7.values())}</div><div class="mh-stat-lbl">Son 7 Gün</div></div>""", unsafe_allow_html=True)
        except Exception: pass
        st.divider()
        st.markdown("### 🤖 Otomatik Veri Çekme")
        vs1, vs2, vs3 = st.tabs(["🔄 Gelecek Maçlar", "📜 Lig Geçmişi", "🏁 Sonuçları İşle"])
        with vs1:
            if st.session_state.toplu_cek_ozet:
                oz = st.session_state.toplu_cek_ozet
                st.markdown(f"**Son çekim:** Eklenen: **{oz.get('eklenen', 0)}** | Atlanan: **{oz.get('atlanan', 0)}**")
            c1, c2 = st.columns(2)
            with c1: w = st.number_input("Paralel", 1, 6, 2, 1, key="fw")
            with c2:
                st.markdown("")
                if st.button("🚀 Bugünün Maçlarını Çek", use_container_width=True, type="primary", key="mbtn"):
                    ph = st.empty()
                    def _p(i, t, n):
                        try: ph.progress(min((i + 1) / t, 1.0), text=f"{i+1}/{t}: {n}")
                        except Exception: pass
                    with st.spinner("Çekiliyor..."):
                        bas, hat = mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=_p, max_workers=int(w))
                    ph.empty()
                    if hat:
                        with st.expander(f"⚠️ {len(hat)} hata"):
                            for h in hat: st.caption(h)
                    if not bas: st.error("❌ Hiçbir maç çekilemedi.")
                    else: st.success(f"✅ {len(bas)} maç işlendi."); time.sleep(2); st.rerun()
        with vs2:
            lurl = st.text_input("Lig URL", key="lig_url_input")
            c1, c2 = st.columns(2)
            with c1: la = st.number_input("Kaç maç?", 5, 30, 10, 1, key="lig_adet")
            with c2: lw = st.number_input("Paralel", 1, 6, 2, 1, key="lig_workers")
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
                    if bas: st.success(f"✅ {len(bas)} maç eklendi!"); time.sleep(2); st.rerun()
                    else: st.error("Hiçbir maç eklenemedi.")
        with vs3:
            if st.session_state.skor_ozet:
                oz = st.session_state.skor_ozet
                st.success(f"✅ {oz['tasinan']} maç Geçmişe taşındı • {oz['bitmemis']} maç bitmemiş")
            sy = st.checkbox("Tarayıcıyla da dene", value=False, key="skor_yedek")
            c1, c2 = st.columns(2)
            with c1: sw = st.number_input("Paralel", 1, 8, 4, 1, key="skor_w")
            with c2:
                st.markdown("")
                if st.button("🏁 Biten Maçları Aktar", use_container_width=True, type="primary", key="skor_btn"):
                    if not st.session_state.gelecek_analizler: st.warning("Gelecek'te maç yok")
                    else:
                        with st.spinner("Skorlar kontrol ediliyor..."):
                            st.session_state.skor_ozet = sonuclari_isle(bool(sy), int(sw))
                        st.rerun()
    else:
        gelecek = st.session_state.gelecek_analizler
        gelecek_goster = [(idx, g) for idx, g in enumerate(gelecek) if _mac_tahmin_var_mi(g.get("veri", {}))]
        toplam = len(gelecek_goster)
        premium = uye_premium_mu()
        kota = int(ayar_al("ucretsiz_kotasi", 3))
        if premium:
            st.markdown(f'''<div class="mh2-hero"><div class="mh2-hero-title">Futbol Analiz Pro</div><div style="color:#8fa0bd;margin-top:8px;">Hoş geldin, {_e(uye_adi())}</div><div style="display:flex;justify-content:center;gap:8px;margin-top:14px;"><span class="mh2-badge green">⚡ {toplam} MAÇ</span><span class="mh2-badge purple">👑 PREMIUM</span></div></div>''', unsafe_allow_html=True)
        elif uye_mi():
            st.markdown(f'''<div class="mh2-hero"><div class="mh2-hero-title">Futbol Analiz Pro</div><div style="color:#8fa0bd;margin-top:8px;">Hoş geldin, {_e(uye_adi())}</div><div style="display:flex;justify-content:center;gap:8px;margin-top:14px;"><span class="mh2-badge green">⚡ {toplam} MAÇ</span><span class="mh2-badge blue">🎁 İLK {kota} ÜCRETSİZ</span><span class="mh2-badge amber">⚠️ ABONELİK YOK</span></div></div>''', unsafe_allow_html=True)
        else:
            st.markdown(f'''<div class="mh2-hero"><div class="mh2-hero-title">Futbol Analiz Pro</div><div style="color:#8fa0bd;margin-top:8px;">Bugün {toplam} maç analize hazır</div><div style="display:flex;justify-content:center;gap:8px;margin-top:14px;"><span class="mh2-badge green">⚡ {toplam} MAÇ</span><span class="mh2-badge blue">🎁 İLK {kota} ÜCRETSİZ</span></div></div>''', unsafe_allow_html=True)
        modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ", stil="line")
        if premium: pass
        elif uye_mi():
            if st.button("💳 Premium'a Geç", use_container_width=True, type="primary", key="ana_premium_btn"):
                st.session_state["odeme_hedef_kadi"] = uye_adi(); st.session_state.sayfa = "odeme"; st.rerun()
        else:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✨ Hemen Üye Ol", use_container_width=True, type="primary", key="mis_prem"):
                    st.session_state.sayfa = "kayit"; st.rerun()
            with c2:
                if st.button("🔐 Giriş Yap", use_container_width=True, key="mis_giris_btn"):
                    st.session_state.sayfa = "giris_yap"; st.rerun()
        st.divider()
        if not gelecek_goster:
            st.markdown('''<div style="text-align:center;padding:36px;color:#64748b;">⚽ Henüz maç yok</div>''', unsafe_allow_html=True)
        else:
            sirali = sorted(gelecek_goster, key=lambda x: saat_sirala_anahtari(x[1]))
            acik = 0
            for idx, g in sirali:
                v = g["veri"]; te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
                ulke = v.get("ulke", ""); saat = v.get("saat", ""); tarih = v.get("tarih", "")
                bayrak = ulke_bayrak_bul(ulke)
                etiket_saat = "—"
                try:
                    if tarih and saat:
                        m = re.match(r'^(\d{1,2})\.(\d{1,2})\.(\d{2,4})$', tarih)
                        if m:
                            g_, a_, y_ = int(m.group(1)), int(m.group(2)), m.group(3)
                            y_ = int(y_) if len(y_) == 4 else 2000 + int(y_)
                            from datetime import date as _dt_date
                            mac_t = _dt_date(y_, a_, g_); bugun = _dt_date.today()
                            fark = (mac_t - bugun).days
                            if fark == 0: etiket_saat = "BUGÜN"
                            elif fark == 1: etiket_saat = "YARIN"
                            elif fark == -1: etiket_saat = "DÜN"
                            else: etiket_saat = f"{g_:02d}.{a_:02d}"
                    elif saat: etiket_saat = "BUGÜN"
                except Exception: etiket_saat = "MAÇ"
                lig_goster = (ulke or "").title()[:22] or "Uluslararası"
                if premium or acik < kota:
                    st.markdown(f'''<div class="mh2-match-v2"><div style="display:flex;justify-content:center;gap:8px;margin-bottom:8px;"><span style="font-size:0.78rem;color:#22c55e;font-weight:900;">🕐 {_e(saat or "--:--")}</span><span style="font-size:0.55rem;color:#8fa0bd;background:rgba(34,197,94,0.12);padding:2px 8px;border-radius:99px;">{_e(etiket_saat)}</span></div><div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:10px;"><span class="mh2-v2-tk mh2-v2-tk-ev" style="flex:1;">{_e(te)}</span><span style="font-size:0.72rem;color:#64748b;font-weight:900;">VS</span><span class="mh2-v2-tk mh2-v2-tk-dep" style="flex:1;">{_e(td)}</span></div><div style="text-align:center;font-size:0.72rem;color:#8fa0bd;padding:6px;background:rgba(34,197,94,0.08);border-radius:8px;">{bayrak} {_e(lig_goster)}</div></div>''', unsafe_allow_html=True)
                    if st.button("🔍 DETAYLI ANALİZ →", use_container_width=True, key=f"gmac_{idx}", type="primary"):
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


elif st.session_state.sayfa == "kayit":
    st.markdown('''<div style="text-align:center;padding:40px 10px 24px 10px;"><div style="font-size:4rem;">✨</div><h1 style="color:#22c55e;">Üye Ol</h1></div>''', unsafe_allow_html=True)
    with st.form("kayit_form"):
        yk = st.text_input("👤 Kullanıcı Adı", max_chars=30)
        ys = st.text_input("🔐 Şifre", type="password")
        yst = st.text_input("🔐 Şifre Tekrar", type="password")
        yasal_onay = st.checkbox("✅ Kullanım Şartlarını okudum, 18 yaşından büyüğüm.")
        c1, c2 = st.columns(2)
        with c1: kb = st.form_submit_button("✅ Kayıt Ol", use_container_width=True, type="primary")
        with c2: gb = st.form_submit_button("⬅️ Geri", use_container_width=True)
        if kb:
            if not yk.strip() or len(yk.strip()) < 3: st.error("❌ En az 3 karakter.")
            elif not yk.replace("_", "").isalnum(): st.error("❌ Sadece harf, rakam, _")
            elif yk.strip() == ADMIN_KULLANICI_ADI: st.error("❌ Bu isim kullanılamaz.")
            elif len(ys) < 4: st.error("❌ Şifre en az 4 karakter.")
            elif ys != yst: st.error("❌ Şifreler uyuşmuyor.")
            elif not yasal_onay: st.error("❌ Şartları kabul etmelisiniz.")
            else:
                b, m = kullanici_ekle(yk.strip(), ys)
                if b:
                    try:
                        _u_token = _token_uret()
                        _kk = kullanicilar_yukle()
                        if yk.strip() in _kk:
                            _kk[yk.strip()]["oturum_token"] = _token_hash(_u_token)
                            kullanicilar_kaydet(_kk)
                        _cerez_yaz("fa_token", _u_token); _cerez_yaz("fa_kadi", yk.strip())
                    except Exception: pass
                    st.session_state["aktif_kullanici"] = yk.strip()
                    st.session_state["odeme_hedef_kadi"] = yk.strip()
                    st.success(f"✅ {m}"); time.sleep(1.5); st.session_state.sayfa = "odeme"; st.rerun()
                else: st.error(f"❌ {m}")
        if gb: st.session_state.sayfa = "giris"; st.rerun()
    yasal_metin_goster()


elif st.session_state.sayfa == "odeme":
    hedef = st.session_state.get("odeme_hedef_kadi") or uye_adi()
    if not hedef:
        st.error("❌ Kullanıcı yok."); st.stop()
    iban = ayar_al("iban", "TR00 0000 0000 0000 0000 0000 00")
    hs = ayar_al("hesap_sahibi", "ADINIZ SOYADINIZ")
    fh = float(ayar_al("fiyat_haftalik", 49.0)); fa = float(ayar_al("fiyat_aylik", 149.0))
    st.markdown(f'''<div class="mh2-hero"><div class="mh2-hero-title">💳 Premium'a Geç</div><div style="color:#8fa0bd;margin-top:8px;">Havale / EFT ile ödeme</div></div>''', unsafe_allow_html=True)
    st.markdown(f'<div style="background:#131c2e;border:1px solid #1f2c44;border-radius:12px;padding:12px;margin-bottom:12px;"><b>👤 Kullanıcı:</b> {_e(hedef)}</div>', unsafe_allow_html=True)
    sec = st.radio("Paket", ["haftalik", "aylik"], format_func=lambda x: {"haftalik": f"📅 Haftalık — {fh:.0f} ₺", "aylik": f"📆 Aylık — {fa:.0f} ₺"}[x], index=1)
    sg = {"haftalik": 7, "aylik": 30}[sec]; fy_ = {"haftalik": fh, "aylik": fa}[sec]; et = {"haftalik": "Haftalık", "aylik": "Aylık"}[sec]
    st.markdown(f'<div style="background:#131c2e;border:1px solid #22c55e;border-radius:12px;padding:12px;margin-bottom:12px;"><b>Alıcı:</b> {_e(hs)}<br><b>IBAN:</b> {_e(iban)}<br><b>Tutar:</b> {fy_:.0f} ₺<br><b>Açıklama:</b> {_e(hedef)}</div>', unsafe_allow_html=True)
    bk = bekleyen_yukle()
    if hedef in bk and bk[hedef].get("durum") == "bekliyor": st.warning(f"⏳ Bekleyen bildirimin var: **{bk[hedef].get('sure_etiket', '?')}**")
    else:
        if st.button("📤 Ödeme Yaptım — Bildir", use_container_width=True, type="primary", key="odeme_bildir_btn"):
            bk[hedef] = {"tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "sure_gun": int(sg), "sure_etiket": et, "fiyat": float(fy_), "durum": "bekliyor"}
            bekleyen_kaydet(bk); st.success("✅ Bildirimin alındı!"); time.sleep(2); st.rerun()
    yasal_metin_goster()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, key="odeme_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "admin_odemeler":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>💳 Bekleyen Ödemeler</h1>", unsafe_allow_html=True)
    bk = bekleyen_yukle()
    if not bk: st.info("ℹ️ Bekleyen ödeme yok.")
    else:
        for k, b in list(bk.items()):
            tg = b.get("sure_gun", 0); te = b.get("sure_etiket", "?"); fi = b.get("fiyat", 0); tt = b.get("tarih", "?")
            st.markdown(f'<div style="background:#131c2e;border:1px solid #1f2c44;border-radius:12px;padding:12px;margin-bottom:8px;"><b>👤 {_e(k)}</b> — {te} — {fi:.0f} ₺ — 📅 {_e(tt)}</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button(f"✅ Onayla", use_container_width=True, type="primary", key=f"o_{k}"):
                    b_, yb = abonelik_aktif_et(k, tg)
                    if b_:
                        del bk[k]; bekleyen_kaydet(bk)
                        st.success(f"✅ {k} aktif! Bitiş: {yb}"); time.sleep(2); st.rerun()
            with c2:
                if st.button(f"❌ Reddet", use_container_width=True, key=f"r_{k}"):
                    del bk[k]; bekleyen_kaydet(bk); st.rerun()
            with c3:
                if st.button(f"🗑️ Sil", use_container_width=True, key=f"s_{k}"):
                    del bk[k]; bekleyen_kaydet(bk); st.rerun()
            st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="og"):
        st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "admin_aboneler":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>👥 Aboneler</h1>", unsafe_allow_html=True)
    kl = kullanicilar_yukle()
    if not kl: st.info("ℹ️ Kayıtlı kullanıcı yok.")
    else:
        top = len(kl); ak = sum(1 for k in kl if abonelik_aktif_mi(k))
        st.markdown(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;"><div class="mh-stat"><div class="mh-stat-num">{top}</div><div class="mh-stat-lbl">Toplam</div></div><div class="mh-stat"><div class="mh-stat-num">{ak}</div><div class="mh-stat-lbl">Aktif</div></div></div>', unsafe_allow_html=True)
        st.divider()
        for k, kd in list(kl.items()):
            bs = kd.get("abonelik_bitis"); aktif = abonelik_aktif_mi(k); kalan = 0
            if bs:
                try: kalan = (datetime.strptime(bs, "%Y-%m-%d") - datetime.now()).days
                except Exception: pass
            if aktif: dr = "#22c55e"; dt = f"🌟 AKTİF ({kalan} gün)"
            elif bs: dr = "#ef4444"; dt = "⛔ DOLMUŞ"
            else: dr = "#94a3b8"; dt = "⚪ YOK"
            st.markdown(f'<div style="background:#131c2e;border:1px solid #1f2c44;border-radius:12px;padding:12px;margin-bottom:8px;"><b>👤 {_e(k)}</b> <span style="color:{dr};float:right;">{_e(dt)}</span></div>', unsafe_allow_html=True)
            ca, cb = st.columns(2)
            with ca:
                if st.button("🚫 İptal Et", use_container_width=True, key=f"ip_{k}"):
                    abonelik_iptal_et(k); st.warning("İptal edildi."); time.sleep(1.5); st.rerun()
            with cb:
                if st.button("🗑️ Sil", use_container_width=True, key=f"ks_{k}"):
                    st.session_state.sil_onay_kadi = k
            if st.session_state.sil_onay_kadi == k:
                st.warning(f"⚠️ **{k}** silinsin mi?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Evet", key=f"yes_{k}", use_container_width=True, type="primary"):
                        kullanici_sil(k); st.session_state.sil_onay_kadi = None; st.rerun()
                with c2:
                    if st.button("❌ Hayır", key=f"no_{k}", use_container_width=True):
                        st.session_state.sil_onay_kadi = None; st.rerun()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="abg"):
        st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "admin_bildirimler":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>📬 Bildirimler</h1>", unsafe_allow_html=True)
    bd = bildirimler_yukle()
    if not bd: st.info("ℹ️ Bildirim yok.")
    else:
        for b in sorted(bd, key=lambda x: x.get("tarih", ""), reverse=True):
            bid = b.get("id"); tip = b.get("tip", "diger")
            tb = BILDIRIM_TIPLERI.get(tip, BILDIRIM_TIPLERI["diger"])
            st.markdown(f'<div style="background:#131c2e;border-left:4px solid #22c55e;border-radius:12px;padding:12px;margin-bottom:8px;"><b>{tb["ikon"]} {tb["isim"]}</b> — {_e(b.get("kullanici","?"))}<br><b>Konu:</b> {_e(b.get("konu",""))}<br>{_e(b.get("mesaj",""))}<br><small>📅 {_e(b.get("tarih","?"))}</small></div>', unsafe_allow_html=True)
            with st.expander("💬 Cevapla / Sil"):
                yanit = st.text_area("Yanıt", value=b.get("cevap", ""), key=f"cy_{bid}")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("💬 Kaydet", key=f"kaydet_{bid}", use_container_width=True, type="primary"):
                        bildirim_guncelle(bid, cevap=yanit, durum="okundu"); st.success("Kaydedildi."); time.sleep(1); st.rerun()
                with c2:
                    if st.button("🗑️ Sil", key=f"sil_{bid}", use_container_width=True):
                        bildirim_sil(bid); st.rerun()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="bdg"):
        st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "kullanici_bildirim":
    if not uye_mi(): st.error("❌ Giriş yap."); st.stop()
    st.markdown("<h1>📬 Bildirim Gönder</h1>", unsafe_allow_html=True)
    with st.form("bildirim_form"):
        tip = st.selectbox("Kategori", options=list(BILDIRIM_TIPLERI.keys()), format_func=lambda x: f"{BILDIRIM_TIPLERI[x]['ikon']} {BILDIRIM_TIPLERI[x]['isim']}")
        konu = st.text_input("Konu")
        mesaj = st.text_area("Mesaj", height=150)
        c1, c2 = st.columns(2)
        with c1: gb = st.form_submit_button("📤 Gönder", use_container_width=True, type="primary")
        with c2: gb2 = st.form_submit_button("⬅️ Geri", use_container_width=True)
        if gb:
            if not konu.strip() or not mesaj.strip(): st.error("❌ Konu ve mesaj gerekli.")
            else:
                bildirim_ekle(uye_adi(), tip, konu.strip(), mesaj.strip()); st.success("✅ Gönderildi!"); time.sleep(2); st.rerun()
        if gb2: st.session_state.sayfa = "giris"; st.rerun()
    st.divider()
    st.markdown("### 📋 Gönderdiklerin")
    bl = kullanici_bildirimleri(uye_adi())
    if not bl: st.info("Henüz bildirim yok.")
    else:
        for b in sorted(bl, key=lambda x: x.get("tarih", ""), reverse=True):
            tip = b.get("tip", "diger"); tb = BILDIRIM_TIPLERI.get(tip, BILDIRIM_TIPLERI["diger"])
            st.markdown(f'<div style="background:#131c2e;border-left:4px solid #3b82f6;border-radius:12px;padding:12px;margin-bottom:8px;"><b>{tb["ikon"]} {tb["isim"]}</b> — {b.get("durum","?")}<br>{_e(b.get("konu",""))}<br>{_e(b.get("mesaj",""))}</div>', unsafe_allow_html=True)
            if b.get("cevap"): st.info(f"💬 Admin: {b['cevap']}")


elif st.session_state.sayfa == "gelecek_admin":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    gel = st.session_state.gelecek_analizler
    gel_goster = [(idx, g) for idx, g in enumerate(gel) if _mac_tahmin_var_mi(g.get("veri", {}))]
    st.markdown("### 💾 Yedekleme")
    c1, c2 = st.columns(2)
    with c1:
        json_str2 = json.dumps(st.session_state.gelecek_analizler, ensure_ascii=False, indent=2)
        st.download_button(label=f"📥 Geleceği İndir ({len(gel_goster)} maç)", data=json_str2, file_name=f"gelecek_{len(gel_goster)}mac.json", mime="application/json", use_container_width=True)
    with c2:
        yuk2 = st.file_uploader("📤 Geleceği Yükle", type=["json"], key="yuk_gelecek")
        if yuk2 is not None:
            try:
                veri2 = json.loads(yuk2.read().decode("utf-8"))
                if isinstance(veri2, list):
                    st.session_state.gelecek_analizler = veri2; gelecek_kaydet(veri2); st.rerun()
            except Exception as e: st.error(f"❌ {e}")
    st.divider()
    if not gel_goster: st.info("ℹ️ Gelecek maç yok.")
    else:
        for idx, g in sorted(gel_goster, key=lambda x: saat_sirala_anahtari(x[1])):
            v = g["veri"]; te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
            st.markdown(mac_karti(te, td, False, 0, 0, 0, 0, v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
            th = mac_tahmin_karti(v, g)
            if th: st.markdown(th, unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1: st.number_input("Ev", 0, 20, 0, 1, key=f"ise_{idx}")
            with c2: st.number_input("Dep", 0, 20, 0, 1, key=f"isd_{idx}")
            with c3:
                st.markdown(""); st.markdown("")
                st.button("📥 Skor Gir & Taşı", key=f"inline_skor_btn_{idx}", on_click=_inline_skor_tasi_callback, args=(idx,), use_container_width=True, type="primary")
            c1, c2 = st.columns([5, 1])
            with c1:
                if st.button("🔍 Detay", use_container_width=True, key=f"gmac_{idx}"):
                    st.session_state.form_verileri = copy.deepcopy(v); st.session_state.kayit_yapildi = True
                    st.session_state.gelecekten_gelindi = True; st.session_state.aktif_gelecek_idx = idx
                    st.session_state.sayfa = "sonuc"; st.rerun()
            with c2:
                if st.button("🗑️ Sil", use_container_width=True, key=f"gsil_{idx}"):
                    st.session_state.tek_silme_gelecek = idx if st.session_state.get("tek_silme_gelecek") != idx else None
                    st.rerun()
            if st.session_state.get("tek_silme_gelecek") == idx:
                st.warning(f"⚠️ **{te} vs {td}** silinsin mi?")
                oc1, oc2 = st.columns(2)
                with oc1:
                    if st.button("✅ Evet", key=f"ge_{idx}", use_container_width=True, type="primary"):
                        st.session_state.gelecek_analizler.pop(idx); gelecek_kaydet(st.session_state.gelecek_analizler)
                        st.session_state.tek_silme_gelecek = None; st.rerun()
                with oc2:
                    if st.button("❌ Hayır", key=f"gi_{idx}", use_container_width=True):
                        st.session_state.tek_silme_gelecek = None; st.rerun()
            st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gg_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gc = st.session_state.gecmis_analizler; top = len(gc)
    if admin_mi():
        c1, c2 = st.columns(2)
        with c1:
            json_str = json.dumps(st.session_state.gecmis_analizler, ensure_ascii=False, indent=2)
            st.download_button(label=f"📥 Geçmişi İndir ({top})", data=json_str, file_name=f"gecmis_{top}.json", mime="application/json", use_container_width=True)
        with c2:
            yuk = st.file_uploader("📤 Yükle", type=["json"], key="yuk_gecmis")
            if yuk is not None:
                try:
                    veri = json.loads(yuk.read().decode("utf-8"))
                    if isinstance(veri, list):
                        st.session_state.gecmis_analizler = veri; gecmis_kaydet(veri); st.rerun()
                except Exception as e: st.error(f"❌ {e}")
        st.divider()
    if top == 0: st.info("Henüz kayıt yok.")
    else:
        modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ")
        st.divider()
        st.markdown(f"### 📋 Toplam: {top} maç")
        for i, g in enumerate(reversed(gc)):
            idx = len(gc) - 1 - i; v = g["veri"]
            te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
            se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
            st.markdown(f'<div style="background:#131c2e;border:1px solid #1f2c44;border-radius:12px;padding:12px;margin-bottom:8px;"><div style="text-align:center;font-weight:900;">{_e(te)} <span style="color:#22c55e;">{se} - {sd}</span> {_e(td)}</div></div>', unsafe_allow_html=True)
            dogruluk = g.get("dogruluk") or sonuc_hesapla(g)
            if dogruluk:
                o1 = dogruluk.get("oneri_1x2", {}); og = dogruluk.get("oneri_gol", {}); okg = dogruluk.get("oneri_kg", {})
                def _cls(t): return "✅" if t is True else ("❌" if t is False else "—")
                st.markdown(f'<div style="display:flex;justify-content:space-around;font-size:0.75rem;color:#8fa0bd;"><span>1X2: {o1.get("tahmin","—")} {_cls(o1.get("tuttu"))}</span><span>GOL: {og.get("tahmin","—")} {_cls(og.get("tuttu"))}</span><span>KG: {okg.get("tahmin","—")} {_cls(okg.get("tuttu"))}</span></div>', unsafe_allow_html=True)
            if st.button("🔍 Detay", use_container_width=True, key=f"mac_{idx}"):
                st.session_state.form_verileri = copy.deepcopy(v); st.session_state.kayit_yapildi = True
                st.session_state.gecmisten_gelindi = True; st.session_state.aktif_kayit_idx = idx
                st.session_state.sayfa = "sonuc"; st.rerun()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gc_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "backtest":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>🔬 Model Test</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: s1x2 = st.checkbox("⚽ 1X2", key="bt_1x2")
    with c2: skv = st.checkbox("🤝 KG Var", key="bt_kg_var")
    with c3: su = st.checkbox("⬆️ Üst 2.5", key="bt_ust")
    if st.button("🚀 TESTİ ÇALIŞTIR", use_container_width=True, type="primary"):
        sec = {"1x2": s1x2, "kg_var": skv, "kg_yok": False, "ust": su, "alt": False}
        esk = {"esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "kg_var": 70.0, "kg_yok": 70.0, "ust": 70.0, "alt": 70.0}
        s, d = backtest_hesapla(st.session_state.gecmis_analizler, sec, esk)
        st.session_state.bt_sonuc = s
    if st.session_state.get("bt_sonuc"):
        sonuc = st.session_state.bt_sonuc
        for k in ["1x2", "kg_var", "ust"]:
            if sonuc[k]["dogru"] + sonuc[k]["yanlis"] > 0:
                d = sonuc[k]; tt = d["dogru"] + d["yanlis"]; y = d["dogru"] / tt * 100
                st.markdown(f'<div style="background:#131c2e;border:1px solid #1f2c44;border-radius:12px;padding:12px;margin-bottom:8px;"><b>{k.upper()}</b>: %{y:.1f} ({d["dogru"]}✓ / {d["yanlis"]}✗)</div>', unsafe_allow_html=True)
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary"):
        st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "ayarlar":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>⚙️ Ayarlar</h1>", unsafe_allow_html=True)
    mv = st.session_state.esikler.copy()
    st.markdown("### 🏦 Ödeme")
    yiban = st.text_input("IBAN", value=mv.get("iban", ""))
    yhs = st.text_input("Hesap Sahibi", value=mv.get("hesap_sahibi", ""))
    st.markdown("### 💰 Fiyatlar")
    c1, c2 = st.columns(2)
    with c1: yfh = st.number_input("Haftalık", min_value=1.0, value=float(mv.get("fiyat_haftalik", 49.0)), step=10.0)
    with c2: yfa = st.number_input("Aylık", min_value=1.0, value=float(mv.get("fiyat_aylik", 149.0)), step=10.0)
    st.markdown("### 🎯 Eşikler")
    c1, c2, c3 = st.columns(3)
    with c1: ye1 = st.slider("1 %", 0, 100, int(mv.get("esik_1", 55.0)))
    with c2: yex = st.slider("X %", 0, 100, int(mv.get("esik_x", 55.0)))
    with c3: ye2 = st.slider("2 %", 0, 100, int(mv.get("esik_2", 55.0)))
    c4, c5 = st.columns(2)
    with c4: yu = st.slider("Üst %", 0, 100, int(mv["ust"]))
    with c5: ya = st.slider("Alt %", 0, 100, int(mv["alt"]))
    c6, c7 = st.columns(2)
    with c6: ykv = st.slider("KG Var %", 0, 100, int(mv["kg_var"]))
    with c7: yky = st.slider("KG Yok %", 0, 100, int(mv["kg_yok"]))
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💾 Kaydet", use_container_width=True, type="primary"):
            y = dict(mv); y.update({"iban": yiban, "hesap_sahibi": yhs, "fiyat_haftalik": float(yfh), "fiyat_aylik": float(yfa), "esik_1": float(ye1), "esik_x": float(yex), "esik_2": float(ye2), "ust": float(yu), "alt": float(ya), "kg_var": float(ykv), "kg_yok": float(yky)})
            st.session_state.esikler = y; ayarlar_kaydet(y); st.success("✅ Kaydedildi!")
    with c2:
        if st.button("🔄 Sıfırla", use_container_width=True):
            v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "iban": "TR00 0000 0000 0000 0000 0000 00", "hesap_sahibi": "ADINIZ SOYADINIZ", "fiyat_haftalik": 49.0, "fiyat_aylik": 149.0, "fiyat_yillik": 999.0, "ucretsiz_kotasi": 3}
            st.session_state.esikler = v; ayarlar_kaydet(v); st.rerun()
    with c3:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="ayg"):
            st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)
    te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
    sb = v.get("skor_belli", False); se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    ulke = v.get("ulke", ""); saat = v.get("saat", ""); tarih = v.get("tarih", "")
    bayrak = ulke_bayrak_bul(ulke)
    meta_parcalar = []
    if ulke: meta_parcalar.append(f"{bayrak} {ulke.title()}")
    if tarih: meta_parcalar.append(f"📅 {tarih}")
    if saat: meta_parcalar.append(f"🕐 {saat}")
    meta = " • ".join(meta_parcalar) if meta_parcalar else "MAÇ ANALİZİ"
    skor_html = f'<div style="font-size:2.1rem;font-weight:900;color:#22c55e;">{se} - {sd}</div>' if sb else '<div style="font-size:1.8rem;font-weight:900;color:#64748b;">VS</div>'
    st.markdown(f'''<div class="an-hero"><div style="text-align:center;font-size:0.68rem;color:#8fa0bd;font-weight:800;margin-bottom:14px;">{meta}</div><div style="display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:14px;"><div style="flex:1;text-align:center;font-size:1rem;font-weight:900;color:#93c5fd;">{_e(te)}</div><div style="min-width:100px;text-align:center;">{skor_html}</div><div style="flex:1;text-align:center;font-size:1rem;font-weight:900;color:#fbbf24;">{_e(td)}</div></div><div style="text-align:center;padding-top:12px;border-top:1px dashed rgba(34,197,94,0.3);font-size:0.72rem;color:#8fa0bd;">⚡ Beklenen Gol: <b style="color:#22c55e;">{a["lam_ev"]:.2f}</b> – <b style="color:#22c55e;">{a["lam_dep"]:.2f}</b> | Toplam: <b style="color:#22c55e;">{a["lam_ev"]+a["lam_dep"]:.2f}</b></div></div>''', unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.74rem;font-weight:900;color:#22c55e;margin:20px 0 12px 0;">📋 TAKIM FORMLARI (SON 5 MAÇ)</div>', unsafe_allow_html=True)
    def _form_html(form_str, takim, ev_mi=True):
        cls = "ev" if ev_mi else "dep"; renk = "#3b82f6" if ev_mi else "#f59e0b"
        s = "".join(c for c in str(form_str or "").upper() if c in "WDL")
        if not s: icerik = '<div style="font-size:0.65rem;color:#64748b;text-align:center;padding:10px;">Veri yok</div>'
        else:
            boxes = "".join(f'<span style="flex:1;max-width:34px;aspect-ratio:1;display:inline-flex;align-items:center;justify-content:center;font-size:0.82rem;font-weight:900;border-radius:7px;color:#fff;background:{"#22c55e" if c=="W" else "#64748b" if c=="D" else "#ef4444"};">{c}</span>' for c in s)
            icerik = f'<div style="display:flex;gap:4px;justify-content:space-between;">{boxes}</div>'
        return f'<div style="background:#131c2e;border:1.5px solid #1d2940;border-top:2.5px solid {renk};border-radius:14px;padding:10px;"><div style="font-size:0.74rem;font-weight:900;color:{"#93c5fd" if ev_mi else "#fbbf24"};text-align:center;margin-bottom:8px;">{_e(takim)}</div>{icerik}</div>'
    f_ev = _form_html(v.get("form_str_ev", ""), te, True); f_dep = _form_html(v.get("form_str_dep", ""), td, False)
    st.markdown(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px;">{f_ev}{f_dep}</div>', unsafe_allow_html=True)

    # SON 5 MAÇ ANALİZİ KARTLARI
    st.markdown('<div style="font-size:0.74rem;font-weight:900;color:#22c55e;margin:20px 0 12px 0;">🔥 SON 5 MAÇ ANALİZİ (xG & İSTATİSTİK)</div>', unsafe_allow_html=True)
    son5_xg_ev = v.get("son5_xg_atak", 0); son5_xg_dep = v.get("son5_xg_savunma", 0)
    son5_ppg = v.get("son5_ppg", 0); son5_btts = v.get("son5_btts_yuzde", 0)
    son5_ust = v.get("son5_ust25_yuzde", 0); son5_cs = v.get("son5_cs_yuzde", 0)
    st.markdown(f'''<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:16px;">
    <div style="background:#131c2e;border:1px solid #1d2940;border-radius:12px;padding:10px;text-align:center;"><div style="font-size:0.6rem;color:#8fa0bd;text-transform:uppercase;font-weight:800;margin-bottom:4px;">⚽ xG (Atak)</div><div style="font-size:1.1rem;font-weight:900;color:#22c55e;">{son5_xg_ev:.2f}</div></div>
    <div style="background:#131c2e;border:1px solid #1d2940;border-radius:12px;padding:10px;text-align:center;"><div style="font-size:0.6rem;color:#8fa0bd;text-transform:uppercase;font-weight:800;margin-bottom:4px;">🛡️ xG (Savunma)</div><div style="font-size:1.1rem;font-weight:900;color:#ef4444;">{son5_xg_dep:.2f}</div></div>
    <div style="background:#131c2e;border:1px solid #1d2940;border-radius:12px;padding:10px;text-align:center;"><div style="font-size:0.6rem;color:#8fa0bd;text-transform:uppercase;font-weight:800;margin-bottom:4px;">📈 PPG</div><div style="font-size:1.1rem;font-weight:900;color:#3b82f6;">{son5_ppg:.2f}</div></div>
    <div style="background:#131c2e;border:1px solid #1d2940;border-radius:12px;padding:10px;text-align:center;"><div style="font-size:0.6rem;color:#8fa0bd;text-transform:uppercase;font-weight:800;margin-bottom:4px;">🤝 BTTS</div><div style="font-size:1.1rem;font-weight:900;color:#f59e0b;">%{son5_btts:.0f}</div></div>
    <div style="background:#131c2e;border:1px solid #1d2940;border-radius:12px;padding:10px;text-align:center;"><div style="font-size:0.6rem;color:#8fa0bd;text-transform:uppercase;font-weight:800;margin-bottom:4px;">⬆️ 2.5 Üst</div><div style="font-size:1.1rem;font-weight:900;color:#8b5cf6;">%{son5_ust:.0f}</div></div>
    <div style="background:#131c2e;border:1px solid #1d2940;border-radius:12px;padding:10px;text-align:center;"><div style="font-size:0.6rem;color:#8fa0bd;text-transform:uppercase;font-weight:800;margin-bottom:4px;">🧤 Clean Sheet</div><div style="font-size:1.1rem;font-weight:900;color:#ec4899;">%{son5_cs:.0f}</div></div>
    </div>''', unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.74rem;font-weight:900;color:#22c55e;margin:20px 0 12px 0;">⚔️ Takım Karşılaştırması</div>', unsafe_allow_html=True)
    ae = float(v.get("atilan_ev", 0) or 0); ad = float(v.get("atilan_dep", 0) or 0)
    ye = float(v.get("yenen_ev", 0) or 0); yd = float(v.get("yenen_dep", 0) or 0)
    xge = float(v.get("xg_ev", 0) or 0); xgd = float(v.get("xg_dep", 0) or 0)
    u25e = float(v.get("ust25_ev", 0) or 0); u25d = float(v.get("ust25_dep", 0) or 0)
    kge = float(v.get("kg_siklik_ev", 0) or 0); kgd = float(v.get("kg_siklik_dep", 0) or 0)
    cs_e = float(v.get("clean_sheets_ev", 0) or 0); cs_d = float(v.get("clean_sheets_dep", 0) or 0)
    def _cmp(lbl, ev_val, dep_val, ev_max=100, dep_max=100, fmt=".1f", suffix=""):
        ev_p = max(0, min(100, (ev_val / ev_max * 100) if ev_max else 0)); dep_p = max(0, min(100, (dep_val / dep_max * 100) if dep_max else 0))
        return f'''<div style="display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;margin:8px 0;"><div><div style="font-size:0.72rem;font-weight:900;color:#93c5fd;text-align:right;">{ev_val:{fmt}}{suffix}</div></div><div style="font-size:0.55rem;font-weight:800;color:#8fa0bd;text-align:center;min-width:76px;">{lbl}</div><div><div style="font-size:0.72rem;font-weight:900;color:#fbbf24;text-align:left;">{dep_val:{fmt}}{suffix}</div></div></div>'''
    rows = []
    if ae or ad: rows.append(_cmp("Atılan Gol", ae, ad, 4.0, 4.0, ".2f"))
    if ye or yd: rows.append(_cmp("Yenen Gol", ye, yd, 4.0, 4.0, ".2f"))
    if xge or xgd: rows.append(_cmp("xG", xge, xgd, 3.0, 3.0, ".2f"))
    if u25e or u25d: rows.append(_cmp("Üst 2.5", u25e, u25d, 100, 100, ".0f", "%"))
    if kge or kgd: rows.append(_cmp("KG Sıklık", kge, kgd, 100, 100, ".0f", "%"))
    if cs_e or cs_d: rows.append(_cmp("Clean Sheet", cs_e, cs_d, 100, 100, ".0f", "%"))
    if rows: st.markdown(f'<div style="background:#131c2e;border:1px solid #1d2940;border-radius:16px;padding:14px 12px;"><div style="display:grid;grid-template-columns:1fr auto 1fr;gap:8px;margin-bottom:12px;padding-bottom:10px;border-bottom:1px dashed rgba(59,130,246,0.2);"><div style="font-size:0.78rem;font-weight:900;color:#93c5fd;text-align:right;">{_e(te)}</div><div style="font-size:0.66rem;font-weight:900;color:#64748b;text-align:center;">VS</div><div style="font-size:0.78rem;font-weight:900;color:#fbbf24;text-align:left;">{_e(td)}</div></div>{"".join(rows)}</div>''', unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.74rem;font-weight:900;color:#22c55e;margin:20px 0 12px 0;">🎯 Maç Sonucu Olasılıkları</div>', unsafe_allow_html=True)
    def _donut(yuzde, renk):
        y = max(0.0, min(100.0, yuzde)); r = 34; cevre = 2 * 3.14159 * r; offset = cevre * (1 - y / 100)
        return f'''<svg viewBox="0 0 82 82" style="width:82px;height:82px;margin:0 auto;display:block;"><circle cx="41" cy="41" r="{r}" fill="none" stroke="#0d1626" stroke-width="7"/><circle cx="41" cy="41" r="{r}" fill="none" stroke="{renk}" stroke-width="7" stroke-dasharray="{cevre:.2f}" stroke-dashoffset="{offset:.2f}" stroke-linecap="round" transform="rotate(-90 41 41)"/><text x="41" y="41" text-anchor="middle" dominant-baseline="central" fill="{renk}" font-size="20" font-weight="900">%{y:.0f}</text></svg>'''
    def _prob(lbl, yuzde, renk, esik=""):
        return f'<div style="background:linear-gradient(145deg,rgba(19,28,46,0.94),rgba(11,18,32,1));border:1px solid {renk};border-radius:16px;padding:14px 8px;text-align:center;"><div style="font-size:0.6rem;font-weight:900;color:#8fa0bd;text-transform:uppercase;margin-bottom:8px;">{lbl}</div>{_donut(yuzde, renk)}<div style="font-size:0.58rem;color:#64748b;margin-top:6px;">{esik}</div></div>'
    p1, px, p2 = a["p1"], a["px"], a["p2"]
    e1_ = esik_1x2_al("1"); eX_ = esik_1x2_al("X"); e2_ = esik_1x2_al("2")
    kartlar = []
    if p1 >= e1_: kartlar.append(_prob("EV KAZANIR", p1, "#3b82f6", f"Eşik %{e1_:.0f}"))
    if px >= eX_: kartlar.append(_prob("BERABERLİK", px, "#94a3b8", f"Eşik %{eX_:.0f}"))
    if p2 >= e2_: kartlar.append(_prob("DEP KAZANIR", p2, "#f59e0b", f"Eşik %{e2_:.0f}"))
    if kartlar: st.markdown(f'<div style="display:grid;grid-template-columns:repeat({len(kartlar)},1fr);gap:9px;margin-bottom:12px;">{"".join(kartlar)}</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="font-size:0.74rem;font-weight:900;color:#22c55e;margin:20px 0 12px 0;">⚽ Gol & KG Piyasaları</div>', unsafe_allow_html=True)
    u25, a25 = a["ust_25"], a["alt_25"]; kgv, kgy = a["kg_var_model"], a["kg_yok_model"]
    kartlar_gol = []
    if u25 >= esik_al("ust") and u25 >= a25: kartlar_gol.append(_prob("ÜST 2.5", u25, "#22c55e", f"Eşik %{esik_al('ust'):.0f}"))
    if a25 >= esik_al("alt") and a25 >= u25: kartlar_gol.append(_prob("ALT 2.5", a25, "#ef4444", f"Eşik %{esik_al('alt'):.0f}"))
    if kartlar_gol: st.markdown(f'<div style="display:grid;grid-template-columns:repeat({len(kartlar_gol)},1fr);gap:9px;margin-bottom:12px;">{"".join(kartlar_gol)}</div>', unsafe_allow_html=True)
    kartlar_kg = []
    if kgv >= esik_al("kg_var") and kgv >= kgy: kartlar_kg.append(_prob("KG VAR", kgv, "#8b5cf6", f"Eşik %{esik_al('kg_var'):.0f}"))
    if kgy >= esik_al("kg_yok") and kgy >= kgv: kartlar_kg.append(_prob("KG YOK", kgy, "#ec4899", f"Eşik %{esik_al('kg_yok'):.0f}"))
    if kartlar_kg: st.markdown(f'<div style="display:grid;grid-template-columns:repeat({len(kartlar_kg)},1fr);gap:9px;margin-bottom:12px;">{"".join(kartlar_kg)}</div>', unsafe_allow_html=True)
    
    ai_html = ai_yorum_paneli(v, a)
    if ai_html:
        st.markdown('<div style="font-size:0.74rem;font-weight:900;color:#22c55e;margin:20px 0 12px 0;">🤖 Yapay Zeka Analizi</div>', unsafe_allow_html=True)
        st.markdown(ai_html, unsafe_allow_html=True)
    
    s1, y1 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    km = (u25 >= esik_al("ust") and u25 >= a25) or (a25 >= esik_al("alt") and a25 >= u25) or (y1 >= esik_1x2_al(s1))
    if not st.session_state.kayit_yapildi and admin_mi():
        yk = kayit_olustur(v, a)
        if sb: st.session_state.gecmis_analizler.append(yk); gecmis_kaydet(st.session_state.gecmis_analizler)
        elif km: st.session_state.gelecek_analizler.append(yk); gelecek_kaydet(st.session_state.gelecek_analizler)
        st.session_state.kayit_yapildi = True
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Geri", use_container_width=True, key="sonuc_geri_btn"):
            if st.session_state.get("gecmisten_gelindi"): st.session_state.sayfa = "gecmis"
            elif st.session_state.get("gelecekten_gelindi"): st.session_state.sayfa = "gelecek_admin" if admin_mi() else "giris"
            else: st.session_state.sayfa = "giris"
            st.session_state.gecmisten_gelindi = False; st.session_state.gelecekten_gelindi = False; st.rerun()
    with c2:
        if st.button("🔄 Yeni", use_container_width=True, type="primary", key="sonuc_yeni_btn"):
            st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI); st.session_state.kayit_yapildi = False
            st.session_state.sayfa = "giris"; st.rerun()
