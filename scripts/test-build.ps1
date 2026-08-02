# test-build.ps1 — Build test flow for VitePress project
# Usage:
#   .\scripts\test-build.ps1              # Build only
#   .\scripts\test-build.ps1 -Dev         # Build + start dev server, then shutdown
#   .\scripts\test-build.ps1 -MaxRetry 5  # Max retry on failure

param(
    [switch]$Dev,
    [int]$MaxRetry = 3
)

$ErrorActionPreference = "Continue"
$projectRoot = Split-Path $PSScriptRoot -Parent

function Test-Build {
    Write-Host "`n=== Build Test ===" -ForegroundColor Cyan
    Push-Location $projectRoot
    npm run build 2>&1 | Out-Host
    $exitCode = $LASTEXITCODE
    Pop-Location
    return $exitCode
}

function Stop-DevServer {
    $ports = @(5173, 4173, 3000)
    foreach ($port in $ports) {
        $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
        foreach ($conn in $connections) {
            $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
            if ($proc) {
                Write-Host "Stopping process $($proc.Name) (PID $($proc.Id)) on port $port" -ForegroundColor Yellow
                Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
            }
        }
    }
}

# === DEDUPLICATE CHECK ===
Write-Host "`n=== Checking for duplicate/corrupted content ===" -ForegroundColor Cyan
$mdFiles = Get-ChildItem "$projectRoot\docs\developer\*\*.md" -Recurse
$fixedCount = 0
foreach ($f in $mdFiles) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    $lines = $content -split "`n"
    $corruptLine = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '\.Matches\[0\]|\$val|StartsWith\(') {
            $corruptLine = $i
            break
        }
    }
    if ($corruptLine -gt 0) {
        $clean = $lines[0..($corruptLine-1)] -join "`n"
        Set-Content $f.FullName -Value $clean -Encoding UTF8 -NoNewline
        Write-Host "  Fixed: $($f.Name) (cut at line $corruptLine)" -ForegroundColor Yellow
        $fixedCount++
    }
}
if ($fixedCount -eq 0) {
    Write-Host "  No corruption found." -ForegroundColor Green
} else {
    Write-Host "  Fixed $fixedCount files." -ForegroundColor Yellow
}

# === BUILD TEST ===
$retry = 0
$success = $false

while ($retry -lt $MaxRetry -and -not $success) {
    $exitCode = Test-Build
    if ($exitCode -eq 0) {
        $success = $true
    } else {
        $retry++
        Write-Host "`nBuild FAILED (attempt $retry/$MaxRetry)" -ForegroundColor Red
        if ($retry -lt $MaxRetry) {
            Write-Host "Fix the error and press Enter to retry..." -ForegroundColor Yellow
            Read-Host
        }
    }
}

if (-not $success) {
    Write-Host "`n=== BUILD FAILED after $MaxRetry attempts ===" -ForegroundColor Red
    exit 1
}

Write-Host "`n=== BUILD SUCCESS ===" -ForegroundColor Green

# === DEV SERVER TEST ===
if ($Dev) {
    Write-Host "`nStarting dev server..." -ForegroundColor Cyan
    Push-Location $projectRoot
    $devProcess = Start-Process -FilePath "npm" -ArgumentList "run", "dev" -PassThru -NoNewWindow
    Pop-Location

    Start-Sleep -Seconds 5

    Write-Host "Dev server started (PID $($devProcess.Id)). Press Enter to shutdown." -ForegroundColor Green
    Read-Host

    Stop-DevServer
    Write-Host "Dev server stopped." -ForegroundColor Yellow
}

Write-Host "`n=== TEST COMPLETE ===" -ForegroundColor Green
exit 0
