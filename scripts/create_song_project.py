#!/usr/bin/env python3
"""Create a vocaloid-song-studio project from bundled templates."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

TEMPLATE_NAMES = [
    "lyrics-design.md",
    "lyrics-ja.md",
    "lyrics-reading-zh.md",
    "music-agent-prompt.md",
    "cover-prompt.md",
    "release-copy.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title-ja", required=True, help="Japanese song title")
    parser.add_argument("--title-zh", default="", help="Chinese title or translation")
    parser.add_argument("--output", required=True, type=Path, help="New project directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"Output directory is not empty: {output}")

    skill_root = Path(__file__).resolve().parents[1]
    templates = skill_root / "assets" / "templates"
    output.mkdir(parents=True, exist_ok=True)

    replacements = {
        "<日本語タイトル>": args.title_ja,
        "<中文标题>": args.title_zh or args.title_ja,
    }

    for name in TEMPLATE_NAMES:
        text = (templates / name).read_text(encoding="utf-8")
        for source, target in replacements.items():
            text = text.replace(source, target)
        (output / name).write_text(text, encoding="utf-8", newline="\n")

    manifest = json.loads((templates / "song-manifest.json").read_text(encoding="utf-8"))
    manifest["title"]["ja"] = args.title_ja
    manifest["title"]["zh"] = args.title_zh or args.title_ja
    (output / "song-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print(f"Created project: {output}")
    for name in ["song-manifest.json", *TEMPLATE_NAMES]:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
