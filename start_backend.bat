@echo off
REM Simple script to start backend only
setlocal enabledelayedexpansion
set "ROOT=%~dp0"

echo Starting Crisis Simulator Backend API...
echo.
echo Activating virtual environment...
call "%ROOT%venv\Scripts\activate.bat"

if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo Starting Flask server on http://localhost:5000...
echo Press Ctrl+C to stop
echo.

cd /d "%ROOT%crisis_simulator\backend"
"%ROOT%venv\Scripts\python.exe" app.py
