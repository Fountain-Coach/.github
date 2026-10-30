#!/usr/bin/env python3
"""Publish ONLY a validated derived FCIS marketplace projection to canonical Git.

Run on the main-branch checkout in GitHub Actions, after plugin_projection.sync,
its digest verification, and the organization's source tests. The target is
Fountain-Coach/.github Git only, never a ChatGPT installation or Skills API.
"""
import json
from pathlib import Path
import re
import subprocess
import sys

from plugin_projection import MIRROR_PATH, PLUGIN_PATH, ProjectionError, check
from skillctl import ROOT


class PublicationError(ValueError):
    pass


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise PublicationError(
            "git " + " ".join(args[:3]) + ": "
            + result.stderr.strip()
        )
    return result.stdout.strip()


def eligible_path(path):
    """No changes outside the single derived FCIS plugin may be committed."""
    return path == (PLUGIN_PATH / "plugin.json").as_posix() or (
        path.startswith(MIRROR_PATH.as_posix() + "/")
        and path.count("/") > 3
    )


def validate_changed_paths(root):
    root = Path(root).resolve(strict=True)
    if git(root, "diff", "--cached", "--name-only"):
        raise PublicationError("Refusing pre-staged changes")
    changed = set(git(root, "diff", "--name-only").splitlines())
    untracked = set(git(root, "ls-files", "--others", "--exclude-standard").splitlines())
    all_changed = changed | untracked
    forbidden = sorted(path for path in all_changed if not eligible_path(path))
    if forbidden:
        raise PublicationError("Unrelated file changes block publication: " + ", ".join(forbidden))
    git(root, "diff", "--check")
    return sorted(all_changed)


def check_remote(root):
    name = git(root, "symbolic-ref", "--short", "HEAD")
    if name != "main":
        raise PublicationError("GitHub marketplace publication must run on main")
    url = git(root, "remote", "get-url", "origin")
    if not re.fullmatch(
        r"(https://github\.com/Fountain-Coach/\.github(?:\.git)?|git@github\.com:Fountain-Coach/\.github\.git)",
        url,
    ):
        raise PublicationError("Unexpected canonical origin repository")
    head = git(root, "rev-parse", "HEAD")
    ref = git(root, "ls-remote", "origin", "refs/heads/main").split()
    if len(ref) != 2 or ref[1] != "refs/heads/main" or ref[0] != head:
        raise PublicationError("Canonical main advanced or diverged; refusing to publish stale files")
    return head


def validate_projection(root):
    # Both source catalog and derived bytes must be valid before any write.
    result = subprocess.run(
        [sys.executable, str(Path(root) / "skills" / "skillctl.py"), "check"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise PublicationError("Canonical Skill check failed: " + (result.stderr or result.stdout))
    return check(root)


def publish(root=ROOT, *, perform_push=True):
    root = Path(root).resolve(strict=True)
    data = validate_projection(root)
    changes = validate_changed_paths(root)
    if not changes:
        return {
            "state": "ALREADY_SYNCHRONIZED",
            "commit": git(root, "rev-parse", "HEAD"),
            "digest": data["contentSHA256"],
            "version": data["version"],
        }
    prior = check_remote(root) if perform_push else git(root, "rev-parse", "HEAD")

    # Do not include any source changes in the projection commit.
    git(root, "add", "--", *changes)
    staged = set(git(root, "diff", "--cached", "--name-only").splitlines())
    if staged != set(changes):
        raise PublicationError("Staging did not preserve the exact derived file set")
    git(root, "diff", "--cached", "--check")
    if perform_push:
        git(root, "config", "user.name", "github-actions[bot]")
        git(root, "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    git(root, "commit", "-m", "plugins: sync FCIS marketplace from canonical Skill")
    result = git(root, "rev-parse", "HEAD")
    if perform_push:
        # A non-fast-forward push is rejected: no force, reset or rebase of others.
        git(root, "push", "origin", "HEAD:refs/heads/main")
        remote = git(root, "ls-remote", "origin", "refs/heads/main").split()
        if len(remote) != 2 or remote[0] != result:
            raise PublicationError("Remote branch did not read back to the published commit")
    if git(root, "status", "--porcelain", "--untracked-files=all"):
        raise PublicationError("Unexpected source changes remain after derived commit")
    if not set(changes).issubset(set(
        git(root, "show", "--pretty=format:", "--name-only", "HEAD").splitlines()
    )):
        raise PublicationError("Derived changes missing from the resulting commit")
    return {
        "state": "GITHUB_MARKETPLACE_PUBLISHED" if perform_push else "DERIVED_COMMITTED_FOR_TEST",
        "commit": result, "parent": prior, "digest": data["contentSHA256"],
        "version": data["version"], "files": changes,
    }


def main():
    try:
        output = publish()
    except (PublicationError, ProjectionError, OSError, KeyError, ValueError) as exc:
        sys.exit(f"REFUSED: {exc}")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
