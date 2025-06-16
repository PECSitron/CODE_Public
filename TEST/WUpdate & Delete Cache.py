import os
import subprocess
import ctypes
import sys

def is_admin():
    """Vérifie si le script est exécuté en mode administrateur."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_updates():
    """Force la recherche des mises à jour Windows."""
    print("[INFO] Vérification des mises à jour...")
    update_commands = [
        'schtasks /Run /TN "\\Microsoft\\Windows\\WindowsUpdate\\Automatic App Update"',
        'schtasks /Run /TN "\\Microsoft\\Windows\\WindowsUpdate\\Automatic App Update (Postponed)"',
        'UsoClient.exe StartScan',
        'UsoClient.exe RefreshSettings'
    ]
    for cmd in update_commands:
        try:
            subprocess.run(cmd, check=True, shell=True)
        except subprocess.CalledProcessError:
            print(f"[WARNING] Échec de l'exécution : {cmd}")

def clean_cache():
    """Nettoie le cache DNS et les fichiers temporaires."""
    print("[INFO] Nettoyage du cache...")
    
    # Nettoyage DNS
    try:
        subprocess.run(["ipconfig", "/flushdns"], check=True)
        print("[OK] Cache DNS vidé.")
    except subprocess.CalledProcessError:
        print("[WARNING] Impossible de vider le cache DNS.")

    # Suppression des fichiers temporaires
    temp_path = os.environ.get("TEMP", "C:\\Windows\\Temp")
    try:
        subprocess.run(f'del /F /S /Q "{temp_path}\\*"', check=True, shell=True)
        subprocess.run(f'for /d %x in ("{temp_path}\\*") do rd /s /q "%x"', check=True, shell=True)
        print("[OK] Fichiers temporaires supprimés.")
    except subprocess.CalledProcessError:
        print("[WARNING] Impossible de supprimer les fichiers temporaires.")

def main():
    if not is_admin():
        print("[ERREUR] Ce script doit être exécuté en mode administrateur.")
        print("Relancez-le en tant qu'administrateur.")
        sys.exit(1)
    
    check_updates()
    clean_cache()
    print("[INFO] Opération terminée.")

if __name__ == '__main__':
    main()
