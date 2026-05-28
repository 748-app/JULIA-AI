@echo off
REM JULIA AI - Windows Launch Script
REM 
REM This batch file starts JULIA AI on Windows systems.
REM It ensures Python is available and runs main.py from the correct directory.
REM
REM Usage: run.bat

echo [INFO] Starting JULIA AI...

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

REM Run the main application
python main.py

REM Pause to see output before window closes (optional)
pause
