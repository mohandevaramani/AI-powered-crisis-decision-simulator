@echo off
REM AI Crisis Decision Simulator - Setup and Run Script

echo.
echo ================================================
echo AI Crisis Decision Simulator - Setup
echo ================================================
echo.

setlocal enabledelayedexpansion

REM Check if venv exists
if not exist "venv" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Make sure Python is installed and in PATH
        pause
        exit /b 1
    )
) else (
    echo [1/4] Virtual environment already exists
)

echo.
echo [2/4] Activating virtual environment...
set "ROOT=%~dp0"
call "%ROOT%venv\Scripts\activate.bat"
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo [3/4] Installing dependencies...
pip install --upgrade pip > nul 2>&1
pip install -r "%ROOT%crisis_simulator\requirements.txt"
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [4/4] Setup complete!
echo.
echo ================================================
echo Running AI Crisis Decision Simulator
echo ================================================
echo.
echo Backend API will start on http://localhost:5000
echo Frontend will open automatically in your browser
echo.

REM Start Flask backend in a new window
echo Starting backend API...
start "Crisis Simulator Backend" cmd /k "cd /d \"%ROOT%\" && set PYTHONPATH=. && \"%ROOT%venv\Scripts\python.exe\" crisis_simulator/backend/app.py"

REM Wait a few seconds for backend to start
timeout /t 3 /nobreak

REM Open frontend in default browser
echo.
echo Opening frontend dashboard in your browser...
start "" "http://localhost:5000"

echo.
echo ================================================
echo System Running
echo ================================================
echo.
echo Application: http://localhost:5000
echo Backend:     http://localhost:5000
echo.
echo Press Ctrl+C in the command windows to stop
echo.

pause
