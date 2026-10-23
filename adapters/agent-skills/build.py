#!/usr/bin/env python3
"""
Generate agent-installable skills (SKILL.md layout) from canonical markdown in /skills.

Input:
  skills/*.md  (canonical, vendor-neutral skill definitions)

Output (COMMITTED — do not gitignore):
  skills/<skill-name>/SKILL.md

This output follows the cross-agent SKILL.md convention used by:
  - Devin plugins (.devin-plugin/plugin.json)
  - Claude Code plugins (.claude-plugin/plugin.json)
  - skills.sh / Agent Plugins-style loaders
  - any agent that scans skills/<name>/SKILL.md

Unlike the Codex adapter output, these files are committed so the repository
itself is directly installable as a plugin — no local copy step required.
Re-run this script after any change to skills/*.md (e.g. an upstream merge).

Skill names are normalized to hyphenated slugs (htmx_modal_form_flow ->
htmx-modal-form-flow) because the SKILL.md spec restricts `name` to
lowercase letters, numbers, and hyphens.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from typing import Tuple


REPO_ROOT = Path(__file__).resolve().parents[2]
CANON_SKILLS_DIR = REPO_ROOT / "skills"
OUT_DIR = REPO_ROOT / "skills"

GENERATED_MARKER = "generated-by: adapters-agent-skills"


def slugify(name: str) -> str:
    # SKILL.md name spec: lowercase letters, numbers, hyphens only.
    s = name.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


def parse_skill_name(md: str) -> str:
    """
    Preferred patterns:
      '# Skill: <name>'
    Fallback:
      first H1 line '# <name>'
    """
    m = re.search(r"^\s*#\s*Skill:\s*(.+?)\s*$", md, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()

    m = re.search(r"^\s*#\s*(.+?)\s*$", md, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()

    raise ValueError("Could not find skill name. Expected a '# Skill: ...' H1.")


def parse_intent(md: str) -> str:
    """
    Extract the first paragraph under '## Intent' as a description seed.
    """
    m = re.search(r"^##\s+Intent\s*\n(.*?)(?=^\s*##\s|\Z)", md, flags=re.MULTILINE | re.DOTALL)
    if not m:
        return ""

    block = m.group(1).strip()
    block = re.sub(r"^\s*---\s*$", "", block, flags=re.MULTILINE).strip()

    parts = [p.strip() for p in re.split(r"\n\s*\n", block) if p.strip()]
    return parts[0] if parts else ""


def first_sentence(text: str) -> str:
    t = re.sub(r"\s+", " ", text).strip()
    if not t:
        return ""
    m = re.match(r"(.+?[.!?])(\s|$)", t)
    return m.group(1).strip() if m else (t[:140].strip())


def strip_canonical_header(md: str) -> str:
    """
    Remove the top H1 '# Skill: ...' or '# ...' line.
    Keep the rest intact.
    """
    lines = md.splitlines()
    out = []
    skipped_h1 = False
    for line in lines:
        if not skipped_h1 and re.match(r"^\s*#\s+", line):
            skipped_h1 = True
            continue
        if skipped_h1 and len(out) == 0 and line.strip() == "":
            continue
        out.append(line)
    return "\n".join(out).strip() + "\n"


def yaml_string(value: str) -> str:
    # JSON encoding is valid YAML for a double-quoted scalar.
    return json.dumps(value)


def build_skill(md_path: Path) -> Tuple[str, str, str]:
    md = md_path.read_text(encoding="utf-8")
    name = slugify(parse_skill_name(md))
    intent = parse_intent(md)
    desc = first_sentence(intent)
    # A trailing ':' means the sentence introduces a list; keep the
    # last comma-separated clause so the description reads complete.
    if desc.endswith(":"):
        head = desc[:-1]
        desc = head.rsplit(",", 1)[0] if "," in head else head
    desc = desc.rstrip(":;, ") or f"HTMX skill: {name}"
    body = strip_canonical_header(md)
    return name, desc, body


def main() -> int:
    if not CANON_SKILLS_DIR.exists():
        print(f"ERROR: Missing canonical skills directory: {CANON_SKILLS_DIR}", file=sys.stderr)
        return 2

    md_files = sorted(CANON_SKILLS_DIR.glob("*.md"))
    if not md_files:
        print(f"ERROR: No skills found in: {CANON_SKILLS_DIR}", file=sys.stderr)
        return 2

    expected_dirs = set()
    generated = 0

    for md_path in md_files:
        name, desc, body = build_skill(md_path)
        folder = OUT_DIR / name
        expected_dirs.add(name)
        folder.mkdir(parents=True, exist_ok=True)
        out_path = folder / "SKILL.md"

        out = (
            "---\n"
            f"name: {name}\n"
            f"description: {yaml_string(desc)}\n"
            f"metadata:\n"
            f"  {GENERATED_MARKER}\n"
            "---\n\n"
            f"{body}"
        )

        out_path.write_text(out, encoding="utf-8")
        generated += 1
        print(f"Generated: {out_path.relative_to(REPO_ROOT)}")

    # Remove generated skill dirs whose canonical source was deleted.
    for child in OUT_DIR.iterdir():
        if not child.is_dir() or child.name in expected_dirs:
            continue
        skill_md = child / "SKILL.md"
        if skill_md.exists() and GENERATED_MARKER in skill_md.read_text(encoding="utf-8"):
            shutil.rmtree(child)
            print(f"Removed stale generated skill: {child.relative_to(REPO_ROOT)}")

    print(f"\nDone. Generated {generated} skill(s) into: {OUT_DIR.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
