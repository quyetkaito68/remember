@echo off
title Organize File Tool

set TEMP_FILE=%TEMP%\organize_folder.txt
set SCRIPT_DIR=%~dp0

echo ==== CHON FOLDER CAN ORGANIZE ====

powershell -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; $dialog = New-Object System.Windows.Forms.FolderBrowserDialog; $dialog.Description = 'Chon folder can organize'; if ($dialog.ShowDialog() -eq 'OK') { $dialog.SelectedPath | Out-File -FilePath '%TEMP_FILE%' -Encoding ascii }"

if not exist "%TEMP_FILE%" (
    echo Ban da huy chon folder.
    pause
    exit
)

set /p SOURCE=<"%TEMP_FILE%"
del "%TEMP_FILE%"

:: Strip trailing backslash to prevent CMD escaping issue ("I:\" -> "I:")
if "%SOURCE:~-1%"=="\" set SOURCE=%SOURCE:~0,-1%

echo Folder da chon: %SOURCE%
echo.
echo [1] Chay that su (mac dinh)
echo [2] Dry-run (chi xem truoc)
echo.
set MODE=1
set /p MODE=Chon che do (1/2) [Enter=1]:

echo.
echo [1] Chi quet file o root folder (mac dinh)
echo [2] Quet ca subfolder (recurse)
echo.
set RECURSE=1
set /p RECURSE=Chon pham vi quet (1/2) [Enter=1]:

echo ==== DANG XU LY ====

set ARGS=-source "%SOURCE%"
if "%MODE%"=="2" set ARGS=%ARGS% -dryRun
if "%RECURSE%"=="2" set ARGS=%ARGS% -recurse

powershell.exe -NoExit -ExecutionPolicy Bypass -File "%SCRIPT_DIR%organize.ps1" %ARGS%

echo ==== DONE ====
pause
