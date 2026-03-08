#!/usr/bin/env python3
"""
Extract structured award-result details from official public pages using Firecrawl.

Usage:
    extract_award_results.py <url> [<url> ...]

Examples:
    extract_award_results.py "https://www.chusho.meti.go.jp/keiei/sapoin/2025/250728saitaku.html"
    extract_award_results.py "https://www.chusho.meti.go.jp/koukai/hojyokin/saitaku/2025/251027002.html"
"""

import argparse
import json
import os
import sys


DEFAULT_SCHEMA = {
    "type": "object",
    "properties": {
        "award_results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "program_name": {"type": "string"},
                    "source_url": {"type": "string"},
                    "official_urls": {"type": "array", "items": {"type": "string"}},
                    "administering_body": {"type": "string"},
                    "region": {"type": "string"},
                    "round_or_call": {"type": "string"},
                    "fiscal_year": {"type": "string"},
                    "publication_date": {"type": "string"},
                    "application_window": {"type": "string"},
                    "deadline": {"type": "string"},
                    "applicant_count": {"type": "string"},
                    "selected_count": {"type": "string"},
                    "selection_rate": {"type": "string"},
                    "category_breakdown": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "category": {"type": "string"},
                                "applicant_count": {"type": "string"},
                                "selected_count": {"type": "string"},
                                "notes": {"type": "string"},
                            },
                        },
                    },
                    "result_pdf_urls": {"type": "array", "items": {"type": "string"}},
                    "announcement_summary": {"type": "string"},
                    "evidence_quotes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "field": {"type": "string"},
                                "quote": {"type": "string"},
                            },
                            "required": ["field", "quote"],
                        },
                    },
                    "confidence": {"type": "number"},
                },
                "required": ["program_name", "source_url"],
            },
        }
    },
    "required": ["award_results"],
}


DEFAULT_PROMPT = """
You are extracting facts from official public award-result pages for Japanese subsidies/grants.

Task:
- For EACH input URL, extract one award-result object under `award_results`.

Rules:
- Use only facts present on the page.
- Do not invent recipient examples, project examples, or award amounts unless they are explicitly present.
- If a field is missing, leave it empty.
- Always set `source_url` to the input page URL.
- Put the most authoritative page URLs in `official_urls`.
- Put linked result PDFs or recipient-list PDFs in `result_pdf_urls`.
- Extract applicant and selected counts exactly as written when possible.
- If category/track breakdowns are present, put them in `category_breakdown`.
- Include short supporting quotes in `evidence_quotes` for `application_window`, `deadline`, `applicant_count`, and `selected_count` when present.
- `confidence` should be 0.0 to 1.0.

Fields:
- program_name
- administering_body
- region
- round_or_call
- fiscal_year
- publication_date
- application_window
- deadline
- applicant_count
- selected_count
- selection_rate
- category_breakdown
- result_pdf_urls
- announcement_summary
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
        description="Extract official public award-result fields from result pages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.chusho.meti.go.jp/keiei/sapoin/2025/250728saitaku.html"
  %(prog)s "https://www.chusho.meti.go.jp/koukai/hojyokin/saitaku/2025/251027002.html"
        """,
    )
    parser.add_argument("urls", nargs="+", help="Official award-result page URL(s)")
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
