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

# ... (TÜM CSS BLOKLARI AYNI — değişmedi) ...
# ==========================================
# 🎯 LİG FİLTRESİ — Sadece 1. ve 2. Ligler
# ==========================================
# Her ülke için izin verilen liglerin "Standings" metniyle eşleşen
# anahtar kelimeleri. Sadece bu liglerden gelen maçlar kabul edilir.
IZINLI_LIG_ANAHTARLARI = [
    # 🏴 İngiltere
    "england - premier league",
    "england - championship",
    # 🇹🇷 Türkiye
    "turkey - super lig",
    "turkey - 1. lig",
    "türkiye - süper lig",
    "türkiye - 1. lig",
    # 🇪🇸 İspanya
    "spain - la liga",
    "spain - la liga 2",
    "spain - segunda division",
    # 🇩🇪 Almanya
    "germany - bundesliga",
    "germany - 2. bundesliga",
    # 🇮🇹 İtalya
    "italy - serie a",
    "italy - serie b",
    # 🇫🇷 Fransa
    "france - ligue 1",
    "france - ligue 2",
    # 🇳🇱 Hollanda
    "netherlands - eredivisie",
    "netherlands - eerste divisie",
    # 🇵🇹 Portekiz
    "portugal - primeira liga",
    "portugal - liga portugal 2",
    "portugal - segunda liga",
    # 🇧🇪 Belçika
    "belgium - jupiler pro league",
    "belgium - first division b",
    "belgium - challenger pro league",
]

# Kadın, genç, rezerv ve hazırlık maçlarını engelleyen kelimeler
YASAKLI_KELIMELER = {
    "women", "womens", "women's", "kadın", "kadin", "female", "females",
    "ladies", "kizlar", "kızlar", "kiz", "kız",
    "u15", "u16", "u17", "u18", "u19", "u20", "u21", "u22", "u23",
    "youth", "genç", "genc", "gençlik", "genclik",
    "friendly", "friendlies", "hazırlık", "hazirlik",
    "reserve", "reserves", "yedek",
    "academy", "akademi",
    "b team", "ii team",
}


