# verify-diagram.ps1
# Kiem tra alignment cua ASCII diagram trong file markdown
# Usage: powershell -File scripts/verify-diagram.ps1 -File <path-to-md>

param(
    [Parameter(Mandatory=$true)]
    [string]$File
)

if (-not (Test-Path $File)) {
    Write-Host "ERROR: File not found: $File" -ForegroundColor Red
    exit 1
}

$content = Get-Content $File -Raw -Encoding UTF8
$lines = $content -split "`n"

$inCodeBlock = $false
$diagramLines = @()
$diagramStart = 0
$diagramIndex = 0
$errors = 0
$warnings = 0

# Unicode box drawing chars as code points
$BOX_CHARS = @(
    0x250C,  # ┌
    0x2510,  # ┐
    0x2514,  # └
    0x2518,  # ┘
    0x2502,  # │
    0x2500,  # ─
    0x251C,  # ├
    0x2524,  # ┤
    0x252C,  # ┬
    0x2534,  # ┴
    0x253C   # ┼
)

function Test-LineHasBorder {
    param([string]$Line)
    if ($Line.Length -eq 0) { return $false }
    $firstChar = [int][char]$Line[0]
    return $BOX_CHARS -contains $firstChar
}

function Test-DiagramAlignment {
    param(
        [string[]]$Lines,
        [int]$StartLine,
        [int]$Index
    )

    $localErrors = 0
    $localWarnings = 0

    # Find lines that start with box border character
    $borderLineInfos = @()
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        $line = $Lines[$i]
        if (Test-LineHasBorder -Line $line) {
            $borderLineInfos += @{ Index = $i; Content = $line; Length = $line.Length }
        }
    }

    if ($borderLineInfos.Count -lt 2) {
        return @{ Errors = 0; Warnings = 0 }
    }

    # Check lines starting with │ (vertical border) have same length
    $pipeLines = $borderLineInfos | Where-Object {
        if ($_.Content.Length -eq 0) { return $false }
        [int][char]$_.Content[0] -eq 0x2502
    }

    if ($pipeLines.Count -gt 1) {
        $lengths = $pipeLines | ForEach-Object { $_.Length }
        $uniqueLengths = $lengths | Sort-Object -Unique

        if ($uniqueLengths.Count -gt 1) {
            Write-Host "`n  DIAGRAM #$Index (line $StartLine):" -ForegroundColor Yellow
            Write-Host "  Border alignment mismatch!" -ForegroundColor Red

            foreach ($bl in $pipeLines) {
                $lineNum = $StartLine + $bl.Index
                Write-Host "    Line $lineNum ($($bl.Length) chars): $($bl.Content)" -ForegroundColor Gray
            }

            $uniqueLengthsStr = $uniqueLengths -join ", "
            Write-Host "  Expected all lines to have same length. Found: $uniqueLengthsStr" -ForegroundColor Red
            $localErrors++
        }
    }

    # Check line length is reasonable (< 100 chars)
    foreach ($bl in $borderLineInfos) {
        if ($bl.Length -gt 100) {
            Write-Host "  WARNING: Line too long ($($bl.Length) chars > 100)" -ForegroundColor Yellow
            $localWarnings++
        }
    }

    return @{ Errors = $localErrors; Warnings = $localWarnings }
}

$lineNum = 0
foreach ($line in $lines) {
    $lineNum++

    if ($line -match '```text') {
        $inCodeBlock = $true
        $diagramLines = @()
        $diagramStart = $lineNum
        $diagramIndex++
        continue
    }

    if ($inCodeBlock -and $line -match '```') {
        $inCodeBlock = $false
        $result = Test-DiagramAlignment -Lines $diagramLines -StartLine $diagramStart -Index $diagramIndex
        $errors += $result.Errors
        $warnings += $result.Warnings
        $diagramLines = @()
        continue
    }

    if ($inCodeBlock) {
        $diagramLines += $line
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "DIAGRAM VERIFICATION REPORT" -ForegroundColor Cyan
Write-Host "File: $File" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Diagrams found: $diagramIndex"

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "Status: ALL DIAGRAMS OK" -ForegroundColor Green
} else {
    if ($errors -gt 0) {
        Write-Host "Errors: $errors" -ForegroundColor Red
    }
    if ($warnings -gt 0) {
        Write-Host "Warnings: $warnings" -ForegroundColor Yellow
    }
}

exit $errors
