#!/usr/bin/env bash
# Serve the repo root on 127.0.0.1 with python's http.server on a free port.
# Usage: start.sh [run-id]    Prints RUN_ID, URL, STATE, EVIDENCE as shell assignments.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
RUN_ID="${1:-$(date +%Y%m%d-%H%M%S)-$$}"
STATE_DIR="$STATE_ROOT/$RUN_ID"
EVIDENCE_DIR="$EVIDENCE_ROOT/$RUN_ID"
if [ -e "$STATE_DIR/server.pid" ]; then
  echo "error: run $RUN_ID already has a server (pid $(cat "$STATE_DIR/server.pid")). Use a new run id or stop.sh $RUN_ID." >&2
  exit 1
fi
if [ ! -x "$PY" ]; then
  echo "error: $PY missing. Run $(dirname "$0")/setup.sh first." >&2
  exit 1
fi
mkdir -p "$STATE_DIR" "$EVIDENCE_DIR"

# First free port at or above 4360 (8000, http.server's default, is avoided on purpose).
PORT="${VERIFY_AIR360_PORT:-$("$PY" - <<'PYEOF'
import socket
for port in range(4360, 4460):
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", port))
    except OSError:
        continue
    finally:
        s.close()
    print(port)
    break
PYEOF
)}"
URL="http://127.0.0.1:$PORT"

nohup python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$REPO_ROOT" \
  >"$STATE_DIR/server.log" 2>&1 &
echo $! >"$STATE_DIR/server.pid"
echo "$PORT" >"$STATE_DIR/port"
echo "$URL" >"$STATE_DIR/url"

# Fixture photos for the import flow live in scratch state, not in the repo.
"$PY" "$SKILL_DIR/scripts/make-fixtures.py" "$STATE_DIR/fixtures" >/dev/null

# Ready when GET /360/ returns the Air360 title. The site root is the Waypoint homepage. Fail fast if the server exits.
for _ in $(seq 1 50); do
  if ! kill -0 "$(cat "$STATE_DIR/server.pid")" 2>/dev/null; then
    echo "error: server exited. Log:" >&2; cat "$STATE_DIR/server.log" >&2; exit 1
  fi
  if curl -fsS "$URL/360/" 2>/dev/null | grep -q '<title>Air360 • DJI 360 Viewer</title>'; then
    echo "RUN_ID=$RUN_ID"
    echo "URL=$URL"
    echo "STATE=$STATE_DIR"
    echo "EVIDENCE=$EVIDENCE_DIR"
    exit 0
  fi
  sleep 0.2
done
echo "error: $URL/360/ never served the Air360 page within 10s. Log:" >&2
cat "$STATE_DIR/server.log" >&2
exit 1
