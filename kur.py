import mini
import fonksiyonlar




        

def sako(x,begenisınır,yorumsınır,kaydetsınır,takipsınır,kaydırsınır):
    if x in (range(begenisınır+yorumsınır+kaydetsınır+takipsınır, begenisınır+yorumsınır+kaydetsınır+takipsınır+kaydırsınır)):
        fonksiyonlar.bekle(4,6)
        a = mini.azkay2()
        return a   
    if x in (range(0, begenisınır)):
        fonksiyonlar.bekle(1,3)
        a = mini.begenop3() 
        fonksiyonlar.bekle(0,2)
        return a   
    if x in (range(begenisınır, begenisınır+yorumsınır)):
        fonksiyonlar.bekle(2,5)
        a = mini.yorumop4()
        fonksiyonlar.bekle(1,4)
        return a        
    if x in (range(begenisınır+yorumsınır, begenisınır+yorumsınır+kaydetsınır)):
        a = mini.reelskaydetop6()   
        return a       
    if x in (range(begenisınır+yorumsınır+kaydetsınır,begenisınır+yorumsınır+kaydetsınır+takipsınır)):
        fonksiyonlar.bekle(1,3)
        a = mini.takipreels() 
        fonksiyonlar.bekle(1,2)  
        return a    
        