def _ulke_izinli_mi(ulke_lig_metni, takim_ev="", takim_dep=""):
    """
    Maç verisindeki 'Standings' bilgisinden (ülke - lig adı) yola çıkarak
    sadece izin verilen 1. ve 2. ligleri kabul eder.
    Örn: 'england - premier league' → ✅ kabul
         'england - league one'    → ❌ red
         'turkey - super lig'      → ✅ kabul
         'turkey - 2. lig'         → ❌ red
    """
    if not ulke_lig_metni:
        return False

    metin = str(ulke_lig_metni).strip().lower()
    if not metin:
        return False

    # Kadın/genç/hazırlık/rezerv maçlarını her durumda engelle
    tum_metin = f"{metin} {takim_ev} {takim_dep}".lower()
    for yasak in YASAKLI_KELIMELER:
        if yasak in tum_metin:
            return False

    # İzinli lig anahtar kelimelerinden biri geçiyor mu?
    for anahtar in IZINLI_LIG_ANAHTARLARI:
        if anahtar in metin:
            return True

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
if "bt_market" not in st.session_state: st.session_state.bt_market = {"1x2": False, "kg_var": False, "kg_yok": False, "ust": False, "alt": False}
if "bt_market_esik" not in st.session_state: st.session_state.bt_market_esik = {"esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "kg_var": 70.0, "kg_yok": 70.0, "ust": 70.0, "alt": 70.0}
if "bt_sonuc" not in st.session_state: st.session_state.bt_sonuc = None
if "bt_detaylar" not in st.session_state: st.session_state.bt_detaylar = []
if "toplu_cek_ozet" not in st.session_state: st.session_state.toplu_cek_ozet = None
if "skor_ozet" not in st.session_state: st.session_state.skor_ozet = None
if "aktif_kullanici" not in st.session_state: st.session_state.aktif_kullanici = None
if "odeme_hedef_kadi" not in st.session_state: st.session_state.odeme_hedef_kadi = None
if "sil_onay_kadi" not in st.session_state: st.session_state.sil_onay_kadi = None
if "kayit_yasal_onay" not in st.session_state: st.session_state.kayit_yasal_onay = False
if "odeme_yasal_onay" not in st.session_state: st.session_state.odeme_yasal_onay = False


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


ULKE_BAYRAK = {"switzerland": "🇨🇭", "isviçre": "🇨🇭", "i̇sviçre": "🇨🇭", "england": "🏴", "ingiltere": "🏴", "i̇ngiltere": "🏴", "spain": "🇪🇸", "ispanya": "🇪🇸", "italy": "🇮🇹", "italya": "🇮🇹", "germany": "🇩🇪", "almanya": "🇩🇪", "france": "🇫🇷", "fransa": "🇫🇷", "netherlands": "🇳🇱", "hollanda": "🇳🇱", "portugal": "🇵🇹", "portekiz": "🇵🇹", "belgium": "🇧🇪", "belçika": "🇧🇪", "turkey": "🇹🇷", "türkiye": "🇹🇷", "turkiye": "🇹🇷", "argentina": "🇦🇷", "arjantin": "🇦🇷", "brazil": "🇧🇷", "brezilya": "🇧🇷", "mexico": "🇲🇽", "meksika": "🇲🇽", "usa": "🇺🇸", "abd": "🇺🇸", "japan": "🇯🇵", "japonya": "🇯🇵", "south korea": "🇰🇷", "güney kore": "🇰🇷", "china": "🇨🇳", "çin": "🇨🇳", "russia": "🇷🇺", "rusya": "🇷🇺", "ukraine": "🇺🇦", "ukrayna": "🇺🇦", "poland": "🇵🇱", "polonya": "🇵🇱", "greece": "🇬🇷", "yunanistan": "🇬🇷", "scotland": "🏴", "wales": "🏴", "ireland": "🇮🇪", "austria": "🇦🇹", "avusturya": "🇦🇹", "croatia": "🇭🇷", "hırvatistan": "🇭🇷", "serbia": "🇷🇸", "sırbistan": "🇷🇸", "romania": "🇷🇴", "romanya": "🇷🇴", "bulgaria": "🇧🇬", "bulgaristan": "🇧🇬", "denmark": "🇩🇰", "danimarka": "🇩🇰", "sweden": "🇸🇪", "norway": "🇳🇴", "norveç": "🇳🇴", "finland": "🇫🇮", "finlandiya": "🇫🇮", "iceland": "🇮🇸", "hungary": "🇭🇺", "macaristan": "🇭🇺", "czech": "🇨🇿", "slovakia": "🇸🇰", "slovenia": "🇸🇮", "saudi": "🇸🇦", "suudi arabistan": "🇸🇦", "qatar": "🇶🇦", "katar": "🇶🇦", "egypt": "🇪🇬", "mısır": "🇪🇬", "morocco": "🇲🇦", "fas": "🇲🇦", "algeria": "🇩🇿", "cezayir": "🇩🇿", "tunisia": "🇹🇳", "tunus": "🇹🇳", "nigeria": "🇳🇬", "nijerya": "🇳🇬", "south africa": "🇿🇦", "australia": "🇦🇺", "avustralya": "🇦🇺", "new zealand": "🇳🇿", "india": "🇮🇳", "hindistan": "🇮🇳", "iran": "🇮🇷", "iraq": "🇮🇶", "irak": "🇮🇶", "israel": "🇮🇱", "colombia": "🇨🇴", "kolombiya": "🇨🇴", "chile": "🇨🇱", "şili": "🇨🇱", "peru": "🇵🇪", "uruguay": "🇺🇾", "ecuador": "🇪🇨", "paraguay": "🇵🇾", "bolivia": "🇧🇴", "venezuela": "🇻🇪", "canada": "🇨🇦", "kanada": "🇨🇦", "kosovo": "🇽🇰", "kosova": "🇽🇰", "albania": "🇦🇱", "arnavutluk": "🇦🇱", "georgia": "🇬🇪", "gürcistan": "🇬🇪", "armenia": "🇦🇲", "azerbaijan": "🇦🇿", "azerbaycan": "🇦🇿", "kazakhstan": "🇰🇿", "kazakistan": "🇰🇿", "uzbekistan": "🇺🇿", "belarus": "🇧🇾", "latvia": "🇱🇻", "lithuania": "🇱🇹", "estonia": "🇪🇪", "luxembourg": "🇱🇺", "malta": "🇲🇹", "cyprus": "🇨🇾", "kıbrıs": "🇨🇾", "montenegro": "🇲🇪", "karadağ": "🇲🇪", "north macedonia": "🇲🇰", "bosnia": "🇧🇦", "bosna": "🇧🇦", "moldova": "🇲🇩"}


def ulke_bayrak_bul(ulke_adi):
    if not ulke_adi: return "🌍"
    u = ulke_adi.lower().strip()
    for a in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if a in u: return ULKE_BAYRAK[a]
    return "🌍"


def _ulke_bul(metin):
    """
    'Standings' satırından ülke ve lig adını birlikte çeker.
    Örn: 'Standings' sonrası 'England - Premier League' → 'england - premier league'
    """
    m = re.search(r'Standings\s+([^\n]+)', metin)
    if not m:
        return ""
    s = m.group(1).strip()
    if not s:
        return ""
    # Tam satırı (ülke - lig adı) küçük harfle döndür
    return s.lower().strip()


def clamp(x, lo, hi): return max(lo, min(hi, x))


def guven_seviyesi_bul(o):
    if o >= ESIK_YUKSEK: return ("yuksek", "🟢", "success", "Yüksek")
    if o >= ESIK_ORTA: return ("orta", "🟡", "warning", "Orta")
    if o >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "error", "Belirsiz")
    return ("cok_dusuk", "⚫", "error", "Düşük")


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
    tse = v.get("team_scored_ev", 0); tsd = v.get("team_scored_dep", 0)
    if tse > 0: he *= clamp(tse / 60, 0.7, 1.3)
    if tsd > 0: hd *= clamp(tsd / 60, 0.7, 1.3)
    sd = yd if yd > 0 else 1.2; se = ye if ye > 0 else 1.0
    cse = v.get("clean_sheets_ev", 0.0); csd = v.get("clean_sheets_dep", 0.0)
    def cf(cs):
        if cs <= 0: return 1.0
        if cs < 40.0: return 1.0 - (cs / 250.0)
        return max(0.40, 0.84 - (cs - 40.0) * (0.44 / 60.0))
    df = cf(cse); ef = cf(csd)
    le = he * 0.60 + sd * 0.40; ld = hd * 0.60 + se * 0.40
    u25e = v.get("ust25_ev", 0); u25d = v.get("ust25_dep", 0)
    if u25e > 0: le *= clamp(u25e / 50, 0.85, 1.15)
    if u25d > 0: ld *= clamp(u25d / 50, 0.85, 1.15)
    kge = v.get("kg_siklik_ev", 0); kgd = v.get("kg_siklik_dep", 0)
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
    anahtar = json.dumps(v2, sort_keys=True, ensure_ascii=False)
    if "bt_analiz_cache" not in st.session_state: st.session_state.bt_analiz_cache = {}
    cache = st.session_state.bt_analiz_cache
    if anahtar not in cache:
        a = analiz_hesapla(v2)
        cache[anahtar] = {"ust_25": a["ust_25"], "kg_var_model": a["kg_var_model"], "p1": a["p1"], "px": a["px"], "p2": a["p2"]}
    return cache[anahtar]


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
            try:
                ya = yeniden_analiz(v)
                u25 = ya["ust_25"]; kgv = ya["kg_var_model"]
                p1y = ya["p1"]; pxy = ya["px"]; p2y = ya["p2"]
            except Exception:
                u25 = analiz.get("ust_25", 50); kgv = analiz.get("kg_var_model", 50)
                p1y = analiz.get("p1", 33.33); pxy = analiz.get("px", 33.33); p2y = analiz.get("p2", 33.34)
            alt = 100 - u25; kgy = 100 - kgv
            mk = {"takim_ev": v.get("takim_ev", "Ev"), "takim_dep": v.get("takim_dep", "Dep"), "skor": f"{se}-{sd}", "gercek_kg": "Var" if gkv else "Yok", "gercek_gol": "Üst" if gust else "Alt", "gercek_1x2": g1, "detaylar": []}
            if ms.get("1x2", False):
                s, y = max([("1", p1y), ("X", pxy), ("2", p2y)], key=lambda x: x[1])
                ek = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}[s]; esc = me.get(ek, 55.0)
                if y >= esc:
                    if s == g1: sonuc["1x2"]["dogru"] += 1; mk["detaylar"].append(f"1X2: {s} ✅")
                    else: sonuc["1x2"]["yanlis"] += 1; mk["detaylar"].append(f"1X2: {s} ❌")
            if ms.get("kg_var", False) and kgv >= me["kg_var"] and kgv >= kgy:
                if gkv: sonuc["kg_var"]["dogru"] += 1; mk["detaylar"].append("KG Var ✅")
                else: sonuc["kg_var"]["yanlis"] += 1; mk["detaylar"].append("KG Var ❌")
            if ms.get("kg_yok", False) and kgy >= me["kg_yok"] and kgy >= kgv:
                if not gkv: sonuc["kg_yok"]["dogru"] += 1; mk["detaylar"].append("KG Yok ✅")
                else: sonuc["kg_yok"]["yanlis"] += 1; mk["detaylar"].append("KG Yok ❌")
            if ms.get("ust", False) and u25 >= me["ust"] and u25 >= alt:
                if gust: sonuc["ust"]["dogru"] += 1; mk["detaylar"].append("Üst ✅")
                else: sonuc["ust"]["yanlis"] += 1; mk["detaylar"].append("Üst ❌")
            if ms.get("alt", False) and alt >= me["alt"] and alt >= u25:
                if not gust: sonuc["alt"]["dogru"] += 1; mk["detaylar"].append("Alt ✅")
                else: sonuc["alt"]["yanlis"] += 1; mk["detaylar"].append("Alt ❌")
            if mk["detaylar"]: detaylar.append(mk)
        except Exception: continue
    return sonuc, detaylar


