import time
import os
import multiprocessing
import fonksiyonlar  # 5000 satırlık kodların olduğu dosya
import kurucu
import den
def bot_icin_gorev(serial):
    # Ortam değişkenini bu süreç için ayarla
    os.environ["ANDROID_SERIAL"] = serial
    fonksiyonlar.open_app_at_coordinates(1,1)
    # Şimdi bu süreç içinde yapılan tüm subprocess çağrıları bu cihazı kullanır
    #kodlar buraya
    
    print(f"✅ {serial} için işlemler tamamlandı.")

if __name__ == "__main__":
    serial_list = ["emulator-5558","emulator-5556"]

    processes = []
    for serial in serial_list:
        p = multiprocessing.Process(target=bot_icin_gorev, args=(serial,))
        p.start()
        processes.append(p)

    # İstersen hepsinin bitmesini bekleyebilirsin
    for p in processes:
        p.join()
