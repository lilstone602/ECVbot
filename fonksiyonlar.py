import adbutils
import subprocess
import time
import random
import cv2
import numpy as np
import os
import re
import takip
import acıklamaal
import keyokuyucu

# Bu kodun bulunduğu dosya nerede çalışıyorsa orayı al
base = os.path.dirname(os.path.abspath(__file__)) 

# Ekranı uyandırmak için ADB komutunu tanımla
def wake_up_screen():
    command = "adb shell input keyevent 26"  # Ekranı uyandırmak için
    try:
        # Komutu çalıştır
        subprocess.run(command, shell=True, check=True)
        print("Ekran başarıyla uyandırıldı!")
    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e}")


def sleep_screen():
    command = "adb shell input keyevent 223"  # Ekranı uyutmak için
    try:
        subprocess.run(command, shell=True, check=True)
        print("Ekran başarıyla uyutuldu!")
    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e}")


def swipe_up():
    # Aşağıdan yukarı kaydırma komutu
    start_x = 540  # Ekranın ortası (X koordinatı)
    start_y = 1600  # Ekranın altı (Y koordinatı)
    end_x = 540  # Ekranın ortası (X koordinatı)
    end_y = 300  # Ekranın üstü (Y koordinatı)
    duration = 500  # Kaydırma süresi (ms)

    command = f"adb shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Aşağıdan yukarı kaydırma yapıldı!")
    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e}")

# Kaydırma işlemini başlat
# kaydırma komudu swipe_up()


# Uygulamanın ikonu üzerindeki koordinatlara tıklamak için ADB komutunu tanımla
def open_app_at_coordinates(x, y):
    command = f"adb shell input tap {x} {y}"  # Belirtilen koordinatlara tıkla
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Uygulamaya {x}, {y} koordinatlarına tıklanarak giriş yapıldı!")
    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e}")
    

# Uygulamanın koordinatlarını belirle ve fonksiyonu çalıştır

def dokunma_koruma():
    random_number = random.randint(1,5)
    if random_number==1:
        random_number_2 = random.randint(12,40)
    if random_number==2:
        random_number_2 = random.randint(2,30)
    if random_number==3:
        random_number_2 = random.randint(12,30)
    if random_number==4:
        random_number_2 = random.randint(2,20)
    if random_number==5:
        random_number_2 = random.randint(4,10)
    return random_number_2

def dokunma_koruma2():
    random_number = random.randint(1,5)
    if random_number==1:
        random_number_2 = random.randint(5,13)
    if random_number==2:
        random_number_2 = random.randint(2,12)
    if random_number==3:
        random_number_2 = random.randint(12,20)
    if random_number==4:
        random_number_2 = random.randint(6,10)
    if random_number==5:
        random_number_2 = random.randint(4,10)
    return random_number_2

def dokunma_koruma3():
    random_number = random.randint(1,2)
    if random_number==1:
        random_number_2 = random.randint(1,3)
    if random_number==2:
        random_number_2 = random.randint(1,3)    
    return random_number_2

def insta_like(x,y):
    a = x + dokunma_koruma()
    b = y + dokunma_koruma()
    c = x + dokunma_koruma2()
    d = y + dokunma_koruma2()
    e = dokunma_koruma3()
    f = e/100
    open_app_at_coordinates(a,b)
    time.sleep(f)
    open_app_at_coordinates(c,d)
    

