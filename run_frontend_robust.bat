@echo off
echo ==============================================
echo Building and Serving Frontend...
echo ==============================================

cd frontend-web

echo Building React App...
cmd /c "npm run build"

echo Starting Static Server at http://127.0.0.1:5173/
python -m http.server 5173 --directory dist

pause
