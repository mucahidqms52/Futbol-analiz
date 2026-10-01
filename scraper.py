"""
Mutating.com Veri Toplayıcı Bot (PARALEL + AUTO)
- Bugünün maçları: skor varsa Geçmiş'e, yoksa hem gelecek.json hem gelecek_tahmin.json'a
- LİGLER: son N maçı Geçmiş'e ekler
"""
import sys
sys.stdout.reconfigure(line_buffering=True)

import os
import json
import time
import re
import math
import random
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Playwright kurulu değil.")
    sys.exit(1)

# ==========================================
# AYARLAR
# ==========================================
PARALEL = 3
ANA_URL = "https://www.mutating.com/football-stats/"
LIGLER = [
    "https://www.mutating.com/football-stats/league-uefa-champions-league-country-world-tables-stats-h2h-2/",
]
LIG_BASINA_MAC = 10

ESIKLER = {
    "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0,
    "ust": 65.0, "alt": 55.0,
    "kg_var": 57.0, "kg_yok": 72.0,
}

VERI_DOSYA_GELECEK = "data/gelecek.json"              # Tüm oynanmamış
VERI_DOSYA_GELECEK_TAHMIN = "data/gelecek_tahmin.json"  # Sadece eşiği geçen
VERI_DOSYA_GECMIS = "data/gecmis.json"

MAX_GOL = 8
BELIRSIZLIK = 0.20
MONTE_CARLO_N = 10000

_kilit = threading.Lock()


# ==========================================
# YARDIMCILAR
# ==========================================
def clamp(x, lo, hi): return max(lo, min(hi, x))


def html_to_text(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
        tag.decompose()
    for td in soup.find_all(["td", "th"]):
        td.insert_after("\t")
    for tr in soup.find_all("tr"):
        tr.insert_after("\n")
    for e in soup.find_all(["div", "p", "li", "h1", "h2", "h3", "h4", "br"]):
        e.insert_after("\n")
    metin = soup.get_text(separator="", strip=False)
    metin = re.sub(r'[ \t]+\n', '\n', metin)
    metin = re.sub(r'\n{3,}', '\n\n', metin)
    return metin


def _yukle(dosya):
    try:
        if os.path.exists(dosya):
            with open(dosya, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _kaydet(dosya, veri):
    os.makedirs(os.path.dirname(dosya) or ".", exist_ok=True)
    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)


# ==========================================
# POISSON & MODEL
# ==========================================
def poisson_pmf(k, lam):
    if lam <= 0: return 1.0 if k == 0 else 0.0
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)


def poisson_random(lam, rng):
    if lam <= 0: return 0
    L = math.exp(-lam); k = 0; p = 1.0
    while True:
        k += 1; p *= rng.random()
        if p <= L: return k - 1


def poisson_matris(lam_ev, lam_dep, mg=MAX_GOL):
    return [[poisson_pmf(i, lam_ev) * poisson_pmf(j, lam_dep) for j in range(mg)] for i in range(mg)]


def matristen_olasilik(matris, mg=MAX_GOL):
    p1 = px = p2 = 0.0; u25 = 0.0; kg = 0.0; tot = 0.0
    for i in range(mg):
        for j in range(mg):
            p = matris[i][j]; tot += p
            if i > j: p1 += p
            elif i == j: px += p
            else: p2 += p
            tg = i + j
            if tg > 2.5: u25 += p
            if i > 0 and j > 0: kg += p
    return {"1": p1, "X": px, "2": p2, "ust_25": u25, "kg_var": kg, "toplam": tot}


def mac_ici_sok(le, ld, rng):
    if rng.random() < 0.03:
        if rng.random() < 0.5: le *= 0.70
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
    return {"p1": yz(s["1"]), "px": yz(s["X"]), "p2": yz(s["2"]), "ust25": yz(s["u25"]), "kg_var": yz(s["kg"])}


def hesapla_lambda(v):
    at_e = v.get("atilan_ev", 0.0); ye = v.get("yenen_ev", 0.0)
    at_d = v.get("atilan_dep", 0.0); yd = v.get("yenen_dep", 0.0)
    h_ev = at_e if at_e > 0 else 1.2
    h_dep = at_d if at_d > 0 else 1.0
    ts_e = v.get("team_scored_ev", 0); ts_d = v.get("team_scored_dep", 0)
    if ts_e > 0: h_ev *= clamp(ts_e / 60, 0.7, 1.3)
    if ts_d > 0: h_dep *= clamp(ts_d / 60, 0.7, 1.3)
    sd = yd if yd > 0 else 1.2
    se = ye if ye > 0 else 1.0
    le = (h_ev * 0.6 + sd * 0.4) * 1.05
    ld = (h_dep * 0.6 + se * 0.4) * 0.95
    u25e = v.get("ust25_ev", 0); u25d = v.get("ust25_dep", 0)
    if u25e > 0: le *= clamp(u25e / 50, 0.85, 1.15)
    if u25d > 0: ld *= clamp(u25d / 50, 0.85, 1.15)
    return clamp(le, 0.05, 4.5), clamp(ld, 0.05, 4.5)


