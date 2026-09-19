def frekans_hesapla(tel_no, perde_no):
    # Standart gitar akort frekansları (Hz) - kalın telden ince tele
    acik_tel_frekanslari = {
        6: 82.41,
        5: 110.00,
        4: 146.83,
        3: 196.00,
        2: 246.94,
        1: 329.63
    }
    
    acik_frekans = acik_tel_frekanslari[tel_no]
    frekans = acik_frekans * (2 ** (perde_no / 12))
    return frekans


def nota_hesapla(tel_no, perde_no):
    # Her tel için açık halin "MIDI numarası" (piyanodaki karşılığı gibi düşün)
    acik_tel_midi = {
        6: 40,  # E2
        5: 45,  # A2
        4: 50,  # D3
        3: 55,  # G3
        2: 59,  # B3
        1: 64   # E4
    }
    
    nota_isimleri = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    toplam_midi = acik_tel_midi[tel_no] + perde_no
    nota = nota_isimleri[toplam_midi % 12]
    oktav = toplam_midi // 12 - 1
    
    return f"{nota}{oktav}"


# Kullanıcıdan girdi al
tel = int(input("Tel numarası (1-6): "))
perde = int(input("Perde numarası (0-24): "))

frekans = frekans_hesapla(tel, perde)
nota = nota_hesapla(tel, perde)

print(f"Nota: {nota}")
print(f"Frekans: {frekans:.2f} Hz")