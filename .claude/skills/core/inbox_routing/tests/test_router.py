"""Tests for inbox_routing.router."""

from pathlib import Path

import pytest

from inbox_routing.router import (
    DeptRule,
    _load_shared_pack,
    _parse_routing_keywords_yaml,
    _resolve_keywords_from_skill_md,
    collect_pending,
    decide_route,
    load_dept_rules,
    parse_frontmatter,
    route_file,
    score_file_against_rules,
)


def _make_kw_file(dept_dir: Path, dept_name: str, keywords: list[str]) -> Path:
    """Create a memory/capture_routing_keywords.md for a fake dept."""
    mem = dept_dir / "memory"
    mem.mkdir(parents=True, exist_ok=True)
    kw_path = mem / "capture_routing_keywords.md"
    body = "---\n"
    body += f"name: kw {dept_name}\n"
    body += "type: reference\n"
    body += f"dept: {dept_name}\n"
    body += "keywords:\n"
    for k in keywords:
        body += f"  - {k}\n"
    body += "---\n\nbody.\n"
    kw_path.write_text(body, encoding="utf-8")
    return kw_path


@pytest.fixture
def fake_workspace(tmp_path):
    """Fake COWORK with DEPARTMENTS/{FINANCE,MEDIA,SOFTWARE DEV,CEO} + INBOX + Clippings."""
    depts = tmp_path / "DEPARTMENTS"
    for d in ("FINANCE", "MEDIA", "SOFTWARE DEV", "CEO"):
        (depts / d).mkdir(parents=True)
    _make_kw_file(depts / "FINANCE", "FINANCE", ["tradingview", "oklo", "thinkorswim"])
    _make_kw_file(depts / "MEDIA", "MEDIA", ["widget", "gizmo platform", "flagship product"])
    _make_kw_file(depts / "SOFTWARE DEV", "SOFTWARE DEV", ["api", "python", "react"])
    # CEO has no kw file — it just receives stubs
    (tmp_path / "INBOX" / "processed").mkdir(parents=True)
    (tmp_path / "Clippings").mkdir()
    return tmp_path


class TestParseFrontmatter:
    def test_inline_list(self):
        text = '---\ntags: [a, b, c]\n---\nbody'
        fm, body = parse_frontmatter(text)
        assert fm["tags"] == ["a", "b", "c"]
        assert body == "body"

    def test_block_list(self):
        text = '---\nkeywords:\n  - foo\n  - bar baz\n---\n\ndone'
        fm, _ = parse_frontmatter(text)
        assert fm["keywords"] == ["foo", "bar baz"]

    def test_no_frontmatter(self):
        text = "just body"
        fm, body = parse_frontmatter(text)
        assert fm == {}
        assert body == "just body"

    def test_quoted_string(self):
        text = '---\noriginal_filename: "Hello World.png"\n---\nx'
        fm, _ = parse_frontmatter(text)
        assert fm["original_filename"] == "Hello World.png"


class TestLoadDeptRules:
    def test_finds_all_kw_files(self, fake_workspace, monkeypatch):
        monkeypatch.setattr("inbox_routing.router.DEPARTMENTS_DIR", fake_workspace / "DEPARTMENTS")
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        names = {r.name for r in rules}
        assert names == {"FINANCE", "MEDIA", "SOFTWARE DEV"}

    def test_dept_without_kw_file_is_skipped(self, fake_workspace):
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        assert "CEO" not in {r.name for r in rules}


class TestScoring:
    def test_keyword_hit_in_body(self, fake_workspace):
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "x.md"
        f.write_text("---\ntags: []\n---\n\nThis is a TradingView screenshot of OKLO chart.\n")
        scores = score_file_against_rules(f, rules)
        assert scores.get("FINANCE", 0) >= 2
        assert "MEDIA" not in scores

    def test_keyword_hit_in_filename(self, fake_workspace):
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "widget-mcp-server-thing.md"
        f.write_text("---\n---\n\ngeneric note.\n")
        scores = score_file_against_rules(f, rules)
        assert "MEDIA" in scores

    def test_word_boundary_avoids_false_match(self, fake_workspace):
        # "ict" must not match "predict"
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        # Add ICT to FINANCE rules
        kw_path = fake_workspace / "DEPARTMENTS" / "FINANCE" / "memory" / "capture_routing_keywords.md"
        text = kw_path.read_text(encoding="utf-8").replace("  - thinkorswim\n", "  - thinkorswim\n  - ict\n")
        kw_path.write_text(text, encoding="utf-8")
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "predict.md"
        f.write_text("---\n---\n\nThe model predicts the future, but does not predict well.\n")
        scores = score_file_against_rules(f, rules)
        assert scores.get("FINANCE", 0) == 0

    def test_zero_hits_returns_empty(self, fake_workspace):
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "irrelevant.md"
        f.write_text("---\n---\n\nThis is unrelated content about cooking pasta.\n")
        scores = score_file_against_rules(f, rules)
        assert scores == {}


