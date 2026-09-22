# Start Glassbench: http://127.0.0.1:8765
#   .\glassbench.ps1            start the app (builds the frontend the first time)
#   .\glassbench.ps1 -Build     rebuild the frontend first (after editing frontend/src)
# Keys are read by the backend from .env at the repository root (see .env.example). Ctrl+C stops it.
param([switch]$Build)

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONUTF8 = "1"

if ($Build -or -not (Test-Path (Join-Path $here "frontend\dist\index.html"))) {
    Push-Location (Join-Path $here "frontend")
    try { npm run build } finally { Pop-Location }
}

Push-Location (Join-Path $here "backend")
try {
    & (Join-Path $here ".venv\Scripts\python.exe") -m deskapp serve
} finally {
    Pop-Location
}
