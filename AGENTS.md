# Agent Development Guidelines

## Project Overview

This is a collection of skills for AI coding agents following the [Agent Skills](https://agentskills.io/) format.
Each skill provides executable scripts and documentation for specific capabilities like web scraping, data extraction, etc.

## Repository Structure

```
skills/
├── README.md              # Main documentation
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
└── {skill-name}/         # Individual skill directories
    ├── SKILL.md          # Agent instructions (YAML frontmatter + docs)
    ├── README.md         # Full documentation for users
    └── scripts/          # Executable Python scripts
```

## Build/Test Commands

### Running Scripts

All scripts are executable Python files located in `{skill}/scripts/`:

```bash
# Make scripts executable (if needed)
chmod +x {skill}/scripts/*.py

# Run a script
./{skill}/scripts/{script-name}.py [arguments]

# Example: Scrape a webpage
./firecrawl/scripts/scrape.py "https://example.com"

# Example: Run web search
./firecrawl/scripts/search.py "AI research papers" --limit 5
```

### Testing Individual Scripts

```bash
# Test with help flag to verify script is working
./firecrawl/scripts/scrape.py --help

# Run with minimal arguments to test functionality
./firecrawl/scripts/scrape.py "https://example.com"

# Check error handling (missing API key)
unset FIRECRAWL_API_KEY
./firecrawl/scripts/scrape.py "https://example.com"
```

### Environment Setup

```bash
# Install Python dependencies for a skill
pip install firecrawl-py  # For firecrawl skill

# Set required environment variables
export FIRECRAWL_API_KEY="your-api-key-here"
```

## Code Style Guidelines

### Python Scripts

#### File Structure

1. **Shebang**: Always start with `#!/usr/bin/env python3`
2. **Docstring**: Multi-line module docstring with usage and examples
3. **Imports**: Standard library first, then third-party (alphabetical within groups)
4. **Main function**: Business logic in `main()` function
5. **Entry point**: `if __name__ == "__main__":` at bottom

#### Import Style

```python
# Standard library imports
import argparse
import json
import os
import sys

# Third-party imports (imported inside try/except for error handling)
try:
    from firecrawl import FirecrawlApp
except ImportError:
    # Handle gracefully with JSON error output
    print(json.dumps({"success": False, "error": "..."}))
    sys.exit(1)
```

#### Formatting

- **Indentation**: 4 spaces (no tabs)
- **Line length**: Keep reasonable (~100 chars), but not strict
- **Quotes**: Use double quotes for strings
- **Trailing commas**: Use in multi-line dicts/lists for cleaner diffs

#### Naming Conventions

- **Files**: `snake_case.py` (e.g., `scrape.py`, `search.py`)
- **Functions**: `snake_case()` (e.g., `def main():`)
- **Variables**: `snake_case` (e.g., `api_key`, `result`)
- **Constants**: Not used extensively, but would be `UPPER_SNAKE_CASE`

#### Argument Parsing

Use `argparse` with:
- Clear description
- `RawDescriptionHelpFormatter` for multi-line epilog
- Helpful epilog with examples
- Descriptive help text for each argument

```python
parser = argparse.ArgumentParser(
    description="Clear one-line description",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  %(prog)s "https://example.com"
  %(prog)s "https://example.com" --format html
    """,
)
```

#### Error Handling

**Always** output JSON for consistency:

```python
try:
    # Main logic
    result = do_something()
    print(json.dumps({"success": True, "data": result}, indent=2, default=str))
except Exception as e:
    print(json.dumps({"success": False, "error": str(e)}))
    sys.exit(1)
```

**Key principles**:
- All output to stdout is JSON
- Check environment variables early
- Exit with code 1 on errors
- Use `default=str` in `json.dumps()` for non-serializable objects

### Documentation Files

#### SKILL.md Format

```yaml
---
name: skill-name
description: |
  Multi-line description explaining what the skill does
  and when to use it.
---

# Skill Name

[Markdown content with installation, usage, examples]
```

#### README.md Format

- Start with H1 title
- Include sections: Features, Installation, Quick Start, Reference, Examples, Tips
- Use code blocks with language hints
- Provide both simple and complex examples
- Include troubleshooting section

#### Markdown Style

- Use fenced code blocks with language: ` ```bash ` or ` ```python `
- Use inline code for commands: `` `./scripts/scrape.py` ``
- Use **bold** for emphasis on important terms
- Keep line length reasonable for readability
- Use tables for structured comparisons

## Creating a New Skill

1. **Create directory**: `mkdir {skill-name}`
2. **Add SKILL.md**: Include YAML frontmatter + instructions
3. **Add README.md**: Full user-facing documentation
4. **Create scripts/**: Executable Python scripts (chmod +x)
5. **Update main README.md**: Add skill to Available Skills section
6. **Follow naming**: Use kebab-case for skill directory names

## Git Workflow

```bash
# Standard commit flow
git add .
git commit -m "feat: add new skill for X"
git push
```

**Commit message format**: `type: description`
- `feat:` - New feature/skill
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks

## File Permissions

All Python scripts must be executable:

```bash
chmod +x scripts/*.py
```

## JSON Output Standard

All Python scripts **must** output JSON to stdout:

```json
{
  "success": true,
  "data": { ... }
}
```

Or on error:

```json
{
  "success": false,
  "error": "Error message"
}
```

This ensures consistent parsing by AI agents and automation tools.

## Environment Variables

- Store in `.env` files (never commit)
- Document required variables in README.md
- Check early in script execution
- Provide clear error messages when missing

## License

All code is MIT licensed. Include LICENSE file in root.
