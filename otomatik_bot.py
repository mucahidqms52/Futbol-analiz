import time
import requests
from bs4 import BeautifulSoup
import copy
import os
import json
from datetime import datetime

# Senin ana dosyadaki fonksiyonlarını ve veri yapılarını içe aktarıyoruz
from app import (
    VARSAYILAN_VERI, 
    metinden_veri_cikar, 
    analiz_hesapla, 
    kayit_olustur, 
    sonuc_hesapla, 
    gelecek_yukle, 
    gelecek_kaydet, 
    gecmis_yukle, 
    gecmis_kaydet,
    esik_al,
    esik_1x2_al
)

ANA_URL = "https://www.mutating.com/soccer-predictions/?last=5"

def headers_uret():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

def json_dosyalarini_kontrol_et():
    if not os.path.exists("gelecek.json"):
        with open("gelecek.json", "w", encoding="utf-8") as f:
            json.dump([], f)
    if not os.path.exists("gecmis.json"):
        with open("gecmis.json", "w", encoding="utf-8") as f:
            json.dump([], f)

def mutaring_calistir():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Bugün ve önümüzdeki 3 günün maçları taranıyor...")
    json_dosyalarini_kontrol_et()
    
    try:
        # Önce ana sayfayı (bugün ve tarih sekmelerini içeren sayfayı) çekiyoruz
        response = requests.get(ANA_URL, headers=headers_uret(), timeout=15)
        if response.status_code != 200:
            print(f"❌ Ana sayfaya erişilemedi. HTTP Kod: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Adım: Sayfadaki tarih sekmelerinin linklerini (02, 03, 04 günleri vb.) buluyoruz
        taranacak_sayfalar = [ANA_URL]
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Tarih veya gün geçiş linklerini yakalama
            if any(t in href for t in ["/2026-", "/soccer-predictions/"]):
                tam_tarih_link = href if href.startswith("http") else "https://www.mutating.com" + href
                if "?last=5" not in tam_tarih_link:
                    tam_tarih_link += "?last=5"
                if tam_tarih_link not in taranacak_sayfalar:
                    taranacak_sayfalar.append(tam_tarih_link)

        # Çok fazla sayfada boğulmamak için ilk 5 gün/sayfa sekmesini sınır alıyoruz
        taranacak_sayfalar = taranacak_sayfalar[:5]

        mac_linkleri = []
        for sayfa_url in taranacak_sayfalar:
            try:
                s_resp = requests.get(sayfa_url, headers=headers_uret(), timeout=10)
                if s_resp.status_code != 200:
                    continue
                s_soup = BeautifulSoup(s_resp.text, 'html.parser')
                for a_tag in s_soup.find_all('a', href=True):
                    href = a_tag['href']
                    if "-vs-" in href or "match" in href:
                        temiz_url = href.split("?")[0] if "?" in href else href
                        tam_link = temiz_url if temiz_url.startswith("http") else "https://www.mutating.com" + temiz_url
                        tam_link_5_mac = tam_link + "?last=5"
                        
                        if tam_link_5_mac not in mac_linkleri:
                            mac_linkleri.append(tam_link_5_mac)
            except Exception:
                continue

        gelecek_listesi = gelecek_yukle()
        gecmis_listesi = gecmis_yukle()
        
        guncellenen_gelecek = list(gelecek_listesi) if gelecek_listesi else []
        guncellenen_gecmis = list(gecmis_listesi) if gecmis_listesi else []

        for link in mac_linkleri[:40]: # Toplam taranacak maç limiti
            try:
                detay_resp = requests.get(link, headers=headers_uret(), timeout=10)
                if detay_resp.status_code != 200:
                    continue

                detay_soup = BeautifulSoup(detay_resp.text, 'html.parser')
                
                for element in detay_soup(["nav", "footer", "header", "aside", "script", "style", "menu", "form"]):
                    element.decompose()

                ana_icerik = detay_soup.find("main") or detay_soup.find("div", class_="content") or detay_soup
                ham_metin = ana_icerik.get_text(separator="\n")

                cikan_veri, _ = metinden_veri_cikar(ham_metin)

                if cikan_veri and cikan_veri.get("takim_ev") and cikan_veri.get("takim_dep"):
                    takim_ev = cikan_veri.get("takim_ev")
                    takim_dep = cikan_veri.get("takim_dep")

                    yasaklar = ["Leagues", "Premier", "Bundesliga", "Serie", "Blog", "Stats", "Preview", "Prediction", "Champions"]
                    if any(y in takim_ev for y in yasaklar) or any(y in takim_dep for y in yasaklar):
                        continue

                    v = copy.deepcopy(VARSAYILAN_VERI)
                    v.update(cikan_veri)
                    
                    # BİTMİŞ MAÇ (FT) FİLTRESİ: Maç bittiyse kesinlikle geleceğe eklenmez
                    if "FT" in ham_metin or "Full Time" in ham_metin:
                        v["skor_belli"] = True

                    if v.get("skor_belli", False):
                        continue

                    a = analiz_hesapla(v)
                    yeni_kayit = kayit_olustur(v, a)

                    p1 = a["p1"]; px = a["px"]; p2 = a["p2"]
                    ust_25 = a["ust_25"]; alt_25 = a["alt_25"]
                    kg_var = a["kg_var_model"]; kg_yok = a["kg_yok_model"]

                    en_yuksek_1x2 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
                    sec_1x2, yuzde_1x2 = en_yuksek_1x2
                    poz_1x2 = yuzde_1x2 >= esik_1x2_al(sec_1x2)

                    gol_yuzde = ust_25 if ust_25 >= alt_25 else alt_25
                    gol_esik = esik_al("ust") if ust_25 >= alt_25 else esik_al("alt")
                    gol_poz = gol_yuzde >= gol_esik

                    kg_yuzde = kg_var if kg_var >= kg_yok else kg_yok
                    kg_esik = esik_al("kg_var") if kg_var >= kg_yok else esik_al("kg_yok")
                    kg_poz = kg_yuzde >= kg_esik

                    # KESİN EŞİK FİLTRESİ: Eşiği geçmeyenler safdışı kalır
                    kaydet_mi = bool(gol_poz or kg_poz or poz_1x2)
                    if not kaydet_mi:
                        continue

                    mac_anahtar = f"{takim_ev}-{takim_dep}"
                    gelecek_keys = [f"{g['veri']['takim_ev']}-{g['veri']['takim_dep']}" for g in guncellenen_gelecek]
                    
                    if mac_anahtar not in gelecek_keys:
                        guncellenen_gelecek.append(yeni_kayit)

                time.sleep(1)
            except Exception as e:
                continue

        # --- NİHAİ KRONOLOJİK SIRALAMA: En erken tarih ve saat en üstte ---
        def sira_anahtari(item):
            try:
                tarih_str = item["veri"].get("tarih", "01.01.2026")
                saat_str = item["veri"].get("saat", "00:00")
                return datetime.strptime(f"{tarih_str} {saat_str}", "%d.%m.%Y %H:%M")
            except Exception:
                return datetime.max

        # reverse=False ile en erken maç (ve en erken gün) en üste getirilir
        guncellenen_gelecek.sort(key=sira_anahtari, reverse=False)

        gelecek_kaydet(guncellenen_gelecek)
        gecmis_kaydet(gecmis_listesi)
        print("✅ Bugün ve önümüzdeki günlerin 5 maçlık verileri, FT filtresi ve kronolojik sıralaması tamamlandı.")

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    mutaring_calistir()
