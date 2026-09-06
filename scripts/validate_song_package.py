#!/usr/bin/env python3
"""Validate a vocaloid-song-studio text project against song-manifest.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SECTION_RE = re.compile(r"^\[([^\]]+)\]$", re.MULTILINE)
FENCE_RE = re.compile(r"```text\s*\n(.*?)\n```", re.DOTALL)
BOLD_RE = re.compile(r"^\*\*(.+?)\*\*\s{0,2}$", re.MULTILINE)
LOCKED_RE = re.compile(
    r"<!--\s*LYRICS_START\s*-->\s*```text\s*\n(.*?)\n```\s*<!--\s*LYRICS_END\s*-->",
    re.DOTALL,
)
PLACEHOLDER_RE = re.compile(r"<(?!\!--)[^>\n]+>|\b(?:TBD|TODO)\b|【在此填写")


def extract_lyrics(path: Path) -> str:
    match = FENCE_RE.search(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"No ```text lyric block found in {path.name}")
    return match.group(1).strip()


def split_sections(lyrics: str) -> tuple[list[str], dict[str, list[str]]]:
    markers = list(SECTION_RE.finditer(lyrics))
    if not markers:
        raise ValueError("No section tags found")
    order: list[str] = []
    sections: dict[str, list[str]] = {}
    for index, marker in enumerate(markers):
        name = marker.group(1)
        if name in sections:
            raise ValueError(f"Duplicate section tag: {name}")
        end = markers[index + 1].start() if index + 1 < len(markers) else len(lyrics)
        lines = [line.strip() for line in lyrics[marker.end():end].splitlines() if line.strip()]
        order.append(name)
        sections[name] = lines
    return order, sections


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--allow-placeholders", action="store_true")
    args = parser.parse_args()

    root = args.project.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    manifest_path = root / "song-manifest.json"
    if not manifest_path.exists():
        fail(errors, "Missing song-manifest.json")
        manifest = {}
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            fail(errors, f"Invalid song-manifest.json: {exc}")
            manifest = {}

    files = manifest.get("files", {}) if isinstance(manifest, dict) else {}
    required_keys = ["design", "lyrics", "reading_translation", "production_prompt"]
    for key in required_keys:
        name = files.get(key)
        if not name:
            fail(errors, f"Manifest missing files.{key}")
        elif not (root / name).exists():
            fail(errors, f"Missing declared file: {name}")

    lyrics_path = root / files.get("lyrics", "lyrics-ja.md")
    lyrics = ""
    order: list[str] = []
    sections: dict[str, list[str]] = {}
    if lyrics_path.exists():
        try:
            lyrics = extract_lyrics(lyrics_path)
            order, sections = split_sections(lyrics)
        except ValueError as exc:
            fail(errors, str(exc))

    expected_sections = manifest.get("sections", []) if isinstance(manifest, dict) else []
    expected_order = [item.get("tag") for item in expected_sections if isinstance(item, dict)]
    if expected_order and order != expected_order:
        fail(errors, f"Section order mismatch: expected {expected_order}, got {order}")
    for item in expected_sections:
        if not isinstance(item, dict):
            continue
        tag = item.get("tag")
        expected_count = item.get("lines")
        if tag in sections and isinstance(expected_count, int) and len(sections[tag]) != expected_count:
            fail(errors, f"{tag}: expected {expected_count} lines, got {len(sections[tag])}")

    hook = manifest.get("hook", {}) if isinstance(manifest, dict) else {}
    source_tag = hook.get("source_section")
    line_numbers = hook.get("line_numbers", [])
    if source_tag in sections and line_numbers:
        try:
            source_hook = [sections[source_tag][number - 1] for number in line_numbers]
            for target_tag in hook.get("repeat_sections", []):
                if target_tag not in sections:
                    fail(errors, f"Hook repeat section missing: {target_tag}")
                    continue
                target_hook = [sections[target_tag][number - 1] for number in line_numbers]
                if target_hook != source_hook:
                    fail(errors, f"Hook mismatch between {source_tag} and {target_tag}")
        except (IndexError, TypeError):
            fail(errors, "Hook line_numbers are invalid")

    reading_name = files.get("reading_translation")
    if lyrics and reading_name and (root / reading_name).exists():
        originals = [match.strip() for match in BOLD_RE.findall((root / reading_name).read_text(encoding="utf-8"))]
        lyric_lines = [line for tag in order for line in sections[tag]]
        if originals != lyric_lines:
            fail(errors, f"Reading file originals differ from lyrics: {len(originals)} vs {len(lyric_lines)} lines")

    prompt_name = files.get("production_prompt")
    if lyrics and prompt_name and (root / prompt_name).exists():
        prompt = (root / prompt_name).read_text(encoding="utf-8")
        locked = LOCKED_RE.search(prompt)
        if locked:
            if locked.group(1).strip() != lyrics:
                fail(errors, "Locked lyrics in production prompt differ from lyrics file")
        elif lyrics not in prompt:
            fail(errors, "Production prompt does not contain the complete frozen lyrics")
        else:
            warnings.append("Production prompt contains lyrics but lacks LYRICS_START/LYRICS_END markers")

    if not args.allow_placeholders:
        for path in root.glob("*.md"):
            match = PLACEHOLDER_RE.search(path.read_text(encoding="utf-8"))
            if match:
                fail(errors, f"Placeholder in {path.name}: {match.group(0)}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        for warning in warnings:
            print(f"- warning: {warning}")
        return 1

    print("PASS")
    print(f"- sections: {len(order)}")
    print(f"- lyric lines: {sum(len(lines) for lines in sections.values())}")
    for warning in warnings:
        print(f"- warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
