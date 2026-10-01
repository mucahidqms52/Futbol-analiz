import streamlit as st
import math
import copy
import re
import random
import json
import os
import html as _html
import time

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

# ==========================================
# DOSYALAR (GitHub Actions botunun yazdığı)
# ==========================================
GECMIS_DOSYA = "data/gecmis.json"
GELECEK_DOSYA = "data/gelecek.json"
AYARLAR_DOSYA = "ayarlar.json"
ADMIN_SIFRE = "Mg153759"


def _yukle(dosya):
    try:
        if os.path.exists(dosya):
            with open(dosya, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _kaydet(dosya, veri):
    try:
        os.makedirs(os.path.dirname(dosya) or ".", exist_ok=True)
        with open(dosya, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def gecmis_yukle(): return _yukle(GECMIS_DOSYA)
def gecmis_kaydet(v): _kaydet(GECMIS_DOSYA, v)
def gelecek_yukle(): return _yukle(GELECEK_DOSYA)
def gelecek_kaydet(v): _kaydet(GELECEK_DOSYA, v)


def ayarlar_yukle():
    v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0}
    try:
        if os.path.exists(AYARLAR_DOSYA):
            with open(AYARLAR_DOSYA, "r", encoding="utf-8") as f:
                v.update(json.load(f))
    except Exception:
        pass
    return v


def ayarlar_kaydet(esikler):
    try:
        with open(AYARLAR_DOSYA, "w", encoding="utf-8") as f:
            json.dump(esikler, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ==========================================
# SABİTLER
# ==========================================
ESIK_YUKSEK = 65.0
ESIK_ORTA = 55.0
ESIK_BELIRSIZ = 50.0
MONTE_CARLO_N = 10000
MAX_GOL = 8
BELIRSIZLIK = 0.20


VARSAYILAN_VERI = {
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
    "btts_over25_ev": 0.0, "btts_over25_dep": 0.0,
    "tg_0_ev": 0.0, "tg_0_dep": 0.0, "tg_1_ev": 0.0, "tg_1_dep": 0.0,
    "tg_2_ev": 0.0, "tg_2_dep": 0.0, "tg_3_ev": 0.0, "tg_3_dep": 0.0,
    "tg_4_ev": 0.0, "tg_4_dep": 0.0, "tg_01_ev": 0.0, "tg_01_dep": 0.0,
    "tg_23_ev": 0.0, "tg_23_dep": 0.0, "tg_4p_ev": 0.0, "tg_4p_dep": 0.0,
    "ht_ust05_ev": 0.0, "ht_ust05_dep": 0.0, "ht_ust15_ev": 0.0, "ht_ust15_dep": 0.0,
    "ht_ust25_ev": 0.0, "ht_ust25_dep": 0.0,
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
}


# ==========================================
# SESSION STATE
# ==========================================
if "sayfa" not in st.session_state: st.session_state.sayfa = "giris"
if "form_verileri" not in st.session_state: st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
if "gecmis_analizler" not in st.session_state: st.session_state.gecmis_analizler = gecmis_yukle()
if "gelecek_analizler" not in st.session_state: st.session_state.gelecek_analizler = gelecek_yukle()
if "kayit_yapildi" not in st.session_state: st.session_state.kayit_yapildi = False
if "gelecekten_gelindi" not in st.session_state: st.session_state.gelecekten_gelindi = False
if "aktif_gelecek_idx" not in st.session_state: st.session_state.aktif_gelecek_idx = None
if "tek_silme_onay" not in st.session_state: st.session_state.tek_silme_onay = None
if "tek_silme_gelecek" not in st.session_state: st.session_state.tek_silme_gelecek = None
if "silme_onay" not in st.session_state: st.session_state.silme_onay = False
if "silme_onay_gelecek" not in st.session_state: st.session_state.silme_onay_gelecek = False
if "giris_yapildi" not in st.session_state: st.session_state.giris_yapildi = False
if "rol" not in st.session_state: st.session_state.rol = None
if "esikler" not in st.session_state: st.session_state.esikler = ayarlar_yukle()


def admin_mi(): return st.session_state.get("rol") == "admin"
def esik_al(key): return st.session_state.esikler.get(key, 50.0)
def esik_1x2_al(secim):
    km = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}
    return st.session_state.esikler.get(km.get(secim, ""), 55.0)


# ==========================================
# ÜLKE BAYRAK
# ==========================================
ULKE_BAYRAK = {
    "switzerland": "🇨🇭", "isviçre": "🇨🇭", "england": "🏴", "ingiltere": "🏴",
    "spain": "🇪🇸", "ispanya": "🇪🇸", "italy": "🇮🇹", "italya": "🇮🇹",
    "germany": "🇩🇪", "almanya": "🇩🇪", "france": "🇫🇷", "fransa": "🇫🇷",
    "netherlands": "🇳🇱", "hollanda": "🇳🇱", "portugal": "🇵🇹", "portekiz": "🇵🇹",
    "belgium": "🇧🇪", "belçika": "🇧🇪", "turkey": "🇹🇷", "türkiye": "🇹🇷",
    "argentina": "🇦🇷", "arjantin": "🇦🇷", "brazil": "🇧🇷", "brezilya": "🇧🇷",
    "mexico": "🇲🇽", "meksika": "🇲🇽", "usa": "🇺🇸", "abd": "🇺🇸",
    "japan": "🇯🇵", "japonya": "🇯🇵", "south korea": "🇰🇷", "güney kore": "🇰🇷",
    "china": "🇨🇳", "çin": "🇨🇳", "russia": "🇷🇺", "rusya": "🇷🇺",
    "ukraine": "🇺🇦", "ukrayna": "🇺🇦", "poland": "🇵🇱", "polonya": "🇵🇱",
    "greece": "🇬🇷", "yunanistan": "🇬🇷", "scotland": "🏴", "i̇skoçya": "🏴",
    "wales": "🏴", "galler": "🏴", "ireland": "🇮🇪", "i̇rlanda": "🇮🇪",
    "austria": "🇦🇹", "avusturya": "🇦🇹", "croatia": "🇭🇷", "hırvatistan": "🇭🇷",
    "serbia": "🇷🇸", "sırbistan": "🇷🇸", "romania": "🇷🇴", "romanya": "🇷🇴",
    "bulgaria": "🇧🇬", "bulgaristan": "🇧🇬", "denmark": "🇩🇰", "danimarka": "🇩🇰",
    "sweden": "🇸🇪", "i̇sveç": "🇸🇪", "norway": "🇳🇴", "norveç": "🇳🇴",
    "finland": "🇫🇮", "finlandiya": "🇫🇮", "iceland": "🇮🇸", "i̇zlanda": "🇮🇸",
    "hungary": "🇭🇺", "macaristan": "🇭🇺", "czech": "🇨🇿", "çekya": "🇨🇿",
    "slovakia": "🇸🇰", "slovakya": "🇸🇰", "slovenia": "🇸🇮", "slovenya": "🇸🇮",
    "saudi": "🇸🇦", "suudi arabistan": "🇸🇦", "qatar": "🇶🇦", "katar": "🇶🇦",
    "egypt": "🇪🇬", "mısır": "🇪🇬", "morocco": "🇲🇦", "fas": "🇲🇦",
    "algeria": "🇩🇿", "cezayir": "🇩🇿", "tunisia": "🇹🇳", "tunus": "🇹🇳",
    "nigeria": "🇳🇬", "nijerya": "🇳🇬", "south africa": "🇿🇦", "güney afrika": "🇿🇦",
    "australia": "🇦🇺", "avustralya": "🇦🇺", "new zealand": "🇳🇿", "yeni zelanda": "🇳🇿",
    "india": "🇮🇳", "hindistan": "🇮🇳", "iran": "🇮🇷", "iraq": "🇮🇶", "irak": "🇮🇶",
    "israel": "🇮🇱", "i̇srail": "🇮🇱", "colombia": "🇨🇴", "kolombiya": "🇨🇴",
    "chile": "🇨🇱", "şili": "🇨🇱", "peru": "🇵🇪", "uruguay": "🇺🇾",
    "ecuador": "🇪🇨", "ekvador": "🇪🇨", "paraguay": "🇵🇾", "bolivia": "🇧🇴",
    "venezuela": "🇻🇪", "costa rica": "🇨🇷", "panama": "🇵🇦", "jamaica": "🇯🇲",
    "canada": "🇨🇦", "kanada": "🇨🇦", "kosovo": "🇽🇰", "kosova": "🇽🇰",
    "albania": "🇦🇱", "arnavutluk": "🇦🇱", "moldova": "🇲🇩",
    "georgia": "🇬🇪", "gürcistan": "🇬🇪", "armenia": "🇦🇲", "ermenistan": "🇦🇲",
    "azerbaijan": "🇦🇿", "azerbaycan": "🇦🇿", "kazakhstan": "🇰🇿", "kazakistan": "🇰🇿",
    "uzbekistan": "🇺🇿", "özbekistan": "🇺🇿", "belarus": "🇧🇾",
    "latvia": "🇱🇻", "letonya": "🇱🇻", "lithuania": "🇱🇹", "litvanya": "🇱🇹",
    "estonia": "🇪🇪", "estonya": "🇪🇪", "luxembourg": "🇱🇺", "lüksemburg": "🇱🇺",
    "malta": "🇲🇹", "cyprus": "🇨🇾", "kıbrıs": "🇨🇾",
    "montenegro": "🇲🇪", "karadağ": "🇲🇪", "north macedonia": "🇲🇰", "kuzey makedonya": "🇲🇰",
    "bosnia": "🇧🇦", "bosna": "🇧🇦", "liechtenstein": "🇱🇮",
}


def ulke_bayrak_bul(ulke_adi):
    if not ulke_adi: return "🌍"
    u = ulke_adi.lower().strip()
    for a in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if a in u: return ULKE_BAYRAK[a]
    return "🌍"


def _ulke_bul(metin):
    m = re.search(r'Standings\s+([^\n]+)', metin)
    if not m: return ""
    satir = m.group(1).strip()
    if not satir: return ""
    alt = satir.lower()
    for a in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if a in alt: return a
    parcalar = satir.split()
    return " ".join(parcalar[:2]) if len(parcalar) >= 2 else (parcalar[0] if parcalar else "")


def clamp(x, lo, hi): return max(lo, min(hi, x))


def guven_seviyesi_bul(o):
    if o >= ESIK_YUKSEK: return ("yuksek", "🟢", "success", "Yüksek")
    if o >= ESIK_ORTA: return ("orta", "🟡", "warning", "Orta")
    if o >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "error", "Belirsiz")
    return ("cok_dusuk", "⚫", "error", "Düşük")


