#!/usr/bin/env python3
"""Promote KEEP lines from a daily log into MEMORY.md.

The daily log should contain bullet lines like:

  - KEEP: staging deploys hit prod directly

This script appends a "Promoted" section to MEMORY.md.

All output is JSON on stdout.

Examples:
  python3 promote_keep.py --daily ./memory/2026-02-19.md --memory ./MEMORY.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


KEEP_RE = re.compile(r"^\s*[-*]\s*KEEP:\s*(.+?)\s*$")


def _read_keep_lines(daily_path: Path) -> list[str]:
    keep_lines: list[str] = []
    for line in daily_path.read_text(encoding="utf-8").splitlines():
        m = KEEP_RE.match(line)
        if m:
            keep_lines.append(m.group(1))
    return keep_lines


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promote KEEP lines from a daily memory log into MEMORY.md",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s --daily ./memory/2026-02-19.md --memory ./MEMORY.md
""",
    )
    parser.add_argument("--daily", required=True, help="Path to memory/YYYY-MM-DD.md")
    parser.add_argument("--memory", required=True, help="Path to MEMORY.md")
    args = parser.parse_args()

    try:
        daily_path = Path(args.daily).expanduser().resolve()
        memory_path = Path(args.memory).expanduser().resolve()

        if not daily_path.exists():
            raise FileNotFoundError(f"Daily file not found: {daily_path}")

        keep_lines = _read_keep_lines(daily_path)
        if not keep_lines:
            print(json.dumps({"success": True, "result": {"promoted": 0}}))
            return 0

        stamp = daily_path.stem
        block = "\n".join([f"- {x} (from {stamp})" for x in keep_lines])

        existing = (
            memory_path.read_text(encoding="utf-8") if memory_path.exists() else ""
        )
        if existing and not existing.endswith("\n"):
            existing += "\n"

        updated = existing + "\n## Promoted\n\n" + block + "\n"
        memory_path.parent.mkdir(parents=True, exist_ok=True)
        memory_path.write_text(updated, encoding="utf-8")

        print(
            json.dumps(
                {
                    "success": True,
                    "result": {
                        "promoted": len(keep_lines),
                        "memory": str(memory_path),
                        "daily": str(daily_path),
                    },
                },
                indent=2,
            )
        )
        return 0
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
