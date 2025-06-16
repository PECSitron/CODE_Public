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
    """ Relance le script en mode administrateur si nécessaire. """
    if not is_admin():
        print("[INFO] == Demande d'élévation des privilèges... ==")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)  # On quitte le script actuel après avoir demandé l'élévation
        except Exception as e:
            print(f"[ERREUR] Impossible de s'exécuter en administrateur : {e}")
            sys.exit(1)

def check_updates():
    """ Force la recherche des mises à jour Windows en contournant les restrictions GPO. """
    print("==[INFO] Vérification des mises à jour...==")
    
    try:
        subprocess.run('UsoClient.exe StartScan', check=True, shell=True)
        print("[OK] Scan des mises à jour lancé via UsoClient.")
    except subprocess.CalledProcessError:
        print("[WARNING] UsoClient.exe bloqué, tentative via wuauclt...")

        try:
            # Méthode alternative via Powershell
            subprocess.run('wuauclt /detectnow /reportnow', check=True, shell=True)
            print("[OK] Scan des mises à jour effectué via wuauclt.")
        except subprocess.CalledProcessError:
            print("[WARNING] wuauclt bloqué, tentative via schtasks...")

            try:
                # Méthode alternative Bis via le planificateur de tâches
                subprocess.run('schtasks /Run /TN "\\Microsoft\\Windows\\WindowsUpdate\\Automatic App Update"', check=True, shell=True)
                print("[OK] Recherche de mises à jour forcée via Tâche planifiée.")
            except subprocess.CalledProcessError:
                print("[ERREUR] Impossible d'exécuter la recherche de mises à jour.")

def clean_cache():
    """ Nettoie le cache DNS et supprime les fichiers temporaires. """
    print("== [INFO] Nettoyage du cache... ==")

    # Nettoyage DNS
    try:
        subprocess.run(["ipconfig", "/flushdns"], check=True)
        print("[OK] Cache DNS vidé.")
    except subprocess.CalledProcessError:
        print("[WARNING] Impossible de vider le cache DNS.")

    # Suppression des fichiers temporaires
    temp_paths = [os.environ.get("TEMP", "C:\\Windows\\Temp"), os.environ.get("TMP", "C:\\Windows\\Temp")]

    for temp_path in temp_paths:
        if os.path.exists(temp_path):
            try:
                shutil.rmtree(temp_path, ignore_errors=True)
                print(f"[OK] Cache temporaire vidé : {temp_path}")
            except Exception as e:
                print(f"[ERREUR] Impossible de nettoyer {temp_path} : {e}")

    # Exécution du nettoyage de disque
    try:
        subprocess.run("cleanmgr /sagerun:1", shell=True, check=True)
        print("[OK] Nettoyage avancé effectué via cleanmgr.")
    except subprocess.CalledProcessError:
        print("[WARNING] Nettoyage cleanmgr non exécuté.")

def main():
    if not is_admin():
        run_as_admin()

    check_updates()
    clean_cache()
    print("[INFO] Opération terminée.")

if __name__ == '__main__':
    main()
