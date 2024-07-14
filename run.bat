@echo off
REM Save current directory
set CURRENT_DIR=%cd%

REM Change directory to a specific folder, e.g., Desktop
cd /d %USERPROFILE%\Desktop

REM Check Python version
python --version >nul 2>&1

if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and rerun this script.
    exit /b 1
)

REM Get the Python version
FOR /F "tokens=2 delims= " %%a in ('python --version') DO SET PYTHON_VERSION=%%a

echo Python is already installed.
echo Python version: %PYTHON_VERSION%

REM Restore the original directory
cd %CURRENT_DIR%

REM Define the name of the virtual environment
set VENV_DIR=projectenv
REM Define the requirements file
set REQUIREMENTS_FILE=requirements.txt


REM Get the directory of the batch file
set SCRIPT_DIR=%~dp0

REM Check if the virtual environment already exists
if exist %SCRIPT_DIR%%VENV_DIR%\Scripts\activate (
    echo Virtual environment '%VENV_DIR%' already exists.
    
    REM Activate the virtual environment
    call %VENV_DIR%\Scripts\activate

    REM Check if the required packages are installed
    pip check >nul 2>&1
    if %errorlevel%==0 (
        echo All required packages are already installed.
    ) else (
        echo Installing packages from '%REQUIREMENTS_FILE%'...
        pip install -r %SCRIPT_DIR%%REQUIREMENTS_FILE%
    )


) else (
    REM Create the virtual environment
    python -m venv %SCRIPT_DIR%%VENV_DIR%
    echo Virtual environment '%VENV_DIR%' created.

    REM Activate the virtual environment
    call %SCRIPT_DIR%%VENV_DIR%\Scripts\activate

    REM Install the required packages
    echo Installing packages from '%REQUIREMENTS_FILE%'...
    pip install -r %SCRIPT_DIR%%REQUIREMENTS_FILE%
)

REM Run module 'HandTrackingModule.py' in module directory
cd %CURRENT_DIR%/module
python HandTrackingModule.py

pause