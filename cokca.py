

from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import re
import opencv

def scale_coordinates(coords, orig_size, target_size):
    x1, y1, x2, y2 = coords
    orig_w, orig_h = orig_size
    target_w, target_h = target_size

    x1_scaled = int(x1 * target_w / orig_w)
    y1_scaled = int(y1 * target_h / orig_h)
    x2_scaled = int(x2 * target_w / orig_w)
    y2_scaled = int(y2 * target_h / orig_h)

    return (x1_scaled, y1_scaled, x2_scaled, y2_scaled)

def temizle_simge_hatalari(text):
    # Filtrelemeyi devre dışı bıraktım
    return text

def temizle_anlamsiz_rakamlar(text):
    # Filtrelemeyi devre dışı bıraktım
    return text

def crop_and_ocr(image_path, orig_coords, orig_size, show_cropped=True, lang='tur'):
    image = Image.open(image_path)
    target_size = image.size

    scaled_coords = scale_coordinates(orig_coords, orig_size, target_size)
    print("Ölçeklenmiş koordinatlar:", scaled_coords)

    cropped = image.crop(scaled_coords)

    if show_cropped:
        plt.imshow(cropped)
        plt.axis('off')
        plt.title("Ölçeklenmiş Kırpma Alanı")
        plt.pause(2)
        plt.close()

    text = pytesseract.image_to_string(cropped, lang=lang)

    # Satır sonlarını koruyarak izin verilen karakterler dışındakileri temizle
    text = re.sub(r"[^a-zA-Z0-9ğüşöçıİĞÜŞÖÇ.,!?()\-:;\"' \n]+", "", text)

    text = temizle_simge_hatalari(text)
    text = temizle_anlamsiz_rakamlar(text)

    return text

# Örnek kullanım
"""
image_path = "as.jpg"
orig_coords = (0, 1400, 1080, 2400)
orig_size = (1080, 2400)

ocr_text = crop_and_ocr(image_path, orig_coords, orig_size)
print("OCR Sonucu:\n", ocr_text)
"""



import fonksiyonlar
import opencv
import time
import acıklamaal



import cv2
import numpy as np

def sadece_beyaz_metni_al(image_path, output_path="screenshot.png"):
    img = cv2.imread(image_path)
    # BGR formatında beyaz aralığı - biraz toleransla
    lower = np.array([200, 200, 200])  # minimum beyaz (gri tonlar da dahil)
    upper = np.array([255, 255, 255])  # maksimum beyaz
    
    # Beyaz alanları maskele
    mask = cv2.inRange(img, lower, upper)
    
    # Siyah arka plan, beyaz yazı olarak ayarla
    result = cv2.bitwise_and(img, img, mask=mask)
    
    # İstersen griye çevir, OCR'a uygundur
    result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    
    # Arka planı tamamen siyah yapmak için
    _, thresh = cv2.threshold(result_gray, 1, 255, cv2.THRESH_BINARY)
    
    cv2.imwrite(output_path, thresh)
    return output_path



















import fonksiyonlar 
import time
import cv2
import numpy as np
import yazitespit
import os
import warnings

# Matplotlib uyarılarını gizle
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

def filter_close_points(points, min_distance=10):
    filtered = []
    for pt in points:
        if all(np.linalg.norm(np.array(pt) - np.array(fpt)) > min_distance for fpt in filtered):
            filtered.append(pt)
    return filtered

def openc(image_path, template_path, x0=None, y0=None, x1=None, y1=None, threshold=0.7, scale_factor=0.4):
    try:
        img = cv2.imread(image_path)
        if img is None:
            print("Görüntü yüklenemedi!")
            return [1], [1]
        
        template = cv2.imread(template_path, 0)
        if template is None:
            print("Şablon yüklenemedi!")
            return [1], [1]
        
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = template.shape
        
        if x0 is not None and y0 is not None and x1 is not None and y1 is not None:
            roi = gray_img[y0:y1, x0:x1]
            roi_color = img[y0:y1, x0:x1].copy()
            offset_x, offset_y = x0, y0
        else:
            roi = gray_img
            roi_color = img.copy()
            offset_x, offset_y = 0, 0
        
        found_locations = []
        for scale in np.linspace(0.5, 1.5, 30):
            resized = cv2.resize(template, (int(w*scale), int(h*scale)))
            res = cv2.matchTemplate(roi, resized, cv2.TM_CCOEFF_NORMED)
            
            y_coords, x_coords = np.where(res >= threshold)
            
            for (x, y) in zip(x_coords, y_coords):
                actual_x = x + offset_x
                actual_y = y + offset_y
                actual_w = int(w * scale)
                actual_h = int(h * scale)
                x_center = int(round((actual_x + actual_x + actual_w) / 2))
                y_center = int(round((actual_y + actual_y + actual_h) / 2))
                found_locations.append((x_center, y_center))
                
                cv2.rectangle(roi_color, (x, y), (x + actual_w, y + actual_h), (0, 255, 0), 2)
        
        # Yakın sonuçları filtrele
        found_locations = filter_close_points(found_locations, min_distance=10)

        # Sadece Y koordinatlarına göre sırala (X değerleri olduğu gibi kalır)
        found_locations.sort(key=lambda pt: pt[1])
        
        if found_locations:
            print(f"Toplam bulunan şablon sayısı (filtrelenmiş): {len(found_locations)}")
            resized_roi = cv2.resize(roi_color, (int(roi_color.shape[1] * scale_factor), int(roi_color.shape[0] * scale_factor)))
            cv2.imshow("Sonuç (Belirtilen Alan)", resized_roi)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            x_coords = [pt[0] for pt in found_locations]
            y_coords = [pt[1] for pt in found_locations]
            return x_coords, y_coords
        else:
            # Hiçbir eşleşme bulunamazsa 1,1 döndür
            return [1], [1]
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return [1], [1]

