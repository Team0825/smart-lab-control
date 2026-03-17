@echo off
title Smart Lab Agent

cd /d E:\SmartLabControlSystem\pc_client

echo Starting Agent...

:: Wait for server.txt
:wait
if not exist server.txt (
    echo Waiting for server...
    timeout /t 2 > nul
    goto wait
)

:: Run agent
start /min python agent.py

echo Agent started successfully!
exit