def analiz_hesapla(v):
    le, ld = hesapla_lambda(v)
    matris = poisson_matris(le, ld, MAX_GOL)
    o = matristen_olasilik(matris, MAX_GOL)
    tot = o["toplam"] or 1
    p1p = o["1"] / tot * 100; pxp = o["X"] / tot * 100; p2p = o["2"] / tot * 100
    u25p = o["ust_25"] / tot * 100; kgp = o["kg_var"] / tot * 100
    mc = monte_carlo(le, ld, MONTE_CARLO_N)
    p1 = p1p * 0.60 + mc["p1"] * 0.40
    px = pxp * 0.60 + mc["px"] * 0.40
    p2 = p2p * 0.60 + mc["p2"] * 0.40
    ge = v.get("galibiyet_ev", 0); gd = v.get("galibiyet_dep", 0)
    if ge > 0 and gd > 0:
        p1 = p1 * 0.85 + ge * 0.15; p2 = p2 * 0.85 + gd * 0.15
    t = p1 + px + p2
    if t > 0: p1, px, p2 = (p1 / t) * 100, (px / t) * 100, (p2 / t) * 100
    u25 = u25p * 0.65 + mc["ust25"] * 0.35
    kgm = kgp * 0.60 + mc["kg_var"] * 0.40
    tbg = le + ld
    if tbg < 1.80:
        bf = (1.80 - tbg) / 1.80
        u25 = max(10.0, u25 * (1.0 - bf * 0.8))
        kgm = max(15.0, kgm * (1.0 - bf * 0.9))
    kgy = 100.0 - kgm; alt = 100.0 - u25
    eo = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    eg = max([("1X", p1 + px), ("X2", p2 + px), ("12", p1 + p2)], key=lambda x: x[1])
    return {
        "lam_ev": le, "lam_dep": ld,
        "p1": p1, "px": px, "p2": p2,
        "ust_25": u25, "alt_25": alt,
        "kg_var_model": kgm, "kg_yok_model": kgy,
        "en_olasi": eo, "en_guvenli": eg,
        "en_olasi_gol": "Üst" if u25 > alt else "Alt",
        "en_olasi_kg": "Var" if kgm > kgy else "Yok",
    }


def esik_al(key): return ESIKLER.get(key, 50.0)
def esik_1x2_al(secim):
    km = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}
    return ESIKLER.get(km.get(secim, ""), 55.0)


def tahmin_var_mi(v):
    """Bu maçta eşiği geçen bir tahmin var mı?"""
    try:
        a = analiz_hesapla(v)
        s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
        if y1 >= esik_1x2_al(s1): return True
        if a["ust_25"] >= esik_al("ust") and a["ust_25"] >= a["alt_25"]: return True
        if a["alt_25"] >= esik_al("alt") and a["alt_25"] >= a["ust_25"]: return True
        if a["kg_var_model"] >= esik_al("kg_var") and a["kg_var_model"] >= a["kg_yok_model"]: return True
        if a["kg_yok_model"] >= esik_al("kg_yok") and a["kg_yok_model"] >= a["kg_var_model"]: return True
        return False
    except Exception:
        return False


