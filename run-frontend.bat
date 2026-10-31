@echo off
cd /d "%~dp0frontend"
echo [PRISM CLASSROOM] Starting React Frontend on http://localhost:5173 ...
call npm.cmd run dev
pause

