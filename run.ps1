# AI Crisis Decision Simulator - PowerShell Launcher
# Run this script to start both backend and frontend automatically

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "AI Crisis Decision Simulator" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$root = Resolve-Path $scriptDir

# Check if venv exists
if (-not (Test-Path "$root\venv")) {
    Write-Host "[1/4] Creating virtual environment..." -ForegroundColor Yellow
    & python -m venv "$root\venv"
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment. Make sure Python is installed."
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "[1/4] Virtual environment already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/4] Activating virtual environment..." -ForegroundColor Yellow
& "$root\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "[3/4] Installing/updating dependencies..." -ForegroundColor Yellow
& pip install --upgrade pip | Out-Null
& pip install -r "$root\crisis_simulator\requirements.txt"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install dependencies"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[4/4] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Starting AI Crisis Decision Simulator" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API will start on http://localhost:5000" -ForegroundColor White
Write-Host "Frontend will start on http://localhost:8080" -ForegroundColor White
Write-Host ""

# Start backend in new window
Write-Host "Starting backend API..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    param($root)
    Set-Location $root
    $env:PYTHONPATH = "."
    & "$root\venv\Scripts\python.exe" "crisis_simulator/backend/app.py"
} -ArgumentList $root

# Wait a moment for backend to initialize
Start-Sleep -Seconds 3

# Start frontend server in new window
Write-Host "Starting frontend server..." -ForegroundColor Yellow
$frontendJob = Start-Job -ScriptBlock {
    param($root)
    Set-Location "$root\crisis_simulator\frontend"
    & "$root\venv\Scripts\python.exe" -m http.server 8080
} -ArgumentList $root

# Wait for frontend to start
Start-Sleep -Seconds 2

# Open browser
Write-Host ""
Write-Host "Opening application in browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8080"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "System Running Successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: http://localhost:8080" -ForegroundColor White
Write-Host "Backend:  http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "Close this window and the command windows to stop the application" -ForegroundColor Yellow
Write-Host ""

# Keep the script running to show status
Read-Host "Press Enter to stop the servers and exit"

# Clean up jobs
Write-Host "Stopping servers..." -ForegroundColor Yellow
Stop-Job $backendJob -ErrorAction SilentlyContinue
Stop-Job $frontendJob -ErrorAction SilentlyContinue
Remove-Job $backendJob -ErrorAction SilentlyContinue
Remove-Job $frontendJob -ErrorAction SilentlyContinue

Write-Host "Servers stopped. Goodbye!" -ForegroundColor Green