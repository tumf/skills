#!/usr/bin/env python3
"""
Find and extract official public award-result pages in one step.

This helper uses the direct official fallback finder, then passes the matching URLs to
the dedicated award-result extractor.

Usage:
    extract_official_award_results.py --query "ものづくり補助金"

Examples:
    extract_official_award_results.py --query "ものづくり補助金"
    extract_official_award_results.py --query "IT導入補助金" --limit 3
"""

import argparse
import json
import os
import subprocess
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIND_SCRIPT = os.path.join(SCRIPT_DIR, "find_official_award_results.py")
EXTRACT_SCRIPT = os.path.join(SCRIPT_DIR, "extract_programs.py")
AWARD_EXTRACT_SCRIPT = os.path.join(SCRIPT_DIR, "extract_award_results.py")


def _run_json_command(command):
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(
            completed.stderr.strip() or completed.stdout.strip() or "Command failed"
        )
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON output: {exc}") from exc


def main():
    parser = argparse.ArgumentParser(
        description="Find and extract official public award-result pages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --query "ものづくり補助金"
  %(prog)s --query "IT導入補助金" --limit 3
        """,
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Query used to locate official award-result pages",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Maximum number of official result pages to extract (default: 3)",
    )
    args = parser.parse_args()

    try:
        found = _run_json_command(
            [
                sys.executable,
                FIND_SCRIPT,
                "--query",
                args.query,
                "--limit",
                str(args.limit),
            ]
        )
        urls = [item["url"] for item in found.get("results", []) if item.get("url")]
        if not urls:
            print(
                json.dumps(
                    {
                        "success": True,
                        "query": args.query,
                        "discovered_results": found.get("results", []),
                        "extracted": None,
                        "warning": "No official award-result URLs found",
                    },
                    indent=2,
                    default=str,
                )
            )
            return

        extracted = _run_json_command([sys.executable, AWARD_EXTRACT_SCRIPT, *urls])
        print(
            json.dumps(
                {
                    "success": True,
                    "query": args.query,
                    "discovered_results": found.get("results", []),
                    "extracted": extracted,
                },
                indent=2,
                default=str,
            )
        )
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