class TestDecideRoute:
    def test_primary_is_highest_scoring(self, fake_workspace):
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "x.md"
        f.write_text("---\n---\n\nTradingView OKLO ThinkOrSwim and a passing widget mention.\n")
        decision = decide_route(f, rules)
        assert decision.primary == "FINANCE"

    def test_secondary_meets_new_threshold(self, fake_workspace):
        # New threshold: secondary needs >=4 hits AND >=50% of primary score.
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "x.md"
        # FINANCE: tradingview×2, oklo×3, thinkorswim×1 = 6 hits
        # MEDIA: widget×2, gizmo platform×2 = 4 hits   →   4/6 = 67%, qualifies
        f.write_text(
            "---\n---\n\nTradingView OKLO TradingView ThinkOrSwim OKLO OKLO. "
            "Also widget widget gizmo platform gizmo platform integration.\n"
        )
        decision = decide_route(f, rules)
        assert decision.primary == "FINANCE"
        assert "MEDIA" in decision.secondaries

    def test_secondary_below_min_hits_excluded(self, fake_workspace):
        # MEDIA with only 2 hits fails the >=4 hits gate even at high ratio.
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "x.md"
        # FINANCE: 3 hits; MEDIA: 2 hits  →  MEDIA ratio = 67% but hits < 4
        f.write_text("---\n---\n\nTradingView OKLO ThinkOrSwim. your runtime platform widget.\n")
        decision = decide_route(f, rules)
        assert decision.primary == "FINANCE"
        assert "MEDIA" not in decision.secondaries

    def test_no_hits_returns_no_primary(self, fake_workspace):
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "x.md"
        f.write_text("---\n---\n\nUnrelated.\n")
        decision = decide_route(f, rules)
        assert decision.primary is None


