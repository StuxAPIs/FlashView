@echo off
setlocal
REM FlashView - Local dev server (Windows)
REM Usage: dev-server.bat [port] [--no-dev-mode] [--lan]
REM   port            default: 8000
REM   --no-dev-mode   serve the site exactly as production does (no "local dev" banner)
REM   --lan           listen on all interfaces so phones/tablets on your network can
REM                   connect (prints the addresses to open); default is 127.0.0.1 only
REM Fetches the pinned Ruffle into ruffle\ if it's missing (needs Git Bash's bash on PATH), then serves
REM the repo root.

set "DIR=%~dp0"
set "PORT=8000"
set "DEV_MODE=1"
set "HOST=127.0.0.1"
:args
if "%~1"=="" goto run
if /i "%~1"=="--no-dev-mode" (
    set "DEV_MODE=0"
    shift
    goto args
)
if /i "%~1"=="--lan" (
    set "HOST=0.0.0.0"
    shift
    goto args
)
echo %~1| findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo Unknown argument: %~1
    echo Usage: dev-server.bat [port] [--no-dev-mode] [--lan]
    exit /b 1
)
set "PORT=%~1"
shift
goto args

:run
bash "%DIR%scripts\fetch-ruffle.sh"
if errorlevel 1 exit /b 1
echo Serving %DIR% at http://127.0.0.1:%PORT% (DEV_MODE=%DEV_MODE%)
if "%HOST%"=="0.0.0.0" (
    echo On your local network ^(--lan^), open one of these on the other device:
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
        for /f "tokens=* delims= " %%b in ("%%a") do echo     http://%%b:%PORT%
    )
    echo   ^(usually the 192.168.x.x one; allow Python through the firewall if asked^)
)
python -I "%DIR%scripts\dev-server.py" "%DIR%." %PORT% %HOST%
