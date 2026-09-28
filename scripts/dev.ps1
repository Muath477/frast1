# RootIQ local dev (Windows PowerShell)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

if (Get-Command docker -ErrorAction SilentlyContinue) {
  docker compose up -d db
}

$backend = Start-Process -PassThru -NoNewWindow powershell -ArgumentList @(
  "-NoProfile", "-Command",
  "Set-Location '$PWD\backend'; if (Test-Path .venv\Scripts\Activate.ps1) { . .\.venv\Scripts\Activate.ps1 }; uvicorn app.main:app --reload --port 8000"
)

$frontend = Start-Process -PassThru -NoNewWindow powershell -ArgumentList @(
  "-NoProfile", "-Command",
  "Set-Location '$PWD\frontend'; npm run dev"
)

Write-Host "Backend PID $($backend.Id) | Frontend PID $($frontend.Id)"
Write-Host "API http://localhost:8000/api/health  UI http://localhost:5173"
Wait-Process -Id $backend.Id, $frontend.Id
