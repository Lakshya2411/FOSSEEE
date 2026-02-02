@echo off
echo ==============================================
echo Starting Backend (Django)...
echo ==============================================

cd backend

:: Check for Virtual Environment
if exist "..\.venv\Scripts\activate.bat" (
    echo Activating Virtual Environment...
    call ..\.venv\Scripts\activate.bat
) else (
    echo .venv not found! Attempting to use global python...
    echo You might need to create a venv: python -m venv .venv
)

:: Install Requirements (just in case)
echo Installing Dependencies...
pip install -r ..\backend_requirements.txt

:: Run Migrations
echo Running Migrations...
python manage.py migrate

:: Setup Admin if needed (ignores errors if exists)
python create_user.py

:: Start Server
echo Starting Server at http://127.0.0.1:8000/
python manage.py runserver

pause
