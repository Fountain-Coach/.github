#!/bin/sh
# Owner-controlled Git disaster recovery; never needs GitHub, a plugin, or an API.
set -eu
ROOT=$(CDPATH= cd "$(dirname "$0")/.." && pwd -P)
cd "$ROOT"
fail() { printf 'FCIS recovery ERROR: %s\n' "$*" >&2; exit 1; }
note() { printf 'FCIS recovery: %s\n' "$*"; }
cfg() { git config --local --get "fcis.$1" || :; }
absolute() { case "$1" in /*) ;; *) fail "An absolute local path is required: $1";; esac; }
mounted() { [ -z "$1" ] || mount | grep -F " on $1 (" >/dev/null 2>&1; }
load_config() {
  BARE=$(cfg recoveryBare); BUNDLES=$(cfg recoveryBundles); MOUNT=$(cfg recoveryMount)
  [ -n "$BARE" ] && [ -n "$BUNDLES" ] || fail "Recovery locations not configured"
  absolute "$BARE"; absolute "$BUNDLES"
  [ -z "$MOUNT" ] || absolute "$MOUNT"
  [ -f "$BARE/HEAD" ] || fail "Missing bare repository: $BARE"
}
latest_bundle() {
  [ -f "$BUNDLES/LATEST" ] || fail "Missing latest bundle index"
  name=$(cat "$BUNDLES/LATEST")
  case "$name" in *.bundle) ;; *) fail "Invalid backup filename";; esac
  case "$name" in */*|*..*) fail "Unsafe backup filename";; esac
  printf '%s/%s\n' "$BUNDLES" "$name"
}
verify_bundle() {
  bundle=$1
  [ -f "$bundle" ] && [ -f "$bundle.sha256" ] || fail "Missing bundle or SHA-256 file"
  expected=$(cat "$bundle.sha256")
  actual=$(shasum -a 256 "$bundle" | awk '{print $1}')
  [ "$expected" = "$actual" ] || fail "Backup checksum mismatch"
  checkdir=$(mktemp -d "${TMPDIR:-/tmp/}fcis-restore.XXXXXXXX")
  git init -q --bare "$checkdir/empty.git"
  if ! git --git-dir="$checkdir/empty.git" bundle verify "$bundle" >/dev/null 2>&1; then
    rm -rf "$checkdir"; fail "Bundle requires unavailable Git objects"
  fi
  if ! git clone -q --mirror "$bundle" "$checkdir/restored.git" ||
     ! git --git-dir="$checkdir/restored.git" fsck --full --no-reflogs >/dev/null 2>&1; then
    rm -rf "$checkdir"; fail "Offline clone or repository validation failed"
  fi
  rm -rf "$checkdir"
  note "Independent offline Git bundle restore verified: $bundle"
}
require_full_history() {
  [ "$(git rev-parse --is-shallow-repository)" = false ] ||
    fail "Shallow Git history is incomplete; obtain a full clone before accepting a disaster backup"
}
case "${1:-}" in
  setup)
    require_full_history
    [ "$#" -ge 3 ] && [ "$#" -le 4 ] || fail "Usage: $0 setup ABSOLUTE_BARE_GIT ABSOLUTE_BUNDLE_DIR [EXTERNAL_MOUNT]"
    bare=$2; bundles=$3; mount_root=${4:-}
    absolute "$bare"; absolute "$bundles"
    [ -z "$mount_root" ] || absolute "$mount_root"
    mounted "$mount_root" || fail "External drive not mounted: $mount_root"
    [ ! -e "$bare" ] || [ -f "$bare/HEAD" ] || fail "Bare repository path already occupied"
    mkdir -p "$(dirname "$bare")" "$bundles"
    if [ ! -e "$bare/HEAD" ]; then git init -q --bare "$bare"; fi
    git config --local fcis.recoveryBare "$bare"
    git config --local fcis.recoveryBundles "$bundles"
    if [ -n "$mount_root" ]; then
      git config --local fcis.recoveryMount "$mount_root"
    else
      git config --local --unset-all fcis.recoveryMount >/dev/null 2>&1 || :
    fi
    git config --local core.hooksPath .githooks
    note "Version-controlled hooks configured for this local Git clone"
    exec "$0" snapshot
    ;;
  snapshot)
    require_full_history
    load_config
    status=0
    # Dedicated mirror is one-way. To work from it after a disaster, clone it first.
    if git -c core.hooksPath=/dev/null push --mirror --quiet "$BARE"; then
      # Bare repos created with git init may still point HEAD to nonexistent master.
      if git --git-dir="$BARE" show-ref --verify --quiet refs/heads/main; then
        git --git-dir="$BARE" symbolic-ref HEAD refs/heads/main
      fi
      note "Bare Git recovery mirror updated"
    else
      printf 'FCIS recovery WARNING: bare mirror failed\n' >&2; status=1
    fi
    if ! mounted "$MOUNT"; then
      printf 'FCIS recovery WARNING: external mount unavailable (%s)\n' "$MOUNT" >&2
      status=1
    else
      mkdir -p "$BUNDLES"
      stamp=$(date -u '+%Y%m%dT%H%M%SZ')
      short=$(git rev-parse --short=12 HEAD)
      name="fcis-${stamp}-${short}-$$.bundle"
      temp=$(mktemp -d "$BUNDLES/.pending.XXXXXXXX")
      if git bundle create "$temp/snapshot.bundle" --all &&
         git bundle verify "$temp/snapshot.bundle" >/dev/null 2>&1; then
        mv "$temp/snapshot.bundle" "$BUNDLES/$name"
        shasum -a 256 "$BUNDLES/$name" | awk '{print $1}' > "$BUNDLES/$name.sha256"
        printf '%s\n' "$name" > "$temp/LATEST"
        mv "$temp/LATEST" "$BUNDLES/LATEST"
        note "Portable Git bundle saved: $BUNDLES/$name"
      else
        printf 'FCIS recovery WARNING: Git bundle failed\n' >&2; status=1
      fi
      rmdir "$temp" 2>/dev/null || :
    fi
    exit "$status"
    ;;
  verify)
    load_config
    git --git-dir="$BARE" fsck --full --no-reflogs >/dev/null 2>&1 ||
      fail "Bare mirror failed git fsck"
    note "Bare mirror passed git fsck"
    mounted "$MOUNT" || fail "External mount unavailable"
    verify_bundle "$(latest_bundle)"
    ;;
  *) fail "Usage: $0 {setup|snapshot|verify}";;
esac
