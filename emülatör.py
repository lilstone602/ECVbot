import random
import string
import subprocess
import time
import fonksiyonlar


def adb(cmd):
    """ADB komutu çalıştırır, çıktıyı döner."""
    result = subprocess.run(f'adb {cmd}', shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ADB komut hatası: {result.stderr}")
    return result.stdout.strip()

# === Kimlik Rastgeleleştirme Fonksiyonları ===

def generate_android_id():
    return ''.join(random.choices('abcdef' + string.digits, k=16))

def generate_serial_no():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

# === Android Aygıt Ayarları ===

def get_android_id():
    return adb("shell settings get secure android_id")

def set_android_id(new_id):
    return adb(f"shell settings put secure android_id {new_id}")

def remount_system_rw():
    return adb("shell su -c 'mount -o remount,rw /system'")

def write_build_prop(line):
    """build.prop'a satır ekle (zaten varsa ekleme)."""
    check = adb(f"shell su -c \"grep '{line.split('=')[0]}' /system/build.prop\"")
    if not check:
        return adb(f"shell su -c \"echo '{line}' >> /system/build.prop\"")
    else:
        print("Zaten eklenmiş.")
        return check

def reboot_device():
    return adb("reboot")

# === Dokunmatik ===

def get_screen_size():
    out = adb("shell wm size")
    if "Physical size:" in out:
        try:
            width, height = map(int, out.split(":")[1].strip().split("x"))
            return width, height
        except:
            return 1080, 2400
    return 1080, 2400

def random_tap():
    width, height = get_screen_size()
    x = random.randint(int(width * 0.1), int(width * 0.9))
    y = random.randint(int(height * 0.1), int(height * 0.9))
    adb(f"shell input tap {x} {y}")
    print(f"📱 Rastgele tıklama: {x},{y}")

# === Gecikmeli Doğal Davranış ===

def human_delay(min_sec=1.5, max_sec=3.5):
    delay = round(random.uniform(min_sec, max_sec), 2)
    print(f"⏳ Bekleniyor: {delay} saniye...")
    time.sleep(delay)

# === Ana Fonksiyon ===

def main():
    print("🤖 LDPlayer Otomatik Spoof Başlatılıyor...")

    devices = adb("devices")
    print("🔌 Bağlı cihazlar:\n", devices)
    if "emulator" not in devices and "device" not in devices:
        print("🚫 Emülatör bağlı değil. ADB bağlantısını kontrol et.")
        return

    print("\n📎 Mevcut Android ID:", get_android_id())

    new_android_id = generate_android_id()
    new_serial_no = generate_serial_no()

    print(f"🆕 Yeni Android ID atanıyor: {new_android_id}")
    set_android_id(new_android_id)
    print("✅ Yeni Android ID:", get_android_id())

    human_delay()

    print("\n🛠️ build.prop düzenleniyor...")
    remount_system_rw()
    write_build_prop(f"ro.serialno={new_serial_no}")
    print(f"🆔 Serial No ayarlandı: {new_serial_no}")

    human_delay()

    print("🔁 Emülatör yeniden başlatılıyor...")
    reboot_device()

    print("⏳ 20 saniye bekleniyor (yeniden başlama)...")
    time.sleep(20)

    print("📲 Rastgele tıklama ile insan benzeri hareket simülasyonu...")
    for _ in range(random.randint(2, 4)):
        random_tap()
        human_delay(0.5, 1.2)

    print("\n✅ İşlem tamamlandı!")

if __name__ == "__main__":
    main()
