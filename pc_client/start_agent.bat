@echo off
title Smart Lab Control System

:: 🔐 Request Admin Permission
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Requesting Administrator permission...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~s0' -Verb runAs"
    exit
)

cd /d %~dp0

echo ===============================
echo   SMART LAB CONTROL STARTING
echo ===============================

:: Check Python
python --version >nul 2>&1
if %errorLevel% NEQ 0 (
    echo ❌ Python not installed!
    pause
    exit
)

:: Run Agent
echo Starting Agent...
start "" python agent.py

echo.
echo ✅ Lab System Running Successfully
echo You can now use the PC
echo.

pause