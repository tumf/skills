# Documentation Standards

## SKILL.md Format

Each skill must have a `SKILL.md` file with YAML frontmatter followed by markdown content.

### Structure

```yaml
---
name: skill-name
description: |
  Multi-line description explaining what the skill does,
  when to use it, and what capabilities it provides.
  Be clear and concise.
---

# Skill Name

[Detailed markdown documentation follows here]
```

### YAML Frontmatter Rules

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Kebab-case skill name (e.g., `web-scraping`) |
| `description` | string | Yes | Multi-line description with pipe `|` |

### Content Structure

After the frontmatter, include:

1. **H1 Title** - Skill name
2. **Installation** - Dependencies and setup
3. **Usage** - How to use the skill
4. **Examples** - Practical usage examples
5. **Reference** - Detailed command/API reference

## README.md Format

User-facing documentation that provides complete information about the skill.

Best practice: keep `README.md` user-facing. Put contributor/developer workflow details in `CONTRIBUTING.md`.

### Required Sections

```markdown
# Skill Name

Brief one-paragraph overview of the skill.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

### Prerequisites

List required tools, accounts, API keys.

### Setup

\`\`\`bash
# Step-by-step installation commands
pip install package-name
export API_KEY="your-key"
\`\`\`

## Quick Start

\`\`\`bash
# Simplest possible example
./scripts/example.py "basic input"
\`\`\`

## Usage

### Command Reference

Detailed documentation of all commands and options.

## Examples

### Example 1: Simple Use Case

\`\`\`bash
./scripts/command.py "input"
\`\`\`

### Example 2: Advanced Use Case

\`\`\`bash
./scripts/command.py "input" --option value
\`\`\`

## Configuration

Environment variables and configuration options.

## Tips & Best Practices

- Tip 1
- Tip 2

## Troubleshooting

Common issues and solutions.

## License

MIT License
```

## Markdown Style Guide

### Code Blocks

Use fenced code blocks with language hints:

````markdown
```bash
./scripts/scrape.py "https://example.com"
```

```python
from firecrawl import FirecrawlApp
```

```json
{
  "success": true,
  "data": {}
}
```
````

### Inline Code

Use backticks for:
- Commands: `` `./scripts/scrape.py` ``
- File names: `` `SKILL.md` ``
- Variable names: `` `api_key` ``
- Short code snippets: `` `import json` ``

### Emphasis

| Style | Usage | Example |
|-------|-------|---------|
| **Bold** | Important terms, warnings | **Required:** API key |
| *Italic* | Subtle emphasis | *optional* parameter |
| `Code` | Commands, variables, files | `SKILL.md` |

### Lists

**Unordered lists** for features, tips:
```markdown
- Feature 1
- Feature 2
  - Sub-feature 2a
  - Sub-feature 2b
```

**Ordered lists** for sequential steps:
```markdown
1. First step
2. Second step
3. Third step
```

### Tables

Use tables for structured comparisons:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
```

### Line Length

- Keep lines under ~100 characters for readability
- Break long sentences at natural points
- Code blocks can exceed this limit

### Headings

```markdown
# H1 - Document title only
## H2 - Main sections
### H3 - Subsections
#### H4 - Rarely needed
```

## Examples Section Best Practices

1. **Start simple** - Basic example first
2. **Build complexity** - Gradually add advanced features
3. **Include output** - Show expected results
4. **Explain why** - Comment on what each example demonstrates

### Good Example

````markdown
## Examples

### Basic Scraping

Extract content from a single webpage:

\`\`\`bash
./scripts/scrape.py "https://example.com"
\`\`\`

**Output:**
\`\`\`json
{
  "success": true,
  "data": {
    "markdown": "# Example Page\n\nContent..."
  }
}
\`\`\`

### Advanced: Custom Format

Get HTML instead of markdown:

\`\`\`bash
./scripts/scrape.py "https://example.com" --format html
\`\`\`

This is useful when you need to preserve exact HTML structure.
````

## Documentation Checklist

Before committing documentation:

```
[ ] SKILL.md has proper YAML frontmatter
[ ] README.md includes all required sections
[ ] Code blocks have language hints
[ ] Examples show both input and expected output
[ ] All commands are tested and work
[ ] Environment variables are documented
[ ] Installation steps are complete
[ ] Troubleshooting section addresses common issues
```
