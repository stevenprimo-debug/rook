"""
WebFetch host allowlist gate (fail-closed).

Threat model: prompt-injection can introduce attacker-controlled URLs into
agent context. Any skill that performs autonomous WebFetch MUST validate the
target URL through this gate first. Hosts not present in known-services.json
are rejected. Default-deny.

Usage (Python):
    from _gate import check_url
    verdict = check_url("https://shopify.dev/docs/...", service_hint="shopify-admin-api")
    if verdict.allowed:
        # proceed with fetch
        ...
    else:
        # log + abort
        ...

Usage (CLI, from repo root):
    python .claude/connectors/_gate.py <url> [service-hint]
    Exit code: 0 = allowed, 1 = blocked, 2 = malformed input.

Log: appends to .claude/connectors/_gate.log
Block notice: appends to agents/librarian/memory/gate_blocks.md
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


ALLOWED_SCHEMES = {"https"}
REGISTRY_FILENAME = "known-services.json"
LOG_FILENAME = "_gate.log"
LIBRARIAN_BLOCK_LOG = "agents/librarian/memory/gate_blocks.md"


@dataclass
class Verdict:
    allowed: bool
    reason: str
    host: Optional[str] = None
    matched_service: Optional[str] = None


def _find_repo_root(start: Path) -> Optional[Path]:
    cur = start.resolve()
    for _ in range(8):
        if (cur / ".claude" / "connectors").is_dir() and (cur / "agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def _repo_root() -> Path:
    here = Path(__file__).resolve().parent
    root = _find_repo_root(here)
    if root is None:
        root = here.parent.parent
    return root


def _canonical_host(raw_host: str) -> str:
    h = raw_host.strip().lower()
    if ":" in h:
        h = h.split(":", 1)[0]
    try:
        h = h.encode("idna").decode("ascii")
    except (UnicodeError, UnicodeDecodeError):
        pass
    return h


def _load_registry(repo_root: Path) -> dict:
    path = repo_root / ".claude" / "connectors" / REGISTRY_FILENAME
    if not path.is_file():
        return {"services": []}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _append_log(repo_root: Path, url: str, service_hint: str, verdict: str, reason: str) -> None:
    log_path = repo_root / ".claude" / "connectors" / LOG_FILENAME
    log_path.parent.mkdir(parents=True, exist_ok=True)
    iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"{iso} | {url} | {service_hint or '-'} | {verdict} | {reason}\n"
    try:
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line)
    except OSError:
        pass


def _append_block_to_librarian(repo_root: Path, url: str, service_hint: str, reason: str) -> None:
    block_path = repo_root / LIBRARIAN_BLOCK_LOG
    block_path.parent.mkdir(parents=True, exist_ok=True)
    iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    needs_header = not block_path.is_file() or block_path.stat().st_size == 0
    try:
        with block_path.open("a", encoding="utf-8") as f:
            if needs_header:
                f.write("# Gate Blocks\n\n")
                f.write("Append-only log of URLs rejected by the WebFetch allowlist gate. ")
                f.write("Surfaced in the weekly digest so repeated rejections can be reviewed.\n\n")
                f.write("| timestamp | url | service-hint | reason |\n")
                f.write("|---|---|---|---|\n")
            safe_url = url.replace("|", "%7C")
            safe_reason = reason.replace("|", "%7C")
            f.write(f"| {iso} | `{safe_url}` | {service_hint or '-'} | {safe_reason} |\n")
    except OSError:
        pass


def check_url(url: str, service_hint: Optional[str] = None) -> Verdict:
    """
    Hard-gate a URL against the known-services registry.

    Default-deny. Returns Verdict(allowed=False, ...) for any host not in the
    registry, any non-https scheme, or any cross-service mismatch when
    service_hint is provided.
    """
    repo_root = _repo_root()
    service_hint = (service_hint or "").strip() or None

    if not isinstance(url, str) or not url:
        v = Verdict(False, "empty-or-non-string-url")
        _append_log(repo_root, str(url), service_hint or "", "block", v.reason)
        _append_block_to_librarian(repo_root, str(url), service_hint or "", v.reason)
        return v

    try:
        parsed = urlparse(url)
    except (ValueError, TypeError) as exc:
        v = Verdict(False, f"url-parse-error:{type(exc).__name__}")
        _append_log(repo_root, url, service_hint or "", "block", v.reason)
        _append_block_to_librarian(repo_root, url, service_hint or "", v.reason)
        return v

    scheme = (parsed.scheme or "").lower()
    if scheme not in ALLOWED_SCHEMES:
        v = Verdict(False, f"scheme-not-allowed:{scheme or 'empty'}", host=parsed.hostname)
        _append_log(repo_root, url, service_hint or "", "block", v.reason)
        _append_block_to_librarian(repo_root, url, service_hint or "", v.reason)
        return v

    if not parsed.hostname:
        v = Verdict(False, "no-host-in-url")
        _append_log(repo_root, url, service_hint or "", "block", v.reason)
        _append_block_to_librarian(repo_root, url, service_hint or "", v.reason)
        return v

    host = _canonical_host(parsed.hostname)
    registry = _load_registry(repo_root)
    services = registry.get("services", [])

    if service_hint:
        entry = next((s for s in services if s.get("service") == service_hint), None)
        if entry is None:
            v = Verdict(False, f"unknown-service-hint:{service_hint}", host=host)
            _append_log(repo_root, url, service_hint, "block", v.reason)
            _append_block_to_librarian(repo_root, url, service_hint, v.reason)
            return v
        allowed = {_canonical_host(h) for h in entry.get("allowed_hosts", [])}
        if host in allowed:
            v = Verdict(True, "host-in-named-service-allowlist", host=host, matched_service=service_hint)
            _append_log(repo_root, url, service_hint, "pass", v.reason)
            return v
        v = Verdict(False, f"cross-service-mismatch:host-not-in-{service_hint}-allowlist", host=host)
        _append_log(repo_root, url, service_hint, "block", v.reason)
        _append_block_to_librarian(repo_root, url, service_hint, v.reason)
        return v

    for entry in services:
        allowed = {_canonical_host(h) for h in entry.get("allowed_hosts", [])}
        if host in allowed:
            svc = entry.get("service", "unknown")
            v = Verdict(True, "host-in-union-allowlist", host=host, matched_service=svc)
            _append_log(repo_root, url, "", "pass", f"matched-service:{svc}")
            return v

    v = Verdict(False, "host-not-in-any-allowlist", host=host)
    _append_log(repo_root, url, "", "block", v.reason)
    _append_block_to_librarian(repo_root, url, "", v.reason)
    return v


def _cli() -> int:
    if len(sys.argv) < 2:
        sys.stderr.write("usage: _gate.py <url> [service-hint]\n")
        return 2
    url = sys.argv[1]
    hint = sys.argv[2] if len(sys.argv) > 2 else None
    v = check_url(url, hint)
    if v.allowed:
        sys.stdout.write(f"PASS host={v.host} service={v.matched_service} reason={v.reason}\n")
        return 0
    sys.stdout.write(f"BLOCK host={v.host} reason={v.reason}\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(_cli())
