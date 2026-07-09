@echo off
setlocal enabledelayedexpansion

:: ========== Configuration ==========
set "JMETER_HOME=D:\0_FullShare\Jmeter\apache-jmeter-5.4.3"
set "TESTPLAN_DIR=D:\0_FullShare\Jmeter\PerformanceTestMAU\testplan"

:: ========== Validate config ==========
if not exist "%JMETER_HOME%\bin\jmeter.bat" (
    echo [ERROR] JMETER_HOME not found: "%JMETER_HOME%"
    echo Please check path in script.
    pause
    exit /b 1
)
if not exist "%TESTPLAN_DIR%" (
    echo [ERROR] TESTPLAN_DIR not found: "%TESTPLAN_DIR%"
    echo Please check path in script.
    pause
    exit /b 1
)

:: ========== Get timestamp (YYYYMMDD_HHmmss) ==========
for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command "Get-Date -Format 'yyyyMMdd_HHmmss'"`) do set "timestamp=%%I"

:main_menu
cls
echo ==========================================
echo        JMeter Test Plan Selection
echo ==========================================
echo Directory: "%TESTPLAN_DIR%"
echo Date: %timestamp%
echo.

:: List test plans with natural sort
set "count=0"
for /f "delims=" %%f in ('powershell -Command "Get-ChildItem '%TESTPLAN_DIR%\*.jmx' | Sort-Object {[regex]::Replace($_.Name, '\d+', {$args[0].Value.PadLeft(20)})} | Select-Object -ExpandProperty Name"') do (
    set /a count+=1
    set "test!count!=%%~nf"
    echo   !count!. %%~nf
)

if !count! EQU 0 (
    echo [ERROR] No .jmx files found in "%TESTPLAN_DIR%"
    pause
    exit /b 1
)

echo.
echo   0. Exit
echo ==========================================
set /p "choice=Select test (0-!count!): "

if "%choice%"=="0" (
    echo Goodbye!
    exit /b 0
)

:: Validate input is a number in range
set /a "num=%choice%" 2>nul
if %errorlevel% NEQ 0 goto invalid_input
if %num% LSS 1 goto invalid_input
if %num% GTR !count! goto invalid_input

:: Get test name dynamically (avoids 15 if statements)
call set "testname=%%test%num%%%"

echo.
echo Selected: !testname!
set /p "confirm=Run this test? (y/n): "
if /i not "!confirm!"=="y" (
    echo Cancelled.
    pause
    goto main_menu
)

:: ========== Setup paths ==========
set "result_dir=testresult\!testname!_%timestamp%"
set "report_dir=testreport\!testname!_%timestamp%"
set "result_file=!result_dir!\!testname!_%timestamp%.jtl"
set "test_file=%TESTPLAN_DIR%\!testname!.jmx"

echo.
echo ==========================================
echo Running: !testname!
echo ==========================================
echo Test file: !test_file!
echo Result:   !result_file!
echo Report:   !report_dir!\index.html
echo ==========================================
echo.

:: Create output directories
if not exist "!result_dir!" mkdir "!result_dir!"
if not exist "!report_dir!" mkdir "!report_dir!"

:: Run JMeter
"%JMETER_HOME%\bin\jmeter" -n -t "!test_file!" -l "!result_file!" -e -o "!report_dir!" -f

if %errorlevel% EQU 0 (
    echo.
    echo ==========================================
    echo Test completed successfully!
    echo ==========================================
    echo Results: !result_file!
    echo Report:  !report_dir!\index.html
    echo.
    set /p "open_report=Open HTML report? (y/n): "
    if /i "!open_report!"=="y" start "" "!report_dir!\index.html"
) else (
    echo.
    echo ==========================================
    echo Test failed with exit code: %errorlevel%
    echo ==========================================
)

pause
goto main_menu

:invalid_input
echo.
echo Invalid input! Please enter 0-!count!
pause
goto main_menu



