import subprocess
import time

lnk_path = "C:\\Users\\PasifikGaming\\Desktop\\BlueLDPlayer-1.lnk"
subprocess.Popen([lnk_path], shell=True)
time.sleep(100)  # Script 100 saniye bekler, ancak LDPlayer kapanmaz.