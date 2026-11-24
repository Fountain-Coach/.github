#!/bin/sh
# FCIS canonical source-owned CI. POSIX shell on macOS/Ubuntu; no hosted CI dependency.
# This runner validates source/checkouts, not issuer/Host authority or a production release.
set -eu
ROOT=$(CDPATH= cd "$(dirname "$0")/.." && pwd -P)
cd "$ROOT"
fail() { printf 'FCIS CI REFUSED: %s\n' "$*" >&2; exit 1; }
note() { printf 'FCIS CI: %s\n' "$*"; }
require() { command -v "$1" >/dev/null 2>&1 || fail "Missing required executable: $1"; }
is_zero() {
  case "$1" in
    0000000000000000000000000000000000000000|0000000000000000000000000000000000000000000000000000000000000000) return 0 ;;
    *) return 1 ;;
  esac
}
check_commit() {
  case "$1" in
    ''|*[!0123456789abcdefABCDEF]*) fail "Invalid Git commit argument" ;;
  esac
  git cat-file -e "$1^{commit}" 2>/dev/null || fail "Unavailable Git commit: $1"
}
diff_range() {
  [ "$#" -eq 2 ] || fail "diff requires exactly BASE and HEAD revisions"
  require git
  check_commit "$1"; check_commit "$2"
  git merge-base "$1" "$2" >/dev/null || fail "No common ancestor for candidate"
  note "Formatting changed committed bytes: $1...$2"
  git diff --check "$1...$2" || fail "Committed source contains whitespace errors"
}
default_diff() {
  require git
  if [ -n "${FCIS_CI_BASE:-}" ] && [ -z "${FCIS_CI_HEAD:-}" ]; then fail "FCIS_CI_HEAD is missing for supplied base"; fi
  if [ -n "${FCIS_CI_HEAD:-}" ] && [ -z "${FCIS_CI_BASE:-}" ]; then fail "FCIS_CI_BASE is missing for supplied head"; fi
  if [ -n "${FCIS_CI_BASE:-}" ] && [ -n "${FCIS_CI_HEAD:-}" ] && ! is_zero "$FCIS_CI_BASE"; then
    diff_range "$FCIS_CI_BASE" "$FCIS_CI_HEAD"
  elif git rev-parse --verify -q 'HEAD^' >/dev/null 2>&1; then
    diff_range "$(git rev-parse 'HEAD^')" "$(git rev-parse HEAD)"
  else
    note "Single root commit: checking tracked additions"
    git diff-tree --root --check -r HEAD || fail "Root commit contains whitespace errors"
  fi
}
staged() {
  require git
  require python3
  note "Fast local commit gate: canonical skill digests and staged whitespace"
  python3 skills/skillctl.py check
  git diff --cached --check || fail "Staged source contains whitespace errors"
}
source_checks() {
  require git
  require python3
  [ -f FCIS-OPENAPI.json ] || fail "Missing canonical root OpenAPI"
  note "Validate canonical OpenAPI JSON"
  python3 -m json.tool FCIS-OPENAPI.json >/dev/null
  # Minimal disposable H2/H3 Git-hook fixtures intentionally carry no system spec.
  # If any system-spec artifact exists, require ALL artifacts and refuse drift.
  if [ -e FCIS-SYSTEM.json ] || [ -e FCIS-SYSTEM.schema.json ] || [ -e scripts/verify_fcis_system_spec.py ]; then
    [ -f FCIS-SYSTEM.json ] || fail "Missing whole-system FCIS composition"
    [ -f FCIS-SYSTEM.schema.json ] || fail "Missing whole-system FCIS schema"
    [ -f scripts/verify_fcis_system_spec.py ] || fail "Missing whole-system FCIS source validator"
    note "Validate prerequisite-free whole-system FCIS composition and source bindings"
    python3 scripts/verify_fcis_system_spec.py
  fi
  note "Validate nine maintained canonical Skill hashes and the one owner-approved active publication"
  python3 skills/skillctl.py check
  note "Validate the existing plugin with exactly one active FCIS-GO mirror"
  python3 skills/plugin_projection.py check
  note "Run source, contract and Git-hook regression suite"
  python3 -m unittest discover -s skills/tests -v
  if [ "$#" -eq 2 ]; then
    diff_range "$1" "$2"
  elif [ "$#" -eq 0 ]; then
    default_diff
  else
    fail "source accepts either no revisions or exactly BASE HEAD"
  fi
  note "SOURCE PASS (not native Go, installed owner Git or production acceptance)"
}
go_checks() {
  [ "$#" -eq 0 ] || fail "go uses pinned FCIS_CI_GO_MODULE / FCIS_CI_GO_SHA / FCIS_CI_GO_CACHE_ROOT"
  require git
  require go
  [ "$(uname -s)" = "Linux" ] || fail "Native Go CI is approved for isolated Linux/external build host only"
  [ -n "${FCIS_CI_GO_MODULE:-}" ] || fail "FCIS_CI_GO_MODULE is required (separate owned source checkout)"
  [ -n "${FCIS_CI_GO_SHA:-}" ] || fail "FCIS_CI_GO_SHA is required"
  [ -n "${FCIS_CI_GO_CACHE_ROOT:-}" ] || fail "FCIS_CI_GO_CACHE_ROOT is required"
  case "$FCIS_CI_GO_MODULE" in /*) ;; *) fail "Go module must be an absolute checked-out path" ;; esac
  case "$FCIS_CI_GO_CACHE_ROOT" in /*) ;; *) fail "Go cache root must be an absolute isolated path" ;; esac
  [ -d "$FCIS_CI_GO_CACHE_ROOT" ] || fail "Isolated Go cache root is not mounted"
  [ -f "$FCIS_CI_GO_MODULE/go.mod" ] || fail "Go module go.mod is missing"
  case "$FCIS_CI_GO_SHA" in ''|*[!0123456789abcdefABCDEF]*) fail "Invalid pinned Go revision" ;; esac
  git -C "$FCIS_CI_GO_MODULE" cat-file -e "$FCIS_CI_GO_SHA^{commit}" 2>/dev/null || fail "Pinned Go commit missing in module checkout"
  actual=$(git -C "$FCIS_CI_GO_MODULE" rev-parse HEAD) || fail "Go module checkout is not Git"
  [ "$actual" = "$FCIS_CI_GO_SHA" ] || fail "Pinned Go commit does not match checkout"
  [ -z "$(git -C "$FCIS_CI_GO_MODULE" status --porcelain)" ] || fail "Go module checkout is dirty"
  mkdir -p "$FCIS_CI_GO_CACHE_ROOT/cache" "$FCIS_CI_GO_CACHE_ROOT/path"
  cd "$FCIS_CI_GO_MODULE"
  export GOPROXY=off GOTOOLCHAIN=local GOFLAGS=-mod=readonly
  export GOCACHE="$FCIS_CI_GO_CACHE_ROOT/cache" GOPATH="$FCIS_CI_GO_CACHE_ROOT/path"
  note "Verify pinned native Go module $actual (offline)"
  go mod verify
  go vet ./...
  go test -race -count=1 ./...
  go build ./...
  note "GO PASS: source-only, no runtime/Store admission"
}
case "${1:-}" in
  staged) shift; [ "$#" -eq 0 ] || fail "staged has no arguments"; staged ;;
  diff) shift; diff_range "$@" ;;
  source) shift; source_checks "$@" ;;
  go) shift; go_checks "$@" ;;
  full) shift; source_checks; go_checks "$@" ;;
  *) fail "Usage: sh scripts/fcis-ci.sh {staged|source [BASE HEAD]|diff BASE HEAD|go|full}" ;;
esac
