#!/usr/bin/env bash
# Start Glassbench on Mac or Linux: http://127.0.0.1:8765  (./glassbench.sh --build rebuilds the frontend first)
set -e
here="$(cd "$(dirname "$0")" && pwd)"
export PYTHONUTF8=1
if [ "$1" = "--build" ] || [ ! -f "$here/frontend/dist/index.html" ]; then
  (cd "$here/frontend" && npm run build)
fi
cd "$here/backend" && "$here/.venv/bin/python" -m deskapp serve
