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

# 5 maçlık veriyi çekmek için ana sayfa isteği de 5 maç olarak ayarlanıyor
MUTATING_URL = "https://www.mutating.com/soccer-predictions/?last=5"

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
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 5 maçlık veri ve kesin biten maç filtresi başlatıldı...")
    json_dosyalarini_kontrol_et()
    
    try:
        response = requests.get(MUTATING_URL, headers=headers_uret(), timeout=15)
        if response.status_code != 200:
            print(f"❌ Siteye erişilemedi. HTTP Kod: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        mac_linkleri = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if "-vs-" in href or "match" in href:
                # 5 maçlık veri filtresini (?last=5) her maç linkine kesin olarak ekliyoruz
                temiz_url = href.split("?")[0] if "?" in href else href
                tam_link = temiz_url if temiz_url.startswith("http") else "https://www.mutating.com" + temiz_url
                tam_link_5_mac = tam_link + "?last=5"
                
                if tam_link_5_mac not in mac_linkleri:
                    mac_linkleri.append(tam_link_5_mac)

        gelecek_listesi = gelecek_yukle()
        gecmis_listesi = gecmis_yukle()
        
        guncellenen_gelecek = list(gelecek_listesi) if gelecek_listesi else []
        guncellenen_gecmis = list(gecmis_listesi) if gecmis_listesi else []

        for link in mac_linkleri[:25]:
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
                    
                    # --- BİTMİŞ MAÇ (FT) KONTROLÜ ---
                    # Metin içinde "FT" geçiyorsa veya skor kesin belliyse maç bitmiştir!
                    if "FT" in ham_metin or "Full Time" in ham_metin:
                        v["skor_belli"] = True

                    skor_belli = v.get("skor_belli", False)

                    # Eğer maç bittiyse (FT ise), GELECEK MAÇLARA ASLA EKLENMEZ!
                    if skor_belli:
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

                    # --- KESİN EŞİK FİLTRESİ ---
                    # Eşiği geçmeyen hiçbir maç gelecek listesine alınmaz (safdışı kalır)
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

        # --- SIRALAMA: En erken maç en üstte ---
        def sira_anahtari(item):
            try:
                tarih_str = item["veri"].get("tarih", "01.01.2026")
                saat_str = item["veri"].get("saat", "00:00")
                return datetime.strptime(f"{tarih_str} {saat_str}", "%d.%m.%Y %H:%M")
            except Exception:
                return datetime.max

        guncellenen_gelecek.sort(key=sira_anahtari, reverse=False)

        gelecek_kaydet(guncellenen_gelecek)
        gecmis_kaydet(gecmis_listesi)
        print("✅ 5 maçlık veri garantilendi, bitmiş maçlar (FT) filtrelendi ve eşik kuralları uygulandı.")

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    mutaring_calistir()
