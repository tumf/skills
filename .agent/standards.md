# Project Standards

## JSON Output Standard

All Python scripts **must** output JSON to stdout for consistent parsing by AI agents and automation tools.

### Success Response

```json
{
  "success": true,
  "data": {
    "key": "value"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### Implementation

```python
import json
import sys

try:
    # Main logic
    result = perform_operation()
    
    # Always output JSON on success
    print(json.dumps({
        "success": True,
        "data": result,
    }, indent=2, default=str))
    
except Exception as e:
    # Always output JSON on error
    print(json.dumps({
        "success": False,
        "error": str(e),
    }))
    sys.exit(1)
```

### Non-Serializable Objects

Use `default=str` to handle objects that can't be serialized directly:

```python
from datetime import datetime

data = {
    "timestamp": datetime.now(),  # Not JSON serializable
    "name": "Example"
}

# This works with default=str
print(json.dumps(data, indent=2, default=str))
```

### Why This Matters

1. **Consistency** - All scripts have the same output format
2. **Automation** - Easy to parse in shell scripts and other tools
3. **AI Agents** - Agents can reliably process results
4. **Error Handling** - Standardized error format across all scripts

## Environment Variables

### Storage Rules

| Type | Storage | Committed? | Example |
|------|---------|------------|---------|
| API Keys | `.env` file | **Never** | `FIRECRAWL_API_KEY=abc123` |
| Secrets | `.env` file | **Never** | `DATABASE_PASSWORD=secret` |
| Configuration | `.env` or script args | **Never** | `API_TIMEOUT=30` |
| Defaults | Script code | Yes | `DEFAULT_FORMAT="markdown"` |

### .env File Format

```bash
# API Keys
FIRECRAWL_API_KEY="your-api-key-here"
OPENAI_API_KEY="your-openai-key"

# Configuration
API_TIMEOUT=60
MAX_RETRIES=3
```

### Loading in Scripts

```python
import os

# Check if variable is set
api_key = os.getenv("FIRECRAWL_API_KEY")
if not api_key:
    print(json.dumps({
        "success": False,
        "error": "FIRECRAWL_API_KEY environment variable not set"
    }))
    sys.exit(1)

# Get with default value
timeout = int(os.getenv("API_TIMEOUT", "30"))
```

### Documentation Requirements

Every skill's README.md must document required environment variables:

```markdown
## Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `FIRECRAWL_API_KEY` | Yes | Firecrawl API key | `fc-abc123...` |
| `API_TIMEOUT` | No | Request timeout in seconds | `60` |

### Setup

\`\`\`bash
export FIRECRAWL_API_KEY="your-api-key-here"
export API_TIMEOUT="60"
\`\`\`
```

### Security Best Practices

1. **Never commit** `.env` files
2. **Add to .gitignore**: `echo ".env" >> .gitignore`
3. **Check early** - Validate environment variables before main logic
4. **Clear errors** - Explain which variable is missing and where to get it
5. **Use .env.example** - Provide template without real values

```bash
# .env.example (safe to commit)
FIRECRAWL_API_KEY="your-key-here"
API_TIMEOUT="30"
```

## File Naming Conventions

### Directories

| Type | Convention | Example |
|------|------------|---------|
| Skills | `kebab-case` | `web-scraping/`, `data-extraction/` |
| Hidden dirs | `.lowercase` | `.agent/`, `.github/` |

### Files

| Type | Convention | Example |
|------|------------|---------|
| Python scripts | `snake_case.py` | `scrape.py`, `web_search.py` |
| Documentation | `UPPERCASE.md` or `lowercase.md` | `README.md`, `SKILL.md` |
| Config | `lowercase` or `.lowercase` | `.env`, `.gitignore` |

### Script Names

Choose descriptive, action-oriented names:

```bash
# Good
scrape.py          # Clear action
search.py          # Clear action
crawl.py           # Clear action

# Avoid
script.py          # Too generic
utils.py           # Not action-oriented
helper.py          # Unclear purpose
```

## License

This project uses the **MIT License**.

### License File

Every repository must include a `LICENSE` file in the root:

```
MIT License

Copyright (c) [year] [copyright holders]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[... full MIT License text ...]
```

### File Headers

No need to add license headers to individual files - the repository-level LICENSE file covers all code.

## Code Organization

### Directory Structure Per Skill

```
skill-name/
├── SKILL.md              # Agent instructions
├── README.md             # User documentation
└── scripts/              # Executable scripts only
    ├── script1.py
    └── script2.py
```

**Rules:**
- One skill = one directory
- Scripts go in `scripts/` subdirectory
- No nested subdirectories (keep flat)
- No test files (use docstrings and examples instead)

### Import Organization

```python
# 1. Shebang
#!/usr/bin/env python3

# 2. Module docstring
"""Script description"""

# 3. Standard library (alphabetical)
import argparse
import json
import os
import sys

# 4. Third-party (in try/except)
try:
    from firecrawl import FirecrawlApp
except ImportError:
    print(json.dumps({
        "success": False,
        "error": "Missing dependency"
    }))
    sys.exit(1)
```

## Version Control

### .gitignore

Minimum required entries:

```gitignore
# Environment variables (secrets)
.env

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### What to Commit

| Type | Commit? | Reason |
|------|---------|--------|
| `.py` scripts | Yes | Source code |
| `.md` docs | Yes | Documentation |
| `LICENSE` | Yes | Legal requirement |
| `.gitignore` | Yes | Defines excluded files |
| `.env` | **No** | Contains secrets |
| `__pycache__/` | **No** | Generated files |
| `.DS_Store` | **No** | OS-specific |

### Commit Frequency

- Commit after each complete feature/fix
- Don't commit broken code
- Commit documentation with related code changes
- Group related changes in one commit

## Script Portability

Scripts should work across environments:

### Shebang

```python
#!/usr/bin/env python3
```

**Why:** Uses `env` to find Python, works on different systems

### File Paths

```python
# Good - works everywhere
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")

# Avoid - assumes Unix
config_path = "/usr/local/config.json"
```

### Line Endings

Git should handle this automatically, but prefer LF (`\n`) over CRLF (`\r\n`).

### Dependencies

Document all dependencies in README.md:

```markdown
## Installation

### Prerequisites

- Python 3.7+
- pip

### Dependencies

\`\`\`bash
pip install firecrawl-py requests
\`\`\`
```