def kayit_olustur(v, a):
    return {"veri": v, "analiz": {
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
# HTML PARSE
# ==========================================
def mac_html_parse(html, url=""):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    veri = {}
    h1 = soup.find("h1")
    if h1:
        baslik = h1.get_text(strip=True)
        if " - " in baslik:
            p = baslik.replace(" Stats", "").replace(" stats", "").split(" - ")
            veri["takim_ev"] = p[0].strip()
            if len(p) > 1: veri["takim_dep"] = p[1].strip()
    metin = html_to_text(html)
    m = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', metin)
    if m: veri["tarih"] = m.group(1)
    m = re.search(r'(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1)

    skor_ev = skor_dep = None
    m = re.search(r'FT\s*\n+\s*(\d{1,2})\s*[-:]\s*(\d{1,2})', metin)
    if m:
        skor_ev = int(m.group(1)); skor_dep = int(m.group(2))
    if skor_ev is not None:
        veri["skor_ev"] = skor_ev; veri["skor_dep"] = skor_dep; veri["skor_belli"] = True
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
    return veri


# ==========================================
# PLAYWRIGHT
# ==========================================
def fetch_html_tek(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
            page = browser.new_page()
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            js = """
            (function() {
                var tum = document.querySelectorAll('label, span, div, button');
                for (var i = 0; i < tum.length; i++) {
                    var t = (tum[i].textContent || '').trim();
                    if (t === '5' && tum[i].children.length <= 1) {
                        try { tum[i].click(); } catch(e) {}
                    }
                }
                var hedef = ['Home', 'Away'];
                var els = document.querySelectorAll('label, span, div, button');
                for (var k = 0; k < els.length; k++) {
                    var txt = (els[k].textContent || '').trim();
                    if (hedef.indexOf(txt) !== -1 && els[k].children.length <= 1) {
                        try { els[k].click(); } catch(e) {}
                    }
                }
                return true;
            })();
            """
            try: page.evaluate(js)
            except Exception: pass
            page.wait_for_timeout(2500)

            html = page.content()
            browser.close()
            return html
    except Exception as e:
        print(f"    ⚠️ fetch hatası: {e}")
        return None


def ana_sayfa_linkleri():
    html = fetch_html_tek(ANA_URL)
    if not html: return []
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gorulen = set()
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        if not any(x in href for x in ["match-preview", "/match/"]): continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gorulen: continue
        gorulen.add(href)
        h2_list = link.find_all("h2")
        te = h2_list[0].get_text(strip=True) if len(h2_list) > 0 else ""
        td = h2_list[1].get_text(strip=True) if len(h2_list) > 1 else ""
        maclar.append({"url": href, "takim_ev": te, "takim_dep": td})
    return maclar


def lig_linkleri(lig_url, adet=10):
    html = fetch_html_tek(lig_url)
    if not html: return []
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gorulen = set()
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        if "match-preview" not in href: continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gorulen: continue
        gorulen.add(href)
        te = ""; td = ""
        img = link.find_all("img", alt=True)
        if len(img) >= 2:
            te = img[0].get("alt", "").strip()
            td = img[1].get("alt", "").strip()
        maclar.append({"url": href, "takim_ev": te, "takim_dep": td})
        if len(maclar) >= adet: break
    return maclar


# ==========================================
# WORKER
# ==========================================
def _mac_isle(mac, hedef_tip, mevcut_urls):
    try:
        if mac["url"] in mevcut_urls:
            return ("atlandi", None, "Zaten var")

        html = fetch_html_tek(mac["url"])
        if not html:
            return ("hata", mac, "HTML yok")

        veri = mac_html_parse(html, mac["url"])
        skor_var = veri.get("skor_belli", False)

        if hedef_tip == "gelecek" and skor_var:
            return ("atlandi", None, "Bitmiş maç")
        if hedef_tip == "gecmis" and not skor_var:
            return ("atlandi", None, "Skor yok")

        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")

        if veri.get("atilan_ev", 0) == 0 or veri.get("yenen_ev", 0) == 0:
            return ("atlandi", None, "İstatistik eksik")

        kayit = kayit_olustur(veri, analiz_hesapla(veri))
        if skor_var:
            kayit["dogruluk"] = sonuc_hesapla(kayit)
            return ("eklendi_gecmis", kayit, f"{veri.get('skor_ev')}-{veri.get('skor_dep')}")
        else:
            # Skorsuz → gelecek.json'a her zaman ekle
            # Tahmin varsa → ayrıca gelecek_tahmin.json için işaretle
            tahmin_var = tahmin_var_mi(veri)
            return ("eklendi_gelecek", kayit, "tahminli" if tahmin_var else "tahminsiz")
    except Exception as e:
        return ("hata", mac, str(e))


# ==========================================
# ANA
# ==========================================
def main():
    print("=" * 60)
    print(f"🤖 Bot Başladı — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"⚡ Paralel: {PARALEL} thread")
    print("=" * 60)

    gelecek_mevcut = _yukle(VERI_DOSYA_GELECEK)            # Tüm oynanmamış
    tahmin_mevcut = _yukle(VERI_DOSYA_GELECEK_TAHMIN)       # Sadece tahmini
    gecmis_mevcut = _yukle(VERI_DOSYA_GECMIS)

    gelecek_urls = set(g.get("veri", {}).get("kaynak_url", "") for g in gelecek_mevcut)
    tahmin_urls = set(g.get("veri", {}).get("kaynak_url", "") for g in tahmin_mevcut)
    gecmis_urls = set(g.get("veri", {}).get("kaynak_url", "") for g in gecmis_mevcut)

    print(f"📂 Mevcut: Gelecek={len(gelecek_mevcut)}, Tahmin={len(tahmin_mevcut)}, Geçmiş={len(gecmis_mevcut)}")

    yeni_g = 0; yeni_t = 0; yeni_ge = 0

    # ---- 1) BUGÜNÜN MAÇLARI (AUTO) ----
    print("\n🔄 Bugünün maçları...")
    try:
        maclar = ana_sayfa_linkleri()
        print(f"  → {len(maclar)} maç bulundu")

        tum_urls = gelecek_urls | gecmis_urls
        tamamlanan = 0

        with ThreadPoolExecutor(max_workers=PARALEL) as executor:
            futures = {executor.submit(_mac_isle, m, "auto", tum_urls): m for m in maclar}
            for fut in as_completed(futures):
                tamamlanan += 1
                try:
                    sonuc, kayit, mesaj = fut.result()
                    if sonuc == "eklendi_gecmis":
                        with _kilit:
                            gecmis_mevcut.append(kayit)
                            gecmis_urls.add(kayit["veri"].get("kaynak_url", ""))
                        yeni_ge += 1
                        print(f"  [{tamamlanan}/{len(maclar)}] ✅ Bitmiş → Geçmiş ({mesaj})")
                    elif sonuc == "eklendi_gelecek":
                        with _kilit:
                            # Her zaman gelecek.json'a ekle
                            gelecek_mevcut.append(kayit)
                            gelecek_urls.add(kayit["veri"].get("kaynak_url", ""))
                            yeni_g += 1
                            # Tahmin varsa ayrıca tahmin.json'a ekle
                            if mesaj == "tahminli":
                                url = kayit["veri"].get("kaynak_url", "")
                                if url not in tahmin_urls:
                                    tahmin_mevcut.append(kayit)
                                    tahmin_urls.add(url)
                                    yeni_t += 1
                                    print(f"  [{tamamlanan}/{len(maclar)}] ✅ Tahmin var → Gelecek + Tahmin")
                                else:
                                    print(f"  [{tamamlanan}/{len(maclar)}] ⏭️  Tahmin zaten var")
                            else:
                                print(f"  [{tamamlanan}/{len(maclar)}] ⚪ Tahmin yok → Sadece Gelecek")
                    else:
                        print(f"  [{tamamlanan}/{len(maclar)}] ⏭️  {mesaj}")
                except Exception as e:
                    print(f"  [{tamamlanan}/{len(maclar)}] ❌ {e}")
    except Exception as e:
        print(f"  ❌ Genel hata: {e}")

    # ---- 2) LİGLER → GEÇMİŞ ----
    for lig_url in LIGLER:
        print(f"\n📜 Lig: {lig_url[:80]}...")
        try:
            maclar = lig_linkleri(lig_url, adet=LIG_BASINA_MAC)
            print(f"  → {len(maclar)} maç bulundu")

            tamamlanan = 0
            with ThreadPoolExecutor(max_workers=PARALEL) as executor:
                futures = {executor.submit(_mac_isle, m, "gecmis", gecmis_urls): m for m in maclar}
                for fut in as_completed(futures):
                    tamamlanan += 1
                    try:
                        sonuc, kayit, mesaj = fut.result()
                        if sonuc == "eklendi_gecmis":
                            with _kilit:
                                gecmis_mevcut.append(kayit)
                                gecmis_urls.add(kayit["veri"].get("kaynak_url", ""))
                            yeni_ge += 1
                            print(f"  [{tamamlanan}/{len(maclar)}] ✅ {mesaj} → Geçmiş")
                        else:
                            print(f"  [{tamamlanan}/{len(maclar)}] ⏭️  {mesaj}")
                    except Exception as e:
                        print(f"  [{tamamlanan}/{len(maclar)}] ❌ {e}")
        except Exception as e:
            print(f"  ❌ Lig hatası: {e}")

    _kaydet(VERI_DOSYA_GELECEK, gelecek_mevcut)
    _kaydet(VERI_DOSYA_GELECEK_TAHMIN, tahmin_mevcut)
    _kaydet(VERI_DOSYA_GECMIS, gecmis_mevcut)

    print("\n" + "=" * 60)
    print(f"✅ Bitti!")
    print(f"   Gelecek: +{yeni_g} → Toplam {len(gelecek_mevcut)}")
    print(f"   Tahmin:  +{yeni_t} → Toplam {len(tahmin_mevcut)}")
    print(f"   Geçmiş:  +{yeni_ge} → Toplam {len(gecmis_mevcut)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
