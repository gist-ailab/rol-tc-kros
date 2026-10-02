#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
port=8000
if ! python3 -c 'import socket; s=socket.socket(); s.bind(("", 8000)); s.close()' 2>/dev/null; then
  port=8001
fi

echo "로컬 미리보기: http://localhost:${port}/"
exec python3 -m http.server "$port"
