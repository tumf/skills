#!/usr/bin/env python3
"""
Extract individual official award/adoption cases from public pages or PDFs using Firecrawl.

Usage:
    extract_case_examples.py <url> [<url> ...]

Examples:
    extract_case_examples.py "https://example.go.jp/saitakusha.pdf"
    extract_case_examples.py "https://example.lg.jp/case-study.html"
"""

import argparse
import json
import os
import sys


DEFAULT_SCHEMA = {
    "type": "object",
    "properties": {
        "case_examples": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "program_name": {"type": "string"},
                    "source_url": {"type": "string"},
                    "organization_name": {"type": "string"},
                    "project_title": {"type": "string"},
                    "project_summary": {"type": "string"},
                    "location": {"type": "string"},
                    "industry": {"type": "string"},
                    "round_or_year": {"type": "string"},
                    "award_amount": {"type": "string"},
                    "category": {"type": "string"},
                    "official_urls": {"type": "array", "items": {"type": "string"}},
                    "evidence_quote": {"type": "string"},
                    "confidence": {"type": "number"},
                },
                "required": ["source_url"],
            },
        }
    },
    "required": ["case_examples"],
}


DEFAULT_PROMPT = """
You are extracting individual official award/adoption cases for Japanese subsidies/grants.

Task:
- For EACH input URL, extract the individual recipient/project cases explicitly listed on the page or PDF.
- Return them under `case_examples`.

Rules:
- Use only cases explicitly present in the source.
- Do not invent organizations, project titles, summaries, industries, or award amounts.
- If the source contains only summary statistics and no individual cases, return an empty list.
- Always set `source_url` to the page or PDF you extracted from.
- Put the most authoritative URLs in `official_urls`.
- Prefer concise case rows/entries over long prose summaries.
- `evidence_quote` should contain a short exact snippet supporting the case.
- `confidence` should be 0.0 to 1.0.

Fields:
- program_name
- organization_name
- project_title
- project_summary
- location
- industry
- round_or_year
- award_amount
- category
- official_urls
- evidence_quote
""".strip()


def _to_jsonable(obj):
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, list):
        return [_to_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): _to_jsonable(v) for k, v in obj.items()}
    for meth in ("model_dump", "dict"):
        if hasattr(obj, meth):
            try:
                return _to_jsonable(getattr(obj, meth)())
            except Exception:
                pass
    if hasattr(obj, "__dict__"):
        try:
            return _to_jsonable(obj.__dict__)
        except Exception:
            pass
    return str(obj)


def main():
    parser = argparse.ArgumentParser(
        description="Extract individual official award/adoption cases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://example.go.jp/saitakusha.pdf"
  %(prog)s "https://example.lg.jp/case-study.html"
        """,
    )
    parser.add_argument(
        "urls", nargs="+", help="Official page or PDF URL(s) with individual cases"
    )
    parser.add_argument(
        "--prompt", default=DEFAULT_PROMPT, help="Override extraction prompt"
    )
    parser.add_argument(
        "--schema", type=str, help="Override JSON schema (pass JSON string)"
    )
    args = parser.parse_args()

    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": "FIRECRAWL_API_KEY environment variable not set",
                }
            )
        )
        sys.exit(1)

    schema = DEFAULT_SCHEMA
    if args.schema:
        try:
            schema = json.loads(args.schema)
        except json.JSONDecodeError as exc:
            print(
                json.dumps({"success": False, "error": f"Invalid JSON schema: {exc}"})
            )
            sys.exit(1)

    try:
        from firecrawl import FirecrawlApp
    except ImportError:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": "firecrawl-py not installed. Run: pip install firecrawl-py",
                }
            )
        )
        sys.exit(1)

    try:
        app = FirecrawlApp(api_key=api_key)
        result = app.extract(args.urls, prompt=args.prompt, schema=schema)
        print(
            json.dumps(
                {"success": True, "data": _to_jsonable(result)}, indent=2, default=str
            )
        )
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