# ==========================================
# POISSON & MODEL
# ==========================================
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
    at_e = v.get("atilan_ev", 0.0); ye = v.get("yenen_ev", 0.0)
    at_d = v.get("atilan_dep", 0.0); yd = v.get("yenen_dep", 0.0)
    xg_e = v.get("xg_ev", 0.0); xg_d = v.get("xg_dep", 0.0)
    h_ev = (xg_e * 0.60 + at_e * 0.40) if xg_e > 0 else (at_e if at_e > 0 else 1.2)
    h_dep = (xg_d * 0.60 + at_d * 0.40) if xg_d > 0 else (at_d if at_d > 0 else 1.0)
    ts_e = v.get("team_scored_ev", 0); ts_d = v.get("team_scored_dep", 0)
    if ts_e > 0: h_ev *= clamp(ts_e / 60, 0.7, 1.3)
    if ts_d > 0: h_dep *= clamp(ts_d / 60, 0.7, 1.3)
    sd = yd if yd > 0 else 1.2
    se = ye if ye > 0 else 1.0
    cs_e = v.get("clean_sheets_ev", 0.0); cs_d = v.get("clean_sheets_dep", 0.0)
    def cf(cs):
        if cs <= 0: return 1.0
        if cs < 40.0: return 1.0 - (cs / 250.0)
        return max(0.40, 0.84 - (cs - 40.0) * (0.44 / 60.0))
    df = cf(cs_e); ef = cf(cs_d)
    le_h = h_ev * 0.60 + sd * 0.40
    ld_h = h_dep * 0.60 + se * 0.40
    u25e = v.get("ust25_ev", 0); u25d = v.get("ust25_dep", 0)
    if u25e > 0: le_h *= clamp(u25e / 50, 0.85, 1.15)
    if u25d > 0: ld_h *= clamp(u25d / 50, 0.85, 1.15)
    kg_e = v.get("kg_siklik_ev", 0); kg_d = v.get("kg_siklik_dep", 0)
    if kg_e > 0 and kg_d > 0:
        kg_ort = (kg_e + kg_d) / 2
        if kg_ort >= 60: le_h *= 1.05; ld_h *= 1.05
        elif kg_ort <= 35: le_h *= 0.95; ld_h *= 0.95
    fe = clamp(1 + (v.get("ppg_ev", 1.5) - 1.5) / 15, 0.85, 1.15)
    fd = clamp(1 + (v.get("mpg_dep", 1.5) - 1.5) / 15, 0.85, 1.15)
    se_s = v.get("siralama_ev", 10); sd_s = v.get("siralama_dep", 10)
    dom = 1.0
    if 1 <= se_s <= 5 and sd_s >= 10: dom = 1.20
    ge = v.get("galibiyet_ev", 0); gd = v.get("galibiyet_dep", 0)
    if ge > 0 and gd > 0:
        if ge - gd >= 25: le_h *= 1.08; ld_h *= 0.95
        elif gd - ge >= 25: le_h *= 0.95; ld_h *= 1.08
    le = le_h * 1.05 * fe * ef * dom
    ld = ld_h * 0.95 * fd * df
    if le > 2.50: le = 2.50 + (le - 2.50) * 0.5
    if ld > 2.50: ld = 2.50 + (ld - 2.50) * 0.5
    return clamp(le, 0.05, 4.5), clamp(ld, 0.05, 4.5), 0.80


