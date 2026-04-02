@echo off
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
    echo ERROR: No Windows venv found. Run:
    echo   py -3.11 -m venv venv
    echo   venv\Scripts\pip install -r requirements.txt
    echo   venv\Scripts\python manage.py migrate
    pause
    exit /b 1
)
echo Open http://127.0.0.1:8000 in your browser
"venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
pause
