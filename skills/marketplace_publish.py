#!/usr/bin/env python3
"""Commit only validated derived FCIS plugin files to local Git.

A versioned hook runs this after a canonical source commit; main is reached
only by a verified pull request, never by a GitHub bot direct push.
"""
import json
from pathlib import Path
import re
import subprocess
import sys

from plugin_projection import CANONICAL_SKILLS, MIRROR_PATH, PLUGIN_PATH, ProjectionError, check
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
    """Only the existing plugin manifest and reviewed five Skill mirror trees."""
    if path == (PLUGIN_PATH / "plugin.json").as_posix():
        return True
    return any(path.startswith((PLUGIN_PATH / "skills" / name).as_posix() + "/")
               for name in CANONICAL_SKILLS)


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
    raise PublicationError("Direct-to-main publishing retired; use the verified PR")


def validate_projection(root):
    # Both source catalog and derived bytes must be valid before any write.
    result = subprocess.run(
        [sys.executable, str(Path(root) / "skills" / "skillctl.py"), "check"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise PublicationError("Canonical Skill check failed: " + (result.stderr or result.stdout))
    return check(root)


def publish(root=ROOT, *, perform_push=False):
    if perform_push:
        raise PublicationError("Direct push to protected main is disabled")
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
    prior = git(root, "rev-parse", "HEAD")

    # Do not include any source changes in the projection commit.
    git(root, "add", "--", *changes)
    staged = set(git(root, "diff", "--cached", "--name-only").splitlines())
    if staged != set(changes):
        raise PublicationError("Staging did not preserve the exact derived file set")
    git(root, "diff", "--cached", "--check")
    git(root, "commit", "-m", "plugins: sync FCIS marketplace from canonical Skill")
    result = git(root, "rev-parse", "HEAD")
    if git(root, "status", "--porcelain", "--untracked-files=all"):
        raise PublicationError("Unexpected source changes remain after derived commit")
    if not set(changes).issubset(set(
        git(root, "show", "--pretty=format:", "--name-only", "HEAD").splitlines()
    )):
        raise PublicationError("Derived changes missing from the resulting commit")
    return {
        "state": "DERIVED_COMMITTED_LOCAL",
        "commit": result, "parent": prior, "digest": data["contentSHA256"],
        "version": data["version"], "files": changes,
    }


def main():
    try:
        output = publish(perform_push=False)
    except (PublicationError, ProjectionError, OSError, KeyError, ValueError) as exc:
        sys.exit(f"REFUSED: {exc}")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
