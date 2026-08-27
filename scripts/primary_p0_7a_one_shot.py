#!/usr/bin/env python3
"""One-shot local PRIMARY helper for P0-7A.

Packages the exact audited BEST56, verifies the canonical payload round-trip,
and optionally commits/pushes only artifacts/best56 from a non-main branch.
The large payload never passes through a chat/connector text transport.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from materialize_canonical_app import EXPECTED_SHA256, load_payload, validated_parts
from package_best56_artifact import DEFAULT_PARTS_DIR, package
from stage_canonical_app import discover_exact

ALLOWED_EXACT_BRANCHES = {"develop"}
ALLOWED_PREFIXES = ("feature/", "fix/", "audit/")
FORBIDDEN_BRANCHES = {"main", "master"}


def run_git(args: list[str], repo: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def current_branch(repo: Path) -> str:
    return run_git(["rev-parse", "--abbrev-ref", "HEAD"], repo).stdout.strip()


def assert_safe_branch(branch: str) -> None:
    if branch in FORBIDDEN_BRANCHES:
        raise RuntimeError(f"refusing P0-7A write on protected branch: {branch}")
    if branch not in ALLOWED_EXACT_BRANCHES and not branch.startswith(ALLOWED_PREFIXES):
        raise RuntimeError(f"branch not allowed for P0-7A automation: {branch}")


def verify_payload(parts_dir: Path) -> dict:
    parts = validated_parts(parts_dir)
    html = load_payload(parts_dir)
    return {
        "parts": [p.name for p in parts],
        "bytes": len(html),
        "sha256": EXPECTED_SHA256,
    }


def commit_payload(repo: Path, message: str, *, push: bool) -> dict:
    run_git(["add", "--", str(DEFAULT_PARTS_DIR)], repo)
    staged = run_git(["diff", "--cached", "--quiet", "--", str(DEFAULT_PARTS_DIR)], repo, check=False)
    if staged.returncode == 0:
        return {"committed": False, "pushed": False, "reason": "payload already matches index"}
    if staged.returncode != 1:
        raise RuntimeError(staged.stderr.strip() or "git diff --cached failed")

    commit = run_git(["commit", "-m", message, "--", str(DEFAULT_PARTS_DIR)], repo)
    result = {"committed": True, "pushed": False, "commit_output": commit.stdout.strip()}
    if push:
        branch = current_branch(repo)
        assert_safe_branch(branch)
        run_git(["push", "origin", branch], repo)
        result["pushed"] = True
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", nargs="?", help="exact BEST56 baseline HTML")
    parser.add_argument("--auto", action="store_true", help="discover exact BEST56 by SHA-256")
    parser.add_argument("--search-root", action="append", default=[], help="root used by --auto; may repeat")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--commit", action="store_true", help="git add + commit canonical payload")
    parser.add_argument("--push", action="store_true", help="push current safe branch after commit")
    parser.add_argument("--message", default="build: persist exact BEST56 canonical payload")
    args = parser.parse_args()

    if bool(args.candidate) == bool(args.auto):
        parser.error("choose exactly one: explicit candidate or --auto")
    if args.push and not args.commit:
        parser.error("--push requires --commit")

    repo = args.repo.expanduser().resolve()
    try:
        branch = current_branch(repo)
        assert_safe_branch(branch)
        candidate = Path(args.candidate).expanduser().resolve() if args.candidate else discover_exact(
            [Path(p) for p in args.search_root] or None
        )["candidate"]
        package_report = package(candidate, repo / DEFAULT_PARTS_DIR)
        payload_report = verify_payload(repo / DEFAULT_PARTS_DIR)
        if payload_report["sha256"] != EXPECTED_SHA256:
            raise RuntimeError("unexpected payload SHA after verification")
        git_report = {"committed": False, "pushed": False, "reason": "dry run"}
        if args.commit:
            git_report = commit_payload(repo, args.message, push=args.push)
    except (OSError, RuntimeError, ValueError, SystemExit, subprocess.CalledProcessError) as exc:
        print(f"BLOCKED: {exc}")
        return 2

    print(
        "P0-7A READY_PAYLOAD: "
        f"branch={branch} sha256={payload_report['sha256']} parts={len(payload_report['parts'])} "
        f"bytes={payload_report['bytes']} committed={git_report['committed']} pushed={git_report['pushed']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
