@echo off
chcp 65001 >nul
title Chess Game

cd /d "%~dp0"

echo ========================================
echo    Starting Chess Game
echo ========================================
echo.

echo [1/3] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found
    pause
    exit
)
python --version

echo [2/3] Installing Flask...
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    python -m pip install flask
)

echo [3/3] Starting services...
echo.

start "Backend" cmd /k "cd /d "%~dp0" && python server.py"
timeout /t 2 /nobreak >nul
start "Frontend" cmd /k "cd /d "%~dp0" && python -m http.server 8080"

echo.
echo ========================================
echo Started! Visit: http://localhost:8080
echo ========================================
timeout /t 2 /nobreak >nul
start http://localhost:8080