def matristen_olasilik(matris, mg=MAX_GOL):
    p1 = px = p2 = 0.0
    u05 = u15 = u25 = u35 = 0.0
    kg = 0.0; sk = {}; tot = 0.0
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


def mac_ici_sok(le, ld, rng=None):
    r = rng if rng is not None else random
    if r.random() < 0.03:
        if r.random() < 0.5: le *= 0.70
        else: ld *= 0.70
    return le, ld


def monte_carlo(le_b, ld_b, n=MONTE_CARLO_N):
    seed = int(round(le_b * 1_000_000)) * 1_000_003 + int(round(ld_b * 1_000_000))
    rng = random.Random(seed)
    s = {"1": 0, "X": 0, "2": 0, "u25": 0, "kg": 0}
    for _ in range(n):
        le = le_b * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        ld = ld_b * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
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
    mc = monte_carlo(le, ld, MONTE_CARLO_N)
    lu = v.get("lig_ust25", 0.0); lk = v.get("lig_kg", 0.0)
    p1 = p1p * 0.60 + mc["p1"] * 0.40
    px = pxp * 0.60 + mc["px"] * 0.40
    p2 = p2p * 0.60 + mc["p2"] * 0.40
    ge = v.get("galibiyet_ev", 0); gd = v.get("galibiyet_dep", 0)
    if ge > 0 and gd > 0:
        p1 = p1 * 0.85 + ge * 0.15; p2 = p2 * 0.85 + gd * 0.15
    be = v.get("beraberlik_ev", 0); bd = v.get("beraberlik_dep", 0)
    if be > 0 and bd > 0:
        px = px * 0.85 + ((be + bd) / 2) * 0.15
    t = p1 + px + p2
    if t > 0: p1, px, p2 = (p1 / t) * 100, (px / t) * 100, (p2 / t) * 100
    u25 = u25p * 0.60 + lu * 0.10 + mc["ust25"] * 0.30 if lu > 0 else u25p * 0.65 + mc["ust25"] * 0.35
    kgm = kgp * 0.40 + lk * 0.30 + mc["kg_var"] * 0.30 if lk > 0 else kgp * 0.60 + mc["kg_var"] * 0.40
    kge = v.get("kg_siklik_ev", 0); kgd = v.get("kg_siklik_dep", 0)
    if kge > 0 and kgd > 0:
        kgm = kgm * 0.85 + ((kge + kgd) / 2) * 0.15
    tbg = le + ld
    if tbg < 1.80:
        bf = (1.80 - tbg) / 1.80
        u25 = max(10.0, u25 * (1.0 - bf * 0.8))
        kgm = max(15.0, kgm * (1.0 - bf * 0.9))
    kgy = 100.0 - kgm; alt = 100.0 - u25
    eo = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    eg = max([("1X", p1 + px), ("X2", p2 + px), ("12", p1 + p2)], key=lambda x: x[1])
    return {
        "lam_ev": le, "lam_dep": ld, "guven": gv,
        "p1": p1, "px": px, "p2": p2,
        "ust_25": u25, "alt_25": alt, "kg_var_model": kgm, "kg_yok_model": kgy,
        "en_olasi": eo, "en_guvenli": eg,
        "en_olasi_gol": "Üst" if u25 > alt else "Alt",
        "en_olasi_kg": "Var" if kgm > kgy else "Yok",
    }


