#!/usr/bin/env bash
# Read-only health check: is this run's Air360 instance worth driving?
# Usage: doctor.sh [run-id]    Exit 0 when every check passes.
set -uo pipefail
source "$(dirname "$0")/lib.sh"
resolve_run "${1:-}" || exit 2
fail=0
check() { # check "label" command...
  local label="$1"; shift
  if out="$("$@" 2>&1)"; then echo "OK   $label${out:+: $out}"; else echo "FAIL $label${out:+: $out}"; fail=1; fi
}

check "state dir $STATE_DIR" test -f "$STATE_DIR/server.pid"
PID="$(cat "$STATE_DIR/server.pid" 2>/dev/null || echo none)"
PORT="$(cat "$STATE_DIR/port" 2>/dev/null || echo none)"
URL="$(cat "$STATE_DIR/url" 2>/dev/null || echo none)"

check "server pid $PID alive" kill -0 "$PID"
check "pid $PID is our http.server on $PORT serving $REPO_ROOT" bash -c \
  "tr '\0' ' ' </proc/$PID/cmdline | grep -q 'http.server $PORT --bind 127.0.0.1 --directory $REPO_ROOT'"
check "port $PORT listening, owned by pid $PID" bash -c \
  "ss -ltnpH 'sport = :$PORT' | grep -q 'pid=$PID,'"
check "GET $URL/ shows the Waypoint Aerial homepage" bash -c \
  "curl -fsS '$URL/' | grep -q '<title>Waypoint Aerial — Precision from above.</title>'"
check "GET $URL/360/ shows the Air360 title" bash -c \
  "curl -fsS '$URL/360/' | grep -q '<title>Air360 • DJI 360 Viewer</title>'"
check "served 360/index.html matches the checkout" bash -c \
  "[ \"\$(curl -fsS '$URL/360/index.html' | sha256sum)\" = \"\$(sha256sum <'$REPO_ROOT/360/index.html')\" ] && git -C '$REPO_ROOT' rev-parse --short HEAD"
check "360/manifest.json parses, short_name Air360" bash -c \
  "curl -fsS '$URL/360/manifest.json' | python3 -c 'import json,sys; assert json.load(sys.stdin)[\"short_name\"]==\"Air360\"'"
check "fixtures present" bash -c "ls '$STATE_DIR/fixtures/sphere-2to1.jpg' '$STATE_DIR/fixtures/wide-4to1.jpg' '$STATE_DIR/fixtures/photo-4to3.jpg' >/dev/null"
# The page loads Tailwind and Pannellum from CDNs. Without them it renders unstyled and the viewer fails.
check "CDN cdn.tailwindcss.com reachable" curl -fsSL -o /dev/null --max-time 10 https://cdn.tailwindcss.com
check "CDN pannellum 2.5.7 reachable" curl -fsS -o /dev/null --max-time 10 https://cdn.jsdelivr.net/npm/pannellum@2.5.7/build/pannellum.js
check "Playwright Chromium usable from $VENV" "$PY" -c \
  "from playwright.sync_api import sync_playwright as s; p=s().start(); b=p.chromium.launch(); print(b.version); b.close(); p.stop()"

[ "$fail" = 0 ] && echo "doctor: healthy ($URL, run $RUN_ID)" || echo "doctor: NOT healthy, do not drive this instance"
exit "$fail"
