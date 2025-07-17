import fonksiyonlar 
import time
import opencv
import random 
import acıklamaal





def reelstakıpcıbul():
    xdeger , ydeger = opencv.opencv(template_path="ol.png", threshold=0.9) #olreel jpeg vardı
    if isinstance(xdeger, int) and (xdeger >1):
        fonksiyonlar.takipcibul(xdeger,ydeger)
    if(xdeger>1):
        return 2
    else:
        return 1
    

def takipet():
    adeger , bdeger = acıklamaal.opencv(template_path="takip.png", threshold=0.9) #olreel jpeg vardı
    b = len(adeger)
    a = random.randint(0,b-1)
    k = random.randint(1,5)
    if(adeger[a]>1):
        fonksiyonlar.open_app_at_coordinates(adeger[a],bdeger[a])
        return k
    return k


def reelstakip(xdeger,ydeger):
    fonksiyonlar.open_app_at_coordinates(xdeger,ydeger)
    time.sleep(3)
    fonksiyonlar.swipe_down_small()

 
 
def randomkaydırtakipci():
    a =random.randint(0,5)
    i = 0
    b = random.randint(1,2)
    if b ==1:
        for i in range(0,a+1):
            fonksiyonlar.swipe_down_mid()
    if b==2:
        for i in range(0,a+1):
            fonksiyonlar.swipe_down_small()        
        
    
    

    
def reelstakipana():
    b = random.randint(0,3)
    time.sleep(1)
    time.sleep(b)
    fonksiyonlar.swipe_down_mid()
    time.sleep(b)
    a = takipet()
    k = random.randint(1,5)
    sayac = 1
    if isinstance(a, int) and (a > 0):
        sayac =sayac + 1
    if(k==1)or(k==2)or(k==3):
        a = takipet()
        sayac=sayac+1
        fonksiyonlar.swipe_down_mid()
        time.sleep(a)
        if(a==2)or(a==4)or(a==5):
            a = takipet()
            sayac=sayac+1
            time.sleep(a)
            if(a==1)or(a==4)or(a==5):
                a = takipet()
                time.sleep(a)
                sayac=sayac+1
                if(a==1)or(a==5):
                    a = takipet()
                    sayac=sayac+1
                    time.sleep(a)        
    return sayac     




"""kullanım 
fonksiyonlar.baglan()
takip.reelstakıpcıbul()
time.sleep(3)
a = takip.reelstakipana()
print(a)
         """  
    
    
    

def enüsttakipet():
    adeger , bdeger = acıklamaal.opencv("takip.png", threshold=0.9) #olreel jpeg vardı
    b = len(adeger)
    a = 0
    k = random.randint(1,5)
    if(adeger[a]>1):
        fonksiyonlar.open_app_at_coordinates(adeger[a],bdeger[a])    
    