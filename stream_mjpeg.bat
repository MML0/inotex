@echo off
:: Check if FFmpeg is installed
where ffmpeg >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo FFmpeg is not installed or not in PATH. Please install it.
    pause
    exit /b
)

:: Check if 10min.mp4 exists
if not exist "10min.mp4" (
    echo 10min.mp4 not found in the current directory.
    pause
    exit /b
)

:: Run FFmpeg to stream MJPEG over HTTP
ffmpeg -i 10min.mp4 ^
  -vf fps=15 ^
  -q:v 2 ^
  -f mjpeg ^
  -http_persistent 1 ^
  -http_multiple 1 ^
  -listen 1 ^
  http://0.0.0.0:8080/stream.mjpg

pause 