def kayit_olustur(v, a):
    return {"veri": copy.deepcopy(v), "analiz": {
        "p1": a["p1"], "px": a["px"], "p2": a["p2"],
        "tahmini_gol": a["lam_ev"] + a["lam_dep"],
        "kg_var_model": a["kg_var_model"], "ust_25": a["ust_25"],
        "en_olasi_1x2": a["en_olasi"][0], "en_guvenli_cifte": a["en_guvenli"][0],
        "en_olasi_gol": a["en_olasi_gol"], "en_olasi_kg": a["en_olasi_kg"]}}


def sonuc_hesapla(kayit):
    v = kayit["veri"]; a = kayit.get("analiz", {})
    if not v.get("skor_belli", False): return None
    se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    tg = se + sd
    gu = tg > 2.5
    gk = (se > 0 and sd > 0)
    g1 = "1" if se > sd else ("X" if se == sd else "2")
    u25 = a.get("ust_25", 50); alt = 100 - u25
    kgv = a.get("kg_var_model", 50); kgy = 100 - kgv
    p1a = a.get("p1", 33.33); pxa = a.get("px", 33.33); p2a = a.get("p2", 33.34)
    s1x2, y1x2 = max([("1", p1a), ("X", pxa), ("2", p2a)], key=lambda x: x[1])
    o1 = s1x2 if y1x2 >= esik_1x2_al(s1x2) else None
    og = None
    if u25 >= esik_al("ust") and u25 >= alt: og = "Üst"
    elif alt >= esik_al("alt") and alt >= u25: og = "Alt"
    okg = None
    if kgv >= esik_al("kg_var") and kgv >= kgy: okg = "Var"
    elif kgy >= esik_al("kg_yok") and kgy >= kgv: okg = "Yok"
    def _t(o, g):
        if o is None: return None, None
        d = "tam" if o == g else "yanlis"
        return d == "tam", d
    t1, d1 = _t(o1, g1)
    tg_, dg_ = _t(og, "Üst" if gu else "Alt")
    tk, dk = _t(okg, "Var" if gk else "Yok")
    return {
        "oneri_1x2": {"tahmin": o1, "tuttu": t1, "durum": d1},
        "oneri_gol": {"tahmin": og, "tuttu": tg_, "durum": dg_},
        "oneri_kg": {"tahmin": okg, "tuttu": tk, "durum": dk},
        "gercek_1x2": g1, "gercek_gol": "Üst" if gu else "Alt", "gercek_kg": "Var" if gk else "Yok",
    }


# ==========================================
# UI YARDIMCILARI
# ==========================================
def _e(x): return _html.escape(str(x))
def rozet(m, t="gray"): return f'<span class="fa-badge fa-b-{t}">{_e(m)}</span>'


def mac_karti(ev, dep, sb, se, sd, le, ld, saat="", ulke="", tarih=""):
    orta = f'<div class="fa-score">{int(se)} - {int(sd)}</div>' if sb else '<div class="fa-vs">VS</div>'
    b = ulke_bayrak_bul(ulke)
    ust = ""
    if saat or ulke or tarih:
        p = []
        if b != "🌍" or ulke: p.append(f"{b} {_e((ulke or '').title())}")
        if tarih: p.append(f"📅 {_e(tarih)}")
        if saat: p.append(f"🕐 {_e(saat)}")
        if p: ust = f'<div class="fa-sub" style="margin-bottom:8px;">{" • ".join(p)}</div>'
    alt = f'<div class="fa-sub">Model beklenen gol: {le:.2f} - {ld:.2f}</div>'
    return f'<div class="fa-hero">{ust}<div class="fa-teams"><div class="fa-team">{_e(ev)}</div>{orta}<div class="fa-team">{_e(dep)}</div></div>{alt}</div>'


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
        + '<div class="fa-ttl" style="margin-top:12px">Piyasalar</div>'
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


