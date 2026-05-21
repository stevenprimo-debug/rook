"""
ROOK Brand Loader — reads brand config and emits a JSON dict of brand tokens.

Priority order:
  1. ROOK_BRAND_OVERRIDE env var -> path to an override brand config file
  2. .claude/memory/rook_brand.md (ship product default)

Emitted dict consumed by HTML templates:
  {primary_color, secondary_color, accent, body_font, heading_font, logo_url, brand_name}

Usage:
    python brand-loader.py           # print JSON dict
    python brand-loader.py --check   # validate config only
"""

import json
import os
import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).parents[3]
DEFAULT_BRAND_PATH = VAULT_ROOT / ".claude" / "memory" / "rook_brand.md"

SHIP_DEFAULTS = {
    "primary_color": "#0F172A",
    "secondary_color": "#1E293B",
    "accent": "#3B82F6",
    "body_font": "Inter, system-ui, sans-serif",
    "heading_font": "Inter, system-ui, sans-serif",
    "logo_url": "",
    "brand_name": "ROOK"
}

BRAND_KEYS = list(SHIP_DEFAULTS.keys())


def _parse_brand_file(path: Path) -> dict:
    if not path.exists():
        return {}
    content = path.read_text(encoding="utf-8", errors="ignore")
    result = {}
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        for line in fm_match.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k in BRAND_KEYS and v:
                    result[k] = v
    for line in content.splitlines():
        for key in BRAND_KEYS:
            pattern = rf"^\s*[*-]?\s*`?{key}`?\s*[:\-]\s*(.+)$"
            m = re.match(pattern, line, re.IGNORECASE)
            if m and key not in result:
                result[key] = m.group(1).strip().strip('"').strip("'")
    return result


def load_brand() -> dict:
    override_path = os.environ.get("ROOK_BRAND_OVERRIDE")
    if override_path:
        p = Path(override_path)
        if p.exists():
            return {**SHIP_DEFAULTS, **_parse_brand_file(p)}
        print(f"WARNING: ROOK_BRAND_OVERRIDE missing: {override_path}", file=sys.stderr)
    if DEFAULT_BRAND_PATH.exists():
        return {**SHIP_DEFAULTS, **_parse_brand_file(DEFAULT_BRAND_PATH)}
    return SHIP_DEFAULTS.copy()


if __name__ == "__main__":
    brand = load_brand()
    if "--check" in sys.argv:
        missing = [k for k in BRAND_KEYS if not brand.get(k)]
        if missing:
            print(f"WARN: missing brand keys: {missing}")
        else:
            print("OK: all brand keys present")
    else:
        print(json.dumps(brand, indent=2))
