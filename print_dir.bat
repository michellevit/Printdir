@echo off
setlocal ENABLEDELAYEDEXPANSION

:: Use UTF-8 in this console so box-drawing chars render correctly
chcp 65001 >nul

:: Run from the folder where this .bat lives
cd /d "%~dp0"

:: Ensure Python is available
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found on PATH.
  echo Install Python or add it to PATH: https://www.python.org/downloads/
  echo.
  pause
  exit /b 1
)

echo ===============================
echo   Folder Tree Generator
echo ===============================
echo.
echo Tip: Enter a full path, a relative path, or just a project name.
echo If a project name is entered, it will search in:
echo   C:\Users\Michelle\Documents\Coding_Projects
echo.

set "USER_INPUT="
set /p USER_INPUT=Enter target (path or project name) [current folder]: 
if "%USER_INPUT%"=="" set "USER_INPUT=."

echo.
echo Running...
echo.

:: Temp file to capture UTF-8 output
set "tmpfile=%TEMP%\dir_output_%RANDOM%.txt"

:: Call python; it writes UTF-8 to --output-file and also prints to console
python "print_dir.py" "%USER_INPUT%" --output-file "!tmpfile!"
set "rc=%ERRORLEVEL%"

:: Copy using PowerShell to preserve UTF-8 (more reliable than clip.exe)
if exist "!tmpfile!" (
  powershell -NoLogo -NoProfile -Command ^
    "Get-Content -Raw -Encoding UTF8 '%tmpfile%' | Set-Clipboard"
  echo (Copied to clipboard)
)

:: --- OPTIONAL: also save to a timestamped file (uncomment to enable) ---
:: for /f "tokens=1-3 delims=/ " %%a in ("%date%") do set d=%%c-%%a-%%b
:: for /f "tokens=1-2 delims=:." %%a in ("%time%") do set t=%%a-%%b
:: set "outfile=tree-!d!_!t!.txt"
:: copy /y "!tmpfile!" "!outfile!" >nul
:: echo Saved output to "!outfile!"

:: Clean up
del /q "!tmpfile!" >nul 2>nul

echo.
if "%rc%"=="0" (
  echo Done. Press any key to close.
) else (
  echo Finished with exit code %rc%. Press any key to close.
)
pause >nul
endlocal
