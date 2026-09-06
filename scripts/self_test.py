#!/usr/bin/env python3
"""Run deterministic smoke tests for all bundled utility scripts."""

from __future__ import annotations

import json
import shutil
import struct
import subprocess
import sys
import tempfile
import wave
import zlib
from pathlib import Path


def run(*args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def make_png(path: Path, width: int = 2, height: int = 2) -> None:
    raw = b"".join(b"\x00" + b"\x20\x40\x80" * width for _ in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    payload = b"\x89PNG\r\n\x1a\n"
    payload += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    payload += chunk(b"IDAT", zlib.compress(raw))
    payload += chunk(b"IEND", b"")
    path.write_bytes(payload)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    scripts = root / "scripts"
    python = sys.executable

    with tempfile.TemporaryDirectory(prefix="vocaloid-song-studio-") as temp_name:
        temp = Path(temp_name)

        project = temp / "project"
        result = run(
            python,
            str(scripts / "create_song_project.py"),
            "--title-ja",
            "夜の標本",
            "--title-zh",
            "夜之标本",
            "--output",
            str(project),
        )
        assert "Created project" in result.stdout
        assert json.loads((project / "song-manifest.json").read_text(encoding="utf-8"))["title"]["ja"] == "夜の標本"
        assert len([path for path in project.iterdir() if path.is_file()]) == 7

        noisy = temp / "noisy.lrc"
        clean = temp / "clean.lrc"
        noisy.write_text(
            "[ti:夜の標本]\n"
            "[00:01.00](Fast piano enters)\n"
            "[00:02.00]夜が名前を呼んでいる\n"
            "[00:04.00]まだ帰らない (Whispered)\n"
            "[00:06.00]\n"
            "[00:08.00][End]\n",
            encoding="utf-8",
        )
        run(python, str(scripts / "clean_lrc.py"), str(noisy), str(clean))
        clean_text = clean.read_text(encoding="utf-8")
        assert "Fast piano" not in clean_text
        assert "Whispered" not in clean_text
        assert "End" not in clean_text
        assert "[00:02.00]夜が名前を呼んでいる" in clean_text
        assert "[00:04.00]まだ帰らない" in clean_text

        audio = temp / "source.wav"
        with wave.open(str(audio), "wb") as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(44100)
            wav.writeframes(b"\x00\x00\x00\x00" * 4410)
        cover = temp / "art.png"
        make_png(cover)
        translation = temp / "source.t.lrc"
        translation.write_text("[00:02.00]夜晚正在呼唤名字\n[00:04.00]我还不回去\n", encoding="utf-8")
        folia = temp / "release" / "夜の標本"
        run(
            python,
            str(scripts / "build_folia_package.py"),
            "--audio",
            str(audio),
            "--lyrics",
            str(clean),
            "--translation",
            str(translation),
            "--cover",
            str(cover),
            "--title",
            "夜の標本",
            "--output",
            str(folia),
        )
        expected = {
            "夜の標本.wav",
            "夜の標本.lrc",
            "夜の標本.t.lrc",
            "cover.png",
            ".foliaignore",
            "Folia导入说明.md",
        }
        assert {path.name for path in folia.iterdir() if path.is_file()} == expected

        sample_result = run(
            python,
            str(scripts / "validate_song_package.py"),
            str(root / "samples" / "mabataki-no-sotogawa"),
        )
        assert sample_result.stdout.startswith("PASS")

    print("PASS")
    print("- create_song_project.py")
    print("- clean_lrc.py")
    print("- build_folia_package.py")
    print("- validate_song_package.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
