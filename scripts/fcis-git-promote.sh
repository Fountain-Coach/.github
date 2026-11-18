#!/bin/sh
# FCIS H3: owner-invoked, signature-bound Git promotion. Do not invoke from a receive hook.
# Install a REVIEWED copy outside incoming Git and run under a separate operator identity.
set -eu
umask 077
die() { printf 'FCIS promotion REFUSED: %s\n' "$*" >&2; exit 1; }
say() { printf 'FCIS promotion: %s\n' "$*"; }
[ "$#" -eq 6 ] || die 'usage: fcis-git-promote.sh BARE POLICY CANDIDATE_REF CANDIDATE_SHA EXPECTED_MAIN_SHA APPROVAL_FILE'
bare=$1 policy=$2 candidate=$3 wanted=$4 old=$5 approval=$6
case "$bare" in /*) ;; *) die 'bare path must be absolute' ;; esac
case "$policy" in /*) ;; *) die 'trusted policy path must be absolute' ;; esac
case "$approval" in /*) ;; *) die 'signed approval path must be absolute' ;; esac
[ -d "$bare" ] && [ -d "$policy" ] || die 'bare repository or trusted policy directory missing'
[ "$(git --git-dir="$bare" rev-parse --is-bare-repository 2>/dev/null)" = true ] || die 'not a bare Git repository'
case "$candidate" in refs/heads/candidates/*) ;; *) die 'only immutable candidate refs may be promoted' ;; esac
case "$candidate" in refs/heads/candidates/*/*) die 'nested candidate refs forbidden' ;; esac
case "\${candidate#refs/heads/candidates/}" in ''|*[!a-zA-Z0-9._-]*) die 'unsafe candidate ref' ;; esac
is_sha() { case "$1" in
    *[!0123456789abcdef]*|'') return 1 ;;
esac
case \${#1} in 40|64) return 0 ;; *) return 1 ;; esac
}
is_sha "$wanted" && is_sha "$old" || die 'expected full commit object IDs'
git --git-dir="$bare" cat-file -e "$wanted^{commit}" 2>/dev/null || die 'candidate commit missing'
resolved=$(git --git-dir="$bare" rev-parse --verify "$candidate^{commit}") || die 'candidate ref missing'
[ "$resolved" = "$wanted" ] || die 'candidate moved since approval'
main=$(git --git-dir="$bare" rev-parse --verify 'refs/heads/main^{commit}') || die 'main must be owner-bootstrapped before promotion'
[ "$main" = "$old" ] || die 'stale expected main'
git --git-dir="$bare" merge-base --is-ancestor "$old" "$wanted" || die 'candidate is not a descendant of main'
repo=$(git --git-dir="$bare" config --local --get fcis.repositoryID) || die 'missing owner repo identity'
[ -n "$repo" ] || die 'empty owner repo identity'
[ -f "$policy/repository-id" ] && [ -f "$policy/authorized_signers" ] &&
  [ -f "$policy/trusted-files.sha256" ] || die 'incomplete owner-controlled policy'
[ ! -L "$policy/authorized_signers" ] && [ ! -L "$policy/trusted-files.sha256" ] || die 'policy symlinks forbidden'
[ "$(cat "$policy/repository-id")" = "$repo" ] || die 'policy and origin repository identity differ'
command -v ssh-keygen >/dev/null || die 'OpenSSH signer verifier unavailable'
command -v bwrap >/dev/null || die 'Bubblewrap isolated runner unavailable'
command -v timeout >/dev/null || die 'bounded timeout unavailable'
command -v python3 >/dev/null || die 'Python source validator unavailable'
sha_file() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$1" | awk '{print $1}'
    else
        shasum -a 256 "$1" | awk '{print $1}'
    fi
}
policy_sha=$(sha_file "$policy/trusted-files.sha256")
[ -f "$approval" ] && [ -f "$approval.sig" ] || die 'missing owner approval and detached signature'
[ ! -L "$approval" ] && [ ! -L "$approval.sig" ] || die 'symlinked approval forbidden'
# Exact signed payload: the caller cannot change ref, candidate, predecessor or pinned CI policy.
expires=$(sed -n '7s/^expires=//p' "$approval")
case "$expires" in ''|*[!0-9]*) die 'invalid approval expiry' ;; esac
now=$(date -u +%s)
[ "$expires" -ge "$now" ] && [ "$expires" -le "$((now + 900))" ] || die 'expired or excessively long-lived approval'
payload=$(mktemp "\${TMPDIR:-/tmp}/fcis-approved-payload.XXXXXXXX")
tmp=''
clean() { rm -f "$payload"; [ -z "$tmp" ] || rm -rf "$tmp"; }
trap clean 0
trap 'exit 1' HUP INT TERM
printf 'FCIS-OWNER-PROMOTION-v1\nrepository=%s\ncandidate_ref=%s\ncandidate_sha=%s\nexpected_main=%s\npolicy_sha256=%s\nexpires=%s\n' \
    "$repo" "$candidate" "$wanted" "$old" "$policy_sha" "$expires" > "$payload"
