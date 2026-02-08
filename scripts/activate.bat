@echo off
REM Activate script for Dimensionics Framework virtual environment
REM Usage: scripts\activate.bat

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "VENV_PATH=%PROJECT_ROOT%\venv"

if not exist "%VENV_PATH%" (
    echo Error: Virtual environment not found at %VENV_PATH%
    echo Run: python setup_env.py
    exit /b 1
)

if exist "%VENV_PATH%\Scripts\activate.bat" (
    call "%VENV_PATH%\Scripts\activate.bat"
    echo Virtual environment activated
    for /f "tokens=*" %%a in ('python --version') do set PYTHON_VER=%%a
    echo Python: %PYTHON_VER%
    
    REM Add src to PYTHONPATH
    set "PYTHONPATH=%PROJECT_ROOT%\src;%PYTHONPATH%"
    echo PYTHONPATH updated
) else (
    echo Error: Could not find activation script
    exit /b 1
)
