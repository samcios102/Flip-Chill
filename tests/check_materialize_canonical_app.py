#!/usr/bin/env python3
from __future__ import annotations

import base64
import gzip
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "materialize_canonical_app.py"
WORKFLOW = ROOT / ".github" / "workflows" / "quality.yml"
EXPECTED = "3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=ROOT, text=True, capture_output=True)


def main() -> int:
    text = SCRIPT.read_text(encoding="utf-8")
    required = [
        "base64.b64decode",
        "gzip.decompress",
        "hashlib.sha256",
        EXPECTED,
        "os.replace",
        "PART_RE",
        "validated_parts",
        "artifact parts must be contiguous",
    ]
    for token in required:
        assert token in text, f"missing safety token: {token}"

    workflow = WORKFLOW.read_text(encoding="utf-8")
    materialize_step = "Materialize canonical BEST56 app when repository payload exists"
    materialize_command = "python scripts/materialize_canonical_app.py"
    static_step = "Static application checks"
    assert materialize_step in workflow, "CI must declare canonical materialization step"
    assert materialize_command in workflow, "CI materialization step must invoke repository materializer"
    assert workflow.index(materialize_step) < workflow.index(static_step), "CI must materialize before static checks"

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        bad_dir = tmp / "bad"
        bad_dir.mkdir()
        bad = b"not-best56"
        payload = base64.b64encode(gzip.compress(bad, mtime=0))
        (bad_dir / "best56.html.gz.b64.part001").write_bytes(payload)
        target = tmp / "app.html"
        proc = run("--parts-dir", str(bad_dir), "--output", str(target))
        assert proc.returncode != 0, "wrong SHA must be rejected"
        assert not target.exists(), "rejected artifact must not be written"

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        invalid_name = tmp / "invalid-name"
        invalid_name.mkdir()
        (invalid_name / "best56.html.gz.b64.part01").write_text("AAAA", encoding="ascii")
        proc = run("--parts-dir", str(invalid_name), "--check-only")
        assert proc.returncode != 0, "non-canonical part name must be rejected"
        assert "invalid artifact part name" in (proc.stderr + proc.stdout)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        gap_dir = tmp / "gap"
        gap_dir.mkdir()
        (gap_dir / "best56.html.gz.b64.part001").write_text("AAAA", encoding="ascii")
        (gap_dir / "best56.html.gz.b64.part003").write_text("AAAA", encoding="ascii")
        proc = run("--parts-dir", str(gap_dir), "--check-only")
        assert proc.returncode != 0, "gapped part sequence must be rejected"
        assert "artifact parts must be contiguous" in (proc.stderr + proc.stdout)

    parts_dir = ROOT / "artifacts" / "best56"
    if parts_dir.exists() and list(parts_dir.glob("best56.html.gz.b64.part*")):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "app.html"
            proc = run("--parts-dir", str(parts_dir), "--output", str(target))
            assert proc.returncode == 0, proc.stderr or proc.stdout
            assert hashlib.sha256(target.read_bytes()).hexdigest() == EXPECTED

    print("PASS: BEST56 canonical materializer contract + canonical part set + CI ordering")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
