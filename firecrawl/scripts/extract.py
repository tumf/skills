#!/usr/bin/env python3
"""
Extract structured data from web pages using Firecrawl API with LLM capabilities.

Usage:
    extract.py <url> [<url>...] --prompt "extraction prompt" [--schema '{"type":"object",...}']

Examples:
    extract.py "https://example.com/pricing" --prompt "Extract pricing tiers"
    extract.py "https://example.com/team" --prompt "Extract team members" --schema '{"type":"object","properties":{"members":{"type":"array"}}}'
"""

import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Extract structured data from web pages using LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://example.com/pricing" --prompt "Extract all pricing tiers"
  
  %(prog)s "https://example.com/team" \\
    --prompt "Extract team member information" \\
    --schema '{"type":"object","properties":{"members":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"role":{"type":"string"}}}}}}'
  
  %(prog)s "https://example.com/page1" "https://example.com/page2" \\
    --prompt "Extract product information"
        """,
    )
    parser.add_argument("urls", nargs="+", help="URL(s) to extract data from")
    parser.add_argument(
        "--prompt",
        required=True,
        help="Extraction prompt describing what data to extract",
    )
    parser.add_argument(
        "--schema",
        type=str,
        help="JSON schema for structured output (optional)",
    )

    args = parser.parse_args()

    # Check for API key
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

    # Parse schema if provided
    schema = None
    if args.schema:
        try:
            schema = json.loads(args.schema)
        except json.JSONDecodeError as e:
            print(
                json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid JSON schema: {e}",
                    }
                )
            )
            sys.exit(1)

    try:
        from firecrawl import FirecrawlApp

        app = FirecrawlApp(api_key=api_key)

        params = {
            "prompt": args.prompt,
        }
        if schema:
            params["schema"] = schema

        result = app.extract(args.urls, params=params)

        print(json.dumps({"success": True, "data": result}, indent=2, default=str))

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
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
