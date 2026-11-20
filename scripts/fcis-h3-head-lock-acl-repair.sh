#!/bin/bash
# One-time, owner-SSH-authorized repair of HEAD.lock capability on installed
# FCIS H3 bare origin; leaves Git receiver without top-level write permission.
set -euo pipefail
umask 077
refuse() { printf 'H3 HEAD LOCK REFUSED: %s\n' "$*" >&2; exit 2; }
[[ $# == 1 && $1 == --apply ]] || refuse 'explicit --apply required'
[[ $(id -u) == 0 ]] || refuse 'root SSH owner authorization required'
[[ $(hostname) == ubuntu-2gb-hel1-1 ]] || refuse 'wrong Hetzner host'
BARE=/srv/fcis-owner-git/origin.git
POLICY=/var/lib/fcis-owner-git-policy
OLD=be5a12b295d8ff7cfd40fd1c3e756698580bd2e9
STALE=390a21532930c4876a527d6d64252d26d4f199a1
PROMOTER=/usr/local/libexec/fcis-owner-git/fcis-git-promote.sh
PROMOTER_BLOB=ffce53bb2577724a3d48f596376b8269c396090f
RECEIPT="$POLICY/receipts/$STALE.$OLD"
for tool in git stat runuser getent sha256sum flock mktemp getfacl setfacl; do
  # The two ACL utilities are installed after the provenance preflight.
  case "$tool" in getfacl|setfacl) : ;; *) command -v "$tool" >/dev/null || refuse "missing $tool" ;; esac
done
[[ -d $BARE && ! -L $BARE && -d $POLICY ]] || refuse 'installed origin or policy missing'
[[ $(stat -c %U:%G "$BARE") == root:fcis-git ]] || refuse 'unexpected bare root owner/group'
[[ ! -L $BARE/HEAD && -f $BARE/HEAD ]] || refuse 'bare HEAD missing or symlinked'
[[ $(cat "$BARE/HEAD") == 'ref: refs/heads/main' ]] || refuse 'bare HEAD not main symbolic ref'
[[ $(stat -c %U "$BARE/config") == root ]] || refuse 'config not root-owned'
[[ $(stat -c %U "$BARE/hooks/pre-receive") == root ]] || refuse 'receive hook not root-owned'
[[ $(stat -c %U "$POLICY/authorized_signers") == root ]] || refuse 'signer policy not root-owned'
[[ $(git hash-object "$PROMOTER") == "$PROMOTER_BLOB" ]] || refuse 'installed promoter changed'
[[ $(git --git-dir="$BARE" rev-parse refs/heads/main) == "$OLD" ]] || refuse 'main changed; no repair'
[[ $(git --git-dir="$BARE" rev-parse "${STALE}^{commit}") == "$STALE" ]] || refuse 'prior candidate missing'
[[ ! -e $BARE/HEAD.lock && ! -L $BARE/HEAD.lock ]] || refuse 'bare HEAD.lock is present'
[[ -f $RECEIPT.prepared && -f $RECEIPT.ci.log && ! -e $RECEIPT.promoted ]] || refuse 'failed CAS source receipt missing or already promoted'
[[ $(sed -n 's/^ci_log_sha256=//p' "$RECEIPT.prepared") == "$(sha256sum "$RECEIPT.ci.log" | awk '{print $1}')" ]] || refuse 'prior source CI receipt digest mismatch'
grep -F 'SOURCE PASS' "$RECEIPT.ci.log" >/dev/null || refuse 'prior source CI did not pass'
runuser -u fcis-git -- test ! -w "$BARE" || refuse 'receiver already can write bare root'
runuser -u fcis-operator -- test ! -w "$BARE" || refuse 'operator already can write bare root; unexpected preimage'
[[ ! -L $BARE/refs && ! -L $BARE/objects ]] || refuse 'bare Git subdirectory symlink'
printf '%s\n' 'H3_ORIGIN_AND_PREPARED_RECEIPT_PREIMAGE_VERIFIED'

# On Ubuntu, the ACL utility package is the only missing external prerequisite
# permitted to be installed here. No AppArmor or service settings are changed.
if ! command -v setfacl >/dev/null || ! command -v getfacl >/dev/null; then
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends acl
fi
command -v setfacl >/dev/null && command -v getfacl >/dev/null || refuse 'ACL utilities unavailable'

# Ensure there is no concurrent copy of this exact owner repair running.
exec 8>"$POLICY/.h3-head-lock-acl.lock"
flock -n 8 || refuse 'another owner ACL repair is active'
TMP=$(mktemp -d /var/tmp/fcis-h3-acl-XXXXXXXX)
chmod 0755 "$TMP"
getfacl -p "$BARE" > "$TMP/preimage.acl"
head_owner=$(stat -c %u:%g "$BARE/HEAD")
head_mode=$(stat -c %a "$BARE/HEAD")
mutated=0
cleanup() {
  status=$?
  if [[ $status -ne 0 && $mutated == 1 ]]; then
    echo 'H3 HEAD LOCK: restoring original ACL and HEAD ownership'
    setfacl --restore="$TMP/preimage.acl" || echo 'CRITICAL: ACL rollback failed' >&2
    chown "$head_owner" "$BARE/HEAD" || echo 'CRITICAL: HEAD owner rollback failed' >&2
    chmod "$head_mode" "$BARE/HEAD" || echo 'CRITICAL: HEAD mode rollback failed' >&2
  fi
  rm -rf -- "$TMP"
}
trap cleanup EXIT

