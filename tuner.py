import numpy as np
import sounddevice as sd

gitar_telleri = {
    "E (kalın, 6. tel)": 82.41,
    "A (5. tel)": 110.00,
    "D (4. tel)": 146.83,
    "G (3. tel)": 196.00,
    "B (2. tel)": 246.94,
    "E (ince, 1. tel)": 329.63
}


def en_yakin_tel(frekans):
    en_yakin = min(gitar_telleri.items(), key=lambda x: abs(x[1] - frekans))
    return en_yakin


def frekans_bul(ses_verisi, ornekleme_hizi):
    ses_verisi = ses_verisi.astype(np.float64)
    genlik_ortalama = np.abs(ses_verisi).mean()

    if genlik_ortalama < 0.002:
        return 0

    ses_verisi = ses_verisi - np.mean(ses_verisi)

    min_tau = int(ornekleme_hizi / 400)
    max_tau = int(ornekleme_hizi / 60)

    fark = np.zeros(max_tau)

    for tau in range(1, max_tau):
        fark[tau] = np.sum(
            (ses_verisi[:-tau] - ses_verisi[tau:]) ** 2
        )

    cmndf = np.ones(max_tau)
    toplam = 0.0

    for tau in range(1, max_tau):
        toplam += fark[tau]
        cmndf[tau] = fark[tau] / (toplam / tau) if toplam > 0 else 1

    esik = 0.15
    tau_tahmini = -1

    for tau in range(min_tau, max_tau):
        if cmndf[tau] < esik:
            tau_tahmini = tau

            while (
                tau_tahmini + 1 < max_tau
                and cmndf[tau_tahmini + 1] < cmndf[tau_tahmini]
            ):
                tau_tahmini += 1

            break

    if tau_tahmini == -1:
        return 0

    if 0 < tau_tahmini < max_tau - 1:
        y0 = cmndf[tau_tahmini - 1]
        y1 = cmndf[tau_tahmini]
        y2 = cmndf[tau_tahmini + 1]

        payda = y0 - 2 * y1 + y2

        if payda != 0:
            tau_tahmini += 0.5 * (y0 - y2) / payda

    return ornekleme_hizi / tau_tahmini


# Kullanıcıya mevcut ses giriş cihazlarını göster
print("Mevcut ses giriş cihazları:\n")

cihazlar = sd.query_devices()
giris_cihazlari = []

for i, cihaz in enumerate(cihazlar):
    if cihaz['max_input_channels'] > 0:
        giris_cihazlari.append(i)
        print(
            f"  {i}: {cihaz['name']} "
            f"({cihaz['max_input_channels']} kanal)"
        )

print()

secim = input("Kullanmak istediğin cihazın numarasını gir: ")
hedef_index = int(secim)

if hedef_index not in giris_cihazlari:
    print("Geçersiz cihaz numarası!")

else:
    ornekleme_hizi = 44100
    pencere_suresi = 0.5

    print(
        "Sürekli dinleme başladı. "
        "Durdurmak için Ctrl+C bas.\n"
    )

    try:
        while True:
            kanal_sayisi = cihazlar[hedef_index]['max_input_channels']

            # En fazla 2 kanal kullan
            kullanilacak_kanal = min(kanal_sayisi, 2)

            kayit = sd.rec(
                int(pencere_suresi * ornekleme_hizi),
                samplerate=ornekleme_hizi,
                channels=kullanilacak_kanal,
                device=hedef_index
            )

            sd.wait()

            # Son kanalı al
            kayit = kayit[:, kullanilacak_kanal - 1]

            frekans = frekans_bul(
                kayit,
                ornekleme_hizi
            )

            if frekans == 0:
                print("...", end="\r")

            else:
                tel_adi, hedef_frekans = en_yakin_tel(frekans)
                fark = frekans - hedef_frekans

                if abs(fark) < 1:
                    durum = "✓ Akortlu!          "

                elif fark > 0:
                    durum = (
                        f"Çok tiz, "
                        f"{abs(fark):5.2f} Hz gevşet   "
                    )

                else:
                    durum = (
                        f"Çok pes, "
                        f"{abs(fark):5.2f} Hz sıkıştır "
                    )

                print(
                    f"{tel_adi:20s} | "
                    f"{frekans:6.2f} Hz | "
                    f"{durum}",
                    end="\r"
                )

    except KeyboardInterrupt:
        print("\n\nDinleme durduruldu.")