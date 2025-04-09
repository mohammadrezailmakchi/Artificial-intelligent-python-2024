@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Move to script directory
cd /d %~dp0

REM === STEP 1: Create venv if not exists ===
if not exist "venv\Scripts\activate.bat" (
    echo [*] Creating virtual environment...
    python -m venv venv
)

REM === STEP 2: Check activation script exists ===
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Failed to create virtual environment. Exiting.
    exit /b 1
)

REM === STEP 3: Activate the virtual environment ===
call "venv\Scripts\activate.bat"
echo [✓] Virtual environment activated.

REM === STEP 4: Upgrade pip, setuptools, wheel ===
echo [*] Upgrading pip, setuptools, wheel...
python -m pip install --upgrade pip setuptools wheel

REM === STEP 5: Install requirements ===
echo [*] Installing required packages...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

REM === STEP 6: Run the main Python program ===
echo [*] Running main.py...
python main.py

echo.
echo [✓] Finished running the project.
ENDLOCAL
pause