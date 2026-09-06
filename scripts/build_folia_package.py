#!/usr/bin/env python3
"""Build a minimal Folia folder-import package without modifying source media."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

AUDIO_EXTENSIONS = {".mp3", ".flac", ".m4a", ".wav", ".ogg", ".opus", ".aac"}
COVER_NAMES = {".png": "cover.png", ".jpg": "cover.jpg", ".jpeg": "cover.jpeg"}
MANAGED_NAMES = {".foliaignore", "Folia导入说明.md"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--lyrics", required=True, type=Path)
    parser.add_argument("--translation", type=Path)
    parser.add_argument("--cover", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def ensure_source(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not resolved.is_file():
        raise SystemExit(f"Missing {label}: {resolved}")
    return resolved


def main() -> int:
    args = parse_args()
    audio = ensure_source(args.audio, "audio")
    lyrics = ensure_source(args.lyrics, "lyrics")
    cover = ensure_source(args.cover, "cover")
    translation = ensure_source(args.translation, "translation") if args.translation else None

    if audio.suffix.lower() not in AUDIO_EXTENSIONS:
        raise SystemExit(f"Unsupported audio extension: {audio.suffix}")
    if lyrics.suffix.lower() != ".lrc":
        raise SystemExit("Main lyrics must be an .lrc file")
    if translation and not translation.name.lower().endswith(".t.lrc"):
        raise SystemExit("Translation lyrics must use the .t.lrc suffix")
    cover_name = COVER_NAMES.get(cover.suffix.lower())
    if not cover_name:
        raise SystemExit("Cover must be PNG, JPG, or JPEG")

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    targets = {
        output / f"{args.title}{audio.suffix.lower()}": audio,
        output / f"{args.title}.lrc": lyrics,
        output / cover_name: cover,
    }
    if translation:
        targets[output / f"{args.title}.t.lrc"] = translation

    existing = [str(path) for path in targets if path.exists()]
    existing.extend(str(output / name) for name in MANAGED_NAMES if (output / name).exists())
    if existing and not args.force:
        raise SystemExit("Managed output files already exist; use --force:\n" + "\n".join(existing))

    for target, source in targets.items():
        shutil.copy2(source, target)

    (output / ".foliaignore").write_text(
        "# Backups kept beside the package can be excluded with these patterns.\n"
        "Tunee_*.lrc\n"
        "*_original.*\n",
        encoding="utf-8",
        newline="\n",
    )

    translation_line = f"├─ {args.title}.t.lrc     中文翻译歌词\n" if translation else ""
    guide = f"""# Folia 导入说明

这个目录是最小化的一键文件夹导入包。

```text
{output.name}/
├─ {args.title}{audio.suffix.lower()}       主音频
├─ {args.title}.lrc       主时间轴歌词
{translation_line}├─ {cover_name}              文件夹封面
└─ .foliaignore          可选备份忽略规则
```

在 Folia 的“本地音乐”区域点击“导入文件夹”，选择当前目录。音频与歌词使用相同基础名，封面使用 Folia 优先识别的固定文件名。

若这个目录以前导入过，请执行“重新导入”。Web 版文件夹导入依赖 File System Access API；不可用时使用桌面版或支持该 API 的 Chromium 系浏览器。
"""
    (output / "Folia导入说明.md").write_text(guide, encoding="utf-8", newline="\n")

    print(f"Built Folia package: {output}")
    for path in sorted(output.iterdir()):
        if path.is_file():
            print(f"  {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
