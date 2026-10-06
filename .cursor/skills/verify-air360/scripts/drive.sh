#!/usr/bin/env bash
# Run drive.py with the verify-air360 venv. See drive.sh --help for the step list.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
[ -x "$PY" ] || { echo "error: $PY missing. Run $(dirname "$0")/setup.sh first." >&2; exit 1; }
exec "$PY" "$SKILL_DIR/scripts/drive.py" "$@"
