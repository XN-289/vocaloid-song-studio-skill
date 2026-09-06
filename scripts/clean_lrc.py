#!/usr/bin/env python3
"""Remove production directions and terminal markers from generated LRC files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TIMED_RE = re.compile(r"^(\[(?:\d{1,3}:)?\d{2}:\d{2}(?:[.:]\d{1,3})?\]|\[\d{2}:\d{2}(?:[.:]\d{1,3})?\])(.*)$")
SIMPLE_TIMED_RE = re.compile(r"^(\[\d{2}:\d{2}(?:[.:]\d{1,3})?\])(.*)$")
METADATA_RE = re.compile(r"^\[(ti|ar|al|by|offset|re|ve):.*\]$", re.IGNORECASE)
ASCII_DIRECTION_RE = re.compile(r"^\([^\n]*[A-Za-z][^\n]*\)$")
TRAILING_DIRECTION_RE = re.compile(r"\s*\([^\n]*[A-Za-z][^\n]*\)\s*$")
END_RE = re.compile(r"^\[?end\]?$", re.IGNORECASE)


def clean_lines(lines: list[str], keep_role_labels: bool = False) -> list[str]:
    output: list[str] = []
    for raw in lines:
        line = raw.rstrip("\r\n")
        if not line.strip():
            if output and output[-1] != "":
                output.append("")
            continue
        if METADATA_RE.match(line.strip()):
            output.append(line.strip())
            continue

        match = SIMPLE_TIMED_RE.match(line.strip())
        if not match:
            continue
        stamp, content = match.groups()
        content = content.strip()
        if not content or END_RE.match(content):
            continue
        if ASCII_DIRECTION_RE.match(content):
            continue
        content = TRAILING_DIRECTION_RE.sub("", content).strip()
        if not content or END_RE.match(content):
            continue
        output.append(f"{stamp}{content}")

    while output and output[-1] == "":
        output.pop()
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--keep-role-labels", action="store_true", help="Reserved for explicit role-label workflows")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.output.exists() and not args.force:
        raise SystemExit(f"Output exists; use --force to replace it: {args.output}")

    source = args.input.read_text(encoding="utf-8-sig").splitlines()
    cleaned = clean_lines(source, keep_role_labels=args.keep_role_labels)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(cleaned) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {args.output} with {sum(1 for line in cleaned if SIMPLE_TIMED_RE.match(line))} timed lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
