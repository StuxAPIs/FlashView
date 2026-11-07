@echo off
setlocal
REM FlashView - Local dev server (Windows)
REM Usage: dev-server.bat [port] [--no-dev-mode]
REM   port            default: 8000
REM   --no-dev-mode   serve the site exactly as production does (no "local dev" banner)
REM Fetches the pinned Ruffle into ruffle\ if it's missing (needs Git Bash's bash on PATH), then serves
REM the repo root.

set "DIR=%~dp0"
set "PORT=8000"
set "DEV_MODE=1"
:args
if "%~1"=="" goto run
if /i "%~1"=="--no-dev-mode" (set "DEV_MODE=0") else (set "PORT=%~1")
shift
goto args

:run
bash "%DIR%scripts\fetch-ruffle.sh"
if errorlevel 1 exit /b 1
echo Serving %DIR% at http://127.0.0.1:%PORT% (DEV_MODE=%DEV_MODE%)
python -I "%DIR%scripts\dev-server.py" "%DIR%." %PORT%
