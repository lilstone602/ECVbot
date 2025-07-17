import key

import subprocess



def readkey1(kelime):
    for i in range(len(kelime)):
      unkey = kelime[i]
      if unkey == " ":
        subprocess.run(["adb", "shell", "input", "text", "%s"])
      else:  
        subprocess.run(["adb", "shell", "input", "text", unkey])


def readkey(kelime):
    for i in range(len(kelime)):
      unkey = kelime[i]
      if (unkey=="q")or(unkey=="Q"):
        key.keyq()
      if (unkey=="w")or(unkey=="W"):
        key.keyw()
      if (unkey=="e")or(unkey=="E"):
        key.keye()
      if (unkey=="r")or(unkey=="R"):
        key.keyr()
      if (unkey=="t")or(unkey=="T"):
        key.keyt()    
      if (unkey=="y")or(unkey=="Y"):
        key.keyy()    
      if (unkey=="u")or(unkey=="U")or(unkey=="ü")or(unkey=="Ü"):
        key.keyu()
      if (unkey=="i")or(unkey=="İ")or(unkey=="ı")or(unkey=="I"):
        key.keyi()
      if (unkey=="o")or(unkey=="ö")or(unkey=="O")or(unkey=="Ö"):
        key.keyo()
      if (unkey=="p")or(unkey=="P"):
        key.keyp()
      if (unkey=="a")or(unkey=="A"):
        key.keya()    
      if (unkey=="s")or(unkey=="ş")or(unkey=="S")or(unkey=="Ş"):
        key.keys() 
      if (unkey=="d")or(unkey=="D"):
        key.keyd()
      if (unkey=="f")or(unkey=="F"):
        key.keyf()
      if (unkey=="g")or(unkey=="ğ")or(unkey=="G")or(unkey=="Ğ"):
        key.keyg()
      if (unkey=="h")or(unkey=="H"):
        key.keyh()
      if (unkey=="j")or(unkey=="J"):
        key.keyj()    
      if (unkey=="k")or(unkey=="K"):
        key.keyk()  
      if (unkey=="l")or(unkey=="L"):
        key.keyl()
      if (unkey=="z")or(unkey=="z"):
        key.keyz()
      if (unkey=="x")or(unkey=="X"):
        key.keyx()
      if (unkey=="c")or(unkey=="ç")or(unkey=="C")or(unkey=="Ç"):
        key.keyc()
      if (unkey=="v")or(unkey=="V"):
        key.keyv()    
      if (unkey=="b")or(unkey=="B"):
        key.keyb()      
      if (unkey=="n")or(unkey=="N"):
        key.keyn()                       
      if (unkey=="m")or(unkey=="M"):
        key.keym()      
      if (unkey=="1"):
        key.key1()                       
      if (unkey=="2"):
        key.key2()      
      if (unkey=="3"):
        key.key3()                       
      if (unkey=="4"):
        key.key4()      
      if (unkey=="5"):
        key.key5()                       
      if (unkey=="6"):
        key.key6()      
      if (unkey=="7"):
        key.key7()                       
      if (unkey=="8"):
        key.key8()      
      if (unkey=="9"):
        key.key9()                       
      if (unkey=="0"):
        key.key0()    
      if (unkey==" "):
        key.keyspace()  
      if(unkey=="."):
        key.keynokta()     
      if(unkey==","):
        key.keyvirgül() 
                     
                            
               
            
     
                     
                            
               
            