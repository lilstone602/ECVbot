import fonksiyonlar 
import random 
import den
import acıklamaal


def fonk():
    acıklamaal.verisıfırla()
    begenisınır = random.randint(150,200)
    yorumsınır = random.randint(0,0)
    kaydetsınır = random.randint(0,0)   
    takipsınır = random.randint(8,10)
    kaydırsınır = random.randint(90,120)
    


    for i in range(1,6):
        if(i==1):
            süre = random.randint(1200,1600)
            begeni, yorumyaz ,reelskaydet, takip = den.hepsi(begenisınır,yorumsınır,kaydetsınır,takipsınır,kaydırsınır,süre)
        
        
        if(i==2):
            süre = random.randint(1200,1600)
            a = random.randint(600,800)
        
            begeni, yorumyaz ,reelskaydet, takip = den.hepsi(begenisınır,yorumsınır,kaydetsınır,takipsınır,kaydırsınır,a)
        
            begenisınır = begenisınır-begeni
            yorumsınır = yorumsınır-yorumyaz
            kaydetsınır = kaydetsınır-reelskaydet
            takipsınır = takipsınır-takip
        
            begeni, yorumyaz ,reelskaydet, takip = den.hepsi(begenisınır,yorumsınır,kaydetsınır,takipsınır,kaydırsınır,süre-a)
        
        if(i==3):
            süre = random.randint(1200,1600)
            a = random.randint(400,535)
        
            begeni, yorumyaz ,reelskaydet, takip = den.hepsi(begenisınır,yorumsınır,kaydetsınır,takipsınır,kaydırsınır,süre)
        
        if(i==4):
            süre = random.randint(1200,1600)
            begeni, yorumyaz ,reelskaydet, takip = den.hepsi(begenisınır,yorumsınır,kaydetsınır,takipsınır,kaydırsınır,süre)
            
        if(i==5):
            süre = random.randint(1200,1600)
            begeni, yorumyaz ,reelskaydet, takip = den.hepsi(begenisınır,yorumsınır,kaydetsınır,takipsınır,kaydırsınır,süre)                
   

# if 1 işlemse 2 işlemse 3 işlemse ve 4 işlemse olmak üzere yap mantıkan süre bölünsede işemler aynı kalabilir


    begeni, reelskaydet ,yorumyaz, takip = den.hepsi(begenisınır,yorumsınır,kaydetsınır,takipsınır,kaydırsınır)
  
    yenibegenisınır =begenisınır - begeni 
    
