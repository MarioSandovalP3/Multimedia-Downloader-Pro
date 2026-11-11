@echo off
cd /d "%~dp0"
py -m pip install -U "yt-dlp[default]"
if errorlevel 1 (
  echo No se pudieron instalar las dependencias.
  pause
  exit /b 1
)
py app.py
pause