def swipe_up_natural():
    # Ekranda kaydırma yapacak başlangıç ve bitiş koordinatları
    start_x = 540  # Ekranın ortası (X koordinatı)
    start_y = 1900  # Ekranın alt kısmı (Y koordinatı)
    end_x = 540  # Ekranın ortası (X koordinatı)
    end_y = 300  # Ekranın üst kısmı (Y koordinatı)
    
    # Kaydırma süresi ve adım sayısı
    total_duration = random.randint(800, 1500)  # Kaydırma süresi (ms), rastgele bir süre
    steps = random.randint(1, 5)  # Kaydırma adım sayısı, daha doğal bir kaydırma için

    step_y = (start_y - end_y) / steps  # Y eksenindeki her adım uzunluğu
    step_duration = total_duration / steps  # Her adım için süre

    # İnsan hareketi simülasyonu için X ve Y ekseninde küçük sapmalar
    for i in range(steps):
        # X ve Y ekseninde küçük rastgele sapmalar
        random_variation_x = random.randint(-10, 10)  # X eksenindeki küçük sapmalar
        random_variation_y = random.randint(-5, 5)   # Y eksenindeki küçük sapmalar

        new_x = start_x + random_variation_x  # Yeni X koordinatı
        new_y = start_y - (i * step_y) + random_variation_y  # Yeni Y koordinatı (adım adım)

        # ADB komutunu oluştur
        command = f"adb shell input swipe {new_x} {new_y} {new_x} {new_y + step_y} {int(step_duration)}"
        
        # ADB komutunu çalıştır
        try:
            subprocess.run(command, shell=True, check=True)
            time.sleep(step_duration / 1000)  # Her adımda kısa bir bekleme
        except subprocess.CalledProcessError as e:
            print(f"Hata oluştu: {e}")
        
        # Arada rastgele duraklamalar ekleyerek hız çeşitliliği oluşturuyoruz
        if random.random() < 0.2:  # %20 ihtimalle duraklama
            time.sleep(random.uniform(0.2, 1.0))  # Duraklama süresi rastgele (0.2 ile 1 saniye arasında)

    print("Doğal kaydırma işlemi tamamlandı!")


def swipe_down_natural():
    # Ekranda kaydırma yapacak başlangıç ve bitiş koordinatları
    start_x = 540  # Ekranın ortası (X koordinatı)
    start_y = 300  # Ekranın alt kısmı (Y koordinatı)
    end_x = 540  # Ekranın ortası (X koordinatı)
    end_y = 1900  # Ekranın üst kısmı (Y koordinatı)
    
    # Kaydırma süresi ve adım sayısı
    total_duration = random.randint(800, 1500)  # Kaydırma süresi (ms), rastgele bir süre
    steps = random.randint(1, 5)  # Kaydırma adım sayısı, daha doğal bir kaydırma için

    step_y = (start_y - end_y) / steps  # Y eksenindeki her adım uzunluğu
    step_duration = total_duration / steps  # Her adım için süre

    # İnsan hareketi simülasyonu için X ve Y ekseninde küçük sapmalar
    for i in range(steps):
        # X ve Y ekseninde küçük rastgele sapmalar
        random_variation_x = random.randint(-10, 10)  # X eksenindeki küçük sapmalar
        random_variation_y = random.randint(-5, 5)   # Y eksenindeki küçük sapmalar

        new_x = start_x + random_variation_x  # Yeni X koordinatı
        new_y = start_y - (i * step_y) + random_variation_y  # Yeni Y koordinatı (adım adım)

        # ADB komutunu oluştur
        command = f"adb shell input swipe {new_x} {new_y} {new_x} {new_y + step_y} {int(step_duration)}"
        
        # ADB komutunu çalıştır
        try:
            subprocess.run(command, shell=True, check=True)
            time.sleep(step_duration / 1000)  # Her adımda kısa bir bekleme
        except subprocess.CalledProcessError as e:
            print(f"Hata oluştu: {e}")
        
        # Arada rastgele duraklamalar ekleyerek hız çeşitliliği oluşturuyoruz
        if random.random() < 0.2:  # %20 ihtimalle duraklama
            time.sleep(random.uniform(0.2, 1.0))  # Duraklama süresi rastgele (0.2 ile 1 saniye arasında)

    print("Doğal kaydırma işlemi tamamlandı!")

