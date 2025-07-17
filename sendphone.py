import os
import subprocess
import shlex
import fonksiyonlar

def push_video_to_android(local_video_path, device_target_path="/sdcard/DCIM/Job/"):
    # Dosya yolunun geçerli olup olmadığını kontrol et
    if not os.path.isfile(local_video_path):
        print(f"Hata: '{local_video_path}' dosyası bulunamadı.")
        return

    # Dosya adını al
    video_filename = os.path.basename(local_video_path)
    # Hedef yolu oluştur
    device_full_path = device_target_path.rstrip('/') + '/' + video_filename

    # ADB push komutunu oluştur
    push_command = f'adb push "{local_video_path}" "{device_full_path}"'
    print(f"ADB Komutu: {push_command}")

    try:
        # Komutu çalıştır
        result = subprocess.run(shlex.split(push_command), capture_output=True, text=True)

        # Komutun çıktısını kontrol et
        if result.returncode == 0:
            print(f"✅ Video başarıyla gönderildi: {device_full_path}")
        else:
            print(f"❌ Hata oluştu:\n{result.stderr}")
            return

        # Medya tarayıcısını güncelle
        scan_command = f'adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:{device_full_path}'
        subprocess.run(shlex.split(scan_command), capture_output=True, text=True)
        print("📂 Medya tarayıcısı güncellendi.")

    except Exception as e:
        print(f"⚠️ İstisna oluştu: {e}")

# Kullanım örneği
#push_video_to_android("C:/Users/PasifikGaming/Desktop/out/processed_da.mp4")