cmp -s "$payload" "$approval" || die 'signed approval does not match the selected promotion'
ssh-keygen -Y verify -I owner -n fcis-git-promotion \
    -f "$policy/authorized_signers" -s "$approval.sig" < "$approval" >/dev/null 2>&1 ||
    die 'owner Ed25519 approval signature not valid'
# Only files pinned by the preinstalled policy may be executed as CI code in the sandbox.
tmp=$(mktemp -d "\${TMPDIR:-/tmp}/fcis-git-accept.XXXXXXXX") || die 'isolated temp directory failed'
chmod 755 "$tmp"
git -c protocol.file.allow=always clone --quiet --no-hardlinks --no-checkout "$bare" "$tmp/source" ||
    die 'independent Git checkout failed'
git -C "$tmp/source" checkout --quiet --detach "$wanted" || die 'candidate checkout failed'
[ "$(git -C "$tmp/source" rev-parse HEAD)" = "$wanted" ] || die 'candidate checkout digest mismatch'
for rel in scripts/fcis-ci.sh skills/skillctl.py skills/plugin_projection.py skills/tests/test_fcis_posix_ci.py; do
    match=$(awk -v p="$rel" '$2 == p { print $1 }' "$policy/trusted-files.sha256")
    is_sha "$match" || die "missing or duplicate trusted validator entry: $rel"
    [ -f "$tmp/source/$rel" ] && [ ! -L "$tmp/source/$rel" ] || die "missing trusted validator: $rel"
    [ "$(sha_file "$tmp/source/$rel")" = "$match" ] || die "candidate changes pinned CI authority: $rel"
done
# Candidate tests run only inside a read-only checkout with no network, keys, owner
# Git origin or production Store. Operator-side program is pinned outside the candidate.
set -- bwrap --unshare-user --unshare-net --unshare-ipc --unshare-uts --unshare-pid \
    --die-with-parent --new-session --uid 65534 --gid 65534 --ro-bind /usr /usr
for d in /bin /lib /lib64; do
    [ -d "$d" ] && set -- "$@" --ro-bind "$d" "$d"
done
set -- "$@" --proc /proc --dev /dev --tmpfs /tmp --dir /home \
    --ro-bind "$tmp/source" /source --chdir /source \
    --setenv HOME /tmp --setenv PYTHONDONTWRITEBYTECODE 1 \
    --setenv GIT_CONFIG_NOSYSTEM 1 --setenv GIT_CONFIG_GLOBAL /dev/null \
    --setenv GIT_CONFIG_COUNT 1 --setenv GIT_CONFIG_KEY_0 safe.directory \
    --setenv GIT_CONFIG_VALUE_0 /source \
    /bin/sh /source/scripts/fcis-ci.sh source "$old" "$wanted"
say "Running pinned candidate $wanted under isolated, networkless H2 source CI"
if ! env -i PATH=/usr/bin:/bin LANG=C LC_ALL=C timeout -s KILL 180 "$@" > "$tmp/source-ci.log" 2>&1; then
    tail -n 50 "$tmp/source-ci.log" >&2
    die 'sandboxed source CI failed or timed out'
fi
grep -F 'SOURCE PASS' "$tmp/source-ci.log" >/dev/null || die 'source CI did not emit terminal PASS'
[ "$(git --git-dir="$bare" rev-parse "$candidate")" = "$wanted" ] || die 'candidate changed during CI'
[ "$(git --git-dir="$bare" rev-parse refs/heads/main)" = "$old" ] || die 'main changed during CI'
receipts="$policy/receipts"
[ -d "$receipts" ] || die 'owner-managed private receipts directory missing'
[ ! -L "$receipts" ] || die 'receipt directory symlink forbidden'
receipt="$receipts/$wanted.$old"
[ ! -e "$receipt.prepared" ] && [ ! -e "$receipt.promoted" ] || die 'duplicate candidate receipt'
logsha=$(sha_file "$tmp/source-ci.log")
approvalsha=$(sha_file "$approval")
cp "$tmp/source-ci.log" "$receipt.ci.log"
printf 'state=source-tested\nrepository=%s\ncandidate=%s\nexpected_main=%s\npolicy_sha256=%s\napproval_sha256=%s\nci_log_sha256=%s\n' \
    "$repo" "$wanted" "$old" "$policy_sha" "$approvalsha" "$logsha" > "$receipt.prepared"
git --git-dir="$bare" update-ref refs/heads/main "$wanted" "$old" ||
    die 'atomic main compare-and-swap refused (source receipt retained)'
[ "$(git --git-dir="$bare" rev-parse refs/heads/main)" = "$wanted" ] ||
    die 'post-promotion independent ref readback mismatch'
printf 'state=promoted\nrepository=%s\ncandidate=%s\nprevious_main=%s\npolicy_sha256=%s\napproval_sha256=%s\nci_log_sha256=%s\n' \
    "$repo" "$wanted" "$old" "$policy_sha" "$approvalsha" "$logsha" > "$receipt.promoted"
say "ACCEPTED candidate=$wanted previous=$old ci_log_sha256=$logsha"
