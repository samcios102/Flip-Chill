#!/usr/bin/env python3
"""Stage the canonical BEST56 app only from the exact audited baseline artifact.

The stager accepts either an explicit candidate path or deterministic auto-discovery
across explicitly supplied/local search roots. A file is eligible only when its
SHA-256 exactly matches the audited BEST56 baseline. It never touches `main`; it
only prepares `app/FlippChill_Kalkulator.html` in the current working tree.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import sys

EXPECTED_BEST56_SHA256 = "3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92"
DEFAULT_TARGET = Path("app/FlippChill_Kalkulator.html")
ARTIFACT_ROOTS_ENV = "FLIPPCHILL_ARTIFACT_ROOTS"
NAME_HINTS = (
    "FlippChill_Kalkulator_BEST56_BAZA_MIESZKAN.html",
    "FlippChill_Kalkulator_BEST56_BAZA_MIESZKAŃ.html",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _env_search_roots() -> list[Path]:
    raw = os.environ.get(ARTIFACT_ROOTS_ENV, "").strip()
    if not raw:
        return []
    return [Path(part) for part in raw.split(os.pathsep) if part.strip()]


def default_search_roots() -> list[Path]:
    home = Path.home()
    roots = [*_env_search_roots(), Path.cwd(), home / "Downloads", home / "Desktop", home / "OneDrive"]
    seen: set[str] = set()
    result: list[Path] = []
    for root in roots:
        key = str(root.expanduser().resolve(strict=False))
        if key not in seen:
            seen.add(key)
            result.append(root)
    return result


def _candidate_files(root: Path):
    root = root.expanduser()
    if root.is_file():
        yield root
        return
    if not root.is_dir():
        return

    for name in NAME_HINTS:
        direct = root / name
        if direct.is_file():
            yield direct

    # Keep discovery bounded and deterministic. Two levels cover repo/download
    # layouts without recursively traversing entire OneDrive trees.
    patterns = ["*.html", "*/*.html", "*/*/*.html"]
    yielded: set[Path] = set()
    for pattern in patterns:
        for path in sorted(root.glob(pattern), key=lambda p: str(p).lower()):
            if path.is_file() and path not in yielded:
                yielded.add(path)
                yield path


def discover_exact(search_roots: list[Path] | None = None) -> dict:
    roots = search_roots or default_search_roots()
    scanned = 0
    exact: list[Path] = []
    seen: set[str] = set()

    for root in roots:
        for candidate in _candidate_files(root):
            key = str(candidate.expanduser().resolve(strict=False))
            if key in seen:
                continue
            seen.add(key)
            scanned += 1
            try:
                digest = sha256(candidate)
            except OSError:
                continue
            if digest == EXPECTED_BEST56_SHA256:
                exact.append(candidate.expanduser().resolve())

    exact = sorted(exact, key=lambda p: str(p).lower())
    if not exact:
        raise FileNotFoundError(
            f"exact BEST56 not found in {len(roots)} search roots; scanned {scanned} HTML candidates"
        )

    return {
        "candidate": exact[0],
        "candidate_sha256": EXPECTED_BEST56_SHA256,
        "matches": [str(p) for p in exact],
        "scanned": scanned,
        "search_roots": [str(p.expanduser().resolve(strict=False)) for p in roots],
    }


def stage(candidate: Path, target: Path = DEFAULT_TARGET, dry_run: bool = False) -> dict:
    candidate = candidate.expanduser().resolve()
    target = target.expanduser()
    if not candidate.is_file():
        raise FileNotFoundError(f"candidate not found: {candidate}")

    candidate_sha = sha256(candidate)
    if candidate_sha != EXPECTED_BEST56_SHA256:
        raise ValueError(
            "BEST56 SHA-256 mismatch: "
            f"expected {EXPECTED_BEST56_SHA256}, got {candidate_sha} ({candidate})"
        )

    target_abs = target.resolve()
    report = {
        "candidate": str(candidate),
        "candidate_sha256": candidate_sha,
        "target": str(target_abs),
        "status": "VERIFIED_DRY_RUN" if dry_run else "STAGED",
    }
    if dry_run:
        return report

    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    try:
        shutil.copyfile(candidate, tmp)
        with tmp.open("rb") as fh:
            os.fsync(fh.fileno())
        staged_sha = sha256(tmp)
        if staged_sha != EXPECTED_BEST56_SHA256:
            raise RuntimeError(f"staged temp hash mismatch: {staged_sha}")
        os.replace(tmp, target)
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass

    target_sha = sha256(target)
    if target_sha != EXPECTED_BEST56_SHA256:
        raise RuntimeError(f"canonical target hash mismatch after replace: {target_sha}")
    report["target_sha256"] = target_sha
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", nargs="?", help="exact BEST56 baseline HTML candidate")
    parser.add_argument("--auto", action="store_true", help="discover exact BEST56 by SHA-256")
    parser.add_argument(
        "--search-root",
        action="append",
        default=[],
        help=f"directory/file searched by --auto; may be repeated. Defaults also include {ARTIFACT_ROOTS_ENV}.",
    )
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="canonical app destination")
    parser.add_argument("--dry-run", action="store_true", help="verify only; do not copy")
    args = parser.parse_args()

    if bool(args.candidate) == bool(args.auto):
        parser.error("choose exactly one: explicit candidate or --auto")

    try:
        candidate = Path(args.candidate) if args.candidate else discover_exact(
            [Path(p) for p in args.search_root] or None
        )["candidate"]
        report = stage(candidate, Path(args.target), args.dry_run)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2

    print(f"{report['status']}: {report['candidate_sha256']} -> {report['target']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
