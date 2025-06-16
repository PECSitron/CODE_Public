import os
import platform
import subprocess


def check_updates():
    subprocess.run('schtasks /Run /TN "\\Microsoft\\Windows\\WindowsUpdate\\Automatic App Update"', shell=True)
    subprocess.run('schtasks /Run /TN "\\Microsoft\\Windows\\WindowsUpdate\\Automatic App Update (Postponed)"', shell=True)
    subprocess.call(['wuauclt', '/detectnow'])   



def clean_cache():
    subprocess.run('ipconfig /flushdns', shell=True)
    subprocess.run('DEL /F /S /Q /A "%TEMP%\\*"', shell=True)


def main():
    check_updates()
    clean_cache()
    print("Cache cleared.")

if __name__ == '__main__':
    main()