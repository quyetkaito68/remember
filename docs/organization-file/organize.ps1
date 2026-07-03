param (
    [string]$source,
    [string]$config,
    [switch]$dryRun,
    [switch]$recurse
)

if (-not $source) {
    $source = "$env:USERPROFILE\Downloads"
}
$source = $source.Trim()

if (-not $config) {
    $config = Join-Path $PSScriptRoot "config.json"
}

if (!(Test-Path $config)) {
    Write-Host "Khong tim thay config: $config"
    exit 1
}

$cfg = Get-Content $config -Raw | ConvertFrom-Json

# Build extension -> rule map
$extMap = @{}
foreach ($rule in $cfg.rules) {
    foreach ($ext in $rule.extensions) {
        $extMap[$ext.ToLower()] = $rule
    }
}

if (!(Test-Path $source)) {
    Write-Host "Source khong ton tai: $source"
    exit 1
}

if ($recurse) {
    $files = Get-ChildItem -Path $source -File -Recurse
} else {
    $files = Get-ChildItem -Path $source -File
}

$startTime = Get-Date

Write-Host "Folder: $source"
Write-Host "So file: $($files.Count)"

if ($dryRun) {
    Write-Host "[DRY-RUN] Chi xem truoc, khong di chuyen file.`n"
}

$summary = @{}
$skipped = 0
$failed = 0
$total = $files.Count
$current = 0

foreach ($file in $files) {
    $ext = $file.Extension.ToLower()
    $current++

    if ($extMap.ContainsKey($ext)) {
        $rule = $extMap[$ext]
        $dest = $rule.destination
        $name = $rule.name

        if (-not $summary.ContainsKey($name)) {
            $summary[$name] = 0
        }

        $targetFile = Join-Path $dest $file.Name

        if (Test-Path $targetFile) {
            $newName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name) + "_" + (Get-Date -Format "yyyyMMddHHmmss") + $file.Extension
            $targetFile = Join-Path $dest $newName
        }

        if ($dryRun) {
            Write-Host "[DRY-RUN] Would move: $($file.Name) -> $dest"
            $summary[$name]++
        } else {
            if (!(Test-Path $dest)) {
                New-Item -ItemType Directory -Path $dest | Out-Null
            }

            try {
                Move-Item -LiteralPath $file.FullName -Destination $targetFile -Force
                $summary[$name]++
            }
            catch {
                Write-Host "FAILED: $($file.Name) | $($_.Exception.Message)"
                $failed++
            }
        }
    } else {
        $skipped++
    }

    Write-Progress -Activity "Organizing files" -Status "Da xu ly $current/$total" -PercentComplete (($current / $total) * 100)
}

Write-Progress -Activity "Organizing files" -Completed -Status "Hoan thanh"

$totalMoved = 0
if ($summary.Count -gt 0) {
    $totalMoved = ($summary.Values | Measure-Object -Sum).Sum
}

$elapsed = (Get-Date) - $startTime
if ($elapsed.TotalSeconds -lt 60) {
    $elapsedStr = "$([Math]::Round($elapsed.TotalSeconds)) giay"
} elseif ($elapsed.TotalMinutes -lt 60) {
    $elapsedStr = "$([Math]::Round($elapsed.TotalMinutes)) phut"
} else {
    $elapsedStr = "$([Math]::Round($elapsed.TotalHours, 1)) gio"
}

Write-Host ""
Write-Host "===== KET QUA ====="
foreach ($name in $summary.Keys) {
    Write-Host "  $name : $($summary[$name]) file"
}
Write-Host "  Bo qua (khong khop loai) : $skipped file"
if ($failed -gt 0) {
    Write-Host "  Loi                     : $failed file"
}
Write-Host "  Tong da di chuyen        : $totalMoved / $total file"
Write-Host "  Thoi gian xu ly          : $elapsedStr"
