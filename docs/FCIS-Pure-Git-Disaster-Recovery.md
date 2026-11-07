# Fountain Coach: pure-Git disaster recovery

**Authority:** Fountain-Coach/.github remains the canonical source at its reviewed Git commit.
GitHub is a distribution and collaboration service, not a requirement for retaining or
recovering the committed source. This procedure does not change Governance Chapter 160,
make an installed ChatGPT skill current, or install a new publisher.

## Two independent copies

Use the existing **owner-owned Mac** and mounted **NINJA2** drive:
- **APFS local bare mirror:** a Git remote with all branches, tags and remote-tracking refs,
  usable for offline fetch/clone and later a different SSH server.
- **NINJA2 Git bundle snapshots:** portable Git archives with SHA-256 companions and a
  `LATEST` pointer, each independently recoverable with normal Git. Snapshots are retained,
  not silently pruned. On ExFAT, use bundles instead of assuming Unix filesystem semantics.

This repo was observed public on GitHub during setup. Do not automatically copy private
repositories, credentials or uncommitted changes to an unencrypted ExFAT disk.

**A shallow checkout is not an accepted disaster backup.** The script refuses to
snapshot a shallow repository. Before the first setup, obtain its missing Git
history from an available upstream using `git fetch --unshallow`; then verify
that `git rev-parse --is-shallow-repository` prints `false`. Do not attempt an
unshallow operation after an upstream disappears and claim that Git recovered
objects it never had.

## One-time setup on each participating clone

On the authorized Mac with NINJA2 mounted, from the repository root:

```sh
./scripts/git-disaster-recovery.sh setup \
  "$HOME/Dev/_git-recovery/fountain-coach-org.git" \
  /Volumes/NINJA2/Fountain-Coach-Git-Recovery \
  /Volumes/NINJA2
./scripts/git-disaster-recovery.sh verify
```

Setup creates the local bare Git repository (if absent), stores destination paths in the
clone-local `.git/config`, and enables the repository's **versioned** `.githooks` via
`core.hooksPath`. No hooks are installed or automatically trusted in unrelated clones.

The hooks `post-commit`, `post-merge`, `post-rewrite` and `pre-push` snapshot Git
history without connecting to GitHub. The pre-existing `pre-commit` and `pre-push`
canonical skill digest checks remain in force. **A missing external disk issues a warning
but cannot prevent a valid commit/push.** Always inspect backup status; a warning is not
proof of recovery.

Run a manual snapshot and real restore acceptance any time:

```sh
./scripts/git-disaster-recovery.sh snapshot
./scripts/git-disaster-recovery.sh verify
```

## Recover without GitHub

From the owner Mac's local bare Git mirror:

```sh
git clone "$HOME/Dev/_git-recovery/fountain-coach-org.git" recovered-fcis
cd recovered-fcis && git fsck --full
```

Or, if the Mac was lost but NINJA2 survived, read the exact `LATEST` filename and
clone the standalone Git bundle:

```sh
bundle="/Volumes/NINJA2/Fountain-Coach-Git-Recovery/$(cat /Volumes/NINJA2/Fountain-Coach-Git-Recovery/LATEST)"
git clone -b main "$bundle" recovered-fcis
cd recovered-fcis && git fsck --full
python3 skills/skillctl.py check
python3 -m unittest discover -s skills/tests -q
```

The `verify` operation checks checksum, verifies the bundle against a **new empty Git
repository**, performs an isolated `git clone --mirror`, and runs `git fsck`. It does not
contact GitHub or the OpenAI platform.

A restored repository starts with Git hooks **disabled** unless explicitly configured again.
Once a new authorized Git host is available, push only reviewed branches/tags to it;
do not replay or silently alter hosted ChatGPT active versions.

## Limitations

- Git backups contain committed objects and refs; they do not include working-tree edits,
  GitHub PR reviews/issues, hosted CI logs, GitHub repository settings, ChatGPT
  installations, or API credentials.
- A hook fires only during the local Git operation. It is not an external timer or a
  monitor of commits made elsewhere while the Mac is offline.
- The APFS bare mirror and removable SSD protect against GitHub loss, but a full
  site-level disaster also needs a **second offsite copy** and a separately rehearsed
  restoration of any private repositories. That broader replication is not silently
  introduced here.
