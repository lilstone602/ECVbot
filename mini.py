import fonksiyonlar 
import time
import opencv
import random 
import acıklamaal
import keyokuyucu
import takip
import os

def begen1():
    fonksiyonlar.insta_like(550,1100)
    
    return 1 

def azkay2():
    fonksiyonlar.swipe_down_small()
    time.sleep(1)
    return 0

def begenop3():
    xdeger , ydeger = opencv.opencv( "ol.png", threshold=0.9)
    print("begeni")
    if(xdeger>1):
        fonksiyonlar.open_app_at_coordinates(xdeger,ydeger)
        return "begenop3"
    return 0
    
def yorumop4():
    print("yorum yapılıyor")
    xdeger , ydeger = opencv.opencv10("yor.png", x0=0, y0=0, x1=1080, y1=2000, threshold=0.7)
    time.sleep(2)
    print("yorum")
    if(xdeger[0]>1):
        fonksiyonlar.open_app_at_coordinates(xdeger[0],ydeger[0])
        time.sleep(1)
        s = acıklamaal.tane_acıklama(1)
        a = acıklamaal.verinpyread()
        print(a)
        time.sleep(1)
        if(len(a)>0):
            c = random.randint(1,1)
            print(c)
            if (((c !=1)and(c !=2)and(c !=3)and(c !=4)and(c !=5))):
                fonksiyonlar.back()
            if(c==1):
                print(1)
                fonksiyonlar.open_app_at_coordinates(550,2300)
                time.sleep(1)
                f = len(a)
                s = random.randint(0,f)
                keyokuyucu.readkey1(a[s-1])
                time.sleep(1)
                fonksiyonlar.open_app_at_coordinates(950,2300)
                time.sleep(1)
                fonksiyonlar.back()
                time.sleep(1)
                fonksiyonlar.back()
                return "yorumyaz"
            if((c==2)or(c==3)or(c==4)or(c==5)):
                adeger , bdeger = opencv.opencv10( "ol.png", x0=0, y0=0, x1=1080, y1=2000, threshold=0.7)
                asds = len(xdeger)
                lık = random.randint(0,asds-1)
                fonksiyonlar.open_app_at_coordinates(adeger[lık],bdeger[lık])
                time.sleep(0.5)   
                sa = random.randint(1,5)
                print(sa)
                if(sa!=2):
                    fonksiyonlar.back()
                if(sa==2):
                   cdeger , ddeger = opencv.opencv10("ol.png", x0=0, y0=0, x1=1080, y1=2000, threshold=0.7)
                   asds = len(xdeger)
                   lık = random.randint(0,asds-1)
                   fonksiyonlar.open_app_at_coordinates(cdeger[lık],ddeger[lık])
                   time.sleep(0.5)
                   ka = random.randint(1,5)
                   if (ka !=2):
                       fonksiyonlar.back()
                   if(ka==2):
                        edeger , fdeger = opencv.opencv10("ol.png", x0=0, y0=0, x1=1080, y1=2000, threshold=0.7)
                        time.sleep(0.5)
                        asds = len(xdeger)
                        lık = random.randint(0,asds)
                        fonksiyonlar.open_app_at_coordinates(edeger[lık],fdeger[lık])
                        fonksiyonlar.back()
        if(len(a)==0):
            fonksiyonlar.back()                    
    return 0
    


def gonderop5():
    xdeger , ydeger = opencv.opencv("gonder.png", threshold=0.7)
    if (xdeger>2):
        fonksiyonlar.open_app_at_coordinates(xdeger,ydeger)
    return 5


def reelskaydetop6():
    adeger , bdeger = opencv.opencv10("ucnokta.png", x0=0, y0=0, x1=1080, y1=2000, threshold=0.7)
    if adeger[0]>1:
        fonksiyonlar.open_app_at_coordinates(adeger[0],bdeger[0])
        time.sleep(1)
        xdeger , ydeger = opencv.opencv10("reelskaydet.png", x0=0, y0=0, x1=1080, y1=2000, threshold=0.7)
        time.sleep(1)
        if xdeger[0]>1:
            fonksiyonlar.open_app_at_coordinates(xdeger[0],ydeger[0])    
            time.sleep(2)
            return "kaydet"
        else:
            fonksiyonlar.open_app_at_coordinates(250,550)
            time.sleep(1)

def anakaydetop7():
    xdeger , ydeger = opencv.opencv("anakaydet.jpeg", threshold=0.7)
    if xdeger>1:
        fonksiyonlar.open_app_at_coordinates(xdeger,ydeger)
    time.sleep(1)
    return 7


def takipreels():
    f =takip.reelstakıpcıbul()
    if(f==2):
        a = takip.reelstakipana()
        adeger , bdeger = acıklamaal.opencv(template_path="tamamkoruma.png", threshold=0.9) 
        if(adeger[0]>1):
            fonksiyonlar.open_app_at_coordinates(adeger[0],bdeger[0])
            n = random.randint(4,22)
            time.sleep(n/10)
        sdeger , ldeger = opencv.opencv(template_path="takipkoruma.png", threshold=0.9)
        print(sdeger)
        if(sdeger>1):
           print("geri tuşu bulundu")
           time.sleep(1)
           fonksiyonlar.back()
           n = random.randint(4,22)
           time.sleep(n/10)            
           time.sleep(2)
        fonksiyonlar.back()
    if(f==1):
        a = -1
    c = random.randint(0,2)
    time.sleep(c) 
    print("takip")
    return a