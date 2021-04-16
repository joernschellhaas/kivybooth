@echo off

set VENV_DIR=%~dp0\..\venv\

REM Check Python version
python -c "import sys; print('Python version: {}'.format(sys.version_info)); sys.version_info[0] == 3 or sys.exit(1)"
IF NOT ERRORLEVEL 0 (
    echo."Wrong Python version"
    GOTO :die
)

REM Only create and enter venv if we are not already inside one
IF NOT DEFINED VIRTUAL_ENV (
    echo.Setting up venv...
    python -m venv %VENV_DIR% || GOTO :die
    echo.set KBOOTH_EMULATE=1 >>%VENV_DIR%\Scripts\activate.bat
    CALL %VENV_DIR%\Scripts\activate.bat || GOTO :die
)

echo.Installing pip packages...
python -m pip install -r %~dp0\requirements.txt || GOTO :die

GOTO :eof

:die 
echo.ERROR during setup, exiting.
exit /b 1
