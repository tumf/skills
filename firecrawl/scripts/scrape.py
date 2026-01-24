#!/usr/bin/env python3
"""
Scrape content from a single URL using Firecrawl API.

Usage:
    scrape.py <url> [--format markdown|html] [--only-main]

Examples:
    scrape.py "https://example.com"
    scrape.py "https://example.com" --format html
    scrape.py "https://example.com" --only-main
"""

import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Scrape content from a single URL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://example.com"
  %(prog)s "https://example.com" --format html
  %(prog)s "https://example.com" --only-main
        """,
    )
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument(
        "--format",
        choices=["markdown", "html"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--only-main",
        action="store_true",
        help="Extract only main content (removes headers, footers, etc.)",
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

    try:
        from firecrawl import FirecrawlApp

        app = FirecrawlApp(api_key=api_key)

        # Call scrape with keyword arguments
        result = app.scrape(args.url, formats=[args.format], only_main_content=args.only_main)

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
