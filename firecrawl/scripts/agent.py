#!/usr/bin/env python3
"""
Autonomous web data gathering agent using Firecrawl API.

The agent searches, navigates, and extracts data from anywhere on the web
based on your natural language description.

Usage:
    agent.py --prompt "what data to find" [--urls url1,url2] [--schema '{"type":"object",...}']

Examples:
    agent.py --prompt "Find the founders of Firecrawl"
    agent.py --prompt "Find top 5 AI startups founded in 2024"
    agent.py --prompt "Compare features" --urls "https://a.com,https://b.com"
"""

import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Autonomous web data gathering agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --prompt "Find the founders of Firecrawl and their backgrounds"
  
  %(prog)s --prompt "Find the top 5 AI startups founded in 2024 and their funding amounts"
  
  %(prog)s --prompt "Compare the features and pricing" \\
    --urls "https://example1.com,https://example2.com"
  
  %(prog)s --prompt "Find recent tech layoffs" \\
    --schema '{"type":"object","properties":{"layoffs":{"type":"array","items":{"type":"object","properties":{"company":{"type":"string"},"count":{"type":"number"}}}}}}'

Note: The agent autonomously searches and navigates the web. No URLs required.
        """,
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Natural language description of the data you want",
    )
    parser.add_argument(
        "--urls",
        type=str,
        help="Optional comma-separated URLs to focus the agent on",
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

    # Parse URLs if provided
    urls = None
    if args.urls:
        urls = [url.strip() for url in args.urls.split(",")]

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

        # Build agent parameters
        params = {
            "prompt": args.prompt,
        }
        if urls:
            params["urls"] = urls
        if schema:
            params["schema"] = schema

        # Note: The firecrawl-py SDK may have different method names
        # Check the SDK documentation for the exact method
        # Common patterns: app.agent(), app.extract_agent(), etc.

        # Try the agent method (based on Firecrawl API)
        if hasattr(app, "agent"):
            result = app.agent(params)
        else:
            # Fallback: use extract with web search enabled
            extract_params = {
                "prompt": args.prompt,
                "enableWebSearch": True,
            }
            if schema:
                extract_params["schema"] = schema

            if urls:
                result = app.extract(urls, params=extract_params)
            else:
                # If no URLs and no agent method, we need to search first
                print(
                    json.dumps(
                        {
                            "success": False,
                            "error": "Agent functionality requires URLs or the agent method. Try using search.py first to find relevant URLs.",
                        }
                    )
                )
                sys.exit(1)

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
