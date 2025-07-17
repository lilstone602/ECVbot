import os
import random
import subprocess


def video_converter(INPUT_DIR, OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 🎨 Video Özellikleri
    RESOLUTIONS = [(1080, 1920), (720, 1280), (640, 1136)]
    FPS_OPTIONS = [24, 25, 30, 60]
    COLOR_FILTERS = ["eq=contrast=1.1:brightness=0.05", "eq=contrast=0.9:brightness=-0.05"]

    # 🔄 Hash Değiştirme Fonksiyonu
    def change_file_hash(file_path):
        with open(file_path, 'ab') as f:
            # Dosyanın sonuna rastgele bir byte ekleyerek hash'i değiştiriyoruz
            f.write(os.urandom(1))

    # 🎥 Video İşleme
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith('.mp4'):
            # Video Yükleme
            video_path = os.path.join(INPUT_DIR, filename)
            output_file = os.path.join(OUTPUT_DIR, f"processed_{filename}")
            thumbnail_file = os.path.join(OUTPUT_DIR, f"thumbnail_{os.path.splitext(filename)[0]}.jpg")
            
            # 📐 Çözünürlük ve FPS Değiştirme
            resolution = random.choice(RESOLUTIONS)
            fps = random.choice(FPS_OPTIONS)
            
            # 🎨 Renk Ayarları
            color_filter = random.choice(COLOR_FILTERS)
            
            # 🔄 Ayna Efekti (Yatay)
            mirror = False
            mirror_filter = "hflip," if mirror else ""
            
            # 🛠️ FFmpeg Komutu
            command = [
                "ffmpeg", "-i", video_path,
                "-vf", f"{mirror_filter}scale={resolution[0]}:{resolution[1]},{color_filter}",
                "-r", str(fps),
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                output_file
            ]
            
            # 🎞️ Kapak Fotoğrafı Çekme Komutu (320x480)
            thumbnail_command = [
                "ffmpeg", "-i", video_path,
                "-ss", "00:00:00.000",
                "-vframes", "1",
                "-vf", "scale=320:480",
                thumbnail_file
            ]
            
            # Komutları Çalıştır
            try:
                subprocess.run(command, check=True)
                subprocess.run(thumbnail_command, check=True)
                # 🔄 Hash Değiştirme
                change_file_hash(output_file)
                print(f"✅ İşlendi: {filename} - Kapak: {thumbnail_file}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Hata: {filename} - {e}")
    
    print("✅ Tüm videolar başarıyla benzersizleştirildi!")

    
    
    
    
#a="C:\\Users\\PasifikGaming\\Desktop\\input"
#b="C:\\Users\\PasifikGaming\\Desktop\\out"
    
    
#video_converter(a,b)