MANUEL_ALANLAR = {
    "Sıralama": [("siralama_ev", "Ev Sıralaması", "int", 1), ("siralama_dep", "Dep Sıralaması", "int", 1)],
    "Takım isimleri (Ev)": [("takim_ev", "Ev Takım Adı", "str", "")],
    "Takım isimleri (Dep)": [("takim_dep", "Dep Takım Adı", "str", "")],
    "PPG (Ev Form)": [("ppg_ev", "PPG (Ev)", "float", 0.0)],
    "MPG (Dep Form)": [("mpg_dep", "MPG (Dep)", "float", 0.0)],
    "xG": [("xg_ev", "xG (Ev)", "float", 0.0), ("xg_dep", "xG (Dep)", "float", 0.0)],
    "Atılan Gol": [("atilan_ev", "Atılan Gol (Ev)", "float", 0.0), ("atilan_dep", "Atılan Gol (Dep)", "float", 0.0)],
    "Yenen Gol": [("yenen_ev", "Yenen Gol (Ev)", "float", 0.0), ("yenen_dep", "Yenen Gol (Dep)", "float", 0.0)],
}


def _cift_tab(etiket, blok):
    pattern = r'([\d.,]+)%?\s*\t\s*' + re.escape(etiket) + r'\s*\t\s*([\d.,]+)%?'
    m = re.search(pattern, blok, re.IGNORECASE)
    if m:
        try: return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError: pass
    pattern2 = r'([\d.,]+)%?\s{1,4}' + re.escape(etiket) + r'\s{1,4}([\d.,]+)%?'
    m = re.search(pattern2, blok, re.IGNORECASE)
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
            if 1 <= sira <= 30:
                devam = metin[m.end()-1:]
                m_puan = re.match(r'[\s\S]{0,80}?\r?\n\s*(\d{1,2})\s*\r?\n', devam)
                puan = int(m_puan.group(1)) if m_puan else 0
                return sira, puan
        except (ValueError, AttributeError): pass
    return None, None


