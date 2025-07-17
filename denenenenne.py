import fonksiyonlar
import time
import acıklamaal
import random
import opencv
import os



fonksiyonlar.baglan()
import subprocess

def proxy_tanimla(serial, proxy_ip, proxy_port):
    proxy = f"{proxy_ip}:{proxy_port}"
    try:
        subprocess.run(
            ["adb", "-s", serial, "shell", "settings", "put", "global", "http_proxy", proxy],
            check=True
        )
        print(f"✅ Proxy tanımlandı: {serial} -> {proxy}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Proxy tanımlama hatası: {e}")

# Örnek kullanım
serial = "emulator-5556"
proxy_ip = "8.188.250.240"
proxy_port = "50535"

proxy_tanimla(serial, proxy_ip, proxy_port)