# Keep the root-owned Git config/hooks inaccessible for changes by either
# unprivileged identity. Directory sticky bit protects unlink/rename of
# root-owned files even for the named ACL writer; no wildcard ACL, no 0777.
mutated=1
chown root:root "$BARE/HEAD"
chmod 0644 "$BARE/HEAD"
chmod +t "$BARE"
setfacl -m 'u:fcis-operator:rwx,g::r-x,o::---' "$BARE"
getfacl -cp "$BARE" | grep -Fx 'user:fcis-operator:rwx' >/dev/null || refuse 'named operator ACL missing'
getfacl -cp "$BARE" | grep -Fx 'group::r-x' >/dev/null || refuse 'receiver group permissions widened'
getfacl -cp "$BARE" | grep -Fx 'other::---' >/dev/null || refuse 'world permissions widened'
[[ -k $BARE ]] || refuse 'sticky-directory protection missing'
runuser -u fcis-operator -- test -w "$BARE" || refuse 'operator cannot create HEAD.lock'
runuser -u fcis-git -- test ! -w "$BARE" || refuse 'receiver can rewrite bare root'
runuser -u fcis-operator -- test ! -w "$BARE/config" || refuse 'operator can write root config'
runuser -u fcis-operator -- test ! -w "$BARE/HEAD" || refuse 'operator can write root HEAD'
runuser -u fcis-operator -- test ! -w "$BARE/hooks" || refuse 'operator can write hooks directory'
[[ $(stat -c %U "$BARE/HEAD") == root ]] || refuse 'bare HEAD not root-owned'
[[ $(git --git-dir="$BARE" rev-parse refs/heads/main) == "$OLD" ]] || refuse 'bare main moved during ACL repair'

# Actual Git compare-and-swap test is performed only in a disposable origin.
# Never test a mutable promotion against the live Git main without owner signature.
git clone --quiet --bare --no-hardlinks "$BARE" "$TMP/fixture.git" || refuse 'disposable origin clone failed'
FIXTURE="$TMP/fixture.git"
[[ $(git --git-dir="$FIXTURE" rev-parse refs/heads/main) == "$OLD" ]] || refuse 'fixture main differs'
git --git-dir="$FIXTURE" cat-file -e "$STALE^{commit}" || refuse 'fixture candidate object missing'
chown -R fcis-git:fcis-git "$FIXTURE"
# A bare clone created with umask 077 can leave top-level packed-refs at
# mode 0600. The operator is a supplementary member of fcis-git and must
# READ packed-refs to resolve HEAD during a genuine update-ref. Give group
# read/traverse access to the disposable fixture only, not the live origin.
chmod -R g+rX "$FIXTURE"
for sub in refs objects logs; do
  [[ ! -d $FIXTURE/$sub ]] || chmod -R g+rwX "$FIXTURE/$sub"
done
chown root:fcis-git "$FIXTURE"
chown root:root "$FIXTURE/config" "$FIXTURE/HEAD" "$FIXTURE/hooks"
chmod 0644 "$FIXTURE/config" "$FIXTURE/HEAD"
chmod +t "$FIXTURE"
setfacl -m 'u:fcis-operator:rwx,g::r-x,o::---' "$FIXTURE"
runuser -u fcis-git -- test ! -w "$FIXTURE" || refuse 'fixture receiver can rewrite Git root'
runuser -u fcis-operator -- env HOME=/var/lib/fcis-owner-git-operator \
  GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0="$FIXTURE" \
  git --git-dir="$FIXTURE" update-ref refs/heads/main "$STALE" "$OLD" || refuse 'operator fixture CAS failed'
[[ $(git --git-dir="$FIXTURE" rev-parse refs/heads/main) == "$STALE" ]] || refuse 'fixture CAS readback mismatch'
git --git-dir="$FIXTURE" fsck --full --no-reflogs >/dev/null || refuse 'fixture Git integrity failed'
[[ $(git --git-dir="$BARE" rev-parse refs/heads/main) == "$OLD" ]] || refuse 'actual Git main changed by fixture test'
mutated=0
printf '%s\n' 'H3_OPERATOR_HEAD_LOCK_ACL_VERIFIED'
printf '%s\n' 'H3_DISPOSABLE_ATOMIC_CAS_VERIFIED'
printf '%s\n' 'H3_PREVIOUS_PREPARED_RECEIPT_PRESERVED'