def sportytrader_veri_cikar(metin):
    veri = {}; okunamayanlar = []
    m = re.search(r'^([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s*-\s*([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s+Stats', metin, re.MULTILINE)
    if m:
        veri["takim_ev"] = m.group(1).strip(); veri["takim_dep"] = m.group(2).strip()
    m = re.search(r'Time\s*\t\s*(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1).strip()
    else:
        m = re.search(r'\d{1,2}\.\d{1,2}\.\d{2,4}\s+(\d{1,2}:\d{2})', metin)
        if m: veri["saat"] = m.group(1).strip()
    m = re.search(r'Date\s*\t\s*(\d{1,2}\.\d{1,2}\.\d{2,4})', metin)
    if m: veri["tarih"] = m.group(1).strip()
    else:
        m = re.search(r'(\d{1,2}\.\d{1,2}\.\d{2,4})\s+\d{1,2}:\d{2}', metin)
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
    if veri.get("siralama_ev", 0) == 0: okunamayanlar.append("Sıralama (Ev)")
    if veri.get("siralama_dep", 0) == 0: okunamayanlar.append("Sıralama (Dep)")
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
    veri["format"] = "sportytrader"
    return veri, okunamayanlar


def metinden_veri_cikar(metin):
    metin = metin.replace(",", ".")
    if "Main Stats" in metin and "Goals scored per game" in metin:
        veri, okunamayanlar = sportytrader_veri_cikar(metin)
        if not veri.get("takim_ev"): okunamayanlar.append("Takım isimleri (Ev)")
        if not veri.get("takim_dep"): okunamayanlar.append("Takım isimleri (Dep)")
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
                        const inp3 = document.querySelector('input[id*="game_count_5"], input[id*="5"]');
                        if (inp3 && inp3.type === 'radio') { inp3.checked = true; inp3.dispatchEvent(new Event('change', { bubbles: true })); inp3.click(); return true; }
                        return false;
                    }""")
                except Exception: tiklandi = False
                if not tiklandi:
                    for sel in ["input[type='radio'][value='5']", "input#game_count_5", "label.containerbutton:has-text('5')", "label:has-text('5') input"]:
                        try:
                            pg.click(sel, timeout=2000); tiklandi = True; break
                        except Exception: continue
                pg.wait_for_timeout(3500)
                try:
                    pg.wait_for_function("""() => { const t = document.body.innerText || ''; return t.includes('Last 5 Games') || t.includes('last 5 games'); }""", timeout=8000)
                except Exception: pass
                pg.wait_for_timeout(1000)
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
            r = requests.get(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9", "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1"}, timeout=timeout)
            if r.status_code == 200 and r.text and len(r.text) > 500: return r.text, None
            hata = f"HTTP {r.status_code} • Boyut: {len(r.text) if r.text else 0}"
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
            p = baslik.replace(" Stats", "").replace(" stats", "").split(" - ")
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
        for pat in [r'([\d.,]+)\s*%?\s*\t\s*' + re.escape(label) + r'\s*\t\s*([\d.,]+)', r'([\d.,]+)\s*%?\s*\|\s*' + re.escape(label) + r'\s*\|\s*([\d.,]+)', r'([\d.,]+)\s*%?\s+' + re.escape(label) + r'\s+([\d.,]+)\s*%?', r'([\d.,]+)\s*%?\s*\n\s*' + re.escape(label) + r'\s*\n\s*([\d.,]+)']:
            mm = re.search(pat, metin, re.IGNORECASE)
            if mm:
                try: return float(mm.group(1).replace(",", ".")), float(mm.group(2).replace(",", "."))
                except ValueError: continue
        return None, None
    for label, k_ev, k_dep in [("Goals scored per game", "atilan_ev", "atilan_dep"), ("Goals conceded per game", "yenen_ev", "yenen_dep"), ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"), ("Team scored", "team_scored_ev", "team_scored_dep"), ("Both Teams to Score", "kg_siklik_ev", "kg_siklik_dep"), ("Over 2.5 goals", "ust25_ev", "ust25_dep"), ("Over 1.5 goals", "ust15_ev", "ust15_dep"), ("Over 3.5 goals", "ust35_ev", "ust35_dep")]:
        a, b = _cift(label)
        if a is not None and veri.get(k_ev, 0) == 0: veri[k_ev] = a; veri[k_dep] = b
    for label, k_ev, k_dep in [("Win", "galibiyet_ev", "galibiyet_dep"), ("Draw", "beraberlik_ev", "beraberlik_dep"), ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
        mm = re.search(r'([\d.,]+)\s*%\s*\t\s*' + label + r'\s*\t\s*([\d.,]+)\s*%', metin, re.MULTILINE)
        if mm:
            try:
                veri[k_ev] = float(mm.group(1).replace(",", "."))
                veri[k_dep] = float(mm.group(2).replace(",", "."))
            except ValueError: pass
    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) + veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2
    veri["format"] = "mutating"
    if url: veri["kaynak_url"] = url
    if not veri.get("takim_ev"): okunamayanlar.append("Takım isimleri (Ev)")
    if not veri.get("takim_dep"): okunamayanlar.append("Takım isimleri (Dep)")
    if veri.get("atilan_ev", 0) == 0: okunamayanlar.append("Atılan Gol (Ev)")
    if veri.get("yenen_ev", 0) == 0: okunamayanlar.append("Yenen Gol (Ev)")

    try:
        form_bloklari = re.findall(
            r'(?:^|\n)\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*\r?\n\s*([WDL])\s*(?=\r?\n)',
            metin, re.MULTILINE
        )
        if form_bloklari and len(form_bloklari) >= 2:
            veri["form_str_ev"] = "".join(form_bloklari[0])
            veri["form_str_dep"] = "".join(form_bloklari[1])
        else:
            try:
                soup2 = BeautifulSoup(html, "html.parser")
                form_kaplari = soup2.select(".form, .match-form, .last5, .form-string, [class*='form']")
                form_harfleri = []
                for kap in form_kaplari:
                    for c in kap.get_text(" ", strip=True):
                        if c.upper() in "WDL":
                            form_harfleri.append(c.upper())
                if len(form_harfleri) >= 10:
                    veri["form_str_ev"] = "".join(form_harfleri[:5])
                    veri["form_str_dep"] = "".join(form_harfleri[5:10])
            except Exception:
                pass
            if not veri.get("form_str_ev"):
                form_harfleri = re.findall(r'(?:^|\s)([WDL])(?=\s|$)', metin)
                if len(form_harfleri) >= 10:
                    veri["form_str_ev"] = "".join(form_harfleri[:5])
                    veri["form_str_dep"] = "".join(form_harfleri[5:10])
    except Exception:
        pass

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
        if idx < 0 or idx >= len(gel_list):
            st.session_state["_inline_msg"] = ("error", "❌ Maç bulunamadı (indeks geçersiz)"); return
        k = gel_list[idx]
        k["veri"]["skor_ev"] = yse_val; k["veri"]["skor_dep"] = ysd_val; k["veri"]["skor_belli"] = True
        yd = sonuc_hesapla(k)
        if yd: k["dogruluk"] = yd
        st.session_state.gecmis_analizler.append(k); st.session_state.gelecek_analizler.pop(idx)
        gecmis_kaydet(st.session_state.gecmis_analizler); gelecek_kaydet(st.session_state.gelecek_analizler)
        st.session_state["_inline_msg"] = ("success", f"✅ {k['veri'].get('takim_ev','?')} vs {k['veri'].get('takim_dep','?')} → {yse_val}-{ysd_val} Geçmişe taşındı!")
    except Exception as e:
        st.session_state["_inline_msg"] = ("error", f"❌ Taşıma hatası: {e}")


def _gelecek_mac_isle(mac, mevcut_urls, esikler=None):
    try:
        veri, _ = _mac_detay_cek_5games(mac["url"])
        if not veri: return ("hata", mac, "Veri çekilemedi", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        if not veri.get("saat"): veri["saat"] = mac.get("saat", "")
        if veri.get("saat"): veri["saat"] = saat_2_saat_ileri(veri["saat"])
        veri["kaynak_url"] = mac["url"]
        # 🎯 YENİ LİG FİLTRESİ: Sadece 1. ve 2. liglere izin ver
        ulke_lig = str(veri.get("ulke", "") or "").strip()
        if not ulke_lig:
            return ("ulke_yok", veri, "Ülke/lig bilgisi yok", None)
        if not _ulke_izinli_mi(ulke_lig, veri.get("takim_ev", ""), veri.get("takim_dep", "")):
            return ("ulke_yok", veri, f"İzin verilmeyen lig: {ulke_lig}", None)
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
                if sonuc == "ulke_yok":
                    pass
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
        if not takim_ev:
            txt = link.get_text(" ", strip=True)
            if " - " in txt:
                p = txt.split(" - "); takim_ev = p[0].strip(); takim_dep = p[1].strip() if len(p) > 1 else ""
        maclar.append({"url": href, "takim_ev": takim_ev, "takim_dep": takim_dep})
        if len(maclar) >= adet: break
    return maclar, []


def _gecmis_mac_isle(mac, mevcut_urls):
    try:
        if mac["url"] in mevcut_urls: return ("atlandi", None, "Zaten var", None)
        html, hata = _scrapingbee_get(mac["url"], render_js=True, mac_sec="5", dogrula=True)
        if hata or not html: return ("hata", mac, hata or "HTML yok", None)
        veri, _ = _mac_html_parse(html, mac["url"])
        if not veri.get("skor_belli", False): return ("atlandi", None, "Skor yok (bitmemiş maç)", None)
        if veri.get("atilan_ev", 0) == 0 or veri.get("yenen_ev", 0) == 0: return ("atlandi", None, "İstatistik eksik", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
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


# ==========================================
# FLASHSCORE SKOR ENTEGRASYONU
# ==========================================
def _takim_normalize(isim):
    if not isim: return ""
    s = str(isim).lower().strip()
    s = (s.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c").replace("İ", "i").replace("Ğ", "g").replace("Ü", "u").replace("Ş", "s").replace("Ö", "o").replace("Ç", "c"))
    s = re.sub(r'[^\w\s]', ' ', s)
    for ek in [" fc", " sc", " cf", " sk", " ac", " as", " fk", " if", " bk"]:
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
        try: maclar.append({"id": alanlar["AA"], "ev": alanlar["AE"].strip(), "dep": alanlar["AF"].strip(), "skor_ev": int(se), "skor_dep": int(sd), "durum": alanlar.get("AB", "")})
        except (ValueError, TypeError): continue
    return maclar


@st.cache_data(ttl=120, show_spinner=False)
def _flashscore_gun_maclari(day_offset=0):
    url = f"https://global.flashscore.ninja/2/x/feed/f_1_{day_offset}_3_en_1"
    try:
        r = requests.get(url, headers={"x-fsign": "SW9D1eZo", "User-Agent": UA, "Accept": "*/*", "Referer": "https://www.flashscore.com/"}, timeout=20)
        if r.status_code != 200: return []
        return _flashscore_feed_parse(r.text)
    except Exception: return []


def _flashscore_skor_bul(takim_ev, takim_dep, tarih=""):
    ev_n = _takim_normalize(takim_ev); dep_n = _takim_normalize(takim_dep)
    if not ev_n or not dep_n: return None
    offsets = [0]
    if tarih:
        try:
            m = re.match(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', tarih)
            if m:
                mac_t = datetime(int(m.group(3)), int(m.group(2)), int(m.group(1))).date()
                off = (mac_t - datetime.now().date()).days
                if -7 <= off <= 7: offsets = [off, 0, off - 1, off + 1]
        except Exception: pass
    tum = []
    for off in dict.fromkeys(offsets):
        try: tum.extend(_flashscore_gun_maclari(off))
        except Exception: continue
    if not tum: return None
    for m in tum:
        if m.get("durum") != "3": continue
        if _takim_normalize(m["ev"]) == ev_n and _takim_normalize(m["dep"]) == dep_n: return (m["skor_ev"], m["skor_dep"])
    en_iyi_puan, en_iyi_skor = 0.0, None
    for m in tum:
        if m.get("durum") != "3": continue
        puan = (_benzerlik(ev_n, _takim_normalize(m["ev"])) + _benzerlik(dep_n, _takim_normalize(m["dep"])))
        if puan > en_iyi_puan: en_iyi_puan, en_iyi_skor = puan, (m["skor_ev"], m["skor_dep"])
    if en_iyi_puan >= 1.4: return en_iyi_skor
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
            r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=30)
            if r.status_code == 200 and r.text: html = r.text
            else: hata = f"HTTP {r.status_code}"
        except Exception as e: hata = f"Bağlantı: {str(e)[:80]}"
    skor = _skor_parse(html) if html else None
    if skor is None and tarayici_yedek and url:
        try:
            h2 = _playwright_skor_cek(url, timeout=25)
            if h2: skor = _skor_parse(h2)
        except Exception as e: hata = f"Tarayıcı: {str(e)[:120]}"
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
    st.session_state.aktif_gelecek_idx = None
    st.session_state.gelecekten_gelindi = False
    gecmis_kaydet(st.session_state.gecmis_analizler); gelecek_kaydet(st.session_state.gelecek_analizler)
    return {"tasinan": tasinan, "bitmemis": bitmemis, "hatalar": hatalar, "toplam": len(isler)}


# ==========================================
# TASARIM YARDIMCILARI
# ==========================================
def _e(x): return _html.escape(str(x))
def rozet(m, t="gray"): return f'<span class="fa-badge fa-b-{t}">{_e(m)}</span>'


def _donut_svg(yuzde, renk, boyut=82):
    y = max(0.0, min(100.0, yuzde)); r = 38
    cevre = 2 * 3.14159265 * r; offset = cevre * (1 - y / 100)
    return f'''<svg class="fa-donut-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="{r}" fill="none" stroke="#1a2438" stroke-width="8"/><circle cx="50" cy="50" r="{r}" fill="none" stroke="{renk}" stroke-width="8" stroke-dasharray="{cevre:.2f}" stroke-dashoffset="{offset:.2f}" stroke-linecap="round" transform="rotate(-90 50 50)"/><text x="50" y="50" text-anchor="middle" dominant-baseline="central" fill="{renk}" font-size="22" font-weight="900" font-family="Rajdhani, Inter, sans-serif">%{y:.0f}</text></svg>'''


def _sparkline_svg(degerler, renk, yukseklik=62, genislik=300):
    if not degerler or len(degerler) < 2:
        return f'<svg class="fa-spark-svg" viewBox="0 0 {genislik} {yukseklik}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;display:block;"><text x="50%" y="50%" text-anchor="middle" fill="#64748b" font-size="10">Yetersiz veri</text></svg>'
    n = len(degerler); pad_top = 8; pad_bot = 6
    h = yukseklik - pad_top - pad_bot; step_x = genislik / (n - 1) if n > 1 else genislik
    noktalar = []
    for i, v in enumerate(degerler):
        v = max(0.0, min(100.0, v)); x = i * step_x; y = pad_top + (1 - v / 100) * h
        noktalar.append((x, y))
    path_d = f"M {noktalar[0][0]:.2f} {noktalar[0][1]:.2f}"
    for i in range(1, n):
        x0, y0 = noktalar[i - 1]; x1, y1 = noktalar[i]; cx = (x0 + x1) / 2
        path_d += f" C {cx:.2f} {y0:.2f}, {cx:.2f} {y1:.2f}, {x1:.2f} {y1:.2f}"
    alan_d = path_d + f" L {genislik} {yukseklik} L 0 {yukseklik} Z"
    son_x, son_y = noktalar[-1]
    grad_id = f"grad_{renk.replace('#','').replace(':','').replace('.','')}"
    return f'''<svg viewBox="0 0 {genislik} {yukseklik}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;display:block;"><defs><linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{renk}" stop-opacity="0.45"/><stop offset="100%" stop-color="{renk}" stop-opacity="0"/></linearGradient></defs><path d="{alan_d}" fill="url(#{grad_id})"/><path d="{path_d}" fill="none" stroke="{renk}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="{son_x:.2f}" cy="{son_y:.2f}" r="3.2" fill="{renk}" stroke="#0b1220" stroke-width="1.6"/></svg>'''


def mac_karti(ev, dep, skor_belli, skor_ev, skor_dep, lam_ev, lam_dep, saat="", ulke="", tarih=""):
    bayrak = ulke_bayrak_bul(ulke); ust_bilgi = ""
    if saat or ulke or tarih:
        parcalar = []
        if bayrak != "🌍" or ulke: parcalar.append(f"{bayrak} {(ulke or '').title()}")
        if tarih: parcalar.append(f"📅 {tarih}")
        if saat: parcalar.append(f"🕐 {saat}")
        if parcalar: ust_bilgi = f'<div style="font-size:0.7rem;color:#7f92b3;margin-bottom:10px;text-align:center;">{" • ".join(parcalar)}</div>'
    if skor_belli: skor_html = f'<div style="font-size:1.8rem;font-weight:900;color:#22c55e;">{skor_ev} - {skor_dep}</div>'
    else: skor_html = '<div style="font-size:1.2rem;font-weight:800;color:#7f92b3;">VS</div>'
    gol_bilgi = ""
    if lam_ev > 0 or lam_dep > 0: gol_bilgi = f'<div style="font-size:0.75rem;color:#7f92b3;margin-top:6px;">Model beklenen gol: {lam_ev:.2f} - {lam_dep:.2f}</div>'
    return f"""<div style="background:linear-gradient(145deg,#131c2e,#0f1829);border:1px solid #1f2c44;border-radius:16px;padding:16px;margin:8px 0;box-shadow:0 4px 20px rgba(0,0,0,0.3);">{ust_bilgi}<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;"><div style="flex:1;text-align:center;font-weight:800;font-size:0.95rem;color:#eaf1fb;">{ev}</div><div style="flex:1;text-align:center;">{skor_html}</div><div style="flex:1;text-align:center;font-weight:800;font-size:0.95rem;color:#eaf1fb;">{dep}</div></div>{gol_bilgi}</div>"""


