#!/usr/bin/env python3
"""Fetch and clean YouTube video transcript.

Usage:
    python fetch_transcript.py <video_url_or_id> [--lang LANG]

Output:
    Prints cleaned transcript text to stdout.
    Prints metadata (title, video_id, language) to stderr as JSON.

Dependencies:
    pip install yt-dlp
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile


def extract_video_id(url_or_id: str) -> str:
    """Extract YouTube video ID from URL or return as-is if already an ID."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pat in patterns:
        m = re.search(pat, url_or_id)
        if m:
            return m.group(1)
    return url_or_id


def clean_vtt(filepath: str) -> str:
    """Parse VTT file and return deduplicated plain text."""
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    text_blocks: list[str] = []
    prev = ""

    for line in lines:
        # Skip VTT headers and timestamps
        if (
            line.startswith("WEBVTT")
            or line.startswith("Kind:")
            or line.startswith("Language:")
            or "-->" in line
            or line.strip() == ""
        ):
            continue
        # Strip VTT tags like <00:00:01.234><c>word</c>
        clean = re.sub(r"<[^>]+>", "", line).strip()
        if clean and clean != prev:
            text_blocks.append(clean)
            prev = clean

    # Remove consecutive duplicates
    final: list[str] = []
    for block in text_blocks:
        if not final or final[-1] != block:
            final.append(block)

    return " ".join(final)


def fetch_transcript(video_id: str, lang: str = "ja") -> dict:
    """Download auto-generated subtitles via yt-dlp and return cleaned text.

    Returns dict with keys: video_id, title, language, transcript
    """
    url = f"https://www.youtube.com/watch?v={video_id}"

    with tempfile.TemporaryDirectory() as tmpdir:
        output_template = os.path.join(tmpdir, "%(id)s")

        # First get the title
        title_cmd = [
            "yt-dlp",
            "--print",
            "title",
            "--skip-download",
            url,
        ]
        result = subprocess.run(title_cmd, capture_output=True, text=True)
        title = result.stdout.strip() if result.returncode == 0 else ""

        # Try original language first (e.g. ja-orig), then fall back to lang
        langs_to_try = [f"{lang}-orig", lang, "en"]
        vtt_path = None

        for try_lang in langs_to_try:
            sub_cmd = [
                "yt-dlp",
                "--write-auto-subs",
                "--skip-download",
                "--sub-lang",
                try_lang,
                "--sub-format",
                "vtt",
                "-o",
                output_template,
                url,
            ]
            subprocess.run(sub_cmd, capture_output=True, text=True)

            # Look for downloaded VTT file
            for fname in os.listdir(tmpdir):
                if fname.endswith(".vtt"):
                    vtt_path = os.path.join(tmpdir, fname)
                    break

            if vtt_path and os.path.getsize(vtt_path) > 0:
                actual_lang = try_lang
                break
            vtt_path = None

        if not vtt_path:
            print(
                json.dumps({"error": f"No subtitles found for video {video_id}"}),
                file=sys.stderr,
            )
            sys.exit(1)

        transcript = clean_vtt(vtt_path)

    return {
        "video_id": video_id,
        "title": title,
        "language": actual_lang,
        "transcript": transcript,
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube transcript")
    parser.add_argument("video", help="YouTube video URL or ID")
    parser.add_argument(
        "--lang", default="ja", help="Preferred subtitle language (default: ja)"
    )
    args = parser.parse_args()

    video_id = extract_video_id(args.video)
    result = fetch_transcript(video_id, lang=args.lang)

    # Metadata to stderr (JSON)
    meta = {k: v for k, v in result.items() if k != "transcript"}
    print(json.dumps(meta, ensure_ascii=False), file=sys.stderr)

    # Transcript to stdout
    print(result["transcript"])


if __name__ == "__main__":
    main()
