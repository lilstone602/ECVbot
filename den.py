import time
import random
import kur

from datetime import datetime

def hepsi(begenisınır, yorumsınır, kaydetsınır, takipsınır, kaydırsınır, calısma_zamanı, kontrol):
    sayac = 1
    begeni = 0
    yorumyaz = 0
    reelskaydet = 0
    takip = 0
    
    baslangıc = time.time()  # Unix timestamp olarak başlangıç zamanı
    bitis = baslangıc + calısma_zamanı

    while time.time() < bitis and not kontrol.durdur:
        kalan_sure = int(bitis - time.time())
        print(f"\n{sayac}. adım (Kalan süre: {kalan_sure}s)")
        sayac += 1

        # Rastgele işlem seçimi
        b = random.randint(0, begenisınır + yorumsınır + kaydetsınır + takipsınır + kaydırsınır)
        a = kur.sako(b, begenisınır, yorumsınır, kaydetsınır, takipsınır, kaydırsınır)
        print("Yapılan işlem:", a)

        # İşlem sayacı güncelleme
        if a == "yorumyaz":
            yorumyaz += 1
        elif a == "begenop3":
            begeni += 1
        elif a == "kaydet":
            reelskaydet += 1
        elif isinstance(a, int) and a >= 0:
            takip += a

        # Dinamik bekleme süresi (1-10s arası)
        bekleme = random.uniform(1, 10) if random.randint(1, 3) != 1 else random.uniform(1, 4)
        time.sleep(bekleme)

        # Anlık istatistikler
        print(f"İstatistikler | Beğeni: {begeni} | Yorum: {yorumyaz} | Kaydet: {reelskaydet} | Takip: {takip}")

    # Döngüden çıkış sebebi kontrolü
    if kontrol.durdur:
        print("Kullanıcı tarafından durduruldu!")
        return "Kullanıcı tarafından durduruldu"
    else:
        calisma_suresi = int(time.time() - baslangıc)
        print(f"Görev tamamlandı! Toplam süre: {calisma_suresi}s")
        return begeni, reelskaydet, yorumyaz, takip