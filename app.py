Sorun şu: 31 maçın hepsi bitmiş ama sistem "0 taşındı, 31 bitmemiş" diyor. Yani `_skor_cek` hiçbir maçta skor bulamıyor.

Bunun nedeni muhtemelen şu:
1. `requests.get` ile çekilen HTML'de JavaScript ile yüklenen "FT" ve skor yok
2. Playwright tarayıcısı çalışmıyor olabilir (kurulu değil, veya hata veriyor ama sessizce geçiliyor)

Debug yapmam lazım. Şunu ekleyeyim: Her maç için ne olduğunu gösteren detaylı hata mesajları. Böylece neden skor bulunamadığını görebiliriz.

Ama önce bir şey kontrol edeyim — Playwright gerçekten çalışıyor mu? Kodda `_playwright_skor_cek` fonksiyonu var ama belki chromium kurulu değil.

Şunu yapacağım: `_skor_cek` fonksiyonuna debug modu ekleyeceğim. Her maç için:
- requests.get sonucu (başarılı mı, HTML boyutu ne)
- skor_parse sonucu (skor bulundu mu)
- Playwright sonucu (çalıştı mı, hata var mı)

Böylece "Sonuçları İşle" sonrasında hangi aşamada sorun olduğunu göreceğiz.

Yapıyorum:
Tam kod hazır. Şimdi "Skor İşle" dediğinde her maç için detaylı bilgi göreceksin:

**Yeni davranış:**
- Her maç için `requests.get` ve Playwright sonuçları loglanıyor
- "Hata" sayısı 0 değil, artık her maçın neden taşınmadığı detaylı gösteriliyor
- Hata detaylarında şunlar görünecek:
  - "HTTP OK, 5234 bytes | requests ile skor bulunamadı | Playwright OK, 15234 bytes | Playwright ile de skor bulunamadı"
  - veya "Playwright hatası: ..." gibi

**Şimdi yapman gereken:**
1. "Skor İşle" butonuna bas
2. İşlem bitince "⚠️ X hata detayı" expander'ına tıkla
3. Oradaki mesajları bana gönder

Bu mesajlara göre sorunun tam nedenini bulacağım — ya Playwright çalışmıyor, ya da `_skor_parse` fonksiyonu sayfadaki FT'yi bulamıyor.
