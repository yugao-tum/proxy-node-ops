#!/usr/bin/env python3
"""Validate a Clash/Mihomo subscription without printing credentials."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request


BUILTIN_TARGETS = {"DIRECT", "REJECT", "REJECT-DROP", "PASS", "GLOBAL", "COMPATIBLE"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def redact_url(value: str) -> str:
    try:
        p = urllib.parse.urlsplit(value)
        host = p.hostname or ""
        if p.port:
            host += f":{p.port}"
        parts = [x for x in p.path.split("/") if x]
        if not parts:
            path = "/"
        elif re.search(r"\.(?:ya?ml|json|txt)$", parts[-1], re.IGNORECASE):
            path = ("/.../" if len(parts) > 1 else "/") + parts[-1]
        else:
            path = "/..."
        return urllib.parse.urlunsplit((p.scheme, host, path, "", ""))
    except Exception:
        return "<redacted-url>"


def redact_text(value: str) -> str:
    value = re.sub(r"(?i)\b(vless|hysteria2|hy2)://[^@\s]+@", r"\1://<redacted>@", value)
    value = re.sub(r"(?i)(https?://)([^/@\s]+)@", r"\1<redacted>@", value)
    value = re.sub(
        r"(?i)\b(password|passwd|token|auth|uuid|private[-_ ]?key|public[-_ ]?key|short[-_ ]?id)\b(\s*[:=]\s*)([^\s,}\]]+)",
        r"\1\2<redacted>",
        value,
    )
    return value


def fetch(url: str, timeout: float, direct: bool) -> tuple[bytes, dict]:
    handlers = [urllib.request.ProxyHandler({})] if direct else []
    opener = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(url, headers={"User-Agent": "proxy-node-ops-validator/1"})
    with opener.open(req, timeout=timeout) as response:
        body = response.read()
        status = getattr(response, "status", response.getcode())
        return body, {
            "url": redact_url(url),
            "status": status,
            "bytes": len(body),
            "sha256": sha256(body),
            "content_type": response.headers.get("Content-Type", ""),
        }


def load_yaml(data: bytes) -> tuple[dict | None, str | None]:
    try:
        import yaml  # type: ignore
    except Exception:
        return None, "PyYAML is unavailable"
    try:
        parsed = yaml.safe_load(data.decode("utf-8-sig"))
    except Exception as exc:
        return None, redact_text(f"{type(exc).__name__}: {exc}")
    if not isinstance(parsed, dict):
        return None, "top-level YAML value is not a mapping"
    return parsed, None


def inspect_structure(
    doc: dict,
    expected_nodes: list[str],
    expected_groups: list[str],
    show_names: bool,
) -> tuple[dict, list[str]]:
    errors: list[str] = []
    proxies = doc.get("proxies") or []
    groups = doc.get("proxy-groups") or []
    rules = doc.get("rules") or []
    if not isinstance(proxies, list):
        errors.append("proxies must be a list")
        proxies = []
    if not isinstance(groups, list):
        errors.append("proxy-groups must be a list")
        groups = []
    if not isinstance(rules, list):
        errors.append("rules must be a list")
        rules = []

    node_names = [x.get("name") for x in proxies if isinstance(x, dict) and isinstance(x.get("name"), str)]
    group_names = [x.get("name") for x in groups if isinstance(x, dict) and isinstance(x.get("name"), str)]
    for label, names in (("node", node_names), ("group", group_names)):
        duplicates = sorted({x for x in names if names.count(x) > 1})
        if duplicates:
            detail = f": {duplicates}" if show_names else ""
            errors.append(f"duplicate {label} names ({len(duplicates)}){detail}")

    for index, node in enumerate(proxies):
        if not isinstance(node, dict):
            errors.append(f"proxy #{index + 1} is not a mapping")
            continue
        missing = [key for key in ("name", "type", "server", "port") if not node.get(key)]
        if missing:
            errors.append(f"proxy #{index + 1} missing fields: {missing}")
        node_type = str(node.get("type", "")).lower()
        if node_type == "vless" and not node.get("uuid"):
            errors.append(f"VLESS proxy #{index + 1} is missing uuid")
        if node_type == "hysteria2" and not (node.get("password") or node.get("auth")):
            errors.append(f"Hysteria2 proxy #{index + 1} is missing authentication")

    valid_targets = set(node_names) | set(group_names) | BUILTIN_TARGETS
    unresolved: set[str] = set()
    for group in groups:
        if not isinstance(group, dict):
            continue
        refs = group.get("proxies") or []
        if isinstance(refs, list):
            for ref in refs:
                if isinstance(ref, str) and ref not in valid_targets:
                    unresolved.add(ref)
    if unresolved:
        detail = f": {sorted(unresolved)}" if show_names else ""
        errors.append(f"unresolved proxy-group references ({len(unresolved)}){detail}")

    missing_nodes = sorted(set(expected_nodes) - set(node_names))
    missing_groups = sorted(set(expected_groups) - set(group_names))
    if missing_nodes:
        detail = f": {missing_nodes}" if show_names else ""
        errors.append(f"missing expected nodes ({len(missing_nodes)}){detail}")
    if missing_groups:
        detail = f": {missing_groups}" if show_names else ""
        errors.append(f"missing expected groups ({len(missing_groups)}){detail}")

    protocol_counts: dict[str, int] = {}
    for node in proxies:
        if isinstance(node, dict):
            kind = str(node.get("type", "unknown"))
            protocol_counts[kind] = protocol_counts.get(kind, 0) + 1
    summary = {
        "nodes": len(proxies),
        "groups": len(groups),
        "rules": len(rules),
        "protocol_counts": protocol_counts,
    }
    if show_names:
        summary["node_names"] = node_names
        summary["group_names"] = group_names
    return summary, errors


def locate_mihomo(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    for name in ("mihomo", "mihomo.exe", "clash-meta", "clash-meta.exe"):
        found = shutil.which(name)
        if found:
            return found
    return None


def run_mihomo(executable: str, data: bytes, fresh: bool, timeout: float) -> dict:
    with tempfile.TemporaryDirectory(prefix="proxy-node-ops-") as td:
        config = Path(td) / "config.yaml"
        config.write_bytes(data)
        command = [executable, "-t"]
        if fresh:
            command += ["-d", td]
        command += ["-f", str(config)]
        completed = subprocess.run(
            command,
            cwd=td if fresh else None,
            text=True,
            capture_output=True,
            timeout=timeout,
            env={**os.environ, "NO_COLOR": "1"},
        )
        combined = "\n".join(x for x in (completed.stdout, completed.stderr) if x).strip()
        tail = "\n".join(combined.splitlines()[-20:])
        return {
            "executable": Path(executable).name,
            "fresh_data_dir": fresh,
            "return_code": completed.returncode,
            "output_tail": redact_text(tail),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    local = parser.add_mutually_exclusive_group()
    local.add_argument("--file", type=Path, help="Local Clash YAML file")
    local.add_argument("--stdin", action="store_true", help="Read local YAML bytes from stdin")
    parser.add_argument("--url", help="Served subscription URL to fetch and optionally compare")
    parser.add_argument("--direct", action="store_true", help="Ignore environment proxy settings for the URL fetch")
    parser.add_argument("--mihomo", help="Path to the Mihomo executable; auto-detected when omitted")
    parser.add_argument("--require-mihomo", action="store_true", help="Fail if Mihomo is unavailable")
    parser.add_argument("--fresh-data-dir", action="store_true", help="Run Mihomo with an empty data directory")
    parser.add_argument("--expect-node", action="append", default=[], help="Expected node name; repeat as needed")
    parser.add_argument("--expect-group", action="append", default=[], help="Expected proxy-group name; repeat as needed")
    parser.add_argument("--show-names", action="store_true", help="Include node/group labels in output; may reveal topology")
    parser.add_argument("--timeout", type=float, default=60.0, help="Fetch and Mihomo timeout in seconds")
    args = parser.parse_args()
    if not (args.file or args.stdin or args.url):
        parser.error("provide --file, --stdin, or --url")
    if args.fresh_data_dir:
        args.require_mihomo = True
    return args


def main() -> int:
    args = parse_args()
    report: dict = {"ok": False, "errors": [], "warnings": []}
    local_data: bytes | None = None
    if args.file:
        local_data = args.file.read_bytes()
        report["local"] = {"path": args.file.name, "bytes": len(local_data), "sha256": sha256(local_data)}
    elif args.stdin:
        local_data = sys.stdin.buffer.read()
        report["local"] = {"path": "<stdin>", "bytes": len(local_data), "sha256": sha256(local_data)}

    remote_data: bytes | None = None
    if args.url:
        try:
            remote_data, remote_report = fetch(args.url, args.timeout, args.direct)
            report["remote"] = remote_report
            if remote_report["status"] != 200:
                report["errors"].append(f"subscription returned HTTP {remote_report['status']}")
        except Exception as exc:
            message = f"subscription fetch failed: {type(exc).__name__}: {exc}"
            message = message.replace(args.url, redact_url(args.url))
            report["errors"].append(redact_text(message))

    if local_data is not None and remote_data is not None:
        report["hash_match"] = sha256(local_data) == sha256(remote_data)
        if not report["hash_match"]:
            report["errors"].append("served bytes do not match the local file")

    data = remote_data if remote_data is not None else local_data
    if data is None:
        report["errors"].append("no YAML bytes were available to validate")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    doc, yaml_error = load_yaml(data)
    if yaml_error:
        report["warnings"].append(f"YAML structure inspection unavailable: {yaml_error}")
    else:
        structure, errors = inspect_structure(doc or {}, args.expect_node, args.expect_group, args.show_names)
        report["structure"] = structure
        report["errors"].extend(errors)

    mihomo = locate_mihomo(args.mihomo)
    if mihomo:
        try:
            result = run_mihomo(mihomo, data, args.fresh_data_dir, args.timeout)
            report["mihomo"] = result
            if result["return_code"] != 0:
                report["errors"].append("Mihomo configuration test failed")
        except Exception as exc:
            report["errors"].append(redact_text(f"Mihomo test failed to run: {type(exc).__name__}: {exc}"))
    elif args.require_mihomo:
        report["errors"].append("Mihomo executable was required but not found")
    else:
        report["warnings"].append("Mihomo executable not found; native configuration test skipped")

    if doc is None and mihomo is None:
        report["errors"].append("neither PyYAML nor Mihomo was available for configuration validation")
    report["ok"] = not report["errors"]
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
