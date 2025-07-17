import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pytesseract
import re
import time

# --- Yazitespit modülünden fonksiyon ---
def scale_coordinates(coords, orig_size, target_size):
    x1, y1, x2, y2 = coords
    orig_w, orig_h = orig_size
    target_w, target_h = target_size

    x1_scaled = int(x1 * target_w / orig_w)
    y1_scaled = int(y1 * target_h / orig_h)
    x2_scaled = int(x2 * target_w / orig_w)
    y2_scaled = int(y2 * target_h / orig_h)

    return (x1_scaled, y1_scaled, x2_scaled, y2_scaled)

SIMGE_HATALARI = ["vvu", "uuv", "vvv", "vv", "uu", "000", "111", "222", "333", "444", "555", "666", "777", "888", "999"]

def temizle_simge_hatalari(text):
    for hata in SIMGE_HATALARI:
        text = text.replace(hata, "")
    return text.strip()

def temizle_anlamsiz_rakamlar(text):
    text = re.sub(r'(\d)\1{2,}', '', text)
    return text.strip()

def crop_and_ocr(image, orig_coords, orig_size, show_cropped=False, lang='tur'):
    # image numpy array veya PIL.Image olabilir
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

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
    text = re.sub(r"[^a-zA-Z0-9ğüşöçıİĞÜŞÖÇ.,!?()\-:;\"' \n]+", "", text)
    text = temizle_simge_hatalari(text)
    text = temizle_anlamsiz_rakamlar(text)

    return text


# --- Senin sadece beyaz metni alma fonksiyonun ---
def sadece_beyaz_metni_al(img):
    lower = np.array([200, 200, 200])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(img, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(result_gray, 1, 255, cv2.THRESH_BINARY)
    return thresh

"""
# --- Örnek kullanım ---
if __name__ == "__main__":
    # Örnek ekran görüntüsü al, burada kendi koduna göre değiştir
    # img = fonksiyonlar.take_screenshot_to_custom_folder()

    # Örnek: Dosyadan oku
    img = cv2.imread("ornek_screenshot.png")  # BGR formatında

    if img is None:
        print("Resim bulunamadı!")
        exit()

    thresh = sadece_beyaz_metni_al(img)

    # OCR yapılacak bölge koordinatları ve orijinal resim boyutu
    orig_coords = (180, 1400, 950, 2000)  # Örnek, kendi ihtiyacına göre ayarla
    orig_size = (1080, 2400)  # Orijinal ekran boyutu

    # OCR yap, grafik göstermeden
    ocr_text = crop_and_ocr(thresh, orig_coords, orig_size, show_cropped=False)

    print("OCR Sonucu:\n", ocr_text)"""
