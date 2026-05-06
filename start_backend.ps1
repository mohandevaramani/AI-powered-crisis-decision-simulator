$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$root = Resolve-Path "$scriptDir"
$pythonExe = Join-Path $root "venv\Scripts\python.exe"
$backendDir = Join-Path $root "crisis_simulator\backend"

if (-not (Test-Path $pythonExe)) {
    Write-Error "Virtual environment not found at $pythonExe. Run .\run.bat or create the venv first."
    exit 1
}

if (-not (Test-Path $backendDir)) {
    Write-Error "Backend folder not found at $backendDir."
    exit 1
}

Set-Location $backendDir
& $pythonExe app.py
