#!/usr/bin/env bash
# ============================================================
#  Khởi động nhanh muse2api (bản dịch tiếng Việt) — macOS / Linux
#  - Đọc MUSE2API_PORT và MUSE2API_KEY từ .env
#  - Tự tạo venv và cài dependencies nếu thiếu
#  - Nếu server đã chạy sẵn thì chỉ mở trang quản trị
#  - Thêm tham số --nobrowser để không tự mở trình duyệt
# ============================================================
set -euo pipefail

cd "$(dirname "$0")"

read_env() {
  local key="$1" def="$2" line
  line=$(grep -E "^${key}=" .env 2>/dev/null | tail -n 1 || true)
  line=${line#*=}
  line=${line%$'\r'}
  printf '%s' "${line:-$def}"
}

PORT=$(read_env MUSE2API_PORT 18610)
API_KEY=$(read_env MUSE2API_KEY "")
HOST=127.0.0.1

URL="http://127.0.0.1:${PORT}/"
[ -n "$API_KEY" ] && URL="${URL}?key=${API_KEY}"

open_browser() {
  if command -v open >/dev/null 2>&1; then
    open "$URL"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$URL" >/dev/null 2>&1
  fi
}

NOBROWSER=0
[ "${1:-}" = "--nobrowser" ] && NOBROWSER=1

PY=venv/bin/python
if [ ! -x "$PY" ]; then
  echo "[1/2] Chưa có venv, đang tạo..."
  python3 -m venv venv
  echo "[2/2] Đang cài dependencies..."
  "$PY" -m pip install --disable-pip-version-check -q -r requirements.txt
fi

if curl -sf --max-time 2 "http://127.0.0.1:${PORT}/healthz" >/dev/null 2>&1; then
  echo "Server đã chạy sẵn: $URL"
  [ "$NOBROWSER" -eq 1 ] || open_browser
  exit 0
fi

echo "Đang khởi động muse2api: http://127.0.0.1:${PORT}"
echo "Nhấn Ctrl+C để dừng server."
echo

if [ "$NOBROWSER" -eq 0 ]; then
  (
    for _ in $(seq 1 60); do
      if curl -sf --max-time 1 "http://127.0.0.1:${PORT}/healthz" >/dev/null 2>&1; then
        open_browser
        break
      fi
      sleep 0.5
    done
  ) &
fi

export PYTHONIOENCODING=utf-8
export PYTHONUTF8=1
exec "$PY" -m uvicorn app:app --host "$HOST" --port "$PORT"
