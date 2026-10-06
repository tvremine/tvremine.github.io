#!/usr/bin/env bash
# One-time setup: a venv with Playwright and Pillow, plus Playwright's Chromium.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
if [ ! -x "$PY" ]; then
  python3 -m venv "$VENV"
fi
"$PY" -m pip install -q --upgrade playwright pillow
"$PY" -m playwright install chromium
"$PY" -c "import playwright, PIL; print('setup ok:', '$VENV')"
