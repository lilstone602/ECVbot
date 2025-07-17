import fonksiyonlar
import time
import opencv
import videoconverter
import sendphone
import keyokuyucu
import acıklamaal


def uploadreels():
    a="C:\\Users\\PasifikGaming\\Desktop\\instabot\\input"
    b="C:\\Users\\PasifikGaming\\Desktop\\instabot"
    videoconverter.video_converter(a,b)
    sendphone.push_video_to_android("C:/Users/PasifikGaming/Desktop/instabot/processed_name.mp4")
    fonksiyonlar.open_profil()
    time.sleep(1)
    fonksiyonlar.open_anasayfa()
    time.sleep(1)
    fonksiyonlar.open_profil()
    time.sleep(1)
    fonksiyonlar.open_app_at_coordinates(850,180)    
    time.sleep(1)
    fonksiyonlar.take_screenshot_to_custom_folder("C:\\Users\\PasifikGaming\\Desktop\\instabot") 
    xdeger , ydeger = opencv.opencv("screenshot.png", "instaupreels.png", threshold=0.7)
    fonksiyonlar.sil_dosya("screenshot.png")
    time.sleep(1)
    fonksiyonlar.open_app_at_coordinates(xdeger,ydeger)
    time.sleep(2)
    fonksiyonlar.take_screenshot_to_custom_folder("C:\\Users\\PasifikGaming\\Desktop\\instabot") 
    xdeger , ydeger = opencv.opencv("screenshot.png", "protect.png", threshold=0.7)
    fonksiyonlar.sil_dosya("screenshot.png")
    if (xdeger>1):
        fonksiyonlar.open_app_at_coordinates(xdeger,ydeger)
        time.sleep(2)
        fonksiyonlar.open_app_at_coordinates(550,940) 
        time.sleep(2)
    fonksiyonlar.open_app_at_coordinates(550,940) 
    time.sleep(2)
    fonksiyonlar.take_screenshot_to_custom_folder("C:\\Users\\PasifikGaming\\Desktop\\instabot") 
    xdeger , ydeger = opencv.opencv("screenshot.png", "tamam.jpeg", threshold=0.7)
    fonksiyonlar.sil_dosya("screenshot.png")
    if (xdeger>1):
        fonksiyonlar.open_app_at_coordinates(xdeger,ydeger)
        time.sleep(1)
    fonksiyonlar.open_app_at_coordinates(950,2200)
    time.sleep(2)
    fonksiyonlar.open_app_at_coordinates(300,1220)
    time.sleep(2)
    """burası açıklama kısmı bura geliştirilecek ve yeni fonksiyonlar eklenecek veri tabanı düzenlemesi gerekli tahminen"""
    a = acıklamaal.verinpyread()
    keyokuyucu.readkey(a[1])
    """"bu aralık"""
    time.sleep(1)
    fonksiyonlar.back()
    time.sleep(2)
    #fonksiyonlar.open_app_at_coordinates(800,2120)
    time.sleep(1)
    fonksiyonlar.take_screenshot_to_custom_folder("C:\\Users\\PasifikGaming\\Desktop\\instabot") 
    xdeger , ydeger = opencv.opencv("screenshot.png", "paylas.png", threshold=0.7)
    fonksiyonlar.sil_dosya("screenshot.png")
    if (xdeger>1):
        fonksiyonlar.open_app_at_coordinates(xdeger,ydeger)
        time.sleep(2)
    
    fonksiyonlar.sil_dosya("thumbnail_name.jpg")
    fonksiyonlar.sil_dosya("processed_name.mp4")
 

#tam detaylarına inilmedi hata kontrol dene ve bunun için ilgili sayıda veri kümesi ve etiket oluştur

uploadreels()