$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

$Python = Join-Path $ProjectRoot "..\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

& $Python -m pip install -r requirements.txt
& $Python manage.py migrate
& $Python manage.py collectstatic --noinput
& $Python manage.py initialize_app

Write-Host ""
Write-Host "Starting production server on http://0.0.0.0:8000"
Write-Host "Keep this window open while WhatsApp sending is needed."
& $Python -m waitress --listen=0.0.0.0:8000 school_notification.wsgi:application