def mac_tahmin_karti(v_g, g=None):
    try:
        a = analiz_hesapla(v_g)
        p1 = a["p1"]; px = a["px"]; p2 = a["p2"]
        u25 = a["ust_25"]; alt = a["alt_25"]
        kgv = a["kg_var_model"]; kgy = a["kg_yok_model"]
        s1, y1 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        e1 = esik_1x2_al(s1); poz1 = y1 >= e1
        i1 = {"1": "1 — Ev Kazanır", "X": "X — Beraberlik", "2": "2 — Dep Kazanır"}[s1]
        if u25 >= alt: gs = "Üst 2.5"; gy = u25; ge_ = esik_al("ust")
        else: gs = "Alt 2.5"; gy = alt; ge_ = esik_al("alt")
        gp = gy >= ge_
        if kgv >= kgy: ks = "KG Var"; ky = kgv; ke = esik_al("kg_var")
        else: ks = "KG Yok"; ky = kgy; ke = esik_al("kg_yok")
        kp = ky >= ke
        def r(p): return "pass" if p else "off"
        def b(p): return "ok" if p else "no"
        def bt(p): return "✅" if p else "⚪"
        return f'''<div class="fa-mk">
        <div class="fa-mk-row"><span class="fa-mk-lbl">🎯 1X2</span><span class="fa-mk-pick {r(poz1)}">{_e(i1)}</span><span class="fa-mk-pct">%{y1:.0f} <span class="fa-mk-badge {b(poz1)}">{bt(poz1)} eşik %{e1:.0f}</span></span></div>
        <div class="fa-mk-row"><span class="fa-mk-lbl">⚽ Gol</span><span class="fa-mk-pick {r(gp)}">{_e(gs)}</span><span class="fa-mk-pct">%{gy:.0f} <span class="fa-mk-badge {b(gp)}">{bt(gp)} eşik %{ge_:.0f}</span></span></div>
        <div class="fa-mk-row"><span class="fa-mk-lbl">🤝 KG</span><span class="fa-mk-pick {r(kp)}">{_e(ks)}</span><span class="fa-mk-pct">%{ky:.0f} <span class="fa-mk-badge {b(kp)}">{bt(kp)} eşik %{ke:.0f}</span></span></div>
        </div>'''
    except Exception:
        return ""


def okunan_veriler_paneli(v):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{v.get('takim_ev', 'Ev')}**")
        st.markdown(f"- Atılan: **{v.get('atilan_ev', 0):.2f}**")
        st.markdown(f"- Yenen: **{v.get('yenen_ev', 0):.2f}**")
        st.markdown(f"- CS: **{v.get('clean_sheets_ev', 0):.1f}%**")
        st.markdown(f"- KG Var: **{v.get('kg_siklik_ev', 0):.1f}%**")
        st.markdown(f"- Üst 2.5: **{v.get('ust25_ev', 0):.1f}%**")
    with c2:
        st.markdown(f"**{v.get('takim_dep', 'Dep')}**")
        st.markdown(f"- Atılan: **{v.get('atilan_dep', 0):.2f}**")
        st.markdown(f"- Yenen: **{v.get('yenen_dep', 0):.2f}**")
        st.markdown(f"- CS: **{v.get('clean_sheets_dep', 0):.1f}%**")
        st.markdown(f"- KG Var: **{v.get('kg_siklik_dep', 0):.1f}%**")
        st.markdown(f"- Üst 2.5: **{v.get('ust25_dep', 0):.1f}%**")


