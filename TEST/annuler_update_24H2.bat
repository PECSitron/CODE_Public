@echo off
:: Stop services liés à Windows Update
net stop wuauserv
net stop bits
net stop usosvc
net stop dosvc

:: Supprimer la clé de redémarrage en attente
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired" /f

:: Supprimer les tâches d'orchestration de mise à jour
del /f /q C:\Windows\System32\Tasks\Microsoft\Windows\UpdateOrchestrator\*.*
del /f /q C:\Windows\System32\Tasks\Microsoft\Windows\Update\*.*

:: Nettoyage terminé
echo.
echo [OK] Nettoyage effectué. Vous pouvez maintenant redémarrer le PC sans risque de mise à jour forcée.
pause
