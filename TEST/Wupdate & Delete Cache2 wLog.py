import os
import subprocess
import ctypes
import sys
import shutil
import datetime
import logging

LOG_FILE = "script_logs.txt"  # Nom du fichier de logs

def is_admin():
    """ Écrit un message horodaté dans le fichier de logs et l'affiche. """
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_message = f"{timestamp} {message}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(log_message)  # Écrit dans le fichier de logs

    print(log_message.strip())  # Affiche aussi à l'écran

def is_admin():
    """ Vérifie si le script est exécuté en mode administrateur. """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        logging.warning("Le script n'est pas en mode administrateur.")
        return False 

def run_as_admin():
    """ Relance le script en mode administrateur si ce n'est pas déjà le cas. """
    if not is_admin():
        logging.info("Demande d'élévation des privilèges...")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        except Exception as e:
            logging.error(f"[Impossible de s'exécuter en administrateur : {e}")
        sys.exit(1)

def check_updates():
    """ Force la recherche des mises à jour Windows. """
    logging.info("Vérification des mises à jour...")
    
    try:
        subprocess.run('UsoClient.exe StartScan', check=True, shell=True)
        logging.info("[OK] Scan des mises à jour lancé.")

    except subprocess.CalledProcessError:
        write_log("[WARNING] UsoClient.exe bloqué, tentative via PowerShell...")
        ps_command = 'Install-Module PSWindowsUpdate -Force; Get-WindowsUpdate -Scan'
        try:
            subprocess.run(['powershell', '-Command', ps_command], check=True)
            write_log("[OK] Scan des mises à jour effectué via PowerShell.")
        except subprocess.CalledProcessError:
            write_log("[ERREUR] Impossible d'exécuter la recherche de mises à jour.")

def clean_cache():
    """ Nettoie le cache DNS et supprime les fichiers temporaires. """
    write_log("[INFO] Nettoyage du cache...")
    
    # Nettoyage DNS
    try:
        subprocess.run(["ipconfig", "/flushdns"], check=True)
        write_log("[OK] Cache DNS vidé.")
    except subprocess.CalledProcessError:
        write_log("[WARNING] Impossible de vider le cache DNS.")

    # Suppression des fichiers temporaires
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
            write_log("[OK] Fichiers temporaires supprimés.")
        except Exception as e:
            write_log(f"[ERREUR] Impossible de supprimer les fichiers temporaires : {e}")

def main():
    logging.info("=== Début de l'exécution du script ===")
    run_as_admin()
    check_updates()
    clean_cache()
    write_log("Opération terminée.")
    write_log("=== Fin de l'exécution du script ===\n")

if __name__ == '__main__':
    main()
