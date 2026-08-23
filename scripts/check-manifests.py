#!/usr/bin/env python3
"""Validate Scoop bucket manifests against their own live 64bit assets."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUCKET_DIR = REPO_ROOT / "bucket"
CHUNK_SIZE = 1024 * 1024


def parse_manifests() -> dict[str, dict]:
    """Parse every bucket/*.json and return {filename: data}."""
    manifests: dict[str, dict] = {}
    paths = sorted(BUCKET_DIR.glob("*.json"))
    if not paths:
        raise SystemExit("no bucket/*.json files found")
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            manifests[path.name] = json.load(handle)
        print(f"parsed {path.name}")
    return manifests


def check_url(url: str) -> str | None:
    """HEAD the zip URL; return an error message unless status is 200 or 302."""
    result = subprocess.run(
        ["curl", "-sI", url],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return f"{url}: curl failed ({result.returncode}): {result.stderr.strip()}"
    status_line = next(
        (line.strip() for line in result.stdout.splitlines() if line.startswith("HTTP/")),
        "",
    )
    parts = status_line.split()
    if len(parts) >= 2 and parts[1] in {"200", "302"}:
        print(f"{url}: {status_line}")
        return None
    return f"{url}: expected HTTP 200 or 302, got {status_line or result.stdout.strip()!r}"


def downloaded_sha256(url: str) -> str:
    """Return the SHA256 hex digest of the file at url (follows redirects)."""
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / "asset.zip"
        result = subprocess.run(
            ["curl", "-sL", "--fail", "-o", str(dest), url],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"{url}: download failed ({result.returncode}): {result.stderr.strip()}"
            )
        hasher = hashlib.sha256()
        with dest.open("rb") as handle:
            while True:
                chunk = handle.read(CHUNK_SIZE)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()


def check_manifest(filename: str, data: dict) -> list[str]:
    """Validate one manifest's 64bit url reachability and hash against the live zip."""
    errors: list[str] = []
    try:
        arch = data["architecture"]["64bit"]
        url = arch["url"]
        expected_hash = arch["hash"]
    except KeyError as exc:
        return [f"{filename}: missing {exc}"]

    url_error = check_url(url)
    if url_error:
        errors.append(f"{filename}: {url_error}")
        return errors

    try:
        actual_hash = downloaded_sha256(url)
    except RuntimeError as exc:
        errors.append(f"{filename}: {exc}")
        return errors

    if actual_hash.lower() != expected_hash.lower():
        errors.append(
            f"{filename}: hash mismatch: manifest={expected_hash} downloaded={actual_hash}"
        )
        return errors

    print(f"{filename}: url and hash match downloaded zip")
    return errors


def main() -> int:
    """Parse every manifest and check each 64bit url + hash. Exit 1 on any failure."""
    manifests = parse_manifests()
    errors: list[str] = []
    for filename, data in manifests.items():
        errors.extend(check_manifest(filename, data))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("check-manifests: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
