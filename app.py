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
import subprocess, sys


# ==========================================
# YASAL METİN — Tam Sorumluluk Reddi
# ==========================================
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
- **Gelecekteki sonuçları garanti etmez**,
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

**Abonelik Süreleri:** Haftalık, Aylık ve Yıllık olmak üzere üç paket sunulmaktadır.

**Abonelik Aktivasyonu:** Ödeme yapıldıktan sonra Kullanıcı'nın **"Ödeme Yaptım"** bildirimi üzerine, ödeme kontrol edilerek **manuel olarak** aktive edilir. Aktivasyon **birkaç saat ile 24 saat** arasında tamamlanır.

**İADE KOŞULLARI:**

- **Aboneliği aktive edilmiş hiçbir kullanıcı için iade yapılmaz.**
- Yanlış/fazla/mükerrer ödemede **10 iş günü içinde** iade yapılır.
- **Hizmet memnuniyetsizliği, tahminlerin tutmaması, kayıplar veya benzeri nedenlerle iade talep edilemez.**
- Abonelik aktivasyonundan sonra **hiçbir koşulda para iadesi talep edilemez.**

---

## 9. ABONELİK İPTALİ

- Kullanıcı, aboneliğini **Uygulama içindeki "Bildirim"** bölümünden iptal talebi oluşturabilir.
- İptal talebi onaylandığında abonelik **bir sonraki yenilenme tarihine kadar** aktif kalır.
- **İptal edilen abonelikler için kısmi iade yapılmaz.**

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

Her türlü soru, görüş, şikayet, iptal ve iade talepleri için Uygulama içindeki **"Bildirim"** bölümünden iletişime geçebilirsiniz.

---

