import fonksiyonlar 
import time
import opencv
import random 
import kur
import acıklamaal
import mini

fonksiyonlar.baglan()

fonksiyonlar.yanakaydır()
time.sleep(1)
fonksiyonlar.open_app_at_coordinates(170,400)
time.sleep(1)
i=0
s = random.randint(4,10)
for i in range(1,100):
    fonksiyonlar.yanakaydır()
    c = random.randint(1,6)
    a =random.randint(1,2)
    s = random.randint(4,12)
    if(a==1):
        time.sleep(a)
        
    if(a==2):
        time.sleep(s)    