#!/usr/bin/env python3
"""Scan reusable text artifacts for credential-like values without printing them."""

from __future__ import annotations

import argparse
import ipaddress
import json
from pathlib import Path
import re
import sys


TEXT_EXTENSIONS = {
    ".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".ini", ".conf",
    ".py", ".ps1", ".sh", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs",
}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "dist", "build"}
MAX_BYTES = 2 * 1024 * 1024


def private_key_pattern() -> re.Pattern[str]:
    marker = "-----BE" + "GIN "
    return re.compile(re.escape(marker) + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----")


PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    ("private-key-block", "secret", private_key_pattern()),
    ("aws-access-key", "secret", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("tailscale-key", "secret", re.compile(r"\btskey-(?:auth|client|api)-[A-Za-z0-9_-]{10,}\b")),
    ("github-token", "secret", re.compile(r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("jwt", "secret", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("credential-uri", "secret", re.compile(r"(?i)\b(?:vless|hysteria2|hy2)://[^<\s`]+@")),
    ("tokenized-url", "secret", re.compile(r"https?://[^\s)]+/[A-Za-z0-9_-]{24,}(?:/|\b)")),
    ("secret-assignment", "secret", re.compile(
        r"(?im)^\s*(?:password|passwd|token|auth[-_]?key|private[-_]?key|client[-_]?secret|secret[-_]?access[-_]?key|uuid)\s*[:=]\s*[\"']?(?!<|your[-_]|test[-_])[^\s\"']{6,}"
    )),
    ("uuid-literal", "sensitive-identifier", re.compile(
        r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
    )),
    ("aws-instance-id", "sensitive-identifier", re.compile(r"\bi-[0-9a-f]{17}\b")),
    ("aws-account-arn", "sensitive-identifier", re.compile(r"arn:aws(?:-[a-z]+)?:[A-Za-z0-9_-]*:[^:]*:\d{12}:")),
    ("oci-ocid", "sensitive-identifier", re.compile(r"\bocid1\.[a-z0-9.]+\b")),
]
IP_CANDIDATE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")


def iter_files(paths: list[Path]):
    seen: set[Path] = set()
    for source in paths:
        if source.is_file():
            candidates = [source]
        elif source.is_dir():
            candidates = (p for p in source.rglob("*") if p.is_file())
        else:
            raise FileNotFoundError(source)
        for path in candidates:
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield resolved


def display_path(path: Path, sources: list[Path]) -> str:
    for source in sources:
        resolved = source.resolve()
        base = resolved if resolved.is_dir() else resolved.parent
        try:
            relative = path.relative_to(base)
            return str(relative) if str(relative) != "." else path.name
        except ValueError:
            continue
    return path.name


def add_finding(
    findings: list[dict], kind: str, severity: str, path_label: str, line: int
) -> None:
    findings.append({"type": kind, "severity": severity, "file": path_label, "line": line})


def scan_file(path: Path, path_label: str, findings: list[dict]) -> tuple[bool, str | None]:
    if path.stat().st_size > MAX_BYTES:
        return False, "too-large"
    try:
        text = path.read_text("utf-8")
    except (UnicodeDecodeError, OSError):
        return False, "unreadable"
    for line_number, line in enumerate(text.splitlines(), 1):
        for kind, severity, pattern in PATTERNS:
            if pattern.search(line):
                add_finding(findings, kind, severity, path_label, line_number)
        for match in IP_CANDIDATE.finditer(line):
            try:
                address = ipaddress.ip_address(match.group(0))
            except ValueError:
                continue
            if address.version == 4 and address.is_global:
                add_finding(findings, "public-ipv4", "sensitive-identifier", path_label, line_number)
    return True, None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Files or directories to scan")
    parser.add_argument(
        "--fail-on",
        choices=("all", "secret"),
        default="all",
        help="Exit nonzero for all findings or only secret findings",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    findings: list[dict] = []
    scanned = 0
    skipped: dict[str, int] = {}
    errors: list[str] = []
    try:
        files = list(iter_files(args.paths))
    except FileNotFoundError as exc:
        errors.append(f"path not found: {exc}")
        files = []
    for path in files:
        ok, reason = scan_file(path, display_path(path, args.paths), findings)
        if ok:
            scanned += 1
        elif reason:
            skipped[reason] = skipped.get(reason, 0) + 1
    blocking = [f for f in findings if args.fail_on == "all" or f["severity"] == "secret"]
    report = {
        "ok": not blocking and not errors,
        "scanned_files": scanned,
        "skipped": skipped,
        "finding_count": len(findings),
        "findings": findings,
        "errors": errors,
        "note": "Matched values are intentionally omitted.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