def take_screenshot_to_custom_folder():
    import subprocess
    import numpy as np
    import cv2

    try:
        raw_bytes = subprocess.check_output(["adb", "exec-out", "screencap", "-p"])
        img_array = np.frombuffer(raw_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            print("Hata: Ekran görüntüsü çözümlenemedi!")
        return img
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None



def detect_heart(image_path, template_path, threshold=0.7):
    # Görüntüyü orijinal haliyle yükle
    img = cv2.imread(image_path)
    if img is None:
        print("Görüntü yüklenemedi!")
        return None
    
    # Şablonu gri tonlamalı yükle
    template = cv2.imread(template_path, 0)
    if template is None:
        print("Şablon yüklenemedi!")
        return None
    
    # Görüntüyü griye çevir
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = template.shape
    
    # Multi-scale arama
    max_val = -1
    max_loc = None
    best_scale = 1.0
    
    for scale in np.linspace(0.5, 1.5, 30):
        resized = cv2.resize(template, (int(w*scale), int(h*scale)))
        res = cv2.matchTemplate(gray_img, resized, cv2.TM_CCOEFF_NORMED)
        _, current_val, _, current_loc = cv2.minMaxLoc(res)
        
        if current_val > max_val:
            max_val = current_val
            max_loc = current_loc
            best_scale = scale
    
    if max_val >= threshold:
        # Düzeltilmiş Y koordinatı için görüntü yüksekliğini kullan
        img_height = img.shape[0]
        x = max_loc[0]
        y = max_loc[1]
        
        # Y koordinatını düzelt (OpenCV'de üst sol (0,0) noktasıdır)
        actual_y = y
        actual_x = x
        
        # Gerçek boyutlar
        actual_w = int(w * best_scale)
        actual_h = int(h * best_scale)
        
        # Sağ alt köşe koordinatları
        x2 = actual_x + actual_w
        y2 = actual_y + actual_h
        xdeger = int(round((actual_x + x2)/2))
        ydeger = int(round((actual_y + y2)/2))
        print(f"Doğru Koordinatlar: Sol-Üst ({actual_x}, {actual_y}), Sağ-Alt ({x2}, {y2}), Orta-Nokta({xdeger},{ydeger})")
        
        # Görsel doğrulama (yeşil kutu)
        cv2.rectangle(img, (actual_x, actual_y), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("Düzeltilmiş Kalp Tespiti", img)
        cv2.waitKey(5000)  #bekleme süresi
        cv2.destroyAllWindows()
        
        
       
        
        return (xdeger, ydeger)
    else:
        print("Kalp bulunamadı.")
        return None


def sil_dosya(dosya_yolu):
    """
    Verilen dosya yolundaki dosyayı siler.
    
    Parametre:
    dosya_yolu (str): Silinmek istenen dosyanın tam yolu.
    
    Dönüş:
    - Başarılı olursa dosya silindi mesajı döndürür.
    - Hata durumunda uygun hata mesajı döndürür.
    """
    try:
        os.remove(dosya_yolu)
        print(f"'{dosya_yolu}' başarıyla silindi.")
    except FileNotFoundError:
        print(f"'{dosya_yolu}' bulunamadı.")
    except PermissionError:
        print(f"'{dosya_yolu}' dosyasını silmek için yeterli izin yok.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")


def begenen_görüntüle(x,y):
    open_app_at_coordinates(x+100,y)
    
    
def sleep():
   open_app_at_coordinates(550, 2300)  
   print("sleep**")

   time.sleep(1)

   sleep_screen()
   
  
def fixdetect_heart(dosya, simge, threshold=0.7):
    # Simgeyi bulmaya çalış
    result = detect_heart(dosya, simge, threshold) or (None, None)
    
    # Sonucu kontrol et
    xdeger, ydeger = result
    if xdeger is not None and ydeger is not None:
        print(f"Bulunan koordinatlar: x={xdeger}, y={ydeger}")
        return xdeger, ydeger
    else:
        print("Simge bulunamadı, diğer işlemlere devam ediliyor...")
        return None, None
    
       
def open_anasayfa():
    open_app_at_coordinates(110,2300)
    
def open_arama_ara():
    open_app_at_coordinates(330,180)
        
def open_arama():
    open_app_at_coordinates(330,2300)
        
def open_reels():
    open_app_at_coordinates(770,2300)
    
def open_profil():
    open_app_at_coordinates(960,2300)            
    
       
def baglan():
        # ADB client oluşturma
    client = adbutils.AdbClient(host="127.0.0.1", port=5037)

    # Bağlı cihazları listele
    devices = client.device_list()
    if len(devices) == 0:
        print("Cihaz bulunamadı.")
    else:
        print("Bağlı cihazlar:")
        for device in devices:
            print(f"- {device.serial}")

    # Cihaza komut gönderme
        device = devices[0]
       
               
def open_instagram():
    open_app_at_coordinates(150,260)        
    

def open_upload():
    open_app_at_coordinates(535,2200)
    
    
def open_insta_search_button():   
    open_app_at_coordinates(500,200)
    
    
def back():
    subprocess.run("adb shell input keyevent 4", shell=True)
    
    
def swipe_down_small():
    # Aşağıdan yukarı kaydırma komutu
    start_x = 540  # Ekranın ortası (X koordinatı)
    start_y = 1450  # Ekranın altı (Y koordinatı)
    end_x = 540  # Ekranın ortası (X koordinatı)
    end_y = 1300  # Ekranın üstü (Y koordinatı)
    duration = 500  # Kaydırma süresi (ms)

    command = f"adb shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Aşağıdan yukarı kaydırma yapıldı!")
    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e}")    
        
        
