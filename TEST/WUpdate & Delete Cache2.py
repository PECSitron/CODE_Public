import os
import subprocess
import ctypes
import sys
import shutil

def is_admin():
    """ Vérifie si le script est exécuté en mode administrateur. """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """ Relance le script en mode administrateur si ce n'est pas déjà le cas. """
    if not is_admin():
        print("[INFO] Demande d'élévation des privilèges...")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        except Exception as e:
            print(f"[ERREUR] Impossible de s'exécuter en administrateur : {e}")
        sys.exit(1)

def check_updates():
    """ Force la recherche des mises à jour Windows en contournant les restrictions GPO. """
    print("[INFO] Vérification des mises à jour...")
    
    try:
        # Méthode standard (risque d'être bloquée)
        subprocess.run('UsoClient.exe StartScan', check=True, shell=True)
        print("[OK] Scan des mises à jour lancé.")
    except subprocess.CalledProcessError:
        print("[WARNING] UsoClient.exe bloqué, tentative via PowerShell...")

        # Méthode alternative via PowerShell
        ps_command = 'Install-Module PSWindowsUpdate -Force; Get-WindowsUpdate -Scan'
        try:
            subprocess.run(['powershell', '-Command', ps_command], check=True)
            print("[OK] Scan des mises à jour effectué via PowerShell.")
        except subprocess.CalledProcessError:
            print("[ERREUR] Impossible d'exécuter la recherche de mises à jour.")

def clean_cache():
    """ Nettoie le cache DNS et supprime proprement les fichiers temporaires verrouillés. """
    print("[INFO] Nettoyage du cache...")
    
    # Nettoyage DNS
    try:
        subprocess.run(["ipconfig", "/flushdns"], check=True)
        print("[OK] Cache DNS vidé.")
    except subprocess.CalledProcessError:
        print("[WARNING] Impossible de vider le cache DNS.")

    # Nettoyage des fichiers temporaires avec gestion des erreurs
    temp_path = os.environ.get("TEMP", "C:\\Windows\\Temp")
    
    if os.path.exists(temp_path):
        try:
            for root, dirs, files in os.walk(temp_path, topdown=False):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except PermissionError:
                        pass
                for dir in dirs:
                    try:
                        os.rmdir(os.path.join(root, dir))
                    except PermissionError:
                        pass
            print("[OK] Fichiers temporaires supprimés.")
        except Exception as e:
            print(f"[ERREUR] Impossible de supprimer les fichiers temporaires : {e}")

def main():
    run_as_admin()
    check_updates()
    clean_cache()
    print("[INFO] Opération terminée.")

if __name__ == '__main__':
    main()
