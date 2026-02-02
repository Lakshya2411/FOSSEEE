@echo off
echo ==============================================
echo Starting Frontend (React/Vite) on Port 5173...
echo ==============================================

cd frontend-web

:: Install Node Modules if missing
if not exist "node_modules" (
    echo node_modules not found. Installing dependencies...
    cmd /c "npm install"
)

:: Start Dev Server
echo Starting Frontend...
echo Please wait for "Local: http://127.0.0.1:5173/" to appear.
cmd /c "npm run dev"

pause
