#!/bin/bash
# One-time OWNER-INITIATED bootstrap of separate FCIS H3 Git origin.
# Runs on an owner's Mac. Sends only PUBLIC keys and a pinned, reviewed script.
# All host changes go through the exact-SHA, refusal-gated H3 installer.
set -euo pipefail
[[ "${1:-}" == --apply && "$#" -eq 1 ]] || { echo 'H3 OWNER SETUP REFUSED: explicit --apply required' >&2; exit 2; }
umask 077
HOST='root@65.109.14.71'
SSH_KEY="$HOME/.ssh/id_rsa"
SIGNER_KEY="$HOME/.ssh/fcis_owner_git_ed25519"
# Immutable source, reviewed in Fountain-Coach/.github PR #109.
SOURCE_COMMIT='bc26476974e547c7230f99b997b7b6c3b5024a91'
SOURCE_SHA256='b33a4954baa4d730ca7737ab12aa25243f0703398106d4d6df1c5cd94087fe86'
PINNED_ORG_MAIN='be5a12b295d8ff7cfd40fd1c3e756698580bd2e9'
FILENAME='fcis-h3-hetzner-bootstrap.sh'
SSH_OPTS=(-o BatchMode=yes -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -i "$SSH_KEY")
LOCAL_TMP=''
REMOTE_TMP=''
fail() { echo "H3 OWNER SETUP REFUSED: $*" >&2; exit 2; }
cleanup() {
    if [[ -n "$REMOTE_TMP" && "$REMOTE_TMP" == /root/fcis-h3-stage.* ]]; then
        ssh "${SSH_OPTS[@]}" "$HOST" "rm -rf -- '$REMOTE_TMP'" >/dev/null 2>&1 || true
    fi
    [[ -z "$LOCAL_TMP" ]] || rm -rf "$LOCAL_TMP"
}
trap cleanup EXIT
[[ -f "$SSH_KEY" ]] || fail "existing owner SSH key not found: $SSH_KEY"
for tool in curl ssh scp ssh-keygen shasum awk; do command -v "$tool" >/dev/null || fail "missing Mac tool: $tool"; done
LOCAL_TMP=$(mktemp -d "${TMPDIR:-/tmp}/fcis-h3-owner.XXXXXXXX") || fail 'temporary directory unavailable'
URL="https://raw.githubusercontent.com/Fountain-Coach/.github/$SOURCE_COMMIT/scripts/$FILENAME"
echo 'Downloading the exact reviewed FCIS H3 host installer...'
curl -fsSL --max-time 30 "$URL" -o "$LOCAL_TMP/$FILENAME" || fail 'reviewed source download unavailable'
ACTUAL_SHA256=$(shasum -a 256 "$LOCAL_TMP/$FILENAME" | awk '{print $1}')
[[ "$ACTUAL_SHA256" == "$SOURCE_SHA256" ]] || fail "reviewed source digest mismatch: $ACTUAL_SHA256"
sh -n "$LOCAL_TMP/$FILENAME" || fail 'downloaded installer is not valid POSIX shell'
REMOTE_TMP=$(ssh "${SSH_OPTS[@]}" "$HOST" 'umask 077; mktemp -d /root/fcis-h3-stage.XXXXXXXX') || fail 'SSH staging unavailable'
[[ "$REMOTE_TMP" == /root/fcis-h3-stage.* ]] || fail 'remote stage path unexpected'
scp -q "${SSH_OPTS[@]}" "$LOCAL_TMP/$FILENAME" "$HOST:$REMOTE_TMP/" || fail 'reviewed bootstrap transfer failed'
echo '=== Host readiness ==='
INSPECT=$(ssh "${SSH_OPTS[@]}" "$HOST" "sh '$REMOTE_TMP/$FILENAME' --inspect") || fail 'host preflight failed'
printf '%s\n' "$INSPECT"
if printf '%s\n' "$INSPECT" | grep -Eq 'tool MISSING:|present:|account present:'; then
    fail 'host has missing prerequisites or existing installation; no OS mutation attempted'
fi
if [[ ! -f "$SIGNER_KEY" ]]; then
    echo 'Creating a dedicated Ed25519 owner signing key on this Mac only.'
    echo 'Choose a passphrase when prompted. The private key is NEVER transferred.'
    ssh-keygen -t ed25519 -a 64 -f "$SIGNER_KEY" -C 'fountain-owner-git' || fail 'owner signing key creation refused'
fi
if [[ ! -f "$SIGNER_KEY.pub" ]]; then
    ssh-keygen -y -f "$SIGNER_KEY" > "$SIGNER_KEY.pub" || fail 'owner signer public key unavailable'
fi
cp "$SIGNER_KEY.pub" "$LOCAL_TMP/owner.pub"
if [[ -f "$SSH_KEY.pub" ]]; then
    cp "$SSH_KEY.pub" "$LOCAL_TMP/receiver.pub"
else
    ssh-keygen -y -f "$SSH_KEY" > "$LOCAL_TMP/receiver.pub" || fail 'receiver public key unavailable'
fi
scp -q "${SSH_OPTS[@]}" "$LOCAL_TMP/owner.pub" "$LOCAL_TMP/receiver.pub" "$HOST:$REMOTE_TMP/" || fail 'public-key transfer failed'
echo '=== Owner public key validation ==='
ssh "${SSH_OPTS[@]}" "$HOST" "sh '$REMOTE_TMP/$FILENAME' --check-keys '$REMOTE_TMP/owner.pub' '$REMOTE_TMP/receiver.pub'" || fail 'public owner key validation failed'
echo '=== Installing isolated owner Git origin (no FCIS production service changes) ==='
ssh "${SSH_OPTS[@]}" "$HOST" "sh '$REMOTE_TMP/$FILENAME' --apply '$PINNED_ORG_MAIN' '$REMOTE_TMP/owner.pub' '$REMOTE_TMP/receiver.pub'" || fail 'H3 host installer refused or failed; inspect server state before retry'
echo 'H3 OWNER SETUP: source installed and read back; signed live promotion and Go deployment remain separate gates.'