def kilitli_mac_karti(ev, dep, saat="", ulke="", tarih=""):
    bayrak = ulke_bayrak_bul(ulke); ust_bilgi = ""
    if saat or ulke or tarih:
        parcalar = []
        if bayrak != "🌍" or ulke: parcalar.append(f"{bayrak} {(ulke or '').title()}")
        if tarih: parcalar.append(f"📅 {tarih}")
        if saat: parcalar.append(f"🕐 {saat}")
        if parcalar: ust_bilgi = f'<div style="font-size:0.7rem;color:#7f92b3;margin-bottom:10px;text-align:center;">{" • ".join(parcalar)}</div>'
    return f'''<div style="background:linear-gradient(145deg,#131c2e,#0f1829);border:1px solid #1f2c44;border-radius:16px;padding:16px;margin:8px 0;box-shadow:0 4px 20px rgba(0,0,0,0.3);position:relative;overflow:hidden;opacity:0.7;"><div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:3rem;opacity:0.15;">🔒</div>{ust_bilgi}<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;filter:blur(3px);"><div style="flex:1;text-align:center;font-weight:800;font-size:0.95rem;color:#eaf1fb;">{ev}</div><div style="flex:1;text-align:center;font-size:1.2rem;font-weight:800;color:#7f92b3;">VS</div><div style="flex:1;text-align:center;font-weight:800;font-size:0.95rem;color:#eaf1fb;">{dep}</div></div><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(34,197,94,0.08),rgba(59,130,246,0.08));z-index:2;"><div style="background:linear-gradient(135deg,#16a34a,#22c55e);color:#04130a;font-weight:900;font-size:0.85rem;padding:10px 20px;border-radius:99px;box-shadow:0 8px 24px rgba(34,197,94,0.4);letter-spacing:0.5px;">🔒 PREMIUM'A GEÇ</div></div></div>'''


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
