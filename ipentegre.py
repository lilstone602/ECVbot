import subprocess
import fonk


fonk.baglan()
# Proxy bilgileri
PROXY_HOST = "38.250.126.201"
PROXY_PORT = "999"

# ADB komutu ile proxy ayarla
subprocess.run([
    "adb", "shell", "settings", "put", "global", "http_proxy",
    f"{PROXY_HOST}:{PROXY_PORT}"
])
print("Proxy ayarlandı!")