class TestRouteFile:
    def test_moves_to_primary_and_writes_stubs(self, fake_workspace, monkeypatch):
        monkeypatch.setattr("inbox_routing.router.DEPARTMENTS_DIR", fake_workspace / "DEPARTMENTS")
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "test.md"
        # FINANCE 6 hits (primary), MEDIA 4 hits (secondary qualifies under new threshold)
        f.write_text(
            '---\ncaptured_date: 2026-05-03T13:31:00-05:00\ntags: [tradingview]\n---\n\n'
            'TradingView OKLO TradingView ThinkOrSwim OKLO OKLO. '
            'Also widget widget gizmo platform gizmo platform.\n'
        )
        decision = route_file(f, rules)
        assert decision.primary == "FINANCE"
        assert not f.exists()
        primary = fake_workspace / "DEPARTMENTS" / "FINANCE" / "context" / "2026-05" / "test.md"
        assert primary.exists()
        media_stub = fake_workspace / "DEPARTMENTS" / "MEDIA" / "context" / "2026-05" / "test.md"
        assert media_stub.exists()
        assert "cross_ref: true" in media_stub.read_text(encoding="utf-8")
        # CEO stub disabled by default — should NOT exist
        ceo_stub = fake_workspace / "DEPARTMENTS" / "CEO" / "context" / "2026-05" / "test.md"
        assert not ceo_stub.exists()

    def test_dry_run_does_not_move(self, fake_workspace, monkeypatch):
        monkeypatch.setattr("inbox_routing.router.DEPARTMENTS_DIR", fake_workspace / "DEPARTMENTS")
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "x.md"
        f.write_text("---\n---\n\nTradingView OKLO.\n")
        route_file(f, rules, dry_run=True)
        assert f.exists()
        assert not (fake_workspace / "DEPARTMENTS" / "FINANCE" / "context").exists()

    def test_unrouteable_stays_in_place(self, fake_workspace, monkeypatch):
        monkeypatch.setattr("inbox_routing.router.DEPARTMENTS_DIR", fake_workspace / "DEPARTMENTS")
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "x.md"
        f.write_text("---\n---\n\nUnrelated cooking content.\n")
        decision = route_file(f, rules)
        assert decision.primary is None
        assert f.exists()

    def test_secondary_stub_uses_full_vault_path_in_wikilink(self, fake_workspace, monkeypatch):
        """Stubs and primary share basename across depts; wikilink must use full path so Obsidian disambiguates."""
        monkeypatch.setattr("inbox_routing.router.DEPARTMENTS_DIR", fake_workspace / "DEPARTMENTS")
        monkeypatch.setattr("inbox_routing.router.COWORK_ROOT", fake_workspace)
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "shared.md"
        # FINANCE 6, MEDIA 4 — secondary qualifies under new threshold
        f.write_text(
            '---\ncaptured_date: 2026-05-03T00:00:00-05:00\n---\n\n'
            'TradingView OKLO TradingView ThinkOrSwim OKLO OKLO. '
            'widget widget gizmo platform gizmo platform.\n'
        )
        route_file(f, rules)
        media_stub = fake_workspace / "DEPARTMENTS" / "MEDIA" / "context" / "2026-05" / "shared.md"
        text = media_stub.read_text(encoding="utf-8")
        # Wikilink must reference the FINANCE primary by full path, not bare basename
        assert "[[DEPARTMENTS/FINANCE/context/2026-05/shared|shared]]" in text
        assert 'primary_path: "DEPARTMENTS/FINANCE/context/2026-05/shared.md"' in text

    def test_image_path_rewritten_after_move(self, fake_workspace, monkeypatch):
        monkeypatch.setattr("inbox_routing.router.DEPARTMENTS_DIR", fake_workspace / "DEPARTMENTS")
        rules = load_dept_rules(fake_workspace / "DEPARTMENTS")
        f = fake_workspace / "INBOX" / "processed" / "img.md"
        f.write_text(
            '---\ncaptured_date: 2026-05-03T00:00:00-05:00\nimage_ref: ../processed_images/img.png\n---\n\n'
            'TradingView OKLO. ![](../processed_images/img.png)\n'
        )
        route_file(f, rules)
        moved = fake_workspace / "DEPARTMENTS" / "FINANCE" / "context" / "2026-05" / "img.md"
        content = moved.read_text(encoding="utf-8")
        assert "../../../../INBOX/processed_images/img.png" in content


