@echo off
:: Windows Setup Script for STEP File Face Coloring Tool
:: This script will install Python, required dependencies, and set up the environment

setlocal enabledelayedexpansion

:: Set variables
set "PYTHON_VERSION=3.10.11"
set "PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe"
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%"
set "PYTHON_PATH=C:\Python310"
set "PIP_PATH=%PYTHON_PATH%\Scripts\pip.exe"
set "PYTHON_EXE=%PYTHON_PATH%\python.exe"
set "REQUIREMENTS=requirements.txt"
set "APP_ENTRY=main.py"

:: Check if running as administrator
net session >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo Running with administrator privileges
) else (
    echo Please run this script as administrator
    echo Right-click on setup.bat and select "Run as administrator"
    pause
    exit /b 1
)

:: Check if Python is already installed
echo Checking Python installation...
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Python is already installed.
    for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1 ^| findstr /i "Python"') do set PYTHON_VERSION_INSTALLED=%%a
    echo Installed Python version: %PYTHON_VERSION_INSTALLED%
) else (
    echo Python is not installed. Downloading Python %PYTHON_VERSION%...
    
    :: Download Python installer
    echo Downloading Python installer...
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%PYTHON_URL%', '%PYTHON_INSTALLER%')"
    if not exist "%PYTHON_INSTALLER%" (
        echo Failed to download Python installer.
        exit /b 1
    )
    
    :: Install Python
    echo Installing Python...
    start /wait "" "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 TargetDir="%PYTHON_PATH%"
    
    :: Clean up installer
    del /f "%PYTHON_INSTALLER%"
    
    :: Verify Python installation
    if not exist "%PYTHON_EXE%" (
        echo Python installation failed. Please install Python %PYTHON_VERSION% manually.
        exit /b 1
    )
    
    echo Python installed successfully.
)

:: Install/upgrade pip
echo Updating pip...
"%PYTHON_EXE%" -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
    echo Failed to update pip.
    exit /b 1
)

:: Install required packages
echo Installing required packages...
"%PIP_PATH%" install -r "%REQUIREMENTS%"
if %ERRORLEVEL% neq 0 (
    echo Failed to install required packages.
    exit /b 1
)

:: Create desktop shortcut
echo Creating desktop shortcut...
set "SHORTCUT=%USERPROFILE%\Desktop\STEP File Face Coloring Tool.lnk"
set "ICON_PATH=%CD%\icon.ico"

:: Check if icon exists, if not, create a default one
if not exist "%ICON_PATH%" (
    echo Creating default icon...
    echo [.ShellClassInfo] > "%TEMP%\desktop.ini"
    echo IconResource=%%SystemRoot%%\System32\SHELL32.dll,15 >> "%TEMP%\desktop.ini"
    attrib +s +h "%TEMP%\desktop.ini"
    set "ICON_PATH=%%SystemRoot%%\System32\SHELL32.dll,15"
)

powershell -command "
$WshShell = New-Object -comObject WScript.Shell;
$Shortcut = $WshShell.CreateShortcut('%SHORTCUT%');
$Shortcut.TargetPath = '%PYTHON_EXE%';
$Shortcut.Arguments = '\"%CD%\%APP_ENTRY%\"';
$Shortcut.WorkingDirectory = '%CD%';
$Shortcut.IconLocation = '%ICON_PATH%';
$Shortcut.WindowStyle = 1;
$Shortcut.Description = 'STEP File Face Coloring Tool';
$Shortcut.Save()
"

if exist "%SHORTCUT%" (
    echo Desktop shortcut created successfully.
) else (
    echo Failed to create desktop shortcut.
)

:: Create run script
@echo @echo off > "run.bat"
@echo "%PYTHON_EXE%" "%CD%\%APP_ENTRY%" %%* >> "run.bat"

:: Display completion message
echo.
echo ===================================================
echo  Setup completed successfully!
echo  You can now run the application by:
echo  1. Double-clicking the desktop shortcut, or
echo  2. Double-clicking run.bat in the application folder
echo ===================================================

pause
