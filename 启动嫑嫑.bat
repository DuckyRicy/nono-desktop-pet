@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  start "" pyw nono.py
) else (
  start "" pythonw nono.py
)
