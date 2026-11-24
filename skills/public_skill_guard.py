#!/usr/bin/env python3
"""Refuse unapproved Skill source paths in the PUBLIC organization repository.

This is a publication boundary, not a confidentiality scanner. Run before
push, including intermediate commits. Hosted CI detects drift after upload;
it cannot undo disclosure. Keep private content out of Git from authoring.
"""
import argparse
from pathlib import PurePosixPath
import subprocess
import sys

LEGACY = frozenset({
    "estate-publisher-deployment", "fcis-go-runtime-migration",
    "fcis-skill-authoring-and-sync", "fcis-owner-access", "fcis-swift-build",
    "linotype-estate-template", "linotype-proof-press", "satzfunk-voice-render",
    "teatro-scenario-composer",
})
PUBLIC = frozenset({
    "skills/canonical/fcis-go",
    ".codex/skills/fcis-go",
    "plugins/fcis-skill-authoring-and-sync/skills/fcis-go",
    *(".codex/skills/" + name for name in LEGACY),
})
KNOWN_PRIVATE = frozenset({"fcis-console-development"})


def validate_paths(paths):
    for name in paths:
        p = PurePosixPath(name)
        parts = tuple(x.casefold() for x in p.parts)
        if any(x in KNOWN_PRIVATE for x in parts):
            raise ValueError("private Skill path refused")
        if parts[:2] == ("skills", "canonical") and name != "skills/canonical/README.md":
            if not name.startswith("skills/canonical/fcis-go/"):
                raise ValueError("unapproved public canonical Skill path")
        if parts[:2] == (".codex", "skills"):
            if len(parts) < 4 or "/".join(p.parts[:3]) not in PUBLIC:
                raise ValueError("unapproved provider Skill path")
        if parts[:1] == ("plugins",) and "skills" in parts:
            if not name.startswith("plugins/fcis-skill-authoring-and-sync/skills/fcis-go/"):
                raise ValueError("unapproved marketplace Skill path")
        if parts[:2] in {("skills", "private"), ("skills", "paid"), ("skills", "restricted")}:
            raise ValueError("private Skill custody belongs in FountainStore")
        if p.name.casefold() == "skill.md" and str(p.parent) not in PUBLIC:
            raise ValueError("unapproved Skill entrypoint in public repository")


def git(*args):
    return subprocess.check_output(["git", *args])


def tree_paths(rev):
    return git("ls-tree", "-r", "--name-only", "-z", rev).decode("utf-8").split("\0")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--staged", action="store_true")
    group.add_argument("--tree")
    group.add_argument("--range", nargs=2, metavar=("BASE", "HEAD"))
    args = parser.parse_args()
    try:
        if args.staged:
            validate_paths(git("ls-files", "--cached", "-z").decode("utf-8").split("\0"))
        elif args.tree:
            validate_paths(tree_paths(args.tree))
        else:
            base, head = args.range
            # Include every newly reachable commit, not just the final diff.
            for rev in git("rev-list", base + ".." + head).decode().splitlines():
                validate_paths(tree_paths(rev))
            validate_paths(tree_paths(head))
    except (ValueError, subprocess.CalledProcessError, UnicodeError) as exc:
        sys.exit("FCIS PUBLICATION REFUSED: " + str(exc))
    print("FCIS PUBLICATION PATHS PASS (not proof of absence of arbitrary sensitive text)")


if __name__ == "__main__":
    main()
