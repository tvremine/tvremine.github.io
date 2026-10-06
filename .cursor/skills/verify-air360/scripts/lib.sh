# Shared paths for the verify-air360 helpers. Sourced, not executed.
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"
VENV="${VERIFY_AIR360_VENV:-$HOME/.cache/verify-air360/venv}"
PY="$VENV/bin/python"
STATE_ROOT="${VERIFY_AIR360_STATE:-${TMPDIR:-/tmp}/verify-air360}"
EVIDENCE_ROOT="$REPO_ROOT/.verify-evidence/air360"

# Resolve the run id from $1 or $VERIFY_AIR360_RUN and set STATE_DIR.
resolve_run() {
  RUN_ID="${1:-${VERIFY_AIR360_RUN:-}}"
  if [ -z "$RUN_ID" ]; then
    echo "error: pass a run id or set VERIFY_AIR360_RUN (start.sh prints it)" >&2
    return 2
  fi
  STATE_DIR="$STATE_ROOT/$RUN_ID"
  EVIDENCE_DIR="$EVIDENCE_ROOT/$RUN_ID"
}
