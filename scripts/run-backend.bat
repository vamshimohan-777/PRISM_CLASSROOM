@echo off
cd /d "%~dp0..\backend"
echo [PRISM CLASSROOM] Starting FastAPI Backend on http://127.0.0.1:8000 ...
.\.venv\Scripts\uvicorn.exe app.main:app --reload --port 8000
pause

