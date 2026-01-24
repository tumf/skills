#!/usr/bin/env python3
"""
Crawl multiple pages from a website using Firecrawl API.

Usage:
    crawl.py <url> [--limit N] [--depth N] [--async]

Examples:
    crawl.py "https://docs.example.com"
    crawl.py "https://docs.example.com" --limit 20
    crawl.py "https://docs.example.com" --limit 10 --depth 2
    crawl.py "https://docs.example.com" --async
"""

import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Crawl multiple pages from a website",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://docs.example.com"
  %(prog)s "https://docs.example.com" --limit 20
  %(prog)s "https://docs.example.com" --limit 10 --depth 2
  %(prog)s "https://docs.example.com" --async

Note: Crawling can be slow for large sites. Consider using map + scrape for better control.
        """,
    )
    parser.add_argument("url", help="Base URL to crawl")
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of pages to crawl (default: 10)",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=2,
        help="Maximum crawl depth (default: 2)",
    )
    parser.add_argument(
        "--async",
        dest="async_mode",
        action="store_true",
        help="Start async crawl and return job ID",
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

        params = {
            "limit": args.limit,
            "maxDepth": args.depth,
            "scrapeOptions": {
                "formats": ["markdown"],
                "onlyMainContent": True,
            },
        }

        if args.async_mode:
            # Start async crawl
            result = app.async_crawl_url(args.url, params=params)
            print(
                json.dumps(
                    {
                        "success": True,
                        "async": True,
                        "data": result,
                        "message": "Crawl started. Use the job ID to check status.",
                    },
                    indent=2,
                    default=str,
                )
            )
        else:
            # Synchronous crawl (waits for completion)
            result = app.crawl_url(args.url, params=params)
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
