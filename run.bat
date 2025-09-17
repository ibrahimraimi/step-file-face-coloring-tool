@echo off
:: Run script for STEP File Face Coloring Tool
:: This script ensures the application runs from the correct directory

setlocal enabledelayedexpansion

:: Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

:: Change to the script directory
cd /d "%SCRIPT_DIR%"

:: Check if Python is available
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not found in PATH.
    echo Please ensure Python is installed and added to your system PATH.
    pause
    exit /b 1
)

:: Run the application
echo Starting STEP File Face Coloring Tool...
python "%SCRIPT_DIR%main.py" %*

:: If the above fails, try with python3
if %ERRORLEVEL% neq 0 (
    echo Trying with python3...
    python3 "%SCRIPT_DIR%main.py" %*
)

:: Pause if there was an error
if %ERRORLEVEL% neq 0 (
    echo.
    echo Application failed to start. Please check the error message above.
    pause
    exit /b %ERRORLEVEL%
)

exit /b 0
