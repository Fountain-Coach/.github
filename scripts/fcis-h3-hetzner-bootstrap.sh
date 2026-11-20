#!/bin/sh
# One-time, owner-authorized FCIS H3 Git origin bootstrap for Ubuntu Hetzner.
# Never run an incoming branch's hook or use a private owner signing key here.
set -eu
umask 077
ROOT=/srv/fcis-owner-git
BARE=$ROOT/origin.git
POLICY=/var/lib/fcis-owner-git-policy
RECEIVER_HOME=/var/lib/fcis-owner-git-receiver
OPERATOR_HOME=/var/lib/fcis-owner-git-operator
OPERATOR_BIN=/usr/local/libexec/fcis-owner-git
REPO=https://github.com/Fountain-Coach/.github.git
REPO_ID=Fountain-Coach/.github
refuse() { printf 'H3 BOOTSTRAP REFUSED: %s\n' "$*" >&2; exit 2; }
report() { printf 'H3 BOOTSTRAP: %s\n' "$*"; }
need() { command -v "$1" >/dev/null 2>&1 || refuse "missing $1"; }
sha256() { sha256sum "$1" | awk '{print $1}'; }
key_body() {
  [ -f "$1" ] && [ ! -L "$1" ] || refuse "public key file missing or symlinked"
  [ "$(wc -l < "$1")" -eq 1 ] || refuse "public key must contain exactly one line"
  awk 'NF >= 2 && ($1 == "ssh-ed25519" || $1 == "ssh-rsa") && $2 ~ /^[A-Za-z0-9+\/=]+$/ { print $1 " " $2 }' "$1"
}
validate_key() {
  body=$(key_body "$1")
  [ -n "$body" ] || refuse "malformed SSH public key"
  [ "$2" != signer ] || { case "$body" in 'ssh-ed25519 '*) : ;; *) refuse 'owner signer must be Ed25519' ;; esac; }
  ssh-keygen -l -f "$1" >/dev/null 2>&1 || refuse "invalid SSH public key"
  printf '%s\n' "$body"
}
if [ "${1:-}" = --inspect ] && [ "$#" -eq 1 ]; then
  report "mode=inspect host=$(hostname)"
  for tool in git git-shell python3 ssh-keygen sha256sum awk bwrap timeout getent groupadd useradd runuser setfacl getfacl; do
    if command -v "$tool" >/dev/null 2>&1; then report "tool available: $tool"; else report "tool MISSING: $tool"; fi
  done
  for path in "$ROOT" "$POLICY" "$RECEIVER_HOME" "$OPERATOR_HOME" "$OPERATOR_BIN"; do
    [ ! -e "$path" ] && [ ! -L "$path" ] && report "absent: $path" || report "present: $path"
  done
  for name in fcis-git fcis-operator; do
    if getent passwd "$name" >/dev/null 2>&1; then report "account present: $name"; else report "account absent: $name"; fi
  done
  report 'INSPECTED (no changes)'
  exit 0
fi
if [ "${1:-}" = --check-keys ] && [ "$#" -eq 3 ]; then
  need ssh-keygen
  signer=$(validate_key "$2" signer)
  receiver=$(validate_key "$3" receiver)
  report "owner signer: ${signer%% *} (valid public key)"
  report "Git receiver: ${receiver%% *} (valid public key)"
  report 'KEYS VALIDATED (no changes)'
  exit 0
fi
[ "${1:-}" = --apply ] && [ "$#" -eq 4 ] || refuse 'usage: --inspect | --check-keys OWNER_PUBLIC_KEY RECEIVER_PUBLIC_KEY | --apply PINNED_MAIN_COMMIT OWNER_ED25519_PUBLIC_KEY RECEIVER_SSH_PUBLIC_KEY'
[ "$(id -u)" -eq 0 ] || refuse 'root authorization required for one-time installation'
pin=$2; signer_file=$3; receiver_file=$4
case "$pin" in ''|*[!0123456789abcdef]*) refuse 'malformed pinned Git SHA' ;; esac
[ "${#pin}" -eq 40 ] || refuse 'pinned Git SHA must contain exactly 40 lowercase hexadecimal characters'
for tool in git git-shell python3 ssh-keygen sha256sum awk bwrap timeout getent groupadd useradd runuser setfacl getfacl; do need "$tool"; done
[ -x /usr/sbin/nologin ] || refuse 'missing /usr/sbin/nologin'
signer=$(validate_key "$signer_file" signer)
receiver=$(validate_key "$receiver_file" receiver)
# Immutable, new-install-only target; no repairing or overwriting an unknown host.
for path in "$ROOT" "$POLICY" "$RECEIVER_HOME" "$OPERATOR_HOME" "$OPERATOR_BIN"; do
  [ ! -e "$path" ] && [ ! -L "$path" ] || refuse "existing installation target: $path"
