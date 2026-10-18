@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"

rem ============================================================
rem  Khởi động nhanh muse2api (bản dịch tiếng Việt)
rem  - Đọc MUSE2API_PORT và MUSE2API_KEY từ .env
rem  - Tự tạo venv và cài dependencies nếu thiếu
rem  - Nếu server đã chạy sẵn thì chỉ mở trang quản trị
rem  - Thêm tham số /nobrowser để không tự mở trình duyệt
rem ============================================================

set "HOST=127.0.0.1"
set "PORT=18610"
set "API_KEY="

if exist ".env" (
  for /f "usebackq eol=# tokens=1,* delims==" %%A in (".env") do (
    if /i "%%A"=="MUSE2API_PORT" set "PORT=%%B"
    if /i "%%A"=="MUSE2API_KEY" set "API_KEY=%%B"
  )
)

set "PY=.\venv\Scripts\python.exe"
if not exist "%PY%" (
  echo [1/2] Chưa có venv, đang tạo...
  python -m venv venv
  if errorlevel 1 goto :fail
  echo [2/2] Đang cài dependencies...
  "%PY%" -m pip install --disable-pip-version-check -q -r requirements.txt
  if errorlevel 1 goto :fail
)

set "URL=http://127.0.0.1:%PORT%/"
if defined API_KEY set "URL=http://127.0.0.1:%PORT%/?key=%API_KEY%"

curl -s -o nul --max-time 2 "http://127.0.0.1:%PORT%/healthz" >nul 2>&1
if not errorlevel 1 (
  echo Server đã chạy sẵn: %URL%
  if /i not "%~1"=="/nobrowser" start "" "%URL%"
  exit /b 0
)

echo Đang khởi động muse2api: http://127.0.0.1:%PORT%
echo Nhấn Ctrl+C để dừng server.
echo.

if /i not "%~1"=="/nobrowser" (
  start "" /b powershell -NoProfile -WindowStyle Hidden -Command "for($i=0;$i -lt 60;$i++){try{Invoke-WebRequest -UseBasicParsing -TimeoutSec 1 'http://127.0.0.1:%PORT%/healthz'|Out-Null; Start-Process '%URL%'; break}catch{Start-Sleep -Milliseconds 500}}"
)

set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"
"%PY%" -m uvicorn app:app --host %HOST% --port %PORT%
exit /b %errorlevel%

:fail
echo Khởi động thất bại.
pause
exit /b 1
