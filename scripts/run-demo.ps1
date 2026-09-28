# RootIQ one-command demo (Windows PowerShell): simulation mode, backend :8000 + UI :5173, opens the Agents page.
#
#   .\scripts\run-demo.ps1                      # everything deterministic, no LLM, works offline
#   $env:GROQ_API_KEY = '<your key>'            # key stays in this shell only; it is never written to a file
#   .\scripts\run-demo.ps1 -Llm groq            # also: gemini (GEMINI_API_KEY) | anthropic (ANTHROPIC_API_KEY)
#   .\scripts\run-demo.ps1 -Stop                # stop both servers
#
# First run creates backend\.venv and installs frontend dependencies (a few minutes).
param(
  [ValidateSet('off', 'groq', 'gemini', 'anthropic')][string]$Llm = 'off',
  [switch]$Stop,
  [switch]$NoBrowser
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent

function Stop-Port([int]$Port) {
  Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
}

if ($Stop) { Stop-Port 8000; Stop-Port 5173; Write-Host 'RootIQ stopped.'; return }

$py = Join-Path $root 'backend\.venv\Scripts\python.exe'
if (-not (Test-Path $py)) {
  Write-Host 'Creating backend virtualenv and installing requirements...'
  python -m venv (Join-Path $root 'backend\.venv')
  & $py -m pip install -q -r (Join-Path $root 'backend\requirements.txt')
}
if (-not (Test-Path (Join-Path $root 'frontend\node_modules'))) {
  Write-Host 'Installing frontend dependencies...'
  Push-Location (Join-Path $root 'frontend'); npm install; Pop-Location
}

$env:ROOTIQ_MODE = 'sim'
if ($Llm -eq 'off') {
  $env:LLM_ENABLED = '0'
} else {
  $keyVar = @{ groq = 'GROQ_API_KEY'; gemini = 'GEMINI_API_KEY'; anthropic = 'ANTHROPIC_API_KEY' }[$Llm]
  if (-not [Environment]::GetEnvironmentVariable($keyVar)) {
    throw "Set `$env:$keyVar first (it is read from the environment and never saved)."
  }
  $env:LLM_ENABLED = '1'
  $env:LLM_PROVIDER = $Llm
}

Stop-Port 8000; Stop-Port 5173
Start-Process -WindowStyle Minimized -FilePath $py -WorkingDirectory (Join-Path $root 'backend') `
  -ArgumentList '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000'
Start-Process -WindowStyle Minimized -FilePath 'cmd.exe' -WorkingDirectory (Join-Path $root 'frontend') `
  -ArgumentList '/c', 'npm run dev -- --host 127.0.0.1 --port 5173'

Write-Host 'Waiting for the servers...'
foreach ($i in 1..60) {
  try {
    $api = (Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8000/api/health' -TimeoutSec 2).StatusCode
    $ui = (Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:5173/' -TimeoutSec 2).StatusCode
    if ($api -eq 200 -and $ui -eq 200) { break }
  } catch { Start-Sleep -Seconds 1 }
}
Write-Host 'API  http://localhost:8000/api/health'
Write-Host 'UI   http://localhost:5173        (Agents page: http://localhost:5173/agents)'
Write-Host "LLM  $Llm"
Write-Host 'Demo: Shift+1 injects uplink congestion, Shift+2 DNS, Shift+3 server spike, Shift+R resets.'
if (-not $NoBrowser) { Start-Process 'http://localhost:5173/agents' }