done
for name in fcis-git fcis-operator; do
  getent passwd "$name" >/dev/null 2>&1 && refuse "existing OS identity: $name" || :
done
getent group fcis-git >/dev/null 2>&1 && refuse 'existing fcis-git group' || :
getent group fcis-operator >/dev/null 2>&1 && refuse 'existing fcis-operator group' || :
# Do network retrieval and independent Git provenance checks BEFORE OS mutation.
tmp=$(mktemp -d /tmp/fcis-h3-bootstrap.XXXXXXXX) || refuse 'cannot create isolated scratch'
trap 'rm -rf "$tmp"' 0
trap 'exit 1' 1 2 3 15
report "fetching exact full-history $REPO_ID main"
GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git clone --quiet --bare "$REPO" "$tmp/origin.git" || refuse 'trusted source clone failed'
actual=$(git --git-dir="$tmp/origin.git" rev-parse refs/heads/main) || refuse 'source main ref missing'
[ "$actual" = "$pin" ] || refuse "source main drifted (wanted $pin, got $actual)"
[ "$(git --git-dir="$tmp/origin.git" rev-parse --is-shallow-repository)" = false ] || refuse 'shallow origin seed forbidden'
git --git-dir="$tmp/origin.git" fsck --full --no-reflogs >/dev/null 2>&1 || refuse 'Git object integrity failed'
mkdir "$tmp/policy"
printf '%s\n' "$REPO_ID" > "$tmp/policy/repository-id"
printf 'owner %s\n' "$signer" > "$tmp/policy/authorized_signers"
: > "$tmp/policy/trusted-files.sha256"
for path in scripts/fcis-ci.sh skills/skillctl.py skills/plugin_projection.py skills/tests/test_fcis_posix_ci.py; do
  git --git-dir="$tmp/origin.git" cat-file -e "refs/heads/main:$path" || refuse "trusted validator missing: $path"
  digest=$(git --git-dir="$tmp/origin.git" show "refs/heads/main:$path" | sha256sum | awk '{print $1}')
  printf '%s  %s\n' "$digest" "$path" >> "$tmp/policy/trusted-files.sha256"
