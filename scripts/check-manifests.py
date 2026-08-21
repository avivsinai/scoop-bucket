#!/usr/bin/env python3
"""Validate Scoop bucket manifests: parse, expected amq/sabx fields, zip URLs."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUCKET_DIR = REPO_ROOT / "bucket"

EXPECTED = {
    "amq.json": {
        "url": (
            "https://github.com/avivsinai/agent-message-queue/releases/"
            "download/v0.66.0/amq_0.66.0_windows_amd64.zip"
        ),
        "hash": "8552fe50107dc7346272d25101f33337e408375d45ed01f6c06f3c0b9f637749",
    },
    "sabx.json": {
        "url": (
            "https://github.com/avivsinai/sabx/releases/"
            "download/v0.1.11/sabx_0.1.11_windows_x86_64.zip"
        ),
        "hash": "f5d15a9d89546de939e88ab7db0688f23fee7ffca9cbb37c0c35673456d7f9da",
    },
}


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


def check_expected(manifests: dict[str, dict]) -> list[str]:
    """Return mismatch messages for amq.json and sabx.json hashes and URLs."""
    errors: list[str] = []
    for filename, expected in EXPECTED.items():
        if filename not in manifests:
            errors.append(f"{filename}: missing")
            continue
        actual_url = manifests[filename]["architecture"]["64bit"]["url"]
        actual_hash = manifests[filename]["architecture"]["64bit"]["hash"]
        if actual_url != expected["url"]:
            errors.append(f"{filename}: url mismatch")
        if actual_hash != expected["hash"]:
            errors.append(f"{filename}: hash mismatch")
        if actual_url == expected["url"] and actual_hash == expected["hash"]:
            print(f"{filename}: url and hash match")
    return errors


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


def main() -> int:
    """Run parse, exact-value, and URL checks. Exit 1 on any failure."""
    manifests = parse_manifests()
    errors = check_expected(manifests)
    for expected in EXPECTED.values():
        url_error = check_url(expected["url"])
        if url_error:
            errors.append(url_error)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("check-manifests: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
