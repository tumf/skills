#!/usr/bin/env python3
"""
Extract structured subsidy/grant program details from official pages using Firecrawl LLM extraction.

Usage:
    extract_programs.py <url> [<url> ...]

Examples:
    extract_programs.py "https://jgrants-portal.go.jp/subsidy/xxxxx"
    extract_programs.py "https://www.mhlw.go.jp/..." "https://www.chusho.meti.go.jp/..."
"""

import argparse
import json
import os
import sys


DEFAULT_SCHEMA = {
    "type": "object",
    "properties": {
        "programs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "source_url": {"type": "string"},
                    "official_urls": {"type": "array", "items": {"type": "string"}},
                    "administering_body": {"type": "string"},
                    "region": {"type": "string"},
                    "target_applicants": {"type": "string"},
                    "purpose": {"type": "string"},
                    "eligible_costs": {"type": "string"},
                    "subsidy_amount": {"type": "string"},
                    "subsidy_rate": {"type": "string"},
                    "application_window": {"type": "string"},
                    "deadline": {"type": "string"},
                    "how_to_apply": {"type": "string"},
                    "required_documents": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "pdf_urls": {"type": "array", "items": {"type": "string"}},
                    "last_updated": {"type": "string"},
                    "notes": {"type": "string"},
                    "confidence": {"type": "number"},
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
                },
                "required": ["name", "source_url"],
            },
        }
    },
    "required": ["programs"],
}


DEFAULT_PROMPT = """
You are extracting facts about Japanese subsidies/grants (補助金・助成金) from official pages.

Task:
- For EACH input URL, extract one or more subsidy/grant programs described on that page.
- Return a list of program objects under `programs`.

Rules:
- Do not guess. If a field is not present, leave it empty.
- Always set `source_url` to the page you extracted from.
- Put the most authoritative URLs in `official_urls` and any linked official PDFs in `pdf_urls`.
- Prefer quoting small, relevant snippets in `evidence_quotes` for eligibility/deadline/amount fields.
- `confidence` should be 0.0 to 1.0.

Fields:
- name
- administering_body
- region (national / prefecture / city)
- target_applicants (who can apply)
- eligible_costs (what costs are covered)
- subsidy_amount and/or subsidy_rate
- application_window and/or deadline
- how_to_apply (J-Grants, online, etc.)
- required_documents
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
        description="Extract Japanese subsidy/grant program fields from official pages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://jgrants-portal.go.jp/subsidy/xxxxx"
  %(prog)s "https://www.chusho.meti.go.jp/..." "https://www.metro.tokyo.lg.jp/..."
        """,
    )
    parser.add_argument("urls", nargs="+", help="URL(s) to extract from")
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Override extraction prompt (advanced)",
    )
    parser.add_argument(
        "--schema",
        type=str,
        help="Override JSON schema (advanced): pass a JSON string",
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
        except json.JSONDecodeError as e:
            print(json.dumps({"success": False, "error": f"Invalid JSON schema: {e}"}))
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
                {"success": True, "data": _to_jsonable(result)},
                indent=2,
                default=str,
            )
        )
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
