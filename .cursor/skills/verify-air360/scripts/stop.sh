#!/usr/bin/env bash
# Stop the server this run started (by PID file, never by name) and remove scratch state.
# Evidence under .verify-evidence/air360/<run-id>/ is kept; the server log is copied there first.
# Usage: stop.sh [run-id]
set -uo pipefail
source "$(dirname "$0")/lib.sh"
resolve_run "${1:-}" || exit 2
if [ ! -d "$STATE_DIR" ]; then
  echo "nothing to stop: $STATE_DIR does not exist"
  exit 0
fi
PIDFILE="$STATE_DIR/server.pid"
if [ -f "$PIDFILE" ]; then
  PID="$(cat "$PIDFILE")"
  # Only kill the pid if it is still the http.server we launched for this port.
  if kill -0 "$PID" 2>/dev/null && tr '\0' ' ' <"/proc/$PID/cmdline" | grep -q "http.server $(cat "$STATE_DIR/port")"; then
    kill "$PID"
    for _ in $(seq 1 25); do kill -0 "$PID" 2>/dev/null || break; sleep 0.2; done
    kill -0 "$PID" 2>/dev/null && kill -9 "$PID"
    echo "stopped server pid $PID"
  else
    echo "server pid $PID is not running (or is no longer our http.server); not killing anything"
  fi
fi
mkdir -p "$EVIDENCE_DIR"
[ -f "$STATE_DIR/server.log" ] && cp "$STATE_DIR/server.log" "$EVIDENCE_DIR/server.log"
rm -rf "$STATE_DIR"
echo "removed scratch state $STATE_DIR"
echo "evidence kept at $EVIDENCE_DIR"
