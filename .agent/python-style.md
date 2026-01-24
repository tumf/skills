# Python Script Style Guide

## File Structure

Every Python script should follow this order:

1. **Shebang**: `#!/usr/bin/env python3`
2. **Docstring**: Multi-line module docstring with description and examples
3. **Imports**: Standard library first, then third-party (alphabetical within groups)
4. **Main function**: Business logic in `main()` function
5. **Entry point**: `if __name__ == "__main__":` at bottom

## Import Guidelines

```python
# Standard library imports (always at top)
import argparse
import json
import os
import sys

# Third-party imports (inside try/except for graceful error handling)
try:
    from firecrawl import FirecrawlApp
except ImportError:
    print(json.dumps({
        "success": False,
        "error": "Required package not installed. Run: pip install firecrawl-py"
    }))
    sys.exit(1)
```

## Formatting Rules

| Element | Style | Example |
|---------|-------|---------|
| Indentation | 4 spaces (no tabs) | `def main():` |
| Line length | ~100 chars (soft limit) | Keep reasonable |
| Quotes | Double quotes | `"string"` |
| Trailing commas | Use in multi-line structures | `{"key": "value",}` |

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files | `snake_case.py` | `scrape.py`, `web_search.py` |
| Functions | `snake_case()` | `def fetch_data():` |
| Variables | `snake_case` | `api_key`, `result_data` |
| Constants | `UPPER_SNAKE_CASE` | `DEFAULT_TIMEOUT` |

## Argument Parsing

Use `argparse` with clear help text:

```python
parser = argparse.ArgumentParser(
    description="Clear one-line description of what this script does",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  %(prog)s "https://example.com"
  %(prog)s "https://example.com" --format html --output result.json
    """,
)

parser.add_argument(
    "url",
    help="URL to scrape"
)

parser.add_argument(
    "--format",
    default="markdown",
    choices=["markdown", "html"],
    help="Output format (default: markdown)"
)
```

## Error Handling

**Always output JSON** for consistency with automation tools:

### Success Output

```python
try:
    result = perform_operation()
    print(json.dumps({
        "success": True,
        "data": result
    }, indent=2, default=str))
except Exception as e:
    print(json.dumps({
        "success": False,
        "error": str(e)
    }))
    sys.exit(1)
```

### Key Principles

1. **All stdout is JSON** - No plain text output
2. **Check environment variables early** - Before main logic
3. **Exit with code 1 on errors** - Proper error signaling
4. **Use `default=str` in `json.dumps()`** - Handle non-serializable objects (datetime, etc.)

### Environment Variable Checking

```python
def main():
    # Check required environment variables first
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print(json.dumps({
            "success": False,
            "error": "FIRECRAWL_API_KEY environment variable not set"
        }))
        sys.exit(1)
    
    # Continue with main logic...
```

## Complete Example

```python
#!/usr/bin/env python3
"""
Scrape a webpage and extract content.

Usage:
    ./scrape.py "https://example.com"
    ./scrape.py "https://example.com" --format html
"""

import argparse
import json
import os
import sys

try:
    from firecrawl import FirecrawlApp
except ImportError:
    print(json.dumps({
        "success": False,
        "error": "firecrawl-py not installed. Run: pip install firecrawl-py"
    }))
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Scrape webpage content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://example.com"
  %(prog)s "https://example.com" --format html
        """,
    )
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "html"],
        help="Output format (default: markdown)",
    )
    
    args = parser.parse_args()
    
    # Check environment variables
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print(json.dumps({
            "success": False,
            "error": "FIRECRAWL_API_KEY environment variable not set"
        }))
        sys.exit(1)
    
    try:
        app = FirecrawlApp(api_key=api_key)
        result = app.scrape_url(args.url, formats=[args.format])
        
        print(json.dumps({
            "success": True,
            "data": result,
        }, indent=2, default=str))
        
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e),
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
```