class TestSkillMdRouting:
    """Tests for the SKILL.md-as-source-of-truth path with shared keyword pack imports."""

    def _write_skill_md(self, dept_dir: Path, dept_slug: str, body: str) -> Path:
        skill_dir = dept_dir / "skills" / f"{dept_slug}-master"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_path = skill_dir / "SKILL.md"
        skill_path.write_text(body, encoding="utf-8")
        return skill_path

    def _write_pack(self, packs_dir: Path, name: str, body: str) -> Path:
        packs_dir.mkdir(parents=True, exist_ok=True)
        path = packs_dir / f"{name}.yaml"
        path.write_text(body, encoding="utf-8")
        return path

    def test_parse_routing_keywords_yaml_basic(self):
        body = """routing_keywords:
  imports: [media-domain]
  primary:
    - foo
    - bar
  secondary:
    - "baz qux"
    - hello  # comment tail
  exclude:
    - drop me
"""
        parsed = _parse_routing_keywords_yaml(body)
        assert parsed["imports"] == ["media-domain"]
        assert parsed["primary"] == ["foo", "bar"]
        assert parsed["secondary"] == ["baz qux", "hello"]
        assert parsed["exclude"] == ["drop me"]

    def test_load_shared_pack_flattens_categories(self, tmp_path):
        packs = tmp_path / "_shared_keyword_packs"
        self._write_pack(packs, "media-domain", """name: media-domain
keywords:
  timecode:
    - smpte
    - ltc
  networking:
    - ndi
    - dante
""")
        kws = _load_shared_pack("media-domain", packs_dir=packs)
        assert kws == ["smpte", "ltc", "ndi", "dante"]

    def test_load_shared_pack_missing_returns_empty(self, tmp_path):
        kws = _load_shared_pack("does-not-exist", packs_dir=tmp_path)
        assert kws == []

    def test_resolve_keywords_from_skill_md_with_imports(self, tmp_path, monkeypatch):
        # Set up a shared pack
        packs = tmp_path / "_shared_keyword_packs"
        self._write_pack(packs, "media-domain", """name: media-domain
keywords:
  timecode:
    - smpte
    - ltc
""")
        monkeypatch.setattr("inbox_routing.router.SHARED_PACKS_DIR", packs)

        # Set up a fake dept SKILL.md
        dept = tmp_path / "DEPARTMENTS" / "MEDIA_SERVER"
        skill = self._write_skill_md(dept, "media_server", """---
name: x
---

# Stuff

## Routing Keywords

```yaml
routing_keywords:
  imports: [media-domain]
  primary:
    - media_server
    - flagship
  secondary:
    - vj
  exclude:
    - widget
```

more text
""")

        kws = _resolve_keywords_from_skill_md(skill)
        # primary + imported + secondary, deduped, in order
        assert kws == ["media_server", "flagship", "smpte", "ltc", "vj"]

    def test_resolve_keywords_from_skill_md_no_block_returns_none(self, tmp_path):
        dept = tmp_path / "DEPARTMENTS" / "FOO"
        skill = self._write_skill_md(dept, "foo", "no routing block here")
        assert _resolve_keywords_from_skill_md(skill) is None

    def test_load_dept_rules_prefers_skill_md_over_mirror(self, tmp_path, monkeypatch):
        # Both SKILL.md (with routing block) AND mirror exist; SKILL.md should win.
        packs = tmp_path / "_shared_keyword_packs"
        packs.mkdir(parents=True)
        monkeypatch.setattr("inbox_routing.router.SHARED_PACKS_DIR", packs)

        depts = tmp_path / "DEPARTMENTS"
        dept = depts / "MEDIA_SERVER"

        # Mirror file with stale keywords
        (dept / "memory").mkdir(parents=True, exist_ok=True)
        mirror = dept / "memory" / "capture_routing_keywords.md"
        mirror.write_text("---\ndept: MEDIA_SERVER\nkeywords:\n  - stale_keyword\n---\n", encoding="utf-8")

        # SKILL.md with fresh routing block
        self._write_skill_md(dept, "media_server", """---
name: x
---

## Routing Keywords

```yaml
routing_keywords:
  primary:
    - media_server
    - flagship
```
""")

        monkeypatch.setattr("inbox_routing.router.COWORK_ROOT", tmp_path)
        rules = load_dept_rules(depts)
        assert len(rules) == 1
        assert rules[0].name == "MEDIA_SERVER"
        assert "media_server" in rules[0].keywords
        assert "flagship" in rules[0].keywords
        assert "stale_keyword" not in rules[0].keywords

        # Auto-mirror was written, replacing the stale content
        new_mirror = mirror.read_text(encoding="utf-8")
        assert "AUTO-GENERATED" in new_mirror
        assert "media_server" in new_mirror
        assert "stale_keyword" not in new_mirror

    def test_load_dept_rules_falls_back_to_mirror_when_skill_md_missing_block(self, tmp_path, monkeypatch):
        # SKILL.md exists but has no routing_keywords block → mirror takes over.
        depts = tmp_path / "DEPARTMENTS"
        dept = depts / "MEDIA"
        (dept / "memory").mkdir(parents=True, exist_ok=True)
        mirror = dept / "memory" / "capture_routing_keywords.md"
        mirror.write_text(
            "---\ndept: MEDIA\nkeywords:\n  - widget\n  - gizmo platform\n---\n",
            encoding="utf-8",
        )
        # SKILL.md without routing block
        self._write_skill_md(dept, "widget", "# nothing here\nno routing block")

        rules = load_dept_rules(depts)
        assert len(rules) == 1
        assert rules[0].name == "MEDIA"
        assert "widget" in rules[0].keywords
        # Mirror was preserved (no auto-rewrite when no SKILL.md source)
        assert mirror.read_text(encoding="utf-8").startswith("---\n")


class TestCollectPending:
    def test_finds_md_in_all_sources(self, fake_workspace, monkeypatch):
        monkeypatch.setattr(
            "inbox_routing.router.DEFAULT_SOURCE_DIRS",
            [fake_workspace / "INBOX" / "processed", fake_workspace / "Clippings"],
        )
        (fake_workspace / "INBOX" / "processed" / "a.md").write_text("x")
        (fake_workspace / "Clippings" / "b.md").write_text("y")
        (fake_workspace / "Clippings" / "c.txt").write_text("z")  # not md
        pending = collect_pending()
        names = {p.name for p in pending}
        assert names == {"a.md", "b.md"}
