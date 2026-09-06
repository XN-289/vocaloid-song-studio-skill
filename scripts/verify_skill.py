#!/usr/bin/env python3
"""Verify the distributable skill is self-contained, text-first, and publishable."""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

REQUIRED = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "references/workflow.md",
    "references/story-and-song-design.md",
    "references/japanese-lyrics.md",
    "references/hooks-and-structure.md",
    "references/production-agent-prompt.md",
    "references/post-production.md",
    "references/originality-and-safety.md",
    "references/quality-gates.md",
    "scripts/create_song_project.py",
    "scripts/validate_song_package.py",
    "scripts/clean_lrc.py",
    "scripts/build_folia_package.py",
    "scripts/self_test.py",
    "samples/mabataki-no-sotogawa/README.md",
]
BANNED_MEDIA = {".wav", ".mp3", ".flac", ".m4a", ".ogg", ".opus", ".aac", ".mp4", ".mov", ".webm"}
LOCAL_PATH_RE = re.compile(r"(?:(?<![A-Za-z0-9_])[A-Za-z]:[\\/]|/Users/|/home/[^/\s]+/)")
EXTERNAL_SKILL_RE = re.compile(r"(?:superpowers:|skill-creator|write-a-skill)", re.IGNORECASE)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md lacks YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if line.startswith(" ") or not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"\'')
    return fields


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.skill.resolve()
    errors: list[str] = []

    for relative in REQUIRED:
        if not (root / relative).exists():
            errors.append(f"Missing required path: {relative}")

    skill_path = root / "SKILL.md"
    if skill_path.exists():
        text = skill_path.read_text(encoding="utf-8")
        try:
            fields = parse_frontmatter(text)
            if fields.get("name") != "vocaloid-song-studio":
                errors.append("Frontmatter name must be vocaloid-song-studio")
            description = fields.get("description", "")
            if not description or len(description) > 1024:
                errors.append("Description must be present and <= 1024 characters")
        except ValueError as exc:
            errors.append(str(exc))

        body_lines = text.split("\n---\n", 1)[-1].splitlines()
        if len(body_lines) > 180:
            errors.append(f"SKILL.md body is too long for progressive disclosure: {len(body_lines)} lines")

        for link in MARKDOWN_LINK_RE.findall(text):
            if "://" in link or link.startswith("#"):
                continue
            target = (root / link).resolve()
            if not target.exists():
                errors.append(f"Broken SKILL.md link: {link}")

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() in BANNED_MEDIA:
            errors.append(f"Media file must not be packaged: {relative}")
        if path.stat().st_size > 1_000_000:
            errors.append(f"File exceeds 1 MB: {relative}")
        is_self_verifier = relative == "scripts/verify_skill.py"
        if (path.suffix.lower() in {".md", ".json", ".txt", ".py", ".lrc"} or path.name in {"LICENSE", ".foliaignore"}) and not is_self_verifier:
            text = path.read_text(encoding="utf-8")
            if LOCAL_PATH_RE.search(text):
                errors.append(f"Private absolute path found: {relative}")
            if EXTERNAL_SKILL_RE.search(text):
                errors.append(f"External Skill dependency named in package: {relative}")
        if path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                errors.append(f"Python syntax error in {relative}: {exc}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    files = [path for path in root.rglob("*") if path.is_file()]
    print("PASS")
    print(f"- files: {len(files)}")
    print(f"- bytes: {sum(path.stat().st_size for path in files)}")
    print("- external skill dependencies: 0")
    print("- packaged media files: 0")
    print("- private absolute paths: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
