import cv2
import numpy as np

import cv2
import numpy as np
import subprocess
import cv2
import numpy as np
import subprocess

import cv2
import numpy as np
import subprocess

import cv2
import numpy as np
import subprocess

import cv2
import numpy as np
import subprocess

def opencv(template_path, threshold=0.7):
    try:
        # RAM'den ekran görüntüsü al
        raw_bytes = subprocess.check_output(["adb", "exec-out", "screencap", "-p"])
        img_array = np.frombuffer(raw_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            print("RAM'den ekran görüntüsü alınamadı!")
            return (1, 1)

        # Şablon yükle
        template = cv2.imread(template_path, 0)
        if template is None:
            print("Şablon yüklenemedi!")
            return (1, 1)

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = template.shape

        max_val = -1
        max_loc = None
        best_scale = 1.0

        for scale in np.linspace(0.5, 1.5, 30):
            resized = cv2.resize(template, (int(w * scale), int(h * scale)))
            res = cv2.matchTemplate(gray_img, resized, cv2.TM_CCOEFF_NORMED)
            _, current_val, _, current_loc = cv2.minMaxLoc(res)

            if current_val > max_val:
                max_val = current_val
                max_loc = current_loc
                best_scale = scale

        if max_val >= threshold:
            actual_x = max_loc[0]
            actual_y = max_loc[1]
            actual_w = int(w * best_scale)
            actual_h = int(h * best_scale)
            x2 = actual_x + actual_w
            y2 = actual_y + actual_h
            xdeger = int(round((actual_x + x2) / 2))
            ydeger = int(round((actual_y + y2) / 2))

            print(f"Doğru Koordinatlar: Sol-Üst ({actual_x}, {actual_y}), Sağ-Alt ({x2}, {y2}), Orta-Nokta({xdeger},{ydeger})")

            # Görselin üzerine dikdörtgen çiz
            cv2.rectangle(img, (actual_x, actual_y), (x2, y2), (0, 255, 0), 2)

            # Ekran çözünürlüğüne sığacak şekilde yeniden boyutla (örnek: 1080x2400 yerine orana göre)
            max_width = 540
            max_height = 960
            height, width = img.shape[:2]

            scale = min(max_width / width, max_height / height, 1.0)  # Orijinalden büyük gösterme
            new_size = (int(width * scale), int(height * scale))
            resized_img = cv2.resize(img, new_size)

            # Küçük pencere ile göster
            cv2.imshow("Tespit", resized_img)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

            return (xdeger, ydeger)
        else:
            print("Şablon bulunamadı.")
            return (1, 1)

    except subprocess.CalledProcessError as e:
        print(f"ADB hatası: {e}")
        return (1, 1)
    except Exception as e:
        print(f"Hata: {e}")
        return (1, 1)

# Kullanım
#xdeger , ydeger = opencv("screenshot.png", "ol.png", threshold=0.7)
 
#print(xdeger)
#print(ydeger)

import cv2
import numpy as np


import cv2
import numpy as np
import subprocess

def filter_close_points(points, min_distance=10):
    filtered = []
    for pt in points:
        if all(np.linalg.norm(np.array(pt) - np.array(fpt)) > min_distance for fpt in filtered):
            filtered.append(pt)
    return filtered

def opencv10(template_path, x0=None, y0=None, x1=None, y1=None, threshold=0.7, scale_factor=0.4):
    try:
        # RAM'den ekran görüntüsünü al
        raw_bytes = subprocess.check_output(["adb", "exec-out", "screencap", "-p"])
        img_array = np.frombuffer(raw_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            print("RAM'den ekran görüntüsü alınamadı!")
            return [1], [1]

        # Şablonu yükle
        template = cv2.imread(template_path, 0)
        if template is None:
            print("Şablon yüklenemedi!")
            return [1], [1]

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = template.shape

        # ROI varsa kırp
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
            resized_template = cv2.resize(template, (int(w * scale), int(h * scale)))
            res = cv2.matchTemplate(roi, resized_template, cv2.TM_CCOEFF_NORMED)

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
        found_locations.sort(key=lambda pt: pt[1])  # Y eksenine göre sırala

        if found_locations:
            print(f"Toplam bulunan şablon sayısı (filtrelenmiş): {len(found_locations)}")
            resized_roi = cv2.resize(
                roi_color,
                (int(roi_color.shape[1] * scale_factor), int(roi_color.shape[0] * scale_factor))
            )
            cv2.imshow("Sonuç (RAM'den görüntü)", resized_roi)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

            x_coords = [pt[0] for pt in found_locations]
            y_coords = [pt[1] for pt in found_locations]
            return x_coords, y_coords
        else:
            return [1], [1]

    except subprocess.CalledProcessError as e:
        print(f"ADB hatası: {e}")
        return [1], [1]
    except Exception as e:
        print(f"Hata: {e}")
        return [1], [1]







"""xdeger , ydeger = opencv.opencv10("screenshot.png", "yor.png", x0=0, y0=0, x1=1080, y1=1800, threshold=0.7)
fonksiyonlar.open_app_at_coordinates(xdeger[0],ydeger[0])"""






# Kullanım
# Tam ekran tarama
#opencv("screenshot.png", "ol.png", threshold=0.7)

# Belirli alan tarama
#opencv("screenshot.png", "ol.png", x0=100, y0=200, x1=800, y1=1500, threshold=0.7)
