#!/bin/sh
# FCIS H3 owner-side signing helper. Run only where the owner's signing key lives.
# This command never contacts, installs or changes the receiving Git server.
set -eu
umask 077
fail() { printf 'FCIS approval REFUSED: %s\n' "$*" >&2; exit 1; }
[ "$#" -eq 7 ] || fail 'usage: fcis-git-approve.sh PRIVATE_KEY REPOSITORY_ID CANDIDATE_REF CANDIDATE_SHA EXPECTED_MAIN_SHA POLICY_SHA256 OUT_FILE'
key=$1 repo=$2 candidate=$3 wanted=$4 old=$5 policysha=$6 output=$7
[ -f "$key" ] && [ ! -L "$key" ] || fail 'owner signing key unavailable'
[ -n "$repo" ] || fail 'repository identity missing'
case "$candidate" in refs/heads/candidates/*) ;; *) fail 'only candidate refs may be approved' ;; esac
case "$candidate" in refs/heads/candidates/*/*) fail 'nested candidate refs forbidden' ;; esac
case "${candidate#refs/heads/candidates/}" in ''|*[!a-zA-Z0-9._-]*) fail 'unsafe candidate ref' ;; esac
sha() {
    case "$1" in ''|*[!0123456789abcdef]*) return 1 ;; esac
    case "${#1}" in 40|64) return 0 ;; *) return 1 ;; esac
}
sha "$wanted" && sha "$old" || fail 'full candidate and predecessor SHA required'
case "$policysha" in ''|*[!0123456789abcdef]*) fail 'invalid policy SHA-256' ;; esac
[ "${#policysha}" -eq 64 ] || fail 'policy SHA-256 must have 64 hex digits'
case "$output" in /*) ;; *) fail 'owner approval output must be absolute' ;; esac
[ ! -e "$output" ] && [ ! -e "$output.sig" ] || fail 'refusing overwrite of existing approval'
command -v ssh-keygen >/dev/null 2>&1 || fail 'OpenSSH signing unavailable'
expires=$(( $(date -u +%s) + 600 ))
printf 'FCIS-OWNER-PROMOTION-v1\nrepository=%s\ncandidate_ref=%s\ncandidate_sha=%s\nexpected_main=%s\npolicy_sha256=%s\nexpires=%s\n' \
    "$repo" "$candidate" "$wanted" "$old" "$policysha" "$expires" > "$output" || fail 'unable to create owner approval'
if ! ssh-keygen -Y sign -f "$key" -n fcis-git-promotion "$output" >/dev/null 2>&1; then
    rm -f "$output" "$output.sig"
    fail 'owner signature creation failed'
fi
[ -s "$output.sig" ] || fail 'detached signature missing'
printf 'FCIS owner approval SIGNED: %s (expires %s)\n' "$output" "$expires"
