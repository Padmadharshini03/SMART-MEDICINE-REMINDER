@echo off
REM Smart Medicine Reminder System - Startup Script

echo.
echo ================================================
echo  Smart Medicine Reminder System
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [✓] Python detected
echo.

REM Check if Flask is installed
python -m pip show Flask >nul 2>&1
if errorlevel 1 (
    echo [!] Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install packages
        pause
        exit /b 1
    )
)

echo [✓] All dependencies ready
echo.
echo ================================================
echo Starting Flask Server...
echo ================================================
echo.
echo Open your browser to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
