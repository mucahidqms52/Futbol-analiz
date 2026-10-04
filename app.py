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
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


# ==========================================
# YASAL METİN
# ==========================================
YASAL_METIN = """
# ⚖️ KULLANIM ŞARTLARI VE SORUMLULUK REDDİ

Bu uygulama **SADECE bilgilendirme ve analiz amaçlıdır**. Bahis oynamak **yasal risk**, **maddi kayıp riski** ve **bağımlılık riski** içerir.

- 18 yaşından büyük olmalısınız.
- Yasadışı bahis **suçtur** (7258 sayılı Kanun).
- Tahminler **%100 doğru değildir**, garanti içermez.
- Uygulama hiçbir bahis sitesiyle ortak değildir.

**YEDAM: 115**
"""


st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")


st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
    html { font-size: 13px !important; }
    body, .stApp { font-size: 0.85rem !important; }
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    h1, h2, h3, h4, .fa-score, .mh-stat-num { font-family: 'Rajdhani', 'Inter', sans-serif !important; }
    .block-container { padding-top: 0.8rem !important; padding-bottom: 0.8rem !important; padding-left: 0.8rem !important; padding-right: 0.8rem !important; max-width: 100% !important; }
    :root { --bg-0: #060a14; --bg-1: #0b1220; --card: #131c2e; --border: #1f2c44; --text: #eaf1fb; --muted: #7f92b3; --green: #22c55e; --blue: #3b82f6; --yellow: #f59e0b; --red: #ef4444; }
    .stApp { background: radial-gradient(1200px 600px at 10% -10%, rgba(34,197,94,0.08), transparent 60%), linear-gradient(180deg, #060a14 0%, #0b1220 100%) !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp div[data-testid="stMarkdownContainer"] { color: var(--text) !important; }
    .stApp div[data-testid="stCaptionContainer"], .stApp small { color: var(--muted) !important; }
    hr { border-color: var(--border) !important; margin: 0.5rem 0 !important; }
    h1 { font-size: 1.35rem !important; font-weight: 800 !important; margin: 0.4rem 0 !important; text-align: center; }
    h2 { font-size: 1rem !important; font-weight: 700 !important; margin: 0.4rem 0 !important; }
    h3 { font-size: 0.88rem !important; font-weight: 700 !important; margin: 0.25rem 0 !important; border-left: 3px solid var(--green); padding-left: 0.5rem; }
    p { font-size: 0.8rem !important; margin: 0.2rem 0 !important; line-height: 1.45; }
    .stButton button { background: linear-gradient(145deg, #18233a, #131c2e) !important; border: 1.5px solid var(--border) !important; border-radius: 10px !important; font-weight: 700 !important; font-size: 0.8rem !important; color: var(--text) !important; padding: 0.4rem 0.6rem !important; }
    .stButton button p { color: var(--text) !important; font-weight: 700 !important; font-size: 0.8rem !important; }
    .stButton button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; border: none !important; }
    .stButton button[kind="primary"] p { color: #04130a !important; }
    .stApp .fa-hero { background: linear-gradient(135deg, #14243e 0%, #0d1729 100%); border: 1px solid var(--border); border-radius: 16px; padding: 14px 12px; margin: 6px 0 10px 0; text-align: center; }
    .stApp .fa-teams { display: flex; align-items: center; justify-content: space-between; gap: 6px; }
    .stApp .fa-team { flex: 1; font-weight: 800; font-size: 0.9rem; }
    .stApp .fa-score { font-size: 1.6rem; font-weight: 900; color: var(--green) !important; }
    .stApp .fa-vs { font-size: 0.9rem; font-weight: 800; color: var(--muted) !important; }
    .stApp .fa-sub { font-size: 0.68rem; color: var(--muted) !important; margin-top: 6px; }
    .stApp .fa-card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 10px 12px; margin-bottom: 10px; }
    .stApp .fa-ttl { font-size: 0.68rem; font-weight: 800; color: var(--muted) !important; text-transform: uppercase; margin-bottom: 6px; }
    .stApp .fa-pickrow { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .stApp .fa-pick { font-size: 1rem; font-weight: 800; }
    .stApp .fa-pct { font-size: 1.35rem; font-weight: 900; color: var(--green) !important; }
    .stApp .fa-mut { font-size: 0.68rem; color: var(--muted) !important; margin-top: 6px; }
    .mh-hero { text-align: center; padding: 28px 14px 22px 14px; background: linear-gradient(135deg, rgba(22,35,61,0.9), rgba(15,26,46,0.95)); border: 1.5px solid rgba(34,197,94,0.25); border-radius: 20px; margin: 6px 0 16px 0; }
    .mh-hero-title { font-size: 1.7rem; font-weight: 900; color: var(--green); }
    .mh-hero-sub { font-size: 0.8rem; color: var(--muted); margin-top: 8px; }
    .mh-hero-badge { display: inline-block; margin-top: 12px; padding: 4px 14px; background: rgba(34,197,94,0.12); border: 1px solid rgba(34,197,94,0.45); border-radius: 99px; font-size: 0.7rem; font-weight: 800; color: var(--green) !important; }
    .mh-hero-ust { font-size: 0.7rem; color: #8fa0bd !important; letter-spacing: 2px; text-transform: uppercase; font-weight: 800; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# DOSYALAR
# ==========================================
GECMIS_DOSYA = "gecmis.json"
GELECEK_DOSYA = "gelecek.json"
AYARLAR_DOSYA = "ayarlar.json"
KULLANICI_DOSYA = "kullanicilar.json"
BEKLEYEN_DOSYA = "bekleyen_odemeler.json"
BILDIRIM_DOSYA = "bildirimler.json"

ADMIN_KULLANICI_ADI = "admin52"


def _admin_sifre_al():
    try:
        if "ADMIN_SIFRE" in st.secrets:
            return st.secrets["ADMIN_SIFRE"]
    except Exception:
        pass
    return os.environ.get("ADMIN_SIFRE", "Mg153759")

ADMIN_SIFRE = _admin_sifre_al()


def sifre_hashle(sifre, salt=None):
    if salt is None:
        salt = _secrets.token_hex(16)
    h = hashlib.sha256((salt + sifre).encode("utf-8")).hexdigest()
    return salt, h


def sifre_dogrula(sifre, salt, kayitli_hash):
    _, h = sifre_hashle(sifre, salt)
    return h == kayitli_hash


def _yukle_json(dosya, varsayilan):
    try:
        if os.path.exists(dosya):
            with open(dosya, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return varsayilan


def _kaydet_json(dosya, veri):
    try:
        with open(dosya, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def kullanicilar_yukle(): return _yukle_json(KULLANICI_DOSYA, {})
def kullanicilar_kaydet(v): _kaydet_json(KULLANICI_DOSYA, v)
def bekleyen_yukle(): return _yukle_json(BEKLEYEN_DOSYA, {})
def bekleyen_kaydet(v): _kaydet_json(BEKLEYEN_DOSYA, v)
def bildirimler_yukle(): return _yukle_json(BILDIRIM_DOSYA, [])
def bildirimler_kaydet(v): _kaydet_json(BILDIRIM_DOSYA, v)
def gecmis_yukle(): return _yukle_json(GECMIS_DOSYA, [])
def gecmis_kaydet(v): _kaydet_json(GECMIS_DOSYA, v)
def gelecek_yukle(): return _yukle_json(GELECEK_DOSYA, [])
def gelecek_kaydet(v): _kaydet_json(GELECEK_DOSYA, v)


def kullanici_ekle(kullanici_adi, sifre):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi in kullanicilar:
        return False, "Bu kullanıcı adı zaten alınmış."
    salt, s_hash = sifre_hashle(sifre)
    kullanicilar[kullanici_adi] = {
        "salt": salt, "sifre_hash": s_hash,
        "kayit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "abonelik_bitis": None, "son_odeme": None, "son_odeme_gun": 0,
    }
    kullanicilar_kaydet(kullanicilar)
    return True, "Kayıt başarılı."


def kullanici_dogrula(kullanici_adi, sifre):
    kullanicilar = kullanicilar_yukle()
    k = kullanicilar.get(kullanici_adi)
    if not k: return False
    return sifre_dogrula(sifre, k["salt"], k["sifre_hash"])


def abonelik_aktif_mi(kullanici_adi):
    kullanicilar = kullanicilar_yukle()
    k = kullanicilar.get(kullanici_adi)
    if not k: return False
    bitis_str = k.get("abonelik_bitis")
    if not bitis_str: return False
    try:
        return datetime.strptime(bitis_str, "%Y-%m-%d") >= datetime.now()
    except Exception:
        return False


def abonelik_aktif_et(kullanici_adi, gun_sayisi):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi not in kullanicilar:
        return False, "Kullanıcı bulunamadı."
    k = kullanicilar[kullanici_adi]
    mevcut_bitis = None
    if k.get("abonelik_bitis"):
        try: mevcut_bitis = datetime.strptime(k["abonelik_bitis"], "%Y-%m-%d")
        except Exception: mevcut_bitis = None
    bugun = datetime.now()
    baslangic = mevcut_bitis if (mevcut_bitis and mevcut_bitis > bugun) else bugun
    yeni_bitis = baslangic + timedelta(days=int(gun_sayisi))
    k["abonelik_bitis"] = yeni_bitis.strftime("%Y-%m-%d")
    k["son_odeme"] = bugun.strftime("%Y-%m-%d %H:%M")
    k["son_odeme_gun"] = int(gun_sayisi)
    kullanicilar_kaydet(kullanicilar)
    return True, yeni_bitis.strftime("%Y-%m-%d")


def abonelik_iptal_et(kullanici_adi):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi not in kullanicilar: return False
    kullanicilar[kullanici_adi]["abonelik_bitis"] = None
    kullanicilar_kaydet(kullanicilar)
    return True


def kullanici_sil(kullanici_adi):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi in kullanicilar:
        del kullanicilar[kullanici_adi]
        kullanicilar_kaydet(kullanicilar)
        bd = bildirimler_yukle()
        bd = [b for b in bd if b.get("kullanici") != kullanici_adi]
        bildirimler_kaydet(bd)
        return True
    return False


BILDIRIM_TIPLERI = {
    "iptal": {"ikon": "🚫", "isim": "Abonelik İptal Talebi"},
    "sikayet": {"ikon": "⚠️", "isim": "Şikayet"},
    "gorus": {"ikon": "💬", "isim": "Görüş / Öneri"},
    "diger": {"ikon": "📩", "isim": "Diğer"},
}


def bildirim_ekle(kullanici_adi, tip, konu, mesaj):
    bd = bildirimler_yukle()
    yeni = {"id": int(time.time() * 1000), "kullanici": kullanici_adi, "tip": tip, "konu": konu, "mesaj": mesaj, "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "durum": "okunmadi", "cevap": ""}
    bd.append(yeni)
    bildirimler_kaydet(bd)
    return yeni["id"]


def bildirim_guncelle(bid, **kwargs):
    bd = bildirimler_yukle()
    for b in bd:
        if b.get("id") == bid:
            b.update(kwargs)
            break
    bildirimler_kaydet(bd)


def bildirim_sil(bid):
    bd = bildirimler_yukle()
    bd = [b for b in bd if b.get("id") != bid]
    bildirimler_kaydet(bd)


def kullanici_bildirimleri(kullanici_adi):
    bd = bildirimler_yukle()
    return [b for b in bd if b.get("kullanici") == kullanici_adi]


def ayarlar_yukle():
    v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "iban": "TR00 0000 0000 0000 0000 0000 00", "hesap_sahibi": "ADINIZ SOYADINIZ", "fiyat_haftalik": 49.0, "fiyat_aylik": 149.0, "fiyat_yillik": 999.0, "ucretsiz_kotasi": 3}
    try:
        if os.path.exists(AYARLAR_DOSYA):
            with open(AYARLAR_DOSYA, "r", encoding="utf-8") as f:
                v.update(json.load(f))
    except Exception: pass
    return v


def ayarlar_kaydet(v): _kaydet_json(AYARLAR_DOSYA, v)


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


ESIK_YUKSEK = 65.0; ESIK_ORTA = 55.0; ESIK_BELIRSIZ = 50.0; MONTE_CARLO_N = 10000


VARSAYILAN_VERI = {k: v for k, v in {
    "ppg_ev": 0.0, "mpg_dep": 0.0, "form_str_ev": "", "form_str_dep": "",
    "siralama_ev": 0, "siralama_dep": 0, "puan_ev": 0, "puan_dep": 0,
    "xg_ev": 0.0, "xg_dep": 0.0, "atilan_ev": 0.0, "atilan_dep": 0.0,
    "yenen_ev": 0.0, "yenen_dep": 0.0, "clean_sheets_ev": 0.0, "clean_sheets_dep": 0.0,
    "team_scored_ev": 0.0, "team_scored_dep": 0.0,
    "ust05_ev": 80.0, "ust05_dep": 80.0, "ust15_ev": 50.0, "ust15_dep": 50.0,
    "ust25_ev": 30.0, "ust25_dep": 30.0, "ust35_ev": 20.0, "ust35_dep": 20.0,
    "kg_siklik_ev": 50.0, "kg_siklik_dep": 50.0,
    "galibiyet_ev": 30.0, "galibiyet_dep": 30.0, "beraberlik_ev": 30.0, "beraberlik_dep": 30.0,
    "maglubiyet_ev": 30.0, "maglubiyet_dep": 30.0,
    "takim_ev": "", "takim_dep": "", "skor_ev": 0, "skor_dep": 0, "skor_belli": False,
    "lig_ort_toplam": 0.0, "lig_ust25": 0.0, "lig_kg": 0.0,
    "saat": "", "tarih": "", "ulke": "", "format": "bilinmiyor", "kaynak_url": "",
}.items()}

MAX_GOL = 8; BELIRSIZLIK = 0.20; MAX_MAC_SINIRI = 200
_ESIK_CACHE = {}


if "sayfa" not in st.session_state: st.session_state.sayfa = "giris"
if "form_verileri" not in st.session_state: st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
if "gecmis_analizler" not in st.session_state: st.session_state.gecmis_analizler = gecmis_yukle()
if "gelecek_analizler" not in st.session_state: st.session_state.gelecek_analizler = gelecek_yukle()
if "kayit_yapildi" not in st.session_state: st.session_state.kayit_yapildi = False
if "gelecekten_gelindi" not in st.session_state: st.session_state.gelecekten_gelindi = False
if "aktif_gelecek_idx" not in st.session_state: st.session_state.aktif_gelecek_idx = None
if "rol" not in st.session_state: st.session_state.rol = "misafir"
if "admin_login_acik" not in st.session_state: st.session_state.admin_login_acik = False
if "esikler" not in st.session_state: st.session_state.esikler = ayarlar_yukle()
if "toplu_cek_ozet" not in st.session_state: st.session_state.toplu_cek_ozet = None
if "skor_ozet" not in st.session_state: st.session_state.skor_ozet = None
if "aktif_kullanici" not in st.session_state: st.session_state.aktif_kullanici = None
if "odeme_hedef_kadi" not in st.session_state: st.session_state.odeme_hedef_kadi = None


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


ULKE_BAYRAK = {"switzerland": "🇨🇭", "england": "🏴", "spain": "🇪🇸", "italy": "🇮🇹", "germany": "🇩🇪", "france": "🇫🇷", "netherlands": "🇳🇱", "portugal": "🇵🇹", "belgium": "🇧🇪", "turkey": "🇹🇷", "argentina": "🇦🇷", "brazil": "🇧🇷", "mexico": "🇲🇽", "usa": "🇺🇸", "japan": "🇯🇵", "china": "🇨🇳", "russia": "🇷🇺", "poland": "🇵🇱", "greece": "🇬🇷", "austria": "🇦🇹", "croatia": "🇭🇷", "serbia": "🇷🇸", "romania": "🇷🇴", "bulgaria": "🇧🇬", "denmark": "🇩🇰", "sweden": "🇸🇪", "norway": "🇳🇴", "finland": "🇫🇮", "hungary": "🇭🇺"}


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
    return ""


def clamp(x, lo, hi): return max(lo, min(hi, x))


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
    ae = v.get("atilan_ev", 0.0); ye = v.get("yenen_ev", 0.0)
    ad = v.get("atilan_dep", 0.0); yd = v.get("yenen_dep", 0.0)
    xge = v.get("xg_ev", 0.0); xgd = v.get("xg_dep", 0.0)
    he = (xge * 0.60 + ae * 0.40) if xge > 0 else (ae if ae > 0 else 1.2)
    hd = (xgd * 0.60 + ad * 0.40) if xgd > 0 else (ad if ad > 0 else 1.0)
    sd = yd if yd > 0 else 1.2; se = ye if ye > 0 else 1.0
    le = he * 0.60 + sd * 0.40; ld = hd * 0.60 + se * 0.40
    fe = clamp(1 + (v.get("ppg_ev", 1.5) - 1.5) / 15, 0.85, 1.15)
    fd = clamp(1 + (v.get("mpg_dep", 1.5) - 1.5) / 15, 0.85, 1.15)
    le = le * 1.05 * fe; ld = ld * 0.95 * fd
    if le > 2.50: le = 2.50 + (le - 2.50) * 0.5
    if ld > 2.50: ld = 2.50 + (ld - 2.50) * 0.5
    return clamp(le, 0.05, 4.5), clamp(ld, 0.05, 4.5), 0.80


def matristen_olasilik(matris, mg=MAX_GOL):
    p1 = px = p2 = u25 = kg = 0.0; tot = 0.0
    for i in range(mg):
        for j in range(mg):
            p = matris[i][j]; tot += p
            if i > j: p1 += p
            elif i == j: px += p
            else: p2 += p
            if i + j > 2.5: u25 += p
            if i > 0 and j > 0: kg += p
    return {"1": p1, "X": px, "2": p2, "ust_25": u25, "kg_var": kg, "toplam": tot}


def monte_carlo_simulasyon(leb, ldb, n=MONTE_CARLO_N):
    seed = int(round(leb * 1_000_000)) * 1_000_003 + int(round(ldb * 1_000_000))
    rng = random.Random(seed)
    s = {"1": 0, "X": 0, "2": 0, "u25": 0, "kg": 0}
    for _ in range(n):
        le = leb * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        ld = ldb * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        eg = min(MAX_GOL - 1, poisson_random(le, rng))
        dg = min(MAX_GOL - 1, poisson_random(ld, rng))
        if eg > dg: s["1"] += 1
        elif eg == dg: s["X"] += 1
        else: s["2"] += 1
        if eg + dg > 2.5: s["u25"] += 1
        if eg > 0 and dg > 0: s["kg"] += 1
    def yz(x): return x / n * 100 if n > 0 else 0
    return {"p1": yz(s["1"]), "px": yz(s["X"]), "p2": yz(s["2"]), "ust25": yz(s["u25"]), "kg_var": yz(s["kg"])}


def analiz_hesapla(v):
    le, ld, gv = hesapla_lambda(v)
    matris = poisson_matris(le, ld, MAX_GOL)
    o = matristen_olasilik(matris, MAX_GOL)
    tot = o["toplam"] or 1
    p1p = o["1"] / tot * 100; pxp = o["X"] / tot * 100; p2p = o["2"] / tot * 100
    u25p = o["ust_25"] / tot * 100; kgp = o["kg_var"] / tot * 100
    mc = monte_carlo_simulasyon(le, ld, MONTE_CARLO_N)
    p1 = p1p * 0.60 + mc["p1"] * 0.40
    px = pxp * 0.60 + mc["px"] * 0.40
    p2 = p2p * 0.60 + mc["p2"] * 0.40
    t = p1 + px + p2
    if t > 0: p1, px, p2 = (p1 / t) * 100, (px / t) * 100, (p2 / t) * 100
    u25 = u25p * 0.65 + mc["ust25"] * 0.35
    kgm = kgp * 0.60 + mc["kg_var"] * 0.40
    kgy = 100.0 - kgm; alt = 100.0 - u25
    eo = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    return {"lam_ev": le, "lam_dep": ld, "p1": p1, "px": px, "p2": p2, "ust_25": u25, "alt_25": alt, "kg_var_model": kgm, "kg_yok_model": kgy, "en_olasi": eo}


def kayit_olustur(v, a):
    return {"veri": copy.deepcopy(v), "analiz": {"p1": a["p1"], "px": a["px"], "p2": a["p2"], "tahmini_gol": a["lam_ev"] + a["lam_dep"], "kg_var_model": a["kg_var_model"], "ust_25": a["ust_25"]}}


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
    return {"oneri_1x2": {"tahmin": o1, "tuttu": t1, "durum": d1}, "oneri_gol": {"tahmin": og, "tuttu": tg_, "durum": dg_}, "oneri_kg": {"tahmin": okg, "tuttu": tk, "durum": dk}}


def _form_ppg(s):
    return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1)


def yeniden_analiz(v):
    v2 = copy.deepcopy(v)
    if v2.get("form_str_ev"): v2["ppg_ev"] = _form_ppg(v2["form_str_ev"])
    if v2.get("form_str_dep"): v2["mpg_dep"] = _form_ppg(v2["form_str_dep"])
    anahtar = json.dumps(v2, sort_keys=True, ensure_ascii=False)
    if "bt_analiz_cache" not in st.session_state: st.session_state.bt_analiz_cache = {}
    cache = st.session_state.bt_analiz_cache
    if anahtar not in cache:
        a = analiz_hesapla(v2)
        cache[anahtar] = {"ust_25": a["ust_25"], "kg_var_model": a["kg_var_model"], "p1": a["p1"], "px": a["px"], "p2": a["p2"]}
    return cache[anahtar]


# ==========================================
# METİN PARSER
# ==========================================
MANUEL_ALANLAR = {
    "Sıralama": [("siralama_ev", "Ev Sıralaması", "int", 1), ("siralama_dep", "Dep Sıralaması", "int", 1)],
    "Takım isimleri (Ev)": [("takim_ev", "Ev Takım Adı", "str", "")],
    "Takım isimleri (Dep)": [("takim_dep", "Dep Takım Adı", "str", "")],
}


def _cift_tab(etiket, blok):
    pattern = r'([\d.,]+)%?\s*\t\s*' + re.escape(etiket) + r'\s*\t\s*([\d.,]+)%?'
    m = re.search(pattern, blok, re.IGNORECASE)
    if m:
        try: return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError: pass
    return None, None


def sportytrader_veri_cikar(metin):
    veri = {}; okunamayanlar = []
    m = re.search(r'^([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s*-\s*([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s+Stats', metin, re.MULTILINE)
    if m:
        veri["takim_ev"] = m.group(1).strip(); veri["takim_dep"] = m.group(2).strip()
    m = re.search(r'Time\s*\t\s*(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1).strip()
    veri["ulke"] = _ulke_bul(metin)
    m = re.search(r'FT\s*\r?\n\s*(\d+)\s*-\s*(\d+)', metin)
    if m:
        veri["skor_ev"] = int(m.group(1)); veri["skor_dep"] = int(m.group(2)); veri["skor_belli"] = True
    else: veri["skor_belli"] = False
    idx = metin.find("Main Stats")
    if idx != -1:
        blok = metin[idx:idx+1500]
        v1, v2 = _cift_tab("Goals scored per game", blok)
        if v1 is not None: veri["atilan_ev"] = v1; veri["atilan_dep"] = v2
        v1, v2 = _cift_tab("Goals conceded per game", blok)
        if v1 is not None: veri["yenen_ev"] = v1; veri["yenen_dep"] = v2
    veri["format"] = "sportytrader"
    return veri, okunamayanlar


def metinden_veri_cikar(metin):
    metin = metin.replace(",", ".")
    if "Main Stats" in metin and "Goals scored per game" in metin:
        veri, okunamayanlar = sportytrader_veri_cikar(metin)
        if veri.get("saat"): veri["saat"] = saat_2_saat_ileri(veri["saat"])
        return veri, okunamayanlar
    return {}, []


# ==========================================
# VERİ ÇEKME MOTORU (sadece requests)
# ==========================================
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def _sayfa_getir(url, timeout=30, max_retry=3):
    hata = None
    for d in range(max_retry):
        try:
            r = requests.get(url,
                headers={
                    "User-Agent": UA,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                },
                timeout=timeout)
            if r.status_code == 200 and r.text and len(r.text) > 500:
                return r.text, None
            hata = f"HTTP {r.status_code} • Boyut: {len(r.text) if r.text else 0}"
        except Exception as e:
            hata = f"Bağlantı: {str(e)[:150]}"
        if d < max_retry - 1: time.sleep(1 + d)
    return None, hata


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
    html, hata = _sayfa_getir("https://www.mutating.com/football-stats/")
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
        maclar.append({"url": href, "takim_ev": tev, "takim_dep": tdep})
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
    veri["ulke"] = _ulke_bul(m)
    skor = _skor_parse(html)
    if skor:
        veri["skor_ev"] = skor[0]; veri["skor_dep"] = skor[1]; veri["skor_belli"] = True
    else:
        veri["skor_belli"] = False

    def cf(label):
        for pat in [r'([\d.,]+)\s*%?\s*\t\s*' + re.escape(label) + r'\s*\t\s*([\d.,]+)', r'([\d.,]+)\s*%?\s*\|\s*' + re.escape(label) + r'\s*\|\s*([\d.,]+)', r'([\d.,]+)\s*%?\s+' + re.escape(label) + r'\s+([\d.,]+)\s*%?', r'([\d.,]+)\s*%?\s*\n\s*' + re.escape(label) + r'\s*\n\s*([\d.,]+)']:
            x = re.search(pat, m, re.IGNORECASE)
            if x:
                try: return float(x.group(1).replace(",", ".")), float(x.group(2).replace(",", "."))
                except ValueError: continue
        return None, None

    for lb, ke, kd in [("Goals scored per game", "atilan_ev", "atilan_dep"), ("Goals conceded per game", "yenen_ev", "yenen_dep"), ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"), ("Team scored", "team_scored_ev", "team_scored_dep"), ("Both Teams to Score", "kg_siklik_ev", "kg_siklik_dep"), ("Over 2.5 goals", "ust25_ev", "ust25_dep")]:
        a, b = cf(lb)
        if a is not None and veri.get(ke, 0) == 0: veri[ke] = a; veri[kd] = b
    for lb, ke, kd in [("Win", "galibiyet_ev", "galibiyet_dep"), ("Draw", "beraberlik_ev", "beraberlik_dep"), ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
        x = re.search(r'([\d.,]+)\s*%\s*\t\s*' + lb + r'\s*\t\s*([\d.,]+)\s*%', m, re.MULTILINE)
        if x:
            try: veri[ke] = float(x.group(1).replace(",", ".")); veri[kd] = float(x.group(2).replace(",", "."))
            except ValueError: pass
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


def mutating_mac_detay_cek(url):
    h, hata = _sayfa_getir(url)
    if hata: return None, [hata]
    if not h: return None, ["Sayfa indirilemedi"]
    return _mac_html_parse(h, url)


def _gelecek_mac_isle(mac, mevcut):
    try:
        veri, _ = mutating_mac_detay_cek(mac["url"])
        if not veri: return ("hata", mac, "Veri yok", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        veri["kaynak_url"] = mac["url"]
        if mac["url"] in mevcut: return ("zaten_var", veri, "Zaten var", None)
        ae = veri.get("atilan_ev", 0); ye = veri.get("yenen_ev", 0)
        ad = veri.get("atilan_dep", 0); yd = veri.get("yenen_dep", 0)
        if ae == 0 and ye == 0 and ad == 0 and yd == 0: return ("veri_yok", veri, "Boş veri", None)
        try: a = analiz_hesapla(veri)
        except Exception as e: return ("veri_yok", veri, f"Hata: {str(e)[:50]}", None)
        if _mac_tahmin_var_mi(veri):
            kayit = kayit_olustur(veri, a)
            return ("eklendi", veri, "Eklendi", kayit)
        return ("esik_alti", veri, "Eşik altı", None)
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
    html, hata = _sayfa_getir(lig_url)
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
        maclar.append({"url": href, "takim_ev": takim_ev, "takim_dep": takim_dep})
        if len(maclar) >= adet: break
    return maclar, []


def _gecmis_mac_isle(mac, mevcut_urls):
    try:
        if mac["url"] in mevcut_urls:
            return ("atlandi", None, "Zaten var", None)
        html, hata = _sayfa_getir(mac["url"])
        if hata or not html: return ("hata", mac, hata or "HTML yok", None)
        veri, _ = _mac_html_parse(html, mac["url"])
        if not veri.get("skor_belli", False): return ("atlandi", None, "Skor yok", None)
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
    bas = []; hat = []; tam = 0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_gecmis_mac_isle, m, mevcut_urls): m for m in maclar}
        for f in as_completed(futs):
            tam += 1; mac = futs[f]
            try:
                r = f.result()
                sonuc, veri, mesaj, kayit = r if len(r) == 4 else (r[0], r[1], r[2], None)
                if sonuc == "eklendi":
                    bas.append(veri)
                    if kayit is not None:
                        try: st.session_state.gecmis_analizler.append(kayit)
                        except Exception: pass
                elif sonuc == "atlandi": pass
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
# SKOR ÇEKME — YENİ PARSER
# ==========================================
def _skor_parse(html):
    """
    Mutating.com HTML'inden skor çıkarır.
    Örnek HTML: <...>FT</...><...>5 - 2</...>
    """
    if not html:
        return None

    # 1) HAM HTML: FT kelimesinden sonra 200 karakter içinde X-Y ara
    try:
        m = re.search(r'FT\b[^\d]{0,200}?(\d{1,2})\s*[-:]\s*(\d{1,2})', html, re.IGNORECASE)
        if m:
            e, d = int(m.group(1)), int(m.group(2))
            if 0 <= e <= 20 and 0 <= d <= 20:
                return e, d
    except Exception:
        pass

    # 2) METİN: Aynı pattern
    txt = _html_metne_cevir(html)
    try:
        m = re.search(r'FT\b[^\d]{0,200}?(\d{1,2})\s*[-:]\s*(\d{1,2})', txt, re.IGNORECASE)
        if m:
            e, d = int(m.group(1)), int(m.group(2))
            if 0 <= e <= 20 and 0 <= d <= 20:
                return e, d
    except Exception:
        pass

    # 3) TÜM FT pozisyonlarını bul, her birinden sonra 200 karakter içinde X-Y ara
    up = txt.upper()
    idx = up.find("FT")
    while idx >= 0:
        seg = txt[idx:idx + 200]
        for pat in [r'(\d{1,2})\s*[-:]\s*(\d{1,2})', r'\b(\d{1,2})\s+(\d{1,2})\b']:
            try:
                m = re.search(pat, seg)
                if m:
                    e, d = int(m.group(1)), int(m.group(2))
                    if 0 <= e <= 20 and 0 <= d <= 20 and (e + d) > 0:
                        return e, d
            except Exception:
                continue
        idx = up.find("FT", idx + 1)

    # 4) HT pozisyonlarını da dene (bazı sayfalarda HT yazar)
    idx = up.find("HT")
    while idx >= 0:
        seg = txt[idx:idx + 200]
        try:
            m = re.search(r'(\d{1,2})\s*[-:]\s*(\d{1,2})', seg)
            if m:
                e, d = int(m.group(1)), int(m.group(2))
                if 0 <= e <= 20 and 0 <= d <= 20:
                    return e, d
        except Exception:
            pass
        idx = up.find("HT", idx + 1)

    # 5) score/result class'lı elementler
    try:
        soup = BeautifulSoup(html, "html.parser")
        for el in soup.find_all(class_=re.compile(r'(score|result)', re.I)):
            t = el.get_text(" ", strip=True)
            m = re.match(r'^\s*(\d{1,2})\s*[-:]\s*(\d{1,2})\s*$', t)
            if m:
                e, d = int(m.group(1)), int(m.group(2))
                if 0 <= e <= 20 and 0 <= d <= 20:
                    return e, d
    except Exception:
        pass

    return None


def _skor_cek(url):
    h, hata = _sayfa_getir(url, timeout=30, max_retry=2)
    if not h:
        return None, f"Sayfa alınamadı: {hata}"
    skor = _skor_parse(h)
    if skor:
        return skor, None
    return None, None


def sonuclari_isle(max_workers=3, progress_callback=None):
    gel = st.session_state.gelecek_analizler
    isler = [(i, g) for i, g in enumerate(gel) if g.get("veri", {}).get("kaynak_url")]
    sonuc = {}; tam = 0
    if isler:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futs = {ex.submit(_skor_cek, g["veri"]["kaynak_url"]): (i, g) for i, g in isler}
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
        if hata:
            ht.append(f"{isim}: {hata}"); kalan.append(g); continue
        if skor is None:
            bm += 1; kalan.append(g); continue
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


def mac_karti(ev, dep, sb, se, sd, le, ld, saat="", ulke="", tarih=""):
    orta = f'<div class="fa-score">{int(se)} - {int(sd)}</div>' if sb else '<div class="fa-vs">VS</div>'
    return f'<div class="fa-hero"><div class="fa-teams"><div class="fa-team">{_e(ev)}</div>{orta}<div class="fa-team">{_e(dep)}</div></div><div class="fa-sub">Model: {le:.2f} - {ld:.2f} • {_e(ulke)} {_e(saat)} {_e(tarih)}</div></div>'


def mac_tahmin_karti(v_g, g=None):
    try:
        ya = yeniden_analiz(v_g)
        p1 = ya.get("p1", 33.33); px = ya.get("px", 33.33); p2 = ya.get("p2", 33.34)
        u25 = ya.get("ust_25", 50); kgv = ya.get("kg_var_model", 50)
        s1, y1 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        return f'<div class="fa-card"><div class="fa-ttl">Tahmin</div><div class="fa-pickrow"><div class="fa-pick">1X2: {s1}</div><div class="fa-pct">%{y1:.0f}</div></div><div class="fa-mut">Üst 2.5: %{u25:.0f} • KG Var: %{kgv:.0f}</div></div>'
    except Exception: return ""


def olasilik_paneli(a):
    return f'<div class="fa-card"><div class="fa-ttl">Olasılıklar</div><div>1: %{a["p1"]:.1f} • X: %{a["px"]:.1f} • 2: %{a["p2"]:.1f}</div><div>Üst 2.5: %{a["ust_25"]:.1f} • Alt 2.5: %{a["alt_25"]:.1f}</div><div>KG Var: %{a["kg_var_model"]:.1f} • KG Yok: %{a["kg_yok_model"]:.1f}</div></div>'


def yasal_metin_goster():
    with st.expander("📜 Kullanım Şartları", expanded=False):
        st.markdown(YASAL_METIN)


def gecmis_istatistik_hesapla():
    g1x2 = gg = gk = 0
    t1x2 = tg = tk = 0
    for g in st.session_state.gecmis_analizler:
        try:
            v = g["veri"]
            if not v.get("skor_belli"): continue
            d = sonuc_hesapla(g)
            if not d: continue
            o = d["oneri_1x2"]
            if o.get("tuttu") is not None:
                t1x2 += 1
                if o["tuttu"]: g1x2 += 1
            o = d["oneri_gol"]
            if o.get("tuttu") is not None:
                tg += 1
                if o["tuttu"]: gg += 1
            o = d["oneri_kg"]
            if o.get("tuttu") is not None:
                tk += 1
                if o["tuttu"]: gk += 1
        except Exception: continue
    p1 = (g1x2 / t1x2 * 100) if t1x2 else 0
    pg = (gg / tg * 100) if tg else 0
    pk = (gk / tk * 100) if tk else 0
    return p1, g1x2, t1x2, pg, gg, tg, pk, gk, tk


def modern_istatistik_grafik(baslik="📊 İSTATİSTİKLER"):
    p1, t1, s1, pg, tg, sg, pk, tk, sk = gecmis_istatistik_hesapla()
    st.markdown(f"### {baslik}")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("1X2", f"%{p1:.1f}", f"{t1}/{s1}")
    with c2: st.metric("Gol", f"%{pg:.1f}", f"{tg}/{sg}")
    with c3: st.metric("KG", f"%{pk:.1f}", f"{tk}/{sk}")


# ==========================================
# ADMİN GİRİŞ
# ==========================================
def admin_giris_ekrani():
    st.markdown('<h1>🔐 Giriş Yap</h1>', unsafe_allow_html=True)
    with st.form("admin_giris_form"):
        kadi = st.text_input("👤 Kullanıcı Adı")
        sifre = st.text_input("🔐 Şifre", type="password")
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
            else: st.error("❌ Hatalı giriş.")
        if iptal_btn:
            st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"; st.rerun()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✨ Üye Ol", use_container_width=True, key="admin_to_kayit", type="primary"):
            st.session_state.admin_login_acik = False; st.session_state.sayfa = "kayit"; st.rerun()
    with c2:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="admin_to_main"):
            st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# ÜST BAR / NAV
# ==========================================
def ust_bar():
    c1, c2 = st.columns([3, 1])
    with c1:
        if admin_mi(): st.markdown("👑 **Admin Modu**")
        elif uye_mi(): st.markdown(f"👤 **{_e(uye_adi())}**")
        else: st.markdown("👤 Misafir")
    with c2:
        if admin_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="cikis_btn"):
                st.session_state.rol = "misafir"; st.session_state.sayfa = "giris"; st.rerun()
        elif uye_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="uye_cikis_btn"):
                st.session_state.aktif_kullanici = None; st.session_state.sayfa = "giris"; st.rerun()


def nav_git(h):
    st.session_state.sayfa = h
    st.session_state.kayit_yapildi = False
    st.rerun()


def nav_bar():
    if st.session_state.sayfa in ("kayit", "uyegirisi", "odeme", "giris_yap"): return
    if admin_mi():
        sec = [("🏠 Ana", "giris"), ("🔮 Gelecek", "gelecek_admin"), ("📊 Geçmiş", "gecmis"), ("💳 Ödemeler", "admin_odemeler"), ("👥 Aboneler", "admin_aboneler"), ("📬 Bildirimler", "admin_bildirimler"), ("⚙️ Ayar", "ayarlar")]
    elif uye_mi():
        sec = [("🏠 Ana", "giris"), ("📊 Geçmiş", "gecmis"), ("📬 Bildirim", "kullanici_bildirim")]
    else:
        sec = [("🏠 Ana", "giris"), ("📊 Geçmiş", "gecmis")]
    kl = st.columns(len(sec))
    for k, (e, h) in zip(kl, sec):
        with k:
            aktif = st.session_state.sayfa == h
            if st.button(e, key=f"nav_{h}", use_container_width=True, type="primary" if aktif else "secondary"):
                if not aktif: nav_git(h)


# ==========================================
# BAŞLANGIÇ
# ==========================================
if st.session_state.admin_login_acik and not admin_mi():
    admin_giris_ekrani()
    st.stop()

ust_bar()
nav_bar()


# ==========================================
# ANA SAYFA
# ==========================================
if st.session_state.sayfa == "giris_yap":
    admin_giris_ekrani()

elif st.session_state.sayfa == "giris":
    if admin_mi():
        st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:gray;'>Admin Paneli</p>", unsafe_allow_html=True)

        # MANUEL ÇEKİM PANELİ
        st.markdown("### 🖐️ Manuel Çekim Paneli")
        st.info("ℹ️ Otomatik çekim yoktur.")

        st.markdown("**🚀 Bugünün Maçları**")
        if st.button("🚀 Veri Çek", use_container_width=True, key="manuel_veri_btn", type="primary"):
            _ph = st.empty()
            def _p_cb(i, t, n):
                try: _ph.progress(min((i + 1) / t, 1.0), text=f"{i+1}/{t}: {n}")
                except Exception: pass
            with st.spinner("Veri çekiliyor..."):
                mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=_p_cb, max_workers=3)
            _ph.empty()
            st.success("✅ Veri çekimi tamamlandı.")
            time.sleep(1)
            st.rerun()

        st.divider()

        st.markdown("**📜 Lig Geçmişi**")
        _lurl = st.text_input("Lig URL", key="manuel_lig_url", placeholder="https://www.mutating.com/football-stats/league-...")
        _lc1, _lc2 = st.columns(2)
        with _lc1: _la = st.number_input("Kaç maç?", 5, 30, 10, 1, key="manuel_lig_adet")
        with _lc2: _lw = st.number_input("Paralel", 1, 8, 3, 1, key="manuel_lig_workers")
        if st.button("📜 Ligi Çek", use_container_width=True, key="manuel_lig_btn", type="primary"):
            if not _lurl.strip():
                st.warning("⚠️ URL gerekli")
            else:
                _ph2 = st.empty()
                def _p2_cb(i, t, n):
                    try: _ph2.progress(min((i + 1) / t, 1.0), text=f"{i+1}/{t}: {n}")
                    except Exception: pass
                with st.spinner(f"Son {_la} maç..."):
                    _bas, _hat = lig_gecmis_cek(_lurl.strip(), int(_la), int(_lw), _p2_cb)
                _ph2.empty()
                if _hat:
                    with st.expander(f"⚠️ {len(_hat)} hata"):
                        for h in _hat: st.caption(h)
                if _bas:
                    st.success(f"✅ {len(_bas)} maç eklendi!")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("Hiçbir maç eklenemedi.")

        st.divider()

        st.markdown("**⚽ Skor İşle**")
        st.caption(f"Bekleyen maç: **{len(st.session_state.gelecek_analizler)}**")
        if st.button("⚽ Skor İşle", use_container_width=True, key="manuel_skor_btn", type="primary"):
            if not st.session_state.gelecek_analizler:
                st.warning("⚠️ Gelecek'te maç yok.")
            else:
                with st.spinner("Skorlar kontrol ediliyor..."):
                    _oz = sonuclari_isle(3)
                    st.session_state.skor_ozet = _oz
                st.success(f"✅ {_oz.get('tasinan', 0)} maç geçmişe taşındı.")
                time.sleep(1)
                st.rerun()

        st.divider()

        # DEBUG
        with st.expander("🔬 DEBUG — Sorun teşhisi", expanded=False):
            _dbg_url = st.text_input("Test maç URL'si", key="dbg_url", placeholder="https://www.mutating.com/football-stats/...")

            if st.button("⚽ Skor Test Et", key="dbg_skor", use_container_width=True, type="primary"):
                if not _dbg_url.strip():
                    st.warning("URL gir")
                else:
                    with st.spinner("Test ediliyor..."):
                        try:
                            _h, _hata = _sayfa_getir(_dbg_url.strip(), timeout=30, max_retry=2)
                            if not _h:
                                st.error(f"❌ Sayfa alınamadı: {_hata}")
                            else:
                                st.success(f"✅ HTML geldi — {len(_h)} karakter")
                                _txt = _html_metne_cevir(_h)
                                _up = _txt.upper()
                                _ft_bulundu = []
                                _i = _up.find("FT")
                                _cnt = 0
                                while _i >= 0 and _cnt < 10:
                                    _seg = _txt[max(0, _i-30):_i+80].replace("\n", " ⏎ ")
                                    _ft_bulundu.append(_seg)
                                    _i = _up.find("FT", _i + 1)
                                    _cnt += 1
                                if _ft_bulundu:
                                    st.write("📋 **'FT' geçen yerler:**")
                                    for _s in _ft_bulundu:
                                        st.code(_s)
                                else:
                                    st.warning("⚠️ 'FT' hiç geçmiyor")
                                _skor = _skor_parse(_h)
                                if _skor:
                                    st.success(f"✅ **SKOR: {_skor[0]} - {_skor[1]}**")
                                else:
                                    st.error("❌ Parser skor bulamadı. Metnin ilk 3000 karakteri:")
                                    st.text(_txt[:3000])
                        except Exception as _e:
                            st.exception(_e)

        st.divider()

        if st.session_state.toplu_cek_ozet:
            oz = st.session_state.toplu_cek_ozet
            st.caption(f"📊 Son veri çekimi: **{oz.get('eklenen', 0)}** eklendi • **{oz.get('esik_alti', 0)}** eşik altı • **{oz.get('veri_yok', 0)}** veri yok • **{oz.get('hata', 0)}** hata")
            if oz.get("detay_log"):
                with st.expander("🔎 Detay"):
                    for s in oz["detay_log"]: st.text(s)
        if st.session_state.skor_ozet:
            oz = st.session_state.skor_ozet
            st.caption(f"⚽ Son skor: **{oz.get('tasinan', 0)}** taşındı • **{oz.get('bitmemis', 0)}** bitmemiş • **{len(oz.get('hatalar', []))}** hata")

        st.divider()
        st.markdown("### 📋 İstatistik Metnini Yapıştır")
        ym = st.text_area("Yapıştırma", height=200, key="yapistir_input", label_visibility="collapsed")
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
                    st.session_state.sayfa = "sonuc"; st.rerun()
        if gecmis_btn: nav_git("gecmis")
        if gelecek_btn: nav_git("gelecek_admin")
        if backtest_btn: nav_git("backtest")
        if ayarlar_btn: nav_git("ayarlar")

    else:
        gelecek = st.session_state.gelecek_analizler
        toplam = len(gelecek)
        premium = uye_premium_mu()
        kota = int(ayar_al("ucretsiz_kotasi", 3))

        if premium:
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-title">Hoş Geldin, {_e(uye_adi())}</div><div class="mh-hero-sub">Premium aktif</div><div class="mh-hero-badge">🌟 PREMIUM</div></div>', unsafe_allow_html=True)
        elif uye_mi():
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-title">Hoş Geldin, {_e(uye_adi())}</div><div class="mh-hero-sub">İlk {kota} maç ücretsiz</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-title">Bugün {toplam} Maç</div><div class="mh-hero-sub">İlk {kota} maç ücretsiz</div></div>', unsafe_allow_html=True)

        modern_istatistik_grafik()

        if not uye_mi():
            if st.button("💳 Premium / ✨ Üye Ol", use_container_width=True, type="primary", key="mis_prem"):
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
                if premium or acik < kota:
                    try:
                        af = analiz_hesapla(v); le = af["lam_ev"]; ld = af["lam_dep"]
                    except Exception: le = ld = 0
                    st.markdown(mac_karti(te, td, False, 0, 0, le, ld, v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
                    th = mac_tahmin_karti(v, g)
                    if th: st.markdown(th, unsafe_allow_html=True)
                    if st.button("🔍 Detay", use_container_width=True, key=f"gmac_{idx}"):
                        st.session_state.form_verileri = copy.deepcopy(v); st.session_state.kayit_yapildi = True
                        st.session_state.gelecekten_gelindi = True; st.session_state.aktif_gelecek_idx = idx
                        st.session_state.sayfa = "sonuc"; st.rerun()
                    acik += 1
                else:
                    st.markdown(mac_karti(te, td, False, 0, 0, 0, 0, v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
                    st.warning("🔒 Premium'a geç")
                st.divider()

        yasal_metin_goster()


# ==========================================
# KAYIT
# ==========================================
elif st.session_state.sayfa == "kayit":
    st.markdown('<h1>✨ Üye Ol</h1>', unsafe_allow_html=True)
    with st.form("kayit_form"):
        yk = st.text_input("👤 Kullanıcı Adı", max_chars=30)
        ys = st.text_input("🔐 Şifre", type="password")
        yst = st.text_input("🔐 Şifre Tekrar", type="password")
        yasal_onay = st.checkbox("✅ Kullanım Şartlarını okudum, kabul ediyorum.")
        c1, c2 = st.columns(2)
        with c1: kb = st.form_submit_button("✅ Kayıt Ol", use_container_width=True, type="primary")
        with c2: gb = st.form_submit_button("⬅️ Geri", use_container_width=True)
        if kb:
            if not yk.strip() or len(yk.strip()) < 3: st.error("❌ En az 3 karakter.")
            elif len(ys) < 4: st.error("❌ Şifre en az 4 karakter.")
            elif ys != yst: st.error("❌ Şifreler uyuşmuyor.")
            elif not yasal_onay: st.error("❌ Şartları kabul et.")
            else:
                b, m = kullanici_ekle(yk.strip(), ys)
                if b:
                    st.session_state["aktif_kullanici"] = yk.strip()
                    st.session_state["odeme_hedef_kadi"] = yk.strip()
                    st.session_state.sayfa = "odeme"; st.rerun()
                else: st.error(f"❌ {m}")
        if gb: st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# ÖDEME
# ==========================================
elif st.session_state.sayfa == "odeme":
    hedef = st.session_state.get("odeme_hedef_kadi") or uye_adi()
    if not hedef:
        st.error("❌ Kullanıcı yok.")
        st.stop()
    iban = ayar_al("iban", "")
    hs = ayar_al("hesap_sahibi", "")
    fh = float(ayar_al("fiyat_haftalik", 49.0)); fa = float(ayar_al("fiyat_aylik", 149.0)); fy = float(ayar_al("fiyat_yillik", 999.0))
    st.markdown(f'<h1>💳 Premium</h1><p>Kullanıcı: <b>{_e(hedef)}</b></p>', unsafe_allow_html=True)
    sec = st.radio("Süre?", ["haftalik", "aylik", "yillik"], format_func=lambda x: {"haftalik": f"Haftalık {fh:.0f} ₺", "aylik": f"Aylık {fa:.0f} ₺", "yillik": f"Yıllık {fy:.0f} ₺"}[x], index=1)
    sg = {"haftalik": 7, "aylik": 30, "yillik": 365}[sec]
    fy_ = {"haftalik": fh, "aylik": fa, "yillik": fy}[sec]
    et = {"haftalik": "Haftalık", "aylik": "Aylık", "yillik": "Yıllık"}[sec]
    st.markdown(f"### 🏦 Havale\n**Alıcı:** {_e(hs)}\n\n**IBAN:** `{_e(iban)}`\n\n**Tutar:** {fy_:.0f} ₺\n\n**Açıklama:** `{_e(hedef)}`")
    st.divider()
    bk = bekleyen_yukle()
    if hedef in bk and bk[hedef].get("durum") == "bekliyor":
        st.warning("⏳ Bekleyen bildirimin var")
    else:
        iade_onay = st.checkbox("✅ İade kabul etmiyorum")
        if st.button("📤 Ödeme Yaptım", use_container_width=True, type="primary"):
            if not iade_onay: st.error("❌ Kabul et.")
            else:
                bk[hedef] = {"tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "sure_gun": int(sg), "sure_etiket": et, "fiyat": float(fy_), "durum": "bekliyor"}
                bekleyen_kaydet(bk)
                st.success("✅ Bildirimin alındı!"); time.sleep(2); st.rerun()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Ana", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()
    with c2:
        if st.button("🔄 Kontrol", use_container_width=True):
            if abonelik_aktif_mi(hedef):
                st.success("✅ Aktif!"); time.sleep(1); st.session_state.sayfa = "giris"; st.rerun()
            else: st.info("⏳ Bekleniyor")


# ==========================================
# ADMİN ÖDEMELER
# ==========================================
elif st.session_state.sayfa == "admin_odemeler":
    if not admin_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>💳 Bekleyen Ödemeler</h1>", unsafe_allow_html=True)
    bk = bekleyen_yukle()
    if not bk: st.info("Yok.")
    else:
        for k, b in list(bk.items()):
            st.markdown(f"**👤 {_e(k)}** — {b.get('sure_etiket')} — {b.get('fiyat', 0):.0f} ₺ — {b.get('tarih')}")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("✅ Onayla", key=f"o_{k}", type="primary", use_container_width=True):
                    b_, yb = abonelik_aktif_et(k, b.get("sure_gun", 0))
                    if b_:
                        del bk[k]; bekleyen_kaydet(bk)
                        st.success(f"✅ {k} → {yb}"); time.sleep(1); st.rerun()
            with c2:
                if st.button("❌ Reddet", key=f"r_{k}", use_container_width=True):
                    del bk[k]; bekleyen_kaydet(bk); st.rerun()
            with c3:
                if st.button("🗑️ Sil", key=f"s_{k}", use_container_width=True):
                    del bk[k]; bekleyen_kaydet(bk); st.rerun()
            st.divider()
    if st.button("⬅️ Ana", type="primary", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# ADMİN ABONELER
# ==========================================
elif st.session_state.sayfa == "admin_aboneler":
    if not admin_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>👥 Aboneler</h1>", unsafe_allow_html=True)
    kl = kullanicilar_yukle()
    if not kl: st.info("Kayıt yok.")
    else:
        for k, kd in list(kl.items()):
            aktif = abonelik_aktif_mi(k)
            durum = "🌟 AKTİF" if aktif else "⚪ Pasif"
            st.markdown(f"**👤 {_e(k)}** — {durum} — Bitiş: {kd.get('abonelik_bitis', 'Yok')}")
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                if st.button("+1H", key=f"ph_{k}", use_container_width=True):
                    abonelik_aktif_et(k, 7); st.rerun()
            with c2:
                if st.button("+1A", key=f"p1_{k}", use_container_width=True):
                    abonelik_aktif_et(k, 30); st.rerun()
            with c3:
                if st.button("+1Y", key=f"py_{k}", use_container_width=True):
                    abonelik_aktif_et(k, 365); st.rerun()
            with c4:
                if st.button("İptal", key=f"ip_{k}", use_container_width=True):
                    abonelik_iptal_et(k); st.rerun()
            with c5:
                if st.button("🗑️", key=f"ks_{k}", use_container_width=True):
                    kullanici_sil(k); st.rerun()
            st.divider()
    if st.button("⬅️ Ana", type="primary", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# ADMİN BİLDİRİMLER
# ==========================================
elif st.session_state.sayfa == "admin_bildirimler":
    if not admin_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>📬 Bildirimler</h1>", unsafe_allow_html=True)
    bd = bildirimler_yukle()
    if not bd: st.info("Yok.")
    else:
        for b in sorted(bd, key=lambda x: x.get("tarih", ""), reverse=True):
            bid = b.get("id")
            st.markdown(f"**{b.get('tip')}** — {_e(b.get('kullanici', ''))} — {b.get('tarih')}")
            st.write(f"**Konu:** {_e(b.get('konu', ''))}")
            st.write(_e(b.get('mesaj', '')))
            yanit = st.text_area("Yanıt", value=b.get("cevap", ""), key=f"cy_{bid}")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💬 Kaydet", key=f"kaydet_{bid}", use_container_width=True, type="primary"):
                    bildirim_guncelle(bid, cevap=yanit, durum="okundu"); st.rerun()
            with c2:
                if st.button("🗑️ Sil", key=f"sil_{bid}", use_container_width=True):
                    bildirim_sil(bid); st.rerun()
            st.divider()
    if st.button("⬅️ Ana", type="primary", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# KULLANICI BİLDİRİM
# ==========================================
elif st.session_state.sayfa == "kullanici_bildirim":
    if not uye_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>📬 Bildirim Gönder</h1>", unsafe_allow_html=True)
    with st.form("bildirim_form"):
        tip = st.selectbox("Kategori", options=list(BILDIRIM_TIPLERI.keys()), format_func=lambda x: f"{BILDIRIM_TIPLERI[x]['ikon']} {BILDIRIM_TIPLERI[x]['isim']}")
        konu = st.text_input("Konu")
        mesaj = st.text_area("Mesaj", height=150)
        if st.form_submit_button("📤 Gönder", use_container_width=True, type="primary"):
            if not konu.strip() or not mesaj.strip(): st.error("❌")
            else:
                bildirim_ekle(uye_adi(), tip, konu.strip(), mesaj.strip())
                st.success("✅"); time.sleep(1); st.rerun()
    st.divider()
    bl = kullanici_bildirimleri(uye_adi())
    for b in sorted(bl, key=lambda x: x.get("tarih", ""), reverse=True):
        st.markdown(f"**{b.get('tip')}** — {b.get('durum')}")
        st.write(f"**{_e(b.get('konu', ''))}**: {_e(b.get('mesaj', ''))}")
        if b.get("cevap"): st.info(f"💬 {b['cevap']}")
        st.divider()


# ==========================================
# GELECEK
# ==========================================
elif st.session_state.sayfa == "gelecek_admin":
    if not admin_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    gel = st.session_state.gelecek_analizler
    st.caption(f"Toplam: **{len(gel)}** maç")
    if not gel: st.info("Gelecek maç yok.")
    else:
        sirali = sorted(enumerate(gel), key=lambda x: saat_sirala_anahtari(x[1]))
        for idx, g in sirali:
            v = g["veri"]; te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
            st.markdown(mac_karti(te, td, False, 0, 0, 0, 0, v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
            c1, c2 = st.columns([5, 1])
            with c1:
                if st.button("🔍 Detay", key=f"gmac_{idx}", use_container_width=True):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True; st.session_state.gelecekten_gelindi = True
                    st.session_state.aktif_gelecek_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
            with c2:
                if st.button("🗑️", key=f"gsil_{idx}"):
                    st.session_state.gelecek_analizler.pop(idx)
                    gelecek_kaydet(st.session_state.gelecek_analizler); st.rerun()
            st.divider()
    if st.button("⬅️ Ana", type="primary", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# GEÇMİŞ
# ==========================================
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gc = st.session_state.gecmis_analizler
    st.caption(f"Toplam: **{len(gc)}** maç")
    if not gc: st.info("Kayıt yok.")
    else:
        modern_istatistik_grafik()
        st.divider()
        for i, g in enumerate(reversed(gc)):
            idx = len(gc) - 1 - i; v = g["veri"]
            te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
            se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
            st.markdown(mac_karti(te, td, True, se, sd, 0, 0, "", v.get("ulke", ""), ""), unsafe_allow_html=True)
            if admin_mi():
                if st.button("🗑️", key=f"sil_{idx}"):
                    st.session_state.gecmis_analizler.pop(idx)
                    gecmis_kaydet(st.session_state.gecmis_analizler); st.rerun()
            st.divider()
    if admin_mi():
        if st.button("🗑️ Tüm Geçmişi Sil", use_container_width=True):
            st.session_state.gecmis_analizler = []
            gecmis_kaydet([]); st.rerun()
    if st.button("⬅️ Ana", type="primary", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# BACKTEST
# ==========================================
elif st.session_state.sayfa == "backtest":
    if not admin_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>🔬 Backtest</h1>", unsafe_allow_html=True)
    st.info("Backtest fonksiyonu basitleştirildi.")
    if st.button("⬅️ Ana", type="primary", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# AYARLAR
# ==========================================
elif st.session_state.sayfa == "ayarlar":
    if not admin_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>⚙️ Ayarlar</h1>", unsafe_allow_html=True)
    mv = st.session_state.esikler.copy()
    st.markdown("### 🏦 Ödeme")
    c1, c2 = st.columns(2)
    with c1: yiban = st.text_input("IBAN", value=mv.get("iban", ""))
    with c2: yhs = st.text_input("Hesap Sahibi", value=mv.get("hesap_sahibi", ""))
    st.markdown("### 💰 Fiyatlar")
    c1, c2, c3 = st.columns(3)
    with c1: yfh = st.number_input("Haftalık", min_value=1.0, value=float(mv.get("fiyat_haftalik", 49.0)))
    with c2: yfa = st.number_input("Aylık", min_value=1.0, value=float(mv.get("fiyat_aylik", 149.0)))
    with c3: yfy = st.number_input("Yıllık", min_value=1.0, value=float(mv.get("fiyat_yillik", 999.0)))
    st.markdown("### 🔓 Ücretsiz Kota")
    yk = st.number_input("Kaç maç ücretsiz?", 0, 50, int(mv.get("ucretsiz_kotasi", 3)))
    st.markdown("### 🎯 Eşikler")
    c1, c2, c3 = st.columns(3)
    with c1: ye1 = st.slider("1 %", 0, 100, int(mv.get("esik_1", 55.0)))
    with c2: yex = st.slider("X %", 0, 100, int(mv.get("esik_x", 55.0)))
    with c3: ye2 = st.slider("2 %", 0, 100, int(mv.get("esik_2", 55.0)))
    c4, c5 = st.columns(2)
    with c4: yu = st.slider("Üst %", 0, 100, int(mv.get("ust", 65.0)))
    with c5: ya = st.slider("Alt %", 0, 100, int(mv.get("alt", 55.0)))
    c6, c7 = st.columns(2)
    with c6: ykv = st.slider("KG Var %", 0, 100, int(mv.get("kg_var", 57.0)))
    with c7: yky = st.slider("KG Yok %", 0, 100, int(mv.get("kg_yok", 72.0)))
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💾 Kaydet", use_container_width=True, type="primary"):
            y = dict(mv); y.update({"iban": yiban, "hesap_sahibi": yhs, "fiyat_haftalik": float(yfh), "fiyat_aylik": float(yfa), "fiyat_yillik": float(yfy), "ucretsiz_kotasi": int(yk), "esik_1": float(ye1), "esik_x": float(yex), "esik_2": float(ye2), "ust": float(yu), "alt": float(ya), "kg_var": float(ykv), "kg_yok": float(yky)})
            st.session_state.esikler = y; ayarlar_kaydet(y); st.success("✅")
    with c2:
        if st.button("🔄 Sıfırla", use_container_width=True):
            ayarlar_kaydet({}); st.rerun()
    with c3:
        if st.button("⬅️ Ana", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SONUÇ
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri; a = analiz_hesapla(v)
    te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
    sb = v.get("skor_belli", False); se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    st.markdown(mac_karti(te, td, sb, se, sd, a["lam_ev"], a["lam_dep"]), unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)
    s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    st.markdown(f"### 🏆 Final: **{s1}** (%{y1:.1f})")
    if st.button("🔄 Yeni", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI); st.session_state.sayfa = "giris"; st.rerun()
