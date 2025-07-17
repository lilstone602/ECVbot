import fonksiyonlar
import time
import keyokuyucu
import opencv 
import acıklamaal
import takip
import os
import time
import random
import fonksiyonlar



fonksiyonlar.baglan()
fonksiyonlar.open_arama()
time.sleep(2)
fonksiyonlar.open_arama_ara()
time.sleep(1)
keyokuyucu.readkey1("nazo")
time.sleep(12)
fonksiyonlar.open_app_at_coordinates(330,600)
time.sleep(4)


def kullanıcı_reels_begeni():
    adeger , bdeger = opencv.opencv("reelssimgesi.png", threshold=0.6) #olreel jpeg vardı
    fonksiyonlar.open_app_at_coordinates(adeger+200,bdeger)
    time.sleep(3)
    fonksiyonlar.open_app_at_coordinates(adeger,bdeger+100)