# Örnek kullanım



def reelsacıklamakaydedici():
    time.sleep(5)
    fonksiyonlar.swipe_down_small()
    time.sleep(1)
    fonksiyonlar.sil_dosya("screenshot.png")
    temelx0a = 0
    temely0a = 1000
    temelx1a = 1080
    temely1a = 1270

    temelx0x = 0
    temely0x = 1000
    temelx1x = 1080
    temely1x = 1270

    fonksiyonlar.take_screenshot_to_custom_folder("C:\\Users\\PasifikGaming\\Desktop\\instabot") 
    sadece_beyaz_metni_al("screenshot.png")
    adeger, bdeger = opencv("screenshot.png", "ol.png", x0=temelx0a, y0=temely0a-50, x1=temelx1a, y1=temely1a, threshold=0.7)
    print(adeger)
    print(bdeger)
    if(adeger[0]>1):
        xdeger, ydeger = opencv("screenshot.png", "yanitla.png", x0=temelx0x, y0=temely0x, x1=temelx1x, y1=temely1x, threshold=0.7)
        print(xdeger)
        print(ydeger)    
        if (xdeger[0]==1):
             temely1x= temely1x+100
             xdeger, ydeger = opencv("screenshot.png", "yanitla.png", x0=temelx0x, y0=temely0x, x1=temelx1x, y1=temely1x, threshold=0.7)
             print(xdeger)
             print(ydeger)
             if (xdeger[0]==1):
                 temely1x= temely1x+100
                 xdeger, ydeger = opencv("screenshot.png", "yanitla.png", x0=temelx0x, y0=temely0x, x1=temelx1x, y1=temely1x, threshold=0.7)
                 print(xdeger)
                 print(ydeger)
         
        if(bdeger[0]<ydeger[0]): 
            image_path = "screenshot.png"
            orig_coords = (temelx0x+180, bdeger[0], temelx1x-130, ydeger[0]-15)
            orig_size = (1080, 2400)
            ocr_text = yazitespit.crop_and_ocr(image_path, orig_coords, orig_size)
            print("OCR Sonucu:\n", ocr_text)        
           # ada = fonksiyonlar.clean_text_with_newlines(ocr_text)
          #  print("")
          #  print(ada)
         #   if (ada !=None):
             #   return ada
            if ocr_text.strip():
                return ocr_text.strip()
        
    else:
        time.sleep(0.5)           

    
def diziyeekle(kactane):
    ada = []
    for i in range(kactane):
        sonuc = reelsacıklamakaydedici()
        if sonuc is not None:  # None ise ekleme
            ada.append(sonuc)
            
            # Tek elemanlı NumPy dizisi oluşturma (isteğe bağlı)
            veri_dizisi = np.array([sonuc])
        
            print(veri_dizisi)
            print("Eleman Sayısı:", len(veri_dizisi))
        else:
            print(f"{i}. eleman None olduğu için eklenmedi.")
    return ada




def tane_acıklama(x,veri= "veri.npy"):
    # Eğer veri.npy dosyası varsa mevcut verileri yükle
    if os.path.exists(veri):
        mevcut_veriler = np.load(veri, allow_pickle=True).tolist()
    else:
        mevcut_veriler = []

    # Yeni verileri ekle
    yeni_veriler = diziyeekle(x)
    ada = mevcut_veriler + yeni_veriler

    # NumPy dizisi olarak kaydetme
    np.save(veri, np.array(ada, dtype=object))

    # Yükleme ve kontrol
    loaded_array = np.load(veri, allow_pickle=True)
    print("\nYüklenen Veriler:")
    print(loaded_array)
    return loaded_array
 

#veri eklenecek veri öyle bir dosya yoksa oluşturur


def verinpyread(veri= "veri.npy"):
    # .npy dosyasını yükle
    veriler = np.load(veri, allow_pickle=True)
 
    return veriler

#veri eklenecek veri öyle bir dosya yoksa oluşturur

def verisıfırla(veri= "veri.npy"):
    # Dosyayı sil
    os.remove(veri)
    # Yeni boş dosya oluştur
    np.save(veri, np.array([]))
    print(veri +" dosyası tamamen silindi ve boş olarak yeniden oluşturuldu.")
    
    #veri eklenecek veri öyle bir dosya yoksa oluşturur
    
    
#örnek kullanım
"""
acıklamaal.verisıfırla()
s = acıklamaal.tane_acıklama(5)
a = acıklamaal.verinpyread()
print(a[1])
print(a)"""

import opencv
def yorumop4():
    fonksiyonlar.take_screenshot_to_custom_folder("C:\\Users\\PasifikGaming\\Desktop\\instabot") 
    xdeger , ydeger = opencv.opencv10("screenshot.png", "yor.png", x0=0, y0=0, x1=1080, y1=2000, threshold=0.7)
    fonksiyonlar.sil_dosya("screenshot.png")
    print("yorum")
    if(xdeger[0]>1):
        fonksiyonlar.open_app_at_coordinates(xdeger[0],ydeger[0])
        time.sleep(1)
        verisıfırla()
        time.sleep(1)
        asasa = tane_acıklama(5)
        a = verinpyread()
        print(a[1])
        print(a)
        time.sleep(1)
        fonksiyonlar.back()
        time.sleep(2)
        return 4
    else:
        return 0
    
fonksiyonlar.baglan()
yorumop4()