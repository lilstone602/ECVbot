import os
import win32com.client



lnk_path = "C:\\Users\\PasifikGaming\\Desktop\\BlueLDPlayer-1.lnk"

import subprocess

subprocess.run(f'explorer "{lnk_path}"', shell=True)
