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

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet">
<style>
    html, body {
        overscroll-behavior: none !important;
        overscroll-behavior-y: none !important;
        touch-action: pan-y !important;
    }
    .stApp {
        overscroll-behavior: none !important;
    }
    html { font-size: 13px !important; }
    body, .stApp { font-size: 0.85rem !important; }
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    span[data-testid="stIconMaterial"],
    [data-testid="stIconMaterial"],
    [data-testid="stIconMaterial"] span,
    .stApp .material-symbols-rounded,
    .stApp .material-symbols-outlined,
    .stApp .material-icons,
    .stApp [class*="material-symbols"],
    .stApp [class*="material-icons"] {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
        font-weight: normal !important;
        font-style: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: 'liga' !important;
        font-feature-settings: 'liga' !important;
        -webkit-font-smoothing: antialiased !important;
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24 !important;
    }
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
    div[data-testid="stExpander"] details > summary p, div[data-testid="stExpander"] details > summary div[data-testid="stMarkdownContainer"], div[data-testid="stExpander"] details > summary div[data-testid="stMarkdownContainer"] p { font-size: 0.82rem !important; font-weight: 700 !important; margin: 0 !important; line-height: 1.3 !important; color: #eaf1fb !important; white-space: normal !important; display: inline-block !important; }
    div[data-testid="stExpander"] details > summary > div { display: flex !important; align-items: center !important; gap: 6px !important; flex-wrap: nowrap !important; }
    div[data-testid="stExpander"] details > summary svg { flex-shrink: 0 !important; width: 14px !important; height: 14px !important; min-width: 14px !important; transition: transform 0.2s ease !important; }
    div[data-testid="stExpander"] details > div[role="region"] { padding: 0.4rem 0.8rem 0.8rem 0.8rem !important; font-size: 0.82rem !important; }
    div[data-testid="stAlert"] { padding: 0.4rem 0.7rem !important; font-size: 0.8rem !important; border-radius: 10px !important; }
    div[data-testid="stFileUploader"] section { background: var(--card) !important; border: 1.5px dashed var(--border) !important; border-radius: 12px !important; }
    .st-key-fa_nav div[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.3rem !important; overflow: visible !important; }
    .st-key-fa_nav div[data-testid="stColumn"], .st-key-fa_nav div[data-testid="column"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; position: relative !important; overflow: visible !important; }
    .st-key-fa_nav .stButton button { padding: 0.3rem 0.25rem !important; height: 2.1rem !important; background: rgba(19,28,46,0.6) !important; backdrop-filter: blur(8px); border: 1px solid var(--border) !important; }
    .st-key-fa_nav .stButton button p { font-size: 0.72rem !important; white-space: nowrap; font-weight: 700 !important; }
    .st-key-fa_nav .stButton button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; box-shadow: 0 4px 16px rgba(34,197,94,0.4) !important; }
    .fa-nav-badge-wrap { position: relative; height: 0; margin: 0; padding: 0; overflow: visible; }
    .fa-nav-badge { position: absolute; top: -34px; right: -6px; background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff !important; font-size: 0.62rem !important; font-weight: 900 !important; padding: 2px 7px; border-radius: 99px; min-width: 20px; text-align: center; z-index: 99999; box-shadow: 0 2px 10px rgba(239,68,68,0.7); border: 1.5px solid rgba(255,255,255,0.35); line-height: 1.35; pointer-events: none; animation: badgePulse 1.8s ease-in-out infinite; }
    @keyframes badgePulse { 0%, 100% { transform: scale(1); box-shadow: 0 2px 10px rgba(239,68,68,0.7); } 50% { transform: scale(1.12); box-shadow: 0 2px 16px rgba(239,68,68,1); } }
    .stApp .fa-mini-line-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 12px 0 8px 0; }
    .stApp .fa-mini-line-kart { background: linear-gradient(145deg, rgba(19,28,46,0.92), rgba(11,18,32,0.98)); border: 1px solid #1d2940; border-radius: 12px; padding: 7px 6px 5px 6px; position: relative; overflow: hidden; box-shadow: 0 4px 14px rgba(0,0,0,0.3); animation: fadeInUp 0.4s ease-out; transition: all 0.25s ease; }
    .stApp .fa-mini-line-kart:hover { border-color: var(--c); transform: translateY(-2px); }
    .stApp .fa-mini-line-kart::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: var(--c); }
    .stApp .fa-mini-line-ust { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px; }
    .stApp .fa-mini-line-lbl { font-size: 0.55rem; font-weight: 900; color: #8fa0bd !important; letter-spacing: 0.3px; text-transform: uppercase; }
    .stApp .fa-mini-line-pct { font-size: 0.88rem; font-weight: 900; letter-spacing: -0.3px; line-height: 1; }
    .stApp .fa-mini-line-svg { margin: 2px -2px 0 -2px; }
    .stApp .fa-mini-line-svg svg { height: 52px !important; }
    .stApp .fa-mini-line-alt { display: flex; justify-content: space-between; align-items: center; font-size: 0.55rem; font-weight: 800; margin-top: 2px; padding: 0 1px; }
    .stApp .fa-mini-line-alt b { font-weight: 900; letter-spacing: 0.2px; }
    .stApp .fa-donut-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 16px 0 8px 0; }
    .stApp .fa-donut-kart { background: linear-gradient(145deg, rgba(19,28,46,0.85), rgba(11,18,32,0.95)); border: 1px solid #1d2940; border-radius: 16px; padding: 12px 6px 10px 6px; text-align: center; position: relative; overflow: hidden; transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.25); }
    .stApp .fa-donut-kart:hover { border-color: rgba(34,197,94,0.45); transform: translateY(-3px); box-shadow: 0 10px 28px rgba(34,197,94,0.15); }
    .stApp .fa-donut-kart::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--c); }
    .stApp .fa-donut-ttl { font-size: 0.62rem; color: #8fa0bd !important; font-weight: 800; letter-spacing: 0.6px; text-transform: uppercase; margin-bottom: 8px; }
    .stApp .fa-donut-svg { width: 100%; max-width: 82px; height: auto; margin: 0 auto; display: block; }
    .stApp .fa-donut-sub { font-size: 0.62rem; color: #64748b !important; margin-top: 8px; font-weight: 700; }
    .stApp .fa-donut-sub b { color: #eaf1fb !important; }
    .stApp .fa-bt-grid { display: grid; grid-template-columns: 1fr; gap: 10px; margin: 12px 0 8px 0; }
    .stApp .fa-bt-kart { background: linear-gradient(145deg, rgba(19,28,46,0.92), rgba(11,18,32,0.98)); border: 1px solid #1d2940; border-radius: 16px; padding: 14px 16px 12px 16px; position: relative; overflow: hidden; box-shadow: 0 6px 20px rgba(0,0,0,0.3); transition: all 0.3s ease; animation: fadeInUp 0.4s ease-out; }
    .stApp .fa-bt-kart:hover { border-color: var(--c); transform: translateY(-2px); }
    .stApp .fa-bt-kart::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--c); }
    .stApp .fa-bt-kart::after { content: ""; position: absolute; inset: 0; background: radial-gradient(circle at 100% 0%, var(--c) 0%, transparent 55%); opacity: 0.08; pointer-events: none; }
    .stApp .fa-bt-ust { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; position: relative; z-index: 1; }
    .stApp .fa-bt-lbl { font-size: 0.78rem; font-weight: 900; color: #eaf1fb !important; letter-spacing: 0.5px; }
    .stApp .fa-bt-lbl small { font-size: 0.62rem; color: #8fa0bd !important; font-weight: 700; letter-spacing: 0.3px; margin-left: 4px; }
    .stApp .fa-bt-pct { font-size: 1.6rem; font-weight: 900; color: var(--c) !important; letter-spacing: -1px; text-shadow: 0 0 20px var(--c); }
    .stApp .fa-bt-bar { position: relative; height: 12px; background: #0d1626; border-radius: 99px; overflow: hidden; box-shadow: inset 0 1px 4px rgba(0,0,0,0.6); margin-bottom: 8px; }
    .stApp .fa-bt-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, var(--c), var(--c-l)); transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1); position: relative; }
    .stApp .fa-bt-fill::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent); animation: shine 2.5s ease-in-out infinite; }
    @keyframes shine { 0% { transform: translateX(-100%); } 100% { transform: translateX(200%); } }
    .stApp .fa-bt-sub { display: flex; justify-content: space-between; font-size: 0.68rem; color: #8fa0bd !important; font-weight: 700; letter-spacing: 0.3px; position: relative; z-index: 1; }
    .stApp .fa-bt-sub .fa-bt-dog { color: #22c55e !important; font-weight: 900; }
    .stApp .fa-bt-sub .fa-bt-yan { color: #ef4444 !important; font-weight: 900; }
    .stApp .fa-bt-bos { background: linear-gradient(145deg, rgba(19,28,46,0.6), rgba(11,18,32,0.85)); border: 1.5px dashed var(--border); border-radius: 16px; padding: 28px 20px; text-align: center; margin: 12px 0; color: var(--muted) !important; font-size: 0.85rem; font-weight: 700; }
    .stApp .fa-bt-bos .fa-bt-bos-ikon { font-size: 2.2rem; margin-bottom: 8px; display: block; opacity: 0.6; }
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
    .st-key-fa_nav .stButton button { min-height: 2.9rem !important; padding: 0.55rem 0.4rem !important; }
    .st-key-fa_nav .stButton button p { font-size: 0.88rem !important; font-weight: 800 !important; }
    .stApp .mh-hero-ust { font-size: 0.7rem; color: #8fa0bd !important; letter-spacing: 2px; text-transform: uppercase; font-weight: 800; margin-bottom: 8px; opacity: 0.7; }
    .stApp .fa-uye-link { text-align: center; font-size: 0.78rem; color: #8fa0bd !important; margin-top: 8px; }
    .stApp .fa-uye-link b { color: #22c55e !important; font-weight: 800; }
    .stApp .fa-ai-kart { background: linear-gradient(145deg, rgba(19,28,46,0.92), rgba(11,18,32,0.98)); border: 1px solid rgba(59,130,246,0.35); border-radius: 16px; padding: 16px 16px 12px 16px; margin-bottom: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.35), 0 0 0 1px rgba(59,130,246,0.06) inset; animation: fadeInUp 0.4s ease-out; }
    .stApp .fa-ai-baslik { font-size: 0.78rem; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase; color: #3b82f6 !important; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid rgba(59,130,246,0.3); }
    .stApp .fa-ai-bolum { margin-bottom: 14px; }
    .stApp .fa-ai-bolum:last-child { margin-bottom: 4px; }
    .stApp .fa-ai-bolum-baslik { font-size: 0.72rem; font-weight: 900; letter-spacing: 0.8px; color: #8fa0bd !important; text-transform: uppercase; margin-bottom: 6px; }
    .stApp .fa-ai-bolum-metin { font-size: 0.86rem; line-height: 1.7; color: #eaf1fb !important; text-align: justify; letter-spacing: 0.1px; }
    .stApp .fa-ai-bolum-metin b { color: #22c55e !important; font-weight: 800; }
    .stApp .fa-ai-bolum-metin .ev { color: #3b82f6 !important; font-weight: 800; }
    .stApp .fa-ai-bolum-metin .dep { color: #f59e0b !important; font-weight: 800; }
    .stApp .fa-ai-bolum-metin .vurgu { color: #22c55e !important; font-weight: 800; }
    .stApp .fa-ai-bolum-metin .uyari { color: #f59e0b !important; font-weight: 800; }
    .stApp .fa-ai-bolum-metin .kotu { color: #ef4444 !important; font-weight: 800; }
    .stApp .fa-ai-karar { background: rgba(34,197,94,0.08); border-left: 3px solid #22c55e; border-radius: 8px; padding: 10px 12px; margin-top: 12px; font-size: 0.84rem; line-height: 1.55; color: #eaf1fb !important; }
    .stApp .fa-ai-karar b { color: #22c55e !important; font-weight: 900; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# POSTGRESQL VERİ KATMANI
# ==========================================
ADMIN_KULLANICI_ADI = "admin52"


def _admin_sifre_al():
    try:
        if "ADMIN_SIFRE" in st.secrets:
            return st.secrets["ADMIN_SIFRE"]
    except Exception:
        pass
    return os.environ.get("ADMIN_SIFRE", "Mg153759")

ADMIN_SIFRE = _admin_sifre_al()
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "adm_" + hashlib.sha256(ADMIN_SIFRE.encode()).hexdigest()[:40])


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


# ===== KALICI OTURUM (ÇEREZ) YÖNETİMİ =====
def _cookie_manager_al():
    try:
        return stx.CookieManager(key="fa_cookie_mgr_v1")
    except Exception:
        return None

_cookie_mgr = _cookie_manager_al()


def _token_uret():
    return _secrets.token_hex(32)


def _cerez_oku():
    if _cookie_mgr is None:
        return {}
    try:
        return _cookie_mgr.get_all() or {}
    except Exception:
        return {}


def _cerez_yaz(ad, deger):
    if _cookie_mgr is None:
        return
    try:
        _cookie_mgr.set(ad, deger, expires_at=datetime.now() + timedelta(days=30))
    except Exception:
        pass


def _cerez_sil(ad):
    if _cookie_mgr is None:
        return
    try:
        _cookie_mgr.delete(ad)
    except Exception:
        pass


def _otomatik_giris_dene():
    if st.session_state.get("aktif_kullanici") or st.session_state.get("rol") == "admin":
        return
    cerezler = _cerez_oku()
    if not cerezler:
        return
    token = cerezler.get("fa_token")
    kadi = cerezler.get("fa_kadi")
    if not token or not kadi:
        return
    if kadi == ADMIN_KULLANICI_ADI and token == ADMIN_TOKEN:
        st.session_state.rol = "admin"
        st.session_state._otomatik_giris_yapildi = True
        return
    try:
        kullanicilar = kullanicilar_yukle()
        k = kullanicilar.get(kadi)
        if k and k.get("oturum_token") == token:
            st.session_state.aktif_kullanici = kadi
            st.session_state._otomatik_giris_yapildi = True
    except Exception:
        pass


@st.cache_data(ttl=30, show_spinner=False)
def _online_durum_guncelle(session_id):
    online_heartbeat(session_id)
    return online_say()

if "_session_id" not in st.session_state:
    st.session_state._session_id = _secrets.token_hex(16)
try:
    _ONLINE_SAYI = _online_durum_guncelle(st.session_state._session_id)
except Exception:
    _ONLINE_SAYI = 0


# ===== ONLINE GÖSTERGESİ SADECE ADMİN İÇİN =====
if st.session_state.get("rol") == "admin":
    st.markdown(f'''<div style="text-align:center; margin:0 0 10px 0;">
    <span style="display:inline-block; background:rgba(34,197,94,0.15); border:1px solid rgba(34,197,94,0.5); border-radius:99px; padding:4px 14px; font-size:0.75rem; font-weight:800; color:#22c55e; letter-spacing:0.5px;">
    🟢 {_ONLINE_SAYI} KİŞİ ONLINE
    </span>
    </div>''', unsafe_allow_html=True)


def kullanicilar_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT kullanici_adi, veri FROM kullanicilar")
            return {row[0]: row[1] for row in cur.fetchall()}
    finally:
        conn.close()


def kullanicilar_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM kullanicilar")
            for k, veri in v.items():
                cur.execute("INSERT INTO kullanicilar (kullanici_adi, veri) VALUES (%s, %s)", (k, Json(veri)))
        conn.commit()
    finally:
        conn.close()


def bekleyen_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT kullanici_adi, veri FROM bekleyen_odemeler")
            return {row[0]: row[1] for row in cur.fetchall()}
    finally:
        conn.close()


def bekleyen_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM bekleyen_odemeler")
            for k, veri in v.items():
                cur.execute("INSERT INTO bekleyen_odemeler (kullanici_adi, veri) VALUES (%s, %s)", (k, Json(veri)))
        conn.commit()
    finally:
        conn.close()


def bildirimler_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, veri FROM bildirimler ORDER BY id")
            return [row[1] for row in cur.fetchall()]
    finally:
        conn.close()


def bildirimler_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM bildirimler")
            for veri in v:
                bid = veri.get("id") or int(time.time() * 1000)
                cur.execute("INSERT INTO bildirimler (id, veri) VALUES (%s, %s)", (bid, Json(veri)))
        conn.commit()
    finally:
        conn.close()


def gecmis_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT veri FROM gecmis ORDER BY id")
            return [row[0] for row in cur.fetchall()]
    finally:
        conn.close()


def gecmis_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM gecmis")
            for veri in v:
                cur.execute("INSERT INTO gecmis (veri) VALUES (%s)", (Json(veri),))
        conn.commit()
    finally:
        conn.close()


def gelecek_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT veri FROM gelecek ORDER BY id")
            return [row[0] for row in cur.fetchall()]
    finally:
        conn.close()


def gelecek_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM gelecek")
            for veri in v:
                cur.execute("INSERT INTO gelecek (veri) VALUES (%s)", (Json(veri),))
        conn.commit()
    finally:
        conn.close()


def ayarlar_yukle():
    v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "iban": "TR00 0000 0000 0000 0000 0000 00", "hesap_sahibi": "ADINIZ SOYADINIZ", "fiyat_haftalik": 49.0, "fiyat_aylik": 149.0, "fiyat_yillik": 999.0, "ucretsiz_kotasi": 3}
    try:
        conn = _db_baglanti()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT veri FROM ayarlar WHERE id = 1")
                row = cur.fetchone()
                if row and row[0]:
                    v.update(row[0])
        finally:
            conn.close()
    except Exception:
        pass
    return v


def ayarlar_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO ayarlar (id, veri) VALUES (1, %s) ON CONFLICT (id) DO UPDATE SET veri = EXCLUDED.veri", (Json(v),))
        conn.commit()
    finally:
        conn.close()


def online_heartbeat(session_id):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO online_kullanicilar (session_id, son_gorulme) VALUES (%s, NOW()) "
                "ON CONFLICT (session_id) DO UPDATE SET son_gorulme = NOW()",
                (session_id,)
            )
            cur.execute("DELETE FROM online_kullanicilar WHERE son_gorulme < NOW() - INTERVAL '2 minutes'")
        conn.commit()
    finally:
        conn.close()


def online_say():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM online_kullanicilar WHERE son_gorulme > NOW() - INTERVAL '2 minutes'")
            row = cur.fetchone()
            return row[0] if row else 0
    finally:
        conn.close()


def sifre_hashle(sifre, salt=None):
    if salt is None:
        salt = _secrets.token_hex(16)
    h = hashlib.sha256((salt + sifre).encode("utf-8")).hexdigest()
    return salt, h


def sifre_dogrula(sifre, salt, kayitli_hash):
    _, h = sifre_hashle(sifre, salt)
    return h == kayitli_hash


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
        "oturum_token": None,
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


def yeni_kayit_say(saat=24):
    try:
        kl = kullanicilar_yukle()
        simdi = datetime.now()
        count = 0
        for k, kd in kl.items():
            kt = kd.get("kayit_tarihi", "")
            try:
                kayit = datetime.strptime(kt, "%Y-%m-%d %H:%M")
                if (simdi - kayit).total_seconds() < saat * 3600:
                    count += 1
            except Exception:
                pass
        return count
    except Exception:
        return 0


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
    except Exception:
        pass

    try:
        for taraf_k, taraf in [("trends_ev", takim_ev), ("trends_dep", takim_dep)]:
            if not taraf:
                continue
            idx_t = metin.find(f"{taraf} Trends")
            if idx_t == -1:
                idx_t = metin.find(f"{taraf} trends")
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
                if temiz:
                    veri[taraf_k] = temiz[:5]
    except Exception:
        pass

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
        _sp.run([_sys.executable, "-m", "playwright", "install", "chromium"],
                check=False, timeout=600,
                stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
    except Exception:
        pass
    from playwright.sync_api import sync_playwright
    with _TARAYICI_SEM:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
            try:
                ctx = b.new_context(user_agent=UA, locale="en-US")
                pg = ctx.new_page()
                pg.route("**/*", lambda route: route.abort()
                         if route.request.resource_type in ("image", "media", "font", "stylesheet")
                         else route.continue_())
                pg.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
                pg.wait_for_timeout(2000)
                return pg.content()
            finally:
                try: b.close()
                except Exception: pass


def _scrapingbee_get(url, render_js=True, timeout=30, mac_sec="5", max_retry=3, dogrula=False):
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
    else:
        veri["skor_belli"] = False

    def _cift(label):
        for pat in [
            r'([\d.,]+)\s*%?\s*\t\s*' + re.escape(label) + r'\s*\t\s*([\d.,]+)',
            r'([\d.,]+)\s*%?\s*\|\s*' + re.escape(label) + r'\s*\|\s*([\d.,]+)',
            r'([\d.,]+)\s*%?\s+' + re.escape(label) + r'\s+([\d.,]+)\s*%?',
            r'([\d.,]+)\s*%?\s*\n\s*' + re.escape(label) + r'\s*\n\s*([\d.,]+)',
        ]:
            mm = re.search(pat, metin, re.IGNORECASE)
            if mm:
                try: return float(mm.group(1).replace(",", ".")), float(mm.group(2).replace(",", "."))
                except ValueError: continue
        return None, None

    for label, k_ev, k_dep in [
        ("Goals scored per game", "atilan_ev", "atilan_dep"),
        ("Goals conceded per game", "yenen_ev", "yenen_dep"),
        ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"),
        ("Team scored", "team_scored_ev", "team_scored_dep"),
        ("Both Teams to Score", "kg_siklik_ev", "kg_siklik_dep"),
        ("Over 2.5 goals", "ust25_ev", "ust25_dep"),
        ("Over 1.5 goals", "ust15_ev", "ust15_dep"),
        ("Over 3.5 goals", "ust35_ev", "ust35_dep"),
    ]:
        a, b = _cift(label)
        if a is not None and veri.get(k_ev, 0) == 0:
            veri[k_ev] = a; veri[k_dep] = b

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
    except Exception:
        return False


def _inline_skor_tasi_callback(idx):
    try:
        yse_val = int(st.session_state.get(f"ise_{idx}", 0))
        ysd_val = int(st.session_state.get(f"isd_{idx}", 0))
        gel_list = st.session_state.get("gelecek_analizler", [])
        if idx < 0 or idx >= len(gel_list):
            st.session_state["_inline_msg"] = ("error", "❌ Maç bulunamadı (indeks geçersiz)")
            return
        k = gel_list[idx]
        k["veri"]["skor_ev"] = yse_val
        k["veri"]["skor_dep"] = ysd_val
        k["veri"]["skor_belli"] = True
        yd = sonuc_hesapla(k)
        if yd: k["dogruluk"] = yd
        st.session_state.gecmis_analizler.append(k)
        st.session_state.gelecek_analizler.pop(idx)
        gecmis_kaydet(st.session_state.gecmis_analizler)
        gelecek_kaydet(st.session_state.gelecek_analizler)
        st.session_state["_inline_msg"] = (
            "success",
            f"✅ {k['veri'].get('takim_ev','?')} vs {k['veri'].get('takim_dep','?')} → {yse_val}-{ysd_val} Geçmişe taşındı!"
        )
    except Exception as e:
        st.session_state["_inline_msg"] = ("error", f"❌ Taşıma hatası: {e}")


def _gelecek_mac_isle(mac, mevcut_urls, esikler=None):
    try:
        veri, _ = mutating_mac_detay_cek(mac["url"])
        if not veri:
            return ("hata", mac, "Veri çekilemedi", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        if not veri.get("saat"): veri["saat"] = mac.get("saat", "")
        if veri.get("saat"): veri["saat"] = saat_2_saat_ileri(veri["saat"])
        veri["kaynak_url"] = mac["url"]
        if mac["url"] in mevcut_urls:
            return ("atlandi", veri, "Zaten var", None)
        if _mac_tahmin_var_mi(veri, esikler):
            kayit = kayit_olustur(veri, analiz_hesapla(veri))
            return ("eklendi", veri, "Gelecek'e eklendi", kayit)
        return ("atlandi", veri, "Tahmin yok (eşik altı)", None)
    except Exception as e:
        return ("hata", mac, str(e), None)


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

    basarili = []; hatali = []
    eklenecekler = []
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
                if sonuc == "eklendi":
                    eklenen += 1; basarili.append(veri)
                    if kayit is not None: eklenecekler.append(kayit)
                elif sonuc == "atlandi":
                    atlanan += 1; basarili.append(veri)
                else:
                    hatali.append(f"{mac.get('takim_ev','?')}: {mesaj}")
            except Exception as e:
                hatali.append(f"{mac.get('takim_ev','?')}: {e}")
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
        html, hata = _scrapingbee_get(mac["url"], render_js=True, mac_sec="5", dogrula=True)
        if hata or not html:
            return ("hata", mac, hata or "HTML yok", None)
        veri, _ = _mac_html_parse(html, mac["url"])
        if not veri.get("skor_belli", False):
            return ("atlandi", None, "Skor yok (bitmemiş maç)", None)
        if veri.get("atilan_ev", 0) == 0 or veri.get("yenen_ev", 0) == 0:
            return ("atlandi", None, "İstatistik eksik", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")

        yv = copy.deepcopy(VARSAYILAN_VERI); yv.update(veri)
        kayit = kayit_olustur(yv, analiz_hesapla(yv))
        kayit["dogruluk"] = sonuc_hesapla(kayit)
        return ("eklendi", veri, f"{veri['skor_ev']}-{veri['skor_dep']}", kayit)
    except Exception as e:
        return ("hata", mac, str(e), None)


def lig_gecmis_cek(lig_url, adet=10, max_workers=2, progress_callback=None):
    maclar, hatalar = _lig_son_mac_linklerini_al(lig_url, adet=adet)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Lig sayfasında maç linki bulunamadı."]

    mevcut_urls = set()
    for g in st.session_state.gecmis_analizler:
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut_urls.add(u)

    basarili = []; hatali = []
    eklenecekler = []
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
                elif sonuc == "atlandi":
                    atlanan += 1
                else:
                    hatali.append(f"{mac.get('takim_ev','?')}: {mesaj}")
            except Exception as e:
                hatali.append(f"{mac.get('takim_ev','?')}: {e}")
            if progress_callback:
                try: progress_callback(tamamlanan - 1, len(maclar), mac.get("takim_ev", ""))
                except Exception: pass

    if eklenecekler:
        st.session_state.gecmis_analizler.extend(eklenecekler)
        gecmis_kaydet(st.session_state.gecmis_analizler)

    st.session_state.gecmis_cek_ozet = {"eklenen": eklenen, "atlanan": atlanan}
    return basarili, hatali


def _skor_parse(html):
    """HTML içinde FT etiketinin ALTINDAKI skoru bul.
    Sadece 'FT' yazısının hemen altındaki skoru alır."""
    if not html:
        return None

    def _ok(e, d):
        return 0 <= e <= 10 and 0 <= d <= 10

    def _skor_bul_metin(metin):
        """Metin içinde skor kalıbı ara."""
        if not metin:
            return None
        m = re.search(r'(\d{1,2})\s*[-:\u2013\u2014]\s*(\d{1,2})(?!\d)', metin)
        if m:
            e, d = int(m.group(1)), int(m.group(2))
            if _ok(e, d):
                return e, d
        return None

    try:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        # Yöntem 1: Satır satır tara - "FT" bulunca hemen altındaki skoru al
        tum_metin = soup.get_text("\n", strip=True)
        satirlar = [s.strip() for s in tum_metin.split("\n") if s.strip()]

        for i, satir in enumerate(satirlar):
            # Tam "FT" satırı mı?
            if satir == "FT" or satir.upper() == "FT":
                # "Half Time-Full Time" kontrolü
                onceki = " ".join(satirlar[max(0, i-5):i]).lower()
                if "half time" in onceki or "win ht" in onceki or "draw ht" in onceki or "lose ht" in onceki:
                    continue

                # FT'den sonraki 3 satırda skor ara (kısa mesafe!)
                for j in range(i+1, min(i+4, len(satirlar))):
                    skor = _skor_bul_metin(satirlar[j])
                    if skor:
                        return skor

                # Aynı satırda skor ara
                skor = _skor_bul_metin(satir)
                if skor:
                    return skor

        # Yöntem 2: "FT" kelimesini içeren satırlarda skor ara
        for i, satir in enumerate(satirlar):
            if re.search(r'\bFT\b', satir, re.IGNORECASE):
                # İstatistik kontrolü
                if re.search(r'(Half Time|Win HT|Draw HT|Lose HT)', satir, re.IGNORECASE):
                    continue

                # Aynı satırda skor ara
                skor = _skor_bul_metin(satir)
                if skor:
                    return skor

                # Sonraki 2 satırda skor ara
                for j in range(i+1, min(i+3, len(satirlar))):
                    skor = _skor_bul_metin(satirlar[j])
                    if skor:
                        return skor

        # Yöntem 3: HTML elementlerinde "FT" ara
        for el in soup.find_all(True):
            try:
                t = el.get_text(strip=True)
            except Exception:
                continue

            if t == "FT" or t.upper() == "FT":
                # Parent elementte skor ara
                p = el.parent
                for _ in range(2):
                    if p is None:
                        break
                    try:
                        pt = p.get_text(" ", strip=True)
                        skor = _skor_bul_metin(pt)
                        if skor:
                            return skor
                    except Exception:
                        pass
                    p = p.parent

                # Kardeş elementlerde skor ara
                try:
                    for nxt in el.next_elements:
                        if isinstance(nxt, str):
                            t = str(nxt).strip()
                            m = re.match(r'^(\d{1,2})\s*[-:\u2013\u2014]\s*(\d{1,2})$', t)
                            if m:
                                e, d = int(m.group(1)), int(m.group(2))
                                if _ok(e, d):
                                    return e, d
                except Exception:
                    pass

    except Exception:
        pass

    return None



def _skor_cek(url, tarayici_yedek=False):
    if not url:
        return None, "URL yok"
    html = None; hata = None
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=15)
        if r.status_code == 200 and r.text:
            html = r.text
        else:
            hata = f"HTTP {r.status_code}"
    except Exception as e:
        hata = f"Bağlantı: {str(e)[:80]}"
    skor = _skor_parse(html) if html else None
    if skor:
        return skor, None
    if tarayici_yedek:
        try:
            h2 = _playwright_skor_cek(url, timeout=25)
            if h2:
                skor = _skor_parse(h2)
                if skor:
                    return skor, None
        except Exception as e:
            hata = f"Tarayıcı: {str(e)[:60]}"
    if html:
        return None, None
    return None, hata or "Sayfa alınamadı"


def sonuclari_isle(tarayici_yedek=False, max_workers=4, progress_callback=None):
    gel = st.session_state.gelecek_analizler
    isler = [(i, g) for i, g in enumerate(gel) if g.get("veri", {}).get("kaynak_url")]
    sonuc = {}
    tamam = 0
    if isler:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            fut = {ex.submit(_skor_cek, g["veri"]["kaynak_url"], tarayici_yedek): (i, g) for i, g in isler}
            for f in as_completed(fut):
                i, g = fut[f]; tamam += 1
                try:
                    sonuc[i] = f.result()
                except Exception as e:
                    sonuc[i] = (None, str(e)[:80])
                if progress_callback:
                    try:
                        progress_callback(tamam - 1, len(isler), g["veri"].get("takim_ev", ""))
                    except Exception:
                        pass

    mevcut = {x.get("veri", {}).get("kaynak_url") for x in st.session_state.gecmis_analizler}
    tasinan = 0; bitmemis = 0; hatalar = []; kalan = []
    for i, g in enumerate(gel):
        r = sonuc.get(i)
        if r is None:
            kalan.append(g); continue
        skor, hata = r
        v = g["veri"]; isim = f"{v.get('takim_ev', '?')} - {v.get('takim_dep', '?')}"
        if skor is None:
            if hata:
                hatalar.append(f"{isim}: {hata}")
            else:
                bitmemis += 1
            kalan.append(g); continue
        v["skor_ev"], v["skor_dep"], v["skor_belli"] = skor[0], skor[1], True
        d = sonuc_hesapla(g)
        if d: g["dogruluk"] = d
        if v.get("kaynak_url") not in mevcut:
            st.session_state.gecmis_analizler.append(g)
            mevcut.add(v.get("kaynak_url"))
        tasinan += 1

    st.session_state.gelecek_analizler = kalan
    st.session_state.aktif_gelecek_idx = None
    st.session_state.gelecekten_gelindi = False
    gecmis_kaydet(st.session_state.gecmis_analizler)
    gelecek_kaydet(st.session_state.gelecek_analizler)
    return {"tasinan": tasinan, "bitmemis": bitmemis, "hatalar": hatalar, "toplam": len(isler)}


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


def _sparkline_svg(degerler, renk, yukseklik=62, genislik=300):
    if not degerler or len(degerler) < 2:
        return f'<svg class="fa-spark-svg" viewBox="0 0 {genislik} {yukseklik}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;display:block;"><text x="50%" y="50%" text-anchor="middle" fill="#64748b" font-size="10">Yetersiz veri</text></svg>'
    n = len(degerler)
    pad_top = 8
    pad_bot = 6
    h = yukseklik - pad_top - pad_bot
    step_x = genislik / (n - 1) if n > 1 else genislik

    noktalar = []
    for i, v in enumerate(degerler):
        v = max(0.0, min(100.0, v))
        x = i * step_x
        y = pad_top + (1 - v / 100) * h
        noktalar.append((x, y))

    path_d = f"M {noktalar[0][0]:.2f} {noktalar[0][1]:.2f}"
    for i in range(1, n):
        x0, y0 = noktalar[i - 1]
        x1, y1 = noktalar[i]
        cx = (x0 + x1) / 2
        path_d += f" C {cx:.2f} {y0:.2f}, {cx:.2f} {y1:.2f}, {x1:.2f} {y1:.2f}"

    alan_d = path_d + f" L {genislik} {yukseklik} L 0 {yukseklik} Z"
    son_x, son_y = noktalar[-1]
    grad_id = f"grad_{renk.replace('#','').replace(':','').replace('.','')}"

    return f'''<svg viewBox="0 0 {genislik} {yukseklik}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;display:block;">
<defs><linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="{renk}" stop-opacity="0.45"/>
<stop offset="100%" stop-color="{renk}" stop-opacity="0"/>
</linearGradient></defs>
<path d="{alan_d}" fill="url(#{grad_id})"/>
<path d="{path_d}" fill="none" stroke="{renk}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="{son_x:.2f}" cy="{son_y:.2f}" r="3.2" fill="{renk}" stroke="#0b1220" stroke-width="1.6"/>
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


def _modern_seri_hesapla(gc, son_n=30):
    seri_1x2, seri_gol, seri_kg = [], [], []
    t_1x2 = d_1x2 = 0
    t_gol = d_gol = 0
    t_kg = d_kg = 0
    for g in gc:
        try:
            vv = g.get("veri", {})
            if not vv.get("skor_belli", False): continue
            dd = sonuc_hesapla(g)
            if not dd: continue
            o = dd["oneri_1x2"]
            if o.get("tuttu") is not None:
                t_1x2 += 1
                if o["tuttu"]: d_1x2 += 1
                if t_1x2 > 0: seri_1x2.append(d_1x2 / t_1x2 * 100)
            o = dd["oneri_gol"]
            if o.get("tuttu") is not None:
                t_gol += 1
                if o["tuttu"]: d_gol += 1
                if t_gol > 0: seri_gol.append(d_gol / t_gol * 100)
            o = dd["oneri_kg"]
            if o.get("tuttu") is not None:
                t_kg += 1
                if o["tuttu"]: d_kg += 1
                if t_kg > 0: seri_kg.append(d_kg / t_kg * 100)
        except Exception:
            continue
    if len(seri_1x2) > son_n: seri_1x2 = seri_1x2[-son_n:]
    if len(seri_gol) > son_n: seri_gol = seri_gol[-son_n:]
    if len(seri_kg) > son_n: seri_kg = seri_kg[-son_n:]
    return seri_1x2, seri_gol, seri_kg, (d_1x2, t_1x2), (d_gol, t_gol), (d_kg, t_kg)


def _trend_ok(seri):
    if len(seri) < 2: return ''
    son = seri[-1]; onceki = seri[-2]
    if son > onceki + 0.5: return '<span class="fa-trend" style="color:#22c55e;">▲</span>'
    if son < onceki - 0.5: return '<span class="fa-trend" style="color:#ef4444;">▼</span>'
    return '<span class="fa-trend" style="color:#94a3b8;">●</span>'


def modern_istatistik_grafik(baslik="📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ", stil="donut"):
    if stil == "line":
        gc = st.session_state.gecmis_analizler
        seri_1x2, seri_gol, seri_kg, ist_1x2, ist_gol, ist_kg = _modern_seri_hesapla(gc, son_n=20)
        p1 = seri_1x2[-1] if seri_1x2 else 0
        pg = seri_gol[-1] if seri_gol else 0
        pk = seri_kg[-1] if seri_kg else 0

        st.markdown(f'<div class="mh-hero-ust" style="text-align:center;margin-top:14px;">{_e(baslik)}</div>', unsafe_allow_html=True)

        kartlar_html = []
        for ikon, etiket, seri, yuz, ist, renk in [
            ("🎯", "1X2", seri_1x2, p1, ist_1x2, "#22c55e"),
            ("⚽", "GOL", seri_gol, pg, ist_gol, "#3b82f6"),
            ("🤝", "KG", seri_kg, pk, ist_kg, "#f59e0b"),
        ]:
            if not seri:
                continue
            dog, top = ist
            yan = top - dog
            spark = _sparkline_svg(seri, renk, yukseklik=52, genislik=140)
            trend = _trend_ok(seri)
            kartlar_html.append(
                f'<div class="fa-mini-line-kart" style="--c:{renk};">'
                f'<div class="fa-mini-line-ust">'
                f'<span class="fa-mini-line-lbl">{ikon} {etiket}</span>'
                f'<span class="fa-mini-line-pct" style="color:{renk} !important; text-shadow:0 0 12px {renk};">%{yuz:.0f}</span>'
                f'</div>'
                f'<div class="fa-mini-line-svg">{spark}</div>'
                f'<div class="fa-mini-line-alt">'
                f'<span><b style="color:#22c55e !important;">{dog}✓</b> <b style="color:#ef4444 !important;">{yan}✗</b></span>'
                f'<span style="color:#8fa0bd !important;">{trend}</span>'
                f'</div>'
                f'</div>'
            )

        st.markdown(f'<div class="fa-mini-line-grid">{"".join(kartlar_html)}</div>', unsafe_allow_html=True)
    else:
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
                _cerez_yaz("fa_token", ADMIN_TOKEN)
                _cerez_yaz("fa_kadi", ADMIN_KULLANICI_ADI)
                st.session_state.rol = "admin"; st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"; st.rerun()
            elif kullanici_dogrula(kadi.strip(), sifre):
                try:
                    _u_token = _token_uret()
                    _kk = kullanicilar_yukle()
                    if kadi.strip() in _kk:
                        _kk[kadi.strip()]["oturum_token"] = _u_token
                        kullanicilar_kaydet(_kk)
                    _cerez_yaz("fa_token", _u_token)
                    _cerez_yaz("fa_kadi", kadi.strip())
                except Exception:
                    pass
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
                _cerez_sil("fa_token"); _cerez_sil("fa_kadi")
                st.session_state.rol = "misafir"; st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"
                st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI); st.rerun()
        elif uye_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="uye_cikis_btn"):
                try:
                    _kk = kullanicilar_yukle()
                    if uye_adi() in _kk:
                        _kk[uye_adi()]["oturum_token"] = None
                        kullanicilar_kaydet(_kk)
                except Exception:
                    pass
                _cerez_sil("fa_token"); _cerez_sil("fa_kadi")
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


def nav_git(h):
    st.session_state.sayfa = h
    st.session_state.kayit_yapildi = False
    st.session_state.tek_silme_onay = None
    st.session_state.tek_silme_gelecek = None
    st.session_state.sil_onay_kadi = None
    st.session_state.silme_onay = False
    st.session_state.silme_onay_gelecek = False
    if h == "backtest": st.session_state.bt_sonuc = None; st.session_state.bt_detaylar = []
    st.rerun()


def nav_bar():
    if st.session_state.sayfa in ("kayit", "uyegirisi", "odeme", "giris_yap"): return
    try: kutu = st.container(key="fa_nav")
    except TypeError: kutu = st.container()
    with kutu:
        badge_map = {}
        if admin_mi():
            try:
                odeme_say = len(bekleyen_yukle())
            except Exception:
                odeme_say = 0
            try:
                bd_list = bildirimler_yukle()
                bildirim_say = sum(1 for b in bd_list if b.get("durum") == "okunmadi")
            except Exception:
                bildirim_say = 0
            try:
                abone_say = yeni_kayit_say(24)
            except Exception:
                abone_say = 0

            badge_map = {
                "admin_odemeler": odeme_say,
                "admin_bildirimler": bildirim_say,
                "admin_aboneler": abone_say,
            }

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
                cnt = int(badge_map.get(h, 0) or 0)
                if cnt > 0:
                    goster = str(cnt) if cnt < 100 else "99+"
                    st.markdown(
                        f'<div class="fa-nav-badge-wrap">'
                        f'<div class="fa-nav-badge">{goster}</div>'
                        f'</div>',
                        unsafe_allow_html=True
        )
        
# ===== OTOMATİK GİRİŞ DENEMESİ =====
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
        vs1, vs2, vs3 = st.tabs(["🔄 Gelecek Maçlar", "📜 Lig Geçmişi", "🏁 Sonuçları İşle"])
        with vs1:
            if st.session_state.toplu_cek_ozet:
                oz = st.session_state.toplu_cek_ozet
                st.markdown(f"**Son çekim:** Eklenen: **{oz.get('eklenen', 0)}** | Atlanan: **{oz.get('atlanan', 0)}** | Toplam: **{oz.get('toplam', 0)}**")
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
                    else:
                        st.success(f"✅ {len(bas)} maç işlendi.")
                        time.sleep(2); st.rerun()
        with vs2:
            lurl = st.text_input("Lig URL", key="lig_url_input", placeholder="https://www.mutating.com/football-stats/league-...")
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
                    if hat:
                        with st.expander(f"⚠️ {len(hat)} hata"):
                            for h in hat: st.caption(h)
                    if bas:
                        st.success(f"✅ {len(bas)} maç eklendi!"); time.sleep(2); st.rerun()
                    else: st.error("Hiçbir maç eklenemedi.")
        with vs3:
            st.markdown(f"Bekleyen: **{len(st.session_state.gelecek_analizler)}** maç")
            st.info("ℹ️ Bu sekme, gelecek maçların skorlarını kontrol edip bitenleri geçmişe taşır.")

            c1, c2 = st.columns(2)
            with c1:
                sw = st.number_input("Paralel", 1, 4, 2, 1, key="skor_w")
            with c2:
                st.markdown("")
                if st.button("🏁 Biten Maçları Geçmişe Aktar", use_container_width=True, type="primary", key="skor_btn"):
                    if not st.session_state.gelecek_analizler:
                        st.warning("Gelecek'te maç yok")
                    else:
                        ph = st.empty()
                        pb = st.progress(0, text="Başlatılıyor...")
                        def _p3(i, t, n):
                            try: pb.progress(min(i / t, 1.0), text=f"{i}/{t}: {n}")
                            except Exception: pass
                        with st.spinner(f"{len(st.session_state.gelecek_analizler)} maç kontrol ediliyor..."):
                            oz = sonuclari_isle(False, int(sw), _p3)
                        st.session_state.skor_ozet = oz
                        pb.progress(1.0, text="Tamamlandı!")
                        time.sleep(0.5)
                        pb.empty()
                        ph.empty()
                        st.rerun()

            # Son skor çekme sonucu
            if st.session_state.get("skor_ozet"):
                oz = st.session_state.skor_ozet
                hata_say = len(oz.get("hatalar", []))
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                with c1: st.metric("✅ Taşınan", oz.get("tasinan", 0))
                with c2: st.metric("⏳ Bitmemiş", oz.get("bitmemis", 0))
                with c3: st.metric("❌ Hata", hata_say)
                if oz.get("hatalar"):
                    with st.expander(f"⚠️ {hata_say} hata detayı"):
                        for _h in oz["hatalar"][:50]:
                            st.caption(_h)
                if st.button("🗑️ Sonucu Temizle", key="skor_ozet_temizle"):
                    st.session_state.skor_ozet = None
                    st.rerun()

            st.divider()
            st.markdown("### 📋 Gelecek Maçlar")
            gel = st.session_state.gelecek_analizler
            if not gel:
                st.info("Henüz gelecek maç yok.")
            else:
                for i, g in enumerate(gel):
                    v = g["veri"]
                    te = v.get("takim_ev", "Ev")
                    td = v.get("takim_dep", "Dep")
                    saat = v.get("saat", "")
                    ulke = v.get("ulke", "")
                    tarih = v.get("tarih", "")
                    st.markdown(mac_karti(te, td, False, 0, 0, 0, 0, saat, ulke, tarih), unsafe_allow_html=True)
                    if st.button("🔍 Detay", use_container_width=True, key=f"det_{i}"):
                        st.session_state.form_verileri = copy.deepcopy(v)
                        st.session_state.kayit_yapildi = True
                        st.session_state.aktif_gelecek_idx = i
                        st.session_state.sayfa = "sonuc"
                        st.rerun()
                    st.divider()


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
            modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ", stil="line")
        elif uye_mi():
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-title" style="font-size:1.25rem;">Hoş Geldin, {_e(uye_adi())}</div><div class="mh-hero-sub">İlk {kota} maç ücretsiz açık</div><div class="mh-hero-badge" style="background:rgba(245,158,11,0.12);border-color:rgba(245,158,11,0.5);color:#f59e0b !important;">⚠️ ABONELİK YOK</div></div>', unsafe_allow_html=True)
            modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ", stil="line")
            if st.button("💳 Premium'a Geç  •  ✨ Üye Ol", use_container_width=True, type="primary", key="ana_premium_btn"):
                st.session_state["odeme_hedef_kadi"] = uye_adi(); st.session_state.sayfa = "odeme"; st.rerun()
        else:
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-title" style="font-size:1.25rem;">Bugün {toplam} Maç</div><div class="mh-hero-sub">İlk {kota} maç ücretsiz açık</div></div>', unsafe_allow_html=True)
            modern_istatistik_grafik("📊 GEÇMİŞ MAÇ İSTATİSTİKLERİ", stil="line")
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
                    try:
                        _u_token = _token_uret()
                        _kk = kullanicilar_yukle()
                        if yk.strip() in _kk:
                            _kk[yk.strip()]["oturum_token"] = _u_token
                            kullanicilar_kaydet(_kk)
                        _cerez_yaz("fa_token", _u_token)
                        _cerez_yaz("fa_kadi", yk.strip())
                    except Exception:
                        pass
                    st.session_state["aktif_kullanici"] = yk.strip()
                    st.session_state["odeme_hedef_kadi"] = yk.strip()
                    st.success(f"✅ {m} Ödeme sayfasına yönlendiriliyorsun...")
                    time.sleep(1.5); st.session_state.sayfa = "odeme"; st.rerun()
                else: st.error(f"❌ {m}")
        if gb: st.session_state.sayfa = "giris"; st.rerun()
    yasal_metin_goster()


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
                try:
                    _u_token = _token_uret()
                    _kk = kullanicilar_yukle()
                    if k.strip() in _kk:
                        _kk[k.strip()]["oturum_token"] = _u_token
                        kullanicilar_kaydet(_kk)
                    _cerez_yaz("fa_token", _u_token)
                    _cerez_yaz("fa_kadi", k.strip())
                except Exception:
                    pass
                st.session_state["aktif_kullanici"] = k.strip()
                st.success(f"✅ Hoş geldin, {k.strip()}!")
                time.sleep(1); st.session_state.sayfa = "giris"; st.rerun()
            else: st.error("❌ Hatalı giriş.")
        if gg: st.session_state.sayfa = "giris"; st.rerun()


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

            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                st.number_input("Ev", 0, 20, 0, 1, key=f"ise_{idx}")
            with c2:
                st.number_input("Dep", 0, 20, 0, 1, key=f"isd_{idx}")
            with c3:
                st.markdown(""); st.markdown("")
                st.button(
                    "📥 Skor Gir & Geçmişe Taşı",
                    key=f"inline_skor_btn_{idx}",
                    on_click=_inline_skor_tasi_callback,
                    args=(idx,),
                    use_container_width=True,
                    type="primary"
                )

            c1, c2 = st.columns([5, 1])
            with c1:
                if st.button("🔍 Detay", use_container_width=True, key=f"gmac_{idx}"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True; st.session_state.gelecekten_gelindi = True
                    st.session_state.aktif_gelecek_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
            with c2:
                if st.button("🗑️ Sil", use_container_width=True, key=f"gsil_{idx}"):
                    if st.session_state.get("tek_silme_gelecek") == idx:
                        st.session_state.tek_silme_gelecek = None
                    else:
                        st.session_state.tek_silme_gelecek = idx
                    st.rerun()

            if st.session_state.get("tek_silme_gelecek") == idx:
                st.warning(f"⚠️ **{te} vs {td}** silinsin mi? Bu işlem geri alınamaz.")
                oc1, oc2 = st.columns(2)
                with oc1:
                    if st.button("✅ Evet, Sil", key=f"ge_{idx}", use_container_width=True, type="primary"):
                        try:
                            st.session_state.gelecek_analizler.pop(idx)
                            gelecek_kaydet(st.session_state.gelecek_analizler)
                            st.session_state.tek_silme_gelecek = None
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Silme hatası: {e}")
                with oc2:
                    if st.button("❌ Vazgeç", key=f"gi_{idx}", use_container_width=True):
                        st.session_state.tek_silme_gelecek = None
                        st.rerun()
            st.divider()

        if "_inline_msg" in st.session_state:
            _msg_type, _msg_text = st.session_state.pop("_inline_msg")
            if _msg_type == "success":
                st.success(_msg_text)
                time.sleep(1)
                st.rerun()
            else:
                st.error(_msg_text)

    st.divider()
    st.markdown(f"""<div style="background:linear-gradient(135deg,rgba(239,68,68,0.15),rgba(239,68,68,0.05));
        border:1.5px solid rgba(239,68,68,0.5);border-radius:14px;padding:14px;margin-top:10px;">
        <div style="font-size:0.95rem;font-weight:900;color:#ef4444;letter-spacing:0.5px;margin-bottom:4px;">
        🚨 TEHLİKELİ BÖLGE — TOPLU SİLME</div>
        <div style="font-size:0.78rem;color:#fca5a5;font-weight:600;">
        Bu butona bastığınızda <b>TÜM GELECEK MAÇLAR ({len(gel)} maç)</b> kalıcı olarak silinir. Bu işlem geri alınamaz!</div>
        </div>""", unsafe_allow_html=True)

    if st.button(f"🗑️ TÜM GELECEĞİ SİL ({len(gel)} MAÇ)", use_container_width=True,
                 key="temizle_gel", type="primary"):
        if st.session_state.get("silme_onay_gelecek"):
            st.session_state.silme_onay_gelecek = False
        else:
            st.session_state.silme_onay_gelecek = True
        st.rerun()

    if st.session_state.get("silme_onay_gelecek"):
        st.error(f"⚠️ **SON ONAY:** Tüm gelecek silinecek (**{len(gel)} maç**). Emin misin?")
        oc1, oc2 = st.columns(2)
        with oc1:
            if st.button("✅ EVET, TÜMÜNÜ SİL", key="sil_gel_evet", use_container_width=True, type="primary"):
                try:
                    st.session_state.gelecek_analizler = []
                    gelecek_kaydet([])
                    st.session_state.silme_onay_gelecek = False
                    st.session_state.tek_silme_gelecek = None
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Silme hatası: {e}")
        with oc2:
            if st.button("❌ Vazgeç", key="sil_gel_iptal", use_container_width=True):
                st.session_state.silme_onay_gelecek = False
                st.rerun()

    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gg_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


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
                    if st.button("🗑️ Sil", use_container_width=True, key=f"sil_{idx}"):
                        if st.session_state.get("tek_silme_onay") == idx:
                            st.session_state.tek_silme_onay = None
                        else:
                            st.session_state.tek_silme_onay = idx
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
                            except Exception as e:
                                st.error(f"❌ Silme hatası: {e}")
                    with oc2:
                        if st.button("❌ Vazgeç", key=f"hh_{idx}", use_container_width=True):
                            st.session_state.tek_silme_onay = None
                            st.rerun()
            else:
                if st.button("🔍 Detay", use_container_width=True, key=f"mac_{idx}"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True; st.session_state.gecmisten_gelindi = True
                    st.session_state.aktif_kayit_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
            st.divider()

    if admin_mi():
        st.divider()
        st.markdown("""<div style="background:linear-gradient(135deg,rgba(239,68,68,0.15),rgba(239,68,68,0.05));
            border:1.5px solid rgba(239,68,68,0.5);border-radius:14px;padding:14px;margin-top:10px;">
            <div style="font-size:0.95rem;font-weight:900;color:#ef4444;letter-spacing:0.5px;margin-bottom:4px;">
            🚨 TEHLİKELİ BÖLGE — TOPLU SİLME</div>
            <div style="font-size:0.78rem;color:#fca5a5;font-weight:600;">
            Bu butona bastığınızda <b>TÜM GEÇMİŞ MAÇLAR (""" + str(top) + """ maç)</b> kalıcı olarak silinir. Bu işlem geri alınamaz!</div>
            </div>""", unsafe_allow_html=True)

        if st.button(f"🗑️ TÜM GEÇMİŞİ SİL ({top} MAÇ)", use_container_width=True,
                     key="temizle_g", type="primary"):
            if st.session_state.get("silme_onay"):
                st.session_state.silme_onay = False
            else:
                st.session_state.silme_onay = True
            st.rerun()

        if st.session_state.get("silme_onay"):
            st.error(f"⚠️ **SON ONAY:** Tüm geçmiş silinecek (**{top} maç**). Emin misin?")
            oc1, oc2 = st.columns(2)
            with oc1:
                if st.button("✅ EVET, TÜMÜNÜ SİL", key="sil_g_evet", use_container_width=True, type="primary"):
                    try:
                        st.session_state.gecmis_analizler = []
                        gecmis_kaydet([])
                        st.session_state.silme_onay = False
                        st.session_state.tek_silme_onay = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Silme hatası: {e}")
            with oc2:
                if st.button("❌ Vazgeç", key="sil_g_iptal", use_container_width=True):
                    st.session_state.silme_onay = False
                    st.rerun()

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
                if not any(sec.values()):
                    st.warning("⚠️ En az bir market seç.")
                else:
                    s, d = backtest_hesapla(st.session_state.gecmis_analizler, sec, esk)
                    st.session_state.bt_sonuc = s
                    st.session_state.bt_detaylar = d
                    st.session_state.bt_sec = sec

    if st.session_state.bt_sonuc and st.session_state.get("bt_sec"):
        sec = st.session_state.bt_sec
        sonuc = st.session_state.bt_sonuc
        gecmis_len = len(st.session_state.gecmis_analizler)

        st.markdown(f'''<div style="text-align:center;margin:10px 0 6px 0;">
<span style="display:inline-block; background:rgba(59,130,246,0.12); border:1px solid rgba(59,130,246,0.5); border-radius:99px; padding:4px 14px; font-size:0.72rem; font-weight:800; color:#3b82f6; letter-spacing:0.5px;">
🔎 {gecmis_len} MAÇ ÜZERİNDE TEST EDİLDİ
</span>
</div>''', unsafe_allow_html=True)

        def _bt_kart(baslik, ikon, d, renk, acik_renk):
            dog = d["dogru"]; yan = d["yanlis"]; tt = dog + yan
            yuzde = (dog / tt * 100) if tt > 0 else 0
            if tt == 0:
                return f'''<div class="fa-bt-kart" style="--c:{renk};--c-l:{acik_renk};">
<div class="fa-bt-ust"><span class="fa-bt-lbl">{ikon} {baslik}</span><span class="fa-bt-pct">%—</span></div>
<div class="fa-bt-bar"><div class="fa-bt-fill" style="width:0%"></div></div>
<div class="fa-bt-sub"><span>Hiç sinyal yok</span><span>0 maç</span></div>
</div>'''
            return f'''<div class="fa-bt-kart" style="--c:{renk};--c-l:{acik_renk};">
<div class="fa-bt-ust"><span class="fa-bt-lbl">{ikon} {baslik}<small>{tt} sinyal</small></span><span class="fa-bt-pct">%{yuzde:.1f}</span></div>
<div class="fa-bt-bar"><div class="fa-bt-fill" style="width:{yuzde:.1f}%"></div></div>
<div class="fa-bt-sub"><span><span class="fa-bt-dog">✓ {dog} doğru</span> &nbsp; <span class="fa-bt-yan">✗ {yan} yanlış</span></span><span>Başarı %{yuzde:.1f}</span></div>
</div>'''

        kartlar = []
        if sec.get("1x2"):
            kartlar.append(_bt_kart("1X2", "⚽", sonuc["1x2"], "#22c55e", "#4ade80"))
        if sec.get("kg_var"):
            kartlar.append(_bt_kart("KG Var", "🤝", sonuc["kg_var"], "#3b82f6", "#60a5fa"))
        if sec.get("kg_yok"):
            kartlar.append(_bt_kart("KG Yok", "🚫", sonuc["kg_yok"], "#8b5cf6", "#a78bfa"))
        if sec.get("ust"):
            kartlar.append(_bt_kart("Üst 2.5", "⬆️", sonuc["ust"], "#f59e0b", "#fbbf24"))
        if sec.get("alt"):
            kartlar.append(_bt_kart("Alt 2.5", "⬇️", sonuc["alt"], "#ef4444", "#f87171"))

        if not kartlar:
            st.markdown('<div class="fa-bt-bos"><span class="fa-bt-bos-ikon">📭</span>Hiç market seçilmedi.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="fa-bt-grid">{"".join(kartlar)}</div>', unsafe_allow_html=True)

        tum_dog = sum(sonuc[k]["dogru"] for k in sonuc)
        tum_yan = sum(sonuc[k]["yanlis"] for k in sonuc)
        tum_tt = tum_dog + tum_yan
        if tum_tt > 0:
            genel = tum_dog / tum_tt * 100
            sv = "yuksek" if genel >= 65 else "orta" if genel >= 55 else "dusuk"
            renk = "#22c55e" if sv == "yuksek" else "#f59e0b" if sv == "orta" else "#ef4444"
            st.markdown(f'''<div class="fa-bt-kart" style="--c:{renk};--c-l:{renk};margin-top:14px;">
<div class="fa-bt-ust"><span class="fa-bt-lbl">📊 GENEL TOPLAM<small>{tum_tt} sinyal</small></span><span class="fa-bt-pct">%{genel:.1f}</span></div>
<div class="fa-bt-bar"><div class="fa-bt-fill" style="width:{genel:.1f}%"></div></div>
<div class="fa-bt-sub"><span><span class="fa-bt-dog">✓ {tum_dog} doğru</span> &nbsp; <span class="fa-bt-yan">✗ {tum_yan} yanlış</span></span><span>Tüm marketler</span></div>
</div>''', unsafe_allow_html=True)
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
    v = st.session_state.form_verileri; a = analiz_hesapla(v)
    te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
    sb = v.get("skor_belli", False); se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    st.markdown(mac_karti(te, td, sb, se, sd, a["lam_ev"], a["lam_dep"], v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)

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

    km = (a["ust_25"] >= esik_al("ust") and a["ust_25"] >= a["alt_25"]) or (a["alt_25"] >= esik_al("alt") and a["alt_25"] >= a["ust_25"]) or p1
    if not st.session_state.kayit_yapildi and admin_mi():
        yk = kayit_olustur(v, a)
        if sb: st.session_state.gecmis_analizler.append(yk); gecmis_kaydet(st.session_state.gecmis_analizler)
        elif km: st.session_state.gelecek_analizler.append(yk); gelecek_kaydet(st.session_state.gelecek_analizler)
        st.session_state.kayit_yapildi = True
    if st.button("🔄 Yeni", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI); st.session_state.sayfa = "giris"; st.rerun()            