done
mkdir -p "$tmp/operator"
git --git-dir="$tmp/origin.git" show refs/heads/main:.githooks/pre-receive > "$tmp/pre-receive"
git --git-dir="$tmp/origin.git" show refs/heads/main:scripts/fcis-git-promote.sh > "$tmp/operator/fcis-git-promote.sh"
[ -s "$tmp/pre-receive" ] && [ -s "$tmp/operator/fcis-git-promote.sh" ] || refuse 'trusted scripts missing'
sh -n "$tmp/pre-receive" && sh -n "$tmp/operator/fcis-git-promote.sh" || refuse 'reviewed POSIX script syntax failed'
git --git-dir="$tmp/origin.git" config fcis.repositoryID "$REPO_ID"
git --git-dir="$tmp/origin.git" config core.sharedRepository group
report "source verified: $pin; creating dedicated Git identities"
groupadd --system fcis-git
groupadd --system fcis-operator
useradd --system --gid fcis-git --home "$RECEIVER_HOME" --shell "$(command -v git-shell)" --no-create-home fcis-git
useradd --system --gid fcis-operator --groups fcis-git --home "$OPERATOR_HOME" --shell /usr/sbin/nologin --no-create-home fcis-operator
mkdir -p "$ROOT" "$POLICY" "$RECEIVER_HOME/.ssh" "$OPERATOR_HOME" "$OPERATOR_BIN"
cp -a "$tmp/origin.git" "$BARE"
chown -R fcis-git:fcis-git "$BARE"
chmod -R g+rwX "$BARE"
# Root owns both the Git parent and bare origin. The receiver cannot create
# top-level locks. The separate signed-promotion operator needs HEAD.lock for
# Git atomic compare-and-swap, so it receives an exact named ACL on the bare
# root with sticky deletion protection of root-owned config, HEAD and hooks.
# Other users have no access and the Git receiver remains read/traverse only.
chown root:fcis-git "$ROOT" "$BARE"
chmod 2750 "$ROOT" "$BARE"
rm -rf "$BARE/hooks"
mkdir "$BARE/hooks"
cp "$tmp/pre-receive" "$BARE/hooks/pre-receive"
chown root:root "$BARE/config" "$BARE/HEAD" "$BARE/hooks" "$BARE/hooks/pre-receive"
chmod 0644 "$BARE/config" "$BARE/HEAD"
chmod 0755 "$BARE/hooks" "$BARE/hooks/pre-receive"
chmod +t "$BARE"
setfacl -m 'u:fcis-operator:rwx,g::r-x,o::---' "$BARE"
printf 'command="git-receive-pack '\''%s'\''",restrict %s\n' "$BARE" "$receiver" > "$RECEIVER_HOME/.ssh/authorized_keys"
# Git's trusted safe.directory must be explicit because the bare repo root
# is owned by root and neither unprivileged account owns that directory.
# Both global Git configurations are immutable to their respective users.
printf '[safe]\n\tdirectory = %s\n' "$BARE" > "$RECEIVER_HOME/.gitconfig"
printf '[safe]\n\tdirectory = %s\n' "$BARE" > "$OPERATOR_HOME/.gitconfig"
chown -R root:root "$RECEIVER_HOME" "$OPERATOR_HOME"
chmod 0755 "$RECEIVER_HOME" "$RECEIVER_HOME/.ssh" "$OPERATOR_HOME"
chmod 0644 "$RECEIVER_HOME/.ssh/authorized_keys" "$RECEIVER_HOME/.gitconfig" "$OPERATOR_HOME/.gitconfig"
cp "$tmp/policy/"* "$POLICY/"
mkdir "$POLICY/receipts"
# Root owns the signer allowlist and validator policy. Only the operator's
# separate OS group can READ them. The receiver cannot enter the policy dir.
chown root:fcis-operator "$POLICY" "$POLICY/repository-id" "$POLICY/authorized_signers" "$POLICY/trusted-files.sha256"
chmod 0750 "$POLICY"
chmod 0640 "$POLICY/repository-id" "$POLICY/authorized_signers" "$POLICY/trusted-files.sha256"
chown fcis-operator:fcis-operator "$POLICY/receipts"
chmod 0700 "$POLICY/receipts"
cp "$tmp/operator/fcis-git-promote.sh" "$OPERATOR_BIN/fcis-git-promote.sh"
chown -R root:root "$OPERATOR_BIN"
chmod 0755 "$OPERATOR_BIN" "$OPERATOR_BIN/fcis-git-promote.sh"
# Distinct identity readback; both Git users need permission to access the
# pinned origin, but neither may rewrite top-level Git config or hooks.
runuser -u fcis-git -- env HOME="$RECEIVER_HOME" git --git-dir="$BARE" rev-parse refs/heads/main | grep -Fx "$pin" >/dev/null || refuse 'receiver Git readback failed'
runuser -u fcis-operator -- env HOME="$OPERATOR_HOME" git --git-dir="$BARE" rev-parse refs/heads/main | grep -Fx "$pin" >/dev/null || refuse 'operator Git readback failed'
runuser -u fcis-git -- test ! -w "$BARE" || refuse 'receiver can replace Git config/hook'
runuser -u fcis-operator -- test -w "$BARE" || refuse 'operator cannot create Git HEAD.lock'
runuser -u fcis-operator -- test ! -w "$BARE/config" || refuse 'operator can write Git config'
runuser -u fcis-operator -- test ! -w "$BARE/HEAD" || refuse 'operator can write Git HEAD'
runuser -u fcis-operator -- test ! -w "$BARE/hooks" || refuse 'operator can write Git hooks'
[ -k "$BARE" ] || refuse 'Git root sticky protection absent'
getfacl -cp "$BARE" | grep -Fx 'user:fcis-operator:rwx' >/dev/null || refuse 'operator named ACL missing'
getfacl -cp "$BARE" | grep -Fx 'group::r-x' >/dev/null || refuse 'receiver group permissions widened'
getfacl -cp "$BARE" | grep -Fx 'other::---' >/dev/null || refuse 'world permissions widened'
runuser -u fcis-git -- test ! -r "$POLICY/authorized_signers" || refuse 'receiver can read owner signer policy'
[ "$(stat -c %U "$POLICY/authorized_signers")" = root ] || refuse 'signer policy owner is not root'
git --git-dir="$BARE" fsck --full --no-reflogs >/dev/null 2>&1 || refuse 'installed Git integrity failed'
[ "$(sha256 "$BARE/hooks/pre-receive")" = "$(sha256 "$tmp/pre-receive")" ] || refuse 'installed hook digest mismatch'
[ "$(sha256 "$OPERATOR_BIN/fcis-git-promote.sh")" = "$(sha256 "$tmp/operator/fcis-git-promote.sh")" ] || refuse 'installed promotion script digest mismatch'
report "INSTALLED SOURCE: $pin"
report "BARE: $BARE"
report "RECEIVER: fcis-git (restricted Git receive-pack only)"
report "OPERATOR: fcis-operator (isolated CI and signed Git promotion, separately invoked)"
report 'NOT YET VERIFIED: live signed candidate/CI promotion, offline restore, owner Git/Go deployment integration'
