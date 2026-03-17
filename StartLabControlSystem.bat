@echo off
title Smart Lab Control System

echo =====================================
echo   STARTING SMART LAB SYSTEM TEST
echo =====================================

cd /d E:\SmartLabControlSystem\labcontrol

:: -------------------------------
:: GET IP
:: -------------------------------
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    set ip=%%a
    goto :done
)
:done

set ip=%ip:~1%

echo Server IP: %ip%

:: -------------------------------
:: CREATE SERVER FILE
:: -------------------------------
echo http://%ip%:8000 > server.txt

:: ALSO COPY TO CLIENT FOLDER
copy server.txt E:\SmartLabControlSystem\pc_client\server.txt > nul

:: -------------------------------
:: START SERVER
:: -------------------------------
start cmd /k "python manage.py runserver 0.0.0.0:8000"

timeout /t 3 > nul

:: -------------------------------
:: OPEN DASHBOARD
:: -------------------------------
start http://%ip%:8000/dashboard/

:: OPEN ADMIN PANEL
start http://%ip%:8000/admin-panel/

echo.
echo ✅ SERVER STARTED SUCCESSFULLY
echo.

pause