def nav_bar():
    if st.session_state.sayfa == "giris": return
    try: k = st.container(key="fa_nav")
    except TypeError: k = st.container()
    with k:
        if admin_mi():
            sc = [("🏠", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek"), ("⚙️ Ayar", "ayarlar")]
        else:
            sc = [("🏠 Ana", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek")]
        kl = st.columns(len(sc))
        for ko, (e, h) in zip(kl, sc):
            with ko:
                a = st.session_state.sayfa == h
                if st.button(e, key=f"nav_{h}", use_container_width=True, type="primary" if a else "secondary"):
                    if not a:
                        st.session_state.sayfa = h
                        st.session_state.kayit_yapildi = False
                        st.session_state.tek_silme_onay = None
                        st.session_state.tek_silme_gelecek = None
                        st.rerun()


def ust_bar():
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("👑 **Admin Modu**" if admin_mi() else "👤 **Misafir Modu**")
    with c2:
        if st.button("🚪 Çıkış", use_container_width=True, key="cikis_btn"):
            st.session_state.giris_yapildi = False
            st.session_state.rol = None
            st.session_state.sayfa = "giris"
            st.rerun()


def giris_ekrani():
    st.markdown("""
        <div class="login-hero">
            <div class="login-logo">⚽</div>
            <h1 class="login-title">Futbol Analiz Pro</h1>
            <p class="login-subtitle">Akıllı maç analizi ve tahmin motoru</p>
        </div>
    """, unsafe_allow_html=True)
    with st.form("giris_form"):
        s = st.text_input("🔐 Admin Şifresi", type="password", key="sifre_input", placeholder="Şifreni gir...")
        ab = st.form_submit_button("👑  Admin Girişi", use_container_width=True, type="primary")
        st.markdown('<div class="login-divider">VEYA</div>', unsafe_allow_html=True)
        mb = st.form_submit_button("👤  Misafir Olarak Devam Et", use_container_width=True)
        if ab:
            if s == ADMIN_SIFRE:
                st.session_state.giris_yapildi = True
                st.session_state.rol = "admin"
                st.session_state.sayfa = "giris"
                st.rerun()
            else:
                st.error("❌ Yanlış şifre.")
        if mb:
            st.session_state.giris_yapildi = True
            st.session_state.rol = "misafir"
            st.session_state.sayfa = "giris"
            st.rerun()
    st.markdown("""
        <div class="login-features">
            <span class="lf-chip">🎯 1X2</span>
            <span class="lf-chip">⚽ Üst / Alt 2.5</span>
            <span class="lf-chip">🤝 KG Var / Yok</span>
            <span class="lf-chip">📊 İstatistik</span>
        </div>
        <div class="login-footer">© <b>Futbol Analiz Pro</b> • Bilgi amaçlıdır</div>
    """, unsafe_allow_html=True)


if not st.session_state.giris_yapildi:
    giris_ekrani()
    st.stop()

ust_bar()
nav_bar()


# ==========================================
# ANA SAYFA
# ==========================================
if st.session_state.sayfa == "giris":
    if admin_mi():
        st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>Veriler GitHub Actions tarafından otomatik toplanır.</p>", unsafe_allow_html=True)

        st.info("🤖 **Bot günde 2 kez çalışır** (sabah 09:00 ve akşam 21:00). Veriler otomatik güncellenir.")
        st.caption(f"📊 Şu an: **{len(st.session_state.gecmis_analizler)}** geçmiş, **{len(st.session_state.gelecek_analizler)}** gelecek maç")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📊 Geçmiş", use_container_width=True, type="primary"):
                st.session_state.sayfa = "gecmis"; st.rerun()
        with c2:
            if st.button("🔮 Gelecek", use_container_width=True, type="primary"):
                st.session_state.sayfa = "gelecek"; st.rerun()
        with c3:
            if st.button("⚙️ Ayarlar", use_container_width=True):
                st.session_state.sayfa = "ayarlar"; st.rerun()
    else:
        gs = len(st.session_state.gecmis_analizler)
        gl = len(st.session_state.gelecek_analizler)
        st.markdown(f"""
            <div class="mh-hero">
                <div class="mh-hero-icon">⚽</div>
                <div class="mh-hero-title">Futbol Analiz Pro</div>
                <div class="mh-hero-sub">Akıllı maç analizi ve tahmin motoru</div>
                <div class="mh-hero-badge">● CANLI VERİ</div>
            </div>
            <div class="mh-stat-grid">
                <div class="mh-stat"><div class="mh-stat-icon">📊</div><div class="mh-stat-num">{gs}</div><div class="mh-stat-lbl">Geçmiş Maç</div></div>
                <div class="mh-stat"><div class="mh-stat-icon">🔮</div><div class="mh-stat-num">{gl}</div><div class="mh-stat-lbl">Gelecek Maç</div></div>
            </div>
            <div class="mh-section-title">HIZLI ERİŞİM</div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📊  Geçmiş Maçlar", use_container_width=True, type="primary", key="m_gecmis"):
                st.session_state.sayfa = "gecmis"; st.rerun()
        with c2:
            if st.button("🔮  Gelecek Maçlar", use_container_width=True, type="primary", key="m_gelecek"):
                st.session_state.sayfa = "gelecek"; st.rerun()


# ==========================================
# GEÇMİŞ
# ==========================================
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gec = st.session_state.gecmis_analizler
    toplam = len(gec)
    if not gec:
        st.info("ℹ️ Kayıt yok.")
    for i, g in enumerate(reversed(gec)):
        ig = len(gec) - 1 - i
        v = g["veri"]
        te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
        se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
        st.markdown(mac_karti(te, td, True, se, sd, 0, 0, saat=v.get("saat", ""), ulke=v.get("ulke", ""), tarih=v.get("tarih", "")), unsafe_allow_html=True)
        th = mac_tahmin_karti(v, g)
        if th: st.markdown(th, unsafe_allow_html=True)
        if admin_mi():
            cd, csil = st.columns([5, 1])
            with cd:
                if st.button("🔍 Detaylı", use_container_width=True, key=f"gmac_{ig}"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True
                    st.session_state.sayfa = "sonuc"; st.rerun()
            with csil:
                if st.button("🗑️", key=f"gsil_{ig}"):
                    st.session_state.tek_silme_onay = ig if st.session_state.tek_silme_onay != ig else None
                    st.rerun()
            if st.session_state.tek_silme_onay == ig:
                ce, ch = st.columns(2)
                with ce:
                    if st.button("✅ Sil", key=f"gevet_{ig}", use_container_width=True, type="primary"):
                        if 0 <= ig < len(st.session_state.gecmis_analizler):
                            st.session_state.gecmis_analizler.pop(ig)
                            gecmis_kaydet(st.session_state.gecmis_analizler)
                        st.session_state.tek_silme_onay = None; st.rerun()
                with ch:
                    if st.button("❌ İptal", key=f"ghayir_{ig}", use_container_width=True):
                        st.session_state.tek_silme_onay = None; st.rerun()
        st.divider()

    if admin_mi():
        st.markdown("### 💾 Yedekleme (Geçmiş)")
        cind, cyuk = st.columns(2)
        with cind:
            st.download_button(
                label=f"📥 Geçmişi İndir ({toplam} maç)",
                data=json.dumps(st.session_state.gecmis_analizler, ensure_ascii=False, indent=2),
                file_name=f"gecmis_{toplam}mac.json",
                mime="application/json",
                use_container_width=True,
                key="ind_gecmis"
            )
        with cyuk:
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
                        st.error("❌ Format hatalı.")
                except Exception as ex:
                    st.error(f"❌ Hata: {ex}")

        st.divider()
        ct, cg = st.columns(2)
        with ct:
            if st.button("🗑️ Tüm Geçmişi Temizle", use_container_width=True, key="g_temizle"):
                st.session_state.silme_onay = True; st.rerun()
        with cg:
            if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="g_geri"):
                st.session_state.sayfa = "giris"; st.rerun()
        if st.session_state.silme_onay:
            st.warning("⚠️ Tüm geçmiş silinecek. Emin misin?")
            ce, ch = st.columns(2)
            with ce:
                if st.button("✅ Evet, Sil", key="g_sil_evet", use_container_width=True, type="primary"):
                    st.session_state.gecmis_analizler = []
                    try:
                        if os.path.exists(GECMIS_DOSYA): os.remove(GECMIS_DOSYA)
                    except Exception: pass
                    st.session_state.silme_onay = False
                    st.rerun()
            with ch:
                if st.button("❌ İptal", key="g_sil_hayir", use_container_width=True):
                    st.session_state.silme_onay = False; st.rerun()
    else:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="g_geri_m"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# GELECEK
# ==========================================
elif st.session_state.sayfa == "gelecek":
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    gel = st.session_state.gelecek_analizler
    toplam_g = len(gel)
    if not gel:
        st.info("ℹ️ Gelecek maç yok. Bot bir sonraki çalışmasında tahmin olan maçları otomatik ekler.")
    for i, g in enumerate(reversed(gel)):
        ig = len(gel) - 1 - i
        v = g["veri"]
        te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
        try:
            a = analiz_hesapla(v); le = a["lam_ev"]; ld = a["lam_dep"]
        except Exception: le = ld = 0
        st.markdown(mac_karti(te, td, False, 0, 0, le, ld, saat=v.get("saat", ""), ulke=v.get("ulke", ""), tarih=v.get("tarih", "")), unsafe_allow_html=True)
        th = mac_tahmin_karti(v, g)
        if th: st.markdown(th, unsafe_allow_html=True)
        if admin_mi():
            cd, csil = st.columns([5, 1])
            with cd:
                if st.button("🔍 Detaylı", use_container_width=True, key=f"ggmac_{ig}"):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True
                    st.session_state.gelecekten_gelindi = True
                    st.session_state.aktif_gelecek_idx = ig
                    st.session_state.sayfa = "sonuc"; st.rerun()
            with csil:
                if st.button("🗑️", key=f"ggsil_{ig}"):
                    st.session_state.tek_silme_gelecek = ig if st.session_state.tek_silme_gelecek != ig else None
                    st.rerun()
            if st.session_state.tek_silme_gelecek == ig:
                ce, ch = st.columns(2)
                with ce:
                    if st.button("✅ Sil", key=f"ggevet_{ig}", use_container_width=True, type="primary"):
                        if 0 <= ig < len(st.session_state.gelecek_analizler):
                            st.session_state.gelecek_analizler.pop(ig)
                            gelecek_kaydet(st.session_state.gelecek_analizler)
                        st.session_state.tek_silme_gelecek = None; st.rerun()
                with ch:
                    if st.button("❌ İptal", key=f"gghayir_{ig}", use_container_width=True):
                        st.session_state.tek_silme_gelecek = None; st.rerun()
        else:
            if st.button("🔍 Detaylı", use_container_width=True, key=f"ggmac_{ig}"):
                st.session_state.form_verileri = copy.deepcopy(v)
                st.session_state.kayit_yapildi = True
                st.session_state.gelecekten_gelindi = True
                st.session_state.aktif_gelecek_idx = ig
                st.session_state.sayfa = "sonuc"; st.rerun()
        st.divider()

    if admin_mi():
        st.markdown("### 💾 Yedekleme (Gelecek)")
        cind, cyuk = st.columns(2)
        with cind:
            st.download_button(
                label=f"📥 Geleceği İndir ({toplam_g} maç)",
                data=json.dumps(st.session_state.gelecek_analizler, ensure_ascii=False, indent=2),
                file_name=f"gelecek_{toplam_g}mac.json",
                mime="application/json",
                use_container_width=True,
                key="ind_gelecek"
            )
        with cyuk:
            yuk = st.file_uploader("📤 Geleceği Yükle (JSON)", type=["json"], key="yuk_gelecek")
            if yuk is not None:
                try:
                    veri = json.loads(yuk.read().decode("utf-8"))
                    if isinstance(veri, list):
                        st.session_state.gelecek_analizler = veri
                        gelecek_kaydet(veri)
                        st.success(f"✅ {len(veri)} maç yüklendi!")
                        st.rerun()
                    else:
                        st.error("❌ Format hatalı.")
                except Exception as ex:
                    st.error(f"❌ Hata: {ex}")

        st.divider()
        ct, cg = st.columns(2)
        with ct:
            if st.button("🗑️ Tüm Geleceği Temizle", use_container_width=True, key="gel_temizle"):
                st.session_state.silme_onay_gelecek = True; st.rerun()
        with cg:
            if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gel_geri"):
                st.session_state.sayfa = "giris"; st.rerun()
        if st.session_state.silme_onay_gelecek:
            st.warning("⚠️ Tüm gelecek silinecek. Emin misin?")
            ce, ch = st.columns(2)
            with ce:
                if st.button("✅ Evet, Sil", key="gel_sil_evet", use_container_width=True, type="primary"):
                    st.session_state.gelecek_analizler = []
                    try:
                        if os.path.exists(GELECEK_DOSYA): os.remove(GELECEK_DOSYA)
                    except Exception: pass
                    st.session_state.silme_onay_gelecek = False
                    st.rerun()
            with ch:
                if st.button("❌ İptal", key="gel_sil_hayir", use_container_width=True):
                    st.session_state.silme_onay_gelecek = False; st.rerun()
    else:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gel_geri_m"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# AYARLAR
# ==========================================
elif st.session_state.sayfa == "ayarlar":
    if not admin_mi():
        st.error("❌ Sadece admin."); st.stop()
    st.markdown("<h1>⚙️ Eşik Ayarları</h1>", unsafe_allow_html=True)
    st.caption("⚠️ Bu ayarlar Streamlit Cloud'da çalışır ama bot farklı eşikler kullanır. Bot için scraper.py'deki ESIKLER'i güncelle.")
    mv = st.session_state.esikler.copy()
    st.markdown("### 🎯 Maç Sonucu")
    c1, c2, c3 = st.columns(3)
    with c1: y1 = st.slider("1 (Ev) %", 0, 100, int(mv.get("esik_1", 55.0)), 1, key="ay_1")
    with c2: yx = st.slider("X %", 0, 100, int(mv.get("esik_x", 55.0)), 1, key="ay_x")
    with c3: y2 = st.slider("2 (Dep) %", 0, 100, int(mv.get("esik_2", 55.0)), 1, key="ay_2")
    st.markdown("### ⚽ Gol")
    c4, c5 = st.columns(2)
    with c4: yu = st.slider("Üst 2.5 %", 0, 100, int(mv["ust"]), 1, key="ay_ust")
    with c5: ya = st.slider("Alt 2.5 %", 0, 100, int(mv["alt"]), 1, key="ay_alt")
    st.markdown("### 🤝 KG")
    c6, c7 = st.columns(2)
    with c6: ykv = st.slider("KG Var %", 0, 100, int(mv["kg_var"]), 1, key="ay_kgv")
    with c7: yky = st.slider("KG Yok %", 0, 100, int(mv["kg_yok"]), 1, key="ay_kgy")
    st.divider()
    ck, cs, cg = st.columns(3)
    with ck:
        if st.button("💾 Kaydet", use_container_width=True, type="primary"):
            y = {"esik_1": float(y1), "esik_x": float(yx), "esik_2": float(y2), "ust": float(yu), "alt": float(ya), "kg_var": float(ykv), "kg_yok": float(yky)}
            st.session_state.esikler = y; ayarlar_kaydet(y); st.success("✅ Kaydedildi!")
    with cs:
        if st.button("🔄 Sıfırla", use_container_width=True):
            v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0}
            st.session_state.esikler = v; ayarlar_kaydet(v); st.rerun()
    with cg:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="aygeri"):
            st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# SONUÇ
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)
    u25 = a["ust_25"]; alt = a["alt_25"]; kgv = a["kg_var_model"]; kgy = a["kg_yok_model"]
    te = v.get("takim_ev", "") or "Ev Sahibi"; td = v.get("takim_dep", "") or "Deplasman"
    sb = v.get("skor_belli", False); se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    st.markdown(mac_karti(te, td, sb, se, sd, a["lam_ev"], a["lam_dep"], saat=v.get("saat", ""), ulke=v.get("ulke", ""), tarih=v.get("tarih", "")), unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)
    with st.expander("📋 Okunan Veriler", expanded=False):
        okunan_veriler_paneli(v)
    st.divider()
    st.markdown("## 🏆 FİNAL ÖNERİ")
    s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    e1 = esik_1x2_al(s1); p1 = y1 >= e1
    im = {"1": "1 (Ev Sahibi)", "X": "X (Beraberlik)", "2": "2 (Deplasman)"}
    st.markdown(oneri_karti("🎯 1X2", im[s1], y1, e1, p1, f"1: %{a['p1']:.1f} • X: %{a['px']:.1f} • 2: %{a['p2']:.1f}"), unsafe_allow_html=True)
    if u25 >= alt: gs, gy, ge_ = "Üst 2.5", u25, esik_al("ust")
    else: gs, gy, ge_ = "Alt 2.5", alt, esik_al("alt")
    gp = gy >= ge_
    st.markdown(oneri_karti("⚽ Gol", gs, gy, ge_, gp, f"Üst %{u25:.1f} • Alt %{alt:.1f}"), unsafe_allow_html=True)
    if kgv >= kgy: ks, ky, ke = "KG Var", kgv, esik_al("kg_var")
    else: ks, ky, ke = "KG Yok", kgy, esik_al("kg_yok")
    kp = ky >= ke
    st.markdown(oneri_karti("🤝 Karşılıklı Gol", ks, ky, ke, kp, f"Var %{kgv:.1f} • Yok %{kgy:.1f}"), unsafe_allow_html=True)

    if st.session_state.gelecekten_gelindi and admin_mi():
        ig = st.session_state.aktif_gelecek_idx
        if ig is not None and 0 <= ig < len(st.session_state.gelecek_analizler):
            st.divider()
            st.markdown("### 📥 Sonucu Gir ve Geçmişe Taşı")
            sc1, sc2, sc3 = st.columns([1, 1, 1])
            with sc1: yse = st.number_input("Ev Gol", 0, 20, int(v.get("skor_ev", 0)), 1, key=f"gse_{ig}")
            with sc2: ysd = st.number_input("Dep Gol", 0, 20, int(v.get("skor_dep", 0)), 1, key=f"gsd_{ig}")
            with sc3:
                st.markdown(""); st.markdown("")
                if st.button("📥 Taşı", key=f"tasi_{ig}", use_container_width=True, type="primary"):
                    k = st.session_state.gelecek_analizler[ig]
                    k["veri"]["skor_ev"] = int(yse); k["veri"]["skor_dep"] = int(ysd); k["veri"]["skor_belli"] = True
                    yd = sonuc_hesapla(k)
                    if yd: k["dogruluk"] = yd
                    st.session_state.gecmis_analizler.append(k)
                    st.session_state.gelecek_analizler.pop(ig)
                    gecmis_kaydet(st.session_state.gecmis_analizler)
                    gelecek_kaydet(st.session_state.gelecek_analizler)
                    st.session_state.gelecekten_gelindi = False
                    st.session_state.aktif_gelecek_idx = None
                    st.session_state.sayfa = "gelecek"
                    st.rerun()

    st.divider()
    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.sayfa = "giris"
        st.rerun()
