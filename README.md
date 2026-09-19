# gitar-frekans

\# Gitar Frekans \& Tuner Projesi



Elektro gitar telleri için frekans hesaplama ve gerçek zamanlı akort (tuner) uygulaması. Python ile geliştirildi, ses analizi için FFT ve YIN algoritması kullanır.



\## İçerik



\- \*\*gitar.py\*\* — Tel ve perde numarasına göre teorik frekans ve nota ismini hesaplar

\- \*\*tuner.py\*\* — Mikrofon/ses arayüzünden gerçek zamanlı ses alıp, en yakın gitar teline göre akort durumunu gösterir



\## Gereksinimler



\- Python 3.10+

\- Bir ses girişi (dahili mikrofon veya harici ses arayüzü, örn. M-Audio M-Track)



\## Kurulum



```bash

pip install -r requirements.txt

```



\## Kullanım



\*\*Teorik frekans/nota hesaplama:\*\*

```bash

py gitar.py

```

Tel numarası (1-6) ve perde numarası (0-24) girildiğinde, o notanın frekansını ve ismini (örn. "E4") gösterir.



\*\*Gerçek zamanlı tuner:\*\*

```bash

py tuner.py

```

Sürekli dinleme moduna geçer, gitar teline çaldıkça anlık frekans ve akort durumunu ("akortlu", "gevşet", "sıkıştır") gösterir. Durdurmak için `Ctrl+C`.



\## Bilinen Sınırlamalar



\- Ses arayüzü kodda ismiyle ("M-Track") aranıyor; farklı bir cihaz kullanıyorsan `tuner.py` içindeki cihaz arama satırını kendi cihaz isminle güncellemen gerekir.

\- Gürültülü elektriksel ortamlarda (uğultu/hum) yanlış okuma yapabilir; temiz bir sinyal kaynağı (düşük gain, kaliteli kablo) önerilir.



\## Nasıl Çalışır



Frekans tespiti için \*\*YIN algoritması\*\* kullanılır — sinyali kendisiyle farklı zaman kaymalarında karşılaştırıp, periyodikliğin en güçlü olduğu noktayı (temel frekansı) bulur. Bu yöntem, basit otokorelasyona göre yanlış oktav/harmonik kilitlenmelerine karşı daha dayanıklıdır.

