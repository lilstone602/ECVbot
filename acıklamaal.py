import fonksiyonlar 
import time
import cv2
import numpy as np
import yazitespit
import os
import warnings
from PIL import Image
import io
import subprocess

# Matplotlib uyarılarını gizle
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

def filter_close_points(points, min_distance=10):
    filtered = []
    for pt in points:
        if all(np.linalg.norm(np.array(pt) - np.array(fpt)) > min_distance for fpt in filtered):
            filtered.append(pt)
    return filtered

def opencv(img=None, img_path=None, template_path=None, x0=None, y0=None, x1=None, y1=None, threshold=0.7, scale_factor=0.4):
    try:
        # 📌 Görüntüyü belirle
        if img is not None:
            if not isinstance(img, np.ndarray):
                print("img bir NumPy array değil")
                return [1], [1]
        elif img_path is not None:
            img = cv2.imread(img_path)
            if img is None:
                print("Verilen resim dosyası yüklenemedi!")
                return [1], [1]
        else:
            result = subprocess.run("adb exec-out screencap -p", shell=True, stdout=subprocess.PIPE)
            if result.returncode != 0:
                print("ADB ekran görüntüsü alınamadı!")
                return [1], [1]
            img_pil = Image.open(io.BytesIO(result.stdout))
            img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        # 📌 Template yükle
        if template_path is None:
            print("Şablon dosya yolu verilmedi!")
            return [1], [1]

        template = cv2.imread(template_path, 0)
        if template is None:
            print("Şablon yüklenemedi!")
            return [1], [1]

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = template.shape

        # 📌 ROI alanı belirle, negatif indeksleri engelle
        if x0 is not None and y0 is not None and x1 is not None and y1 is not None:
            x0 = max(0, x0)
            y0 = max(0, y0)
            roi = gray_img[y0:y1, x0:x1]
            roi_color = img[y0:y1, x0:x1].copy()
            offset_x, offset_y = x0, y0
        else:
            roi = gray_img
            roi_color = img.copy()
            offset_x, offset_y = 0, 0

        found_locations = []
        for scale in np.linspace(0.5, 1.5, 30):
            resized_w = int(w * scale)
            resized_h = int(h * scale)
            if resized_w <= 0 or resized_h <= 0:
                continue
            resized = cv2.resize(template, (resized_w, resized_h))

            # Şablon ROI'den büyükse atla
            if roi.shape[0] < resized_h or roi.shape[1] < resized_w:
                continue

            res = cv2.matchTemplate(roi, resized, cv2.TM_CCOEFF_NORMED)
            y_coords, x_coords = np.where(res >= threshold)

            for (x, y) in zip(x_coords, y_coords):
                actual_x = x + offset_x
                actual_y = y + offset_y
                actual_w = resized_w
                actual_h = resized_h
                x_center = int(round((actual_x + actual_x + actual_w) / 2))
                y_center = int(round((actual_y + actual_y + actual_h) / 2))
                found_locations.append((x_center, y_center))

                cv2.rectangle(roi_color, (x, y), (x + actual_w, y + actual_h), (0, 255, 0), 2)

        found_locations = filter_close_points(found_locations, min_distance=10)
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
            return [1], [1]

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return [1], [1]


def sadece_beyaz_metni_al(img):
    # img direkt numpy array olmalı
    if img is None:
        print("Boş görüntü verildi.")
        return None

    lower = np.array([200, 200, 200])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(img, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(result_gray, 1, 255, cv2.THRESH_BINARY)
    return thresh



def reelsacıklamakaydedici():
    time.sleep(2)
    fonksiyonlar.swipe_down_small()
    time.sleep(1)
    temelx0a = 0
    temely0a = 1200
    temelx1a = 1080
    temely1a = 1400

    temelx0x = 0
    temely0x = 1200
    temelx1x = 1080
    temely1x = 1500
    
    img = fonksiyonlar.take_screenshot_to_custom_folder()
    adeger, bdeger = opencv(img=img, template_path="kalpyorum.png", x0=temelx0a, y0=temely0a - 50, x1=temelx1a, y1=temely1a, threshold=0.7)
    print(adeger)
    print(bdeger)
    if adeger[0] > 1:
        xdeger, ydeger = opencv(img=img, template_path="yanitla.png", x0=temelx0x, y0=temely0x, x1=temelx1x, y1=temely1x, threshold=0.7)
        print(xdeger)
        print(ydeger)    
        if xdeger[0] == 1:
            temely1x = temely1x + 100
            xdeger, ydeger = opencv(img=img, template_path="yanitla.png", x0=temelx0x, y0=temely0x, x1=temelx1x, y1=temely1x, threshold=0.7)
            print(xdeger)
            print(ydeger)
            if xdeger[0] == 1:
                temely1x = temely1x + 100
                xdeger, ydeger = opencv(img=img, template_path="yanitla.png", x0=temelx0x, y0=temely0x, x1=temelx1x, y1=temely1x, threshold=0.7)
                print(xdeger)
                print(ydeger)
         
        if bdeger[0] < ydeger[0]: 
            thresh = sadece_beyaz_metni_al(img)
            orig_coords = (temelx0x + 180, bdeger[0], temelx1x - 130, ydeger[0] - 15)
            orig_size = (1080, 2400)
            ocr_text = yazitespit.crop_and_ocr(thresh, orig_coords, orig_size)
            print("OCR Sonucu:\n", ocr_text)       
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
            veri_dizisi = np.array([sonuc])  # isteğe bağlı
            print(veri_dizisi)
            print("Eleman Sayısı:", len(veri_dizisi))
        else:
            print(f"{i}. eleman None olduğu için eklenmedi.")
    return ada


def tane_acıklama(x, veri="veri.npy"):
    if os.path.exists(veri):
        mevcut_veriler = np.load(veri, allow_pickle=True).tolist()
    else:
        mevcut_veriler = []

    yeni_veriler = diziyeekle(x)
    ada = mevcut_veriler + yeni_veriler
    np.save(veri, np.array(ada, dtype=object))

    loaded_array = np.load(veri, allow_pickle=True)
    print("\nYüklenen Veriler:")
    print(loaded_array)
    return loaded_array


def verinpyread(veri="veri.npy"):
    veriler = np.load(veri, allow_pickle=True)
    return veriler


def verisıfırla(veri="veri.npy"):
    if os.path.exists(veri):
        os.remove(veri)
    np.save(veri, np.array([]))
    print(veri + " dosyası tamamen silindi ve boş olarak yeniden oluşturuldu.")