**SON SÖZ:** Bu uygulama **SADECE bilgilendirme ve analiz amaçlıdır**. Bahis oynamak **yasal risk**, **maddi kayıp riski** ve **bağımlılık riski** içerir. **YEDAM: 115**
"""


st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")


@st.cache_resource(show_spinner="Tarayıcı kuruluyor (ilk açılışta 1-2 dk sürer)...")
def _tarayici_kur():
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False, timeout=600)
    except Exception:
        pass
    return True


_tarayici_kur()


st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
    html { font-size: 13px !important; }
    body, .stApp { font-size: 0.85rem !important; }
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    h1, h2, h3, h4, .fa-score, .fa-big, .mh-stat-num, .login-title, .mh-hero-title { font-family: 'Rajdhani', 'Inter', sans-serif !important; letter-spacing: 0.4px; }
    .block-container { padding-top: 0.8rem !important; padding-bottom: 0.8rem !important; padding-left: 0.8rem !important; padding-right: 0.8rem !important; max-width: 100% !important; }
    :root { --bg-0: #060a14; --bg-1: #0b1220; --card: #131c2e; --border: #1f2c44; --text: #eaf1fb; --muted: #7f92b3; --green: #22c55e; --blue: #3b82f6; --yellow: #f59e0b; --red: #ef4444; }
    .stApp { background: radial-gradient(1200px 600px at 10% -10%, rgba(34,197,94,0.08), transparent 60%), radial-gradient(900px 500px at 100% 0%, rgba(59,130,246,0.07), transparent 60%), linear-gradient(180deg, #060a14 0%, #0b1220 100%) !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp div[data-testid="stMarkdownContainer"] { color: var(--text) !important; }
    .stApp div[data-testid="stCaptionContainer"], .stApp small { color: var(--muted) !important; }
    hr { border-color: var(--border) !important; margin: 0.5rem 0 !important; }
    h1 { font-size: 1.35rem !important; font-weight: 800 !important; margin: 0.4rem 0 !important; text-align: center; background: linear-gradient(135deg, #eaf1fb 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 0.4px; }
    h2 { font-size: 1rem !important; font-weight: 700 !important; margin: 0.4rem 0 !important; }
    h3 { font-size: 0.88rem !important; font-weight: 700 !important; margin: 0.25rem 0 !important; border-left: 3px solid var(--green); padding-left: 0.5rem; }
    p { font-size: 0.8rem !important; margin: 0.2rem 0 !important; line-height: 1.45; }
    div[data-testid="stNumberInput"] label p { font-size: 0.72rem !important; margin: 0 !important; font-weight: 600; }
    div[data-testid="stNumberInput"] input { font-size: 0.85rem !important; padding: 0.35rem 0.5rem !important; height: 2rem !important; }
    div[data-testid="stNumberInput"] button { height: 2rem !important; }
    div[data-testid="stNumberInput"] > div { margin-bottom: 0.25rem !important; }
    .stTextArea textarea, .stTextInput input, div[data-testid="stNumberInput"] input { background: var(--card) !important; color: var(--text) !important; border: 1.5px solid var(--border) !important; border-radius: 10px !important; transition: all 0.2s ease !important; }
    .stTextArea textarea:focus, .stTextInput input:focus, div[data-testid="stNumberInput"] input:focus { border-color: var(--green) !important; box-shadow: 0 0 0 4px rgba(34,197,94,0.12) !important; }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="base-input"] { background: var(--card) !important; border-radius: 10px !important; }
    .stButton button, div[data-testid="stDownloadButton"] button, div[data-testid="stFormSubmitButton"] button { background: linear-gradient(145deg, #18233a, #131c2e) !important; border: 1.5px solid var(--border) !important; border-radius: 10px !important; font-weight: 700 !important; font-size: 0.8rem !important; color: var(--text) !important; transition: all 0.2s ease !important; box-shadow: 0 2px 8px rgba(0,0,0,0.25) !important; padding: 0.35rem 0.5rem !important; }
    .stButton button p, div[data-testid="stDownloadButton"] button p, div[data-testid="stFormSubmitButton"] button p { color: var(--text) !important; font-weight: 700 !important; font-size: 0.8rem !important; }
    .stButton button:hover, div[data-testid="stDownloadButton"] button:hover { border-color: var(--green) !important; transform: translateY(-1px); box-shadow: 0 6px 20px rgba(34,197,94,0.2) !important; }
    .stButton button[kind="primary"], button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; border: none !important; box-shadow: 0 6px 20px rgba(34,197,94,0.35) !important; color: #04130a !important; }
    .stButton button[kind="primary"] p, button[data-testid="stBaseButton-primary"] p, button[data-testid="stBaseButton-primaryFormSubmit"] p { color: #04130a !important; }
    div[data-testid="stExpander"] { background: linear-gradient(145deg, var(--card), #0f1829) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; overflow: hidden; margin-bottom: 8px !important; }
    div[data-testid="stExpander"] details > summary { display: flex !important; align-items: center !important; gap: 6px !important; padding: 0.5rem 0.8rem !important; font-size: 0.82rem !important; font-weight: 700 !important; line-height: 1.3 !important; min-height: 38px !important; overflow: hidden !important; cursor: pointer !important; list-style: none !important; }
    div[data-testid="stExpander"] details > summary::-webkit-details-marker { display: none !important; }
    div[data-testid="stExpander"] details > summary::marker { display: none !important; content: "" !important; }
    div[data-testid="stExpander"] details > summary:hover { background: rgba(34,197,94,0.05) !important; }
    div[data-testid="stExpander"] details > summary > span[data-testid="stIconMaterial"], div[data-testid="stExpander"] details > summary > span.material-icons, div[data-testid="stExpander"] details > summary [data-testid="stIconMaterial"], div[data-testid="stExpander"] details > summary .material-icons, div[data-testid="stExpander"] details > summary [class*="material-symbols"], div[data-testid="stExpander"] details > summary [class*="Material"], div[data-testid="stExpander"] details > summary > svg + span, div[data-testid="stExpander"] details > summary > span[aria-hidden="true"] { display: none !important; visibility: hidden !important; width: 0 !important; height: 0 !important; font-size: 0 !important; overflow: hidden !important; position: absolute !important; left: -9999px !important; opacity: 0 !important; pointer-events: none !important; }
    div[data-testid="stExpander"] details > summary p, div[data-testid="stExpander"] details > summary div[data-testid="stMarkdownContainer"], div[data-testid="stExpander"] details > summary div[data-testid="stMarkdownContainer"] p { font-size: 0.82rem !important; font-weight: 700 !important; margin: 0 !important; line-height: 1.3 !important; color: #eaf1fb !important; white-space: normal !important; display: inline-block !important; }
    div[data-testid="stExpander"] details > summary > div { display: flex !important; align-items: center !important; gap: 6px !important; flex-wrap: nowrap !important; }
    div[data-testid="stExpander"] details > summary svg { flex-shrink: 0 !important; width: 14px !important; height: 14px !important; min-width: 14px !important; transition: transform 0.2s ease !important; }
    div[data-testid="stExpander"] details > div[role="region"] { padding: 0.4rem 0.8rem 0.8rem 0.8rem !important; font-size: 0.82rem !important; }
    div[data-testid="stAlert"] { padding: 0.4rem 0.7rem !important; font-size: 0.8rem !important; border-radius: 10px !important; }
    div[data-testid="stFileUploader"] section { background: var(--card) !important; border: 1.5px dashed var(--border) !important; border-radius: 12px !important; }
    .st-key-fa_nav div[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.3rem !important; }
    .st-key-fa_nav div[data-testid="stColumn"], .st-key-fa_nav div[data-testid="column"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
    .st-key-fa_nav .stButton button { padding: 0.3rem 0.25rem !important; height: 2.1rem !important; background: rgba(19,28,46,0.6) !important; backdrop-filter: blur(8px); border: 1px solid var(--border) !important; }
    .st-key-fa_nav .stButton button p { font-size: 0.72rem !important; white-space: nowrap; font-weight: 700 !important; }
    .st-key-fa_nav .stButton button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; box-shadow: 0 4px 16px rgba(34,197,94,0.4) !important; }
    .stApp .fa-hero { position: relative; overflow: hidden; background: linear-gradient(135deg, #14243e 0%, #0d1729 100%); border: 1px solid var(--border); border-radius: 16px; padding: 14px 12px; margin: 6px 0 10px 0; text-align: center; box-shadow: 0 10px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(34,197,94,0.05) inset; }
    .stApp .fa-hero::before { content: ""; position: absolute; inset: 0; background: radial-gradient(circle at 50% 0%, rgba(34,197,94,0.15), transparent 60%); pointer-events: none; }
    .stApp .fa-teams { display: flex; align-items: center; justify-content: space-between; gap: 6px; position: relative; z-index: 1; }
    .stApp .fa-team { flex: 1; font-weight: 800; font-size: 0.9rem; line-height: 1.2; word-break: break-word; letter-spacing: 0.2px; }
    .stApp .fa-score { font-size: 1.6rem; font-weight: 900; color: var(--green) !important; min-width: 80px; letter-spacing: 0.5px; text-shadow: 0 0 20px rgba(34,197,94,0.5); }
    .stApp .fa-vs { font-size: 0.9rem; font-weight: 800; color: var(--muted) !important; min-width: 50px; letter-spacing: 1px; }
    .stApp .fa-sub { font-size: 0.68rem; color: var(--muted) !important; margin-top: 6px; letter-spacing: 0.2px; }
    .stApp .fa-card { background: linear-gradient(145deg, var(--card), #0f1829); border: 1px solid var(--border); border-radius: 14px; padding: 10px 12px; margin-bottom: 10px; box-shadow: 0 6px 20px rgba(0,0,0,0.25); transition: all 0.25s ease; }
    .stApp .fa-card:hover { border-color: rgba(34,197,94,0.3); transform: translateY(-1px); }
    .stApp .fa-card.fa-pos { border-color: rgba(34,197,94,0.55); box-shadow: 0 8px 28px rgba(34,197,94,0.15), 0 0 0 1px rgba(34,197,94,0.15) inset; }
    .stApp .fa-ttl { font-size: 0.68rem; font-weight: 800; color: var(--muted) !important; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
    .stApp .fa-pickrow { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .stApp .fa-pick { font-size: 1rem; font-weight: 800; letter-spacing: 0.2px; }
    .stApp .fa-pct { font-size: 1.35rem; font-weight: 900; color: var(--green) !important; text-shadow: 0 0 16px rgba(34,197,94,0.4); }
    .stApp .fa-pct.fa-off { color: var(--muted) !important; text-shadow: none; }
    .stApp .fa-mut { font-size: 0.68rem; color: var(--muted) !important; margin-top: 6px; letter-spacing: 0.15px; }
    .stApp .fa-row { margin: 7px 0; }
    .stApp .fa-row-top { display: flex; justify-content: space-between; font-size: 0.76rem; margin-bottom: 3px; }
    .stApp .fa-lbl { color: #cbd5e1 !important; font-weight: 500; }
    .stApp .fa-val { font-weight: 800; }
    .stApp .fa-bar { position: relative; height: 8px; background: #1a2438; border-radius: 99px; overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.4); }
    .stApp .fa-fill { height: 100%; border-radius: 99px; transition: width 0.6s ease; }
    .stApp .fa-tick { position: absolute; top: 0; bottom: 0; width: 2px; background: #eaf1fb; opacity: 0.8; }
    .stApp .fa-badge { display: inline-block; padding: 3px 9px; border-radius: 99px; font-size: 0.65rem; font-weight: 800; white-space: nowrap; letter-spacing: 0.3px; text-transform: uppercase; }
    .stApp .fa-b-green { background: rgba(34,197,94,0.15); color: var(--green) !important; border: 1px solid rgba(34,197,94,0.5); }
    .stApp .fa-b-yellow { background: rgba(245,158,11,0.15); color: var(--yellow) !important; border: 1px solid rgba(245,158,11,0.5); }
    .stApp .fa-b-red { background: rgba(239,68,68,0.15); color: var(--red) !important; border: 1px solid rgba(239,68,68,0.5); }
    .stApp .fa-b-gray { background: rgba(148,163,184,0.12); color: #94a3b8 !important; border: 1px solid rgba(148,163,184,0.35); }
    .stApp .fa-mk { background: linear-gradient(145deg, var(--card), #0f1829); border: 1px solid var(--border); border-radius: 12px; padding: 8px 12px; margin: -4px 0 8px 0; box-shadow: 0 4px 16px rgba(0,0,0,0.2); }
    .stApp .fa-mk-row { display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px dashed #1d2940; gap: 6px; flex-wrap: wrap; }
    .stApp .fa-mk-row:last-child { border-bottom: none; }
    .stApp .fa-mk-lbl { font-size: 0.75rem; font-weight: 800; color: #cbd5e1 !important; min-width: 55px; }
    .stApp .fa-mk-pick { font-size: 0.86rem; font-weight: 800; }
    .stApp .fa-mk-pick.pass { color: var(--green) !important; }
    .stApp .fa-mk-pick.off { color: #94a3b8 !important; }
    .stApp .fa-mk-pct { font-size: 0.78rem; font-weight: 800; color: var(--text) !important; }
    .stApp .fa-mk-badge { font-size: 0.6rem; font-weight: 800; padding: 2px 7px; border-radius: 99px; margin-left: 4px; letter-spacing: 0.2px; }
    .stApp .fa-mk-badge.ok { background: rgba(34,197,94,0.15); color: var(--green) !important; border: 1px solid rgba(34,197,94,0.5); }
    .stApp .fa-mk-badge.no { background: rgba(148,163,184,0.12); color: #94a3b8 !important; border: 1px solid rgba(148,163,184,0.35); }
    .stApp .fa-locked { position: relative; overflow: hidden; background: linear-gradient(135deg, #14243e 0%, #0d1729 100%); border: 1px solid var(--border); border-radius: 16px; padding: 14px 12px; margin: 6px 0 10px 0; text-align: center; opacity: 0.7; }
    .stApp .fa-locked::after { content: "🔒"; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 3rem; opacity: 0.15; }
    .stApp .fa-locked-teams { display: flex; align-items: center; justify-content: space-between; gap: 6px; filter: blur(3px); }
    .stApp .fa-locked-overlay { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, rgba(34,197,94,0.08), rgba(59,130,246,0.08)); z-index: 2; }
    .stApp .fa-locked-text { background: linear-gradient(135deg, #16a34a, #22c55e); color: #04130a !important; font-weight: 900; font-size: 0.85rem; padding: 10px 20px; border-radius: 99px; box-shadow: 0 8px 24px rgba(34,197,94,0.4); letter-spacing: 0.5px; }
    .login-hero { text-align: center; padding: 40px 10px 24px 10px; position: relative; }
    .login-logo { font-size: 4.2rem; line-height: 1; margin-bottom: 14px; display: inline-block; filter: drop-shadow(0 0 30px rgba(34,197,94,0.6)); animation: logoPulse 3s ease-in-out infinite; }
    @keyframes logoPulse { 0%, 100% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 20px rgba(34,197,94,0.5)); } 50% { transform: scale(1.08) rotate(-3deg); filter: drop-shadow(0 0 40px rgba(34,197,94,0.9)); } }
    .login-title { font-size: 2rem !important; font-weight: 900 !important; background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0 !important; padding: 0 !important; letter-spacing: 1.2px; border: none !important; text-align: center !important; }
    .login-subtitle { font-size: 0.82rem; color: var(--muted) !important; margin-top: 8px; letter-spacing: 0.5px; font-weight: 500; }
    div[data-testid="stForm"] { background: linear-gradient(145deg, rgba(19,28,46,0.9), rgba(11,18,32,0.98)) !important; border: 1.5px solid rgba(34,197,94,0.2) !important; border-radius: 20px !important; padding: 22px 18px !important; box-shadow: 0 20px 60px rgba(0,0,0,0.55), 0 0 0 1px rgba(34,197,94,0.05) inset !important; backdrop-filter: blur(16px); }
    div[data-testid="stForm"] label p { font-size: 0.78rem !important; font-weight: 700 !important; color: #cbd5e1 !important; letter-spacing: 0.3px; margin-bottom: 5px !important; }
    div[data-testid="stForm"] input { height: 42px !important; font-size: 0.9rem !important; padding: 0 14px !important; background: rgba(11,18,32,0.9) !important; border: 1.5px solid var(--border) !important; border-radius: 10px !important; transition: all 0.2s ease; }
    div[data-testid="stForm"] input:focus { border-color: var(--green) !important; box-shadow: 0 0 0 4px rgba(34,197,94,0.15) !important; outline: none !important; }
    div[data-testid="stForm"] button { height: 42px !important; font-size: 0.9rem !important; font-weight: 800 !important; border-radius: 10px !important; letter-spacing: 0.3px; transition: all 0.2s ease; }
    div[data-testid="stForm"] button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; box-shadow: 0 8px 24px rgba(34,197,94,0.4) !important; border: none !important; }
    div[data-testid="stForm"] button[kind="primary"]:hover { box-shadow: 0 12px 32px rgba(34,197,94,0.55) !important; transform: translateY(-2px); }
    div[data-testid="stForm"] button[kind="secondary"] { background: rgba(30,41,59,0.6) !important; border: 1.5px solid var(--border) !important; }
    div[data-testid="stForm"] button[kind="secondary"]:hover { border-color: var(--blue) !important; background: rgba(59,130,246,0.1) !important; }
    .login-divider { display: flex; align-items: center; gap: 12px; margin: 12px 0 8px 0; color: #64748b !important; font-size: 0.68rem; font-weight: 800; letter-spacing: 4px; justify-content: center; }
    .login-divider::before, .login-divider::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, transparent, var(--border) 50%, transparent); }
    .login-footer { text-align: center; margin-top: 24px; font-size: 0.7rem; color: #64748b !important; letter-spacing: 0.5px; }
    .login-footer b { color: var(--green) !important; font-weight: 800; }
    .mh-hero { position: relative; overflow: hidden; text-align: center; padding: 28px 14px 22px 14px; background: linear-gradient(135deg, rgba(22,35,61,0.9), rgba(15,26,46,0.95)); border: 1.5px solid rgba(34,197,94,0.25); border-radius: 20px; margin: 6px 0 16px 0; box-shadow: 0 16px 48px rgba(0,0,0,0.45), 0 0 0 1px rgba(34,197,94,0.06) inset; }
    .mh-hero::before { content: ""; position: absolute; top: -60%; left: -60%; width: 220%; height: 220%; background: radial-gradient(circle at 50% 50%, rgba(34,197,94,0.18), transparent 55%); animation: mhGlow 6s ease-in-out infinite; pointer-events: none; }
    @keyframes mhGlow { 0%, 100% { opacity: 0.5; transform: scale(1) rotate(0deg); } 50% { opacity: 1; transform: scale(1.2) rotate(25deg); } }
    .mh-hero-icon { font-size: 3rem; line-height: 1; margin-bottom: 10px; display: inline-block; filter: drop-shadow(0 0 24px rgba(34,197,94,0.65)); animation: logoPulse 3s ease-in-out infinite; position: relative; z-index: 1; }
    .mh-hero-title { font-size: 1.7rem; font-weight: 900; background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: 1px; position: relative; z-index: 1; margin: 0; }
    .mh-hero-sub { font-size: 0.8rem; color: var(--muted); margin-top: 8px; letter-spacing: 0.4px; position: relative; z-index: 1; }
    .mh-hero-badge { display: inline-block; margin-top: 12px; padding: 4px 14px; background: rgba(34,197,94,0.12); border: 1px solid rgba(34,197,94,0.45); border-radius: 99px; font-size: 0.7rem; font-weight: 800; color: var(--green) !important; letter-spacing: 0.8px; position: relative; z-index: 1; }
    .mh-stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 0 0 16px 0; }
    .mh-stat { position: relative; background: linear-gradient(145deg, #16233d, #0f1a2e); border: 1px solid var(--border); border-radius: 16px; padding: 14px 10px 12px 10px; text-align: center; overflow: hidden; transition: all 0.25s ease; box-shadow: 0 6px 20px rgba(0,0,0,0.25); }
    .mh-stat::after { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #22c55e, #3b82f6); }
    .mh-stat-icon { font-size: 1.3rem; margin-bottom: 4px; }
    .mh-stat-num { font-size: 1.8rem; font-weight: 900; color: var(--green) !important; line-height: 1; letter-spacing: -0.8px; }
    .mh-stat-lbl { font-size: 0.65rem; color: var(--muted) !important; margin-top: 6px; letter-spacing: 0.7px; text-transform: uppercase; font-weight: 800; }
    .mh-info { background: linear-gradient(145deg, rgba(19,28,46,0.7), rgba(11,18,32,0.9)); border: 1px solid var(--border); border-radius: 14px; padding: 12px 14px; margin-top: 14px; font-size: 0.75rem; color: var(--muted) !important; line-height: 1.6; }
    .mh-info b { color: var(--green) !important; }
    ::-webkit-scrollbar { width: 7px; height: 7px; }
    ::-webkit-scrollbar-track { background: var(--bg-1); }
    ::-webkit-scrollbar-thumb { background: #2a3a56; border-radius: 99px; }
    section[data-testid="stSidebar"] { background: var(--bg-1) !important; border-right: 1px solid var(--border); }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
    .stApp .fa-card, .stApp .fa-hero, .stApp .fa-mk, .mh-stat, .stApp .fa-locked { animation: fadeInUp 0.4s ease-out; }
    .stApp div[data-testid="stCheckbox"] { background: linear-gradient(145deg, rgba(19,28,46,0.6), rgba(11,18,32,0.8)); border: 1.5px solid var(--border); border-radius: 12px; padding: 10px 12px; margin: 10px 0; }
    .stApp div[data-testid="stCheckbox"] label p { font-size: 0.78rem !important; line-height: 1.5 !important; }
    .stApp .fa-bildirim { background: linear-gradient(145deg, var(--card), #0f1829); border-left: 4px solid var(--green); border-radius: 12px; padding: 12px 14px; margin-bottom: 10px; }
    .stApp .fa-bildirim.fa-bildirim-iptal { border-left-color: #ef4444; }
    .stApp .fa-bildirim.fa-bildirim-sikayet { border-left-color: #f59e0b; }
    .stApp .fa-bildirim.fa-bildirim-gorus { border-left-color: #3b82f6; }
    .stApp .fa-bildirim.fa-bildirim-diger { border-left-color: #94a3b8; }
    .stApp .fa-bildirim-ttl { font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
    .stApp .fa-bildirim-msg { font-size: 0.85rem; color: #eaf1fb !important; line-height: 1.5; margin: 6px 0; }
    .stApp .fa-bildirim-meta { font-size: 0.68rem; color: var(--muted) !important; }
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
OTOMATIK_LOG_DOSYA = "otomatik_log.json"

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
def otomatik_log_yukle(): return _yukle_json(OTOMATIK_LOG_DOSYA, {})
def otomatik_log_kaydet(v): _kaydet_json(OTOMATIK_LOG_DOSYA, v)


def kullanici_ekle(kullanici_adi, sifre):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi in kullanicilar:
        return False, "Bu kullanıcı adı zaten alınmış."
    salt, s_hash = sifre_hashle(sifre)
    kullanicilar[kullanici_adi] = {
        "salt": salt, "sifre_hash": s_hash,
        "kayit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "abonelik_bitis": None, "son_odeme": None, "son_odeme_gun": 0,
        "yasal_kabul_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"),
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
    "iptal": {"ikon": "🚫", "isim": "Abonelik İptal Talebi", "sinif": "fa-bildirim-iptal"},
    "sikayet": {"ikon": "⚠️", "isim": "Şikayet", "sinif": "fa-bildirim-sikayet"},
    "gorus": {"ikon": "💬", "isim": "Görüş / Öneri", "sinif": "fa-bildirim-gorus"},
    "diger": {"ikon": "📩", "isim": "Diğer", "sinif": "fa-bildirim-diger"},
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


def gecmis_yukle(): return _yukle_json(GECMIS_DOSYA, [])
def gecmis_kaydet(v): _kaydet_json(GECMIS_DOSYA, v)
def gelecek_yukle(): return _yukle_json(GELECEK_DOSYA, [])
def gelecek_kaydet(v): _kaydet_json(GELECEK_DOSYA, v)


def ayarlar_yukle():
    v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "iban": "TR00 0000 0000 0000 0000 0000 00", "hesap_sahibi": "ADINIZ SOYADINIZ", "fiyat_haftalik": 49.0, "fiyat_aylik": 149.0, "fiyat_yillik": 999.0, "ucretsiz_kotasi": 3}
    try:
        if os.path.exists(AYARLAR_DOSYA):
            with open(AYARLAR_DOSYA, "r", encoding="utf-8") as f:
                y = json.load(f)
                if "1x2" in y and "esik_1" not in y:
                    e = float(y["1x2"]); y["esik_1"] = e; y["esik_x"] = e; y["esik_2"] = e
                v.update(y)
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
}.items()}

MAX_GOL = 8; BELIRSIZLIK = 0.20; MAX_MAC_SINIRI = 200
_kilit = threading.Lock(); _ESIK_CACHE = {}


if "sayfa" not in st.session_state: st.session_state.sayfa = "giris"
if "form_verileri" not in st.session_state: st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
if "gecmis_analizler" not in st.session_state: st.session_state.gecmis_analizler = gecmis_yukle()
if "gelecek_analizler" not in st.session_state: st.session_state.gelecek_analizler = gelecek_yukle()
if "kayit_yapildi" not in st.session_state: st.session_state.kayit_yapildi = False
if "gecmisten_gelindi" not in st.session_state: st.session_state.gecmisten_gelindi = False
if "gelecekten_gelindi" not in st.session_state: st.session_state.gelecekten_gelindi = False
if "silme_onay" not in st.session_state: st.session_state.silme_onay = False
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


ULKE_BAYRAK = {"switzerland": "🇨🇭", "isviçre": "🇨🇭", "i̇sviçre": "🇨🇭", "england": "🏴", "ingiltere": "🏴", "i̇ngiltere": "🏴", "spain": "🇪🇸", "ispanya": "🇪🇸", "italy": "🇮🇹", "italya": "🇮🇹", "germany": "🇩🇪", "almanya": "🇩🇪", "france": "🇫🇷", "fransa": "🇫🇷", "netherlands": "🇳🇱", "hollanda": "🇳🇱", "portugal": "🇵🇹", "portekiz": "🇵🇹", "belgium": "🇧🇪", "belçika": "🇧🇪", "turkey": "🇹🇷", "türkiye": "🇹🇷", "turkiye": "🇹🇷", "argentina": "🇦🇷", "arjantin": "🇦🇷", "brazil": "🇧🇷", "brezilya": "🇧🇷", "mexico": "🇲🇽", "meksika": "🇲🇽", "usa": "🇺🇸", "abd": "🇺🇸", "japan": "🇯🇵", "japonya": "🇯🇵", "south korea": "🇰🇷", "güney kore": "🇰🇷", "china": "🇨🇳", "çin": "🇨🇳", "russia": "🇷🇺", "rusya": "🇷🇺", "ukraine": "🇺🇦", "ukrayna": "🇺🇦", "poland": "🇵🇱", "polonya": "🇵🇱", "greece": "🇬🇷", "yunanistan": "🇬🇷", "scotland": "🏴", "wales": "🏴", "ireland": "🇮🇪", "austria": "🇦🇹", "avusturya": "🇦🇹", "croatia": "🇭🇷", "hırvatistan": "🇭🇷", "serbia": "🇷🇸", "sırbistan": "🇷🇸", "romania": "🇷🇴", "romanya": "🇷🇴", "bulgaria": "🇧🇬", "bulgaristan": "🇧🇬", "denmark": "🇩🇰", "danimarka": "🇩🇰", "sweden": "🇸🇪", "norway": "🇳🇴", "norveç": "🇳🇴", "finland": "🇫🇮", "finlandiya": "🇫🇮", "iceland": "🇮🇸", "hungary": "🇭🇺", "macaristan": "🇭🇺", "czech": "🇨🇿", "slovakia": "🇸🇰", "slovenia": "🇸🇮", "saudi": "🇸🇦", "suudi arabistan": "🇸🇦", "qatar": "🇶🇦", "katar": "🇶🇦", "egypt": "🇪🇬", "mısır": "🇪🇬", "morocco": "🇲🇦", "fas": "🇲🇦", "algeria": "🇩🇿", "cezayir": "🇩🇿", "tunisia": "🇹🇳", "tunus": "🇹🇳", "nigeria": "🇳🇬", "nijerya": "🇳🇬", "south africa": "🇿🇦", "australia": "🇦🇺", "avustralya": "🇦🇺", "new zealand": "🇳🇿", "india": "🇮🇳", "hindistan": "🇮🇳", "iran": "🇮🇷", "iraq": "🇮🇶", "irak": "🇮🇶", "israel": "🇮🇱", "colombia": "🇨🇴", "kolombiya": "🇨🇴", "chile": "🇨🇱", "şili": "🇨🇱", "peru": "🇵🇪", "uruguay": "🇺🇾", "ecuador": "🇪🇨", "paraguay": "🇵🇾", "bolivia": "🇧🇴", "venezuela": "🇻🇪", "canada": "🇨🇦", "kanada": "🇨🇦", "kosovo": "🇽🇰", "kosova": "🇽🇰", "albania": "🇦🇱", "arnavutluk": "🇦🇱", "georgia": "🇬🇪", "gürcistan": "🇬🇪", "armenia": "🇦🇲", "azerbaijan": "🇦🇿", "azerbaycan": "🇦🇿", "kazakhstan": "🇰🇿", "uzbekistan": "🇺🇿", "belarus": "🇧🇾", "latvia": "🇱🇻", "lithuania": "🇱🇹", "estonia": "🇪🇪", "luxembourg": "🇱🇺", "malta": "🇲🇹", "cyprus": "🇨🇾", "kıbrıs": "🇨🇾", "montenegro": "🇲🇪", "karadağ": "🇲🇪", "north macedonia": "🇲🇰", "bosnia": "🇧🇦", "bosna": "🇧🇦"}


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
def ort_iki(a, b):
    v = [x for x in [a, b] if x is not None and x > 0]
    return sum(v) / len(v) if v else 0


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


def oneri_istatistik_guncel(gecmis):
    ist = {"1x2": {"tam": 0, "yakin": 0, "yanlis": 0}, "gol": {"tam": 0, "yakin": 0, "yanlis": 0}, "kg": {"tam": 0, "yakin": 0, "yanlis": 0}}
    for g in gecmis:
        try:
            v = g["veri"]
            if not v.get("skor_belli", False): continue
            try: ya = yeniden_analiz(v)
            except Exception: ya = g.get("analiz", {})
            d = sonuc_hesapla({"veri": v, "analiz": ya})
            if not d: continue
            for key in ["oneri_1x2", "oneri_gol", "oneri_kg"]:
                kisa = key.replace("oneri_", ""); durum = d[key].get("durum")
                if durum == "tam": ist[kisa]["tam"] += 1
                elif durum == "yanlis": ist[kisa]["yanlis"] += 1
        except Exception: continue
    return ist


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
    # ==========================================
# METİN PARSER (Sportytrader)
# ==========================================
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


# ==========================================
# LİG GEÇMİŞİ ÇEKME
# ==========================================
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
# OTOMATİK ZAMANLAYICI
# ==========================================
_OTOMATIK_BASLATILDI = False


def _otomatik_worker():
    son_veri_tarih = None
    son_skor_saat = None
    while True:
        try:
            now = datetime.now()
            bugun = now.strftime("%Y-%m-%d")
            if now.hour == 2 and now.minute >= 30 and son_veri_tarih != bugun:
                try:
                    log = otomatik_log_yukle()
                    log["son_veri_cekimi"] = now.strftime("%Y-%m-%d %H:%M:%S")
                    log["son_veri_durum"] = "başlıyor"
                    otomatik_log_kaydet(log)
                    _otomatik_veri_cek()
                    log = otomatik_log_yukle()
                    log["son_veri_durum"] = "tamamlandı"
                    otomatik_log_kaydet(log)
                except Exception as e:
                    log = otomatik_log_yukle()
                    log["son_veri_durum"] = f"hata: {str(e)[:100]}"
                    otomatik_log_kaydet(log)
                son_veri_tarih = bugun
            if now.minute < 5 and son_skor_saat != f"{bugun}-{now.hour}":
                try:
                    log = otomatik_log_yukle()
                    log["son_skor_cekimi"] = now.strftime("%Y-%m-%d %H:%M:%S")
                    log["son_skor_durum"] = "başlıyor"
                    otomatik_log_kaydet(log)
                    _otomatik_skor_cek()
                    log = otomatik_log_yukle()
                    log["son_skor_durum"] = "tamamlandı"
                    otomatik_log_kaydet(log)
                except Exception as e:
                    log = otomatik_log_yukle()
                    log["son_skor_durum"] = f"hata: {str(e)[:100]}"
                    otomatik_log_kaydet(log)
                son_skor_saat = f"{bugun}-{now.hour}"
            time.sleep(60)
        except Exception:
            time.sleep(120)


def _otomatik_veri_cek():
    maclar, hatalar = mutating_ana_sayfa_linklerini_al(max_mac=MAX_MAC_SINIRI)
    if hatalar or not maclar: return
    mevcut_urls = set()
    for g in gelecek_yukle():
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut_urls.add(u)
    _ESIK_CACHE.clear()
    try:
        with open(AYARLAR_DOSYA, "r", encoding="utf-8") as f:
            _ESIK_CACHE.update(json.load(f))
    except Exception: pass
    eklenecek = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(_gelecek_mac_isle, m, mevcut_urls): m for m in maclar}
        for f in as_completed(futs):
            try:
                r = f.result()
                kayit = r[3] if len(r) == 4 else None
                if kayit is not None: eklenecek.append(kayit)
            except Exception: continue
    if eklenecek:
        mg = gelecek_yukle(); mg.extend(eklenecek); gelecek_kaydet(mg)


def _otomatik_skor_cek():
    gel = gelecek_yukle()
    isler = [g for g in gel if g.get("veri", {}).get("kaynak_url")]
    if not isler: return
    sonuc = {}
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(_skor_cek, g["veri"]["kaynak_url"], False): g for g in isler}
        for f in as_completed(futs):
            g = futs[f]
            try: sonuc[id(g)] = f.result()
            except Exception: sonuc[id(g)] = (None, None)
    gecmis = gecmis_yukle()
    mevcut = {x.get("veri", {}).get("kaynak_url") for x in gecmis}
    kalan = []
    for g in gel:
        r = sonuc.get(id(g))
        if r is None: kalan.append(g); continue
        skor, hata = r
        v = g["veri"]
        if skor is None: kalan.append(g); continue
        v["skor_ev"] = skor[0]; v["skor_dep"] = skor[1]; v["skor_belli"] = True
        d = sonuc_hesapla(g)
        if d: g["dogruluk"] = d
        if v.get("kaynak_url") not in mevcut:
            gecmis.append(g); mevcut.add(v.get("kaynak_url"))
    gecmis_kaydet(gecmis); gelecek_kaydet(kalan)


def _otomatik_baslat():
    global _OTOMATIK_BASLATILDI
    if _OTOMATIK_BASLATILDI: return
    _OTOMATIK_BASLATILDI = True
    t = threading.Thread(target=_otomatik_worker, daemon=True)
    t.start()


# ==========================================
# TASARIM YARDIMCILARI
# ==========================================
def _e(x): return _html.escape(str(x))
def rozet(m, t="gray"): return f'<span class="fa-badge fa-b-{t}">{_e(m)}</span>'


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


def yasal_metin_goster():
    with st.expander("📜 Kullanım Şartları ve Sorumluluk Reddi — OKU", expanded=False):
        st.markdown(YASAL_METIN)


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
            sec = [("🏠 Ana Sayfa", "giris"), ("📊 Geçmiş Maçlar", "gecmis"), ("🔬 Test", "backtest"), ("💳 Ödemeler", "admin_odemeler"), ("👥 Aboneler", "admin_aboneler"), ("📬 Bildirimler", "admin_bildirimler"), ("⚙️ Ayar", "ayarlar")]
        elif uye_mi():
            sec = [("🏠 Ana Sayfa", "giris"), ("📊 Geçmiş Maçlar", "gecmis"), ("📬 Bildirim", "kullanici_bildirim")]
        else:
            sec = [("🏠 Ana Sayfa", "giris"), ("📊 Geçmiş Maçlar", "gecmis"), ("✨ Üye Ol", "kayit"), ("🔑 Giriş", "giris_yap")]
        kl = st.columns(len(sec))
        for k, (e, h) in zip(kl, sec):
            with k:
                aktif = st.session_state.sayfa == h
                if st.button(e, key=f"nav_{h}", use_container_width=True, type="primary" if aktif else "secondary"):
                    if not aktif:
                        if h == "giris_yap":
                            st.session_state.sayfa = "giris_yap"
                            st.rerun()
                        else:
                            nav_git(h)


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
            with c1: w = st.number_input("Paralel", 1, 8, 3, 1, key="fw")
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
            with c2: lw = st.number_input("Paralel", 1, 8, 3, 1, key="lig_workers")
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
            with c1: sw = st.number_input("Paralel", 1, 8, 3, 1, key="skor_w")
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
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-icon">🌟</div><div class="mh-hero-title">Hoş Geldin, {_e(uye_adi())}</div><div class="mh-hero-sub">Premium aktif — tüm analizler açık</div>{kl}</div>', unsafe_allow_html=True)
        elif uye_mi():
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-icon">👤</div><div class="mh-hero-title">Hoş Geldin, {_e(uye_adi())}</div><div class="mh-hero-sub">İlk {kota} maç açık</div><div class="mh-hero-badge" style="background:rgba(245,158,11,0.12);border-color:rgba(245,158,11,0.5);color:#f59e0b !important;">⚠️ ABONELİK YOK</div></div>', unsafe_allow_html=True)
            if st.button("💳 Premium'a Geç", use_container_width=True, type="primary", key="ana_premium_btn"):
                st.session_state["odeme_hedef_kadi"] = uye_adi(); st.session_state.sayfa = "odeme"; st.rerun()
        else:
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-icon">⚽</div><div class="mh-hero-title">Futbol Analiz Pro</div><div class="mh-hero-sub">Bugünün {toplam} maçı — ilk {kota} maç açık</div><div class="mh-hero-badge">● CANLI VERİ</div></div>', unsafe_allow_html=True)
            cA, cB = st.columns(2)
            with cA:
                if st.button("💳 Premium'a Geç", use_container_width=True, type="primary", key="mis_prem"):
                    st.session_state.sayfa = "kayit"; st.rerun()
            with cB:
                if st.button("🔑 Giriş Yap", use_container_width=True, key="mis_gir"):
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
    st.markdown(f'''<div class="mh-hero"><div class="mh-hero-icon">💳</div><div class="mh-hero-title">Premium'a Geç</div><div class="mh-hero-sub">Havale / EFT ile ödeme</div><div class="mh-hero-badge">● GÜVENLİ ÖDEME</div></div>''', unsafe_allow_html=True)
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
    kl = kullanicilar_yukle()
    if not kl: st.info("ℹ️ Kayıtlı kullanıcı yok.")
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
            ca, cb, cc, cd, ce = st.columns([1, 1, 1, 1, 1])
            with ca:
                if st.button("+1H", use_container_width=True, key=f"ph_{k}"):
                    b_, y = abonelik_aktif_et(k, 7)
                    if b_: st.success(f"+1 hafta → {y}"); time.sleep(1.5); st.rerun()
            with cb:
                if st.button("+1A", use_container_width=True, key=f"p1_{k}"):
                    b_, y = abonelik_aktif_et(k, 30)
                    if b_: st.success(f"+1 ay → {y}"); time.sleep(1.5); st.rerun()
            with cc:
                if st.button("+1Y", use_container_width=True, key=f"py_{k}"):
                    b_, y = abonelik_aktif_et(k, 365)
                    if b_: st.success(f"+1 yıl → {y}"); time.sleep(1.5); st.rerun()
            with cd:
                if st.button("İptal", use_container_width=True, key=f"ip_{k}"):
                    abonelik_iptal_et(k); st.warning("İptal edildi."); time.sleep(1.5); st.rerun()
            with ce:
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
# SAYFA: GELECEK (ADMİN)
# ==========================================
elif st.session_state.sayfa == "gelecek_admin":
    if not admin_mi(): st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>🔮 Gelecek Maçlar (Admin)</h1>", unsafe_allow_html=True)
    gel = st.session_state.gelecek_analizler
    if not gel: st.info("Maç yok.")
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
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gg_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SAYFA: GEÇMİŞ
# ==========================================
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gc = st.session_state.gecmis_analizler; top = len(gc)
    if top == 0: st.info("Henüz kayıt yok.")
    else:
        st.markdown(f"### Toplam: {top} maç")
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
    with st.expander("📋 Okunan Veriler"):
        okunan_veriler_paneli(v)
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
