import subprocess

def read_build_prop_via_cat():
    try:
        # 'su -c cat' komutuyla dosya içeriğini çek
        result = subprocess.run(
            ["adb", "shell", "su", "-c", "cat /system/build.prop"],
            capture_output=True,
            text=True,
            check=True
        )
        content = result.stdout
        return content
    except subprocess.CalledProcessError as e:
        print("Hata:", e)
        return None

def write_build_prop_locally(content, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def modify_build_prop(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("ro.product.model="):
            new_lines.append("ro.product.model=Pixel 7 Pro\n")
        elif line.startswith("ro.build.fingerprint="):
            new_lines.append("ro.build.fingerprint=google/redfin/redfin:13/TQ3A.230705.001/10296145:user/release-keys\n")
        elif line.startswith("ro.product.device="):
            new_lines.append("ro.product.device=redfin\n")
        elif line.startswith("ro.product.manufacturer="):
            new_lines.append("ro.product.manufacturer=Google\n")
        else:
            new_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def push_build_prop(file_path):
    try:
        # /system dizinini yazılabilir yap
        subprocess.run(["adb", "shell", "su", "-c", "mount -o rw,remount /system"], check=True)
        # Dosyayı geri yükle
        subprocess.run(["adb", "push", file_path, "/system/build.prop"], check=True)
        # İzinleri düzelt
        subprocess.run(["adb", "shell", "su", "-c", "chmod 644 /system/build.prop"], check=True)
        # Emülatörü yeniden başlat
        subprocess.run(["adb", "shell", "su", "-c", "reboot"], check=True)
    except subprocess.CalledProcessError as e:
        print("Push veya remount hatası:", e)

def main():
    local_path = "build.prop"

    print("build.prop okunuyor...")
    content = read_build_prop_via_cat()
    if content is None:
        print("build.prop okunamadı.")
        return

    write_build_prop_locally(content, local_path)
    print("Dosya düzenleniyor...")
    modify_build_prop(local_path)

    print("Dosya geri yükleniyor...")
    push_build_prop(local_path)

if __name__ == "__main__":
    main()