def clean_text_with_newlines(text):
    # Sadece istenen karakterleri bırak ve satır sonlarını koru
    cleaned_text = re.sub(r"[^a-zA-Z0çğıöşüÇĞIİÖŞÜ., \n]", "", text)
    
    # Satır sonlarını daha okunabilir yapmak için çift boşlukları tek boşluğa indir
    cleaned_text = re.sub(r" +", " ", cleaned_text)
    
    # Her satırın sonunda mutlaka bir boşluk bırak
    cleaned_text = re.sub(r"(\S)\n(\S)", r"\1 \2", cleaned_text)

    return cleaned_text

# Örnek kullanım

#filtered_text = clean_text_with_newlines(text)
#print(filtered_text)
        
        
def yanakaydır():
    start_x = 605  # Ekranın ortası (X koordinatı)
    start_y = 500  # Ekranın altı (Y koordinatı)
    end_x = 350  # Ekranın ortası (X koordinatı)
    end_y = 400  # Ekranın üstü (Y koordinatı)
    duration = 500  # Kaydırma süresi (ms)

    command = f"adb shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Aşağıdan yukarı kaydırma yapıldı!")
    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e}")          
    
    
def swipe_down_mid():
    # Aşağıdan yukarı kaydırma komutu
    start_x = 540  # Ekranın ortası (X koordinatı)
    start_y = 1750  # Ekranın altı (Y koordinatı)
    end_x = 540  # Ekranın ortası (X koordinatı)
    end_y = 1300  # Ekranın üstü (Y koordinatı)
    duration = 500  # Kaydırma süresi (ms)

    command = f"adb shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Aşağıdan yukarı kaydırma yapıldı!")
    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e}")   

    
def takipcibul(xdeger,ydeger):
    open_app_at_coordinates(xdeger,ydeger+80)
    
def enter():
    subprocess.run(["adb", "shell", "input", "keyevent", "66"])    
    import os
import subprocess
from PIL import Image

def take_screenshot_to_custom_folder1(base=None):
    # Ekran görüntüsünü ve kesilmiş halini nereye kaydedeceğini belirle
    folder_path = os.path.dirname(os.path.abspath(__file__))

    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Dosya yolları
        full_screenshot = os.path.join(folder_path, "screenshot.png")
        cropped_screenshot = os.path.join(folder_path, "screenshot2.png")

        # 1. ADB ile ekran görüntüsü al
        subprocess.run("adb shell screencap -p /sdcard/screenshot.png", shell=True, check=True)
        subprocess.run(f'adb pull /sdcard/screenshot.png "{full_screenshot}"', shell=True, check=True)

        print(f"Ekran görüntüsü alındı: {full_screenshot}")

        # 2. İstenen bölgeyi kes
        # 📌 Koordinatları burada ayarla (x, y, genişlik, yükseklik)
        x = 300
        y = 120
        width = 450
        height = 100

        # 3. Pillow ile kırpma
        with Image.open(full_screenshot) as img:
            cropped = img.crop((x, y, x + width, y + height))
            cropped.save(cropped_screenshot)
            print(f"Kesilen görüntü kaydedildi: {cropped_screenshot}")

    except subprocess.CalledProcessError as e:
        print(f"ADB hatası oluştu: {e}")
    except Exception as e:
        print(f"Genel hata: {e}")
        sil_dosya("screenshot.png")




def ara_takip(kullanıcıverisi):
    os.system(f'adb shell am start -a android.intent.action.VIEW -d "https://instagram.com/{kullanıcıverisi}"')
    time.sleep(2)
    takip.enüsttakipet()

def kullanıcıprofili(kullanıcıverisi):
    open_arama()
    time.sleep(2)
    open_arama_ara()
    time.sleep(1)
    keyokuyucu.readkey1(kullanıcıverisi)
    time.sleep(12)
    open_app_at_coordinates(330,600)
    time.sleep(4)

    
def bekle(a,b):
    c = random.uniform(a,b)
    time.sleep(c)
    
def enüsttakipet():
    adeger , bdeger = acıklamaal.opencv(template_path="takip.png", threshold=0.9) #olreel jpeg vardı
    b = len(adeger)
    a = 0
    k = random.randint(1,5)
    if(adeger[a]>1):
        open_app_at_coordinates(adeger[a],bdeger[a])    