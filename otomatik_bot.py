import time
import requests
from bs4 import BeautifulSoup
import copy
from datetime import datetime

# Hatalı satır temizlendi, fonksiyonlar doğru şekilde içe aktarılıyor
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

MUTARING_URL = "https://www.mutaring.com"

def headers_uret():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

def mutaring_calistir():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Mutaring.com taraması ve son 5 maç analizi başlatıldı...")
    try:
        response = requests.get(MUTARING_URL, headers=headers_uret(), timeout=15)
        if response.status_code != 200:
            print(f"❌ Siteye erişilemedi. HTTP Kod: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        mac_linkleri = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if "match" in href or "stats" in href or "fotboll" in href:
                if href not in mac_linkleri:
                    mac_linkleri.append(href)

        gelecek_listesi = gelecek_yukle()
        gecmis_listesi = gecmis_yukle()
        
        guncellenen_gelecek = list(gelecek_listesi)
        guncellenen_gecmis = list(gecmis_listesi)

        for link in mac_linkleri[:25]:
            try:
                tam_link = link if link.startswith("http") else MUTARING_URL + link
                detay_resp = requests.get(tam_link, headers=headers_uret(), timeout=10)
                if detay_resp.status_code != 200:
                    continue

                detay_soup = BeautifulSoup(detay_resp.text, 'html.parser')
                ham_metin = detay_soup.get_text(separator="\n")

                cikan_veri, _ = metinden_veri_cikar(ham_metin)

                if cikan_veri and cikan_veri.get("takim_ev") and cikan_veri.get("takim_dep"):
                    v = copy.deepcopy(VARSAYILAN_VERI)
                    v.update(cikan_veri)
                    
                    a = analiz_hesapla(v)
                    yeni_kayit = kayit_olustur(v, a)

                    takim_ev = v.get("takim_ev")
                    takim_dep = v.get("takim_dep")
                    skor_belli = v.get("skor_belli", False)

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

                    kaydet_mi = gol_poz or kg_poz or poz_1x2
                    mac_anahtar = f"{takim_ev}-{takim_dep}"

                    if skor_belli:
                        d = sonuc_hesapla(yeni_kayit)
                        if d: 
                            yeni_kayit["dogruluk"] = d
                        gecmis_keys = [f"{g['veri']['takim_ev']}-{g['veri']['takim_dep']}" for g in guncellenen_gecmis]
                        if mac_anahtar not in gecmis_keys:
                            guncellenen_gecmis.append(yeni_kayit)
                    else:
                        gelecek_keys = [f"{g['veri']['takim_ev']}-{g['veri']['takim_dep']}" for g in guncellenen_gelecek]
                        if mac_anahtar not in gelecek_keys and kaydet_mi:
                            guncellenen_gelecek.append(yeni_kayit)

                time.sleep(1)
            except Exception as e:
                continue

        gelecek_kaydet(guncellenen_gelecek)
        gecmis_kaydet(guncellenen_gecmis)
        print("✅ Güncelleme tamamlandı.")

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    mutaring_calistir()
