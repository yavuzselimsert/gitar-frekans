# 🎸 Gitar Frekans & Tuner

Python ile geliştirilmiş basit bir gitar frekans hesaplama ve gerçek zamanlı akort projesi.

## 📁 Proje Dosyaları

### `gitar.py`

Gitarın belirli bir telindeki ve perdesindeki notanın:

* Nota adını
* Teorik frekansını (Hz)

hesaplar.

Program tel numarası ve perde numarasını kullanıcıdan alır.

Örneğin:

```text
Tel numarası (1-6): 6
Perde numarası (0-24): 0

Nota: E2
Frekans: 82.41 Hz
```

### `tuner.py`

Mikrofondan veya bağlı bir ses kartından gelen gitar sinyalini gerçek zamanlı olarak analiz eder.

Program başlatıldığında mevcut ses giriş cihazlarını listeler:

```text
Mevcut ses giriş cihazları:

  1: Mikrofon (...)
  2: M-Track (...)
```

Kullanıcı kullanmak istediği cihazın numarasını seçtikten sonra tuner çalışmaya başlar.

Program:

1. Gitar sesini kaydeder.
2. Ses sinyalinin temel frekansını YIN algoritmasıyla tahmin eder.
3. Frekansı en yakın standart gitar teliyle karşılaştırır.
4. Telin akort durumunu gösterir.

Örnek çıktı:

```text
E (kalın, 6. tel) | 82.35 Hz | ✓ Akortlu!
```

veya:

```text
A (5. tel)        | 112.40 Hz | Çok tiz, 2.40 Hz gevşet
```

## ⚙️ Gereksinimler

* Python 3.10+
* NumPy
* SoundDevice
* Mikrofon veya ses kartı
* Gitar

Bağımlılıkları yüklemek için:

```bash
pip install -r requirements.txt
```

## ▶️ Kullanım

### Frekans hesaplama

```bash
py gitar.py
```

Ardından tel ve perde numarasını girin.

### Gerçek zamanlı tuner

```bash
py tuner.py
```

Program mevcut ses giriş cihazlarını listeleyecektir.

Kullanmak istediğiniz cihazın numarasını girin. Daha sonra tuner sürekli olarak gitar sinyalini analiz etmeye başlayacaktır.

Programı durdurmak için:

```text
Ctrl + C
```

kullanabilirsiniz.

## 🧠 Nasıl Çalışıyor?

### Frekans hesaplama

Gitar tellerinin standart akort frekansları kullanılarak perde frekansı hesaplanır:

```text
f = f₀ × 2^(n/12)
```

Burada:

* `f₀` = açık telin frekansı
* `n` = perde numarası
* `f` = elde edilen frekans

### Tuner

`tuner.py`, ses sinyalinden temel frekansı tahmin etmek için **YIN algoritması** kullanır.

Tahmin edilen frekans daha sonra standart gitar tellerinin frekanslarıyla karşılaştırılır.

## 🎯 Projenin Amacı

Bu proje, gitar akordunun arkasındaki:

* frekans
* nota
* ses sinyali
* temel frekans tespiti

gibi kavramları Python kullanarak pratik şekilde incelemek amacıyla geliştirilmiştir.

## ⚠️ Sınırlamalar

* Gürültülü ortamlarda frekans tespiti daha az doğru olabilir.
* Çok düşük seviyeli ses sinyalleri algılanmayabilir.
* Tuner, standart gitar akordundaki telleri (EADGBE) temel alır.
* Kullanılan ses giriş cihazının sürücüsü ve ayarları sonuçları etkileyebilir.
