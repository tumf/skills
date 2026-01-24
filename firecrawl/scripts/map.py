#!/usr/bin/env python3
"""
Discover all URLs on a website using Firecrawl API.

Usage:
    map.py <url> [--limit N] [--search "keyword"]

Examples:
    map.py "https://docs.example.com"
    map.py "https://example.com" --limit 100
    map.py "https://docs.example.com" --search "authentication"
"""

import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Discover all URLs on a website",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://docs.example.com"
  %(prog)s "https://example.com" --limit 100
  %(prog)s "https://docs.example.com" --search "authentication"
        """,
    )
    parser.add_argument("url", help="Base URL to map")
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of URLs to return (default: 100)",
    )
    parser.add_argument(
        "--search",
        type=str,
        help="Filter URLs containing this keyword",
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

        params = {"limit": args.limit}
        if args.search:
            params["search"] = args.search

        result = app.map_url(args.url, params=params)

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
